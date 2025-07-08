#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokyo Trip Generator - v3.1 (Multi-Timeline & Section Fix)
==========================================================
สร้าง HTML ไฟล์สำหรับทริปโตเกียว โดยอ่านเนื้อหาจาก content/*.md 
และใส่ลงใน skeleton template ที่มี CSS/JS สมบูรณ์

✨ Version 3.1 Features:
- แก้ไขปัญหา "Double Processing" ด้วย Placeholder Strategy
- ใช้ skeleton_template.html เป็นโครงสร้างหลัก
- รองรับ Multiple Timeline Formats (Time-based, Highlight, Step-based)
- แก้ไข Section Markers (--- และ ```) ให้หายไป
- Markdown Parser ที่แม่นยำสำหรับ Timeline, Tables, Info/Note Boxes
- รองรับ Multi-language (TH/EN) อย่างสมบูรณ์

Author: Claude AI Assistant (Fixed & Enhanced)
Date: 7 July 2025
Version: 3.1.0-multi-timeline-section-fix
"""

import os
import re
import datetime
from pathlib import Path

class TokyoTripGeneratorV3:
    """
    Generator ที่แก้ไขปัญหา Double Processing ด้วย Placeholder Strategy
    รองรับ Multiple Timeline Formats และแก้ไข Section Markers
    """
    def __init__(self):
        # Setup paths
        self.script_dir = Path(__file__).parent
        self.project_dir = self.script_dir.parent
        self.content_dir = self.project_dir / "content"
        self.th_dir = self.content_dir / "th"
        self.en_dir = self.content_dir / "en"
        self.build_dir = self.project_dir / "build"
        self.template_path = self.script_dir / "template" / "skeleton_template.html"

        # Create build directory if not exists
        self.build_dir.mkdir(exist_ok=True)

        print("🚀 Tokyo Trip Generator v3.1 - Multi-Timeline & Section Fix")
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

    def get_skeleton_template(self):
        """อ่าน skeleton template HTML จากไฟล์"""
        print(f"📄 Reading skeleton template from: {self.template_path}")
        return self.read_file(self.template_path)

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

        # อ่านไฟล์ภาษาอังกฤษ (ถ้ามี) และจับคู่กับภาษาไทย
        if self.en_dir.exists():
            for md_file in sorted(self.en_dir.glob("*.md")):
                file_key = md_file.stem
                if file_key in content_data:
                    content_data[file_key]['en'] = self.read_file(md_file)
                else:
                    # กรณีมีไฟล์ EN แต่ไม่มี TH
                    content_data[file_key] = {'th': '', 'en': self.read_file(md_file)}

        print(f"   - Found {len(content_data)} content entries.")
        return content_data

    def markdown_to_html(self, markdown_text):
        """
        🔥 THE MAGIC FUNCTION! 
        Converts Markdown to HTML using PLACEHOLDER STRATEGY to prevent
        double-processing of complex elements like timelines and tables.
        
        🎯 Strategy: Isolate -> Convert -> Replace
        🆕 v3.1: รองรับ Multiple Timeline Formats และแก้ไข Section Markers
        """
        if not markdown_text or not markdown_text.strip():
            return ""

        placeholders = {}
        placeholder_counter = 0
        
        def add_placeholder(html_content):
            nonlocal placeholder_counter
            placeholder = f"__PLACEHOLDER_{placeholder_counter}__"
            placeholders[placeholder] = html_content
            placeholder_counter += 1
            return placeholder

        text = markdown_text

        # 🎯 STEP 1: Handle section markers and clean up content
        print("   🔧 Processing section markers...")
        
        # Remove or convert section markers (--- และ ```)
        text = re.sub(r'^```\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^---\s*$', '\n', text, flags=re.MULTILINE)
        
        # 🎯 STEP 2: Process and replace complex blocks with placeholders
        print("   🔧 Processing complex blocks with placeholder strategy...")
        
        # Tables (highest priority - most complex structure)
        table_pattern = re.compile(r'((?:^\|.*\|.*\n(?:\|.*\|-.*\|.*\n)?(?:\|.*\|.*\n)*)+)', re.MULTILINE)
        tables_found = table_pattern.findall(text)
        if tables_found:
            print(f"   📊 Found {len(tables_found)} tables")
            def table_repl(match):
                return add_placeholder(self._process_table_block(match.group(0)))
            text = table_pattern.sub(table_repl, text)

        # Info/Note Boxes
        box_pattern = re.compile(r'((?:^> \*\*.*?\*\*.*\n(?:^> .*\n?)*)+)', re.MULTILINE)
        boxes_found = box_pattern.findall(text)
        if boxes_found:
            print(f"   📦 Found {len(boxes_found)} info/note boxes")
            def box_repl(match):
                return add_placeholder(self._process_infobox_block(match.group(0)))
            text = box_pattern.sub(box_repl, text)

        # 🌟 Extended Timeline Patterns (multiple formats)
        # 1. Time-based timelines: - **HH:MM**: content
        timeline_time_pattern = re.compile(r'((?:^- \*\*\d+:\d+\*\*:.*\n(?:  .*\n?)*)+)', re.MULTILINE)
        # 2. Highlight timelines: - **text**: content (for daily highlights)
        timeline_highlight_pattern = re.compile(r'((?:^- \*\*(?!\d+:\d+)[^*]+\*\*:.*\n(?:  .*\n?)*)+)', re.MULTILINE)
        # 3. Step-based timelines: - **Step N**: content
        timeline_step_pattern = re.compile(r'((?:^- \*\*(?:Step|ขั้นตอน|ไฮไลต์|รายละเอียด)[^*]*\*\*:.*\n(?:  .*\n?)*)+)', re.MULTILINE)
        # 4. 🆕 H3-based timelines: ### Title + content below
        timeline_h3_pattern = re.compile(r'((?:^### [^\n]+\n(?:(?!^###)[^\n]*\n?)*)+)', re.MULTILINE)
        
        # Process time-based timelines first (highest priority)
        timelines_found = timeline_time_pattern.findall(text)
        if timelines_found:
            print(f"   ⏰ Found {len(timelines_found)} time-based timeline blocks")
            def timeline_repl(match):
                return add_placeholder(self._process_timeline_block(match.group(1), 'time'))
            text = timeline_time_pattern.sub(timeline_repl, text)
            
        # Process highlight timelines
        highlight_timelines_found = timeline_highlight_pattern.findall(text)
        if highlight_timelines_found:
            print(f"   🌟 Found {len(highlight_timelines_found)} highlight timeline blocks")
            def highlight_timeline_repl(match):
                return add_placeholder(self._process_timeline_block(match.group(1), 'highlight'))
            text = timeline_highlight_pattern.sub(highlight_timeline_repl, text)
            
        # Process step-based timelines
        step_timelines_found = timeline_step_pattern.findall(text)
        if step_timelines_found:
            print(f"   📋 Found {len(step_timelines_found)} step timeline blocks")
            def step_timeline_repl(match):
                return add_placeholder(self._process_timeline_block(match.group(1), 'step'))
            text = timeline_step_pattern.sub(step_timeline_repl, text)
            
        # 🆕 Process H3-based timelines (### headings)
        h3_timelines_found = timeline_h3_pattern.findall(text)
        if h3_timelines_found:
            print(f"   🏨 Found {len(h3_timelines_found)} H3-based timeline blocks")
            def h3_timeline_repl(match):
                return add_placeholder(self._process_h3_timeline_block(match.group(1)))
            text = timeline_h3_pattern.sub(h3_timeline_repl, text)

        # 🎯 STEP 3: Process the remaining simple markdown (now safe from interference)
        print("   🔧 Processing simple markdown...")
        html = text
        
        # Headers (order matters: longer first)
        html = re.sub(r'^#### (.*)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Text formatting
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Simple lists (now safe because complex timelines are placeholder-protected)
        html = self._convert_simple_lists(html)
        
        # Paragraphs (last)
        html = self._convert_paragraphs(html)

        # 🎯 STEP 4: Restore the complex blocks from placeholders
        print("   🔧 Restoring complex blocks from placeholders...")
        for placeholder, content in placeholders.items():
            html = html.replace(placeholder, content)

        return html.strip()

    def _process_timeline_block(self, timeline_md, timeline_type='time'):
        """
        🕐 Processes a block of timeline Markdown into a complete HTML <ul class="timeline">.
        This follows the EXACT structure from template.html.old for perfect CSS compatibility.
        
        🆕 v3.1: รองรับ Multiple Timeline Formats!
        - time: ⏰ เวลา (HH:MM)
        - highlight: 🌟 ไฮไลต์ประจำวัน
        - step: 📋 ขั้นตอน/รายละเอียด
        """
        print(f"      ⏰ Processing {timeline_type} timeline block...")
        
        timeline_items = []
        
        # Parse timeline entries: Handle both time-based and text-based
        lines = timeline_md.strip().split('\n')
        current_entry = None
        
        for line in lines:
            # Check if this is a new timeline entry (flexible pattern)
            timeline_match = re.match(r'^- \*\*([^*]+)\*\*:\s*(.*)', line)
            if timeline_match:
                # Save previous entry if exists
                if current_entry:
                    timeline_items.append(self._build_timeline_item(current_entry, timeline_type))
                
                # Start new entry
                current_entry = {
                    'time': timeline_match.group(1),  # Could be time or text
                    'main_content': timeline_match.group(2).strip(),
                    'details': []
                }
            elif line.startswith('  ') and current_entry:
                # This is a detail line (indented with 2+ spaces)
                detail = line.strip()
                if detail:
                    current_entry['details'].append(detail)
        
        # Don't forget the last entry!
        if current_entry:
            timeline_items.append(self._build_timeline_item(current_entry, timeline_type))
        
        # Generate final timeline HTML exactly like template.html.old
        final_timeline = f'<ul class="timeline">\n' + '\n'.join(timeline_items) + '\n</ul>'
        print(f"      ✅ Generated {timeline_type} timeline with {len(timeline_items)} items")
        return final_timeline
        
    def _process_h3_timeline_block(self, h3_block):
        """
        🏨 Processes H3-based blocks into timeline format
        ### Title \n content... → timeline item with details
        """
        print("      🏨 Processing H3-based timeline block...")
        
        timeline_items = []
        
        # Split by ### to get individual items
        h3_items = re.split(r'^### ', h3_block, flags=re.MULTILINE)[1:]  # Skip first empty item
        
        for item in h3_items:
            lines = item.strip().split('\n')
            if not lines:
                continue
                
            # First line is the title
            title = lines[0].strip()
            
            # Rest is content (details)
            content_lines = lines[1:] if len(lines) > 1 else []
            
            # Create timeline entry
            entry = {
                'time': title,  # H3 title becomes timeline label
                'main_content': '',  # No separate main content for H3 format
                'details': content_lines # Pass raw lines to be processed by _process_timeline_details
            }
            
            timeline_items.append(self._build_timeline_item(entry, 'h3'))
        
        # Generate final timeline HTML
        final_timeline = f'<ul class="timeline">\n' + '\n'.join(timeline_items) + '\n</ul>'
        print(f"      ✅ Generated H3 timeline with {len(timeline_items)} items")
        return final_timeline
        
    def _build_timeline_item(self, entry, timeline_type='time'):
        """
        Build individual timeline <li> item following template.html.old structure
        🆕 v3.1: รองรับ different timeline types
        """
        time = entry['time']
        main_content = entry['main_content']
        details = entry['details']
        
        # Generate unique timeline ID
        timeline_id = f"timeline-{timeline_type}-{hash(time + main_content) % 10000}"
        
        # Start with timeline-main div (format depends on type)
        if timeline_type == 'time' and re.match(r'\d+:\d+', time):
            # Time format: 09:00
            item_html = f'<div class="timeline-main"><strong>{time}:</strong> {main_content}</div>'
        elif timeline_type == 'h3':
            # H3 format: just the title (no colon)
            item_html = f'<div class="timeline-main"><strong>{time}</strong></div>'
        else:
            # Text format: ไฮไลต์ประจำวัน, ขั้นตอนที่ 1, etc.
            item_html = f'<div class="timeline-main"><strong>{time}:</strong> {main_content}</div>'
        
        # Add button and detail div if there are details
        if details:
            # Process details (could be markdown-like)
            details_html = self._process_timeline_details(details)
            
            item_html += f'''
                <button class="timeline-toggle" onclick="toggleTimelineDetail('{timeline_id}')">
                    <span class="th">รายละเอียด ▼</span>
                    <span class="en">Details ▼</span>
                </button>
                <div class="timeline-detail" id="{timeline_id}" style="display: none;">
                    {details_html}
                </div>'''
        
        return f'                <li>\n                    {item_html}\n                </li>'
    
    def _process_timeline_details(self, details):
        """
        Process timeline detail lines into proper HTML like template.html.old
        🆕 v3.1 FIXED: Handles both old (emoji-based) and new (H3-based) detail formats.
        - Emoji lines or **Bold** lines -> <h4>
        - "- item" -> <ul><li>...</li></ul>
        - Other lines -> <p> with inline formatting
        """
        html_parts = []
        in_list = False

        def close_list_if_open():
            nonlocal in_list
            if in_list:
                html_parts.append('</ul>')
                in_list = False

        def process_inline_formatting(text):
            text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
            return text

        for detail_line in details:
            stripped_line = detail_line.strip()
            if not stripped_line:
                continue

            # Check for headers (Emoji or **Bold** lines)
            # Added '📅' for check-in/out lines
            emoji_header_pattern = r'^[🚊🎟️🎂📋🗺️🍽️🎪🛍️🏨🎯🚇🏃‍♂️💰🎌🎭🎨🎵🎮🏟️🎢🎡🎠🎈🎉🎊🎁🎀🎄🎃🍰🧁🍭🍬🍫🍩🍪🥧🍺🍻🥂🍾🍷🍸🍹🍴🥄🔸📍⭐🌟💫⚡🔥❄️🌸🌺🌻🌷🌹🏔️🗻🏕️🏞️🚲🚗🚕🚌🚎🏍️✈️🚁⛴️🚤⛵🎫💳💴💵💶💷🧾📅]'
            bold_header_pattern = r'^\s*\*\*([^*]+)\*\*.*'
            
            if re.match(emoji_header_pattern, stripped_line) or re.match(bold_header_pattern, stripped_line):
                close_list_if_open()
                html_parts.append(f'<h4>{process_inline_formatting(stripped_line)}</h4>')
            
            # Check for list items
            elif stripped_line.startswith('- '):
                if not in_list:
                    html_parts.append('<ul>')
                    in_list = True
                item_content = stripped_line[2:].strip()
                html_parts.append(f'<li>{process_inline_formatting(item_content)}</li>')
            
            # Otherwise, it's a paragraph
            else:
                close_list_if_open()
                html_parts.append(f'<p>{process_inline_formatting(stripped_line)}</p>')

        # Close any open list at the end
        close_list_if_open()
        
        return '\n                    '.join(html_parts)

    def _process_table_block(self, table_md):
        """
        📊 Processes a Markdown table into HTML table with responsive wrapper
        """
        print("      📊 Processing table block...")
        
        lines = [line.strip() for line in table_md.strip().split('\n') if line.strip()]
        if len(lines) < 2:
            return table_md  # Not a valid table
            
        # Check if second line is separator
        if not re.match(r'^\|\s*[-:]+\s*(\|\s*[-:]+\s*)*\|?\s*$', lines[1]):
            return table_md  # Not a valid table
        
        # Extract headers
        headers = [h.strip() for h in lines[0].strip('|').split('|')]
        
        # Extract rows
        rows = []
        for line in lines[2:]:
            cells = [c.strip() for c in line.strip('|').split('|')]
            rows.append(cells)
        
        # Generate HTML with responsive wrapper
        html = '<div class="table-container">\n<table class="table">\n'
        html += '<thead><tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead>\n'
        html += '<tbody>\n'
        for row in rows:
            html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>\n'
        html += '</tbody>\n</table>\n</div>'
        
        print(f"      ✅ Generated table with {len(headers)} columns and {len(rows)} rows")
        return html

    def _process_infobox_block(self, box_md):
        """
        📦 Processes info/note box Markdown into collapsible HTML
        """
        print("      📦 Processing info/note box...")
        
        # Extract title and content
        lines = box_md.strip().split('\n')
        first_line = lines[0]
        
        # Extract box type and title from first line
        title_match = re.match(r'^> \*\*(\w+):\*\*\s*(.*)', first_line)
        if not title_match:
            return box_md  # Invalid format
        
        box_type = title_match.group(1).lower()
        title = title_match.group(2).strip()
        
        # Extract content (remove > prefix)
        content_lines = []
        for line in lines[1:]:
            if line.startswith('> '):
                content_lines.append(line[2:])
            elif line.startswith('>'):
                content_lines.append(line[1:])
        
        content_md = '\n'.join(content_lines).strip()
        content_html = self._simple_markdown_to_html(content_md)
        
        # Determine box class based on type
        box_class = "note-box" if "note" in box_type else "info-box"
        toggle_class = "note-toggle" if "note" in box_type else "info-toggle"
        detail_class = "note-detail" if "note" in box_type else "info-detail"
        
        html = f'''<div class="{box_class}">
    <div class="{toggle_class}">
        <span class="th">{title}</span>
        <span class="en">{title}</span>
    </div>
    <div class="{detail_class}">
        {content_html}
    </div>
</div>'''
        
        print(f"      ✅ Generated {box_type} box: {title}")
        return html

    def _simple_markdown_to_html(self, md):
        """Simple markdown conversion for nested content (no complex blocks)"""
        html = md
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Simple paragraphs
        paragraphs = html.split('\n\n')
        processed = []
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith('<'):
                processed.append(f'<p>{p}</p>')
            else:
                processed.append(p)
        
        return '\n'.join(processed)

    def _convert_simple_lists(self, text):
        """
        Convert simple lists (now safe from timeline interference)
        This only processes basic "- item" lists, not timeline "- **time**: content"
        🆕 v3.1: Enhanced pattern matching for better protection
        """
        # Skip lines that look like timeline entries
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            # Skip ALL timeline patterns (time, highlight, step-based)
            if re.match(r'^\s*- \*\*[^*]+\*\*:', line):
                processed_lines.append(line)
            # Process simple list items
            elif re.match(r'^\s*-\s+(?!\*\*)', line):
                content = re.sub(r'^\s*-\s+', '', line)
                processed_lines.append(f'<li>{content}</li>')
            else:
                processed_lines.append(line)
        
        text = '\n'.join(processed_lines)
        
        # Wrap consecutive <li> items in <ul>
        text = re.sub(r'(<li>.*?</li>\s*)+', lambda m: f'<ul>\n{m.group(0)}</ul>\n', text, flags=re.DOTALL)
        
        return text

    def _convert_paragraphs(self, text):
        """ห่อข้อความที่ยังไม่ถูกแปลงเป็น HTML ด้วย <p> tags"""
        lines = text.split('\n\n')
        result = []
        
        for line in lines:
            stripped_line = line.strip()
            # Skip if already HTML, header, placeholder, or empty
            if not stripped_line or stripped_line.startswith(('<', '#', '__PLACEHOLDER_')):
                result.append(line)
            else:
                result.append(f'<p>{stripped_line}</p>')
        
        return '\n\n'.join(result)

    def build_nav_section(self, content_data):
        """สร้าง Navigation Cards แบบ Dynamic"""
        print("🏗️ Building dynamic navigation section...")
        nav_cards_html = ""
        
        # หา day files (001-day1, 002-day2, etc.)
        day_keys = sorted([k for k in content_data if re.match(r'^\d+-day\d+', k)])
        
        for key in day_keys:
            content = content_data[key]
            th_md = content.get('th', '')
            en_md = content.get('en', th_md)
            
            # Extract H1 title for both languages
            th_title_match = re.search(r'^# (.*)', th_md, re.MULTILINE)
            en_title_match = re.search(r'^# (.*)', en_md, re.MULTILINE)
            th_title = th_title_match.group(1).strip() if th_title_match else "Day N/A"
            en_title = en_title_match.group(1).strip() if en_title_match else th_title

            # Extract date (วันที่/Date pattern)
            th_date_match = re.search(r'\*\*วันที่:\*\*\s*([^\n]+)', th_md)
            en_date_match = re.search(r'\*\*Date:\*\*\s*([^\n]+)', en_md)
            th_date = th_date_match.group(1).strip() if th_date_match else ""
            en_date = en_date_match.group(1).strip() if en_date_match else th_date

            # Extract short description (more flexible pattern)
            th_desc_match = re.search(r'(?:^|\n)([^#\*\n].{20,100}[^\n]*)', th_md)
            en_desc_match = re.search(r'(?:^|\n)([^#\*\n].{20,100}[^\n]*)', en_md)
            th_desc = th_desc_match.group(1).strip() if th_desc_match else "รายละเอียดการเดินทาง"
            en_desc = en_desc_match.group(1).strip() if en_desc_match else th_desc

            section_id = self.get_section_id(key)
            
            # Special birthday badge for day 4
            birthday_badge = '<div class="birthday-badge">🎂</div>' if 'day4' in key.lower() else ''

            nav_cards_html += f'''
            <a href="#{section_id}" class="nav-card">
                {birthday_badge}
                <h3><span class="th">{th_title}</span><span class="en">{en_title}</span></h3>
                <div class="date"><span class="th">{th_date}</span><span class="en">{en_date}</span></div>
                <div class="desc"><span class="th">{th_desc}</span><span class="en">{en_desc}</span></div>
            </a>'''

        return f'''<div class="nav-section">
            <h2><span class="th">ภาพรวมการเดินทาง</span><span class="en">Trip Overview</span></h2>
            <div class="nav-grid">{nav_cards_html}</div>
        </div>'''

    def build_content_sections(self, content_data):
        """สร้าง Content Sections ทั้งหมด"""
        print("🏗️ Building content sections...")
        sections_html = ""
        
        for file_key in sorted(content_data.keys()):
            content = content_data[file_key]
            section_id = self.get_section_id(file_key)

            # Extract H1 title to use in the section header
            th_h1_match = re.search(r'^# (.*)', content['th'], re.MULTILINE)
            en_h1_match = re.search(r'^# (.*)', content['en'], re.MULTILINE) if content['en'] else None
            
            th_h1 = th_h1_match.group(1).strip() if th_h1_match else section_id.replace('-', ' ').title()
            en_h1 = en_h1_match.group(1).strip() if en_h1_match else th_h1

            # Remove H1 from content before parsing the rest
            th_body = re.sub(r'^# .*', '', content['th'], count=1, flags=re.MULTILINE).strip()
            en_body = re.sub(r'^# .*', '', content['en'], count=1, flags=re.MULTILINE).strip() if content['en'] else th_body

            # Convert to HTML using the fixed markdown processor
            print(f"   🔧 Processing content for section: {section_id}")
            th_html = self.markdown_to_html(th_body)
            en_html = self.markdown_to_html(en_body) if en_body != th_body else th_html

            sections_html += f'''
            <div class="content-section" id="{section_id}">
                <h1><span class="th">{th_h1}</span><span class="en">{en_h1}</span></h1>
                <div class="th">{th_html}</div>
                <div class="en" style="display:none;">{en_html}</div>
            </div>'''
            
        print(f"   ✅ Generated {len(content_data)} content sections")
        return sections_html

    def get_section_id(self, file_key):
        """สร้าง section ID จากชื่อไฟล์ (เช่น '001-overview' -> 'overview')"""
        return re.sub(r'^\d+-', '', file_key)

    def generate(self):
        """สร้างไฟล์ HTML ตัวเต็ม"""
        print("\n🚀 Starting HTML generation process...")

        # Read skeleton template
        template_html = self.get_skeleton_template()
        if not template_html:
            print("❌ Cannot proceed without skeleton template.")
            return

        # Read all content files
        content_data = self.get_content_data()
        if not content_data:
            print("❌ No content found. Aborting.")
            return

        # Build components
        nav_section = self.build_nav_section(content_data)
        content_sections = self.build_content_sections(content_data)

        # Replace placeholders in template
        final_html = template_html.replace('{{NAV_SECTION_PLACEHOLDER}}', nav_section)
        final_html = final_html.replace('{{CONTENT_SECTIONS_PLACEHOLDER}}', content_sections)

        # Generate output filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_filename = f"Tokyo-Trip-March-2026-v3.1-FIXED-{timestamp}.html"
        output_path = self.build_dir / output_filename

        # Write final HTML file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
            file_size = output_path.stat().st_size
            print("\n🎉 HTML generation complete!")
            print(f"   - File: {output_filename}")
            print(f"   - Path: {output_path}")
            print(f"   - Size: {file_size / 1024:.2f} KB")
            print("\n🔥 Fixed Issues in v3.1:")
            print("   ✅ Double Processing eliminated with Placeholder Strategy")
            print("   ✅ Timeline structure preserved correctly") 
            print("   ✅ Table and Info boxes protected from interference")
            print("   ✅ Section markers (--- และ ```) cleaned up properly")
            print("   ✅ Multiple Timeline Formats supported:")
            print("       - ⏰ Time-based: - **HH:MM**: content")
            print("       - 🌟 Highlight: - **ไฮไลต์**: content") 
            print("       - 📋 Step: - **ขั้นตอน**: content")
            print("   ✅ Enhanced emoji detection for timeline details")
            print("   ✅ Improved regex patterns for better accuracy")
            
        except Exception as e:
            print(f"❌ Error writing final HTML file: {e}")

def main():
    """Main function to run the generator."""
    print("🎌 Tokyo Trip Generator v3.1 - Multi-Timeline & Section Fix")
    print("=" * 70)
    print("🆕 New Features:")
    print("   - Multiple Timeline Format Support")
    print("   - Section Marker Cleanup (--- และ ```)")
    print("   - Enhanced Emoji Detection")
    print("   - Better Error Handling")
    print("   - Improved Regex Patterns")
    print("=" * 70)
    generator = TokyoTripGeneratorV3()
    generator.generate()

if __name__ == "__main__":
    main()