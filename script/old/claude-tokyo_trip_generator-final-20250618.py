#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokyo Trip 2026 HTML Generator - FINAL VERSION
==============================================
Complete self-contained HTML generator for Tokyo trip itinerary

Author: Claude (AI Assistant) 
Date: June 18, 2025
Version: FINAL-20250618
For: Arilek & Pojai's Tokyo Trip 2026

Features:
✅ Timeline expand/collapse functionality
✅ Multi-language support (TH/EN)  
✅ Self-contained HTML (no external dependencies)
✅ Mobile responsive design
✅ Offline-ready output

Usage: python claude-tokyo_trip_generator-final-20250618.py
"""

import os
import re
import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import html


@dataclass 
class TripConfig:
    """Configuration for Tokyo Trip Generator"""
    script_dir: Path
    content_dir: Path 
    build_dir: Path
    base_name: str = "Tokyo-Trip-March-2026"
    version: str = "FINAL-20250618"
    debug: bool = True
    
    def __post_init__(self):
        """Ensure directories exist and are valid"""
        if self.debug:
            print(f"🔧 Config initialized:")
            print(f"   Script dir: {self.script_dir}")
            print(f"   Content dir: {self.content_dir}")
            print(f"   Build dir: {self.build_dir}")
            
class MarkdownProcessor:
    """Enhanced markdown to HTML processor with timeline support"""
    
    def __init__(self, debug: bool = True):
        self.debug = debug
        self.timeline_counter = 0
    
    def basic_md_to_html(self, md_text: str) -> str:
        """Convert basic markdown to HTML"""
        if not md_text or not md_text.strip():
            return ""
            
        lines = md_text.strip().splitlines()
        html_parts = []
        in_ul = False
        in_table = False
        table_headers = []
        
        if self.debug:
            print(f"📝 Processing {len(lines)} lines of markdown")
        
        for i, line in enumerate(lines):
            line = line.rstrip()
            
            # Empty lines
            if not line:
                if in_ul:
                    html_parts.append("</ul>")
                    in_ul = False
                if in_table:
                    html_parts.append("</tbody></table></div>")
                    in_table = False
                    table_headers = []
                html_parts.append("")
                continue
            
            # Headers
            if line.startswith("### "):
                self._close_lists_and_tables(html_parts, in_ul, in_table)
                in_ul = in_table = False
                table_headers = []
                header_text = html.escape(line[4:].strip())
                html_parts.append(f"<h3>{header_text}</h3>")
                continue
            elif line.startswith("## "):
                self._close_lists_and_tables(html_parts, in_ul, in_table)
                in_ul = in_table = False
                table_headers = []
                header_text = html.escape(line[3:].strip())
                html_parts.append(f"<h2>{header_text}</h2>")
                continue
            elif line.startswith("# "):
                self._close_lists_and_tables(html_parts, in_ul, in_table)
                in_ul = in_table = False
                table_headers = []
                header_text = html.escape(line[2:].strip())
                html_parts.append(f"<h1>{header_text}</h1>")
                continue
                
            # Tables
            if line.startswith("|"):
                if not in_table:
                    if in_ul:
                        html_parts.append("</ul>")
                        in_ul = False
                    html_parts.append('<div class="table-container">')
                    html_parts.append('<table>')
                    in_table = True
                    
                cells = [cell.strip() for cell in line.split("|")[1:-1]]
                
                # Skip separator rows
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
                        cell_html = self._process_inline_markdown(cell)
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
                item_content = self._process_inline_markdown(line[2:])
                html_parts.append(f"<li>{item_content}</li>")
                continue
                
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
                
            # Regular paragraphs
            if line.strip():
                processed_line = self._process_inline_markdown(line)
                html_parts.append(f"<p>{processed_line}</p>")
        
        # Close any remaining open tags
        if in_ul:
            html_parts.append("</ul>")
        if in_table:
            html_parts.append("</tbody></table></div>")
            
        result = "\n".join(html_parts)
        if self.debug:
            print(f"✅ Converted to {len(result)} characters of HTML")
        return result
    
    def _close_lists_and_tables(self, html_parts: List[str], in_ul: bool, in_table: bool):
        """Helper to close open lists and tables"""
        if in_ul:
            html_parts.append("</ul>")
        if in_table:
            html_parts.append("</tbody></table></div>")
    
    def _process_inline_markdown(self, text: str) -> str:
        """Process inline markdown like **bold**, *italic*, etc."""
        # Bold
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        # Code
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
        
        # If we already have HTML tags, don't escape
        if '<' in text and '>' in text:
            return text
        
        # Otherwise escape HTML
        return html.escape(text, quote=False)
        
    def process_timeline_markdown(self, md_text: str) -> str:
        """Process timeline markdown with expand/collapse functionality"""
        if not md_text or not md_text.strip():
            return ""
        
        # Check if this looks like a timeline
        if not re.search(r'^- \*\*\d+:\d+\*\*:', md_text, re.MULTILINE):
            if self.debug:
                print("📋 No timeline pattern found, using basic markdown")
            return self.basic_md_to_html(md_text)
            
        if self.debug:
            print("⏰ Processing timeline markdown")
            
        lines = md_text.strip().splitlines()
        html_parts = ['<ul class="timeline">']
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Timeline item with time
            if line.startswith("- **") and "**:" in line:
                match = re.match(r'- \*\*([^*]+)\*\*:\s*(.*)', line)
                if match:
                    time_part = html.escape(match.group(1))
                    content_part = self._process_inline_markdown(match.group(2))
                    
                    # Look for nested content
                    nested_content = []
                    j = i + 1
                    
                    while j < len(lines):
                        next_line = lines[j]
                        # Stop if we hit another timeline item
                        if next_line.strip().startswith("- **") and "**:" in next_line.strip():
                            break
                        # Stop if empty line and next line is timeline item
                        if not next_line.strip() and j + 1 < len(lines):
                            lookahead = lines[j + 1].strip()
                            if lookahead.startswith("- **") and "**:" in lookahead:
                                break
                        
                        if next_line.strip():
                            nested_content.append(next_line)
                        j += 1
                    
                    # Create timeline item
                    item_id = f"timeline-{self.timeline_counter}"
                    html_parts.append('<li>')
                    html_parts.append('<div class="timeline-main">')
                    html_parts.append(f'<strong>{time_part}</strong>: {content_part}')
                    html_parts.append('</div>')
                    
                    # Add expandable details if there's nested content
                    if nested_content:
                        html_parts.append(f'''
                        <button class="timeline-toggle" onclick="toggleTimelineDetail('{item_id}')">
                            <span class="th">▶</span>
                            <span class="en">▶</span>
                        </button>
                        <div class="timeline-detail" id="{item_id}" style="display: none;">''')
                        
                        # Process nested content
                        nested_html = self.basic_md_to_html('\n'.join(nested_content))
                        html_parts.append(nested_html)
                        html_parts.append('</div>')
                    
                    html_parts.append('</li>')
                    self.timeline_counter += 1
                    i = j - 1
            
            # Regular list item (no time)
            elif line.startswith("- ") and not line.startswith("- **"):
                content = self._process_inline_markdown(line[2:])
                html_parts.append('<li>')
                html_parts.append(f'<div class="timeline-main">{content}</div>')
                html_parts.append('</li>')
            
            # Non-list content
            elif line and not line.startswith("#"):
                html_parts.append('</ul>')
                processed_line = self._process_inline_markdown(line)
                html_parts.append(f'<p>{processed_line}</p>')
                html_parts.append('<ul class="timeline">')
            
            i += 1
        
        html_parts.append('</ul>')
        
        result = '\n'.join(html_parts)
        if self.debug:
            print(f"✅ Timeline processed with {self.timeline_counter} expandable items")
        return result            
    
class HtmlTemplate:
    """HTML Template manager with embedded CSS and JavaScript"""
    
    @staticmethod 
    def get_base_template() -> str:
        """Get the main HTML template structure"""
        return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tokyo Trip March 2026 - แผนการเดินทางโตเกียว</title>
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
        <span class="th">🏠</span>
        <span class="en">🏠</span>
    </a>
    <script>{JS_CONTENT}</script>
</body>
</html>'''

    @staticmethod
    def get_css() -> str:
        """Get comprehensive CSS styles"""
        return '''
        /* ===== CSS Variables ===== */
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
        }

        /* ===== Base Styles ===== */
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
            padding-top: 3rem;
        }

        /* ===== Language Switcher ===== */
        .lang-switcher {
            position: fixed; top: 1rem; right: 1rem; z-index: 1000;
            display: flex; gap: 0.5rem;
        }

        .lang-btn {
            padding: 0.5rem 1rem; border: 2px solid var(--primary-color);
            background: white; color: var(--primary-color);
            border-radius: 0.5rem; cursor: pointer; font-weight: bold;
            transition: all 0.3s ease;
        }

        .lang-btn.active, .lang-btn:hover {
            background: var(--primary-color); color: white;
        }

        /* ===== Language Display ===== */
        .lang-en .th, .lang-th .en { display: none; }
        .lang-th .th, .lang-en .en { display: inline; }
        .lang-en .en-block, .lang-th .th-block { display: block; }
        .lang-en .th-block, .lang-th .en-block { display: none; }

        /* ===== Layout ===== */
        .container { max-width: 1200px; margin: 0 auto; padding: 1rem; }

        header {
            text-align: center; margin-bottom: 3rem; padding: 2rem;
            background: linear-gradient(135deg, var(--primary-light), var(--primary-color));
            color: white; border-radius: 1rem; box-shadow: 0 4px 6px var(--shadow);
        }

        header h1 { font-size: 2rem; margin-bottom: 1rem; font-weight: 700; }
        header h2 { font-size: 1.2rem; margin-bottom: 1rem; opacity: 0.9; }
        header p { font-size: 1rem; opacity: 0.8; }

        /* ===== Sections ===== */
        section {
            margin-bottom: 3rem; padding: 2rem; background: var(--card-bg);
            border-radius: 1rem; box-shadow: 0 2px 4px var(--shadow);
        }

        section h1 {
            color: var(--primary-color); font-size: 1.8rem; margin-bottom: 1.5rem;
            border-bottom: 3px solid var(--primary-light); padding-bottom: 0.5rem;
        }

        /* ===== Timeline Styles ===== */
        .timeline {
            list-style: none; padding: 0; margin: 1.5rem 0; position: relative;
        }

        .timeline::before {
            content: ''; position: absolute; left: 1rem; top: 0; bottom: 0;
            width: 2px; background: var(--primary-color);
        }

        .timeline li {
            position: relative; padding: 1rem 0 1rem 3rem;
            border-bottom: 1px solid var(--border-color);
        }

        .timeline li::before {
            content: ''; position: absolute; left: 0.5rem; top: 1.5rem;
            width: 1rem; height: 1rem; background: var(--primary-color);
            border-radius: 50%; border: 3px solid white;
            box-shadow: 0 0 0 3px var(--primary-color);
        }

        .timeline-main { margin-bottom: 0.5rem; }

        .timeline-toggle {
            background: var(--primary-light); color: white; border: none;
            padding: 0.3rem 0.6rem; border-radius: 0.25rem; cursor: pointer;
            font-size: 0.9rem; margin: 0.5rem 0 0.25rem 0;
            transition: all 0.3s ease; display: inline-block;
            min-width: 1.8rem; text-align: center;
        }

        .timeline-toggle:hover { background: var(--primary-color); }
        .timeline-toggle.expanded { background: var(--success); }

        .timeline-detail {
            margin-top: 0.5rem; padding: 0.75rem;
            border-left: 2px solid var(--border-color);
            background: #e8e8e8;
            border-radius: 0.25rem; 
        }
        
        .timeline-detail p {
            font-size: 0.85rem;
            margin: 0.25rem 0;
            line-height: 1.4;
        }
        
        .timeline-detail li {
            font-size: 0.85rem;
            margin: 0.15rem 0;
        }
        
        .timeline-detail ul {
            margin: 0.3rem 0;
            padding-left: 1rem;
        }

        /* ===== Day Overview Cards ===== */
        .day-overviews {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem; margin: 2rem 0;
        }

        .day-overview {
            background: white; border: 1px solid var(--border-color);
            border-radius: 0.75rem; padding: 1.5rem; transition: all 0.3s ease;
            border-left: 4px solid var(--primary-color);
        }

        .day-overview:hover {
            transform: translateY(-2px); box-shadow: 0 4px 12px var(--shadow);
        }

        .day-overview h3 a { text-decoration: none; color: var(--primary-color); }

        .birthday-badge {
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white; padding: 0.5rem 1rem; border-radius: 2rem;
            font-size: 0.9rem; margin-left: 1rem; animation: sparkle 2s infinite;
        }

        @keyframes sparkle {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        /* ===== Tables ===== */
        .table-container { overflow-x: auto; margin: 1rem 0; }

        table {
            width: 100%; border-collapse: collapse; margin: 1rem 0;
            background: white; border-radius: 0.5rem; overflow: hidden;
            box-shadow: 0 2px 4px var(--shadow);
        }

        th, td {
            padding: 0.75rem 1rem; text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        th { background: #f1f5f9; font-weight: 600; color: var(--text-color); }
        tr:nth-child(even) { background: #f9fafb; }

        /* ===== Info Sections ===== */
        .info-section {
            margin: 1.5rem 0;
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 2px 4px var(--shadow);
        }
        
        .info-header {
            background: var(--card-bg);
            padding: 1rem 1.5rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background-color 0.3s ease;
        }
        
        .info-header:hover {
            background: var(--primary-light);
            color: white;
        }
        
        .info-header h3 {
            margin: 0;
            font-size: 1.1rem;
            color: var(--primary-color);
        }
        
        .info-header:hover h3 {
            color: white;
        }

        /* ===== Back to Top ===== */
        .back-to-top {
            position: fixed; bottom: 2rem; right: 2rem;
            background: var(--primary-color); color: white; padding: 1rem;
            border-radius: 50%; text-decoration: none;
            box-shadow: 0 4px 12px var(--shadow); transition: all 0.3s ease;
            z-index: 100;
        }

        .back-to-top:hover {
            background: var(--primary-dark); transform: translateY(-2px);
        }

        /* ===== Mobile Responsive ===== */
        @media (max-width: 768px) {
            .container { padding: 0.5rem; }
            header { padding: 1rem; }
            header h1 { font-size: 1.5rem; }
            section { padding: 1rem; }
            .day-overviews { grid-template-columns: 1fr; }
            .timeline li { padding-left: 2rem; }
            .timeline::before { left: 0.5rem; }
            .timeline li::before { left: 0.25rem; width: 0.5rem; height: 0.5rem; }
            .lang-switcher { top: 0.5rem; right: 0.5rem; }
            .back-to-top { bottom: 1rem; right: 1rem; padding: 0.75rem; }
        }
        '''
        
@staticmethod
def get_js() -> str:
    """Get JavaScript for timeline and language switching"""
    return '''
    // ===== Language Switching =====
    function switchLanguage(lang) {
        const body = document.body;
        const buttons = document.querySelectorAll('.lang-btn');
        
        // Remove all language classes
        body.classList.remove('lang-th', 'lang-en');
        body.classList.add(`lang-${lang}`);
        
        // Update button states
        buttons.forEach(btn => {
            btn.classList.remove('active');
            if (btn.id === `btn-${lang}`) {
                btn.classList.add('active');
            }
        });
        
        // Save to localStorage (with error handling)
        try {
            localStorage.setItem('tokyo-trip-lang', lang);
        } catch (e) {
            console.warn('LocalStorage not available:', e);
        }
    }
    
    // ===== Timeline Expand/Collapse =====
    function toggleTimelineDetail(elementId) {
        const detailElement = document.getElementById(elementId);
        const toggleButtons = document.querySelectorAll(`button[onclick*="${elementId}"]`);
        
        if (!detailElement) {
            console.error(`Element not found: ${elementId}`);
            return;
        }
        
        // Check current display state
        const currentDisplay = window.getComputedStyle(detailElement).display;
        const isHidden = currentDisplay === 'none';
        
        if (isHidden) {
            // Show the detail
            detailElement.style.display = 'block';
            toggleButtons.forEach(btn => {
                btn.classList.add('expanded');
                btn.innerHTML = '<span class="th">▼</span><span class="en">▼</span>';
            });
        } else {
            // Hide the detail
            detailElement.style.display = 'none';
            toggleButtons.forEach(btn => {
                btn.classList.remove('expanded');
                btn.innerHTML = '<span class="th">▶</span><span class="en">▶</span>';
            });
        }
    }
    
    // Make toggleTimelineDetail globally available
    window.toggleTimelineDetail = toggleTimelineDetail;
    
    // ===== Initialize Timeline Toggle =====
    function initializeTimelineToggle() {
        // Find all timeline detail elements and hide them initially
        const timelineDetails = document.querySelectorAll('.timeline-detail');
        timelineDetails.forEach(detail => {
            detail.style.display = 'none';
        });
    }
    
    // ===== Smooth Scrolling =====
    function initializeSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        links.forEach(link => {
            link.addEventListener('click', function(e) {
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
    
    // ===== Main Initialization =====
    document.addEventListener('DOMContentLoaded', function() {
        console.log('🇯🇵 Tokyo Trip 2026 - Initializing...');
        
        // Initialize language (with localStorage fallback)
        try {
            const savedLang = localStorage.getItem('tokyo-trip-lang');
            const defaultLang = (savedLang && (savedLang === 'th' || savedLang === 'en')) ? savedLang : 'th';
            switchLanguage(defaultLang);
        } catch (e) {
            console.warn('LocalStorage not available, using default language');
            switchLanguage('th');
        }
        
        // Initialize all features
        initializeTimelineToggle();
        initializeSmoothScrolling();
        
        console.log('✅ Tokyo Trip 2026 - All features initialized!');
    });
    '''            
    
class TripGenerator:
    """Main Tokyo Trip HTML Generator"""
    
    def __init__(self, config: TripConfig):
        self.config = config
        self.markdown_processor = MarkdownProcessor(debug=config.debug)
        self.template_manager = HtmlTemplate()
        
    def read_markdown_content(self) -> Dict[str, Dict[str, str]]:
        """Read all markdown files from content directories"""
        if self.config.debug:
            print("📂 Reading markdown content...")
            
        markdown_contents = {'th': {}, 'en': {}}
        
        if not self.config.content_dir.exists():
            print(f"⚠️ Warning: Content directory not found: {self.config.content_dir}")
            return markdown_contents
        
        # Read Thai content
        th_dir = self.config.content_dir / "th"
        if th_dir.exists():
            self._read_language_files(th_dir, 'th', markdown_contents['th'])
        else:
            # Fallback: read from content root
            self._read_language_files(self.config.content_dir, 'th', markdown_contents['th'])
        
        # Read English content
        en_dir = self.config.content_dir / "en"
        if en_dir.exists():
            self._read_language_files(en_dir, 'en', markdown_contents['en'])
            
        if self.config.debug:
            print(f"✅ Read {len(markdown_contents['th'])} Thai files")
            print(f"✅ Read {len(markdown_contents['en'])} English files")
            
        return markdown_contents
    
def _read_language_files(self, directory: Path, lang: str, content_dict: Dict[str, str]):
        """Read markdown files from a specific directory"""
        for md_file in sorted(directory.glob("*.md")):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    # Clean up section ID
                    section_id = re.sub(r'^\d+-?', '', md_file.stem)
                    section_id = section_id.replace('_', '-').replace(' ', '-').lower()
                    content_dict[section_id] = f.read()
                    
                    if self.config.debug:
                        print(f"  ✅ {lang}: {md_file.name} -> {section_id}")
            except Exception as e:
                print(f"❌ Error reading {md_file.name}: {e}")
    
def create_overview_section(self, markdown_contents: Dict[str, Dict[str, str]]) -> str:
    """Create overview section with day cards"""
    if self.config.debug:
        print("🏠 Creating overview section...")
        
    th_contents = markdown_contents['th']
    
    # Find day files and sort them
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
            # Extract title from markdown
            title_match = re.search(r'^#+\s*(.+?)(?:\n|$)', th_content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                main_title = re.split(r'\s*[-–|/]\s*', title)[0].strip()
                
                # Special birthday badge for day 4
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
                
                if self.config.debug:
                    print(f"  ✅ Added overview card: {main_title}")
        except Exception as e:
            if self.config.debug:
                print(f"  ❌ Error processing {section_id}: {e}")
            continue
    
    overview_html += '''
        </div>
    </section>
    '''
    
    if self.config.debug:
        print(f"✅ Overview section created with {len(day_files)} day cards")
        
    return overview_html

    
def process_content_sections(self, markdown_contents: Dict[str, Dict[str, str]]) -> str:
        """Process all content sections into HTML"""
        if self.config.debug:
            print("🚀 Processing content sections...")
            
        all_sections = []
        
        # Add overview section first
        all_sections.append(self.create_overview_section(markdown_contents))
        
        th_contents = markdown_contents['th']
        
        # Define section order
        section_order = ['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8', 
                        'accommodation', 'transportation', 'weather', 'budget', 'tips']
        
        for section_id in section_order:
            if section_id in th_contents:
                try:
                    th_content = th_contents[section_id]
                    
                    # Extract title
                    title_match = re.search(r'^#+\s*(.+?)(?:\n|$)', th_content, re.MULTILINE)
                    
                    if title_match:
                        title = title_match.group(1).strip()
                        body = re.sub(r'^#+\s*.+?(?:\n|$)', '', th_content, count=1, flags=re.MULTILINE).strip()
                        
                        # Special birthday badge for day 4
                        birthday_badge = ""
                        if section_id == "day4":
                            birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
                        
                        # Process content based on type
                        if section_id.startswith('day'):
                            html_body = self.markdown_processor.process_timeline_markdown(body)
                        elif section_id == 'accommodation':
                            # Process accommodation as timeline with hotel info
                            html_body = self._process_accommodation_as_timeline(body)
                        elif section_id in ['transportation', 'weather', 'tips']:
                            # Process as info sections with collapsible headers
                            html_body = self._process_info_section(body, section_id)
                        else:
                            # Use basic markdown for other sections
                            html_body = self.markdown_processor.basic_md_to_html(body)
                        
                        # Create section HTML
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
                        
                        if self.config.debug:
                            print(f"  ✅ Processed section: {section_id} ({len(html_body)} chars)")
                            
                except Exception as e:
                    if self.config.debug:
                        print(f"  ❌ Error processing {section_id}: {e}")
                    continue
        
        result = "\n".join(all_sections)
        if self.config.debug:
            print(f"✅ All sections processed: {len(result)} total characters")
            
        return result
    
def _process_accommodation_as_timeline(self, md_text: str) -> str:
    """Process accommodation content as timeline format"""
    if not md_text or not md_text.strip():
        return ""
    
    lines = md_text.strip().splitlines()
    html_parts = ['<ul class="timeline">']
    counter = 0
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for night/day patterns
        if re.match(r'.*(คืนที่|Night|Day).*', line) and ('**' in line or line.startswith('###')):
            # Extract title
            title = re.sub(r'[#*]', '', line).strip()
            
            # Collect details
            details = []
            j = i + 1
            while j < len(lines) and not re.match(r'.*(คืนที่|Night|Day).*', lines[j].strip()):
                if lines[j].strip() and not lines[j].startswith('##'):
                    details.append(lines[j].strip())
                j += 1
            
            # Create timeline item
            item_id = f"hotel-{counter}"
            html_parts.append('<li>')
            html_parts.append(f'<div class="timeline-main"><strong>🏨 {title}</strong></div>')
            
            if details:
                html_parts.append(f'''
                <button class="timeline-toggle" onclick="toggleTimelineDetail('{item_id}')">
                    <span class="th">▶</span>
                    <span class="en">▶</span>
                </button>
                <div class="timeline-detail" id="{item_id}" style="display: none;">''')
                
                for detail in details:
                    if detail.startswith('- '):
                        html_parts.append(f'<p>• {detail[2:]}</p>')
                    else:
                        html_parts.append(f'<p>{detail}</p>')
                
                html_parts.append('</div>')
            
            html_parts.append('</li>')
            counter += 1
            i = j - 1
        
        i += 1
    
    html_parts.append('</ul>')
    return '\n'.join(html_parts)

    
def _process_info_section(self, md_text: str, section_type: str) -> str:
        """Process transportation, weather, tips sections in a clean, organized way"""
        if not md_text or not md_text.strip():
            return ""
        
        lines = md_text.strip().splitlines()
        html_parts = []
        current_section = None
        section_counter = 0
        
        # Section icons
        section_icons = {
            'transportation': '🚆',
            'weather': '🌤️', 
            'tips': '💡'
        }
        
        base_icon = section_icons.get(section_type, '📝')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Major subsections (###)
            if line.startswith('### '):
                title = line[4:].strip()
                
                # Close previous section if exists
                if current_section:
                    html_parts.append('</div></div>')
                
                # Start new section
                section_id = f"{section_type}-{section_counter}"
                
                html_parts.append(f'''
                <div class="info-section">
                    <div class="info-header" onclick="toggleTimelineDetail('{section_id}')">
                        <h3>{base_icon} {title}</h3>
                        <button class="timeline-toggle" onclick="toggleTimelineDetail('{section_id}')">
                            <span class="th">▶</span>
                            <span class="en">▶</span>
                        </button>
                    </div>
                    <div class="timeline-detail" id="{section_id}" style="display: none;">''')
                
                current_section = section_id
                section_counter += 1
            
            # Content within sections
            elif line and current_section:
                if line.startswith('- '):
                    content = line[2:].strip()
                    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
                    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
                    html_parts.append(f'<p>• {content}</p>')
                elif line.startswith('**') and line.endswith('**'):
                    subheading = line[2:-2].strip()
                    html_parts.append(f'<h4>{subheading}</h4>')
                elif line.strip():
                    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
                    html_parts.append(f'<p>{content}</p>')
            
            # Content without section (add to general area)
            elif line and not current_section:
                if line.startswith('- '):
                    content = line[2:].strip()
                    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
                    html_parts.append(f'<p>• {content}</p>')
                elif not line.startswith('#'):
                    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
                    html_parts.append(f'<p>{content}</p>')
            
            i += 1
        
        # Close last section if exists
        if current_section:
            html_parts.append('</div></div>')
        
        return '\n'.join(html_parts)

def generate_html(self) -> str:
    """Generate complete HTML file"""
    if self.config.debug:
        print("🔍 Generating HTML...")
        
    # Read markdown content
    markdown_contents = self.read_markdown_content()
    
    # Process content sections
    content_sections = self.process_content_sections(markdown_contents)
    
    # Get template and insert content
    html_content = self.template_manager.get_base_template()
    html_content = html_content.replace('{CSS_CONTENT}', self.template_manager.get_css())
    html_content = html_content.replace('{JS_CONTENT}', self.template_manager.get_js())
    html_content = html_content.replace('{CONTENT_SECTIONS}', content_sections)
    
    if self.config.debug:
        print(f"✅ HTML generated: {len(html_content):,} characters")
        
    return html_content

def save_html_file(self, html_content: str) -> Path:
    """Save HTML content to file"""
    # Ensure build directory exists
    self.config.build_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"{self.config.base_name}-{self.config.version}-{timestamp}.html"
    output_path = self.config.build_dir / filename
    
    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    if self.config.debug:
        print(f"✅ HTML file saved: {output_path}")
        print(f"📄 File size: {len(html_content):,} characters ({output_path.stat().st_size:,} bytes)")
        
    return output_path


class EnhancedTripGenerator(TripGenerator):
    """Enhanced version with improved features and better organization"""
    
    def process_content_sections(self, markdown_contents: Dict[str, Dict[str, str]]) -> str:
        """Enhanced content processing with better formatting"""
        if self.config.debug:
            print("🎆 Processing content sections - ENHANCED VERSION...")
            
        all_sections = []
        all_sections.append(self.create_overview_section(markdown_contents))
        
        th_contents = markdown_contents['th']
        section_order = ['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8', 
                        'accommodation', 'transportation', 'weather', 'budget', 'tips']
        
        for section_id in section_order:
            if section_id in th_contents:
                try:
                    th_content = th_contents[section_id]
                    title_match = re.search(r'^#+\s*(.+?)(?:\n|$)', th_content, re.MULTILINE)
                    
                    if title_match:
                        title = title_match.group(1).strip()
                        body = re.sub(r'^#+\s*.+?(?:\n|$)', '', th_content, count=1, flags=re.MULTILINE).strip()
                        
                        # Birthday badge
                        birthday_badge = ""
                        if section_id == "day4":
                            birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
                        
                        # Enhanced processing based on section type
                        if section_id.startswith('day'):
                            html_body = self.markdown_processor.process_timeline_markdown(body)
                        elif section_id == 'accommodation':
                            html_body = self._process_accommodation_as_timeline(body)
                        elif section_id in ['transportation', 'weather', 'tips']:
                            html_body = self._process_info_section(body, section_id)
                        elif section_id == 'budget':
                            # Special handling for budget tables
                            html_body = self._process_budget_section(body)
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
                        
                        if self.config.debug:
                            print(f"  ✅ Enhanced: {section_id} ({len(html_body)} chars)")
                            
                except Exception as e:
                    if self.config.debug:
                        print(f"  ❌ Error: {section_id}: {e}")
                    continue
        
        result = "\n".join(all_sections)
        if self.config.debug:
            print(f"✅ ENHANCED processing complete: {len(result):,} chars")
            
        return result
    
    def _process_budget_section(self, md_text: str) -> str:
        """Process budget section with special table formatting"""
        if not md_text or not md_text.strip():
            return ""
        
        # Use basic markdown processor but ensure tables are styled properly
        html_content = self.markdown_processor.basic_md_to_html(md_text)
        
        # Add special styling for budget tables
        html_content = html_content.replace('<table>', '<table class="budget-table">')
        
        return html_content
    
    def get_enhanced_css(self) -> str:
        """Get enhanced CSS with additional styles"""
        base_css = self.template_manager.get_css()
        
        additional_css = '''
        
        /* ===== Budget Table Styles ===== */
        .budget-table {
            font-size: 0.95rem;
        }
        
        .budget-table th {
            background: var(--primary-light);
            color: white;
            font-weight: 600;
        }
        
        .budget-table tr:last-child {
            font-weight: bold;
            background: #f0f9ff;
            border-top: 2px solid var(--primary-color);
        }
        
        /* ===== Enhanced Info Headers ===== */
        .info-header .timeline-toggle {
            background: transparent;
            border: none;
            font-size: 1rem;
            padding: 0.25rem;
        }
        
        .info-header:hover .timeline-toggle {
            color: white;
        }
        
        /* ===== Better List Items ===== */
        .timeline-detail p {
            margin: 0.5rem 0;
            padding-left: 0.5rem;
        }
        
        .timeline-detail h4 {
            color: var(--primary-dark);
            margin: 1rem 0 0.5rem 0;
            font-size: 1rem;
            font-weight: 600;
        }
        '''
        
        return base_css + additional_css
    
    def generate_html(self) -> str:
        """Generate HTML with enhanced features"""
        if self.config.debug:
            print("🎆 Generating ENHANCED HTML...")
            
        markdown_contents = self.read_markdown_content()
        content_sections = self.process_content_sections(markdown_contents)
        
        # Use enhanced CSS
        html_content = self.template_manager.get_base_template()
        html_content = html_content.replace('{CSS_CONTENT}', self.get_enhanced_css())
        html_content = html_content.replace('{JS_CONTENT}', self.template_manager.get_js())
        html_content = html_content.replace('{CONTENT_SECTIONS}', content_sections)
        
        if self.config.debug:
            print(f"✅ ENHANCED HTML generated: {len(html_content):,} characters")
            
        return html_content
    
    
def get_section_icon(title: str, section_type: str) -> str:
    """Get appropriate icon for section based on title and type"""
    title_lower = title.lower()
    
    # Transportation icons
    if section_type == "transportation":
        if any(word in title_lower for word in ['รถไฟ', 'train', 'jr', 'shinkansen']):
            return '🚄'
        elif any(word in title_lower for word in ['รถเมล์', 'metro', 'subway']):
            return '🚇'
        elif any(word in title_lower for word in ['รถบัส', 'bus']):
            return '🚌'
        elif any(word in title_lower for word in ['แท็กซี', 'taxi']):
            return '🚕'
        elif any(word in title_lower for word in ['บัตร', 'card', 'ic']):
            return '🎫'
        else:
            return '🚆'
    
    # Weather icons
    elif section_type == "weather":
        if any(word in title_lower for word in ['อุณหภูมิ', 'temperature']):
            return '🌡️'
        elif any(word in title_lower for word in ['ฝน', 'rain']):
            return '🌧️'
        elif any(word in title_lower for word in ['หิมะ', 'snow']):
            return '❄️'
        elif any(word in title_lower for word in ['เสื้อผ้า', 'clothes']):
            return '👕'
        else:
            return '🌤️'
    
    # Tips icons
    elif section_type == "tips":
        if any(word in title_lower for word in ['ภาษา', 'language']):
            return '🗣️'
        elif any(word in title_lower for word in ['เงิน', 'money', 'payment']):
            return '💳'
        elif any(word in title_lower for word in ['อาหาร', 'food']):
            return '🍱'
        elif any(word in title_lower for word in ['วัฒนธรรม', 'culture']):
            return '🏯'
        elif any(word in title_lower for word in ['ฉุกเฉิน', 'emergency']):
            return '🆘'
        elif any(word in title_lower for word in ['ความปลอดภัย', 'safety']):
            return '🛡️'
        else:
            return '💡'
    
    # Default icons
    else:
        return '📝'
    
def main():
    """Main execution function"""
    print("🇯🇵 Tokyo Trip 2026 HTML Generator - FINAL VERSION")
    print("=" * 60)
    print("✨ Features: Timeline expand/collapse, Multi-language, Responsive, Offline-ready")
    print("")
    
    # Setup configuration
    script_dir = Path(__file__).parent
    config = TripConfig(
        script_dir=script_dir,
        content_dir=script_dir.parent / "content",
        build_dir=script_dir.parent / "build",
        debug=True
    )
    
    # Create ENHANCED generator
    generator = EnhancedTripGenerator(config)
    
    try:
        print(f"📁 Content directory: {config.content_dir}")
        print(f"📁 Build directory: {config.build_dir}")
        print("")
        
        # Generate HTML
        html_content = generator.generate_html()
        output_path = generator.save_html_file(html_content)
        
        print("")
        print("🎉 Generation completed successfully! - ENHANCED VERSION")
        print(f"📄 Output file: {output_path}")
        print(f"📈 File size: {len(html_content):,} characters")
        print("")
        print("💯 Features included:")
        print("   ✅ Timeline expand/collapse functionality")
        print("   ✅ Clean organized sections")
        print("   ✅ Multi-language support (TH/EN)")
        print("   ✅ Mobile responsive design")
        print("   ✅ Birthday special effects 🎂")
        print("   ✅ Smooth scrolling navigation")
        print("   ✅ Offline-ready HTML output")
        print("")
        print("🚀 Ready for Tokyo Trip 2026!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())                    