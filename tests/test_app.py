"""Headless browser test for app/index.html. Run: python3 tests/test_app.py"""
import json, pathlib, sys, datetime
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / "app" / "index.html").as_uri()
SHOTS = ROOT / "screenshots"; SHOTS.mkdir(exist_ok=True)
errors, results = [], []

def check(name, cond):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800}, accept_downloads=True)
    page = ctx.new_page()
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("dialog", lambda d: d.accept("DELETE") if d.type == "prompt" else d.accept())
    page.goto(URL)
    check("empty state shows welcome", page.locator("text=Let's set up your first check-in calls").count() == 1)

    # --- add volunteer
    page.goto(URL + "#volunteers"); page.click("[data-action=add-volunteer]")
    page.fill("#f_name", "Test Volunteer"); page.fill("#f_phone", "555-0199")
    page.check("#f_trained"); page.click("#dlgSubmit")
    check("volunteer added", page.locator(".card h3", has_text="Test Volunteer").count() == 1)

    # --- add participant
    page.goto(URL + "#participants"); page.click("[data-action=add-participant]")
    page.fill("#f_name", "Test Participant"); page.fill("#f_phone", "555-0198"); page.check("#f_consent")
    page.click("#dlgSubmit")
    check("participant added", page.locator(".card h3", has_text="Test Participant").count() == 1)

    # --- pairing on today's weekday + 3 days later
    wd = (datetime.date.today().isoweekday()) % 7  # JS getDay
    wd2 = (wd + 3) % 7
    page.goto(URL + "#pairings"); page.click("[data-action=add-pairing]")
    page.select_option("#f_volunteerId", label="Test Volunteer")
    page.select_option("#f_participantId", label="Test Participant")
    page.check(f"input[name=days][value='{wd}']"); page.check(f"input[name=days][value='{wd2}']")
    page.fill("#f_time", "23:59")
    page.click("#dlgSubmit")
    check("pairing row created", page.locator("tbody tr").count() == 1)

    page.goto(URL + "#upcoming")
    n_slots = page.locator(".slot").count()
    check(f"upcoming calls generated ({n_slots} slots in 14 days, expect 4)", n_slots == 4)
    check("today's call highlighted", page.locator(".slot.today").count() == 1)

    # --- log urgent concern on today's call
    page.click(".slot.today [data-action=log-slot]")
    page.check("input[name=outcome][value=completed]")
    check("crisis panel hidden before urgent", not page.locator("#dlgBody .crisis").is_visible())
    page.check("input[name=concernLevel][value=urgent]")
    check("crisis panel shown in form when urgent selected", page.locator("#dlgBody .crisis").is_visible())
    page.fill("#f_duration", "12"); page.check("input[name=mood][value='2']")
    page.fill("#f_concernText", "Test: said they did not want to be here any more.")
    page.screenshot(path=str(SHOTS / "07-log-call-urgent-form.png"))
    page.click("#dlgSubmit")
    banner = page.locator("#urgentBanner")
    check("urgent banner visible", banner.is_visible())
    check("banner shows crisis lines (988 / 116 123 / findahelpline)", all(s in banner.inner_text() for s in ["988", "116 123", "findahelpline.com"]))
    check("today's slot now marked done", page.locator(".slot.done").count() == 1)
    page.screenshot(path=str(SHOTS / "08-urgent-banner.png"))
    page.goto(URL + "#concerns")
    check("concern listed on dashboard", page.locator(".card.concern", has_text="Test Participant").count() == 1)
    check("nav badge shows 1 open concern", "1" in page.locator("nav a[href='#concerns']").inner_text())
    page.fill(".card.concern textarea", "Coordinator called them back; they called the crisis line together.")
    page.click("[data-action=resolve]")
    check("banner cleared after resolve", not page.locator("#urgentBanner").is_visible())
    check("resolved list shows resolution", "crisis line together" in page.text_content("details"))

    # --- reschedule creates one-off
    page.goto(URL + "#upcoming")
    page.locator(".slot [data-action=log-slot]").first.click()
    page.check("input[name=outcome][value=rescheduled]")
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    page.fill("#f_newDate", tomorrow); page.fill("#f_newTime", "11:00"); page.click("#dlgSubmit")
    check("rescheduled call adds one-off slot", page.locator(".slot", has_text="one-off").count() == 1)

    # --- UCLA
    page.goto(URL + "#stats"); page.click("[data-action=add-ucla]")
    page.select_option("#f_participantId", label="Test Participant")
    for q, v in (("q1", "3"), ("q2", "2"), ("q3", "3")): page.check(f"input[name={q}][value='{v}']")
    page.click("#dlgSubmit")
    check("UCLA score 8/9 recorded", "8/9" in page.inner_text("main"))

    # --- settings: edit crisis line shows on banner text
    page.goto(URL + "#settings"); page.fill("#s_org", "Test Group"); page.fill("#s_cn", "Coord Test")
    page.click("#settingsForm button[type=submit]")
    check("org name saved in header", page.inner_text("#orgName") == "Test Group")

    # --- exports
    with page.expect_download() as d: page.click("#main [data-action=export-csv]")
    csv = pathlib.Path(d.value.path()).read_text(encoding="utf-8-sig")
    check("CSV export has header + 2 rows", csv.splitlines()[0].startswith("date,time,participant") and len(csv.strip().splitlines()) == 3)
    with page.expect_download() as d: page.click("#main [data-action=export-json]")
    backup = pathlib.Path(d.value.path())
    data = json.loads(backup.read_text())
    check("JSON backup has data", len(data["calls"]) == 2 and data["settings"]["orgName"] == "Test Group")

    # --- clear, then import
    page.goto(URL + "#settings"); page.click("[data-action=clear]")
    check("clear all data empties store", page.evaluate("localStorage.getItem('checkinToolkit.v1')") is None)
    page.goto(URL + "#settings"); page.set_input_files("#importFile", str(backup))
    page.wait_for_timeout(300)
    check("import restores data", page.evaluate("JSON.parse(localStorage.getItem('checkinToolkit.v1')).calls.length") == 2)

    # --- XSS safety: names are escaped
    page.evaluate("""()=>{const d=JSON.parse(localStorage.getItem('checkinToolkit.v1'));d.participants[0].name='<img src=x onerror=window.__x=1>';localStorage.setItem('checkinToolkit.v1',JSON.stringify(d));}""")
    page.goto(URL + "#participants"); page.reload(); page.wait_for_timeout(200)
    check("HTML in names is escaped", page.evaluate("window.__x") is None)

    # --- sample data + screenshots
    page.goto(URL + "#settings"); page.click("[data-action=clear]")
    page.goto(URL + "#upcoming"); page.click("[data-action=sample]"); page.wait_for_timeout(300)
    check("sample data loaded", page.locator(".slot").count() > 5)
    check("sample shows an overdue call", page.locator(".slot.overdue").count() >= 1)
    shots = [("01-upcoming", "upcoming"), ("02-call-log", "log"), ("03-concerns", "concerns"),
             ("04-participants", "participants"), ("05-volunteers", "volunteers"), ("06-pairings", "pairings"),
             ("09-stats", "stats"), ("10-settings", "settings")]
    for name, view in shots:
        page.goto(URL + "#" + view); page.wait_for_timeout(250); page.evaluate("document.getElementById('toast').className=''"); page.wait_for_timeout(250)
        page.screenshot(path=str(SHOTS / f"{name}.png"))
        page.screenshot(path=str(SHOTS / f"{name}-full.png"), full_page=True)
    page.goto(URL + "#upcoming"); page.locator(".slot [data-action=log-slot]").first.click()
    page.check("input[name=outcome][value=completed]")
    page.screenshot(path=str(SHOTS / "11-log-call-form.png")); page.click("[data-action=close-dlg] >> nth=1")
    page.click(".crisis-btn"); page.wait_for_timeout(150)
    page.screenshot(path=str(SHOTS / "12-crisis-protocol-dialog.png")); page.click("#crisisDlg .dlg-foot button")
    # mobile
    m = ctx.new_page(); m.set_viewport_size({"width": 390, "height": 844})
    m.on("pageerror", lambda e: errors.append(str(e)))
    m.goto(URL + "#upcoming"); m.wait_for_timeout(600)
    m.screenshot(path=str(SHOTS / "13-mobile-upcoming.png"))
    check("no horizontal overflow on mobile", m.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"))
    browser.close()

check("no JS errors: " + "; ".join(errors) if errors else "no JS errors", not errors)
failed = [n for n, ok in results if not ok]
print(f"\n{len(results)-len(failed)}/{len(results)} checks passed")
sys.exit(1 if failed else 0)
