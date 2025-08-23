#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day-to-Day Tokyo Trip Generator - v4.0 (Time-Based Day Planner)
================================================================
สร้าง HTML ไฟล์สำหรับทริปโตเกียวแบบ day-to-day timeline ที่รวม:
- ที่พัก (Accommodation)
- การเดินทาง (Transportation)
- กิจกรรม (Activities)
- อาหาร (Food)
ในแต่ละวันเป็นแผนงานแบบ timeline พร้อม expand/collapse รายละเอียด

✨ Version 4.0 Features:
- Day-to-day timeline structure
- Integrated accommodation, transport, activities per day
- Collapsible overview/details sections
- SPA functionality with printer-friendly mode
- Responsive design for mobile/desktop
- Clean, modern UI focused on daily planning

Author: Claude AI Assistant (Day-to-Day Redesign)
Date: 23 August 2025
Version: 4.0.0-day-to-day-timeline
"""

import os
import re
import datetime
from pathlib import Path

class DayToDayTokyoGenerator:
    """
    Day-to-Day timeline generator จัดโครงสร้างแบบวันต่อวัน
    """
    def __init__(self):
        # Setup paths
        self.script_dir = Path(__file__).parent
        self.project_dir = self.script_dir.parent
        self.content_dir = self.project_dir / "content"
        self.th_dir = self.content_dir / "th"
        self.en_dir = self.content_dir / "en"
        self.build_dir = self.project_dir / "build"

        # Create build directory if not exists
        self.build_dir.mkdir(exist_ok=True)

        print("🚀 Day-to-Day Tokyo Trip Generator v4.0")
        print(f"   - Project Dir: {self.project_dir}")
        print(f"   - Content Dir: {self.content_dir}")
        print(f"   - Build Dir:   {self.build_dir}")

    def read_file(self, file_path):
        """อ่านไฟล์ด้วย UTF-8 encoding"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"⚠️ File not found: {file_path}")
            return ""
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return ""

    def get_content_data(self):
        """อ่านไฟล์ content ทั้งหมดและจัดโครงสร้างข้อมูล"""
        print("📂 Reading content files...")
        content_data = {}

        # อ่านไฟล์ภาษาไทย (หลัก)
        if self.th_dir.exists():
            for md_file in sorted(self.th_dir.glob("*.md")):
                file_key = md_file.stem
                content_data[file_key] = {
                    'th': self.read_file(md_file),
                    'en': ''
                }
        else:
            print(f"❌ Thai content directory not found: {self.th_dir}")
            return {}

        # อ่านไฟล์ภาษาอังกฤษ (ถ้ามี)
        if self.en_dir.exists():
            for md_file in sorted(self.en_dir.glob("*.md")):
                file_key = md_file.stem
                if file_key in content_data:
                    content_data[file_key]['en'] = self.read_file(md_file)

        print(f"   - Found {len(content_data)} content entries.")
        return content_data

    def extract_day_info(self, content_data):
        """แยกข้อมูลแต่ละวันออกจาก content files - ใช้เนื้อหาต้นฉบับที่สมบูรณ์"""
        print("📅 Extracting day-by-day information...")
        
        days_data = {}
        
        # หา day files (003-day1, 004-day2, etc.)
        day_keys = sorted([k for k in content_data if re.match(r'^\d+-day\d+', k)])
        
        for key in day_keys:
            day_num = re.search(r'day(\d+)', key).group(1)
            content = content_data[key]
            th_md = content.get('th', '')
            
            # ใช้เนื้อหาต้นฉบับทั้งหมด แค่แยกหัวข้อหลัก
            day_data = {
                'day_number': int(day_num),
                'title': self._extract_title(th_md),
                'date': self._extract_date(th_md),
                'full_content': th_md,  # เก็บเนื้อหาเต็ม
                'timeline_section': self._extract_timeline_section(th_md),
                'additional_sections': self._extract_additional_sections(th_md)
            }
            
            days_data[int(day_num)] = day_data
            print(f"   ✅ Day {day_num}: {day_data['title']}")
        
        return days_data

    def _extract_title(self, md_content):
        """Extract day title"""
        match = re.search(r'^# (.*)', md_content, re.MULTILINE)
        return match.group(1).strip() if match else "วันที่ N/A"

    def _extract_date(self, md_content):
        """Extract date information"""
        match = re.search(r'\*\*วันที่:\*\*\s*([^\n]+)', md_content)
        if match:
            return match.group(1).strip()
        
        # Fallback: look for date in title
        date_match = re.search(r'(\d+ มี\.?ค\.? \d{4})', md_content)
        return date_match.group(1) if date_match else ""

    def _extract_timeline_section(self, md_content):
        """Extract timeline section from markdown"""
        # หา section ที่เริ่มด้วย ## ⏰ Timeline รายละเอียด
        timeline_match = re.search(r'## ⏰ Timeline รายละเอียด\s*\n(.*?)(?=\n## |$)', md_content, re.DOTALL)
        if timeline_match:
            return timeline_match.group(1).strip()
        return ""

    def _extract_additional_sections(self, md_content):
        """Extract additional sections after timeline"""
        # หา sections หลัก ## ที่ไม่ใช่ timeline
        sections = {}
        
        # Split เนื้อหาด้วย ## headings
        section_pattern = r'## ([^\n]+)\s*\n(.*?)(?=\n## |$)'
        section_matches = re.findall(section_pattern, md_content, re.DOTALL)
        
        for title, content in section_matches:
            if 'Timeline รายละเอียด' not in title:  # Skip timeline section
                sections[title.strip()] = content.strip()
        
        return sections

    def markdown_to_html_simple(self, md_text):
        """Convert markdown to HTML แบบง่าย สำหรับ content sections"""
        if not md_text:
            return ""
        
        html = md_text
        
        # Headers
        html = re.sub(r'^### (.*)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Lists
        html = self._convert_lists_simple(html)
        
        # Tables
        html = self._convert_tables_simple(html)
        
        # Paragraphs
        html = self._convert_paragraphs_simple(html)
        
        return html

    def _convert_lists_simple(self, text):
        """Convert markdown lists to HTML"""
        lines = text.split('\n')
        result = []
        in_list = False
        
        for line in lines:
            if line.strip().startswith('- '):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                item_content = line.strip()[2:]
                result.append(f'  <li>{item_content}</li>')
            else:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                result.append(line)
        
        if in_list:
            result.append('</ul>')
        
        return '\n'.join(result)

    def _convert_tables_simple(self, text):
        """Convert markdown tables to HTML"""
        lines = text.split('\n')
        result = []
        in_table = False
        
        for i, line in enumerate(lines):
            if '|' in line and line.count('|') >= 2:
                if not in_table:
                    result.append('<div class="table-container"><table class="table">')
                    in_table = True
                    # Check if next line is separator
                    if i + 1 < len(lines) and '---' in lines[i + 1]:
                        # This is header row
                        cells = [cell.strip() for cell in line.split('|')[1:-1]]
                        result.append('<thead><tr>' + ''.join(f'<th>{cell}</th>' for cell in cells) + '</tr></thead><tbody>')
                        continue
                
                # Regular row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                result.append('<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>')
            elif '---' in line and in_table:
                # Skip separator line
                continue
            else:
                if in_table:
                    result.append('</tbody></table></div>')
                    in_table = False
                result.append(line)
        
        if in_table:
            result.append('</tbody></table></div>')
        
        return '\n'.join(result)

    def _convert_paragraphs_simple(self, text):
        """Convert text to paragraphs"""
        paragraphs = text.split('\n\n')
        result = []
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Skip if already HTML or header
            if para.startswith(('<', '#')):
                result.append(para)
            else:
                # Split by single newlines and wrap each non-empty line
                lines = para.split('\n')
                processed = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('<'):
                        processed.append(f'<p>{line}</p>')
                    elif line:
                        processed.append(line)
                result.append('\n'.join(processed))
        
        return '\n\n'.join(result)


    def _clean_markdown_formatting(self, text):
        """Clean markdown formatting from text"""
        if not text:
            return ""
        
        # Remove markdown formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'`(.*?)`', r'\1', text)
        
        return text.strip()

    def generate_day_html(self, day_data):
        """Generate HTML for a single day - ใช้เนื้อหาต้นฉบับที่สมบูรณ์"""
        day_num = day_data['day_number']
        
        # Determine if it's birthday day
        is_birthday = day_num == 4
        birthday_class = ' birthday-day' if is_birthday else ''
        birthday_badge = '🎂' if is_birthday else ''
        
        # Build timeline section (main activities)
        timeline_html = self.markdown_to_html_simple(day_data['timeline_section'])
        
        # Build additional sections
        additional_sections_html = ""
        for section_title, section_content in day_data['additional_sections'].items():
            if section_content.strip():
                section_html = self.markdown_to_html_simple(section_content)
                additional_sections_html += f'''
                <div class="day-section collapsible">
                    <h3 onclick="toggleSection(this)">📋 {section_title} <span class="toggle-icon">▼</span></h3>
                    <div class="section-content">
                        {section_html}
                    </div>
                </div>'''
        
        return f'''
        <div class="day-card{birthday_class}" id="day{day_num}">
            <div class="day-header" onclick="toggleDay({day_num})">
                <div class="day-number">{birthday_badge} Day {day_num}</div>
                <div class="day-title">{day_data['title']}</div>
                <div class="day-date">{day_data['date']}</div>
                <div class="expand-indicator">▼</div>
            </div>
            
            <div class="day-content" id="day-content-{day_num}">
                <div class="day-sections">
                    
                    <!-- Main Timeline -->
                    <div class="day-section timeline-section">
                        <h3>⏰ กิจกรรมตามเวลา</h3>
                        <div class="section-content">
                            {timeline_html}
                        </div>
                    </div>
                    
                    <!-- Additional Sections -->
                    {additional_sections_html}
                    
                </div>
            </div>
        </div>
        '''


    def generate_complete_html(self, days_data):
        """Generate complete HTML document"""
        print("🏗️ Building complete day-to-day HTML...")
        
        # Generate days HTML
        days_html = ""
        for day_num in sorted(days_data.keys()):
            days_html += self.generate_day_html(days_data[day_num])
        
        # Get CSS and JavaScript
        css = self._get_day_to_day_css()
        js = self._get_day_to_day_js()
        
        return f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ทริปโตเกียว มีนาคม 2026 - Day-to-Day Planner</title>
    <style>{css}</style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🗼 ทริปโตเกียว มีนาคม 2026</h1>
            <p class="subtitle">Day-to-Day Travel Planner | 8 วัน 7 คืน</p>
            <div class="header-actions">
                <button onclick="expandAll()">📖 ดูทั้งหมด</button>
                <button onclick="collapseAll()">📑 ย่อทั้งหมด</button>
                <button onclick="togglePrintMode()">🖨️ โหมดพิมพ์</button>
            </div>
        </div>
        
        <!-- Trip Overview -->
        <div class="trip-overview">
            <div class="overview-stats">
                <div class="stat">
                    <span class="stat-number">{len(days_data)}</span>
                    <span class="stat-label">วัน</span>
                </div>
                <div class="stat">
                    <span class="stat-number">7</span>
                    <span class="stat-label">คืน</span>
                </div>
                <div class="stat">
                    <span class="stat-number">3</span>
                    <span class="stat-label">เมือง</span>
                </div>
                <div class="stat special">
                    <span class="stat-number">🎂</span>
                    <span class="stat-label">Birthday</span>
                </div>
            </div>
        </div>
        
        <!-- Days Container -->
        <div class="days-container" id="days-container">
            {days_html}
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Generated on {datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
            <p>🎉 Happy 11th Birthday น้องพอใจ! 🎂</p>
        </div>
    </div>
    
    <script>{js}</script>
</body>
</html>'''

    def _get_day_to_day_css(self):
        """Get CSS for day-to-day layout"""
        return '''
        :root {
            --primary: #2E86AB;
            --secondary: #A23B72;
            --accent: #F18F01;
            --success: #C73E1D;
            --background: #F8FAFC;
            --card-bg: #FFFFFF;
            --text-primary: #2C3E50;
            --text-secondary: #64748B;
            --border: #E2E8F0;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --border-radius: 12px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background: linear-gradient(135deg, var(--background) 0%, #E8F4FD 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 1rem;
        }

        .header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            margin-bottom: 2rem;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }

        .header .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1.5rem;
        }

        .header-actions {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }

        .header-actions button {
            padding: 0.75rem 1.5rem;
            border: 2px solid rgba(255,255,255,0.3);
            background: rgba(255,255,255,0.1);
            color: white;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: var(--transition);
            backdrop-filter: blur(10px);
        }

        .header-actions button:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }

        .trip-overview {
            background: var(--card-bg);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            padding: 1.5rem;
            margin-bottom: 2rem;
        }

        .overview-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            text-align: center;
        }

        .stat {
            padding: 1rem;
            border-radius: var(--border-radius);
            background: var(--background);
        }

        .stat.special {
            background: linear-gradient(135deg, #FFE5CC 0%, #FFF8E7 100%);
        }

        .stat-number {
            display: block;
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
        }

        .stat-label {
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        .days-container {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .day-card {
            background: var(--card-bg);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: var(--transition);
        }

        .day-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }

        .day-card.birthday-day {
            border: 3px solid var(--accent);
            background: linear-gradient(135deg, var(--card-bg) 0%, #FFF8E7 100%);
        }

        .day-header {
            padding: 1.5rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 1rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            transition: var(--transition);
        }

        .day-header:hover {
            background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%);
        }

        .day-number {
            font-size: 1.2rem;
            font-weight: 700;
            min-width: 80px;
        }

        .day-title {
            flex: 1;
            font-size: 1.3rem;
            font-weight: 600;
        }

        .day-date {
            font-size: 0.9rem;
            opacity: 0.9;
        }

        .expand-indicator {
            font-size: 1.2rem;
            transition: transform 0.3s ease;
        }

        .day-card.expanded .expand-indicator {
            transform: rotate(180deg);
        }

        .day-content {
            display: none;
            padding: 1.5rem;
            border-top: 1px solid var(--border);
        }

        .day-content.expanded {
            display: block;
        }

        .day-sections {
            display: grid;
            gap: 1.5rem;
        }

        .day-section {
            background: var(--background);
            border-radius: var(--border-radius);
            padding: 1rem;
        }

        .day-section h3 {
            color: var(--primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.1rem;
        }

        .day-section.collapsible h3 {
            cursor: pointer;
            transition: var(--transition);
        }

        .day-section.collapsible h3:hover {
            color: var(--secondary);
        }

        .day-section.collapsible .section-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }

        .day-section.collapsible.expanded .section-content {
            max-height: 1000px;
        }

        .toggle-icon {
            margin-left: auto;
            transition: transform 0.3s ease;
        }

        .day-section.collapsible.expanded .toggle-icon {
            transform: rotate(180deg);
        }

        .activities-timeline {
            display: grid;
            gap: 0.75rem;
        }

        .activity-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.75rem;
            background: var(--card-bg);
            border-radius: 8px;
            border-left: 4px solid var(--primary);
        }

        .activity-item.activity-highlight {
            border-left-color: var(--accent);
        }

        .activity-time {
            font-weight: 600;
            color: var(--primary);
            min-width: 80px;
            font-size: 0.9rem;
        }

        .activity-content {
            flex: 1;
        }

        .section-content ul {
            list-style: none;
            padding: 0;
        }

        .section-content li {
            padding: 0.5rem 0;
            border-bottom: 1px solid var(--border);
        }

        .section-content li:last-child {
            border-bottom: none;
        }

        .footer {
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            color: var(--text-secondary);
            border-top: 1px solid var(--border);
        }

        /* Print Mode Styles */
        .print-mode {
            background: white !important;
        }

        .print-mode .day-content {
            display: block !important;
        }

        .print-mode .header-actions {
            display: none;
        }

        .print-mode .expand-indicator {
            display: none;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 0.5rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .day-header {
                padding: 1rem;
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }
            
            .day-title {
                font-size: 1.1rem;
            }
            
            .activities-timeline {
                gap: 0.5rem;
            }
            
            .activity-item {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }
            
            .activity-time {
                min-width: auto;
            }
            
            .overview-stats {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media print {
            body {
                background: white !important;
            }
            
            .day-content {
                display: block !important;
            }
            
            .header-actions,
            .expand-indicator {
                display: none !important;
            }
            
            .day-card {
                break-inside: avoid;
                margin-bottom: 1rem;
            }
        }
        '''

    def _get_day_to_day_js(self):
        """Get JavaScript for day-to-day functionality"""
        return '''
        function toggleDay(dayNum) {
            const dayCard = document.getElementById('day' + dayNum);
            const dayContent = document.getElementById('day-content-' + dayNum);
            
            if (dayContent.style.display === 'none' || !dayContent.style.display) {
                dayContent.style.display = 'block';
                dayContent.classList.add('expanded');
                dayCard.classList.add('expanded');
            } else {
                dayContent.style.display = 'none';
                dayContent.classList.remove('expanded');
                dayCard.classList.remove('expanded');
            }
        }

        function toggleSection(headerElement) {
            const section = headerElement.parentElement;
            section.classList.toggle('expanded');
        }

        function expandAll() {
            const dayContents = document.querySelectorAll('.day-content');
            const dayCards = document.querySelectorAll('.day-card');
            
            dayContents.forEach(content => {
                content.style.display = 'block';
                content.classList.add('expanded');
            });
            
            dayCards.forEach(card => {
                card.classList.add('expanded');
            });
        }

        function collapseAll() {
            const dayContents = document.querySelectorAll('.day-content');
            const dayCards = document.querySelectorAll('.day-card');
            
            dayContents.forEach(content => {
                content.style.display = 'none';
                content.classList.remove('expanded');
            });
            
            dayCards.forEach(card => {
                card.classList.remove('expanded');
            });
        }

        function togglePrintMode() {
            document.body.classList.toggle('print-mode');
            
            if (document.body.classList.contains('print-mode')) {
                expandAll();
            }
        }

        // Auto-open Day 1 on load
        document.addEventListener('DOMContentLoaded', function() {
            toggleDay(1);
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 'e':
                        e.preventDefault();
                        expandAll();
                        break;
                    case 'c':
                        e.preventDefault(); 
                        collapseAll();
                        break;
                    case 'p':
                        e.preventDefault();
                        togglePrintMode();
                        break;
                }
            }
        });
        '''

    def generate(self):
        """Main generation process"""
        print("\n🚀 Starting Day-to-Day HTML generation...")
        
        # Get content data
        content_data = self.get_content_data()
        if not content_data:
            print("❌ No content found. Aborting.")
            return
        
        # Extract day-by-day info
        days_data = self.extract_day_info(content_data)
        if not days_data:
            print("❌ No day data found. Aborting.")
            return
        
        # Generate complete HTML
        html_content = self.generate_complete_html(days_data)
        
        # Generate output filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_filename = f"Tokyo-Trip-Day-to-Day-v4.0-{timestamp}.html"
        output_path = self.build_dir / output_filename
        
        # Write file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            file_size = output_path.stat().st_size
            print("\n🎉 Day-to-Day HTML generation complete!")
            print(f"   - File: {output_filename}")
            print(f"   - Path: {output_path}")
            print(f"   - Size: {file_size / 1024:.2f} KB")
            print("\n🔥 Version 4.0 Features:")
            print("   ✅ Day-to-Day timeline structure")
            print("   ✅ Integrated accommodation, transport, activities")
            print("   ✅ Collapsible overview/details sections")  
            print("   ✅ SPA functionality")
            print("   ✅ Printer-friendly mode")
            print("   ✅ Responsive mobile design")
            print("   ✅ Keyboard shortcuts (Ctrl+E/C/P)")
            print("   ✅ Auto-open Day 1 on load")
            
        except Exception as e:
            print(f"❌ Error writing HTML file: {e}")

def main():
    """Main function"""
    print("🗼 Day-to-Day Tokyo Trip Generator v4.0")
    print("=" * 60)
    print("🆕 Features:")
    print("   - Time-based day planner")
    print("   - Integrated daily sections")
    print("   - Expand/collapse functionality") 
    print("   - SPA with printer mode")
    print("   - Mobile-responsive design")
    print("=" * 60)
    
    generator = DayToDayTokyoGenerator()
    generator.generate()

if __name__ == "__main__":
    main()