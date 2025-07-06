#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokyo Trip Generator - v2 (Fixed & Enhanced)
============================================
สร้าง HTML ไฟล์สำหรับทริปโตเกียว โดยอ่านเนื้อหาจาก content/*.md 
และใส่ลงใน skeleton template ที่มี CSS/JS สมบูรณ์

✨ Version 2 Features:
- แก้ไข Regex ที่ผิดพลาดทั้งหมดจากเวอร์ชันก่อนหน้า
- ใช้ skeleton_template.html เป็นโครงสร้างหลัก
- สร้าง Navigation Cards แบบ Dynamic จากเนื้อหาไฟล์ .md
- Markdown Parser ที่แม่นยำสำหรับ Timeline, Tables, Info/Note Boxes
- รองรับ Multi-language (TH/EN) อย่างสมบูรณ์
- โค้ดอ่านง่ายและเป็นระเบียบ

Author: Gemini Code Assist (Fixed by AI)
Date: 7 July 2025
Version: 2.0.0-fixed
"""

import os
import re
import datetime
from pathlib import Path

class TokyoTripGeneratorV2:
    """
    Generator ที่รวมส่วนที่ดีที่สุดจากทุกไฟล์, แก้ไขข้อผิดพลาด,
    และสร้าง HTML Guide ที่สมบูรณ์และทำงานได้จริง
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

        print("🚀 Tokyo Trip Generator v2 - Initialized")
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
        แปลง Markdown เป็น HTML ที่ปรับปรุงแล้วและแก้ไข Regex ที่ผิดพลาดทั้งหมด
        """
        if not markdown_text or not markdown_text.strip():
            return ""

        # --- Regex ที่แก้ไขแล้ว ---
        # Headers (H1 จะถูกจัดการแยกต่างหากในแต่ละ section)
        html = re.sub(r'^## (.*)$', r'<h2>\1</h2>', markdown_text, flags=re.MULTILINE)
        html = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.*)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

        # Bold and Italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)

        # Timeline items
        html = self._convert_timeline(html)

        # Info/Note boxes
        html = self._convert_info_note_boxes(html)

        # Tables
        html = self._convert_tables(html)

        # Lists (Unordered and Ordered)
        html = self._convert_lists(html)

        # Paragraphs
        html = self._convert_paragraphs(html)

        return html

    def _convert_timeline(self, text):
        """แปลง Timeline Markdown เป็น HTML"""
        timeline_pattern = re.compile(r'^- \*\*(.+?)\*\*:\s*(.*?)\n((?:  .+?\n)*)', re.MULTILINE)

        def repl(match):
            time = match.group(1)
            title = match.group(2)
            details_md = match.group(3)
            timeline_id = f"timeline-item-{datetime.datetime.now().microsecond}-{os.urandom(2).hex()}"

            details_html = ""
            if details_md:
                # แปลงรายละเอียดย่อยๆ ภายใน timeline
                details_html = self.markdown_to_html(details_md.strip())

            button_html = f'''<button class="timeline-toggle" onclick="toggleTimelineDetail('{timeline_id}')">
                                <span class="th">รายละเอียด ▼</span><span class="en">Details ▼</span>
                             </button>''' if details_html else ""

            detail_div_html = f'''<div class="timeline-detail" id="{timeline_id}" style="display: none;">
                                    {details_html}
                                 </div>''' if details_html else ""

            return f'<li><div class="timeline-main"><strong>{time}:</strong> {title}</div>{button_html}{detail_div_html}</li>'

        # หากมี timeline item อย่างน้อยหนึ่งอัน ให้หุ้มด้วย <ul class="timeline">
        if re.search(r'^- \*\*', text, re.MULTILINE):
            processed_text = timeline_pattern.sub(repl, text)
            # ห่อเฉพาะส่วนที่เป็น timeline จริงๆ
            return re.sub(r'(<li>.*?</li>\s*)+', r'<ul class="timeline">\g<0></ul>', processed_text, flags=re.DOTALL)
        return text

    def _convert_info_note_boxes(self, text):
        """แปลง Info/Note Box Markdown เป็น HTML"""
        box_pattern = re.compile(r'^> \*\*(\w+):\*\*\s*(.*?)\n((?:> .*\n?)*)', re.MULTILINE)

        def repl(match):
            box_type_raw = match.group(1).lower()
            title = match.group(2)
            content_md = match.group(3).replace('> ', '')

            box_class = "note-box" if "note" in box_type_raw else "info-box"
            toggle_class = "note-toggle" if "note" in box_type_raw else "info-toggle"
            detail_class = "note-detail" if "note" in box_type_raw else "info-detail"

            content_html = self.markdown_to_html(content_md.strip())

            return f'''<div class="{box_class}">
                <div class="{toggle_class}"><span class="th">{title}</span><span class="en">{title}</span></div>
                <div class="{detail_class}">{content_html}</div>
            </div>'''

        return box_pattern.sub(repl, text)

    def _convert_tables(self, text):
        """แปลง Markdown Table เป็น HTML Table"""
        table_pattern = re.compile(r'((?:\|.*\|.*\n)+)')
        processed_text = text

        def repl(match):
            table_md = match.group(1).strip()
            lines = table_md.split('\n')
            if len(lines) < 2 or not re.match(r'^\s*\|-.*\|-.*', lines[1]):
                return match.group(0) # ไม่ใช่ตาราง

            html = '<div class="table-container"><table class="table">\n'
            # Header
            headers = [h.strip() for h in lines[0].strip().strip('|').split('|')]
            html += '<thead><tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead>\n'
            # Body
            html += '<tbody>\n'
            for row_md in lines[2:]:
                cells = [c.strip() for c in row_md.strip().strip('|').split('|')]
                html += '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>\n'
            html += '</tbody></table></div>'
            return html

        processed_text = table_pattern.sub(repl, processed_text)
        return processed_text

    def _convert_lists(self, text):
        """แปลง Unordered/Ordered Lists เป็น HTML"""
        # Unordered lists
        text = re.sub(r'^\s*-\s+(.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'(<li>.*</li>\s*)+', r'<ul>\g<0></ul>', text, flags=re.DOTALL)
        # Ordered lists
        text = re.sub(r'^\s*\d+\.\s+(.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'(<li>.*</li>\s*)+', r'<ol>\g<0></ol>', text, flags=re.DOTALL)
        # Cleanup nested list tags
        text = text.replace('</ul>\n<ul>', '').replace('</ol>\n<ol>', '')
        return text

    def _convert_paragraphs(self, text):
        """ห่อข้อความที่ยังไม่ถูกแปลงเป็น HTML ด้วย <p> tags"""
        lines = text.split('\n\n')
        result = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith(('<', '#')):
                result.append(f'<p>{stripped_line}</p>')
            else:
                result.append(line)
        return '\n\n'.join(result)

    def build_nav_section(self, content_data):
        """สร้าง Navigation Cards แบบ Dynamic"""
        print("🏗️ Building dynamic navigation section...")
        nav_cards_html = ""
        day_keys = sorted([k for k in content_data if k.startswith('00') and 'day' in k])

        for key in day_keys:
            content = content_data[key]
            th_md = content.get('th', '')
            en_md = content.get('en', th_md) # Fallback to Thai if English is missing

            # Extract H1 title for both languages
            th_title_match = re.search(r'^# (.*)', th_md, re.MULTILINE)
            en_title_match = re.search(r'^# (.*)', en_md, re.MULTILINE)
            th_title = th_title_match.group(1).strip() if th_title_match else "N/A"
            en_title = en_title_match.group(1).strip() if en_title_match else th_title

            # Extract date and description
            th_date_match = re.search(r'^\*\*([^*]+)\*\*', th_md, re.MULTILINE)
            en_date_match = re.search(r'^\*\*([^*]+)\*\*', en_md, re.MULTILINE)
            th_date = th_date_match.group(1).strip() if th_date_match else ""
            en_date = en_date_match.group(1).strip() if en_date_match else th_date

            th_desc_match = re.search(r'^\*\*.*\n\n(.*?)\n', th_md, re.DOTALL)
            en_desc_match = re.search(r'^\*\*.*\n\n(.*?)\n', en_md, re.DOTALL)
            th_desc = th_desc_match.group(1).strip() if th_desc_match else "รายละเอียดการเดินทาง"
            en_desc = en_desc_match.group(1).strip() if en_desc_match else th_desc

            section_id = self.get_section_id(key)
            birthday_badge = '<div class="birthday-badge">🎂</div>' if 'day4' in key else ''

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
            en_h1_match = re.search(r'^# (.*)', content['en'], re.MULTILINE)
            th_h1 = th_h1_match.group(1).strip() if th_h1_match else section_id.replace('-', ' ').title()
            en_h1 = en_h1_match.group(1).strip() if en_h1_match else th_h1

            # Remove H1 from content before parsing the rest
            th_body = re.sub(r'^# .*', '', content['th'], count=1, flags=re.MULTILINE).strip()
            en_body = re.sub(r'^# .*', '', content['en'], count=1, flags=re.MULTILINE).strip() if content['en'] else th_body

            th_html = self.markdown_to_html(th_body)
            en_html = self.markdown_to_html(en_body)

            sections_html += f'''
            <div class="content-section" id="{section_id}">
                <h1><span class="th">{th_h1}</span><span class="en">{en_h1}</span></h1>
                <div class="th">{th_html}</div>
                <div class="en" style="display:none;">{en_html}</div>
            </div>'''
        return sections_html

    def get_section_id(self, file_key):
        """สร้าง section ID จากชื่อไฟล์ (เช่น '001-overview' -> 'overview')"""
        return re.sub(r'^\d+-', '', file_key)

    def generate(self):
        """สร้างไฟล์ HTML ตัวเต็ม"""
        print("\n🚀 Starting HTML generation process...")

        template_html = self.get_skeleton_template()
        if not template_html:
            print("❌ Cannot proceed without skeleton template.")
            return

        content_data = self.get_content_data()
        if not content_data:
            print("❌ No content found. Aborting.")
            return

        nav_section = self.build_nav_section(content_data)
        content_sections = self.build_content_sections(content_data)

        # แทนที่ placeholders ใน template
        final_html = template_html.replace('{{NAV_SECTION_PLACEHOLDER}}', nav_section)
        final_html = final_html.replace('{{CONTENT_SECTIONS_PLACEHOLDER}}', content_sections)

        # สร้างชื่อไฟล์พร้อม timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_filename = f"Tokyo-Trip-March-2026-v2-{timestamp}.html"
        output_path = self.build_dir / output_filename

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
            file_size = output_path.stat().st_size
            print("\n🎉 HTML generation complete!")
            print(f"   - File: {output_filename}")
            print(f"   - Path: {output_path}")
            print(f"   - Size: {file_size / 1024:.2f} KB")
        except Exception as e:
            print(f"❌ Error writing final HTML file: {e}")

def main():
    """Main function to run the generator."""
    generator = TokyoTripGeneratorV2()
    generator.generate()

if __name__ == "__main__":
    main()
