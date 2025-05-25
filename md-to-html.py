
from bs4 import BeautifulSoup
from pathlib import Path

# Define paths
template_path = Path("template-skeleton.html")
md_dir = Path("content-md")
output_html_path = Path("final-plan-merged.html")

# Load template
with open(template_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# For each <div id="...">, inject content from corresponding .md
for div in soup.select("div[id]"):
    section_id = div.get("id")
    md_file = md_dir / f"{section_id}.md"
    if md_file.exists():
        with open(md_file, "r", encoding="utf-8") as f_md:
            inner_html = BeautifulSoup(f_md.read(), "html.parser")
            div.clear()
            div.append(inner_html)

# Save final HTML
with open(output_html_path, "w", encoding="utf-8") as f_out:
    f_out.write(str(soup))

print(f"✅ Generated: {output_html_path}")
