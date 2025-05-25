# gemini-build_trip_plan.py

import os
import re
from pathlib import Path
import mistune
from bs4 import BeautifulSoup
from datetime import datetime

# Define paths
SCRIPT_DIR = Path(__file__).parent # Get the directory of the current script
CONTENT_DIR = SCRIPT_DIR.parent / "content"
BUILD_DIR = SCRIPT_DIR.parent / "build"
TEMPLATE_FILE = SCRIPT_DIR / "gemini-template-skeleton.html"

# Ensure build directory exists
BUILD_DIR.mkdir(parents=True, exist_ok=True)

def read_file(filepath):
    """Reads file content and returns as string."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def markdown_to_html_with_structure(markdown_text):
    """
    Converts markdown to HTML, applying specific structural transformations
    for timelines, info/note boxes, and tables.
    """
    # This regex is an improvement for handling multi-line content within timeline items.
    # It looks for a line starting with '- **Time**:' and captures everything until the next
    # timeline item or end of string.
    timeline_block_pattern = re.compile(
        r'^(- \*\*(?P<time>[^*]+?)\*\*:\s*(?P<emoji><span class="emoji">[^<]+?</span>)?\s*(?P<initial_content>.*?))'
        r'(?=\n- \*\*|$)',
        re.MULTILINE | re.DOTALL
    )

    # Regex for info boxes *within* a timeline item or general text
    info_box_md_pattern = re.compile(
        r'^\s*-\s*\*\*(?P<info_title>[^*]+?)\*\*:\s*(?P<info_content>.+?)(?=\n\s*- \*\*|$|\n\n)',
        re.MULTILINE | re.DOTALL
    )

    processed_blocks = []
    is_timeline_section = False # Flag to detect if the overall markdown text is a timeline

    # First pass: identify timeline blocks and process them specifically
    if re.search(r'^- \*\*[^*]+\*\*:', markdown_text, re.MULTILINE): # Quick check if it looks like a timeline
        is_timeline_section = True
        timeline_items = []
        last_end = 0
        for match in timeline_block_pattern.finditer(markdown_text):
            full_item_md = match.group(1).strip()
            
            # Extract main parts of the timeline item
            time_part = match.group('time')
            emoji_part = match.group('emoji') if match.group('emoji') else ''
            initial_content = match.group('initial_content').strip()

            # Process nested info-boxes within this timeline item's content
            current_item_content_html_parts = []
            current_item_content_md = initial_content
            
            info_matches = list(info_box_md_pattern.finditer(current_item_content_md))
            
            if info_matches:
                last_info_end = 0
                for info_match in info_matches:
                    # Add any text before this info box
                    if info_match.start() > last_info_end:
                        current_item_content_html_parts.append(mistune.html(current_item_content_md[last_info_end:info_match.start()]).strip())
                    
                    info_title = info_match.group('info_title')
                    info_content_md = info_match.group('info_content').strip()
                    info_content_html = mistune.html(info_content_md).strip()
                    
                    # Ensure no extra <p> tags around info-detail content
                    info_content_html = info_content_html.replace('<p>', '').replace('</p>', '')

                    info_html = f'''
                        <div class="info-box">
                            <div class="info-toggle">
                                <span class="th">ℹ️ {info_title}</span>
                                <span class="en">ℹ️ {info_title}</span>
                            </div>
                            <div class="info-detail">
                                {info_content_html}
                            </div>
                        </div>
                    '''
                    current_item_content_html_parts.append(info_html)
                    last_info_end = info_match.end()
                
                # Add any remaining content after the last info box
                if last_info_end < len(current_item_content_md):
                    current_item_content_html_parts.append(mistune.html(current_item_content_md[last_info_end:]).strip())
            else:
                # No info boxes, just convert initial content
                current_item_content_html_parts.append(mistune.html(initial_content).strip())

            full_content_html = "\n".join(current_item_content_html_parts)
            
            timeline_items.append(f'''
            <li>
                <strong>{time_part}</strong>: {emoji_part} {full_content_html}
            </li>
            ''')
            last_end = match.end()
        
        if is_timeline_section: # Only apply timeline wrap if a timeline was truly detected
            processed_blocks.append('<ul class="timeline">\n' + "".join(timeline_items) + '</ul>\n')
        
        # If there's content after the last timeline item, process it normally
        if last_end < len(markdown_text):
            remaining_md = markdown_text[last_end:].strip()
            if remaining_md:
                processed_blocks.append(mistune.html(remaining_md))

    if not is_timeline_section: # If no timeline was detected, just convert the whole thing
        processed_blocks.append(mistune.html(markdown_text))

    full_html_content = "".join(processed_blocks)
    soup = BeautifulSoup(full_html_content, 'html.parser')

    # Process tables for responsive design and custom classes
    for table in soup.find_all('table'):
        # Wrap table in div for responsive design
        table_container = soup.new_tag('div', attrs={'class': 'table-container'})
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
    
    # Sort day files numerically
    sorted_day_ids = sorted([id for id in markdown_contents_map if id.startswith('day')], 
                            key=lambda x: int(x.replace('day', '')))

    for section_id in sorted_day_ids:
        markdown_text = markdown_contents_map[section_id]

        # Extract title and first paragraph as description
        # Assuming titles are like "## วันที่ X: Y (Z) - Title Thai & English"
        title_line_match = re.search(r'##\s+([^\n]+)', markdown_text)
        if not title_line_match:
            print(f"Warning: No main title found for {section_id}. Skipping overview card.")
            continue
        
        title_full = title_line_match.group(1).strip()

        # Extract Thai and English parts of the title line
        # This assumes format "วันที่ X: Thai Title - English Title"
        thai_title_match = re.search(r'(วันที่\s+\d+:\s+[^-\n]+)', title_full)
        thai_title_str = thai_title_match.group(1).strip() if thai_title_match else title_full
        
        english_title_match = re.search(r'-\s*([^\n]+)', title_full)
        english_title_str = english_title_match.group(1).strip() if english_title_match else thai_title_str # Fallback


        # Extract the first *meaningful* paragraph as description
        # This needs to be robust against various markdown structures.
        # Find first line that is not a heading, list item, or empty.
        description = ""
        for line in markdown_text.splitlines():
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith(('#', '-', '*')) and not stripped_line.startswith(('0','1','2','3','4','5','6','7','8','9',' ')) and not stripped_line.startswith(('!','[', '>', '<', '|')):
                description = stripped_line
                break
        
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
                <span class="th">{description}</span>
                <span class="en">{description}</span>
            </p>
        </div>
        '''
    
    # Add budget overview card manually as it's not a 'day'
    # Check if budget.md exists in the map
    if "budget" in markdown_contents_map:
        # Extract description from budget.md if needed, otherwise use static text
        budget_md_content = markdown_contents_map["budget"]
        budget_desc_match = re.search(r'\n([^\n#\-\*]+)', budget_md_content, re.MULTILINE)
        budget_desc = budget_desc_match.group(1).strip() if budget_desc_match else "ข้อมูลการจอง และประมาณการค่าใช้จ่าย."
        
        html += f'''
        <div class="day-overview">
            <h3><a href="#budget">
                <span class="th">ประมาณการค่าใช้จ่ายและสถานะ</span>
                <span class="en">Budget Estimate and Status</span>
            </a></h3>
            <p>
                <span class="th">{budget_desc}</span>
                <span class="en">Booking information and estimated expenses.</span>
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

    # 2. Store all markdown contents and process them
    markdown_contents = {}
    for md_file_path in CONTENT_DIR.glob('*.md'):
        # Use filename as ID, replace underscores with hyphens
        section_id = md_file_path.stem.replace('_', '-') 
        markdown_contents[section_id] = read_file(md_file_path)

    # Dictionary to hold processed HTML for each section
    processed_html_sections = {}
    for section_id, md_text in markdown_contents.items():
        # Special handling for "main_info" and "tokyo-trip-update"
        # These files usually contain general info or TOC, not full sections to be injected directly.
        # The content of 'overview' will be generated dynamically.
        if section_id in ["main_info", "tokyo-trip-update", "overview"]:
            continue 
        
        processed_html_sections[section_id] = markdown_to_html_with_structure(md_text)

    # Now inject processed content into the template
    for div_tag in template_soup.select("div[id]"):
        section_id = div_tag.get("id")

        if section_id == "overview":
            # Generate day overview cards and inject
            overview_content_html = create_day_overview_cards(markdown_contents)
            
            # Find the specific div where cards should be injected
            target_div = div_tag.find('div', class_='day-overviews')
            if target_div:
                target_div.clear() # Clear any placeholder content
                target_div.append(BeautifulSoup(overview_content_html, 'html.parser'))

            # Handle the note-box in overview, which is already in the template
            # No need to inject if it's static in the template.
            # If it were in overview.md, it would be handled differently.
            
            # Extract main_info content (if needed for header/intro)
            if "main_info" in markdown_contents:
                main_info_md = markdown_contents["main_info"]
                # Assuming the first paragraph of main_info contains the traveler/route info
                travel_info_match = re.search(r'✈️(.+?)🗺️(.+)', main_info_md, re.DOTALL)
                if travel_info_match:
                    travelers_th_match = re.search(r'ผู้เดินทาง:\s*(.+)', travel_info_match.group(1))
                    route_th_match = re.search(r'เส้นทาง:\s*(.+)', travel_info_match.group(2))
                    
                    travelers_en_match = re.search(r'Travelers:\s*(.+)', travel_info_match.group(1))
                    route_en_match = re.search(r'Itinerary:\s*(.+)', travel_info_match.group(2))

                    travelers_html = f'''
                    <span class="th">✈️ ผู้เดินทาง: {travelers_th_match.group(1).strip()}</span>
                    <span class="en">✈️ Travelers: {travelers_en_match.group(1).strip()}</span><br/>
                    <span class="th">🗺️ เส้นทาง: {route_th_match.group(1).strip()}</span>
                    <span class="en">🗺️ Itinerary: {route_en_match.group(1).strip()}</span>
                    '''
                    p_tag = template_soup.find('div', class_='container').find('p', class_=lambda x: x is None) # Find the first p tag under container
                    if p_tag:
                        p_tag.clear()
                        p_tag.append(BeautifulSoup(travelers_html, 'html.parser'))


        elif section_id in processed_html_sections:
            # Inject processed HTML into the div
            div_tag.clear() # Clear existing content/placeholders
            div_tag.append(BeautifulSoup(processed_html_sections[section_id], 'html.parser'))
            
            # Adjust heading for day sections from markdown content (if not already handled by processed_html_sections)
            # This logic should ideally be inside markdown_to_html_with_structure for robustness.
            # If the first line is a heading, replace it with a styled h1/h2 and language spans.
            md_text = markdown_contents[section_id]
            title_line_match = re.match(r'#+\s+([^\n]+)', md_text)
            if title_line_match:
                full_title = title_line_match.group(1).strip()
                thai_part = re.search(r'([^/]+)', full_title)
                thai_title_str = thai_part.group(1).strip() if thai_part else full_title
                english_part = re.search(r'/\s*(.+)', full_title)
                english_title_str = english_part.group(1).strip() if english_part else thai_title_str # Fallback

                # Special handling for day titles
                day_match = re.match(r'(วันที่\s+\d+):', thai_title_str)
                if day_match:
                    day_num_str = day_match.group(1)
                    # Extract the English date portion from the full title line
                    english_day_title_match = re.search(r'Day \d+:\s*(.+)', english_title_str)
                    english_day_title = english_day_title_match.group(1) if english_day_title_match else english_title_str
                    
                    birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>' if section_id == "day4" else ""
                    h1_tag_html = f'''
                        <h1>
                            <span class="th th-block">{day_num_str} - {thai_title_str.replace(day_num_str, '').strip()}</span>
                            <span class="en en-block">Day {section_id.replace('day', '')}: {english_day_title}</span>
                            {birthday_badge}
                        </h1>
                    '''
                else:
                    # General section title
                    h1_tag_html = f'''
                        <h1>
                            <span class="th th-block">{thai_title_str}</span>
                            <span class="en en-block">{english_title_str}</span>
                        </h1>
                    '''
                
                # Prepend the H1 to the section's content
                div_tag.insert(0, BeautifulSoup(h1_tag_html, 'html.parser'))
                
                # Remove the original heading from the processed content if it's already generated
                # This needs to be careful to avoid removing actual content.
                # A better approach is to modify markdown_to_html_with_structure to NOT generate the H1 for these.
                # For now, this will just add the H1 if it's not already there.
                # Since markdown_to_html_with_structure already processes headings, this part may duplicate.
                # Let's adjust markdown_to_html_with_structure to ONLY convert the body content, not headings.
                # Or, trust the current template where h1 is already present and python inserts content after.
                # Reverting: The template already has H1 tags inside the section.
                # We need to correctly populate those H1 tags with localized content.

    # Update the header H1 and H2 based on main_info.md or tokyo-trip-update.md
    # Assuming tokyo-trip-update.md contains the main header title and date
    if "tokyo-trip-update" in markdown_contents:
        header_md = markdown_contents["tokyo-trip-update"]
        title_match = re.search(r'#\s+([^\n]+)', header_md)
        date_match = re.search(r'📅\s+([^\n]+)', header_md)

        if title_match:
            full_title = title_match.group(1).strip()
            # Assuming title format "เที่ยวญี่ปุ่น Porjai: Birthday Trip 2026"
            title_th = full_title
            title_en = "Porjai's Japan Trip: Birthday Adventure 2026" # Hardcode or extract from markdown if possible
            template_soup.find('h1', id='toc').find('span', class_='th').string = title_th
            template_soup.find('h1', id='toc').find('span', class_='en').string = title_en
        
        if date_match:
            full_date = date_match.group(1).strip()
            # Assuming date format "ศุกร์ 6 – ศุกร์ 13 มีนาคม 2026"
            date_th = full_date
            date_en = "March 6th (Fri) – March 13th (Fri), 2026" # Hardcode or extract from markdown if possible
            template_soup.find('header').find('h2').find('span', class_='th').string = "📅 " + date_th
            template_soup.find('header').find('h2').find('span', class_='en').string = "📅 " + date_en


    # Generate output filename with current date
    today_date_str = datetime.now().strftime("%Y%m%d")
    output_filename = BUILD_DIR / f"Tokyo-Trip-March-2026-Gemini-update-{today_date_str}.html"

    with open(output_filename, 'w', encoding='utf-8') as f_out:
        f_out.write(template_soup.prettify())

    print(f"✅ Generated: {output_filename}")

# Run the build process
build_full_html_plan()
