#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokyo Trip 2026 HTML Generator v4 (Complete & Fixed)
===================================================
สมบูรณ์ครบทุก feature พร้อม debug logging และแก้ไข expand/collapse

Author: Claude (AI Assistant) 
Date: June 2025
Version: 4.0 - Complete & Fixed
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
    version: str = "Claude-Enhanced-v4-Fixed"


class MarkdownProcessor:
    """Class สำหรับ process markdown content"""
    
    @staticmethod
    def md_to_html_basic(md_text: str) -> str:
        """แปลง markdown เป็น HTML แบบ basic"""
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
                        cell_html = MarkdownProcessor._process_inline_formatting(cell)
                        html_parts.append(f"<td>{cell_html}</td>")
                    html_parts.append("</tr>")
                continue
            else:
                if in_table:
                    html_parts.append("</tbody></table></div>")
                    in_table = False
                    table_headers = []
                    
            if line.startswith("- "):
                if not in_ul:
                    html_parts.append("<ul>")
                    in_ul = True
                item_content = MarkdownProcessor._process_inline_formatting(line[2:])
                html_parts.append(f"<li>{item_content}</li>")
                continue
                
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
                
            if line:
                processed_line = MarkdownProcessor._process_inline_formatting(line)
                html_parts.append(f"<p>{processed_line}</p>")
        
        if in_ul:
            html_parts.append("</ul>")
        if in_table:
            html_parts.append("</tbody></table></div>")
            
        return "\n".join(html_parts)
    
    @staticmethod
    def _process_inline_formatting(text: str) -> str:
        """Process inline markdown formatting"""
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
        if '<strong>' in text or '<em>' in text or '<code>' in text:
            return text
        return html.escape(text, quote=False)
        
    @staticmethod
    def process_timeline_content(md_text: str) -> str:
        """แปลง timeline markdown เป็น HTML timeline พร้อม expand/collapse"""
        if not re.search(r'^- \*\*\d+:\d+\*\*:', md_text, re.MULTILINE):
            return MarkdownProcessor.md_to_html_basic(md_text)
            
        lines = md_text.strip().splitlines()
        html_parts = ['<ul class="timeline">']
        current_timeline_item = None
        in_nested_content = False
        item_id_counter = 0
        
        for line in lines:
            original_line = line
            line = line.strip()
            
            if line.startswith("- **") and "**:" in line:
                if current_timeline_item is not None:
                    if in_nested_content:
                        current_timeline_item += "</div>"
                    current_timeline_item += "</li>"
                    html_parts.append(current_timeline_item)
                
                match = re.match(r'- \*\*([^*]+)\*\*:\s*(.*)', line)
                if match:
                    time_part = match.group(1)
                    content_part = MarkdownProcessor._process_inline_formatting(match.group(2))
                    
                    # สร้าง timeline item พร้อม expand/collapse
                    item_id = f"timeline-{item_id_counter}"
                    item_id_counter += 1
                    
                    current_timeline_item = f'''<li>
                        <div class="timeline-main">
                            <strong>{time_part}</strong>: {content_part}
                        </div>'''
                    in_nested_content = False
                    
            elif original_line.startswith("  ") and current_timeline_item is not None:
                if not in_nested_content:
                    # สร้าง expand/collapse button และ detail div
                    current_timeline_item += f'''
                        <button class="timeline-toggle" onclick="toggleTimelineDetail('{item_id}')">
                            <span class="th">รายละเอียด ▼</span>
                            <span class="en">Details ▼</span>
                        </button>
                        <div class="timeline-detail" id="{item_id}" style="display: none;">'''
                    in_nested_content = True
                    
                nested_content = original_line[2:].strip()
                if nested_content.startswith("- "):
                    item_content = MarkdownProcessor._process_inline_formatting(nested_content[2:])
                    current_timeline_item += f'<p>• {item_content}</p>'
                elif nested_content:
                    processed_content = MarkdownProcessor._process_inline_formatting(nested_content)
                    current_timeline_item += f'<p>{processed_content}</p>'
                    
            elif line.startswith("- ") and not line.startswith("- **"):
                if current_timeline_item is not None:
                    if in_nested_content:
                        current_timeline_item += "</div>"
                    current_timeline_item += "</li>"
                    html_parts.append(current_timeline_item)
                    current_timeline_item = None
                    in_nested_content = False
                
                content = MarkdownProcessor._process_inline_formatting(line[2:])
                html_parts.append(f'<li><div class="timeline-main">{content}</div></li>')
                
            elif line and not line.startswith("#"):
                if current_timeline_item is not None:
                    if in_nested_content:
                        current_timeline_item += "</div>"
                    current_timeline_item += "</li>"
                    html_parts.append(current_timeline_item)
                    current_timeline_item = None
                    in_nested_content = False
                
                processed_line = MarkdownProcessor._process_inline_formatting(line)
                html_parts.append(f'</ul><p>{processed_line}</p><ul class="timeline">')
        
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
        """Generate base HTML template"""
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
        """Generate enhanced CSS พร้อม timeline styles"""
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

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }

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

        /* ===== TIMELINE STYLES (FIXED) ===== */
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

        .timeline-main {
            margin-bottom: 0.5rem;
        }

        .timeline-toggle {
            background: var(--primary-light);
            color: white;
            border: none;
            padding: 0.4rem 0.8rem;
            border-radius: 0.25rem;
            cursor: pointer;
            font-size: 0.8rem;
            margin: 0.5rem 0 0.25rem 0;
            transition: all 0.3s ease;
            display: inline-block;
        }

        .timeline-toggle:hover {
            background: var(--primary-color);
            transform: translateY(-1px);
        }

        .timeline-toggle.expanded {
            background: var(--success);
        }

        .timeline-toggle.expanded:hover {
            background: #059669;
        }

        .timeline-detail {
            margin-top: 0.5rem;
            padding: 0.75rem;
            border-left: 2px solid var(--border-color);
            background: rgba(255, 255, 255, 0.7);
            border-radius: 0.25rem;
            display: none;
            animation: slideDown 0.3s ease;
        }

        .timeline-detail.expanded {
            display: block;
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

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* ===== TABLE STYLES ===== */
        .table-container {
            overflow-x: auto;
            margin: 1.5rem 0;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px var(--shadow);
            background: white;
        }

        table {
            width: 100%;
            min-width: 600px;
            border-collapse: collapse;
            background: white;
            table-layout: auto;
        }

        th, td {
            padding: 0.75rem 0.5rem;
            text-align: left;
            border-bottom: 1px solid var(--table-border);
            vertical-align: top;
            word-wrap: break-word;
        }

        th {
            background: var(--table-header);
            font-weight: 600;
            color: var(--text-color);
            position: sticky;
            top: 0;
            z-index: 10;
        }

        td:last-child {
            text-align: center;
            white-space: nowrap;
        }

        td:nth-last-child(2) {
            text-align: right;
            font-weight: 600;
            font-family: 'Courier New', monospace;
        }

        tr:nth-child(even) {
            background: var(--table-alt);
        }

        tr:hover {
            background: var(--info-bg);
        }

        tr.total {
            background: var(--success) !important;
            color: white;
            font-weight: 700;
        }

        tr.total td {
            border-top: 2px solid var(--success);
        }

        tr.remaining {
            background: var(--note-bg) !important;
            font-weight: 600;
        }

        /* ===== INFO/NOTE BOXES ===== */
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

        @media (max-width: 480px) {
            header h1 {
                font-size: 1.25rem;
            }

            header h2 {
                font-size: 1rem;
            }
        }
        '''

    @staticmethod
    def get_enhanced_js() -> str:
        """Generate enhanced JavaScript พร้อม timeline toggle function"""
        return '''
        function switchLanguage(lang) {
            const body = document.body;
            const buttons = document.querySelectorAll('.lang-btn');
            
            body.classList.remove('lang-th', 'lang-en');
            body.classList.add(`lang-${lang}`);
            
            buttons.forEach(btn => {
                btn.classList.remove('active');
                if (btn.id === `btn-${lang}`) {
                    btn.classList.add('active');
                }
            });
            
            try {
                localStorage.setItem('tokyo-trip-lang', lang);
            } catch (e) {}
            
            console.log(`Language switched to: ${lang}`);
        }

        // ===== FIXED TIMELINE TOGGLE FUNCTION =====
        function toggleTimelineDetail(elementId) {
            const detailElement = document.getElementById(elementId);
            const toggleButton = document.querySelector(`button[onclick="toggleTimelineDetail('${elementId}')"]`);
            
            if (!detailElement || !toggleButton) {
                console.error(`Timeline element not found: ${elementId}`);
                return;
            }
            
            const isVisible = detailElement.style.display !== 'none';
            
            if (isVisible) {
                // Hide details
                detailElement.style.display = 'none';
                detailElement.classList.remove('expanded');
                toggleButton.classList.remove('expanded');
                toggleButton.innerHTML = '<span class="th">รายละเอียด ▼</span><span class="en">Details ▼</span>';
            } else {
                // Show details
                detailElement.style.display = 'block';
                detailElement.classList.add('expanded');
                toggleButton.classList.add('expanded');
                toggleButton.innerHTML = '<span class="th">รายละเอียด ▲</span><span class="en">Details ▲</span>';
            }
            
            console.log(`Timeline ${elementId} toggled: ${!isVisible ? 'shown' : 'hidden'}`);
        }

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

        function updateCurrencyDisplay() {
            const yenToThb = 0.23;
            const yenElements = document.querySelectorAll('[data-yen]');
            
            yenElements.forEach(element => {
                const yenAmount = parseInt(element.dataset.yen);
                const thbAmount = Math.round(yenAmount * yenToThb);
                element.textContent = `¥${yenAmount.toLocaleString()} (฿${thbAmount.toLocaleString()})`;
            });
        }

        function debugTimelineElements() {
            const timelineToggles = document.querySelectorAll('.timeline-toggle');
            const timelineDetails = document.querySelectorAll('.timeline-detail');
            
            console.log(`🔍 Debug Timeline:`, {
                toggleButtons: timelineToggles.length,
                detailElements: timelineDetails.length,
                togglesWithOnclick: Array.from(timelineToggles).filter(btn => btn.onclick).length
            });
            
            timelineToggles.forEach((btn, index) => {
                console.log(`Toggle ${index}:`, {
                    hasOnclick: !!btn.onclick,
                    innerHTML: btn.innerHTML.substring(0, 50) + '...'
                });
            });
        }

        document.addEventListener('DOMContentLoaded', function() {
            console.log('🇯🇵 Tokyo Trip 2026 v4 - Loading...');
            
            try {
                const savedLang = localStorage.getItem('tokyo-trip-lang');
                if (savedLang && (savedLang === 'th' || savedLang === 'en')) {
                    switchLanguage(savedLang);
                }
            } catch (e) {
                switchLanguage('th');
            }
            
            initializeCollapsibleBoxes();
            initializeSmoothScrolling();
            initializeBackToTop();
            updateCurrencyDisplay();
            
            // Debug timeline elements
            debugTimelineElements();
            
            // Add interactive effects
            document.querySelectorAll('.day-overview').forEach(card => {
                card.addEventListener('click', function() {
                    this.style.transform = 'scale(0.98)';
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 150);
                });
            });

            document.querySelectorAll('.timeline li').forEach(item => {
                item.addEventListener('mouseenter', function() {
                    this.style.backgroundColor = 'var(--info-bg)';
                });
                
                item.addEventListener('mouseleave', function() {
                    this.style.backgroundColor = '';
                });
            });
            
            console.log('✅ Tokyo Trip 2026 v4 - Ready with timeline expand/collapse!');
        });
        '''


class TokygeneGenerator:
    """Main class สำหรับ generate HTML"""
    
    def __init__(self, config: TokgeneConfig):
        self.config = config
        self.markdown_processor = MarkdownProcessor()
        self.template_manager = TemplateManager()
        
    def read_markdown_files(self) -> Dict[str, Dict[str, str]]:
        """อ่านไฟล์ markdown ทั้งหมดจาก content directory รองรับ multi-language"""
        print("🔍 เริ่มอ่านไฟล์ markdown...")
        
        markdown_contents = {'th': {}, 'en': {}}
        
        if not self.config.content_dir.exists():
            print(f"⚠️  Content directory ไม่พบ: {self.config.content_dir}")
            return markdown_contents
        
        print("📖 อ่านไฟล์ภาษาไทย...")
        self._read_language_files(self.config.content_dir, 'th', markdown_contents['th'])
        
        en_dir = self.config.content_dir / "en"
        if en_dir.exists():
            print(f"📁 พบ English content directory: {en_dir}")
            self._read_language_files(en_dir, 'en', markdown_contents['en'])
        else:
            print(f"📝 ไม่พบ English content (จะใช้ Thai เป็นค่าเริ่มต้น)")
            
        print(f"✅ อ่านไฟล์เสร็จ - Thai: {len(markdown_contents['th'])}, English: {len(markdown_contents['en'])}")
        return markdown_contents
    
    def _read_language_files(self, directory: Path, lang: str, content_dict: Dict[str, str]):
        """อ่านไฟล์ markdown จาก directory โดยเรียงตามหมายเลข"""
        md_files = list(directory.glob("*.md"))
        
        def sort_key(file_path):
            filename = file_path.stem
            number_match = re.match(r'^(\d+)', filename)
            if number_match:
                return (int(number_match.group(1)), filename)
            else:
                return (999999, filename)
        
        md_files.sort(key=sort_key)
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    section_id = self._generate_section_id(md_file.stem)
                    content_dict[section_id] = content
                    print(f"✅ อ่านไฟล์ ({lang}): {md_file.name} -> {section_id}")
                    
            except Exception as e:
                print(f"❌ ไม่สามารถอ่านไฟล์ {md_file.name}: {e}")
    
    def _generate_section_id(self, filename: str) -> str:
        """สร้าง section ID จากชื่อไฟล์"""
        section_id = re.sub(r'^\d+-?', '', filename)
        section_id = section_id.replace('_', '-').replace(' ', '-').lower()
        section_id = re.sub(r'[^a-z0-9\-]', '', section_id)
        return section_id
    
    def create_overview_section(self, markdown_contents: Dict[str, Dict[str, str]]) -> str:
        """สร้าง overview section จาก day files รองรับ multi-language"""
        print("🌟 เริ่มสร้าง overview section...")
        
        overview_html = '''
        <section id="overview">
            <h1>
                <span class="th th-block">ภาพรวมการเดินทางและกิจกรรม</span>
                <span class="en en-block">Travel Overview and Activities</span>
            </h1>
            <div class="day-overviews">
        '''
        
        try:
            th_contents = markdown_contents['th']
            en_contents = markdown_contents['en']
            
            print(f"🔍 th_contents in overview: {type(th_contents)}, length: {len(th_contents)}")
            
            day_files = [(k, v) for k, v in th_contents.items() if k.startswith('day') and not k.endswith('-additional')]
            day_files.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()) if re.search(r'\d+', x[0]) else 0)
            
            print(f"📅 พบ day files: {len(day_files)} วัน")
            
            for section_id, th_content in day_files:
                try:
                    en_content = en_contents.get(section_id, th_content)
                    
                    th_title_match = re.search(r'^#+\s*(.+?)(?:\n|$)', th_content, re.MULTILINE)
                    en_title_match = re.search(r'^#+\s*(.+?)(?:\n|$)', en_content, re.MULTILINE)
                    
                    if th_title_match:
                        th_title = th_title_match.group(1).strip()
                        en_title = en_title_match.group(1).strip() if en_title_match else th_title
                        
                        th_main_title = re.split(r'\s*[-–|/]\s*', th_title)[0].strip()
                        en_main_title = re.split(r'\s*[-–|/]\s*', en_title)[0].strip()
                        
                        th_description = self._extract_description(th_content)
                        en_description = self._extract_description(en_content) if en_content != th_content else th_description
                        
                        birthday_badge = ""
                        if section_id == "day4":
                            birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
                        
                        overview_html += f'''
                        <div class="day-overview">
                            <h3>
                                <a href="#{section_id}">
                                    <span class="th">{th_main_title}</span>
                                    <span class="en">{en_main_title}</span>
                                </a>
                                {birthday_badge}
                            </h3>
                            <p>
                                <span class="th">{th_description}</span>
                                <span class="en">{en_description}</span>
                            </p>
                        </div>
                        '''
                        print(f"    ✅ เพิ่ม day card: {section_id}")
                        
                except Exception as e:
                    print(f"    ⚠️ ข้าม {section_id}: {e}")
                    continue
            
            if 'budget' in th_contents:
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
                print(f"    ✅ เพิ่ม budget card")
            
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
                        <p class="th th-block">คลิกที่ปุ่ม "รายละเอียด" ในแต่ละกิจกรรมเพื่อดูข้อมูลเพิ่มเติม และใช้ปุ่ม "กลับไปหน้าหลัก" ด้านล่างขวาเพื่อไปยังสารบัญ</p>
                        <p class="en en-block">Click on "Details" buttons in each activity to expand for more information, and use the "Back to Top" button at the bottom right to navigate to the table of contents.</p>
                        <p class="th th-block">ใช้ปุ่ม TH/EN ที่มุมบนขวา เพื่อสลับภาษา</p>
                        <p class="en en-block">Use the TH/EN buttons at the top right to switch languages.</p>
                    </div>
                </div>
            </section>
            '''
            
            print("✅ สร้าง overview section เสร็จสิ้น")
            return overview_html
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการสร้าง overview: {e}")
            import traceback
            traceback.print_exc()
            return '''
            <section id="overview">
                <h1>
                    <span class="th th-block">ภาพรวมการเดินทางและกิจกรรม</span>
                    <span class="en en-block">Travel Overview and Activities</span>
                </h1>
                <p>กำลังโหลดข้อมูล...</p>
            </section>
            '''
            