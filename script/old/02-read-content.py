#!/usr/bin/env python3
"""
🇯🇵 Tokyo Trip 2026 HTML Generator - BEAUTIFUL & WORKING VERSION
เอา CSS/JS จาก ultimate_fixer.py ที่สวยและทำงานได้ + อ่านไฟล์ EN/TH ได้
"""

import os
import re
import sys
import json
import datetime
from pathlib import Path

print("🇯🇵 Tokyo Trip 2026 HTML Generator - BEAUTIFUL & WORKING VERSION")
print("=" * 60)
print("✨ Features: Timeline expand/collapse, Multi-language, Responsive, Offline-ready")
print("🎨 Using ultimate_fixer CSS/JS for beautiful look & feel")
print()

# --- Configuration and Paths ---
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
CONTENT_DIR = BASE_DIR / "content"
BUILD_DIR = BASE_DIR / "build"

# Ensure build directory exists
BUILD_DIR.mkdir(parents=True, exist_ok=True)

print(f"🔧 Config initialized:")
print(f"   Script dir: {SCRIPT_DIR}")
print(f"   Content dir: {CONTENT_DIR}")
print(f"   Build dir: {BUILD_DIR}")
print()

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

def simple_markdown_to_html(content):
    """Enhanced markdown to HTML conversion."""
    # Headers
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
    
    # Bold and italic
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
    
    # Code
    content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
    
    # Links
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
    
    # Lists
    lines = content.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            item_content = line.strip()[2:]
            html_lines.append(f'<li>{item_content}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if line.strip():
                html_lines.append(f'<p>{line}</p>')
            else:
                html_lines.append('')
    
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)

def create_beautiful_timeline_content(content):
    """Process timeline content with beautiful expand/collapse functionality."""
    lines = content.split('\n')
    html_parts = []
    timeline_counter = 0
    
    html_parts.append('<ul class="timeline">')
    
    for line in lines:
        if line.strip().startswith('- **') and '**:' in line:
            # Timeline item
            match = re.match(r'- \*\*([^*]+)\*\*:\s*(.*)', line)
            if match:
                time_part = match.group(1)
                content_part = match.group(2)
                
                timeline_counter += 1
                detail_id = f'timeline-{timeline_counter}'
                
                html_parts.append(f'<li>')
                html_parts.append(f'<div class="timeline-main"><strong>{time_part}</strong>: {content_part}</div>')
                html_parts.append(f'<button class="timeline-toggle" onclick="toggleTimelineDetail(\'{detail_id}\')">')
                html_parts.append(f'<span class="th">รายละเอียด ▼</span>')
                html_parts.append(f'<span class="en">Details ▼</span>')
                html_parts.append(f'</button>')
                html_parts.append(f'<div class="timeline-detail" id="{detail_id}" style="display: none;">')
                html_parts.append(f'<p><strong>รายละเอียด:</strong> {content_part}</p>')
                html_parts.append(f'</div>')
                html_parts.append(f'</li>')
        elif line.strip():
            # Regular content
            html_parts.append(f'<p>{line}</p>')
    
    html_parts.append('</ul>')
    return '\n'.join(html_parts)

def generate_trip_guide_html():
    """Main function to generate the complete HTML trip guide."""
    print("🎆 Generating BEAUTIFUL HTML...")
    print("📂 Reading markdown content...")
    
    # Read content files with English fallback to Thai
    markdown_contents = {}
    
    content_files = {
        "001-overview.md": "overview",
        "002-accommodation.md": "accommodation", 
        "003-day1.md": "day1",
        "004-day2.md": "day2",
        "005-day3.md": "day3",
        "006-day4.md": "day4",
        "007-day5.md": "day5",
        "008-day6.md": "day6",
        "009-day7.md": "day7",
        "010-day8.md": "day8",
        "011-transportation.md": "transportation",
        "012-weather.md": "weather",
        "013-budget.md": "budget",
        "014-tips.md": "tips"
    }

    # Read files with English fallback to Thai
    thai_count = 0
    english_count = 0
    
    for filename, section_id in content_files.items():
        content = None
        
        # Try English first
        en_file_path = CONTENT_DIR / "en" / filename
        if en_file_path.exists():
            content = read_file_content(en_file_path)
            if content is not None:
                markdown_contents[section_id] = content
                print(f"  ✅ en: {filename} -> {section_id}")
                english_count += 1
                continue
        
        # Fallback to Thai if English not found
        th_file_path = CONTENT_DIR / "th" / filename
        if th_file_path.exists():
            content = read_file_content(th_file_path)
            if content is not None:
                markdown_contents[section_id] = content
                print(f"  ✅ th (fallback): {filename} -> {section_id}")
                thai_count += 1
        else:
            print(f"  ⚠️ Missing both EN and TH: {filename}")

    print(f"✅ Read {english_count} English files")
    print(f"✅ Read {thai_count} Thai files (fallback)")
    print(f"✅ Total: {english_count + thai_count} files")

    if not markdown_contents:
        print("❌ No content files found! Check content directory.")
        return

    # Start building BEAUTIFUL HTML
    print("🎆 Processing content sections - BEAUTIFUL VERSION...")
    
    # Beautiful CSS from ultimate_fixer.py
    beautiful_css = """
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

        .timeline-toggle {
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 0.4rem 0.8rem;
            border-radius: 0.25rem;
            cursor: pointer;
            font-size: 0.8rem;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
        }
        
        .timeline-toggle.expanded {
            background: var(--success);
        }
        
        .timeline-detail {
            margin-top: 0.5rem;
            padding: 0.75rem;
            border-left: 2px solid var(--border-color);
            background: rgba(255, 255, 255, 0.7);
            border-radius: 0.25rem;
            display: none;
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

        /* Mobile responsive */
        @media (max-width: 768px) {
            .container { padding: 0.5rem; }
            header { padding: 1rem; }
            header h1 { font-size: 1.5rem; }
            section { padding: 1rem; }
            .day-overviews { grid-template-columns: 1fr; }
            .lang-switcher { top: 0.5rem; right: 0.5rem; }
        }
    """

    # Working JavaScript from ultimate_fixer.py
    working_javascript = """
        // Language switching
        function switchLanguage(lang) {
            const body = document.body;
            const buttons = document.querySelectorAll('.lang-btn');
            
            body.classList.remove('lang-th', 'lang-en');
            body.classList.add(`lang-${lang}`);
            
            buttons.forEach(btn => {
                btn.classList.remove('active');
                if (btn.getAttribute('data-lang') === lang) {
                    btn.classList.add('active');
                }
            });
            
            try {
                localStorage.setItem('tokyo-trip-lang', lang);
            } catch (e) {}
        }

        // Timeline expand/collapse functionality
        function toggleTimelineDetail(detailId) {
            const detail = document.getElementById(detailId);
            const button = document.querySelector(`[onclick="toggleTimelineDetail('${detailId}')"]`);
            
            if (!detail || !button) {
                console.warn(`Timeline detail not found: ${detailId}`);
                return;
            }
            
            const isHidden = detail.style.display === 'none' || !detail.style.display;
            
            if (isHidden) {
                detail.style.display = 'block';
                button.textContent = button.textContent.replace('▼', '▲');
                button.classList.add('expanded');
            } else {
                detail.style.display = 'none';
                button.textContent = button.textContent.replace('▲', '▼');
                button.classList.remove('expanded');
            }
        }
        
        // Make it globally available
        window.toggleTimelineDetail = toggleTimelineDetail;

        // Main initialization
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🇯🇵 Tokyo Trip 2026 - Loading...');
            
            // Setup language switcher
            document.querySelectorAll('[data-lang]').forEach(btn => {
                btn.addEventListener('click', function() {
                    switchLanguage(this.getAttribute('data-lang'));
                });
            });
            
            // Initialize with Thai
            switchLanguage('th');
            
            console.log('✅ Tokyo Trip 2026 - READY!');
        });
    """
    
    # Build HTML structure
    html_parts = []
    
    # HTML header
    html_parts.append(f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>เที่ยวญี่ปุ่น Porjai: Birthday Trip 2026</title>
    <style>{beautiful_css}</style>
</head>
<body class="lang-th">
    <div class="lang-switcher">
        <button class="lang-btn active" data-lang="th">TH</button>
        <button class="lang-btn" data-lang="en">EN</button>
    </div>

    <div class="container">
        <header>
            <h1>
                <span class="th">เที่ยวญี่ปุ่น Porjai: Birthday Trip 2026</span>
                <span class="en">Porjai's Japan Trip: Birthday Adventure 2026</span>
            </h1>
            <h2>
                <span class="th">📅 6-13 มีนาคม 2026 (8 วัน 7 คืน)</span>
                <span class="en">📅 March 6-13, 2026 (8 Days 7 Nights)</span>
            </h2>
        </header>
''')

    # Add overview section if available
    if "overview" in markdown_contents:
        print("🏠 Creating overview section...")
        html_parts.append(f'''
        <section id="overview">
            <h1>
                <span class="th">ภาพรวมการเดินทางและกิจกรรม</span>
                <span class="en">Trip Overview & Activities</span>
            </h1>
            <div class="day-overviews">
                <div class="day-overview">
                    <h3><a href="#day1"><span class="th">วันที่ 1</span><span class="en">Day 1</span></a></h3>
                    <p><span class="th">เดินทางและเริ่มต้นการผจญภัย</span><span class="en">Travel and start adventure</span></p>
                </div>
                <div class="day-overview">
                    <h3><a href="#day4"><span class="th">วันที่ 4: วันเกิด Porjai</span><span class="en">Day 4: Porjai's Birthday</span></a></h3>
                    <p><span class="th">วันพิเศษสำหรับการเฉลิมฉลอง</span><span class="en">Special celebration day</span></p>
                    <span class="birthday-badge">🎂 Happy Birthday!</span>
                </div>
            </div>
        </section>
        ''')
        print("✅ Overview section created")

    # Process each section
    section_order = ["day1", "day2", "day3", "day4", "day5", "day6", "day7", "day8", 
                    "accommodation", "transportation", "weather", "budget", "tips"]

    for section_id in section_order:
        if section_id in markdown_contents:
            print(f"⏰ Processing section: {section_id}")
            
            content = markdown_contents[section_id]
            
            # Get title from content
            title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
            if title_match:
                section_title = title_match.group(1).strip()
            else:
                section_title = section_id.title()

            # Process content
            if section_id.startswith('day'):
                # Timeline content
                html_content = create_beautiful_timeline_content(content)
                expandable_items = html_content.count('timeline-detail')
                print(f"✅ Timeline processed with {expandable_items} expandable items")
            else:
                # Regular content
                html_content = simple_markdown_to_html(content)
            
            # Add birthday badge for day 4
            birthday_badge = ""
            if section_id == "day4":
                birthday_badge = '<span class="birthday-badge">🎂 Happy Birthday!</span>'
            
            # Build section HTML
            html_parts.append(f'<section id="{section_id}">')
            html_parts.append(f'<h1>{section_title}{birthday_badge}</h1>')
            html_parts.append(html_content)
            html_parts.append('</section>')
            
            chars = len(html_content)
            print(f"  ✅ Enhanced: {section_id} ({chars} chars)")

    # Add JavaScript and close
    html_parts.append(f'''
    <script>{working_javascript}</script>
    </body>
    </html>
    ''')

    # Calculate total content size
    final_html = '\n'.join(html_parts)
    total_html_chars = len(final_html)
    
    print(f"✅ BEAUTIFUL HTML generated: {total_html_chars:,} characters")

    # Generate final HTML file
    current_datetime_str = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    output_filename = BUILD_DIR / f"Tokyo-Trip-March-2026-BEAUTIFUL-{current_datetime_str}.html"
    
    try:
        with open(output_filename, "w", encoding='utf-8') as f_out:
            f_out.write(final_html)
        
        file_size_bytes = output_filename.stat().st_size
        print(f"✅ HTML file saved: {output_filename}")
        print(f"📄 File size: {total_html_chars:,} characters ({file_size_bytes:,} bytes)")
        print()
        print("🎉 Generation completed successfully! - BEAUTIFUL VERSION")
        print(f"📄 Output file: {output_filename}")
        print()
        print("💯 Beautiful Features included:")
        print("   ✅ Timeline expand/collapse (WORKING!)")
        print("   ✅ Multi-language support (TH/EN)")
        print("   ✅ Beautiful responsive design")
        print("   ✅ Birthday badge animation 🎂")
        print("   ✅ Day overview cards")
        print()
        print("🚀 Ready for Tokyo Trip 2026!")
        
    except Exception as e:
        print(f"Error writing output file {output_filename}: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    generate_trip_guide_html()
