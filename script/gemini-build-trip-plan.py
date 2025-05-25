# gemini-build_trip_plan.py
import os
import re
from pathlib import Path
import mistune
from bs4 import BeautifulSoup
from datetime import datetime

# Define paths relative to the script's location
SCRIPT_DIR = Path(__file__).parent
CONTENT_DIR = SCRIPT_DIR.parent / "content"
BUILD_DIR = SCRIPT_DIR.parent / "build"
TEMPLATE_FILE = SCRIPT_DIR / "gemini-template-skeleton.html"

# Ensure build directory exists
BUILD_DIR.mkdir(parents=True, exist_ok=True)


def read_file(filepath):
    """Reads file content and returns as string."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return ""


def markdown_to_html_with_structure(markdown_text):
    """
    Converts markdown to HTML, applying specific structural transformations
    for timelines, info/note boxes, and tables.
    Handles multi-language spans within the converted HTML.
    """
    # Custom renderer for mistune to handle multi-language spans within inline HTML
    class MultiLangRenderer(mistune.HTMLRenderer):
        def block_html(self, html):
            # Allow raw HTML blocks to pass through, useful for language spans
            return html

        def paragraph(self, text):
            # Check if paragraph contains explicit span classes for language
            if '<span class="th"' in text or '<span class="en"' in text or '<span class="jp"' in text:
                return f'<p>{text}</p>\n'
            return super().paragraph(text)

        def list_item(self, text):
            # Check if list item contains explicit span classes for language
            # And also if it's a timeline item's content.
            if '<span class="th-li"' in text or '<span class="en-li"' in text or '<span class="jp-li"' in text:
                # Add a helper class for JS
                return f'<li class="lang-li-auto">{text}</li>\n'
            return super().list_item(text)

    # Initialize mistune with the custom renderer
    renderer = MultiLangRenderer()
    markdown = mistune.Markdown(renderer=renderer)

    # Pre-process markdown for custom blocks (like info/note boxes and timelines)
    def process_custom_boxes(text_content):
        # Pattern for generic custom boxes (info/note) - uses a temporary tag to avoid mistune interference
        # Modified to ensure it captures content until a clear end or new block.
        # It handles titles like "ℹ️ Title" or "Title"
        box_pattern = re.compile(
            # Start of the box, capture type
            r'(?:^|\n)(?P<type>info|note)-box\n'
            # Title in triple backticks OR single line title
            r'(?:```(?P<title>[^`]+)```|(?P<raw_title>[^\n]+))\n'
            r'(?P<content>.+?)'                # Content of the box
            # Lookahead for next box or end of string
            r'(?=\n(?:info|note)-box|\n---|\n\n|\Z)',
            re.DOTALL | re.MULTILINE
        )

        def replace_box_markup(match):
            box_type = match.group('type')
            title_md = match.group('title') if match.group(
                'title') else match.group('raw_title')
            content_md = match.group('content').strip()

            # Convert title and content of the box, preserving language spans
            # For title, ensure it's wrapped in appropriate language spans if detected
            title_html = markdown.inline(title_md.strip())

            # Use BeautifulSoup to correctly parse and extract text from language spans if present
            title_soup = BeautifulSoup(title_html, 'html.parser')
            th_title_span = title_soup.find('span', class_='th')
            en_title_span = title_soup.find('span', class_='en')
            jp_title_span = title_soup.find('span', class_='jp')

            th_title_text = th_title_span.decode_contents().strip(
            ) if th_title_span else title_soup.get_text(strip=True)
            en_title_text = en_title_span.decode_contents().strip(
            ) if en_title_span else th_title_text  # Fallback
            jp_title_text = jp_title_span.decode_contents().strip(
            ) if jp_title_span else th_title_text  # Fallback

            # Ensure the output toggle uses the multi-language span structure
            toggle_html = f'''
                <div class="{box_type}-toggle">
                    <span class="th">{th_title_text}</span>
                    <span class="en">{en_title_text}</span>
                    <span class="jp">{jp_title_text}</span>
                </div>
            '''

            # Parse content fully. Mistune will handle nested markdown.
            box_content_html = markdown.parse(content_md)

            # Remove outer <p> tags if mistune adds them unnecessarily
            box_content_html = re.sub(
                r'^<p>(.*)</p>$', r'\1', box_content_html, flags=re.DOTALL)

            return f'''
<div class="{box_type}-box">
    {toggle_html}
    <div class="{box_type}-detail">
        {box_content_html}
    </div>
</div>
'''

        return box_pattern.sub(replace_box_markup, text_content)

    # Process info/note boxes first, then convert the rest of markdown
    processed_markdown_with_boxes = process_custom_boxes(markdown_text)
    html_content = markdown.parse(processed_markdown_with_boxes)

    # Post-processing with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Process tables for responsive design and custom classes
    for table in soup.find_all('table'):
        # Wrap table in div for responsive design
        table_container = soup.new_tag(
            'div', attrs={'class': 'table-container'})
        table.wrap(table_container)

        # Add classes to rows if they are special (total, remaining)
        for row in table.find_all('tr'):
            cells = row.find_all(['td', 'th'])
            if cells and len(cells) > 0:
                first_cell_text = cells[0].get_text().strip().lower()
                if 'รวม' in first_cell_text or 'total' in first_cell_text:
                    row['class'] = row.get('class', []) + ['total']
                elif 'งบประมาณที่เหลือ' in first_cell_text or 'remaining' in first_cell_text:
                    row['class'] = row.get('class', []) + ['remaining']

    return str(soup)


def create_day_overview_cards(markdown_contents_map):
    """
    Creates day overview cards for the main overview section.
    Expects markdown_contents_map to be a dictionary: {id: content}
    """
    html = '<div class="day-overviews">\n'

    # Filter for day files and sort numerically
    day_ids = sorted([id for id in markdown_contents_map if id.startswith('day')],
                     key=lambda x: int(re.search(r'\d+', x).group()))

    for section_id in day_ids:
        markdown_text = markdown_contents_map[section_id]

        # Extract title line
        title_line_match = re.search(r'##\s+([^\n]+)', markdown_text)
        if not title_line_match:
            print(
                f"Warning: No main title found for {section_id} to create overview card.")
            continue

        title_full = title_line_match.group(1).strip()

        # Extract Thai and English parts of the title line
        thai_title_str = ""
        english_title_str = ""

        # Attempt to parse title in "วันที่ X: Thai Part - English Part" format
        complex_title_match = re.match(
            r'(วันที่\s+\d+:\s*[^-\n]+)\s*-\s*(.+)', title_full)
        if complex_title_match:
            thai_title_str = complex_title_match.group(1).strip()
            english_title_str = complex_title_match.group(2).strip()
        else:
            # Fallback if not in complex format, use full title for both
            thai_title_str = title_full
            english_title_str = title_full

        # Extract the first *meaningful* paragraph as description
        # Find first line that is not a heading, list item, or empty, or image/link related.
        description_th = ""
        description_en = ""

        temp_md_for_desc = ""
        for line in markdown_text.splitlines():
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith(('#', '-', '*', '|', '>')) and not re.match(r'^\d+\.', stripped_line):
                temp_md_for_desc = stripped_line
                break

        if temp_md_for_desc:
            # Process the description line with mistune to handle potential inline markdown (like bold, links)
            processed_desc_html = mistune.html(temp_md_for_desc)
            desc_soup = BeautifulSoup(processed_desc_html, 'html.parser')

            th_span = desc_soup.find('span', class_='th')
            en_span = desc_soup.find('span', class_='en')

            if th_span:
                description_th = th_span.get_text(strip=True)
            else:
                description_th = desc_soup.get_text(
                    strip=True)  # Fallback if no specific span

            if en_span:
                description_en = en_span.get_text(strip=True)
            else:
                description_en = description_th  # Fallback to Thai if no English span

        # Add birthday badge for day 4
        birthday_badge_html = ""
        if section_id == "day4":
            birthday_badge_html = '<span class="birthday-badge">🎂 Happy Birthday!</span>'

        html += f'''
        <div class="day-overview">
            <h3><a href="#{section_id}">
                <span class="th">{thai_title_str}</span>
                <span class="en">{english_title_str}</span>
            </a>{birthday_badge_html}</h3>
            <p>
                <span class="th">{description_th}</span>
                <span class="en">{description_en}</span>
            </p>
        </div>
        '''

    # Add budget overview card manually as it's not a 'day'
    # Check if budget.md exists in the map
    if "budget" in markdown_contents_map:
        budget_md_content = markdown_contents_map["budget"]

        # Extract description from budget.md
        budget_desc_th = "ข้อมูลการจอง และประมาณการค่าใช้จ่าย."
        budget_desc_en = "Booking information and estimated expenses."

        # Attempt to find the first paragraph content for description
        budget_content_soup = BeautifulSoup(
            mistune.html(budget_md_content), 'html.parser')
        first_p_text = ""
        for p_tag in budget_content_soup.find_all('p'):
            if p_tag.get_text(strip=True):
                first_p_text = p_tag.get_text(strip=True)
                break

        if first_p_text:
            # Try to extract Thai/English from the first paragraph of budget
            th_span = budget_content_soup.find('span', class_='th')
            en_span = budget_content_soup.find('span', class_='en')
            if th_span:
                budget_desc_th = th_span.get_text(strip=True)
            else:
                budget_desc_th = first_p_text

            if en_span:
                budget_desc_en = en_span.get_text(strip=True)
            else:
                budget_desc_en = budget_desc_th  # Fallback

        html += f'''
        <div class="day-overview">
            <h3><a href="#budget">
                <span class="th">ประมาณการค่าใช้จ่ายและสถานะ</span>
                <span class="en">Budget Estimate and Status</span>
            </a></h3>
            <p>
                <span class="th">{budget_desc_th}</span>
                <span class="en">{budget_desc_en}</span>
            </p>
        </div>
        '''

    html += '</div> \n'

    return html


def build_full_html_plan():
    """
    Builds the complete HTML trip plan by combining template, markdown content,
    and inlining CSS/JS.
    """
    # 1. Read the refactored template HTML
    template_html_content = read_file(TEMPLATE_FILE)
    template_soup = BeautifulSoup(template_html_content, 'html.parser')

    # 2. Read content from all markdown files
    markdown_contents = {}
    for md_file_path in CONTENT_DIR.glob('*.md'):
        # Use filename as ID, replace underscores with hyphens
        section_id = md_file_path.stem.replace('_', '-')
        markdown_contents[section_id] = read_file(md_file_path)

    # Process each section and inject into the template
    for div_tag in template_soup.select("div[id]"):
        section_id = div_tag.get("id")

        if section_id == "overview":
            # Generate day overview cards and inject
            overview_content_html = create_day_overview_cards(
                markdown_contents)

            # Find the specific div where cards should be injected
            target_div = div_tag.find('div', class_='day-overviews')
            if target_div:
                target_div.clear()  # Clear any placeholder content
                target_div.append(BeautifulSoup(
                    overview_content_html, 'html.parser'))

            # Handle the note-box within overview, which is already static in the template
            # For dynamic note-box/info-box from MD, process_custom_boxes in markdown_to_html_with_structure handles it.

            # Update the main intro paragraph under header
            # The content of 'main_info.md' typically contains this.
            if "main_info" in markdown_contents:
                main_info_md = markdown_contents["main_info"]
                # Extract travelers and route information from main_info.md
                # Assuming format: "✈️ ผู้เดินทาง: 🧍 Arilek (คุณพ่อ) 👧 Nuntnaphat (พอใจ)"
                # "🗺️ เส้นทาง: Narita – Tokyo – Kawaguchiko – Gala Yuzawa – Tokyo"
                travelers_line_match = re.search(r'✈️(.+)', main_info_md)
                route_line_match = re.search(r'🗺️(.+)', main_info_md)

                travelers_th = "ไม่พบข้อมูลผู้เดินทาง"
                travelers_en = "Travelers info not found"
                route_th = "ไม่พบข้อมูลเส้นทาง"
                route_en = "Route info not found"

                if travelers_line_match:
                    # Extract content within the span tags for TH/EN
                    temp_soup_travelers = BeautifulSoup(
                        travelers_line_match.group(1).strip(), 'html.parser')
                    th_span = temp_soup_travelers.find('span', class_='th')
                    en_span = temp_soup_travelers.find('span', class_='en')

                    if th_span:
                        travelers_th = th_span.get_text(
                            strip=True).replace("ผู้เดินทาง: ", "")
                    else:
                        travelers_th = temp_soup_travelers.get_text(
                            strip=True)  # Fallback

                    if en_span:
                        travelers_en = en_span.get_text(
                            strip=True).replace("Travelers: ", "")
                    else:
                        travelers_en = travelers_th  # Fallback

                if route_line_match:
                    temp_soup_route = BeautifulSoup(
                        route_line_match.group(1).strip(), 'html.parser')
                    th_span = temp_soup_route.find('span', class_='th')
                    en_span = temp_soup_route.find('span', class_='en')

                    if th_span:
                        route_th = th_span.get_text(
                            strip=True).replace("เส้นทาง: ", "")
                    else:
                        route_th = temp_soup_route.get_text(
                            strip=True)  # Fallback

                    if en_span:
                        route_en = en_span.get_text(
                            strip=True).replace("Itinerary: ", "")
                    else:
                        route_en = route_th  # Fallback

                intro_p_html = f'''
                <p>
                    <span class="th">✈️ ผู้เดินทาง: {travelers_th}</span><span class="en">✈️ Travelers: {travelers_en}</span><br/>
                    <span class="th">🗺️ เส้นทาง: {route_th}</span><span class="en">🗺️ Itinerary: {route_en}</span>
                </p>
                '''

                # Find the first <p> tag directly after the header for this intro content
                target_p = template_soup.find(
                    'div', class_='container').find('p')
                if target_p:
                    target_p.replace_with(BeautifulSoup(
                        intro_p_html, 'html.parser'))

        elif section_id in markdown_contents:  # For all other content markdown files
            markdown_text = markdown_contents[section_id]

            # Find the main section title from Markdown to build the H1 tag
            section_title_match = re.match(r'#+\s+([^\n]+)', markdown_text)
            title_html_tag = ""
            if section_title_match:
                full_title_line = section_title_match.group(1).strip()

                # Extract Thai and English parts from the full title line
                thai_title_str = ""
                english_title_str = ""

                # Pattern for titles like "Thai Title - English Title" or "วันที่ X: Thai Title - English Title"
                # This should capture "วันที่ X: Thai" as thai_part and "English" as english_part
                title_split_match = re.match(
                    r'(.+?)\s+-\s*(.+)', full_title_line)
                if title_split_match:
                    thai_title_str = title_split_match.group(1).strip()
                    english_title_str = title_split_match.group(2).strip()
                else:
                    thai_title_str = full_title_line
                    # Fallback to same if no explicit English part
                    english_title_str = full_title_line

                # Check for day sections to add birthday badge
                birthday_badge = ""
                if section_id == "day4":
                    birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'

                title_html_tag = f'''
                    <h1>
                        <span class="th th-block">{thai_title_str}</span>
                        <span class="en en-block">{english_title_str}</span>
                        {birthday_badge}
                    </h1>
                '''

            # Remove the original heading from the markdown_text BEFORE processing its body
            # This avoids duplicate headings once the custom H1 is prepended.
            body_markdown = re.sub(
                r'#+\s*([^\n]+)\n?', '', markdown_text, 1).strip()

            processed_body_html = markdown_to_html_with_structure(
                body_markdown)

            # Clear the target div and insert the new H1 and processed body HTML
            div_tag.clear()
            if title_html_tag:
                div_tag.append(BeautifulSoup(title_html_tag, 'html.parser'))
            div_tag.append(BeautifulSoup(processed_body_html, 'html.parser'))

        # If the ID doesn't match any markdown file, it remains empty or uses its original content.
        # This is fine for divs that might serve as placeholders or are just empty.

    # Update the main header H1 and H2 based on 'tokyo-trip-update.md'
    if "tokyo-trip-update" in markdown_contents:
        header_md = markdown_contents["tokyo-trip-update"]
        # Extracting titles from tokyo-trip-update.md
        main_title_line_match = re.search(r'#\s+([^\n]+)', header_md)
        date_line_match = re.search(r'📅\s+([^\n]+)', header_md)

        if main_title_line_match:
            main_title = main_title_line_match.group(1).strip()
            # Assuming main title is "เที่ยวญี่ปุ่น Porjai: Birthday Trip 2026"
            h1_main = template_soup.find('h1', id='toc')
            if h1_main:
                h1_main.find('span', class_='th').string = main_title
                # English title is already correct in template

        if date_line_match:
            main_date = date_line_match.group(1).strip()
            h2_main = template_soup.find('header').find('h2')
            if h2_main:
                h2_main.find('span', class_='th').string = f"📅 {main_date}"
                # English date is already correct in template

    # Generate output filename with current date
    today_date_str = datetime.now().strftime("%Y%m%d")
    output_filename = BUILD_DIR / \
        f"Tokyo-Trip-March-2026-gemini-{today_date_str}.html"

    # Write the final beautiful HTML to file
    with open(output_filename, 'w', encoding='utf-8') as f_out:
        f_out.write(template_soup.prettify())

    print(f"✅ Generated: {output_filename}")


# Run the build process
build_full_html_plan()
