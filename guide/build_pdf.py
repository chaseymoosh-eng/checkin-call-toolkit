"""Render the guides (Markdown) to styled PDFs with headless Chrome. Run: python3 guide/build_pdf.py"""
import pathlib, re, sys, markdown
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
body { font-family: "Noto Sans", "Segoe UI", Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1d2433; }
h1 { color: #1f4f99; font-size: 24pt; margin: 0 0 6pt; border-bottom: 3px solid #1f4f99; padding-bottom: 6pt; }
h2 { color: #1f4f99; font-size: 16pt; margin: 12pt 0 5pt; break-after: avoid; }
h3 { color: #163a73; font-size: 12.5pt; margin: 12pt 0 4pt; break-after: avoid; }
p, li { orphans: 3; widows: 3; }
hr { border: none; border-top: 1px solid #d6d3cc; margin: 8pt 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 10pt; break-inside: avoid; }
th, td { border: 1px solid #c9c5bb; padding: 4pt 6pt; vertical-align: top; text-align: left; }
th { background: #e6eefb; }
blockquote { margin: 8pt 0; padding: 8pt 12pt; background: #f7f5f0; border-left: 4px solid #1f4f99; border-radius: 4px; }
blockquote p { margin: 4pt 0; }
code { font-size: 9.5pt; }
a { color: #1f4f99; word-break: break-word; }
.page-break { break-before: page; }
.card-ref { border: 2px solid #1f4f99; border-radius: 10px; padding: 10pt 16pt; font-size: 11pt; line-height: 1.45; }
.card-ref p { margin: 4pt 0; } .card-ref ol { margin: 2pt 0; padding-left: 16pt; } .card-ref li { margin: 1pt 0; }
.crisis-box { border: 3px solid #b3261e; background: #fde9e7; border-radius: 8px; padding: 4pt 10pt; margin: 6pt 0; break-inside: avoid; }
.crisis-box strong { color: #8c1d18; }
.footer-note { color: #4a5568; font-size: 9pt; }
.sources { font-size: 8.8pt; line-height: 1.35; } .sources li { margin: 2pt 0; }
"""

def build(md_name):
    src = (HERE / md_name).read_text(encoding="utf-8")
    src = re.sub(r"^---\n.*?\n---\n", "", src, flags=re.S)
    title = re.search(r"^# (.+)$", src, flags=re.M).group(1)
    body = markdown.markdown(src, extensions=["tables", "md_in_html", "sane_lists"])
    html = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"
    out_html = HERE / (md_name[:-3] + ".html"); out_html.write_text(html, encoding="utf-8")
    out_pdf = HERE / (md_name[:-3] + ".pdf")
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome"); pg = b.new_page()
        pg.goto(out_html.as_uri()); pg.emulate_media(media="print")
        pg.pdf(path=str(out_pdf), format="A4", print_background=True, display_header_footer=True,
               header_template="<div></div>",
               footer_template=f"<div style='font-size:8pt;color:#666;width:100%;text-align:center'>{title} · page <span class='pageNumber'></span> of <span class='totalPages'></span></div>",
               margin={"top": "16mm", "bottom": "18mm", "left": "16mm", "right": "16mm"})
        b.close()
    out_html.unlink()
    print("wrote", out_pdf)

for name in (sys.argv[1:] or ["volunteer-training-guide.md", "coordinator-setup-guide.md"]):
    if (HERE / name).exists(): build(name)
