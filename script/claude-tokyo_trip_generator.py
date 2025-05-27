#!/usr/bin/env python3
"""
Tokyo Trip 2026 - Complete HTML Generator
========================================
Single script to generate beautiful, offline-ready HTML trip plan
with Thai/English support and mobile-optimized design.

Author: AI Assistant for Arilek & Porjai's Birthday Trip
Date: May 2025
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class TripSection:
    """Represents a section of the trip plan"""
    id: str
    title_th: str
    title_en: str
    content: str
    is_day: bool = False
    day_number: Optional[int] = None

class TokyoTripGenerator:
    """Main generator class for the Tokyo Trip HTML plan"""
    
    def __init__(self, content_dir: Path, output_dir: Path):
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.sections: Dict[str, TripSection] = {}
        self.exchange_rate = 0.2346  # 100 JPY ≈ 23.46 THB
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def parse_markdown_file(self, file_path: Path) -> TripSection:
        """Parse a markdown file into a TripSection"""
        content = file_path.read_text(encoding='utf-8')
        section_id = file_path.stem.lower()
        
        # Extract title from first header
        title_match = re.search(r'^##?\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title_line = title_match.group(1).strip()
            
            # Parse Thai/English titles
            if ' - ' in title_line:
                title_th, title_en = title_line.split(' - ', 1)
            elif 'วันที่' in title_line:
                title_th = title_line
                # Extract day info for English
                day_match = re.search(r'วันที่\s*(\d+)', title_line)
                if day_match:
                    day_num = day_match.group(1)
                    remaining = title_line.split(':', 1)[1].strip() if ':' in title_line else ''
                    title_en = f"Day {day_num}: {remaining}"
                else:
                    title_en = title_line
            else:
                title_th = title_line
                title_en = title_line
        else:
            title_th = section_id.replace('_', ' ').title()
            title_en = title_th
        
        # Check if this is a day section
        is_day = section_id.startswith('day')
        day_number = None
        if is_day:
            day_match = re.search(r'day(\d+)', section_id)
            if day_match:
                day_number = int(day_match.group(1))
        
        return TripSection(
            id=section_id,
            title_th=title_th,
            title_en=title_en,
            content=content,
            is_day=is_day,
            day_number=day_number
        )
    
    def convert_markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown to HTML with custom processing"""
        html = markdown_text
        
        # Remove the main header (already used for section title)
        html = re.sub(r'^##?\s+.+$', '', html, count=1, flags=re.MULTILINE)
        
        # Convert headers
        html = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        
        # Convert timeline items (- **time**: content)
        def convert_timeline(match):
            time = match.group(1)
            emoji = match.group(2) if match.group(2) else ''
            content = match.group(3)
            return f'<li><strong>{time}</strong>: <span class="emoji">{emoji}</span> {content}</li>'
        
        # Check if this looks like a timeline
        if re.search(r'^\s*-\s+\*\*\d+:\d+\*\*:', html, re.MULTILINE):
            # Convert timeline items
            html = re.sub(r'^\s*-\s+\*\*([^*]+)\*\*:\s*([^-\n]*(?:🚗|🛫|🛬|🚄|🏨|🍽️|🚶‍♀️|🚢|🛍️|🎁|🗼|🚆|🌳|\w)*)\s*(.+)$', 
                         convert_timeline, html, flags=re.MULTILINE)
            # Wrap in timeline UL
            html = '<ul class="timeline">\n' + html + '\n</ul>'
        else:
            # Convert regular lists
            html = re.sub(r'^\s*-\s+(.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
            # Wrap consecutive list items in UL
            html = re.sub(r'(<li>.*</li>\s*)+', lambda m: '<ul>\n' + m.group(0) + '</ul>\n', html, flags=re.DOTALL)
        
        # Convert bold and italic
        html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
        
        # Convert links
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', html)
        
        # Convert info boxes
        html = re.sub(r'^\s*-\s+\*\*([^*]+)\*\*:\s*$\n((?:\s+-.*\n?)*)', 
                     self._convert_info_box, html, flags=re.MULTILINE)
        
        # Convert paragraphs (lines that aren't already HTML)
        lines = html.split('\n')
        processed_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('<') and not line.endswith('>'):
                if not any(tag in line for tag in ['<li>', '<ul>', '<h3>', '<h4>', '<strong>', '<table>']):
                    line = f'<p>{line}</p>'
            processed_lines.append(line)
        
        html = '\n'.join(processed_lines)
        
        # Convert tables (basic support)
        html = self._convert_tables(html)
        
        # Add currency conversion attributes
        html = re.sub(r'¥(\d{1,2},?\d{0,3})', r'<span data-jpy="\1">¥\1</span>', html)
        
        return html
    
    def _convert_info_box(self, match) -> str:
        """Convert info box markdown to HTML"""
        title = match.group(1)
        content = match.group(2)
        
        # Process the content list
        content_html = re.sub(r'^\s+-\s+(.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
        content_html = f'<ul>{content_html}</ul>'
        
        return f'''
<div class="info-box">
    <div class="info-toggle">
        <span class="th">ℹ️ {title}</span>
        <span class="en">ℹ️ {title}</span>
    </div>
    <div class="info-detail">
        {content_html}
    </div>
</div>
'''
    
    def _convert_tables(self, html: str) -> str:
        """Convert markdown tables to HTML"""
        # This is a simplified table converter
        table_pattern = r'(\|[^|\n]+\|(?:\n\|[^|\n]+\|)*)'
        
        def convert_table(match):
            table_text = match.group(1).strip()
            lines = [line.strip() for line in table_text.split('\n') if line.strip()]
            
            if len(lines) < 2:
                return table_text
            
            html_rows = []
            for i, line in enumerate(lines):
                if line.startswith('|') and line.endswith('|'):
                    cells = [cell.strip() for cell in line[1:-1].split('|')]
                    
                    # Skip separator line
                    if all(cell.replace('-', '').replace(':', '').strip() == '' for cell in cells):
                        continue
                    
                    # First row is header
                    tag = 'th' if i == 0 else 'td'
                    row_html = ''.join(f'<{tag}>{cell}</{tag}>' for cell in cells)
                    html_rows.append(f'<tr>{row_html}</tr>')
            
            return f'<div class="table-container"><table>{"".join(html_rows)}</table></div>'
        
        return re.sub(table_pattern, convert_table, html, flags=re.MULTILINE)
    
    def load_all_sections(self):
        """Load all markdown files from content directory"""
        for md_file in self.content_dir.glob('*.md'):
            if md_file.name.startswith('ai-'):
                continue  # Skip AI instruction files
            
            section = self.parse_markdown_file(md_file)
            self.sections[section.id] = section
            print(f"Loaded section: {section.id}")
    
    def generate_day_overview_cards(self) -> str:
        """Generate overview cards for each day"""
        day_sections = sorted(
            [s for s in self.sections.values() if s.is_day],
            key=lambda x: x.day_number or 0
        )
        
        cards_html = '<div class="day-overviews">\n'
        
        for day_section in day_sections:
            birthday_badge = ''
            if day_section.day_number == 4:  # Day 4 is birthday
                birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
            
            # Extract description from content
            description_th = self._extract_description(day_section.content)
            description_en = description_th  # For now, use same description
            
            cards_html += f'''
            <div class="day-overview">
                <h3><a href="#{day_section.id}">
                    <span class="th">{day_section.title_th}</span>
                    <span class="en">{day_section.title_en}</span>
                </a>{birthday_badge}</h3>
                <p>
                    <span class="th">{description_th}</span>
                    <span class="en">{description_en}</span>
                </p>
            </div>
            '''
        
        # Add budget overview
        cards_html += '''
        <div class="day-overview">
            <h3><a href="#budget">
                <span class="th">ประมาณการค่าใช้จ่ายและสถานะ</span>
                <span class="en">Budget Estimate and Status</span>
            </a></h3>
            <p>
                <span class="th">ข้อมูลการจอง และประมาณการค่าใช้จ่าย</span>
                <span class="en">Booking information and estimated expenses</span>
            </p>
        </div>
        '''
        
        cards_html += '</div>\n'
        return cards_html
    
    def _extract_description(self, content: str) -> str:
        """Extract a brief description from section content"""
        # Remove markdown headers
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('-') and not line.startswith('|'):
                # Clean up the line
                line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)  # Remove bold
                line = re.sub(r'\*([^*]+)\*', r'\1', line)      # Remove italic
                if len(line) > 20:  # Only return substantial descriptions
                    return line[:100] + '...' if len(line) > 100 else line
        return "กิจกรรมต่างๆ ในวันนี้"
    
    def generate_html_template(self) -> str:
        """Generate the complete HTML template"""
        return f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>เที่ยวญี่ปุ่น Porjai: Birthday Trip 2026</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body class="lang-th">
    <div class="language-switcher">
        <button data-lang="th" class="active">TH</button>
        <button data-lang="en">EN</button>
    </div>

    <header>
        <h1 id="toc">
            <span class="th">เที่ยวญี่ปุ่น Porjai: Birthday Trip 2026</span>
            <span class="en">Porjai's Japan Trip: Birthday Adventure 2026</span>
        </h1>
        <h2>
            <span class="th">📅 ศุกร์ 6 – ศุกร์ 13 มีนาคม 2026</span>
            <span class="en">📅 March 6th (Fri) – March 13th (Fri), 2026</span>
        </h2>
    </header>

    <div class="container">
        <p>
            <span class="th">✈️ ผู้เดินทาง: 🧍 Arilek (คุณพ่อ) 👧 Nuntnaphat (พอใจ)</span>
            <span class="en">✈️ Travelers: 🧍 Arilek (Dad) 👧 Nuntnaphat (Porjai)</span><br/>
            <span class="th">🗺️ เส้นทาง: Narita – Tokyo – Kawaguchiko – Gala Yuzawa – Tokyo</span>
            <span class="en">🗺️ Itinerary: Narita – Tokyo – Kawaguchiko – Gala Yuzawa – Tokyo</span>
        </p>

        <section id="overview">
            <h1>
                <span class="th th-block">ภาพรวมการเดินทางและกิจกรรม</span>
                <span class="en en-block">Trip Overview & Activities</span>
            </h1>
            {self.generate_day_overview_cards()}
            
            <div class="note-box">
                <div class="note-toggle">
                    <span class="th">ℹ️ วิธีการใช้งานแผนการเดินทาง</span>
                    <span class="en">ℹ️ How to Use the Itinerary</span>
                </div>
                <div class="note-detail">
                    <p class="th th-block">แผนการเดินทางรวมอยู่ในไฟล์เดียวเพื่อความสะดวกในการใช้งานออฟไลน์</p>
                    <p class="en en-block">The itinerary is consolidated into a single file for easy offline use.</p>
                    <p class="th th-block">คลิกที่หัวข้อ <span class="emoji">ℹ️</span> เพื่อขยายดูรายละเอียดเพิ่มเติม และใช้ปุ่ม "กลับไปหน้าหลัก" ด้านล่างขวาเพื่อไปยังสารบัญ</p>
                    <p class="en en-block">Click on the <span class="emoji">ℹ️</span> headings to expand for more details, and use the "Back to Top" button at the bottom right to navigate to the table of contents.</p>
                    <p class="th th-block">ใช้ปุ่ม TH/EN ที่มุมบนขวา (ลอยอยู่) เพื่อสลับภาษา</p>
                    <p class="en en-block">Use the floating TH/EN buttons at the top right to switch languages.</p>
                </div>
            </div>
        </section>

        {self._generate_content_sections()}
    </div>

    <a class="back-to-top" href="#toc">
        <span class="th">🔙 กลับไปหน้าหลัก</span>
        <span class="en">🔙 Back to Top</span>
    </a>

    <script>
        {self._get_javascript()}
    </script>
</body>
</html>'''
    
    def _generate_content_sections(self) -> str:
        """Generate HTML for all content sections"""
        sections_html = ""
        
        # Sort sections: days first, then others
        day_sections = sorted(
            [s for s in self.sections.values() if s.is_day],
            key=lambda x: x.day_number or 0
        )
        other_sections = [s for s in self.sections.values() if not s.is_day]
        
        all_sections = day_sections + other_sections
        
        for section in all_sections:
            birthday_badge = ''
            if section.day_number == 4:
                birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
            
            content_html = self.convert_markdown_to_html(section.content)
            
            sections_html += f'''
        <section id="{section.id}">
            <h1>
                <span class="th th-block">{section.title_th}</span>
                <span class="en en-block">{section.title_en}</span>
                {birthday_badge}
            </h1>
            {content_html}
        </section>
            '''
        
        return sections_html
    
    def _get_css_styles(self) -> str:
        """Return complete CSS styles"""
        return '''
        :root {
            --primary-color: #ff6b8b;
            --primary-light: #ffdfd0;
            --primary-dark: #d6336c;
            --background: #fff8f0;
            --card-bg: #fff;
            --text-color: #333;
            --border-color: #ffc0cb;
            --info-bg: #fff4f7;
            --info-border: #ffa5ba;
            --note-bg: #f9f3ff;
            --note-border: #d4b8ff;
            --table-alt: #fff5f7;
            --table-header: #ffe0e9;
            --table-border: #f2c8d9;
            --shadow: rgba(255, 192, 203, 0.3);
            --success: #28a745;
            --warning: #ffc107;
            --pending: #6c757d;
            --danger: #dc3545;
        }

        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html { scroll-behavior: smooth; }

        body {
            font-family: "Noto Sans Thai", "Sarabun", sans-serif;
            background-color: var(--background);
            color: var(--text-color);
            font-size: 16px;
            line-height: 1.6;
            padding-bottom: 4rem;
        }

        header {
            background-color: var(--primary-light);
            color: var(--text-color);
            padding: 1.5rem 1rem;
            text-align: center;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
        }
        header h1 {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            padding-top: 2.5rem;
        }
        header h2 {
            font-size: 1.2rem;
            margin-top: 0.5rem;
            border-bottom: none;
            padding-bottom: 0;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }

        h1, h2, h3 {
            color: var(--text-color);
            margin-bottom: 1rem;
        }
        section > h1, section > h2 {
            border-bottom: 2px solid var(--primary-light);
            padding-bottom: 0.5rem;
            margin-top: 2.5rem;
        }
        section > h1 { font-size: 1.6rem; }
        section > h2 { font-size: 1.4rem; }
        h3 { font-size: 1.2rem; margin-top: 1.5rem; }

        p, ul, ol { margin-bottom: 1rem; }
        ul, ol { padding-left: 1.5rem; }
        li ul, li ol { margin-top: 0.5rem; margin-bottom: 0.5rem; }

        a { color: var(--primary-dark); text-decoration: none; }
        a:hover { text-decoration: underline; }

        .table-container { overflow-x: auto; margin: 1.5rem 0; }
        table {
            width: 100%; min-width: 600px; border-collapse: collapse;
            background-color: var(--card-bg); box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        th, td {
            padding: 0.75rem; border: 1px solid var(--table-border);
            text-align: left; vertical-align: top;
        }
        th { background-color: var(--table-header); font-weight: bold; }
        tr:nth-child(even) { background-color: var(--table-alt); }
        tr.total { font-weight: bold; background-color: var(--info-bg); }
        tr.remaining { font-weight: bold; background-color: var(--note-bg); }

        .info-box, .note-box {
            border-left: 5px solid var(--info-border);
            padding: 0.8rem 1rem; margin: 1rem 0;
            border-radius: 0 8px 8px 0; transition: all 0.3s ease;
            background-color: var(--info-bg);
        }
        .note-box {
            border-left-color: var(--note-border);
            background-color: var(--note-bg);
        }

        .info-toggle, .note-toggle {
            cursor: pointer; font-weight: bold;
            display: flex; align-items: center; justify-content: space-between;
        }
        .info-toggle::after, .note-toggle::after {
            content: "▼"; font-size: 0.7em; transition: transform 0.3s;
            margin-left: 0.5rem;
        }
        .info-toggle.collapsed::after, .note-toggle.collapsed::after {
            transform: rotate(-90deg);
        }
        .info-detail, .note-detail {
            margin-top: 0.8rem; overflow: hidden;
            transition: max-height 0.4s ease-out; max-height: 1000px;
        }
        .info-detail.collapsed, .note-detail.collapsed {
            max-height: 0; margin-top: 0;
        }

        .timeline {
            list-style-type: none; margin: 1.5rem 0; padding: 0; position: relative;
        }
        .timeline::before {
            content: ''; position: absolute; left: calc(1rem + 7px - 1px);
            top: 0; bottom: 0; width: 2px; background-color: var(--primary-color);
        }
        .timeline li {
            position: relative; padding: 0.5rem 0 1rem 2.5rem; margin-bottom: 1rem;
        }
        .timeline li::before {
            content: ""; position: absolute; left: 1rem; top: 0.8rem;
            transform: translateY(-50%); width: 14px; height: 14px;
            background-color: var(--primary-color); border: 2px solid var(--background);
            border-radius: 50%; z-index: 1;
        }
        .timeline strong {
            font-weight: bold; color: var(--primary-dark);
            display: block; margin-bottom: 0.3rem;
        }
        .timeline .emoji { margin-right: 8px; }

        #overview .day-overviews {
            display: flex; flex-wrap: wrap; gap: 1rem;
        }
        #overview .day-overview {
            background-color: var(--card-bg); border: 1px solid var(--border-color);
            border-radius: 8px; padding: 1rem; box-shadow: 0 2px 5px var(--shadow);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            flex: 1 1 100%;
        }
        #overview .day-overview:hover {
            transform: translateY(-3px); box-shadow: 0 4px 10px var(--shadow);
        }
        #overview .day-overview h3 {
            margin-top: 0; margin-bottom: 0.5rem; font-size: 1.1rem;
        }
        #overview .day-overview h3 a { color: var(--primary-dark); }
        #overview .day-overview p { font-size: 0.95rem; margin-bottom: 0; }

        .back-to-top {
            display: none; position: fixed; bottom: 1.5rem; right: 1.5rem;
            background-color: var(--primary-color); color: white;
            padding: 0.6rem 1rem; border-radius: 50px; text-decoration: none;
            font-weight: bold; box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
            transition: background-color 0.2s, opacity 0.3s, visibility 0.3s;
            opacity: 0; visibility: hidden; z-index: 1000;
        }
        .back-to-top.visible {
            display: inline-block; opacity: 1; visibility: visible;
        }
        .back-to-top:hover { background-color: var(--primary-dark); }

        .emoji { margin-right: 5px; font-size: 1.1em; vertical-align: middle; }

        .birthday-badge {
            display: inline-block; background-color: var(--primary-color);
            color: white; font-weight: bold; padding: 0.3rem 0.8rem;
            border-radius: 20px; margin-left: 1rem; font-size: 0.9rem;
            vertical-align: middle; animation: pulse 2s infinite ease-in-out;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.08); }
            100% { transform: scale(1); }
        }

        .language-switcher {
            position: fixed; top: 1rem; right: 1rem;
            background-color: rgba(255, 255, 255, 0.9);
            padding: 0.3rem; border-radius: 20px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.2); z-index: 1001;
        }
        .language-switcher button {
            background: none; border: none; color: var(--text-color);
            font-weight: bold; cursor: pointer; margin: 0 0.2rem;
            padding: 0.3rem 0.8rem; border-radius: 15px;
            transition: background-color 0.2s, color 0.2s; font-size: 0.9rem;
        }
        .language-switcher button.active {
            background-color: var(--primary-dark); color: white;
        }
        .language-switcher button:not(.active):hover {
             background-color: var(--primary-light);
        }

        .lang-en .th, .lang-th .en { display: none; }
        .lang-th .th, .lang-en .en { display: inline; }
        .lang-en .en-block, .lang-th .th-block { display: block; }
        .lang-en .th-block, .lang-th .en-block { display: none; }

        @media (min-width: 768px) {
            .container { padding: 1.5rem; }
            header h1 { font-size: 2.2rem; }
            header h2 { font-size: 1.4rem; }
            section > h1 { font-size: 1.8rem; }
            section > h2 { font-size: 1.5rem; }
            #overview .day-overview { flex-basis: calc(50% - 0.5rem); }
        }
        @media (min-width: 1024px) {
            .container { padding: 2rem; }
            header h1 { font-size: 2.5rem; }
            #overview .day-overview { flex-basis: calc(33.333% - 0.67rem); }
        }
        @media (max-width: 767px) {
            th, td { padding: 0.6rem; font-size: 0.9rem; }
            .timeline li { padding-left: 2rem; }
            .timeline::before { left: calc(0.5rem + 7px - 1px); }
            .timeline li::before { left: 0.5rem; }
            header h1 { font-size: 1.6rem; padding-top: 3rem; }
            header h2 { font-size: 1.1rem; }
            section > h1 { font-size: 1.4rem; }
            section > h2 { font-size: 1.2rem; }
            .back-to-top { bottom: 1rem; right: 1rem; padding: 0.5rem 0.8rem; font-size: 0.9rem; }
            .language-switcher { top: 0.5rem; right: 0.5rem; }
        }

        @media print {
            .day-overview, table, .info-box, .note-box, .timeline li {
                break-inside: avoid; page-break-inside: avoid;
            }
            .back-to-top, .language-switcher { display: none; }
            body { background-color: white; padding-bottom: 0; }
            header { box-shadow: none; padding-top: 1.5rem; }
            header h1 { padding-top: 0; }
            .table-container { overflow-x: visible; }
            table { min-width: auto; }
        }
        '''
    
    def _get_javascript(self) -> str:
        """Return complete JavaScript functionality"""
        return f'''
        document.addEventListener("DOMContentLoaded", function () {{
            // --- Collapsible Sections ---
            document.querySelectorAll(".info-toggle, .note-toggle").forEach(button => {{
                const detail = button.nextElementSibling;
                if (detail && (detail.classList.contains('info-detail') || detail.classList.contains('note-detail'))) {{
                    button.classList.add("collapsed");
                    detail.classList.add("collapsed");

                    button.addEventListener("click", (e) => {{
                        if (e.target.tagName === 'A') return;
                        button.classList.toggle("collapsed");
                        detail.classList.toggle("collapsed");
                    }});

                    button.setAttribute('role', 'button');
                    button.setAttribute('tabindex', '0');
                    button.addEventListener('keydown', (e) => {{
                        if (e.key === 'Enter' || e.key === ' ') {{
                            e.preventDefault();
                            button.click();
                        }}
                    }});
                }}
            }});

            // --- Language Switching ---
            const langButtons = document.querySelectorAll('.language-switcher button');
            const body = document.body;
            let currentLang = localStorage.getItem('tripLanguage') || 'th';

            function setLanguage(lang) {{
                if (lang !== 'th' && lang !== 'en') lang = 'th';
                localStorage.setItem('tripLanguage', lang);
                currentLang = lang;
                body.className = `lang-${{lang}}`;

                langButtons.forEach(btn => {{
                    btn.classList.toggle('active', btn.dataset.lang === lang);
                }});

                const titleTh = "เที่ยวญี่ปุ่น Porjai: Birthday Trip 2026";
                const titleEn = "Porjai's Japan Trip: Birthday Adventure 2026";
                document.title = lang === 'th' ? titleTh : titleEn;
            }}

            langButtons.forEach(button => {{
                button.addEventListener('click', () => {{
                    setLanguage(button.dataset.lang);
                }});
            }});

            setLanguage(currentLang);

            // --- Currency Conversion (JPY to THB) ---
            const jpyToThbRate = {self.exchange_rate};

            const convertCurrency = () => {{
                document.querySelectorAll('[data-jpy]').forEach(el => {{
                    const jpyString = el.dataset.jpy.replace(/,/g, '');
                    const jpy = parseFloat(jpyString);
                    if (!isNaN(jpy)) {{
                        const thb = (jpy * jpyToThbRate).toFixed(0);
                        const jpyFormatted = `¥${{jpy.toLocaleString('en-US')}}`;
                        const thbFormatted = `฿${{parseInt(thb).toLocaleString('en-US')}}`;

                        let thbSpan = el.querySelector('.thb-amount');
                        if (!thbSpan) {{
                            if (el.tagName === 'TD' || el.tagName === 'STRONG') {{
                                el.innerHTML = `${{thbFormatted}}`;
                            }} else {{
                                el.innerHTML = `${{jpyFormatted}} <span class="thb-amount">(${{thbFormatted}})</span>`;
                            }}
                        }} else {{
                            el.innerHTML = `${{jpyFormatted}} <span class="thb-amount">(${{thbFormatted}})</span>`;
                        }}
                    }}
                }});
            }};

            convertCurrency();

            // --- Back to Top Button Visibility ---
            const backToTopBtn = document.querySelector('.back-to-top');
            if (backToTopBtn) {{
                window.addEventListener('scroll', () => {{
                    if (window.scrollY > 300) {{
                        backToTopBtn.classList.add('visible');
                    }} else {{
                        backToTopBtn.classList.remove('visible');
                    }}
                }});
            }}
        }});
        '''
    
    def generate(self) -> Path:
        """Generate the complete HTML file"""
        # Load all markdown sections
        self.load_all_sections()
        
        # Generate HTML content
        html_content = self.generate_html_template()
        
        # Create output filename with current date
        today = datetime.now().strftime("%Y%m%d")
        output_file = self.output_dir / f"Tokyo-Trip-March-2026-Claude-{today}.html"
        
        # Write the file
        output_file.write_text(html_content, encoding='utf-8')
        
        print(f"✅ Generated: {output_file}")
        print(f"📱 File size: {output_file.stat().st_size / 1024:.1f} KB")
        print(f"🌐 Ready for offline use on mobile devices!")
        
        return output_file

def main():
    """Main function to run the generator"""
    # Define paths
    script_dir = Path(__file__).parent
    content_dir = script_dir.parent / "content"
    output_dir = script_dir.parent / "build"
    
    # Check if content directory exists
    if not content_dir.exists():
        print(f"❌ Content directory not found: {content_dir}")
        print("Please ensure the 'content' directory exists with markdown files.")
        return
    
    # Create generator and run
    generator = TokyoTripGenerator(content_dir, output_dir)
    output_file = generator.generate()
    
    print("\n📋 Generation Summary:")
    print(f"   📂 Content dir: {content_dir}")
    print(f"   📁 Output dir: {output_dir}")
    print(f"   📄 Output file: {output_file.name}")
    print(f"   🔧 Sections processed: {len(generator.sections)}")
    print("\n🎉 Tokyo Trip Plan is ready!")
    print("   💡 Open the HTML file in any browser")
    print("   📱 Works offline on mobile devices")
    print("   🌏 Switch between Thai/English languages")

if __name__ == "__main__":
    main()