import os
import datetime
from pathlib import Path

# === CONFIGURATION ===
BASE_DIR = Path(__file__).resolve().parent
CONTENT_DIR = BASE_DIR / "content"
TEMPLATE_FILE = BASE_DIR / "templates" / "gpt-template-skeleton.html"
CSS_FILE = BASE_DIR / "assets" / "gpt-trip-style.css"
JS_FILE = BASE_DIR / "assets" / "gpt-trip-script.js"
BUILD_DIR = BASE_DIR / "../build"

# === MINIMAL MD TO HTML ===
def md_to_html(md_text):
    import re
    lines = md_text.splitlines()
    html = []
    in_ul = False
    for line in lines:
        line = line.strip()
        if line.startswith("# "): html.append(f"<h1>{line[2:]}</h1>"); continue
        if line.startswith("## "): html.append(f"<h2>{line[3:]}</h2>"); continue
        if line.startswith("### "): html.append(f"<h3>{line[4:]}</h3>"); continue
        if line.startswith("- "):
            if not in_ul:
                html.append("<ul>")
                in_ul = True
            html.append(f"<li>{line[2:]}</li>")
            continue
        if in_ul:
            html.append("</ul>")
            in_ul = False
        line = re.sub(r"\*\*(.*?)\*\*", r"<strong>\\1</strong>", line)
        line = re.sub(r"\*(.*?)\*", r"<em>\\1</em>", line)
        html.append(f"<p>{line}</p>")
    if in_ul:
        html.append("</ul>")
    return "\n".join(html)

# === MAIN FUNCTION ===
def generate():
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    css_inline = CSS_FILE.read_text(encoding="utf-8")
    js_inline = JS_FILE.read_text(encoding="utf-8")

    # Inject CSS/JS inline
    template = template.replace("<!-- INLINE_CSS -->", f"<style>\n{css_inline}\n</style>")
    template = template.replace("<!-- INLINE_JS -->", f"<script>\n{js_inline}\n</script>")

    # Fill in Markdown contents
    for md_file in CONTENT_DIR.glob("*.md"):
        section_id = md_file.stem.lower()
        html_block = md_to_html(md_file.read_text(encoding="utf-8"))
        template = template.replace(f'<section id="{section_id}"></section>', f'<section id="{section_id}">\n{html_block}\n</section>')

    # Save output file
    today = datetime.date.today().strftime("%Y%m%d")
    out_path = BUILD_DIR / f"Tokyo-Trip-March-2026-GPT-{today}.html"
    out_path.write_text(template, encoding="utf-8")
    print(f"✅ Generated: {out_path}")

if __name__ == "__main__":
    generate()
