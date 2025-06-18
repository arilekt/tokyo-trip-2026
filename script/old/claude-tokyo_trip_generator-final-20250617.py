import os
import re
import sys
import json
import mistune
import datetime
from pathlib import Path
from bs4 import BeautifulSoup

# --- Configuration and Paths ---
# กำหนด Base Directory ของโปรเจกต์
# สมมติว่า script นี้จะอยู่ใน tokyo-trip-2026/script/
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
# แก้ไขตรงนี้ให้ชี้ไปที่ folder 'templates'
TEMPLATE_PATH = SCRIPT_DIR / "templates" / "template-skeleton.html" # แก้ไขแล้วนะพี่!
CONTENT_DIR = BASE_DIR / "content"
BUILD_DIR = BASE_DIR / "build"

# Ensure build directory exists
BUILD_DIR.mkdir(parents=True, exist_ok=True)

# --- Inline CSS (from ultimate_fixer.py's get_fixed_css) ---
# นี่คือ CSS ที่น้องดึงมาจาก ultimate_fixer.py ของพี่เลยนะ
INLINE_CSS = """
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

        /* Language switcher */
        .lang-switcher, .language-switcher {
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
            display: flex;
            gap: 0.5rem;
        }

        .lang-btn, .language-switcher button {
            padding: 0.5rem 1rem;
            border: 2px solid var(--primary-color);
            background: white;
            color: var(--primary-color);
            border-radius: 0.5rem;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .lang-btn.active, .language-switcher button.active,
        .lang-btn:hover, .language-switcher button:hover {
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

        /* Timeline styles */
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

        /* Info/Note boxes - THE MAGIC THAT MAKES IT WORK */
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
            user-select: none;
            transition: background-color 0.3s ease;
        }

        .info-toggle:hover, .note-toggle:hover {
            background-color: rgba(255, 255, 255, 0.5);
            border-radius: 0.25rem;
            padding: 0.25rem;
            margin: -0.25rem;
        }

        .info-toggle::after, .note-toggle::after {
            content: "▼";
            transition: transform 0.3s ease;
            font-size: 0.8em;
        }

        .info-toggle.collapsed::after, .note-toggle.collapsed::after {
            transform: rotate(-90deg);
        }

        .info-detail, .note-detail {
            overflow: hidden;
            transition: max-height 0.4s ease-out, margin-top 0.4s ease-out;
            max-height: 3000px; /* Large enough to show content by default for print/no-js fallback */
            margin-top: 0.5rem;
        }

        .info-detail.collapsed, .note-detail.collapsed {
            max-height: 0;
            margin-top: 0;
        }
        
        /* Specific styles for timeline details to make them collapsible */
        .timeline-toggle-button { /* Renamed from .timeline-toggle to avoid conflict with .info-toggle etc. */
            background: var(--primary-color);
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
        .timeline-toggle-button.expanded {
            background: var(--primary-dark);
        }
        .timeline-detail-content { /* Renamed from .timeline-detail to avoid conflict with .info-detail etc. */
            margin-top: 0.5rem;
            padding: 0.75rem;
            border-left: 2px solid var(--border-color);
            background: rgba(255, 255, 255, 0.7);
            border-radius: 0.25rem;
            overflow: hidden;
            transition: max-height 0.4s ease-out, opacity 0.4s ease-out;
            max-height: 0; /* Initially collapsed */
            opacity: 0;   /* Initially hidden with opacity */
        }
        /* Ensure nested lists inside details have correct padding */
        .info-detail ul, .info-detail ol,
        .note-detail ul, .note-detail ol,
        .timeline-detail-content ul, .timeline-detail-content ol { /* Added timeline-detail-content */
            padding-left: 1.5rem;
        }


        /* Tables */
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
        }

        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--table-border);
            vertical-align: top;
        }

        th {
            background: var(--table-header);
            font-weight: 600;
            color: var(--text-color);
        }

        tr:nth-child(even) {
            background: var(--table-alt);
        }

        /* Day overview cards */
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

        .day-overview h3 a {
            text-decoration: none;
            color: var(--primary-color);
        }
        
        /* Birthday badge */
        .birthday-badge {
            display: inline-block;
            background-color: var(--primary-color);
            color: white;
            font-weight: bold;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            margin-left: 1rem;
            font-size: 0.9rem;
            vertical-align: middle;
            animation: pulse 2s infinite ease-in-out;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.08); }
            100% { transform: scale(1); }
        }

        /* Back to top */
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
            opacity: 0; /* Hidden by default */
            pointer-events: none; /* Disable clicks when hidden */
        }

        .back-to-top:hover {
            background: var(--primary-dark);
            transform: translateY(-2px);
        }
        /* Mobile responsive */
        @media (max-width: 768px) {
            .container { padding: 0.5rem; }
            header { padding: 1rem; }
            header h1 { font-size: 1.5rem; }
            section { padding: 1rem; }
            .day-overviews { grid-template-columns: 1fr; }
            .lang-switcher, .language-switcher { top: 0.5rem; right: 0.5rem; }
            .back-to-top { bottom: 1rem; right: 1rem; padding: 0.75rem; }
        }
""" #

# --- Inline JavaScript (from ultimate_fixer.py's get_fixed_js) ---
# นี่คือ JavaScript ที่น้องดึงมาจาก ultimate_fixer.py ของพี่เลยนะ
INLINE_JS = """
        // Language switching
        function switchLanguage(lang) {
            const body = document.body;
            const buttons = document.querySelectorAll('.lang-btn, .language-switcher button');
            
            body.classList.remove('lang-th', 'lang-en');
            body.classList.add(`lang-${lang}`);
            
            buttons.forEach(btn => {
                btn.classList.remove('active');
                if (btn.getAttribute('data-lang') === lang || btn.id === `btn-${lang}`) {
                    btn.classList.add('active');
                }
            });
            
            try {
                localStorage.setItem('tokyo-trip-lang', lang);
            } catch (e) {}
            
            // console.log(`Language switched to: ${lang}`); // Re-enabled for debugging
        }

        // THE MAGIC FUNCTION THAT MAKES EXPAND/COLLAPSE WORK (for .info-box and .note-box)
        function initializeCollapsibleBoxes() {
            // console.log('🔧 Initializing collapsible boxes...'); // Re-enabled for debugging
            
            const toggles = document.querySelectorAll('.info-toggle, .note-toggle');
            // console.log(`Found ${toggles.length} toggle elements`); // Re-enabled for debugging
            
            toggles.forEach((toggle, index) => {
                // Ensure no duplicate event listeners if called multiple times
                const newToggle = toggle.cloneNode(true);
                toggle.parentNode.replaceChild(newToggle, toggle);
                toggle = newToggle; // Update reference
                
                const detail = toggle.nextElementSibling;
                
                if (detail && (detail.classList.contains('info-detail') || detail.classList.contains('note-detail'))) {
                    // Start collapsed by default (CSS handles initial state if .collapsed class is present)
                    toggle.classList.add('collapsed');
                    detail.classList.add('collapsed');
                    
                    // console.log(`Setting up toggle ${index + 1}`); // Re-enabled for debugging
                    
                    toggle.addEventListener('click', function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        // console.log(`Toggle clicked: ${detail.classList.contains('collapsed') ? 'expanding' : 'collapsing'}`); // Re-enabled for debugging
                        
                        toggle.classList.toggle('collapsed');
                        detail.classList.toggle('collapsed');
                    });
                } else {
                    // console.warn(`No matching detail element for toggle ${index + 1}`); // Re-enabled for debugging
                }
            });
            
            // console.log('✅ Collapsible boxes initialized!'); // Re-enabled for debugging
        }

        // THE MAGIC FUNCTION FOR TIMELINE DETAILS EXPAND/COLLAPSE
        function toggleTimelineDetail(detailId) {
            const detail = document.getElementById(detailId);
            const button = document.querySelector(`[onclick="toggleTimelineDetail('${detailId}')"]`);
            
            if (!detail || !button) {
                // console.warn(`Timeline detail not found: ${detailId}`); // Re-enabled for debugging
                return;
            }
            
            // Check if it's currently hidden by max-height 0 and opacity 0
            const isHidden = detail.style.maxHeight === '0px' || detail.style.maxHeight === '' || detail.style.opacity === '0';
            
            if (isHidden) {
                detail.style.display = 'block'; // Make sure it's block for scrollHeight calculation
                detail.style.maxHeight = detail.scrollHeight + "px"; // Set maxHeight to fit content
                detail.style.opacity = "1"; // Fade in
                button.classList.add('expanded');
                button.querySelectorAll('span.th, span.en').forEach(span => {
                    span.textContent = span.textContent.replace('▼', '▲');
                });
                // console.log(`Timeline detail expanded: ${detailId}`); // Re-enabled for debugging
            } else {
                detail.style.maxHeight = "0"; // Collapse
                detail.style.opacity = "0"; // Fade out
                // console.log(`Timeline detail collapsed: ${detailId}`); // Re-enabled for debugging
                // No need to set display: 'none' immediately. CSS transition handles the visual part.
                button.classList.remove('expanded');
                button.querySelectorAll('span.th, span.en').forEach(span => {
                    span.textContent = span.textContent.replace('▲', '▼');
                });
            }
        }
        
        // Make toggleTimelineDetail globally available
        window.toggleTimelineDetail = toggleTimelineDetail;
        
        // Initialize timeline functionality
        function initializeTimelineToggle() {
            // console.log('🔧 Initializing timeline toggle...'); // Re-enabled for debugging
            
            // Find all timeline detail elements and hide them initially using max-height/opacity
            const timelineDetails = document.querySelectorAll('.timeline-detail-content'); // Use the new class name
            timelineDetails.forEach(detail => {
                detail.style.maxHeight = '0px';
                detail.style.opacity = '0';
                detail.style.display = 'none'; // Ensure it's hidden from layout initially
            });
            
            // console.log(`✅ Timeline toggle initialized for ${timelineDetails.length} details`); // Re-enabled for debugging
        }

        // Smooth scrolling
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

        // Back to top button
        function initializeBackToTop() {
            const backToTop = document.querySelector('.back-to-top');
            if (backToTop) {
                window.addEventListener('scroll', function() {
                    if (window.pageYOffset > 300) {
                        backToTop.style.opacity = '1';
                        backToTop.style.pointerEvents = 'auto';
                    } else {
                        backToTop.style.opacity = '0'; // Change to 0 for full fade out
                        backToTop.style.pointerEvents = 'none';
                    }
                });
            }
        }

        // Currency conversion
        function updateCurrencyDisplay() {
            const jpyToThbRate = 0.2346; // Use the rate from context_summary
            const yenElements = document.querySelectorAll('[data-jpy]'); // Use data-jpy from context_summary
            
            yenElements.forEach(element => {
                const jpyString = element.dataset.jpy.replace(/,/g, ''); // Remove commas
                const jpyAmount = parseFloat(jpyString);
                if (!isNaN(jpyAmount)) {
                    const thbAmount = Math.round(jpyAmount * jpyToThbRate);
                    // Check if there's already a .thb-amount span
                    let thbSpan = element.querySelector('.thb-amount');
                    if (!thbSpan) {
                         // If no span, create one and append. Ensure existing content is preserved.
                        const originalContent = element.innerHTML;
                        thbSpan = document.createElement('span');
                        thbSpan.className = 'thb-amount';
                        element.innerHTML = `${originalContent} <span class="thb-amount">(${thbAmount.toLocaleString('en-US', {minimumFractionDigits: 0, maximumFractionDigits: 0})}฿)</span>`;
                    } else {
                        // Update existing span
                        thbSpan.textContent = `(${thbAmount.toLocaleString('en-US', {minimumFractionDigits: 0, maximumFractionDigits: 0})}฿)`;
                    }
                }
            });

            // Update exchange rate info message
            const rateDisplay = document.getElementById('exchange-rate-info');
            if(rateDisplay) {
                const rateTextTh = `อัตราแลกเปลี่ยน: 100 เยน ≈ ${ (jpyToThbRate * 100).toFixed(2) } บาท (ตรวจสอบอัตราปัจจุบัน)`;
                const rateTextEn = `Exchange Rate: 100 Yen ≈ ${ (jpyToThbRate * 100).toFixed(2) } Baht (Check current rates)`;
                rateDisplay.querySelector('.th').textContent = rateTextTh;
                rateDisplay.querySelector('.en').textContent = rateTextEn;
            }
        }

        // Main initialization
        document.addEventListener('DOMContentLoaded', function() {
            // console.log('🇯🇵 Tokyo Trip 2026 Final Generator - Loading...'); // Re-enabled for debugging
            
            // Language setup
            try {
                const savedLang = localStorage.getItem('tokyo-trip-lang');
                if (savedLang && (savedLang === 'th' || savedLang === 'en')) {
                    switchLanguage(savedLang);
                } else {
                    switchLanguage('th'); // Default to Thai
                }
            } catch (e) {
                switchLanguage('th'); // Fallback if localStorage fails
            }
            
            // Setup language switcher buttons
            document.querySelectorAll('[data-lang]').forEach(btn => {
                btn.addEventListener('click', function() {
                    switchLanguage(this.getAttribute('data-lang'));
                });
            });
            
            // Initialize all features
            initializeCollapsibleBoxes(); // For info-box/note-box
            initializeTimelineToggle(); // For timeline details
            initializeSmoothScrolling();
            initializeBackToTop();
            updateCurrencyDisplay(); // For JPY to THB conversion
            
            // console.log('✅ Tokyo Trip 2026 Final Generator - READY WITH WORKING EXPAND/COLLAPSE!'); // Re-enabled for debugging
        });
""" #

# --- Helper Functions ---
def read_file_content(filepath):
    """Reads content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def process_markdown_to_html_section(section_title, section_content, section_id=None):
    """
    Processes a single markdown section into HTML, including handling
    of timeline details and info/note boxes with proper expand/collapse structure.
    """
    if not section_id:
        section_id = re.sub(r'[^\w\-]', '', section_title.lower().replace(' ', '-'), flags=re.UNICODE)
    
    section_html_parts = [f'<section id="{section_id}">\n']
    
    # Add section title (with multi-language support)
    if section_title:
        day_match = re.match(r'วันที่\s+(\d+):\s+([^\n]+)', section_title)
        if day_match:
            day_num = day_match.group(1)
            full_title = day_match.group(2).strip()
            
            thai_date_part = full_title
            english_date_part = ""

            if " - " in full_title:
                parts = full_title.split(" - ", 1)
                thai_date_part = parts[0].strip()
                english_date_part = parts[1].strip()
            
            birthday_badge = ""
            if day_num == "4":
                birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
            
            section_html_parts.append(f'<h1>\n')
            section_html_parts.append(f'<span class="th th-block">วันที่ {day_num}: {thai_date_part}</span>\n')
            section_html_parts.append(f'<span class="en en-block">Day {day_num}: {english_date_part if english_date_part else thai_date_part}</span>\n')
            section_html_parts.append(f'{birthday_badge}\n')
            section_html_parts.append(f'</h1>\n')
        else:
            section_html_parts.append(f'<h1>\n')
            if " / " in section_title:
                thai, english = section_title.split(" / ", 1)
                section_html_parts.append(f'<span class="th th-block">{thai.strip()}</span>\n')
                section_html_parts.append(f'<span class="en en-block">{english.strip()}</span>\n')
            else:
                section_html_parts.append(f'<span class="th th-block">{section_title.strip()}</span>\n')
                section_html_parts.append(f'<span class="en en-block">{section_title.strip()}</span>\n')
            section_html_parts.append(f'</h1>\n')
    
    # Process main content markdown to initial HTML
    initial_html_content = mistune.html(section_content)
    
    # --- Special Handling for Timeline Sections ---
    # This checks for bullet points starting with -** and potential nested ####
    if section_id.startswith('day') and ('-**' in section_content or '####' in section_content):
        timeline_list_html_parts = ['<ul class="timeline">\n']
        
        # Split content by main timeline items (lines starting with -**)
        # This regex attempts to capture a time, optional emoji, and the rest of the content for the item
        timeline_item_pattern = re.compile(r'^- \*\*(.+?)\*\*:\s*(<span class="emoji">[^<]+</span>\s*)?(.*?)(?=\n^- |\Z)', re.DOTALL | re.MULTILINE)
        
        unique_id_counter = 0 # Counter for unique detail IDs
        
        for match in timeline_item_pattern.finditer(section_content):
            time_str = match.group(1).strip()
            emoji_span = match.group(2) if match.group(2) else ''
            item_content_md = match.group(3).strip() # Full markdown content for this item

            timeline_list_html_parts.append(f'<li>\n<strong>{time_str}</strong>: {emoji_span}')

            # Process `item_content_md` for `####` sub-sections (info-boxes within timeline)
            sub_items_pattern = re.compile(r'^(####\s+([^\n]+)\s*\r?\n)(.+?)(?=\n####|\Z)', re.DOTALL | re.MULTILINE)
            sub_item_matches = list(sub_items_pattern.finditer(item_content_md))
            
            if sub_item_matches:
                # Content before the first sub-item (if any)
                initial_text_md = item_content_md[:sub_item_matches[0].start()].strip()
                if initial_text_md:
                    timeline_list_html_parts.append(mistune.html(initial_text_md))
                
                for sub_match in sub_item_matches:
                    sub_title_md = sub_match.group(2).strip()
                    sub_content_md = sub_match.group(3).strip()
                    
                    unique_id_counter += 1
                    detail_id = f'{section_id}-detail-{unique_id_counter}'
                    
                    timeline_list_html_parts.append(f'<div class="info-box">\n')
                    # Use .timeline-toggle-button for timeline specific toggles
                    timeline_list_html_parts.append(f'<button class="timeline-toggle-button" onclick="toggleTimelineDetail(\'{detail_id}\')">\n')
                    timeline_list_html_parts.append(f'<span class="th">ℹ️ {sub_title_md} ▼</span><span class="en">ℹ️ {sub_title_md} ▼</span>\n')
                    timeline_list_html_parts.append(f'</button>\n')
                    # Use .timeline-detail-content for timeline specific detail containers
                    timeline_list_html_parts.append(f'<div class="timeline-detail-content" id="{detail_id}">\n')
                    timeline_list_html_parts.append(mistune.html(sub_content_md))
                    timeline_list_html_parts.append(f'</div>\n')
                    timeline_list_html_parts.append(f'</div>\n')
            else:
                # No sub-items, just convert the entire item_content_md as regular markdown
                timeline_list_html_parts.append(mistune.html(item_content_md))
            
            timeline_list_html_parts.append(f'</li>\n')
        
        timeline_list_html_parts.append('</ul>\n')
        initial_html_content = "".join(timeline_list_html_parts)
    
    # Process tables (must be done after mistune.html to find <table> tags)
    soup_content = BeautifulSoup(initial_html_content, 'html.parser')
    tables = soup_content.find_all('table')
    
    for table in tables:
        table_container = soup_content.new_tag('div', attrs={'class': 'table-container'})
        table.wrap(table_container)
        
        for row in table.find_all('tr'):
            cells = row.find_all(['td', 'th'])
            if cells and len(cells) > 0:
                first_cell_text = cells[0].get_text().strip().lower()
                if 'รวม' in first_cell_text or 'total' in first_cell_text:
                    row['class'] = row.get('class', []) + ['total']
                elif 'งบประมาณที่เหลือ' in first_cell_text or 'remaining' in first_cell_text:
                    row['class'] = row.get('class', []) + ['remaining']
    
    final_section_content_html = str(soup_content)
    
    section_html_parts.append(final_section_content_html)
    section_html_parts.append('</section>\n')
    
    return "".join(section_html_parts)

def create_day_overview_cards_html(markdown_text_full):
    """
    Extracts day summaries and budget overview from the main markdown text
    to create the overview cards section.
    """
    overview_section_match = re.search(r'##\s+ภาพรวมการเดินทางและกิจกรรม\s*\r?\n(.+?)(?=\r?\n##\s+|\Z)', markdown_text_full, re.DOTALL)
    
    if not overview_section_match:
        print("Warning: 'ภาพรวมการเดินทางและกิจกรรม' section not found for overview cards.")
        return ""

    overview_content = overview_section_match.group(1)
    
    # Pattern to extract day summaries: ### วันที่ X: หัวข้อ (ไทย) - หัวข้อ (อังกฤษ) \n เนื้อหา
    day_summary_pattern = re.compile(
        r'###\s+วันที่\s+(\d+):\s+([^\n]+)\s*\r?\n([^\n]+)', 
        re.MULTILINE
    )
    day_summaries = day_summary_pattern.findall(overview_content)
    
    html_cards = ['<div class="day-overviews">\n']
    
    for day_num, title_combo, description_combo in day_summaries:
        title_th, title_en = title_combo.split(' - ', 1) if ' - ' in title_combo else (title_combo, title_combo)
        description_th = description_combo.strip()
        description_en = description_combo.strip() 
        
        html_cards.append(f'<div class="day-overview">\n')
        html_cards.append(f'<h3><a href="#day{day_num}"><span class="th">{title_th}</span><span class="en">{title_en}</span></a></h3>\n')
        html_cards.append(f'<p><span class="th">{description_th}</span><span class="en">{description_en}</span></p>\n')
        html_cards.append(f'</div>\n')
    
    # Add budget overview card
    budget_overview_title_th = "ประมาณการค่าใช้จ่ายและสถานะ"
    budget_overview_title_en = "Budget Estimate and Status"
    budget_overview_desc_th = "ข้อมูลการจอง และประมาณการค่าใช้จ่าย."
    budget_overview_desc_en = "Booking information and estimated expenses."

    html_cards.append(f'''
    <div class="day-overview">
    <h3><a href="#budget"><span class="th">{budget_overview_title_th}</span><span class="en">{budget_overview_title_en}</span></a></h3>
    <p><span class="th">{budget_overview_desc_th}</span><span class="en">{budget_overview_desc_en}</span></p>
    </div>
    ''')
    
    html_cards.append('</div> \n')
    
    # Add the "How to Use" note box as part of the overview section
    usage_info_box = '''
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
    '''
    html_cards.append(usage_info_box)

    return "".join(html_cards)


def generate_trip_guide_html():
    """Main function to generate the complete HTML trip guide."""
    print(f"Starting HTML generation for Tokyo Trip 2026 at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. Read the main template skeleton
    template_html = read_file_content(TEMPLATE_PATH)
    if template_html is None:
        print("Failed to read template skeleton. Exiting.")
        return

    soup = BeautifulSoup(template_html, "html.parser")

    # 2. Inject CSS directly into <head>
    style_tag = soup.find('style') # Find existing style tag
    if style_tag:
        style_tag.string = INLINE_CSS
    else: # If no style tag found, create one
        style_tag = soup.new_tag("style")
        style_tag.string = INLINE_CSS
        soup.head.append(style_tag)
    print("Injected inline CSS.")

    # 3. Inject JavaScript directly into <head> (or before </body> as per template)
    script_tag = soup.find('script')
    if script_tag:
        script_tag.string = INLINE_JS
    else: 
        script_tag = soup.new_tag("script")
        script_tag.string = INLINE_JS
        soup.body.append(script_tag) 
    print("Injected inline JavaScript.")

    # 4. Read all markdown content files
    markdown_contents = {}
    ordered_md_files_to_process = [
        "main_info.md",
        "overview.md",
        "weather_info.md",
        "day1.md", "day2.md", "day3.md", "day4.md", "day5.md", "day6.md", "day7.md", "day8.md",
        "budget.md",
        "accommodation.md",
        "food_recommendations.md",
        "shopping_guide.md",
        "transportation_budget.md",
        "important_updates.md",
        "timeline.md", # This one will be parsed for hotel timeline, might be integrated into a section later
        "tokyo-trip-update.md" # This is the master file, read it first
    ]

    full_markdown_master_content = ""
    for md_file_name in ordered_md_files_to_process:
        md_path = CONTENT_DIR / md_file_name
        if md_path.exists():
            content = read_file_content(md_path)
            if content is not None:
                markdown_contents[md_file_name] = content
                if md_file_name == "tokyo-trip-update.md":
                    full_markdown_master_content = content
        else:
            print(f"Warning: Markdown file '{md_file_name}' not found. Skipping.")

    if not full_markdown_master_content:
        print("Error: 'tokyo-trip-update.md' (master content file) not found or empty. Cannot proceed.")
        return

    # Extract overall title and intro from main_info.md if it exists, otherwise from tokyo-trip-update.md
    overall_title_th = "เที่ยวญี่ปุ่น Porjai: Birthday Trip 2026"
    overall_title_en = "Porjai's Japan Trip: Birthday Adventure 2026"
    
    main_info_content = markdown_contents.get("main_info.md", "")
    title_match = re.search(r'#\s+([^\n]+)', main_info_content)
    if title_match:
        # Assuming main title in main_info.md is only TH or first part is TH
        overall_title_th = title_match.group(1).strip()
        # English title is usually separated by " / " in the main title or taken from static JS
        # For now, keep the static EN title from JS if no explicit EN title in MD
    
    # Update <title> tag in HTML
    if soup.title:
        soup.title.string = overall_title_th # Initial page title in TH
    else:
        new_title_tag = soup.new_tag("title")
        new_title_tag.string = overall_title_th
        soup.head.append(new_title_tag)

    # Populate Header (h1, h2) from tokyo-trip-update.md's main title and date
    header_h1 = soup.find('h1', id='toc')
    if header_h1:
        # Update h1 with proper TH/EN spans
        header_h1.find('span', class_='th').string = overall_title_th
        header_h1.find('span', class_='en').string = overall_title_en # Use static EN title

    header_h2 = soup.find('header').find('h2')
    if header_h2:
        date_match = re.search(r'📅\s+([^\n]+)', full_markdown_master_content)
        if date_match:
            date_text = date_match.group(1).strip()
            date_th = date_text
            date_en = date_text
            if " – " in date_text: # Using " – " (en dash) as separator
                parts = date_text.split(" – ", 1)
                date_th = parts[0].strip()
                date_en = parts[1].strip() # Take the rest as EN
            
            header_h2.find('span', class_='th').string = f"📅 {date_th}"
            header_h2.find('span', class_='en').string = f"📅 {date_en}"

    # Extract general info like travelers and itinerary
    travel_info_match = re.search(r'✈️\s+ผู้เดินทาง:\s+([^\n]+)\s*\r?\n🗺️\s+เส้นทาง:\s+([^\n]+)', full_markdown_master_content)
    if travel_info_match:
        travelers_th = travel_info_match.group(1).strip()
        itinerary_th = travel_info_match.group(2).strip()

        # Hardcode English versions based on context summary, as they are not explicitly paired in MD yet
        travelers_en = "Travelers: 🧍 Arilek (Dad) 👧 Nuntnaphat (Porjai)"
        itinerary_en = "Itinerary: Narita – Tokyo – Kawaguchiko – Gala Yuzawa – Tokyo"
        
        general_info_p = soup.find('div', class_='container').find('p')
        if general_info_p:
            general_info_p.clear() # Clear existing content
            general_info_p.append(BeautifulSoup(f'<span class="th">{travelers_th}</span><span class="en">{travelers_en}</span><br/>\n<span class="th">{itinerary_th}</span><span class="en">{itinerary_en}</span>', 'html.parser'))
    
    print("Updated header and general info.")

    # 5. Process sections and insert into the main container
    sections_in_master_md = re.findall(r'##\s+([^\n]+)\s*\r?\n(.+?)(?=(?:\r?\n##\s+|$))', full_markdown_master_content, re.DOTALL)
    
    processed_sections_html_parts = {}

    # Pre-process "Overview" to generate the cards and usage note box
    # This must be done from the full master content as it relies on summary parts.
    overview_section_html = create_day_overview_cards_html(full_markdown_master_content)
    # The overview section title is already part of the template's <section id="overview">
    # So we just need to place the generated cards + usage box inside it.
    processed_sections_html_parts['overview'] = f'<section id="overview">\n<h1><span class="th th-block">ภาพรวมการเดินทางและกิจกรรม</span><span class="en en-block">Trip Overview &amp; Activities</span></h1>\n{overview_section_html}\n</section>\n'
    print("Processed 'overview' section from master content.")

    # Process other dynamic sections from individual MD files based on their filename
    # Note: sections_in_master_md only captures sections from tokyo-trip-update.md
    # We should also process other individual markdown files that are not part of tokyo-trip-update.md's ## structure
    
    # List all content MDs (excluding tokyo-trip-update.md and overview.md as they are special)
    all_content_md_files = [f.name for f in CONTENT_DIR.glob("*.md") if f.name not in ["tokyo-trip-update.md", "overview.md"]]

    for md_file_name in all_content_md_files:
        section_md_content = markdown_contents.get(md_file_name)
        if section_md_content is None:
            continue

        # Extract actual title from the markdown content (first H1 or H2)
        # Assuming each content/*.md file starts with a single H1 or H2 that defines its title
        title_from_file_match = re.match(r'#+\s+([^\n]+)', section_md_content)
        if not title_from_file_match:
            print(f"Warning: No main title found in {md_file_name}. Skipping section processing.")
            continue
        
        section_title_from_file = title_from_file_match.group(1).strip()
        section_id_from_file = Path(md_file_name).stem # Use filename (without .md) as ID
        
        # Special handling for hotel timeline, which might need to be parsed from 'timeline.md'
        if md_file_name == "timeline.md":
            # The timeline.md content is a bit different, it has ## headers for each date
            # We'll treat it as a single 'hotel-timeline' section for now.
            processed_section_html = process_markdown_to_html_section(
                section_title_from_file, # "ไทม์ไลน์การเดินทาง - เที่ยวญี่ปุ่น Porjai 2026"
                section_md_content, # Pass the whole content to process
                "hotel-timeline" # Assign specific ID
            )
            processed_sections_html_parts["hotel-timeline"] = processed_section_html
        elif md_file_name == "budget.md":
            processed_section_html = process_markdown_to_html_section(
                section_title_from_file, 
                section_md_content, 
                "budget"
            )
            # Inject the dynamic currency rate info placeholder within the budget section
            budget_soup = BeautifulSoup(processed_section_html, 'html.parser')
            # Find the paragraph where exchange rate info should be
            # It's better to find a specific tag with text or pattern
            p_to_replace = budget_soup.find('p', string=lambda text: text and 'อัตราแลกเปลี่ยน' in text)
            if p_to_replace:
                # Replace with the id="exchange-rate-info" element
                new_p = budget_soup.new_tag('p', id='exchange-rate-info')
                new_p.append(BeautifulSoup('<span class="emoji">💰</span>\n<span class="th"></span><span class="en"></span>', 'html.parser'))
                p_to_replace.replace_with(new_p)
                processed_sections_html_parts[section_id_from_file] = str(budget_soup)
            else:
                processed_sections_html_parts[section_id_from_file] = processed_section_html
            print(f"Processed section: {section_id_from_file} with currency placeholder.")
        else:
            # For other regular content files
            processed_section_html = process_markdown_to_html_section(
                section_title_from_file, 
                section_md_content, 
                section_id_from_file
            )
            processed_sections_html_parts[section_id_from_file] = processed_section_html
        print(f"Processed individual content file: {md_file_name} -> {section_id_from_file}")


    # Now, inject the processed sections into the template in a desired order
    container_div = soup.find('div', class_='container')
    if container_div:
        # Define a logical order for sections (matching template structure)
        # This order needs to reflect the desired output sequence
        section_order_to_insert = [
            "overview",
            "weather_info", # Note: filename "weather_info.md" becomes id "weather_info"
            "day1", "day2", "day3", "day4", "day5", "day6", "day7", "day8",
            "budget",
            "accommodation",
            "food_recommendations",
            "shopping_guide",
            "transportation_budget",
            "important_updates",
            "hotel-timeline" # This will contain the detailed hotel timeline
        ]

        # Clear existing section placeholders if they are just empty divs by id
        for div_id in section_order_to_insert:
            placeholder_div = container_div.find('div', id=div_id)
            if placeholder_div:
                placeholder_div.decompose() # Remove the empty placeholder div
        
        # Append the fully formed <section> tags in the defined order
        for section_id_to_add in section_order_to_insert:
            if section_id_to_add in processed_sections_html_parts:
                container_div.append(BeautifulSoup(processed_sections_html_parts[section_id_to_add], 'html.parser'))
                print(f"Injected section: {section_id_to_add}")
            else:
                print(f"Warning: Section '{section_id_to_add}' not found in processed content, skipping insertion.")
    else:
        print("Error: Main content container (.container) not found in template.")
        return

    # 6. Generate final HTML file
    current_datetime_str = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    output_filename = BUILD_DIR / f"Tokyo-Trip-March-2026-FINAL-{current_datetime_str}.html"
    
    try:
        with open(output_filename, "w", encoding='utf-8') as f_out:
            f_out.write(str(soup))
        print(f"✅ Successfully generated: {output_filename}")
    except Exception as e:
        print(f"Error writing output file {output_filename}: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    generate_trip_guide_html()