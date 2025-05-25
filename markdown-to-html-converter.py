import os
import re
import sys
import json
import mistune
from bs4 import BeautifulSoup

# Define paths
MARKDOWN_FILE = "tokyo_trip_plan.md"
HTML_TEMPLATE = "tokyo_trip_template.html"
OUTPUT_HTML = "tokyo_trip_complete.html"

def read_file(filename):
    """Read file contents and return as string"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def process_section(section_title, section_content, section_id=None):
    """Process a section of the markdown content and return HTML"""
    # Create section HTML
    if not section_id:
        # Generate ID from title
        section_id = section_title.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '')
        # Handle Thai characters
        section_id = re.sub(r'[^\w\-]', '', section_id, flags=re.UNICODE)
    
    section_html = f'<section id="{section_id}">\n'
    
    # Add section title
    if section_title:
        # Check if this is a day section
        day_match = re.match(r'วันที่\s+(\d+):\s+(\d+)\s+มีนาคม.*', section_title)
        if day_match:
            day_num = day_match.group(1)
            thai_date = day_match.group(0)
            
            # Extract English version if it exists
            english_date = ""
            if " - " in section_title:
                english_date = section_title.split(" - ")[1]
            
            # Add birthday badge for day 4
            birthday_badge = ""
            if day_num == "4":
                birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
            
            section_html += f'<h1>\n'
            section_html += f'<span class="th th-block">{thai_date}</span>\n'
            section_html += f'<span class="en en-block">Day {day_num}: {english_date}</span>\n'
            section_html += f'{birthday_badge}\n'
            section_html += f'</h1>\n'
        else:
            # Regular section title
            section_html += f'<h1>\n<span class="th th-block">{section_title}</span>\n'
            # If we have English title
            if " / " in section_title:
                thai, english = section_title.split(" / ", 1)
                section_html += f'<span class="en en-block">{english}</span>\n'
            section_html += f'</h1>\n'
    
    # Convert markdown content to HTML
    html_content = mistune.html(section_content)
    
    # Process bullet points into timeline items
    if section_id.startswith('day') and '-**' in section_content:
        timeline_html = '<ul class="timeline">\n'
        
        # Use regex to match timeline items
        pattern = r'-\s+\*\*([^*]+)\*\*:\s+<span class="emoji">([^<]+)</span>\s+(.+?)(?=\n-\s+\*\*|\n\n|\Z)'
        timeline_items = re.findall(pattern, section_content, re.DOTALL)
        
        for time, emoji, content in timeline_items:
            timeline_html += f'<li>\n<strong>{time}</strong>: <span class="emoji">{emoji}</span> {content}\n'
            
            # Check if there's additional info box for this item
            info_box_pattern = r'(  - \*\*[^*]+\*\*:.*?)(?=\n-\s+\*\*|\n\n|\Z)'
            info_boxes = re.findall(info_box_pattern, content, re.DOTALL)
            
            if info_boxes:
                for info_box in info_boxes:
                    info_title_match = re.match(r'  - \*\*([^*]+)\*\*:', info_box)
                    if info_title_match:
                        info_title = info_title_match.group(1)
                        info_content = info_box[len(info_title_match.group(0)):]
                        
                        timeline_html += f'<div class="info-box">\n'
                        timeline_html += f'<div class="info-toggle">\n'
                        timeline_html += f'<span class="th">ℹ️ {info_title}</span><span class="en">ℹ️ {info_title}</span>\n'
                        timeline_html += f'</div>\n'
                        timeline_html += f'<div class="info-detail">\n'
                        timeline_html += mistune.html(info_content)
                        timeline_html += f'</div>\n'
                        timeline_html += f'</div>\n'
            
            timeline_html += f'</li>\n'
        
        timeline_html += '</ul>\n'
        
        # Replace the html_content with our timeline
        html_content = timeline_html
    
    # Process tables
    if '|' in section_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        tables = soup.find_all('table')
        
        for table in tables:
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
        
        html_content = str(soup)
    
    # Add the processed content to the section
    section_html += html_content
    
    # Close the section
    section_html += '</section>\n'
    
    return section_html

def process_markdown(markdown_text):
    """Process the markdown content and convert to structured HTML sections"""
    # Split the markdown by main section headers (## level)
    sections_pattern = r'##\s+([^\n]+)\n(.*?)(?=##\s+|\Z)'
    sections = re.findall(sections_pattern, markdown_text, re.DOTALL)
    
    # Extract the title and intro (content before first ##)
    title_match = re.match(r'#\s+([^\n]+)\n(.*?)(?=##\s+)', markdown_text, re.DOTALL)
    
    title = ""
    intro = ""
    if title_match:
        title = title_match.group(1)
        intro = title_match.group(2)
    
    # Process each section
    html_sections = []
    
    # Add the overview section
    if intro:
        html_sections.append(process_section("ภาพรวมการเดินทางและกิจกรรม", intro, "overview"))
    
    # Process day sections and other sections
    for i, (section_title, section_content) in enumerate(sections):
        # Check if this is a day section
        day_match = re.match(r'วันที่\s+(\d+):', section_title)
        
        if day_match:
            day_num = day_match.group(1)
            section_id = f"day{day_num}"
        else:
            # Use simplified section title as ID
            section_id = re.sub(r'[^\w\-]', '', section_title.lower().replace(' ', '-'), flags=re.UNICODE)
        
        html_sections.append(process_section(section_title, section_content, section_id))
    
    return title, ''.join(html_sections)

def create_day_overview_cards(markdown_text):
    """Create day overview cards for the main page"""
    # Extract day sections with their titles and descriptions
    day_pattern = r'##\s+วันที่\s+(\d+):[^-]+-\s+([^\n]+)\n(.*?)(?=##\s+|\Z)'
    day_sections = re.findall(day_pattern, markdown_text, re.DOTALL)
    
    html = '<div class="day-overviews">\n'
    
    # Process each day
    for day_num, title_en, content in day_sections:
        # Extract the first paragraph as description
        first_para = re.search(r'\n([^\n#]+)', content, re.MULTILINE)
        description = first_para.group(1).strip() if first_para else ""
        
        # Create day card
        html += f'<div class="day-overview">\n'
        html += f'<h3><a href="#day{day_num}"><span class="th">วันที่ {day_num}: {title_en}</span>'
        html += f'<span class="en">Day {day_num}: {title_en}</span></a></h3>\n'
        html += f'<p><span class="th">{description}</span><span class="en">{description}</span></p>\n'
        html += f'</div>\n'
    
    # Add budget overview card
    html += f'''
    <div class="day-overview">
    <h3><a href="#budget"><span class="th">ประมาณการค่าใช้จ่ายและสถานะ</span><span class="en">Budget Estimate and Status</span></a></h3>
    <p><span class="th">ข้อมูลการจอง และประมาณการค่าใช้จ่าย.</span><span class="en">Booking information and estimated expenses.</span></p>
    </div>
    '''
    
    html += '</div> <!-- End .day-overviews -->\n'
    
    return html

def build_html_from_markdown(markdown_file, template_file, output_file):
    """Build the final HTML file from markdown content and HTML template"""
    # Read the files
    markdown_text = read_file(markdown_file)
    template_html = read_file(template_file)
    
    # Process the markdown
    title, sections_html = process_markdown(markdown_text)
    
    # Create day overview section
    overview_cards = create_day_overview_cards(markdown_text)
    
    # Replace placeholders in template
    final_html = template_html.replace('<!-- CONTENT_PLACEHOLDER -->', sections_html)
    final_html = final_html.replace('<!-- OVERVIEW_CARDS_PLACEHOLDER -->', overview_cards)
    final_html = final_html.replace('<!-- TITLE_PLACEHOLDER -->', title)
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(final_html)
    
    print(f"Successfully generated {output_file}")

if __name__ == "__main__":
    # Use command line arguments if provided
    md_file = sys.argv[1] if len(sys.argv) > 1 else MARKDOWN_FILE
    template_file = sys.argv[2] if len(sys.argv) > 2 else HTML_TEMPLATE
    output_file = sys.argv[3] if len(sys.argv) > 3 else OUTPUT_HTML
    
    build_html_from_markdown(md_file, template_file, output_file)
