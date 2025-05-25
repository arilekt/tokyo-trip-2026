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
TEMPLATE_FILE = SCRIPT_DIR / "assets/gemini-template-skeleton.html"

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


class MultiLangRenderer(mistune.HTMLRenderer):
    """Custom renderer to preserve multi-language spans and handle custom blocks."""

    def block_html(self, html):
        # Allow raw HTML blocks (like our custom box placeholders) to pass through
        return html

    def paragraph(self, text):
        # If paragraph contains explicit span classes for language, preserve it
        if '<span class="th"' in text or '<span class="en"' in text or '<span class="jp"' in text:
            return f'<p>{text}</p>\n'
        return super().paragraph(text)

    def list_item(self, text):
        # Preserve multi-language spans within list items
        if '<span class="th-li"' in text or '<span class="en-li"' in text or '<span class="jp-li"' in text:
            return f'<li class="lang-li-auto">{text}</li>\n'
        return super().list_item(text)

    def heading(self, text, level):
        # Headings are handled by the main script for multi-language, so this might be redundant
        # if the script removes markdown heading before parsing body.
        # But if not, ensure it doesn't break multi-lang spans.
        if '<span class="th"' in text or '<span class="en"' in text or '<span class="jp"' in text:
            return f'<h{level}>{text}</h{level}>\n'
        return super().heading(text, level)


# Initialize mistune with the custom renderer globally
markdown_parser = mistune.Markdown(renderer=MultiLangRenderer())


def process_custom_boxes(text_content):
    """Identifies and processes custom info/note box markdown into HTML div structures."""
    box_pattern = re.compile(
        r'(?:^|\n)(?P<type>info|note)-box\s*\n'
        r'(?:```(?P<title_triple_backtick>[^`]+)```|(?P<title_single_line>[^\n]+))\n'
        r'(?P<content>.+?)'
        r'(?=\n(?:info|note)-box|\n---|\n\n|\Z)',
        re.DOTALL | re.MULTILINE
    )

    def replace_box_markup(match):
        box_type = match.group('type')
        title_md = match.group('title_triple_backtick') if match.group(
            'title_triple_backtick') else match.group('title_single_line')
        content_md = match.group('content').strip()

        title_soup = BeautifulSoup(
            markdown_parser.inline(title_md.strip()), 'html.parser')
        th_title = title_soup.find('span', class_='th')
        en_title = title_soup.find('span', class_='en')
        jp_title = title_soup.find('span', class_='jp')

        th_title_text = th_title.decode_contents().strip(
        ) if th_title else title_soup.get_text(strip=True)
        en_title_text = en_title.decode_contents().strip() if en_title else th_title_text
        jp_title_text = jp_title.decode_contents().strip() if jp_title else th_title_text

        toggle_html = f'''
            <div class="{box_type}-toggle">
                <span class="th">{th_title_text}</span>
                <span class="en">{en_title_text}</span>
                <span class="jp">{jp_title_text}</span>
            </div>
        '''

        box_content_html = markdown_parser.parse(content_md)
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


def process_timeline_markup(text_content):
    """Converts timeline markdown into HTML <ul><li> structure."""
    timeline_item_pattern = re.compile(
        r'^- \*\*(?P<time>[^*]+?)\*\*:\s*(?P<emoji><span class="emoji">[^<]+?</span>)?\s*(?P<content>.+?)'
        r'(?=\n^- \*\*|\n\n|\Z)',
        re.MULTILINE | re.DOTALL
    )

    timeline_html_items = []

    matches = list(timeline_item_pattern.finditer(text_content))

    if not matches:
        return text_content  # No timeline found, return original content

    for match in matches:
        time_part = match.group('time').strip()
        emoji_part = match.group('emoji') if match.group('emoji') else ''
        content_md = match.group('content').strip()

        # Process the content of the timeline item (which might contain custom boxes)
        inner_processed_content_html = markdown_parser.parse(
            process_custom_boxes(content_md))

        # IMPORTANT: Ensure it's a string before calling re.sub
        if not isinstance(inner_processed_content_html, str):
            print(
                f"Warning: mistune.parse returned non-string type: {type(inner_processed_content_html)}. Attempting to convert to string.")
            processed_content_html = str(inner_processed_content_html)
        else:
            processed_content_html = inner_processed_content_html

        # Remove outer <p> tags if mistune adds them unnecessarily
        processed_content_html = re.sub(
            r'^<p>(.*)</p>$', r'\1', processed_content_html, flags=re.DOTALL)

        timeline_html_items.append(f'''
        <li>
            <strong>{time_part}</strong>: {emoji_part} {processed_content_html}
        </li>
        ''')

    return '<ul class="timeline">\n' + "".join(timeline_html_items) + '</ul>\n'


def markdown_to_html_with_structure(markdown_text_input):
    """
    Orchestrates the conversion of markdown to HTML, applying specific structural transformations
    for timelines, info/note boxes, and tables.
    """
    # Determine if the primary structure is a timeline or general content
    if re.search(r'^- \*\*[^*]+\*\*:', markdown_text_input, re.MULTILINE):
        # This looks like a primary timeline section
        html_content = process_timeline_markup(markdown_text_input)
    else:
        # General markdown, might contain tables and non-timeline info/note boxes
        html_content = markdown_parser.parse(
            process_custom_boxes(markdown_text_input))

    soup = BeautifulSoup(html_content, 'html.parser')

    # Process tables for responsive design and custom classes
    for table in soup.find_all('table'):
        table_container = soup.new_tag(
            'div', attrs={'class': 'table-container'})
        table.wrap(table_container)

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

    day_ids = sorted([id for id in markdown_contents_map if id.startswith('day')],
                     key=lambda x: int(re.search(r'\d+', x).group()))

    for section_id in day_ids:
        markdown_text = markdown_contents_map[section_id]

        title_line_match = re.search(r'##\s+([^\n]+)', markdown_text)
        if not title_line_match:
            print(
                f"Warning: No main title found for {section_id} to create overview card.")
            continue

        title_full = title_line_match.group(1).strip()

        thai_title_str = ""
        english_title_str = ""

        complex_title_match = re.match(
            r'(วันที่\s+\d+:\s*[^-\n]+)\s*-\s*(.+)', title_full)
        if complex_title_match:
            thai_title_str = complex_title_match.group(1).strip()
            english_title_str = complex_title_match.group(2).strip()
        else:
            thai_title_str = title_full
            english_title_str = title_full

        description_th = ""
        description_en = ""

        temp_md_for_desc = ""
        for line in markdown_text.splitlines():
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith(('#', '-', '*', '|', '>')) and not re.match(r'^\d+\.', stripped_line):
                temp_md_for_desc = stripped_line
                break

        if temp_md_for_desc:
            processed_desc_html = markdown_parser.inline(temp_md_for_desc)
            desc_soup = BeautifulSoup(processed_desc_html, 'html.parser')

            th_span = desc_soup.find('span', class_='th')
            en_span = desc_soup.find('span', class_='en')

            if th_span:
                description_th = th_span.decode_contents().strip()
            else:
                description_th = desc_soup.get_text(strip=True)

            if en_span:
                description_en = en_span.decode_contents().strip()
            else:
                description_en = description_th

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

    if "budget" in markdown_contents_map:
        budget_md_content = markdown_contents_map["budget"]

        budget_desc_th = "ข้อมูลการจอง และประมาณการค่าใช้จ่าย."
        budget_desc_en = "Booking information and estimated expenses."

        budget_content_lines = budget_md_content.splitlines()
        for line in budget_content_lines:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith(('#', '|', '-', '*')) and not stripped_line.startswith(('💰')):
                processed_line_html = markdown_parser.inline(stripped_line)
                line_soup = BeautifulSoup(processed_line_html, 'html.parser')

                th_span = line_soup.find('span', class_='th')
                en_span = line_soup.find('span', class_='en')

                if th_span:
                    budget_desc_th = th_span.decode_contents().strip()
                else:
                    budget_desc_th = line_soup.get_text(strip=True)

                if en_span:
                    budget_desc_en = en_span.decode_contents().strip()
                else:
                    budget_desc_en = budget_desc_th
                break

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


def generate_accommodation_overview(markdown_contents_map):
    """
    Generates the Agoda-style accommodation overview section.
    Requires content from 'accommodation.md', 'main_info.md', 'timeline.md'.
    """
    accommodation_md = markdown_contents_map.get('accommodation', '')
    main_info_md = markdown_contents_map.get('main_info', '')
    timeline_md = markdown_contents_map.get('timeline', '')

    overview_html = '<section id="accommodation_overview_agoda">\n'
    overview_html += '<h1><span class="th th-block">ภาพรวมที่พัก</span><span class="en en-block">Accommodation Overview</span></h1>\n'
    overview_html += '<div class="agoda-style-container">\n'

    # --- Flight Information (Top Card) ---
    flight_info_html = '<div class="agoda-card agoda-flight-card">\n'
    flight_info_html += '<div class="agoda-card-header"><span class="emoji">✈️</span> <span class="th">เที่ยวบิน</span><span class="en">Flights</span></div>\n'

    # Extract flight details from main_info.md and timeline.md
    flight_to_match = re.search(r'ไป:\s*(SL\d+\s+\(.+?\))', main_info_md)
    flight_return_match = re.search(r'กลับ:\s*(XJ\d+\s+\(.+?\))', main_info_md)

    flight_to_text = flight_to_match.group(1).strip(
    ) if flight_to_match else "ไม่พบข้อมูลเที่ยวบินไป"
    flight_return_text = flight_return_match.group(1).strip(
    ) if flight_return_match else "ไม่พบข้อมูลเที่ยวบินกลับ"

    flight_to_timeline_match = re.search(
        r'SL\s*394\s*\| รหัสจองสายการบิน:\s*([^\n]+)', timeline_md)
    flight_return_timeline_match = re.search(
        r'XJ\s*607\s*\| รหัสจองสายการบิน:\s*([^\n]+)', timeline_md)

    flight_to_booking_id = flight_to_timeline_match.group(
        1).strip() if flight_to_timeline_match else "N/A"
    flight_return_booking_id = flight_return_timeline_match.group(
        1).strip() if flight_return_timeline_match else "N/A"

    flight_info_html += f'''
    <div class="agoda-card-body">
        <p><span class="th"><b>ขาไป:</b> {flight_to_text}</span><span class="en"><b>To:</b> {flight_to_text}</span><br/>
        <span class="th">รหัสจอง: {flight_to_booking_id}</span><span class="en">Booking ID: {flight_to_booking_id}</span></p>
        <p><span class="th"><b>ขากลับ:</b> {flight_return_text}</span><span class="en"><b>Return:</b> {flight_return_text}</span><br/>
        <span class="th">รหัสจอง: {flight_return_booking_id}</span><span class="en">Booking ID: {flight_return_booking_id}</span></p>
        <div class="agoda-status-bar status-complete">
            <span class="th">✅ จ่ายแล้ว</span><span class="en">✅ Paid</span>
        </div>
    </div>
    '''
    flight_info_html += '</div>\n'
    overview_html += flight_info_html

    # --- Accommodation Details (Cards for each hotel) ---
    hotel_data_rows = re.findall(r'\|(.*)\|', accommodation_md)
    hotels = []
    if hotel_data_rows:
        # Skip header and separator lines
        for i, row in enumerate(hotel_data_rows):
            if i < 2:
                continue
            cells = [c.strip() for c in row.split('|')]
            if len(cells) >= 8:
                hotels.append({
                    "date": cells[1],
                    "hotel": cells[2],
                    "location": cells[3],
                    "nights": cells[4],
                    "price": cells[5],
                    "booking_id": cells[6],
                    "status": cells[7]
                })

    for hotel in hotels:
        hotel_card_html = '<div class="agoda-card agoda-hotel-card">\n'
        hotel_card_html += f'<div class="agoda-card-header"><span class="emoji">🏨</span> <span class="th">ที่พัก: {hotel["hotel"]}</span><span class="en">Accommodation: {hotel["hotel"]}</span></div>\n'
        hotel_card_html += '<div class="agoda-card-body">\n'
        hotel_card_html += f'<p><span class="th"><b>วันที่:</b> {hotel["date"]}</span><span class="en"><b>Date:</b> {hotel["date"]}</span></p>\n'
        hotel_card_html += f'<p><span class="th"><b>สถานที่:</b> {hotel["location"]}</span><span class="en"><b>Location:</b> {hotel["location"]}</span></p>\n'
        hotel_card_html += f'<p><span class="th"><b>จำนวนคืน:</b> {hotel["nights"]}</span><span class="en"><b>Nights:</b> {hotel["nights"]}</span></p>\n'
        hotel_card_html += f'<p><span class="th"><b>ราคา:</b> {hotel["price"]}</span><span class="en"><b>Price:</b> {hotel["price"]}</span></p>\n'
        hotel_card_html += f'<p><span class="th"><b>หมายเลขจอง:</b> {hotel["booking_id"]}</span><span class="en"><b>Booking ID:</b> {hotel["booking_id"]}</span></p>\n'

        status_map = {
            "✅": {"th": "✅ จ่ายแล้ว", "en": "✅ Paid", "class": "status-complete"},
            # For Asta Hotel (status '-')
            "-": {"th": "✅ จ่ายแล้ว", "en": "✅ Paid", "class": "status-complete"},
            "❗": {"th": "❗ ต้องซื้อ", "en": "❗ Must Buy", "class": "status-urgent"},
            "⏳": {"th": "⏳ วางแผน", "en": "⏳ Planning", "class": "status-planning"},
            "🪪": {"th": "🪪 ประมาณ", "en": "🪪 Estimate", "class": "status-planning"},
            "✅ จ่ายแล้ว": {"th": "✅ จ่ายแล้ว", "en": "✅ Paid", "class": "status-complete"},
        }

        # Determine status emoji and text from the "status" cell of accommodation.md
        # Example status cell: "1891056461 | ✅"
        # The content in hotel["status"] can be like "1891056461 | ✅" or just "✅" or just "-"
        current_status_cell = hotel["status"]

        detected_emoji_match = re.match(r'.*(✅|❗|⏳|🪪)', current_status_cell)
        detected_emoji = detected_emoji_match.group(
            1) if detected_emoji_match else "-"  # Default for Asta Hotel

        # Default to planning if unknown emoji
        status_entry = status_map.get(detected_emoji, status_map["⏳"])

        # If the status cell has complex text like "1891056461 | ✅"
        # We need to extract the actual text for TH/EN
        status_text_th = current_status_cell.strip()
        status_text_en = status_entry["en"]  # Default English text

        if "✅" in status_text_th and "จองแล้ว" not in status_text_th:
            status_text_th = "✅ จองแล้ว"
            status_text_en = "✅ Booked"
            status_entry["class"] = "status-complete"
        # Specific for Asta Hotel
        elif "-" in status_text_th and "Asta Hotel" in hotel["hotel"]:
            status_text_th = "✅ จ่ายแล้ว"
            status_text_en = "✅ Paid"
            status_entry["class"] = "status-complete"
        elif "✅" in status_text_th and "จ่ายแล้ว" not in status_text_th:  # For the original "✅" in status column
            status_text_th = "✅ จ่ายแล้ว"
            status_text_en = "✅ Paid"
            status_entry["class"] = "status-complete"

        hotel_card_html += f'<div class="agoda-status-bar {status_entry["class"]}">\n'
        hotel_card_html += f'<span class="th">{status_text_th}</span><span class="en">{status_text_en}</span>\n'
        hotel_card_html += '</div>\n'

        hotel_card_html += '</div>\n'
        hotel_card_html += '</div>\n'
        overview_html += hotel_card_html

    overview_html += '</div>\n'  # End agoda-style-container
    overview_html += '</section>\n'

    return overview_html


def build_full_html_plan():
    """
    Builds the complete HTML trip plan by combining template, markdown content,
    and inlining CSS/JS.
    """
    # 1. Read the refactored template HTML
    template_html_content = read_file(TEMPLATE_FILE)
    template_soup = BeautifulSoup(template_html_content, 'html.parser')

    # Add custom CSS for Agoda-style overview
    custom_agoda_css = """
    #accommodation_overview_agoda {
        margin-top: 2.5rem; /* Consistent spacing for new section */
    }
    .agoda-style-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem; /* Spacing between cards */
        margin-top: 2rem;
        justify-content: center; /* Center cards */
    }

    .agoda-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        box-shadow: 0 4px 10px var(--shadow);
        overflow: hidden;
        width: 100%; /* Default to full width on small screens */
        max-width: 380px; /* Max width for each card */
        flex-grow: 1; /* Allow cards to grow */
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        display: flex;
        flex-direction: column; /* Stack header and body */
    }

    .agoda-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    }

    .agoda-card-header {
        background-color: var(--primary-light);
        color: var(--text-color);
        padding: 1rem 1.2rem;
        font-weight: bold;
        font-size: 1.15rem;
        border-bottom: 1px solid var(--border-color);
        display: flex;
        align-items: center; /* Align icon and text */
        gap: 0.5rem; /* Space between icon and text */
    }
    .agoda-card-header .emoji {
        font-size: 1.4em; /* Larger emoji in header */
    }

    .agoda-flight-card .agoda-card-header {
        background-color: #e0f2f7; /* Light blue for flights */
        border-bottom: 1px solid #a7d9eb;
    }

    .agoda-card-body {
        padding: 1.2rem;
        flex-grow: 1; /* Allow body to take available space */
        display: flex;
        flex-direction: column;
    }

    .agoda-card-body p {
        margin-bottom: 0.8rem;
        font-size: 0.95rem;
        color: var(--text-color);
    }

    .agoda-card-body p b {
        color: var(--primary-dark);
    }

    .agoda-status-bar {
        margin-top: auto; /* Push to bottom */
        padding: 0.6rem 1rem;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        white-space: nowrap;
        background-color: var(--pending); /* Default neutral */
        color: white;
        font-size: 0.9rem;
    }

    .agoda-status-bar.status-complete { background-color: var(--success); }
    .agoda-status-bar.status-pending { background-color: var(--warning); color: var(--text-color); }
    .agoda-status-bar.status-urgent { background-color: var(--danger); }
    .agoda-status-bar.status-planning { background-color: var(--pending); }

    /* Responsive adjustments for Agoda-style cards */
    @media (min-width: 768px) {
        .agoda-style-container {
            justify-content: space-between; /* Distribute cards evenly */
        }
        .agoda-card {
            width: calc(50% - 0.75rem); /* Two cards per row */
        }
    }

    @media (min-width: 1024px) {
        .agoda-style-container {
            justify-content: flex-start; /* Align to start for more columns */
        }
        .agoda-card {
            width: calc(33.333% - 1rem); /* Three cards per row */
        }
    }
    /* Specific adjustments for print */
    @media print {
        .agoda-card {
            max-width: none; /* Allow cards to take full width */
            width: 100%;
            break-inside: avoid;
            page-break-inside: avoid;
        }
        .agoda-style-container {
            display: block; /* Stack cards vertically */
            gap: 0;
        }
        .agoda-card-header, .agoda-card-body {
            padding: 0.8rem; /* Reduce padding for print */
        }
        .agoda-status-bar {
            margin-top: 0.5rem; /* Add small margin */
        }
    }
    """
    # Find the <style> tag and append the new CSS
    style_tag = template_soup.find('style')
    if style_tag:
        style_tag.append(BeautifulSoup(custom_agoda_css, 'html.parser'))

    # 2. Read content from all markdown files
    markdown_contents = {}
    for md_file_path in CONTENT_DIR.glob('*.md'):
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

            # Update the main intro paragraph under header
            if "main_info" in markdown_contents:
                main_info_md = markdown_contents["main_info"]
                travelers_line_match = re.search(r'✈️(.+)', main_info_md)
                route_line_match = re.search(r'🗺️(.+)', main_info_md)

                travelers_th = "ไม่พบข้อมูลผู้เดินทาง"
                travelers_en = "Travelers info not found"
                route_th = "ไม่พบข้อมูลเส้นทาง"
                route_en = "Route info not found"

                if travelers_line_match:
                    temp_soup_travelers = BeautifulSoup(
                        travelers_line_match.group(1).strip(), 'html.parser')
                    th_span = temp_soup_travelers.find('span', class_='th')
                    en_span = temp_soup_travelers.find('span', class_='en')
                    if th_span:
                        travelers_th = th_span.decode_contents().strip()
                    else:
                        travelers_th = temp_soup_travelers.get_text(strip=True)
                    if en_span:
                        travelers_en = en_span.decode_contents().strip()
                    else:
                        travelers_en = travelers_th

                if route_line_match:
                    temp_soup_route = BeautifulSoup(
                        route_line_match.group(1).strip(), 'html.parser')
                    th_span = temp_soup_route.find('span', class_='th')
                    en_span = temp_soup_route.find('span', class_='en')
                    if th_span:
                        route_th = th_span.decode_contents().strip()
                    else:
                        route_th = temp_soup_route.get_text(strip=True)
                    if en_span:
                        route_en = en_span.decode_contents().strip()
                    else:
                        route_en = route_th

                intro_p_html = f'''
                <p>
                    <span class="th">✈️ ผู้เดินทาง: {travelers_th}</span><span class="en">✈️ Travelers: {travelers_en}</span><br/>
                    <span class="th">🗺️ เส้นทาง: {route_th}</span><span class="en">🗺️ Itinerary: {route_en}</span>
                </p>
                '''
                target_p = template_soup.find(
                    'div', class_='container').find('p')
                if target_p:
                    target_p.replace_with(BeautifulSoup(
                        intro_p_html, 'html.parser'))

        elif section_id == "accommodation_overview_agoda":
            # Generate Agoda-style accommodation overview and inject
            accommodation_overview_html = generate_accommodation_overview(
                markdown_contents)
            div_tag.clear()
            div_tag.append(BeautifulSoup(
                accommodation_overview_html, 'html.parser'))

        elif section_id in markdown_contents:  # For all other content markdown files
            markdown_text = markdown_contents[section_id]

            # Find the main section title from Markdown to build the H1 tag
            section_title_match = re.match(r'#+\s+([^\n]+)', markdown_text)
            title_html_tag = ""
            if section_title_match:
                full_title_line = section_title_match.group(1).strip()

                thai_title_str = ""
                english_title_str = ""

                title_split_match = re.match(
                    r'(.+?)\s+-\s*(.+)', full_title_line)
                if title_split_match:
                    thai_title_str = title_split_match.group(1).strip()
                    english_title_str = title_split_match.group(2).strip()
                else:
                    thai_title_str = full_title_line
                    english_title_str = full_title_line

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

            body_markdown = re.sub(
                r'#+\s*([^\n]+)\n?', '', markdown_text, 1).strip()

            processed_body_html = markdown_to_html_with_structure(
                body_markdown)

            div_tag.clear()
            if title_html_tag:
                div_tag.append(BeautifulSoup(title_html_tag, 'html.parser'))
            div_tag.append(BeautifulSoup(processed_body_html, 'html.parser'))

    # Update the main header H1 and H2 based on 'tokyo-trip-update.md'
    if "tokyo-trip-update" in markdown_contents:
        header_md = markdown_contents["tokyo-trip-update"]
        main_title_line_match = re.search(r'#\s+([^\n]+)', header_md)
        date_line_match = re.search(r'📅\s+([^\n]+)', header_md)

        if main_title_line_match:
            main_title = main_title_line_match.group(1).strip()
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
        f"Tokyo-Trip-March-2026-Gemini-{today_date_str}.html"

    # Write the final beautiful HTML to file
    with open(output_filename, 'w', encoding='utf-8') as f_out:
        f_out.write(template_soup.prettify())

    print(f"✅ Generated: {output_filename}")


# Run the build process
build_full_html_plan()
