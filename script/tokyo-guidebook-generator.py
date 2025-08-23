#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokyo Trip Guidebook Generator - v1.0 (Reference Guide)
=======================================================
สร้าง HTML ไฟล์แบบ Guidebook รวมข้อมูลต่างๆ ที่เป็นประโยชน์
ไม่เรียงตาม timeline แต่จัดตามหมวดหมู่

📖 Guidebook Sections:
- 🏨 ที่พัก (Accommodation)
- 🍽️ ร้านอาหารแนะนำ (Restaurants & Food)
- 🛍️ ช้อปปิ้ง (Shopping Guide)
- 📷 การซื้อกล้อง (Camera Shopping)
- 🚊 การเดินทาง (Transportation)
- 💰 งบประมาณ (Budget Planning)
- 🌤️ สภาพอากาศ (Weather)
- 💡 เคล็ดลับ (Tips & Tricks)

Author: Claude AI Assistant (Guidebook Style)
Date: 23 August 2025  
Version: 1.0.0-guidebook-reference
"""

import os
import re
import datetime
from pathlib import Path

class TokyoGuidebookGenerator:
    """
    Guidebook generator จัดข้อมูลตามหมวดหมู่แทนที่จะเป็น timeline
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

        print("📖 Tokyo Trip Guidebook Generator v1.0")
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
        """อ่านไฟล์ content ทั้งหมด"""
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

        # อ่านไฟล์ภาษาอังกฤษ (ถ้ามี)
        if self.en_dir.exists():
            for md_file in sorted(self.en_dir.glob("*.md")):
                file_key = md_file.stem
                if file_key in content_data:
                    content_data[file_key]['en'] = self.read_file(md_file)

        print(f"   - Found {len(content_data)} content entries.")
        return content_data

    def organize_guidebook_data(self, content_data):
        """จัดระเบียบข้อมูลตามหมวดหมู่สำหรับ guidebook"""
        print("📋 Organizing content by categories...")
        
        guidebook_data = {
            'overview': {'title': '🗼 ภาพรวมการเดินทาง', 'content': ''},
            'accommodation': {'title': '🏨 ที่พัก', 'content': ''},
            'food': {'title': '🍽️ ร้านอาหารแนะนำ', 'content': ''},
            'shopping': {'title': '🛍️ ช้อปปิ้ง', 'content': ''},
            'camera': {'title': '📷 การซื้อกล้อง', 'content': ''},
            'transportation': {'title': '🚊 การเดินทาง', 'content': ''},
            'budget': {'title': '💰 งบประมาณ', 'content': ''},
            'weather': {'title': '🌤️ สภาพอากาศ', 'content': ''},
            'tips': {'title': '💡 เคล็ดลับการเดินทาง', 'content': ''}
        }

        # Overview
        if '001-overview' in content_data:
            guidebook_data['overview']['content'] = content_data['001-overview']['th']

        # Accommodation  
        if '002-accommodation' in content_data:
            guidebook_data['accommodation']['content'] = content_data['002-accommodation']['th']

        # Transportation
        if '011-transportation' in content_data:
            guidebook_data['transportation']['content'] = content_data['011-transportation']['th']

        # Weather
        if '012-weather' in content_data:
            guidebook_data['weather']['content'] = content_data['012-weather']['th']

        # Budget
        if '013-budget' in content_data:
            guidebook_data['budget']['content'] = content_data['013-budget']['th']

        # Tips
        if '014-tips' in content_data:
            guidebook_data['tips']['content'] = content_data['014-tips']['th']

        # Extract food, shopping, camera info from day files
        self._extract_special_sections(content_data, guidebook_data)

        return guidebook_data

    def _extract_special_sections(self, content_data, guidebook_data):
        """แยกข้อมูลพิเศษจากไฟล์วันต่างๆ"""
        food_sections = []
        shopping_sections = []
        camera_sections = []

        # หาข้อมูลจากไฟล์วันต่างๆ
        day_keys = [k for k in content_data if re.match(r'^\d+-day\d+', k)]
        
        for key in day_keys:
            content = content_data[key]['th']
            
            # Extract food sections
            food_matches = re.findall(r'## 🍴 ([^#]+?)\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
            food_sections.extend(food_matches)
            
            # Extract shopping sections  
            shopping_matches = re.findall(r'## 🛍️ ([^#]+?)\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
            shopping_sections.extend(shopping_matches)
            
            # Extract camera sections
            camera_matches = re.findall(r'## 🎁 ([^#]+?)\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
            camera_sections.extend(camera_matches)
            
            # Also look for shopping planning sections
            shopping_plan_matches = re.findall(r'## 🛒 ([^#]+?)\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
            shopping_sections.extend(shopping_plan_matches)
            
            # Skincare/beauty sections
            beauty_matches = re.findall(r'## 💄 ([^#]+?)\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
            shopping_sections.extend(beauty_matches)
            
            # Denim/clothing sections
            clothing_matches = re.findall(r'## 👔 ([^#]+?)\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
            shopping_sections.extend(clothing_matches)

        # Combine sections
        if food_sections:
            combined_food = '\n\n'.join([f'## {title}\n{content}' for title, content in food_sections])
            guidebook_data['food']['content'] = combined_food

        if shopping_sections:
            combined_shopping = '\n\n'.join([f'## {title}\n{content}' for title, content in shopping_sections])
            guidebook_data['shopping']['content'] = combined_shopping

        if camera_sections:
            combined_camera = '\n\n'.join([f'## {title}\n{content}' for title, content in camera_sections])
            guidebook_data['camera']['content'] = combined_camera

    def markdown_to_html(self, md_text):
        """Convert markdown to HTML for guidebook"""
        if not md_text:
            return ""
        
        html = md_text
        
        # Headers
        html = re.sub(r'^### (.*)', r'<h3>\\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*)', r'<h2>\\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*)', r'<h1>\\1</h1>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\\*\\*(.*?)\\*\\*', r'<strong>\\1</strong>', html)
        html = re.sub(r'\\*(.*?)\\*', r'<em>\\1</em>', html)
        
        # Lists
        html = self._convert_lists(html)
        
        # Tables
        html = self._convert_tables(html)
        
        # Info boxes (> **Note:** pattern)
        html = self._convert_info_boxes(html)
        
        # Paragraphs
        html = self._convert_paragraphs(html)
        
        return html

    def _convert_lists(self, text):
        """Convert markdown lists to HTML"""
        lines = text.split('\\n')
        result = []
        in_list = False
        
        for line in lines:
            if line.strip().startswith('- '):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                item_content = line.strip()[2:]
                # Process sub-items (indented with spaces)
                if item_content.strip():
                    result.append(f'  <li>{item_content}</li>')
            elif line.startswith('  - ') and in_list:
                # Sub-item
                sub_item = line.strip()[2:]
                result.append(f'    <li class="sub-item">{sub_item}</li>')
            else:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                result.append(line)
        
        if in_list:
            result.append('</ul>')
        
        return '\\n'.join(result)

    def _convert_tables(self, text):
        """Convert markdown tables to HTML"""
        lines = text.split('\\n')
        result = []
        in_table = False
        
        for i, line in enumerate(lines):
            if '|' in line and line.count('|') >= 2:
                if not in_table:
                    result.append('<div class="table-container">')
                    result.append('<table class="guidebook-table">')
                    in_table = True
                    
                    # Check if next line is separator
                    if i + 1 < len(lines) and '---' in lines[i + 1]:
                        # Header row
                        cells = [cell.strip() for cell in line.split('|')[1:-1]]
                        result.append('<thead>')
                        result.append('<tr>' + ''.join(f'<th>{cell}</th>' for cell in cells) + '</tr>')
                        result.append('</thead><tbody>')
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
        
        return '\\n'.join(result)

    def _convert_info_boxes(self, text):
        """Convert info boxes (> **Note:** pattern) to HTML"""
        # Pattern for info boxes starting with > **Type:**
        pattern = r'> \\*\\*(\\w+):\\*\\*([^\\n]+)\\n((?:> [^\\n]*\\n?)*)'
        
        def replace_info_box(match):
            box_type = match.group(1).lower()
            title = match.group(2).strip()
            content_lines = match.group(3).strip().split('\\n')
            
            # Remove > prefix from content lines
            content = []
            for line in content_lines:
                if line.startswith('> '):
                    content.append(line[2:])
                elif line.startswith('>'):
                    content.append(line[1:])
            
            content_text = '\\n'.join(content).strip()
            
            box_class = 'info-box'
            if 'note' in box_type:
                box_class = 'note-box'
            elif 'tip' in box_type:
                box_class = 'tip-box'
            elif 'warning' in box_type:
                box_class = 'warning-box'
            
            return f'''<div class="{box_class}">
                <h4>{box_type.title()}: {title}</h4>
                <p>{content_text}</p>
            </div>'''
        
        return re.sub(pattern, replace_info_box, text, flags=re.MULTILINE)

    def _convert_paragraphs(self, text):
        """Convert text blocks to paragraphs"""
        paragraphs = text.split('\\n\\n')
        result = []
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Skip if already HTML
            if para.startswith('<') or para.startswith('#'):
                result.append(para)
            else:
                # Handle single lines vs multi-lines
                lines = para.split('\\n')
                if len(lines) == 1:
                    result.append(f'<p>{para}</p>')
                else:
                    # Multiple lines - wrap each in <p>
                    line_paragraphs = []
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('<'):
                            line_paragraphs.append(f'<p>{line}</p>')
                        elif line:
                            line_paragraphs.append(line)
                    result.append('\\n'.join(line_paragraphs))
        
        return '\\n\\n'.join(result)

    def generate_guidebook_html(self, guidebook_data):
        """Generate complete guidebook HTML"""
        print("🏗️ Building guidebook HTML...")
        
        # Generate sections HTML
        sections_html = ""
        
        for section_key, section_data in guidebook_data.items():
            title = section_data['title']
            content = section_data['content']
            
            if content.strip():
                content_html = self.markdown_to_html(content)
                
                sections_html += f'''
                <section class="guidebook-section" id="{section_key}">
                    <div class="section-header" onclick="toggleSection('{section_key}')">
                        <h2>{title}</h2>
                        <span class="toggle-indicator">▼</span>
                    </div>
                    <div class="section-content" id="content-{section_key}">
                        {content_html}
                    </div>
                </section>
                '''

        # Generate navigation
        nav_html = self._generate_navigation(guidebook_data)
        
        # Get CSS and JavaScript
        css = self._get_guidebook_css()
        js = self._get_guidebook_js()
        
        return f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tokyo Trip Guidebook 2026 📖</title>
    <style>{css}</style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="guidebook-header">
            <h1>📖 Tokyo Trip Guidebook 2026</h1>
            <p class="subtitle">คู่มือเดินทางโตเกียว | Reference Guide</p>
            <div class="header-actions">
                <button onclick="expandAll()">📖 เปิดทั้งหมด</button>
                <button onclick="collapseAll()">📑 ย่อทั้งหมด</button>
                <button onclick="togglePrintMode()">🖨️ โหมดพิมพ์</button>
            </div>
        </header>
        
        <!-- Navigation -->
        <nav class="guidebook-nav">
            <h3>📋 สารบัญ</h3>
            {nav_html}
        </nav>
        
        <!-- Main Content -->
        <main class="guidebook-main">
            {sections_html}
        </main>
        
        <!-- Footer -->
        <footer class="guidebook-footer">
            <p>Generated on {datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
            <p>🌸 Tokyo Trip March 2026 - Guidebook Edition</p>
        </footer>
    </div>
    
    <script>{js}</script>
</body>
</html>'''

    def _generate_navigation(self, guidebook_data):
        """Generate table of contents navigation"""
        nav_items = []
        
        for section_key, section_data in guidebook_data.items():
            if section_data['content'].strip():
                title = section_data['title']
                nav_items.append(f'<a href="#{section_key}" class="nav-item">{title}</a>')
        
        return '\\n'.join(nav_items)

    def _get_guidebook_css(self):
        """Get CSS for guidebook layout"""
        return '''
        :root {
            --primary: #2E86AB;
            --secondary: #A23B72;
            --accent: #F18F01;
            --success: #C73E1D;
            --background: #FAFBFC;
            --card-bg: #FFFFFF;
            --text-primary: #2C3E50;
            --text-secondary: #64748B;
            --border: #E2E8F0;
            --shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            --shadow-lg: 0 8px 30px rgba(0, 0, 0, 0.12);
            --border-radius: 10px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.7;
            color: var(--text-primary);
            background: linear-gradient(135deg, var(--background) 0%, #F0F8FF 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }

        .guidebook-header {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            margin-bottom: 2rem;
        }

        .guidebook-header h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .guidebook-header .subtitle {
            font-size: 1.4rem;
            opacity: 0.9;
            margin-bottom: 2rem;
        }

        .header-actions {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }

        .header-actions button {
            padding: 0.8rem 1.8rem;
            border: 2px solid rgba(255,255,255,0.3);
            background: rgba(255,255,255,0.15);
            color: white;
            border-radius: 30px;
            cursor: pointer;
            font-weight: 600;
            font-size: 1rem;
            transition: var(--transition);
            backdrop-filter: blur(10px);
        }

        .header-actions button:hover {
            background: rgba(255,255,255,0.25);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .guidebook-nav {
            background: var(--card-bg);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            padding: 1.5rem;
            margin-bottom: 2rem;
            border-left: 4px solid var(--primary);
        }

        .guidebook-nav h3 {
            color: var(--primary);
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }

        .nav-item {
            display: block;
            padding: 0.7rem 1rem;
            color: var(--text-primary);
            text-decoration: none;
            border-radius: 6px;
            margin-bottom: 0.3rem;
            transition: var(--transition);
            border-left: 3px solid transparent;
        }

        .nav-item:hover {
            background: var(--background);
            border-left-color: var(--accent);
            transform: translateX(5px);
        }

        .guidebook-main {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .guidebook-section {
            background: var(--card-bg);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: var(--transition);
        }

        .guidebook-section:hover {
            box-shadow: var(--shadow-lg);
        }

        .section-header {
            padding: 1.5rem 2rem;
            background: linear-gradient(135deg, #F8FAFF 0%, #EEF6FF 100%);
            border-bottom: 1px solid var(--border);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: var(--transition);
        }

        .section-header:hover {
            background: linear-gradient(135deg, #EEF6FF 0%, #E1EFFF 100%);
        }

        .section-header h2 {
            color: var(--primary);
            font-size: 1.5rem;
            font-weight: 600;
        }

        .toggle-indicator {
            font-size: 1.2rem;
            color: var(--text-secondary);
            transition: transform 0.3s ease;
        }

        .section-expanded .toggle-indicator {
            transform: rotate(180deg);
        }

        .section-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease;
        }

        .section-expanded .section-content {
            max-height: 5000px;
            padding: 2rem;
        }

        .section-content h1,
        .section-content h2,
        .section-content h3 {
            color: var(--primary);
            margin: 1.5rem 0 1rem 0;
        }

        .section-content h1 { font-size: 1.8rem; }
        .section-content h2 { font-size: 1.5rem; }
        .section-content h3 { font-size: 1.3rem; }

        .section-content p {
            margin-bottom: 1rem;
            line-height: 1.7;
        }

        .section-content ul {
            margin: 1rem 0;
            padding-left: 1.5rem;
        }

        .section-content li {
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }

        .section-content li.sub-item {
            margin-left: 1rem;
            font-size: 0.95rem;
            color: var(--text-secondary);
        }

        .table-container {
            overflow-x: auto;
            margin: 1.5rem 0;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
        }

        .guidebook-table {
            width: 100%;
            border-collapse: collapse;
            background: var(--card-bg);
        }

        .guidebook-table th,
        .guidebook-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        .guidebook-table th {
            background: var(--primary);
            color: white;
            font-weight: 600;
        }

        .guidebook-table tbody tr:hover {
            background: var(--background);
        }

        .info-box,
        .note-box,
        .tip-box,
        .warning-box {
            margin: 1.5rem 0;
            padding: 1.2rem;
            border-radius: var(--border-radius);
            border-left: 4px solid;
        }

        .info-box {
            background: #E8F4FD;
            border-left-color: var(--primary);
        }

        .note-box {
            background: #FFF8E7;
            border-left-color: var(--accent);
        }

        .tip-box {
            background: #E8F8F5;
            border-left-color: var(--success);
        }

        .warning-box {
            background: #FFF2F2;
            border-left-color: #EF4444;
        }

        .info-box h4,
        .note-box h4,
        .tip-box h4,
        .warning-box h4 {
            margin-bottom: 0.8rem;
            font-weight: 600;
        }

        .guidebook-footer {
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            color: var(--text-secondary);
            border-top: 1px solid var(--border);
        }

        .print-mode .section-content {
            max-height: none !important;
            padding: 1.5rem !important;
        }

        .print-mode .toggle-indicator,
        .print-mode .header-actions {
            display: none !important;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 0.5rem;
            }
            
            .guidebook-header {
                padding: 2rem 1rem;
            }
            
            .guidebook-header h1 {
                font-size: 2.2rem;
            }
            
            .section-header {
                padding: 1rem 1.5rem;
            }
            
            .section-expanded .section-content {
                padding: 1.5rem;
            }
            
            .header-actions {
                flex-direction: column;
                align-items: center;
            }
            
            .header-actions button {
                width: 200px;
            }
        }

        @media print {
            body {
                background: white !important;
            }
            
            .section-content {
                max-height: none !important;
                padding: 1rem !important;
            }
            
            .toggle-indicator,
            .header-actions {
                display: none !important;
            }
        }
        '''

    def _get_guidebook_js(self):
        """Get JavaScript for guidebook functionality"""
        return '''
        function toggleSection(sectionId) {
            const section = document.getElementById(sectionId);
            section.classList.toggle('section-expanded');
        }

        function expandAll() {
            const sections = document.querySelectorAll('.guidebook-section');
            sections.forEach(section => {
                section.classList.add('section-expanded');
            });
        }

        function collapseAll() {
            const sections = document.querySelectorAll('.guidebook-section');
            sections.forEach(section => {
                section.classList.remove('section-expanded');
            });
        }

        function togglePrintMode() {
            document.body.classList.toggle('print-mode');
            
            if (document.body.classList.contains('print-mode')) {
                expandAll();
            }
        }

        // Smooth scrolling for navigation links
        document.querySelectorAll('.nav-item').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const targetSection = document.getElementById(targetId);
                
                // Expand the target section
                targetSection.classList.add('section-expanded');
                
                // Scroll to target
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            });
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

        // Auto-expand overview section on load
        document.addEventListener('DOMContentLoaded', function() {
            const overviewSection = document.getElementById('overview');
            if (overviewSection) {
                overviewSection.classList.add('section-expanded');
            }
        });
        '''

    def generate(self):
        """Main generation process"""
        print("\\n📖 Starting Guidebook HTML generation...")
        
        # Get content data
        content_data = self.get_content_data()
        if not content_data:
            print("❌ No content found. Aborting.")
            return
        
        # Organize into guidebook structure
        guidebook_data = self.organize_guidebook_data(content_data)
        
        # Generate HTML
        html_content = self.generate_guidebook_html(guidebook_data)
        
        # Generate output filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_filename = f"Tokyo-Trip-Guidebook-v1.0-{timestamp}.html"
        output_path = self.build_dir / output_filename
        
        # Write file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            file_size = output_path.stat().st_size
            print("\\n📖 Guidebook HTML generation complete!")
            print(f"   - File: {output_filename}")
            print(f"   - Path: {output_path}")
            print(f"   - Size: {file_size / 1024:.2f} KB")
            print("\\n📋 Guidebook Sections:")
            print("   ✅ 🗼 ภาพรวมการเดินทาง")
            print("   ✅ 🏨 ที่พัก")
            print("   ✅ 🍽️ ร้านอาหารแนะนำ")
            print("   ✅ 🛍️ ช้อปปิ้ง")
            print("   ✅ 📷 การซื้อกล้อง")
            print("   ✅ 🚊 การเดินทาง")
            print("   ✅ 💰 งบประมาณ")
            print("   ✅ 🌤️ สภาพอากาศ")
            print("   ✅ 💡 เคล็ดลับ")
            
        except Exception as e:
            print(f"❌ Error writing HTML file: {e}")

def main():
    """Main function"""
    print("📖 Tokyo Trip Guidebook Generator v1.0")
    print("=" * 50)
    print("🆕 Features:")
    print("   - Reference guide format")
    print("   - Organized by categories")
    print("   - Collapsible sections")
    print("   - Printer-friendly mode")
    print("   - Table of contents")
    print("=" * 50)
    
    generator = TokyoGuidebookGenerator()
    generator.generate()

if __name__ == "__main__":
    main()