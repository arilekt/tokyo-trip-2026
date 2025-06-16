#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokyo Trip 2026 HTML Generator (Refactored & Enhanced)
===============================================
Refactored เพื่อรวมทุก feature ให้อยู่ในไฟล์เดียว:
- อ่าน *.md files จาก content/ folder
- ใช้ template-skeleton.html เป็น base template
- รวม CSS และ JS inline ลงไฟล์ HTML เดียว
- สร้าง HTML ที่ responsive และใช้งานออฟไลน์ได้
- รองรับภาษาไทย/อังกฤษ (เพิ่ม Japanese ในอนาคต)
- Generate ลง build/ folder ตามวันที่

Author: Claude (AI Assistant) 
Date: June 2025
For: Arilek & Pojai's Tokyo Trip 2026
"""

import os
import re
import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import html


@dataclass
class TokgeneConfig:
    """Configuration class สำหรับ Tokyo Trip Generator"""
    script_dir: Path
    content_dir: Path
    build_dir: Path
    template_file: Path
    base_name: str = "Tokyo-Trip-March-2026"
    version: str = "Claude-Enhanced"


class MarkdownProcessor:
    """Class สำหรับ process markdown content"""
    
    @staticmethod
    def md_to_html_basic(md_text: str) -> str:
        """แปลง markdown เป็น HTML แบบ basic สำหรับเนื้อหาทั่วไป"""
        if not md_text.strip():
            return ""
            
        lines = md_text.strip().splitlines()
        html_parts = []
        in_ul = False
        in_table = False
        table_headers = []
        
        for line in lines:
            line = line.strip()
            
            # Handle empty lines
            if not line:
                if in_ul:
                    html_parts.append("</ul>")
                    in_ul = False
                html_parts.append("")
                continue
                
            # Handle headings
            if line.startswith("# "):
                if in_ul:
                    html_parts.append("</ul>")
                    in_ul = False
                html_parts.append(f"<h1>{html.escape(line[2:])}</h1>")
                continue
            elif line.startswith("## "):
                if in_ul:
                    html_parts.append("</ul>")
                    in_ul = False
                html_parts.append(f"<h2>{html.escape(line[3:])}</h2>")
                continue
            elif line.startswith("### "):
                if in_ul:
                    html_parts.append("</ul>")
                    in_ul = False
                html_parts.append(f"<h3>{html.escape(line[4:])}</h3>")
                continue
                
            # Handle tables
            if line.startswith("|"):
                if not in_table:
                    html_parts.append('<div class="table-container">')
                    html_parts.append('<table>')
                    in_table = True
                    
                cells = [cell.strip() for cell in line.split("|")[1:-1]]
                
                # Check if this is header separator
                if all(cell.strip().replace("-", "").replace(":", "") == "" for cell in cells):
                    continue
                    
                # First row or header row
                if not table_headers:
                    table_headers = cells
                    html_parts.append("<thead><tr>")
                    for cell in cells:
                        html_parts.append(f"<th>{html.escape(cell)}</th>")
                    html_parts.append("</tr></thead><tbody>")
                else:
                    html_parts.append("<tr>")
                    for cell in cells:
                        # Process text formatting in cells
                        cell_html = MarkdownProcessor._process_inline_formatting(cell)
                        html_parts.append(f"<td>{cell_html}</td>")
                    html_parts.append("</tr>")
                continue
            else:
                if in_table:
                    html_parts.append("</tbody></table></div>")
                    in_table = False
                    table_headers = []
                    
            # Handle lists
            if line.startswith("- "):
                if not in_ul:
                    html_parts.append("<ul>")
                    in_ul = True
                item_content = MarkdownProcessor._process_inline_formatting(line[2:])
                html_parts.append(f"<li>{item_content}</li>")
                continue
                
            # Regular paragraph
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
                
            if line:
                processed_line = MarkdownProcessor._process_inline_formatting(line)
                html_parts.append(f"<p>{processed_line}</p>")
        
        # Close any open tags
        if in_ul:
            html_parts.append("</ul>")
        if in_table:
            html_parts.append("</tbody></table></div>")
            
        return "\n".join(html_parts)
    
    @staticmethod
    def _process_inline_formatting(text: str) -> str:
        """Process inline markdown formatting"""
        # Bold text **text**
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        # Italic text *text*
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        # Code `text`
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
        # Don't escape HTML if it contains our formatting tags
        if '<strong>' in text or '<em>' in text or '<code>' in text:
            return text
        # Escape remaining HTML for safety
        return html.escape(text, quote=False)
        
    @staticmethod
    def process_timeline_content(md_text: str) -> str:
        """แปลง timeline markdown เป็น HTML timeline ที่มี nested structure"""
        if not re.search(r'^- \*\*\d+:\d+\*\*:', md_text, re.MULTILINE):
            return MarkdownProcessor.md_to_html_basic(md_text)
            
        lines = md_text.strip().splitlines()
        html_parts = ['<ul class="timeline">']
        current_timeline_item = None
        in_nested_content = False
        
        for line in lines:
            original_line = line
            line = line.strip()
            
            # Main timeline item: - **HH:MM**: content
            if line.startswith("- **") and "**:" in line:
                # Close previous item if exists
                if current_timeline_item is not None:
                    if in_nested_content:
                        current_timeline_item += "</div>"
                    current_timeline_item += "</li>"
                    html_parts.append(current_timeline_item)
                
                # Start new timeline item
                match = re.match(r'- \*\*([^*]+)\*\*:\s*(.*)', line)
                if match:
                    time_part = match.group(1)
                    content_part = MarkdownProcessor._process_inline_formatting(match.group(2))
                    current_timeline_item = f'<li><strong>{time_part}</strong>: {content_part}'
                    in_nested_content = False
                    
            # Nested content (indented with spaces)
            elif original_line.startswith("  ") and current_timeline_item is not None:
                if not in_nested_content:
                    current_timeline_item += '<div class="timeline-detail">'
                    in_nested_content = True
                    
                nested_content = original_line[2:].strip()  # Remove 2 spaces
                if nested_content.startswith("- "):
                    # Nested list item
                    item_content = MarkdownProcessor._process_inline_formatting(nested_content[2:])
                    current_timeline_item += f'<p>• {item_content}</p>'
                elif nested_content:
                    # Regular nested content
                    processed_content = MarkdownProcessor._process_inline_formatting(nested_content)
                    current_timeline_item += f'<p>{processed_content}</p>'
                    
            # Regular list item
            elif line.startswith("- ") and not line.startswith("- **"):
                # Close current timeline item first
                if current_timeline_item is not None:
                    if in_nested_content:
                        current_timeline_item += "</div>"
                    current_timeline_item += "</li>"
                    html_parts.append(current_timeline_item)
                    current_timeline_item = None
                    in_nested_content = False
                
                content = MarkdownProcessor._process_inline_formatting(line[2:])
                html_parts.append(f'<li>{content}</li>')
                
            # Regular paragraph
            elif line and not line.startswith("#"):
                # Close current timeline item first
                if current_timeline_item is not None:
                    if in_nested_content:
                        current_timeline_item += "</div>"
                    current_timeline_item += "</li>"
                    html_parts.append(current_timeline_item)
                    current_timeline_item = None
                    in_nested_content = False
                
                processed_line = MarkdownProcessor._process_inline_formatting(line)
                html_parts.append(f'</ul><p>{processed_line}</p><ul class="timeline">')
        
        # Close the last timeline item
        if current_timeline_item is not None:
            if in_nested_content:
                current_timeline_item += "</div>"
            current_timeline_item += "</li>"
            html_parts.append(current_timeline_item)
        
        html_parts.append('</ul>')
        return "\n".join(html_parts)


class TemplateManager:
    """Class สำหรับจัดการ template และ CSS/JS"""
    
    @staticmethod
    def get_base_template() -> str:
        """Generate base HTML template with embedded CSS and JS"""
        return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tokyo Trip March 2026 - แผนการเดินทางโตเกียว</title>
    <!-- EMBEDDED_CSS -->
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
                <span class="th">✈️ ผู้เดินทาง: Arilek Thummontree & Pojai Thummontree (วันเกิดครบ 11 ปี)</span>
                <span class="en">✈️ Travelers: Arilek Thummontree & Pojai Thummontree (11th Birthday Trip)</span><br/>
                <span class="th">🗺️ เส้นทาง: Bangkok → Tokyo → Kawaguchiko → Tokyo → Bangkok</span>
                <span class="en">🗺️ Route: Bangkok → Tokyo → Kawaguchiko → Tokyo → Bangkok</span>
            </p>
        </header>

        <!-- CONTENT_SECTIONS -->
        
    </div>

    <a class="back-to-top" href="#toc">
        <span class="th">🔙 กลับไปหน้าหลัก</span>
        <span class="en">🔙 Back to Top</span>
    </a>

    <!-- EMBEDDED_JS -->
</body>
</html>'''

    @staticmethod
    def get_enhanced_css() -> str:
        """Generate enhanced CSS สำหรับ responsive design"""
        return '''
        :root {
            --primary-color: #2563eb;
            --primary-light: #3b82f6;
            --primary-dark: #1d4ed8;
            --text-color: #1f2937;
            --bg-color: #ffffff;
            --card-bg: #f8fafc;
            --border-color: #e5e7eb;
            --shadow: rgba(0, 0, 0, 0.1);
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info-bg: #dbeafe;
            --info-border: #3b82f6;
            --note-bg: #f3f4f6;
            --note-border: #6b7280;
            --table-header: #f1f5f9;
            --table-border: #d1d5db;
            --table-alt: #f9fafb;
            --pending: #8b5cf6;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
            padding-top: 3rem;
        }

        /* Language Switcher */
        .lang-switcher {
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
            display: flex;
            gap: 0.5rem;
        }

        .lang-btn {
            padding: 0.5rem 1rem;
            border: 2px solid var(--primary-color);
            background: white;
            color: var(--primary-color);
            border-radius: 0.5rem;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .lang-btn.active,
        .lang-btn:hover {
            background: var(--primary-color);
            color: white;
        }

        /* Language visibility */
        .lang-en .th,
        .lang-th .en {
            display: none;
        }

        .lang-th .th,
        .lang-en .en {
            display: inline;
        }

        .lang-en .en-block, 
        .lang-th .th-block {
            display: block;
        }

        .lang-en .th-block, 
        .lang-th .en-block {
            display: none;
        }

        /* Container */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }

        /* Header */
        header {
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, var(--primary-light), var(--primary-color));
            color: white;
            border-radius: 1rem;
            box-shadow: 0 4px 6px var(--shadow);
        }

        header h1 {
            font-size: 2rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }

        header h2 {
            font-size: 1.2rem;
            margin-bottom: 1rem;
            opacity: 0.9;
        }

        header p {
            font-size: 1rem;
            opacity: 0.8;
        }

        /* Sections */
        section {
            margin-bottom: 3rem;
            padding: 2rem;
            background: var(--card-bg);
            border-radius: 1rem;
            box-shadow: 0 2px 4px var(--shadow);
        }

        section h1 {
            color: var(--primary-color);
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
            border-bottom: 3px solid var(--primary-light);
            padding-bottom: 0.5rem;
        }

        section h2 {
            color: var(--primary-dark);
            font-size: 1.4rem;
            margin: 1.5rem 0 1rem 0;
        }

        section h3 {
            color: var(--text-color);
            font-size: 1.2rem;
            margin: 1rem 0 0.5rem 0;
        }

        /* Birthday badge */
        .birthday-badge {
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            font-size: 0.9rem;
            margin-left: 1rem;
            animation: sparkle 2s infinite;
        }

        @keyframes sparkle {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        /* Day overviews */
        .day-overviews {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .day-overview {
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            padding: 1.5rem;
            transition: all 0.3s ease;
            border-left: 4px solid var(--primary-color);
        }

        .day-overview:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px var(--shadow);
        }

        .day-overview h3 {
            margin-bottom: 1rem;
        }

        .day-overview h3 a {
            text-decoration: none;
            color: var(--primary-color);
        }

        .day-overview h3 a:hover {
            text-decoration: underline;
        }

        /* Timeline */
        .timeline {
            list-style: none;
            padding: 0;
            margin: 1.5rem 0;
            position: relative;
        }

        .timeline::before {
            content: '';
            position: absolute;
            left: 1rem;
            top: 0;
            bottom: 0;
            width: 2px;
            background: var(--primary-color);
        }

        .timeline li {
            position: relative;
            padding: 1rem 0 1rem 3rem;
            border-bottom: 1px solid var(--border-color);
        }

        .timeline li::before {
            content: '';
            position: absolute;
            left: 0.5rem;
            top: 1.5rem;
            width: 1rem;
            height: 1rem;
            background: var(--primary-color);
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 0 0 3px var(--primary-color);
        }

        .timeline li:last-child {
            border-bottom: none;
        }

        /* Timeline Detail */
        .timeline-detail {
            margin-top: 0.5rem;
            padding-left: 1rem;
            border-left: 2px solid var(--border-color);
            background: rgba(255, 255, 255, 0.7);
            border-radius: 0.25rem;
            padding: 0.75rem;
        }

        .timeline-detail p {
            margin: 0.25rem 0;
            font-size: 0.9rem;
            color: var(--text-color);
        }

        .timeline-detail p:first-child {
            margin-top: 0;
        }

        .timeline-detail p:last-child {
            margin-bottom: 0;
        }

        /* Tables */
        .table-container {
            overflow-x: auto;
            margin: 1.5rem 0;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px var(--shadow);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }

        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--table-border);
        }

        th {
            background: var(--table-header);
            font-weight: 600;
            color: var(--text-color);
        }

        tr:nth-child(even) {
            background: var(--table-alt);
        }

        tr:hover {
            background: var(--info-bg);
        }

        /* Info and Note boxes */
        .info-box, .note-box {
            border-left: 4px solid var(--info-border);
            background: var(--info-bg);
            padding: 1rem;
            margin: 1.5rem 0;
            border-radius: 0 0.5rem 0.5rem 0;
        }

        .note-box {
            border-left-color: var(--note-border);
            background: var(--note-bg);
        }

        .info-toggle, .note-toggle {
            cursor: pointer;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }

        .info-toggle::after, .note-toggle::after {
            content: "▼";
            transition: transform 0.3s ease;
        }

        .info-toggle.collapsed::after, .note-toggle.collapsed::after {
            transform: rotate(-90deg);
        }

        .info-detail, .note-detail {
            overflow: hidden;
            transition: max-height 0.3s ease;
        }

        .info-detail.collapsed, .note-detail.collapsed {
            max-height: 0;
        }

        /* Status indicators */
        .status {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-weight: 600;
            font-size: 0.875rem;
        }

        .status-complete {
            background: var(--success);
            color: white;
        }

        .status-pending {
            background: var(--warning);
            color: white;
        }

        .status-planning {
            background: var(--pending);
            color: white;
        }

        /* Back to top button */
        .back-to-top {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: var(--primary-color);
            color: white;
            padding: 1rem;
            border-radius: 50%;
            text-decoration: none;
            box-shadow: 0 4px 12px var(--shadow);
            transition: all 0.3s ease;
            z-index: 100;
        }

        .back-to-top:hover {
            background: var(--primary-dark);
            transform: translateY(-2px);
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .container {
                padding: 0.5rem;
            }

            header {
                padding: 1rem;
            }

            header h1 {
                font-size: 1.5rem;
            }

            section {
                padding: 1rem;
            }

            .day-overviews {
                grid-template-columns: 1fr;
            }

            .lang-switcher {
                top: 0.5rem;
                right: 0.5rem;
            }

            .back-to-top {
                bottom: 1rem;
                right: 1rem;
                padding: 0.75rem;
            }

            table {
                font-size: 0.875rem;
            }

            th, td {
                padding: 0.5rem;
            }
        }

        @media (max-width: 480px) {
            header h1 {
                font-size: 1.25rem;
            }

            header h2 {
                font-size: 1rem;
            }

            .timeline li {
                padding-left: 2rem;
            }

            .timeline::before {
                left: 0.5rem;
            }

            .timeline li::before {
                left: 0.25rem;
                width: 0.5rem;
                height: 0.5rem;
            }
        }
        '''

    @staticmethod
    def get_enhanced_js() -> str:
        """Generate enhanced JavaScript สำหรับ interactive features"""
        return '''
        // Language switching functionality
        function switchLanguage(lang) {
            const body = document.body;
            const buttons = document.querySelectorAll('.lang-btn');
            
            // Update body class
            body.className = `lang-${lang}`;
            
            // Update button states
            buttons.forEach(btn => {
                btn.classList.remove('active');
                if (btn.id === `btn-${lang}`) {
                    btn.classList.add('active');
                }
            });
            
            // Store preference in localStorage (if available)
            try {
                localStorage.setItem('tokyo-trip-lang', lang);
            } catch (e) {
                // Ignore if localStorage is not available
            }
        }

        // Collapsible info/note boxes
        function initializeCollapsibleBoxes() {
            const toggles = document.querySelectorAll('.info-toggle, .note-toggle');
            
            toggles.forEach(toggle => {
                toggle.addEventListener('click', function() {
                    const detail = this.nextElementSibling;
                    const isCollapsed = detail.classList.contains('collapsed');
                    
                    if (isCollapsed) {
                        detail.classList.remove('collapsed');
                        this.classList.remove('collapsed');
                        detail.style.maxHeight = detail.scrollHeight + 'px';
                    } else {
                        detail.classList.add('collapsed');
                        this.classList.add('collapsed');
                        detail.style.maxHeight = '0';
                    }
                });
            });
        }

        // Smooth scrolling for anchor links
        function initializeSmoothScrolling() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        }

        // Show/hide back to top button
        function initializeBackToTop() {
            const backToTop = document.querySelector('.back-to-top');
            
            window.addEventListener('scroll', function() {
                if (window.pageYOffset > 300) {
                    backToTop.style.opacity = '1';
                    backToTop.style.pointerEvents = 'auto';
                } else {
                    backToTop.style.opacity = '0.5';
                    backToTop.style.pointerEvents = 'none';
                }
            });
        }

        // Currency conversion (if needed in future)
        function updateCurrencyDisplay() {
            const yenToThb = 0.23; // Approximate rate, update as needed
            const yenElements = document.querySelectorAll('[data-yen]');
            
            yenElements.forEach(element => {
                const yenAmount = parseInt(element.dataset.yen);
                const thbAmount = Math.round(yenAmount * yenToThb);
                element.textContent = `¥${yenAmount.toLocaleString()} (฿${thbAmount.toLocaleString()})`;
            });
        }

        // Initialize everything when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            // Try to restore saved language preference
            try {
                const savedLang = localStorage.getItem('tokyo-trip-lang');
                if (savedLang && (savedLang === 'th' || savedLang === 'en')) {
                    switchLanguage(savedLang);
                }
            } catch (e) {
                // Default to Thai if localStorage not available
                switchLanguage('th');
            }
            
            // Initialize all interactive features
            initializeCollapsibleBoxes();
            initializeSmoothScrolling();
            initializeBackToTop();
            updateCurrencyDisplay();
            
            console.log('🇯🇵 Tokyo Trip 2026 - Ready for adventure! สนุกกับการเดินทางนะครับ!');
        });

        // Add some fun interactions
        document.addEventListener('DOMContentLoaded', function() {
            // Add click animation to day overview cards
            document.querySelectorAll('.day-overview').forEach(card => {
                card.addEventListener('click', function() {
                    this.style.transform = 'scale(0.98)';
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 150);
                });
            });

            // Add hover effect to timeline items
            document.querySelectorAll('.timeline li').forEach(item => {
                item.addEventListener('mouseenter', function() {
                    this.style.backgroundColor = 'var(--info-bg)';
                });
                
                item.addEventListener('mouseleave', function() {
                    this.style.backgroundColor = '';
                });
            });
        });
        '''


class TokygeneGenerator:
    """Main class สำหรับ generate HTML"""
    
    def __init__(self, config: TokgeneConfig):
        self.config = config
        self.markdown_processor = MarkdownProcessor()
        self.template_manager = TemplateManager()
        
    def read_markdown_files(self) -> Dict[str, str]:
        """อ่านไฟล์ markdown ทั้งหมดจาก content directory"""
        markdown_contents = {}
        
        if not self.config.content_dir.exists():
            print(f"⚠️  Content directory ไม่พบ: {self.config.content_dir}")
            return markdown_contents
            
        for md_file in self.config.content_dir.glob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    section_id = md_file.stem.replace('_', '-').replace(' ', '-').lower()
                    markdown_contents[section_id] = content
                    print(f"✅ อ่านไฟล์: {md_file.name} -> {section_id}")
            except Exception as e:
                print(f"❌ ไม่สามารถอ่านไฟล์ {md_file.name}: {e}")
                
        return markdown_contents
    
    def create_overview_section(self, markdown_contents: Dict[str, str]) -> str:
        """สร้าง overview section จาก day files"""
        overview_html = '''
        <section id="overview">
            <h1>
                <span class="th th-block">ภาพรวมการเดินทางและกิจกรรม</span>
                <span class="en en-block">Travel Overview and Activities</span>
            </h1>
            <div class="day-overviews">
        '''
        
        # หา day files และเรียงลำดับ
        day_files = [(k, v) for k, v in markdown_contents.items() if k.startswith('day')]
        day_files.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()) if re.search(r'\d+', x[0]) else 0)
        
        for section_id, content in day_files:
            # ดึง title จาก markdown
            title_match = re.search(r'^#+\s*(.+?)(?:\n|$)', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                
                # แยก Thai/English title
                thai_title = title
                english_title = title
                if ' - ' in title:
                    parts = title.split(' - ', 1)
                    thai_title = parts[0].strip()
                    english_title = parts[1].strip()
                
                # ดึง description (paragraph แรกที่ไม่ใช่ header/list)
                lines = content.split('\n')
                description = ""
                for line in lines:
                    line = line.strip()
                    if (line and 
                        not line.startswith('#') and 
                        not line.startswith('-') and 
                        not line.startswith('|') and
                        not line.startswith('*') and
                        not re.match(r'^\d+\.', line) and
                        len(line) > 10):  # มีความยาวพอสมควร
                        
                        # ตัด description ที่ยาวเกินไป
                        if len(line) > 150:
                            description = line[:147] + "..."
                        else:
                            description = line
                        break
                
                # เพิ่ม birthday badge สำหรับวันที่ 4
                birthday_badge = ""
                if section_id == "day4":
                    birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
                
                overview_html += f'''
                <div class="day-overview">
                    <h3>
                        <a href="#{section_id}">
                            <span class="th">{thai_title}</span>
                            <span class="en">{english_title}</span>
                        </a>
                        {birthday_badge}
                    </h3>
                    <p>
                        <span class="th">{description}</span>
                        <span class="en">{description}</span>
                    </p>
                </div>
                '''
        
        # เพิ่ม budget overview card
        if 'budget' in markdown_contents:
            overview_html += '''
            <div class="day-overview">
                <h3>
                    <a href="#budget">
                        <span class="th">ประมาณการค่าใช้จ่ายและสถานะ</span>
                        <span class="en">Budget Estimate and Status</span>
                    </a>
                </h3>
                <p>
                    <span class="th">ข้อมูลการจอง และประมาณการค่าใช้จ่าย</span>
                    <span class="en">Booking information and estimated expenses</span>
                </p>
            </div>
            '''
        
        overview_html += '''
            </div>
            <div class="note-box">
                <div class="note-toggle">
                    <span class="th">ℹ️ วิธีการใช้งานแผนการเดินทาง</span>
                    <span class="en">ℹ️ How to Use the Itinerary</span>
                </div>
                <div class="note-detail">
                    <p class="th th-block">แผนการเดินทางรวมอยู่ในไฟล์เดียวเพื่อความสะดวกในการใช้งานออฟไลน์</p>
                    <p class="en en-block">The itinerary is consolidated into a single file for easy offline use.</p>
                    <p class="th th-block">คลิกที่หัวข้อเพื่อขยายดูรายละเอียดเพิ่มเติม และใช้ปุ่ม "กลับไปหน้าหลัก" ด้านล่างขวาเพื่อไปยังสารบัญ</p>
                    <p class="en en-block">Click on headings to expand for more details, and use the "Back to Top" button at the bottom right to navigate to the table of contents.</p>
                    <p class="th th-block">ใช้ปุ่ม TH/EN ที่มุมบนขวา เพื่อสลับภาษา</p>
                    <p class="en en-block">Use the TH/EN buttons at the top right to switch languages.</p>
                </div>
            </div>
        </section>
        '''
        
        return overview_html
    
    def process_section_content(self, section_id: str, content: str) -> str:
        """Process เนื้อหาของแต่ละ section"""
        # ดึง title และ content แยกกัน
        title_match = re.search(r'^#+\s*(.+?)(?:\n|$)', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else f"Section {section_id}"
        
        # ลบ title ออกจาก content
        body_content = re.sub(r'^#+\s*.+?(?:\n|$)', '', content, count=1, flags=re.MULTILINE).strip()
        
        # แยก Thai/English title
        thai_title = title
        english_title = title
        if ' - ' in title:
            parts = title.split(' - ', 1)
            thai_title = parts[0].strip()
            english_title = parts[1].strip()
        
        # เพิ่ม birthday badge สำหรับวันที่ 4
        birthday_badge = ""
        if section_id == "day4":
            birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
        
        # Process content based on type
        if re.search(r'^- \*\*\d+:\d+\*\*:', body_content, re.MULTILINE):
            # Timeline content
            processed_content = self.markdown_processor.process_timeline_content(body_content)
        else:
            # Regular content
            processed_content = self.markdown_processor.md_to_html_basic(body_content)
        
        return f'''
        <section id="{section_id}">
            <h1>
                <span class="th th-block">{thai_title}</span>
                <span class="en en-block">{english_title}</span>
                {birthday_badge}
            </h1>
            {processed_content}
        </section>
        '''
    
    def generate_html(self) -> str:
        """Generate HTML ไฟล์สมบูรณ์"""
        print("🚀 เริ่มต้น generate HTML...")
        
        # อ่าน markdown files
        markdown_contents = self.read_markdown_files()
        if not markdown_contents:
            print("❌ ไม่พบไฟล์ markdown ใดๆ")
            return ""
        
        # สร้าง base template
        template = self.template_manager.get_base_template()
        
        # Embed CSS และ JS
        css_content = self.template_manager.get_enhanced_css()
        js_content = self.template_manager.get_enhanced_js()
        
        template = template.replace('<!-- EMBEDDED_CSS -->', f'<style>\n{css_content}\n</style>')
        template = template.replace('<!-- EMBEDDED_JS -->', f'<script>\n{js_content}\n</script>')
        
        # สร้าง content sections
        sections_html = ""
        
        # เริ่มด้วย overview section
        sections_html += self.create_overview_section(markdown_contents)
        
        # จัดเรียงและสร้าง sections อื่นๆ
        section_order = [
            'weather-info', 'day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8',
            'budget', 'accommodation', 'timeline', 'food-recommendations', 'shopping-guide',
            'kawaguchiko-guide', 'important-updates', 'transportation-budget'
        ]
        
        for section_id in section_order:
            if section_id in markdown_contents:
                sections_html += self.process_section_content(section_id, markdown_contents[section_id])
        
        # เพิ่ม sections ที่เหลือ (ถ้ามี)
        for section_id, content in markdown_contents.items():
            if section_id not in section_order and not section_id.startswith('day'):
                sections_html += self.process_section_content(section_id, content)
        
        # แทนที่ content ใน template
        final_html = template.replace('<!-- CONTENT_SECTIONS -->', sections_html)
        
        return final_html
    
    def save_html_file(self, html_content: str) -> Path:
        """บันทึกไฟล์ HTML"""
        # สร้าง build directory ถ้ายังไม่มี
        self.config.build_dir.mkdir(parents=True, exist_ok=True)
        
        # สร้างชื่อไฟล์ตามวันที่
        today = datetime.date.today().strftime("%Y%m%d")
        filename = f"{self.config.base_name}-{self.config.version}-{today}.html"
        output_path = self.config.build_dir / filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ สร้างไฟล์สำเร็จ: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ ไม่สามารถบันทึกไฟล์: {e}")
            return None


def main():
    """Main function สำหรับรัน script"""
    print("=" * 60)
    print("🇯🇵 Tokyo Trip 2026 HTML Generator (Claude Enhanced)")
    print("=" * 60)
    
    # ตั้งค่า paths
    script_dir = Path(__file__).resolve().parent
    config = TokgeneConfig(
        script_dir=script_dir,
        content_dir=script_dir.parent / "content",
        build_dir=script_dir.parent / "build",
        template_file=script_dir / "template-skeleton.html"
    )
    
    print(f"📁 Script directory: {config.script_dir}")
    print(f"📁 Content directory: {config.content_dir}")
    print(f"📁 Build directory: {config.build_dir}")
    print()
    
    # สร้าง generator และ generate HTML
    generator = TokygeneGenerator(config)
    
    try:
        html_content = generator.generate_html()
        if html_content:
            output_path = generator.save_html_file(html_content)
            if output_path:
                print()
                print("🎉 สำเร็จ! HTML ไฟล์พร้อมใช้งานแล้ว")
                print(f"📱 ใช้งานได้บน: iPad, Android, Mobile (Offline)")
                print(f"🌐 รองรับ: Thai/English switching")
                print(f"📂 ไฟล์: {output_path}")
                print()
                print("🎯 Next steps:")
                print("   1. เปิดไฟล์ HTML บนอุปกรณ์ที่ต้องการใช้")
                print("   2. สำหรับ Japanese translation - รอ feature ต่อไป")
                print("   3. สนุกกับการเดินทาง! 🎌")
            else:
                print("❌ ไม่สามารถบันทึกไฟล์ได้")
        else:
            print("❌ ไม่สามารถ generate HTML ได้")
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()