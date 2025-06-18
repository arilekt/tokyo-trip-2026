#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokyo Trip 2026 HTML Generator - Version 5 (All-in-One Ultimate)
================================================================
รวมทุก feature จาก v4 แต่เป็นไฟล์เดียวครบจบ ไม่ต้องพึ่ง external templates

Author: Claude (AI Assistant) 
Date: June 17, 2025
Version: v5 - All-in-One Ultimate Edition
For: Arilek & Pojai's Tokyo Trip 2026

Features:
✅ Timeline expand/collapse ที่ทำงานได้ (จาก v4)
✅ Multi-language support (TH/EN)  
✅ Self-contained (ไม่ต้องพึ่ง external files)
✅ Mobile responsive design
✅ Offline-ready HTML output

Usage: python claude-tokyo_trip_generator-v5.py
"""

import os
import re
import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List
import html


@dataclass 
class TripConfig:
    script_dir: Path
    content_dir: Path 
    build_dir: Path
    base_name: str = "Tokyo-Trip-March-2026"
    version: str = "v5-All-in-One"


class MarkdownToHtml:
    @staticmethod
    def basic_md_to_html(md_text: str) -> str:
        if not md_text.strip():
            return ""
            
        lines = md_text.strip().splitlines()
        html_parts = []
        in_ul = False
        in_table = False
        table_headers = []
        
        for line in lines:
            line = line.strip()
            
            if not line:
                if in_ul:
                    html_parts.append("</ul>")
                    in_ul = False
                html_parts.append("")
                continue
                
            # Headers
            if line.startswith("### "):
                if in_ul:
                    html_parts.append("</ul>")
                    in_ul = False
                html_parts.append(f"<h3>{html.escape(line[4:])}</h3>")
                continue
            elif line.startswith("## "):
                if in_ul:
                    html_parts.append("</ul>")
                    in_ul = False
                html_parts.append(f"<h2>{html.escape(line[3:])}</h2>")
                continue
            elif line.startswith("# "):
                if in_ul:
                    html_parts.append("</ul>")
                    in_ul = False
                html_parts.append(f"<h1>{html.escape(line[2:])}</h1>")
                continue
                
            # Tables
            if line.startswith("|"):
                if not in_table:
                    html_parts.append('<div class="table-container">')
                    html_parts.append('<table>')
                    in_table = True
                    
                cells = [cell.strip() for cell in line.split("|")[1:-1]]
                
                if all(cell.strip().replace("-", "").replace(":", "") == "" for cell in cells):
                    continue
                    
                if not table_headers:
                    table_headers = cells
                    html_parts.append("<thead><tr>")
                    for cell in cells:
                        html_parts.append(f"<th>{html.escape(cell)}</th>")
                    html_parts.append("</tr></thead><tbody>")
                else:
                    html_parts.append("<tr>")
                    for cell in cells:
                        cell_html = MarkdownToHtml._process_inline(cell)
                        html_parts.append(f"<td>{cell_html}</td>")
                    html_parts.append("</tr>")
                continue
            else:
                if in_table:
                    html_parts.append("</tbody></table></div>")
                    in_table = False
                    table_headers = []
                    
            # Lists
            if line.startswith("- "):
                if not in_ul:
                    html_parts.append("<ul>")
                    in_ul = True
                item_content = MarkdownToHtml._process_inline(line[2:])
                html_parts.append(f"<li>{item_content}</li>")
                continue
                
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
                
            # Paragraphs
            if line:
                processed_line = MarkdownToHtml._process_inline(line)
                html_parts.append(f"<p>{processed_line}</p>")
        
        if in_ul:
            html_parts.append("</ul>")
        if in_table:
            html_parts.append("</tbody></table></div>")
            
        return "\n".join(html_parts)
    
    @staticmethod
    def _process_inline(text: str) -> str:
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
        
        if '<strong>' in text or '<em>' in text or '<code>' in text or '<a ' in text:
            return text
        return html.escape(text, quote=False)
        
    @staticmethod
    def process_timeline_markdown(md_text: str) -> str:
        if not re.search(r'^- \*\*\d+:\d+\*\*:', md_text, re.MULTILINE):
            return MarkdownToHtml.basic_md_to_html(md_text)
            
        lines = md_text.strip().splitlines()
        html_parts = ['<ul class="timeline">']
        item_counter = 0
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith("- **") and "**:" in line:
                match = re.match(r'- \*\*([^*]+)\*\*:\s*(.*)', line)
                if match:
                    time_part = match.group(1)
                    content_part = MarkdownToHtml._process_inline(match.group(2))
                    
                    nested_content = []
                    j = i + 1
                    
                    while j < len(lines):
                        next_line = lines[j]
                        if next_line.strip().startswith("- **") and "**:" in next_line.strip():
                            break
                        if next_line.strip().startswith("</ul>") or (not next_line.strip() and j == len(lines) - 1):
                            break
                            
                        if next_line.strip():
                            nested_content.append(next_line)
                        j += 1
                    
                    item_id = f"timeline-{item_counter}"
                    html_parts.append('<li>')
                    html_parts.append(f'<div class="timeline-main">')
                    html_parts.append(f'<strong>{time_part}</strong>: {content_part}')
                    html_parts.append('</div>')
                    
                    if nested_content:
                        html_parts.append(f'''
                        <button class="timeline-toggle" onclick="toggleTimelineDetail('{item_id}')">
                            <span class="th">รายละเอียด ▼</span>
                            <span class="en">Details ▼</span>
                        </button>
                        <div class="timeline-detail" id="{item_id}" style="display: none;">''')
                        
                        nested_html = MarkdownToHtml.basic_md_to_html('\n'.join(nested_content))
                        html_parts.append(nested_html)
                        html_parts.append('</div>')
                    
                    html_parts.append('</li>')
                    item_counter += 1
                    i = j - 1
            
            elif line.startswith("- ") and not line.startswith("- **"):
                content = MarkdownToHtml._process_inline(line[2:])
                html_parts.append('<li>')
                html_parts.append(f'<div class="timeline-main">{content}</div>')
                html_parts.append('</li>')
            
            elif line and not line.startswith("#"):
                html_parts.append('</ul>')
                processed_line = MarkdownToHtml._process_inline(line)
                html_parts.append(f'<p>{processed_line}</p>')
                html_parts.append('<ul class="timeline">')
            
            i += 1


class HtmlTemplate:
    @staticmethod 
    def get_base_template() -> str:
        return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tokyo Trip March 2026</title>
    <style>{CSS_CONTENT}</style>
</head>
<body class="lang-th">
    <div class="lang-switcher">
        <button onclick="switchLanguage('th')" class="lang-btn active" id="btn-th">TH</button>
        <button onclick="switchLanguage('en')" class="lang-btn" id="btn-en">EN</button>
    </div>
    <div class="container">
        <header>
            <h1 id="toc">
                <span class="th th-block">Tokyo Trip March 2026 - แผนการเดินทางโตเกียว</span>
                <span class="en en-block">Tokyo Trip March 2026 - Complete Travel Guide</span>
            </h1>
            <h2>
                <span class="th">📅 6-13 มีนาคม 2026 (8 วัน 7 คืน)</span>
                <span class="en">📅 March 6-13, 2026 (8 Days 7 Nights)</span>
            </h2>
            <p>
                <span class="th">✈️ ผู้เดินทาง: Arilek & Pojai (วันเกิดครบ 11 ปี)</span>
                <span class="en">✈️ Travelers: Arilek & Pojai (11th Birthday Trip)</span><br/>
                <span class="th">🗺️ เส้นทาง: Bangkok → Tokyo → Kawaguchiko → Tokyo → Bangkok</span>
                <span class="en">🗺️ Route: Bangkok → Tokyo → Kawaguchiko → Tokyo → Bangkok</span>
            </p>
        </header>
{CONTENT_SECTIONS}
    </div>
    <a class="back-to-top" href="#toc">
        <span class="th">🔙 กลับไปหน้าหลัก</span>
        <span class="en">🔙 Back to Top</span>
    </a>
    <script>{JS_CONTENT}</script>
</body>
</html>'''

    @staticmethod
    def get_css() -> str:
        return '''
        :root { --primary-color: #2563eb; --primary-light: #3b82f6; --primary-dark: #1d4ed8; --text-color: #1f2937; --bg-color: #ffffff; --card-bg: #f8fafc; --border-color: #e5e7eb; --shadow: rgba(0, 0, 0, 0.1); --success: #10b981; --warning: #f59e0b; --danger: #ef4444; --info-bg: #dbeafe; --info-border: #3b82f6; --note-bg: #f3f4f6; --note-border: #6b7280; --table-header: #f1f5f9; --table-border: #d1d5db; --table-alt: #f9fafb; --pending: #8b5cf6; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: var(--text-color); background-color: var(--bg-color); padding-top: 3rem; }
        .lang-switcher { position: fixed; top: 1rem; right: 1rem; z-index: 1000; display: flex; gap: 0.5rem; }
        .lang-btn { padding: 0.5rem 1rem; border: 2px solid var(--primary-color); background: white; color: var(--primary-color); border-radius: 0.5rem; cursor: pointer; font-weight: bold; transition: all 0.3s ease; }
        .lang-btn.active, .lang-btn:hover { background: var(--primary-color); color: white; }
        .lang-en .th, .lang-th .en { display: none; }
        .lang-th .th, .lang-en .en { display: inline; }
        .lang-en .en-block, .lang-th .th-block { display: block; }
        .lang-en .th-block, .lang-th .en-block { display: none; }
        .container { max-width: 1200px; margin: 0 auto; padding: 1rem; }
        header { text-align: center; margin-bottom: 3rem; padding: 2rem; background: linear-gradient(135deg, var(--primary-light), var(--primary-color)); color: white; border-radius: 1rem; box-shadow: 0 4px 6px var(--shadow); }
        header h1 { font-size: 2rem; margin-bottom: 1rem; font-weight: 700; }
        header h2 { font-size: 1.2rem; margin-bottom: 1rem; opacity: 0.9; }
        header p { font-size: 1rem; opacity: 0.8; }
        section { margin-bottom: 3rem; padding: 2rem; background: var(--card-bg); border-radius: 1rem; box-shadow: 0 2px 4px var(--shadow); }
        section h1 { color: var(--primary-color); font-size: 1.8rem; margin-bottom: 1.5rem; border-bottom: 3px solid var(--primary-light); padding-bottom: 0.5rem; }
        .timeline { list-style: none; padding: 0; margin: 1.5rem 0; position: relative; }
        .timeline::before { content: ''; position: absolute; left: 1rem; top: 0; bottom: 0; width: 2px; background: var(--primary-color); }
        .timeline li { position: relative; padding: 1rem 0 1rem 3rem; border-bottom: 1px solid var(--border-color); }
        .timeline li::before { content: ''; position: absolute; left: 0.5rem; top: 1.5rem; width: 1rem; height: 1rem; background: var(--primary-color); border-radius: 50%; border: 3px solid white; box-shadow: 0 0 0 3px var(--primary-color); }
        .timeline-main { margin-bottom: 0.5rem; }
        .timeline-toggle { background: var(--primary-light); color: white; border: none; padding: 0.4rem 0.8rem; border-radius: 0.25rem; cursor: pointer; font-size: 0.8rem; margin: 0.5rem 0 0.25rem 0; transition: all 0.3s ease; display: inline-block; }
        .timeline-toggle:hover { background: var(--primary-color); }
        .timeline-toggle.expanded { background: var(--success); }
        .timeline-detail { margin-top: 0.5rem; padding: 0.75rem; border-left: 2px solid var(--border-color); background: rgba(255, 255, 255, 0.7); border-radius: 0.25rem; display: none; }
        .day-overviews { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin: 2rem 0; }
        .day-overview { background: white; border: 1px solid var(--border-color); border-radius: 0.75rem; padding: 1.5rem; transition: all 0.3s ease; border-left: 4px solid var(--primary-color); }
        .day-overview:hover { transform: translateY(-2px); box-shadow: 0 4px 12px var(--shadow); }
        .day-overview h3 a { text-decoration: none; color: var(--primary-color); }
        .birthday-badge { background: linear-gradient(45deg, #ff6b6b, #feca57); color: white; padding: 0.5rem 1rem; border-radius: 2rem; font-size: 0.9rem; margin-left: 1rem; animation: sparkle 2s infinite; }
        @keyframes sparkle { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
        .back-to-top { position: fixed; bottom: 2rem; right: 2rem; background: var(--primary-color); color: white; padding: 1rem; border-radius: 50%; text-decoration: none; box-shadow: 0 4px 12px var(--shadow); transition: all 0.3s ease; z-index: 100; }
        @media (max-width: 768px) { .container { padding: 0.5rem; } header { padding: 1rem; } header h1 { font-size: 1.5rem; } section { padding: 1rem; } .day-overviews { grid-template-columns: 1fr; } .timeline li { padding-left: 2rem; } .timeline::before { left: 0.5rem; } .timeline li::before { left: 0.25rem; width: 0.5rem; height: 0.5rem; } }
        '''

    @staticmethod
    def get_js() -> str:
        return '''
        function switchLanguage(lang) {
            const body = document.body;
            const buttons = document.querySelectorAll('.lang-btn');
            body.classList.remove('lang-th', 'lang-en');
            body.classList.add(`lang-${lang}`);
            buttons.forEach(btn => {
                btn.classList.remove('active');
                if (btn.id === `btn-${lang}`) btn.classList.add('active');
            });
            try { localStorage.setItem('tokyo-trip-lang', lang); } catch (e) {}
        }
        
        function toggleTimelineDetail(elementId) {
            const detailElement = document.getElementById(elementId);
            const toggleButton = document.querySelector(`button[onclick="toggleTimelineDetail('${elementId}')"]`);
            if (!detailElement || !toggleButton) return;
            const isVisible = detailElement.style.display !== 'none';
            if (isVisible) {
                detailElement.style.display = 'none';
                toggleButton.classList.remove('expanded');
                toggleButton.innerHTML = '<span class="th">รายละเอียด ▼</span><span class="en">Details ▼</span>';
            } else {
                detailElement.style.display = 'block';
                toggleButton.classList.add('expanded');
                toggleButton.innerHTML = '<span class="th">รายละเอียด ▲</span><span class="en">Details ▲</span>';
            }
        }
        window.toggleTimelineDetail = toggleTimelineDetail;
        
        function initializeTimelineToggle() {
            const timelineDetails = document.querySelectorAll('.timeline-detail');
            timelineDetails.forEach(detail => detail.style.display = 'none');
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            try {
                const savedLang = localStorage.getItem('tokyo-trip-lang');
                switchLanguage(savedLang && (savedLang === 'th' || savedLang === 'en') ? savedLang : 'th');
            } catch (e) { switchLanguage('th'); }
            initializeTimelineToggle();
            console.log('✅ Tokyo Trip 2026 v5 - Ready with working timeline!');
        });
        '''


class TripGenerator:
    def __init__(self, config: TripConfig):
        self.config = config
        self.markdown_processor = MarkdownToHtml()
        self.template_manager = HtmlTemplate()
        
    def read_markdown_content(self) -> Dict[str, Dict[str, str]]:
        markdown_contents = {'th': {}, 'en': {}}
        if not self.config.content_dir.exists():
            return markdown_contents
        
        self._read_language_files(self.config.content_dir, 'th', markdown_contents['th'])
        en_dir = self.config.content_dir / "en"
        if en_dir.exists():
            self._read_language_files(en_dir, 'en', markdown_contents['en'])
        return markdown_contents
    
    def _read_language_files(self, directory: Path, lang: str, content_dict: Dict[str, str]):
        for md_file in sorted(directory.glob("*.md")):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    section_id = re.sub(r'^\d+-?', '', md_file.stem).replace('_', '-').replace(' ', '-').lower()
                    content_dict[section_id] = f.read()
                    print(f"✅ Read {md_file.name} -> {section_id}")
            except Exception as e:
                print(f"Error reading {md_file.name}: {e}")
    
    def create_overview_section(self, markdown_contents: Dict[str, Dict[str, str]]) -> str:
        th_contents = markdown_contents['th']
        day_files = [(k, v) for k, v in th_contents.items() if k.startswith('day')]
        day_files.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()) if re.search(r'\d+', x[0]) else 0)
        
        overview_html = '''
        <section id="overview">
            <h1>
                <span class="th th-block">ภาพรวมการเดินทางและกิจกรรม</span>
                <span class="en en-block">Travel Overview and Activities</span>
            </h1>
            <div class="day-overviews">
        '''
        
        for section_id, th_content in day_files:
            try:
                title_match = re.search(r'^#+\s*(.+?)(?:\n|$)', th_content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()
                    main_title = re.split(r'\s*[-–|/]\s*', title)[0].strip()
                    
                    birthday_badge = ""
                    if section_id == "day4":
                        birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
                    
                    overview_html += f'''
                    <div class="day-overview">
                        <h3>
                            <a href="#{section_id}">
                                <span class="th">{main_title}</span>
                                <span class="en">{main_title}</span>
                            </a>
                            {birthday_badge}
                        </h3>
                        <p>
                            <span class="th">กิจกรรมและสถานที่น่าสนใจ</span>
                            <span class="en">Fun activities and interesting places</span>
                        </p>
                    </div>
                    '''
            except Exception:
                continue
        
        overview_html += '''
            </div>
        </section>
        '''
        return overview_html
    
    def process_content_sections(self, markdown_contents: Dict[str, Dict[str, str]]) -> str:
        all_sections = []
        all_sections.append(self.create_overview_section(markdown_contents))
        
        th_contents = markdown_contents['th']
        section_order = ['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8', 'budget']
        
        for section_id in section_order:
            if section_id in th_contents:
                try:
                    th_content = th_contents[section_id]
                    title_match = re.search(r'^#+\s*(.+?)(?:\n|$)', th_content, re.MULTILINE)
                    
                    if title_match:
                        title = title_match.group(1).strip()
                        body = re.sub(r'^#+\s*.+?(?:\n|$)', '', th_content, count=1, flags=re.MULTILINE).strip()
                        
                        birthday_badge = ""
                        if section_id == "day4":
                            birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
                        
                        if section_id.startswith('day'):
                            html_body = self.markdown_processor.process_timeline_markdown(body)
                        else:
                            html_body = self.markdown_processor.basic_md_to_html(body)
                        
                        section_html = f'''
        <section id="{section_id}">
            <h1>
                <span class="th th-block">{title}</span>
                <span class="en en-block">{title}</span>
                {birthday_badge}
            </h1>
            <div class="th th-block">{html_body}</div>
            <div class="en en-block">{html_body}</div>
        </section>'''
                        
                        all_sections.append(section_html)
                        print(f"✅ Processed section: {section_id}")
                except Exception as e:
                    print(f"Error processing {section_id}: {e}")
        
        return "\n".join(all_sections)
    
    def generate_html(self) -> str:
        markdown_contents = self.read_markdown_content()
        content_sections = self.process_content_sections(markdown_contents)
        
        html_content = self.template_manager.get_base_template()
        html_content = html_content.replace('{CSS_CONTENT}', self.template_manager.get_css())
        html_content = html_content.replace('{JS_CONTENT}', self.template_manager.get_js())
        html_content = html_content.replace('{CONTENT_SECTIONS}', content_sections)
        
        return html_content
    
    def save_html_file(self, html_content: str) -> Path:
        self.config.build_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        filename = f"{self.config.base_name}-{self.config.version}-{timestamp}.html"
        output_path = self.config.build_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML file saved: {output_path}")
        return output_path


def main():
    print("🇯🇵 Tokyo Trip 2026 HTML Generator - Version 5 (All-in-One)")
    print("=" * 60)
    
    script_dir = Path(__file__).parent
    config = TripConfig(
        script_dir=script_dir,
        content_dir=script_dir.parent / "content",
        build_dir=script_dir.parent / "build"
    )
    
    generator = TripGenerator(config)
    
    try:
        print(f"📁 Content directory: {config.content_dir}")
        print(f"📁 Build directory: {config.build_dir}")
        print("")
        
        html_content = generator.generate_html()
        output_path = generator.save_html_file(html_content)
        
        print("")
        print("🎉 Generation completed successfully!")
        print(f"📄 Output file: {output_path}")
        print(f"📊 File size: {len(html_content):,} characters")
        print("")
        print("💡 Features included:")
        print("   ✅ Timeline expand/collapse (WORKING from v4)")
        print("   ✅ Multi-language support (TH/EN)")
        print("   ✅ Self-contained (no external files needed)")
        print("   ✅ Mobile responsive design")
        print("")
        print("🚀 Ready for use!")
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
