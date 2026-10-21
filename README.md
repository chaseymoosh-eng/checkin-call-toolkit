# Check-in Call Toolkit (v1)

A free, simple toolkit for **small charities, community groups, faith groups, libraries, and neighbour networks** that want to run **regular volunteer check-in phone calls** for people who feel lonely or isolated.

It's built around the model with the strongest evidence we found: **short, regular phone calls by briefly trained volunteers who listen with empathy and let the person lead the conversation.** In a randomized trial with 240 Meals on Wheels clients, 4 weeks of such calls reduced loneliness, depression and anxiety compared with no calls (Kahlon et al., *JAMA Psychiatry*, 2021).

> **This is a friendly-call program, not therapy, counselling, or a crisis service.** Every part of the toolkit says so, and includes a clear crisis protocol. If someone is in danger, call the local emergency number. Crisis lines to offer: **988** in the US, **Samaritans 116 123** in the UK and Ireland, and [findahelpline.com](https://findahelpline.com) elsewhere.

**Live site:** <https://chaseymoosh-eng.github.io/checkin-call-toolkit/>

## What's inside

| Path | What it is |
|---|---|
| `index.html` | Landing page for the website, with a link to the app, the guides, and the privacy note. |
| `app/index.html` | The organizer web app. One file, no install, works offline. Open it in any modern browser. |
| `guide/volunteer-training-guide.md` / `.pdf` | 10-page training guide for volunteers, with call scripts, the crisis protocol, and a one-page quick-reference card (last page). |
| `guide/coordinator-setup-guide.md` / `.pdf` | How to start a program in a few weeks: recruiting, consent script, matching, a 2-hour training agenda, running the program, measuring results, and using the app. |
| `guide/build_pdf.py` | Rebuilds the PDFs from the Markdown (uses headless Chrome via Playwright). |
| `tests/test_app.py` | Automated browser test of the app (27 checks), which also regenerates the screenshots. |
| `screenshots/` | Screenshots of each view with sample data (1280×800, plus full-page and mobile versions). |
| `LICENSE` | MIT license for the code. |
| `LICENSE-content` | CC BY 4.0 notice for the guides and other written content. |

## How to use it

The published website is <https://chaseymoosh-eng.github.io/checkin-call-toolkit/>. GitHub Pages serves this repository from the `main` branch. The same files work if you download the repository and open them on your own computer. Either way, call records stay in that browser.

**On the website**

1. Open <https://chaseymoosh-eng.github.io/checkin-call-toolkit/> and click **Open the app**, or go straight to <https://chaseymoosh-eng.github.io/checkin-call-toolkit/app/>.
2. Click **Load sample data** to explore with made-up people. Then use **Settings & data → Clear all data** when you're ready to start for real.
3. In **Settings**, enter your organization, coordinator contact, and **local crisis numbers**. The defaults are examples: 988 (US), Samaritans 116 123 (UK & Ireland), and findahelpline.com for everywhere else.
4. Add **Volunteers** and **Participants** (record consent), then create **Pairings** with call days and times. Calls appear in **Upcoming calls** automatically.
5. From the landing page, download the coordinator guide and share the volunteer guide before training (PDF or Markdown).

**From a copy of the files**

1. Open `app/index.html` in Chrome, Edge, Firefox, or Safari (double-click it). No internet connection is required.
2. Follow steps 2–4 above.
3. Read `guide/coordinator-setup-guide.pdf` (or the Markdown file). Share `guide/volunteer-training-guide.pdf` with volunteers before training.

The landing page (`index.html`) also links to both guides.

## App features

- **Volunteers:** contact details, availability, training completed (with date), checks/references, active or inactive.
- **Participants:** phone, preferred days/times, time zone (shows "their time" when it differs from yours), language, emergency contact, notes, consent recorded (with date), program start date, status (active / paused / ended).
- **Pairings:** volunteer ↔ participant on a recurring schedule (any days of the week, every week or every other week, with time and start/end dates).
- **Upcoming calls:** generated from the schedules for the next 14 days. **Today is highlighted in yellow; overdue or unlogged calls from the past 14 days are shown in red.** You can print a call sheet.
- **Call log:** outcome (completed / no answer / rescheduled, which adds a one-off call), length, mood check (1–5 with emoji), short notes, and a **concern flag: none / follow-up needed / urgent.** Choosing **Urgent** shows the crisis protocol right in the form, and a red banner with the protocol and crisis numbers stays at the top of every page until the concern is resolved.
- **Concerns dashboard:** open concerns (urgent first) with the participant's phone and emergency contact, resolution notes, mark resolved, and reopen.
- **Stats:** calls completed this week and month, missed-call rate (last 30 days), active participants and volunteers, average call length and mood, calls per volunteer, and an optional **3-item UCLA Loneliness Scale** (Hughes et al., 2004) at start and end, with change scores.
- **Always-visible "⚠️ Crisis protocol" button** in the header.
- **Settings:** organization name, coordinator contact, safeguarding contact, emergency instruction, editable crisis lines.
- **Data:** stored only in this browser (localStorage). **JSON backup export/import**, **CSV export** of the call log (protected against spreadsheet formula injection), backup reminder, **Load sample data**, and **Clear all data** (double confirmation).
- **Accessible design:** 18px base text, high contrast, large touch targets, visible focus, labelled form fields, keyboard-friendly dialogs, and a responsive mobile layout. All user-entered text is HTML-escaped.

## Privacy

All data stays **on the device where the app is used**. Nothing is uploaded, and no account is needed. That is true on the live website as well as when you open the file locally: the app does not send records anywhere. Use a password-protected device, don't use shared computers, and export backups regularly (backup files contain personal details, so store them securely). Clearing browser data or using private browsing will erase the records.

## Testing

```bash
pip install playwright        # uses the system Google Chrome (channel="chrome")
python3 tests/test_app.py     # 27 checks; writes screenshots/
python3 guide/build_pdf.py    # rebuilds both PDFs
```

The test opens the app headlessly and checks: no JS errors; the empty state; adding a volunteer, participant and pairing generates the expected upcoming calls with today highlighted; logging an **urgent** concern shows the crisis panel in the form, then the banner (with 988, 116 123 and findahelpline.com), and lists it on the Concerns dashboard; resolving clears the banner; rescheduling adds a one-off call; the UCLA score is recorded; settings save; CSV/JSON export, clear and import work; HTML in names is escaped; sample data loads; and there's no horizontal overflow on mobile.

## Known limitations (v1)

- **Single device, no sync.** Data lives in one browser. Several volunteers can't share one live dataset; the guide recommends the coordinator keep the app and volunteers report calls by phone or text.
- **No reminders.** It doesn't send texts, emails or notifications.
- **No login or encryption** beyond the device's own protection. Anyone with access to the unlocked device and browser can see the data.
- **Times use the device's time zone.** The participant's local time is shown as a hint only.
- **Browser storage limits** (usually around 5 MB) are plenty for a small program, but not for years of records.
- **English only.**
- The guides are general. They are not legal or clinical advice. Groups should check local safeguarding, volunteer-check and data-protection requirements, and ideally have the crisis protocol reviewed by someone with local safeguarding experience.

## Suggested next steps

1. **Pilot with one local group**: 3–5 volunteers, 5–10 participants, 4 weeks. Interview the coordinator before and after, as the research brief suggested.
2. **Add an offline-install (PWA) manifest** so the published site can be installed and opened like an app. The site is already at <https://chaseymoosh-eng.github.io/checkin-call-toolkit/>, and data still stays on each user's device.
3. **Translations** of the app and guides (Spanish, French, Portuguese, Arabic, Hindi…), reviewed by native speakers, plus a language switcher.
4. **Optional sync for multi-volunteer groups**, e.g. an end-to-end-encrypted shared file, or a small self-hosted backend. Only consider this after the pilot shows a real need.
5. **Calendar (.ics) export and reminder texts** for volunteers.
6. **Safeguarding review** of the guides by a befriending or safeguarding professional; add country-specific crisis-line presets.
7. **Licenses are in place:** MIT for the code (`LICENSE`) and CC BY 4.0 for the guides and other written content (`LICENSE-content`).

## License

- **Code** — the app (`app/`), the tests (`tests/`), `guide/build_pdf.py`, and the landing page markup and styles — is licensed under the [MIT License](LICENSE). Copyright 2026 chaseymoosh-eng.
- **Guides and other written content** — the volunteer training guide, the coordinator setup guide (Markdown and PDF), and the written prose of this README and the landing page — are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). See [LICENSE-content](LICENSE-content). You may share and adapt that writing if you give appropriate credit, link to the license, and note any changes.

## Sources

- Kahlon MK, Aksan N, Aubrey R, et al. Effect of layperson-delivered, empathy-focused program of telephone calls on loneliness, depression, and anxiety among adults during the COVID-19 pandemic: a randomized clinical trial. *JAMA Psychiatry*. 2021;78(6):616–622. doi:10.1001/jamapsychiatry.2021.0113
- Hughes ME, Waite LJ, Hawkley LC, Cacioppo JT. A short scale for measuring loneliness in large surveys: results from two population-based studies. *Research on Aging*. 2004;26(6):655–672. doi:10.1177/0164027504268574
- Lasgaard M, Qualter P, Løvschall C, et al. Are loneliness interventions effective for reducing loneliness? A meta-analytic review of 280 studies. *American Psychologist*. 2026;81(1):36–52. doi:10.1037/amp0001578
- Carr DC, Kail BL, Matz-Costa C, Shavit YZ. Does becoming a volunteer attenuate loneliness among recently widowed older adults? *J Gerontol B*. 2018;73(3):501–510. doi:10.1093/geronb/gbx092
- World Health Organization, Commission on Social Connection (2025); 988 Suicide & Crisis Lifeline, "Help Someone Else"; Samaritans; Age UK telephone befriending; Find A Helpline. Links are in the guides.
