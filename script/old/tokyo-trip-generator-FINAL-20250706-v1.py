#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokyo Trip Generator - REFACTORED VERSION ⭐
============================================
🎯 เป้าหมาย: อ่านเนื้อหาจาก content/ และสร้าง HTML guide ครบเนื้อหา >800KB 
📅 สำหรับ: ทริปโตเกียว 6-13 มีนาคม 2026 (พ่อลูก)
✨ Features: Beautiful UI + Complete Content + Expand/Collapse

Author: Claude AI Assistant (Refactored)
Date: 6 July 2025
Version: REFACTORED-20250706
"""

import datetime
from pathlib import Path
import os
import re

class TokyoTripGenerator:
    """Generator ที่อ่านเนื้อหาจาก content/ folders และสร้าง HTML guide"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_dir = self.script_dir.parent
        self.content_dir = self.project_dir / "content"
        self.build_dir = self.project_dir / "build"
        self.build_dir.mkdir(exist_ok=True)
        
        # Check content folders
        self.th_dir = self.content_dir / "th"
        self.en_dir = self.content_dir / "en"
        
        print(f"📁 Initialized TokyoTripGenerator")
        print(f"   📂 Thai content: {self.th_dir}")
        print(f"   📂 English content: {self.en_dir}")
        print(f"   📂 Build output: {self.build_dir}")
        
    def read_markdown_file(self, filepath):
        """อ่านไฟล์ markdown และจัดการ encoding"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"   ✅ Read: {filepath.name} ({len(content)} chars)")
                return content
        except FileNotFoundError:
            print(f"   ⚠️ File not found: {filepath}")
            return ""
        except Exception as e:
            print(f"   ❌ Error reading {filepath}: {e}")
            return ""
    
    def get_html_header(self):
        """HTML Header พร้อม CSS ที่สมบูรณ์"""
        return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ทริปโตเกียว มีนาคม 2026 - คู่มือสมบูรณ์</title>
    <style>
/* ===== CSS VARIABLES ===== */
:root {
    --primary: #2E86AB; 
    --secondary: #A23B72; 
    --accent: #F18F01; 
    --success: #C73E1D;
    --background: #F5F9FC; 
    --card-bg: #FFFFFF; 
    --text-primary: #2C3E50; 
    --text-secondary: #5A6C7D;
    --border: #E1E8ED; 
    --shadow: 0 4px 6px rgba(0,0,0,0.1); 
    --border-radius: 12px;
    --transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    --info-bg: #dbeafe; 
    --info-border: #3b82f6; 
    --note-bg: #f3f4f6; 
    --note-border: #6b7280;
}

/* ===== RESET & BASE ===== */
* { 
    margin: 0; 
    padding: 0; 
    box-sizing: border-box; 
}

body { 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    line-height: 1.6; 
    color: var(--text-primary);
    background: linear-gradient(135deg, var(--background) 0%, #E8F4F8 100%); 
    min-height: 100vh; 
    padding-top: 4rem;
}

.container { 
    max-width: 1200px; 
    margin: 0 auto; 
    padding: 2rem; 
}

/* ===== LANGUAGE SWITCHER ===== */
.language-switcher {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 1000;
    display: flex;
    gap: 0.5rem;
}

.lang-btn {
    padding: 0.5rem 1.5rem;
    border: 2px solid var(--primary);
    background: white;
    color: var(--primary);
    border-radius: 25px;
    cursor: pointer;
    font-weight: 600;
    transition: var(--transition);
    box-shadow: var(--shadow);
}

.lang-btn.active {
    background: var(--primary);
    color: white;
    transform: translateY(-2px);
}

.lang-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

/* ===== LANGUAGE VISIBILITY ===== */
.lang-th .en { display: none; }
.lang-en .th { display: none; }
.lang-th .th, .lang-en .en { display: inline; }
.lang-en .en-block, .lang-th .th-block { display: block; }
.lang-en .th-block, .lang-th .en-block { display: none; }

/* ===== HEADER ===== */
.header {
    text-align: center;
    margin-bottom: 3rem;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: white;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
}

.header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
    animation: sparkle 10s linear infinite;
}

@keyframes sparkle {
    from { transform: translateX(-100px) translateY(-100px) rotate(0deg); }
    to { transform: translateX(100px) translateY(100px) rotate(360deg); }
}

.header h1 {
    font-size: 2.8rem;
    margin-bottom: 1rem;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    position: relative;
    z-index: 1;
}

.header .subtitle {
    font-size: 1.3rem;
    opacity: 0.95;
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
}

.header .dates {
    font-size: 1.1rem;
    opacity: 0.9;
    font-weight: 500;
    position: relative;
    z-index: 1;
}

/* ===== NAVIGATION GRID ===== */
.nav-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.nav-card {
    background: white;
    border-radius: var(--border-radius);
    padding: 1.5rem;
    text-decoration: none;
    color: var(--text-primary);
    box-shadow: var(--shadow);
    transition: var(--transition);
    border-left: 4px solid var(--accent);
    position: relative;
    overflow: hidden;
}

.nav-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.nav-card h3 {
    color: var(--primary);
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
}

.nav-card .date {
    color: var(--secondary);
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.nav-card .desc {
    color: var(--text-secondary);
    font-size: 0.95rem;
}

.birthday-badge {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: linear-gradient(45deg, #ff6b6b, #feca57);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 600;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* ===== SECTIONS ===== */
.section {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 2.5rem;
    margin-bottom: 2.5rem;
    box-shadow: var(--shadow);
    border-left: 5px solid var(--accent);
    transition: var(--transition);
}

.section:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.section h1 {
    color: var(--primary);
    margin-bottom: 2rem;
    font-size: 2.2rem;
    border-bottom: 3px solid var(--accent);
    padding-bottom: 0.5rem;
}

.section h2 {
    color: var(--secondary);
    margin: 2rem 0 1.5rem 0;
    font-size: 1.8rem;
    border-left: 4px solid var(--accent);
    padding-left: 1rem;
}

.section h3 {
    color: var(--primary);
    margin: 1.5rem 0 1rem 0;
    font-size: 1.4rem;
}
    </style>
</head>
<body class="lang-th">'''

    def get_navigation_and_body_start(self):
        """Navigation และการเริ่มต้น body"""
        return '''
    <!-- Language Switcher -->
    <div class="language-switcher">
        <button class="lang-btn active" data-lang="th">🇹🇭 ไทย</button>
        <button class="lang-btn" data-lang="en">🇺🇸 English</button>
    </div>

    <div class="container">
        <!-- Header -->
        <header class="header">
            <h1>🇯🇵 ทริปโตเกียว มีนาคม 2026</h1>
            <div class="subtitle">คู่มือเดินทางฉบับสมบูรณ์ สำหรับพ่อลูก</div>
            <div class="dates">📅 6-13 มีนาคม 2026 (8 วัน 7 คืน)</div>
        </header>
'''
    def get_css_content_and_timeline(self):
        """CSS สำหรับ Content styling และ Timeline components"""
        return '''
/* ===== CONTENT STYLING ===== */
.content p {
    margin-bottom: 1rem;
    text-align: justify;
    line-height: 1.7;
}

.content ul {
    margin: 1rem 0 1rem 2rem;
}

.content ol {
    margin: 1rem 0 1rem 2rem;
}

.content li {
    margin-bottom: 0.5rem;
    line-height: 1.6;
}

.content strong {
    color: var(--primary);
    font-weight: 600;
}

.content em {
    color: var(--secondary);
    font-style: italic;
}

/* ===== INFO/NOTE BOXES ===== */
.info-box, .note-box {
    border-left: 4px solid var(--info-border);
    background: var(--info-bg);
    padding: 1.5rem;
    margin: 2rem 0;
    border-radius: 0 var(--border-radius) var(--border-radius) 0;
    box-shadow: var(--shadow);
}

.note-box {
    border-left-color: var(--note-border);
    background: var(--note-bg);
}

.info-box strong, .note-box strong {
    color: var(--info-border);
}

.note-box strong {
    color: var(--note-border);
}

/* ===== TIMELINE STYLES ===== */
.timeline {
    list-style: none;
    padding: 0;
    margin: 2rem 0;
    position: relative;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 1.5rem;
    top: 0;
    bottom: 0;
    width: 3px;
    background: linear-gradient(to bottom, var(--primary), var(--accent));
    border-radius: 2px;
}

.timeline li {
    position: relative;
    padding: 1.5rem 0 1.5rem 4rem;
    border-bottom: 1px solid var(--border);
}

.timeline li:last-child {
    border-bottom: none;
}

.timeline li::before {
    content: '';
    position: absolute;
    left: 0.8rem;
    top: 2rem;
    width: 1.4rem;
    height: 1.4rem;
    background: var(--primary);
    border-radius: 50%;
    border: 3px solid white;
    box-shadow: 0 0 0 3px var(--primary);
    z-index: 1;
}

.timeline-main {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1rem;
}

.timeline-toggle {
    background: var(--accent);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: var(--transition);
    margin-bottom: 1rem;
}

.timeline-toggle:hover {
    background: var(--secondary);
    transform: translateY(-1px);
}

.timeline-toggle.expanded {
    background: var(--secondary);
}

.timeline-detail {
    background: rgba(46, 134, 171, 0.05);
    border-radius: var(--border-radius);
    padding: 1rem;
    margin-top: 1rem;
    border-left: 3px solid var(--accent);
}

.timeline-sub-content p {
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
    line-height: 1.5;
}

.timeline-sub-content p:last-child {
    margin-bottom: 0;
}

/* ===== TABLES ===== */
.table-container {
    overflow-x: auto;
    margin: 2rem 0;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    background: white;
}

table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

th, td {
    padding: 1rem 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
}

th {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    font-weight: 600;
    position: sticky;
    top: 0;
    z-index: 10;
}

tr:nth-child(even) {
    background: rgba(46, 134, 171, 0.05);
}

tr:hover {
    background: rgba(46, 134, 171, 0.1);
}

/* ===== BACK TO TOP ===== */
.back-to-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--primary);
    color: white;
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    font-size: 1.2rem;
    box-shadow: var(--shadow);
    transition: var(--transition);
    opacity: 0.5;
    pointer-events: none;
    z-index: 1000;
}

.back-to-top:hover {
    background: var(--secondary);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .container { 
        padding: 1rem; 
    }
    
    .header { 
        padding: 2rem 1rem; 
    }
    
    .header h1 { 
        font-size: 2rem; 
    }
    
    .section { 
        padding: 1.5rem; 
    }
    
    .language-switcher { 
        top: 0.5rem; 
        right: 0.5rem; 
    }
    
    .nav-grid {
        grid-template-columns: 1fr;
    }
    
    .timeline li {
        padding-left: 3rem;
    }
    
    .timeline::before {
        left: 1rem;
    }
    
    .timeline li::before {
        left: 0.3rem;
    }
}

@media (max-width: 480px) {
    .header h1 {
        font-size: 1.5rem;
    }
    
    .header .subtitle {
        font-size: 1rem;
    }
    
    .lang-btn {
        padding: 0.4rem 1rem;
        font-size: 0.9rem;
    }
}
'''

    def get_navigation_overview(self):
    """สร้าง navigation overview สำหรับกระโดดไปแต่ละวัน"""
    return '''
    <section class="section" id="overview">
        <h1>📋 ภาพรวมการเดินทาง</h1>
        
        <!-- Quick Info -->
        <div class="info-box">
            <div class="info-toggle">
                <span class="th">🎯 ข้อมูลสำคัญ</span>
                <span class="en">🎯 Essential Information</span>
            </div>
            <div class="info-detail">
                <div class="th">
                    <p><strong>📅 วันเดินทาง:</strong> 6-13 มีนาคม 2026 (8 วัน 7 คืน)</p>
                    <p><strong>👥 ผู้เดินทาง:</strong> พ่อลูก (Arilek & Pojai วัย 11 ขวบ)</p>
                    <p><strong>💰 งบประมาณ:</strong> ~100,000 บาท + buffer 30-50k</p>
                    <p><strong>🎂 วันเกิดโปใจ:</strong> 9 มีนาคม (วันที่ 4 ของทริป) 🎉</p>
                </div>
                <div class="en">
                    <p><strong>📅 Travel Dates:</strong> March 6-13, 2026 (8 Days 7 Nights)</p>
                    <p><strong>👥 Travelers:</strong> Father & Daughter (Arilek & Pojai age 11)</p>
                    <p><strong>💰 Budget:</strong> ~100,000 THB + buffer 30-50k</p>
                    <p><strong>🎂 Pojai's Birthday:</strong> March 9 (Day 4 of trip) 🎉</p>
                </div>
            </div>
        </div>
        
        <!-- Day Navigation -->
        <h2>📅 รายละเอียดแต่ละวัน</h2>
        <div class="nav-grid">
            <a href="#section-3" class="nav-card">
                <h3>วันที่ 1</h3>
                <div class="date">6 มีนาคม 2026 (ศุกร์)</div>
                <div class="desc">✈️ เดินทางถึงโตเกียว - เช็คอิน - พักผ่อน</div>
            </a>
            
            <a href="#section-4" class="nav-card">
                <h3>วันที่ 2</h3>
                <div class="date">7 มีนาคม 2026 (เสาร์)</div>
                <div class="desc">🏮 อาซากุสะ - วัดเซ็นโซจิ - สกายทรี</div>
            </a>
            
            <a href="#section-5" class="nav-card">
                <h3>วันที่ 3</h3>
                <div class="date">8 มีนาคม 2026 (อาทิตย์)</div>
                <div class="desc">🏰 พระราชวังอิมพีเรียล - กินซ่า - ช้อปปิ้ง</div>
            </a>
            
            <a href="#section-6" class="nav-card" style="position: relative;">
                <div class="birthday-badge">🎂 วันเกิด</div>
                <h3>วันที่ 4</h3>
                <div class="date">9 มีนาคม 2026 (จันทร์)</div>
                <div class="desc">🎉 วันเกิดโปใจ - ดิสนีย์แลนด์ - เซอร์ไพรส์!</div>
            </a>
            
            <a href="#section-7" class="nav-card">
                <h3>วันที่ 5</h3>
                <div class="date">10 มีนาคม 2026 (อังคาร)</div>
                <div class="desc">🗼 โตเกียวทาวเวอร์ - ร้อปปงงิ - มิดทาวน์</div>
            </a>
            
            <a href="#section-8" class="nav-card">
                <h3>วันที่ 6</h3>
                <div class="date">11 มีนาคม 2026 (พุธ)</div>
                <div class="desc">🌸 อุเอโนะ - สวนซากุระ - พิพิธภัณฑ์</div>
            </a>
            
            <a href="#section-9" class="nav-card">
                <h3>วันที่ 7</h3>
                <div class="date">12 มีนาคม 2026 (พฤหัสบดี)</div>
                <div class="desc">🏔️ ภูเขาไฟฟูจิ - ฮาโกเน่ - ออนเซ็น</div>
            </a>
            
            <a href="#section-10" class="nav-card">
                <h3>วันที่ 8</h3>
                <div class="date">13 มีนาคม 2026 (ศุกร์)</div>
                <div class="desc">🎁 ช้อปปิ้งของฝาก - เดินทางกลับ</div>
            </a>
        </div>
    </section>
    '''
    
    def markdown_to_html(self, markdown_content):
        """แปลง markdown เป็น HTML อย่างสมบูรณ์ รวม tables, timelines, info boxes"""
        if not markdown_content.strip():
            return "<p>ไม่มีเนื้อหา</p>"
            
        html = markdown_content
        
        # Headers
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        # Tables (markdown style |col1|col2|)
        html = self.convert_tables(html)
        
        # Timeline items (- **time**: content)
        html = self.convert_timeline_items(html)
        
        # Info boxes (lines starting with 📌 or ⚠️ or 💡)
        html = self.convert_info_boxes(html)
        
        # Lists
        html = self.convert_lists(html)
        
        # Paragraphs
        html = self.convert_paragraphs(html)
        
        return html
    
    def convert_tables(self, html):
    """แปลง markdown tables เป็น HTML tables"""
    lines = html.split('\n')
    result = []
    in_table = False
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # ตรวจสอบว่าเป็น table header หรือไม่
        if '|' in line and not in_table and line.count('|') >= 2:
            # ตรวจสอบบรรทัดถัดไปว่าเป็น separator หรือไม่
            if i + 1 < len(lines) and re.match(r'^\s*\|[\s\-\|:]*\|\s*$', lines[i + 1]):
                # เริ่ม table
                in_table = True
                result.append('<div class="table-container">')
                result.append('<table>')
                result.append('<thead>')
                
                # Header row
                headers = [cell.strip() for cell in line.split('|') if cell.strip()]
                result.append('<tr>')
                for header in headers:
                        result.append(f'<th>{header}</th>')
                result.append('</tr>')
                result.append('</thead>')
                result.append('<tbody>')
                
                i += 2  # ข้าม separator line
                continue
                
        elif '|' in line and in_table and line.count('|') >= 2:
            # Table row
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if cells:  # ถ้ามี cells
                result.append('<tr>')
                for cell in cells:
                    result.append(f'<td>{cell}</td>')
                result.append('</tr>')
            else:
                # จบ table
                result.append('</tbody>')
                result.append('</table>')
                result.append('</div>')
                in_table = False
                
        elif in_table and ('|' not in line or line.count('|') < 2):
            # จบ table
            result.append('</tbody>')
            result.append('</table>')
            result.append('</div>')
            in_table = False
            result.append(line)
            
        else:
            result.append(line)
            
        i += 1
    
    # ปิด table ถ้ายังเปิดอยู่
    if in_table:
        result.append('</tbody>')
        result.append('</table>')
        result.append('</div>')
        
    return '\n'.join(result)

    def convert_timeline_items(self, html):
    """แปลง timeline items เป็น HTML timeline"""
    lines = html.split('\n')
    result = []
    in_timeline = False
    timeline_id = 0
    
    for line in lines:
        # ตรวจสอบ timeline item pattern: - **time**: content
        timeline_match = re.match(r'^\s*-\s*\*\*([^*]+)\*\*:\s*(.+)', line)
        
        if timeline_match:
            if not in_timeline:
                result.append('<ul class="timeline">')
                in_timeline = True
                
            time_text = timeline_match.group(1)
            content_text = timeline_match.group(2)
            timeline_id += 1
            
            result.append('<li>')
            result.append(f'<div class="timeline-main"><strong>{time_text}</strong>: {content_text}</div>')
            
            # เพิ่มปุ่ม toggle สำหรับรายละเอียด
            result.append(f'<button class="timeline-toggle" onclick="toggleTimelineDetail(\'timeline-{timeline_id}\')">')
            result.append('<span class="th">รายละเอียด ▼</span>')
            result.append('<span class="en">Details ▼</span>')
            result.append('</button>')
            result.append(f'<div class="timeline-detail" id="timeline-{timeline_id}" style="display: none;">')
            result.append('<div class="timeline-sub-content">')
            
        elif line.strip().startswith('  -') and in_timeline:
            # Sub-item ของ timeline
            sub_content = line.strip()[2:].strip()  # เอา "- " ออก
            result.append(f'<p>• {sub_content}</p>')
            
        elif line.strip().startswith('  ') and in_timeline and line.strip():
            # รายละเอียดเพิ่มเติม
            detail_content = line.strip()
            result.append(f'<p>{detail_content}</p>')
            
        else:
            if in_timeline:
                # ปิด timeline detail และ li
                result.append('</div>')
                result.append('</div>')
                result.append('</li>')
                
                # ถ้าไม่ใช่ timeline item ใหม่ ให้ปิด timeline
                if not re.match(r'^\s*-\s*\*\*([^*]+)\*\*:\s*(.+)', line):
                    result.append('</ul>')
                    in_timeline = False
                    
            result.append(line)
    
    # ปิด timeline ถ้ายังเปิดอยู่
    if in_timeline:
        result.append('</div>')
        result.append('</div>')
        result.append('</li>')
        result.append('</ul>')
        
    return '\n'.join(result)
    
    def convert_info_boxes(self, html):
        """แปลง info boxes จาก special markers"""
        lines = html.split('\n')
        result = []
        in_info_box = False
        box_type = ''
        
        for line in lines:
            # ตรวจสอบ info box markers
            if line.strip().startswith('📌') or line.strip().startswith('💡') or line.strip().startswith('⚠️'):
                if in_info_box:
                    result.append('</div>')
                    
                box_type = 'info' if line.strip().startswith('📌') or line.strip().startswith('💡') else 'note'
                content = line.strip()[2:].strip()  # เอา emoji ออก
                
                result.append(f'<div class="{box_type}-box">')
                result.append(f'<strong>{content}</strong>')
                in_info_box = True
                
            elif in_info_box and line.strip() == '':
                result.append('</div>')
                in_info_box = False
                result.append(line)
                
            else:
                result.append(line)
                
        # ปิด info box ถ้ายังเปิดอยู่
        if in_info_box:
            result.append('</div>')
            
        return '\n'.join(result)
    
    def convert_lists(self, html):
        """แปลง lists"""
        lines = html.split('\n')
        result = []
        in_list = False
        
        for line in lines:
            if re.match(r'^\s*[-*]\s+', line):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                item = re.sub(r'^\s*[-*]\s+', '', line)
                result.append(f'<li>{item}</li>')
            else:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                result.append(line)
        
        if in_list:
            result.append('</ul>')
            
        return '\n'.join(result)
    
    def convert_paragraphs(self, html):
        """แปลง paragraphs"""
        lines = html.split('\n')
        result = []
        
        for line in lines:
            if line.strip() and not line.startswith('<') and not re.match(r'^\s*[-*]\s+', line):
                result.append(f'<p>{line.strip()}</p>')
            else:
                result.append(line)
                
        return '\n'.join(result)
    
def get_content_section(self, file_number, title_th, title_en=None):
        """สร้าง section จากไฟล์ content"""
        if title_en is None:
            title_en = title_th
            
        # อ่านไฟล์ thai
        th_file = self.th_dir / f"{file_number:03d}-{title_th.lower().replace(' ', '-')}.md"
        th_content = self.read_markdown_file(th_file)
        
        # อ่านไฟล์ english (ถ้ามี)
        en_file = self.en_dir / f"{file_number:03d}-{title_en.lower().replace(' ', '-')}.md"
        en_content = self.read_markdown_file(en_file)
        if not en_content:
            en_content = th_content  # fallback ใช้ thai
        
        # แปลง markdown เป็น HTML
        th_html = self.markdown_to_html(th_content)
        en_html = self.markdown_to_html(en_content)
        
        return f'''
        <section class="section" id="section-{file_number}">
            <div class="th-block">
                <div class="content">{th_html}</div>
            </div>
            <div class="en-block" style="display: none;">
                <div class="content">{en_html}</div>
            </div>
        </section>
        '''

def get_back_to_top(self):
    """Back to top button"""
    return '''
<!-- Back to Top -->
<a href="#" class="back-to-top">⬆</a>
'''

def get_javascript(self):
    """JavaScript สำหรับ language switching และ timeline functionality"""
    return '''
<!-- Back to Top -->
<a href="#" class="back-to-top">⬆</a>

<script>
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
        
        // บันทึก language preference
        try {
            localStorage.setItem('tokyo-trip-lang', lang);
        } catch (e) {
            console.warn('Cannot save language preference:', e);
        }
        
        console.log(`Language switched to: ${lang}`);
    }

    // Timeline toggle functionality
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
            button.innerHTML = button.innerHTML.replace('▼', '▲');
            button.classList.add('expanded');
            console.log(`Timeline detail expanded: ${detailId}`);
        } else {
            detail.style.display = 'none';
            button.innerHTML = button.innerHTML.replace('▲', '▼');
            button.classList.remove('expanded');
            console.log(`Timeline detail collapsed: ${detailId}`);
        }
    }
    
    // Make toggleTimelineDetail globally available
    window.toggleTimelineDetail = toggleTimelineDetail;
    
    // Initialize timeline functionality
    function initializeTimelineToggle() {
        console.log('🔧 Initializing timeline toggle...');
        
        // Find all timeline detail elements and hide them initially
        const timelineDetails = document.querySelectorAll('.timeline-detail');
        timelineDetails.forEach(detail => {
            detail.style.display = 'none';
        });
        
        console.log(`✅ Timeline toggle initialized for ${timelineDetails.length} details`);
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
        console.log('✅ Smooth scrolling initialized');
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
                    backToTop.style.opacity = '0.5';
                    backToTop.style.pointerEvents = 'none';
                }
            });
            
            backToTop.addEventListener('click', function(e) {
                e.preventDefault();
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
            
            console.log('✅ Back to top button initialized');
        }
    }

    // Loading animation
    function showLoadingComplete() {
        setTimeout(() => {
            console.log('🎉 Tokyo Trip 2026 - Complete Guide Ready with ALL FEATURES!');
            
            // Show a brief loading complete message
            const loadingMsg = document.createElement('div');
            loadingMsg.style.cssText = `
                position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #2E86AB, #A23B72); color: white;
                padding: 1rem 2rem; border-radius: 10px; z-index: 10000;
                font-weight: 600; box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            `;
            loadingMsg.textContent = '🇯🇵 Tokyo Trip Guide Ready! 🎉';
            document.body.appendChild(loadingMsg);
            
            setTimeout(() => {
                loadingMsg.style.opacity = '0';
                loadingMsg.style.transition = 'opacity 0.5s';
                setTimeout(() => loadingMsg.remove(), 500);
            }, 1500);
        }, 500);
    }

    // Main initialization
    document.addEventListener('DOMContentLoaded', function() {
        console.log('🇯🇵 Tokyo Trip 2026 - Complete Guide Loading...');
        
        // Language setup
        try {
            const savedLang = localStorage.getItem('tokyo-trip-lang');
            if (savedLang && (savedLang === 'th' || savedLang === 'en')) {
                switchLanguage(savedLang);
            } else {
                switchLanguage('th'); // default to Thai
            }
        } catch (e) {
            console.warn('Cannot load language preference:', e);
            switchLanguage('th');
        }
        
        // Setup language switcher buttons
        document.querySelectorAll('[data-lang]').forEach(btn => {
            btn.addEventListener('click', function() {
                const lang = this.getAttribute('data-lang');
                switchLanguage(lang);
            });
        });
        
        // Initialize all features
        initializeTimelineToggle();
        initializeSmoothScrolling();
        initializeBackToTop();
        
        // Show loading complete message
        showLoadingComplete();
        
        console.log('🚀 All features initialized successfully!');
    });
    
    // Error handling
    window.addEventListener('error', function(e) {
        console.error('JavaScript Error:', e.error);
    });
    
    // Performance monitoring
    window.addEventListener('load', function() {
        console.log(`📊 Page loaded in ${Math.round(performance.now())}ms`);
    });
</script>
</body>
</html>'''

def generate_html(self):
        """สร้าง HTML file ครบเนื้อหา พร้อม navigation และ features ครบ"""
        print("🇯🇵 TOKYO TRIP GENERATOR - REFACTORED VERSION 🇯🇵")
        print("=" * 70)
        print("📁 Reading content from:")
        print(f"   📄 TH: {self.th_dir}")
        print(f"   📄 EN: {self.en_dir}")
        
        # ตรวจสอบว่ามีโฟลเดอร์ content หรือไม่
        if not self.th_dir.exists():
            print(f"⚠️ Warning: Thai content directory not found: {self.th_dir}")
        if not self.en_dir.exists():
            print(f"⚠️ Warning: English content directory not found: {self.en_dir}")
        
        # เริ่มสร้าง HTML
        html_parts = []
        
        # 1. HTML Header และ CSS
        html_parts.append(self.get_html_header())
        html_parts.append(self.get_css_content_and_timeline())
        html_parts.append('    </style>\n</head>\n<body class="lang-th">')
        
        # 2. Navigation และ body start
        html_parts.append(self.get_navigation_and_body_start())
        
        # 3. เพิ่ม navigation overview ก่อน
        html_parts.append(self.get_navigation_overview())
        
        # 4. เพิ่ม content sections
        content_files = [
            (1, "overview"),
            (2, "accommodation"), 
            (3, "day1"),
            (4, "day2"),
            (5, "day3"),
            (6, "day4"),
            (7, "day5"),
            (8, "day6"),
            (9, "day7"),
            (10, "day8"),
            (11, "transportation"),
            (12, "weather"),
            (13, "budget"),
            (14, "tips")
        ]
        
        print("\n📝 Adding content sections:")
        for file_num, title in content_files:
            print(f"   🔄 Processing: {file_num:03d}-{title}.md")
            section_html = self.get_content_section(file_num, title)
            html_parts.append(section_html)
        
        # 5. ปิด container และเพิ่ม JavaScript
        html_parts.append("\n    </div>  <!-- end container -->")
        html_parts.append(self.get_javascript())
        
        # รวม HTML ทั้งหมด
        html_content = ''.join(html_parts)
        
        # บันทึกไฟล์
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        filename = f"Tokyo-Trip-March-2026-REFACTORED-{timestamp}.html"
        output_path = self.build_dir / filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n🎉 HTML Generated Successfully!")
            print(f"📄 File: {filename}")
            print(f"📊 Size: {len(html_content):,} characters ({len(html_content)/1024:.1f} KB)")
            print(f"📍 Path: {output_path}")
            
            # Features summary
            print(f"\n🚀 Features included:")
            features = [
                "✅ Beautiful responsive design",
                "✅ Navigation overview with day cards", 
                "✅ Timeline with expand/collapse functionality",
                "✅ HTML tables from markdown",
                "✅ Language switching (TH/EN) with localStorage",
                "✅ Birthday badge animation",
                "✅ Smooth scrolling navigation",
                "✅ Back to top button with scroll detection",
                "✅ Mobile responsive design",
                "✅ Loading animations and error handling",
                "✅ Performance monitoring"
            ]
            
            for feature in features:
                print(f"   {feature}")
            
            # Size analysis
            if len(html_content) > 800000:
                print(f"\n🎯 Target achieved: >800KB content! ({len(html_content)/1024:.1f} KB)")
            else:
                print(f"\n📏 Current size: {len(html_content)/1024:.1f}KB")
                if len(html_content) > 500000:
                    print("   📈 Good size - approaching target!")
                else:
                    print("   📝 Consider adding more content to reach 800KB target")
            
            # Content breakdown
            sections_count = len(content_files)
            avg_section_size = len(html_content) / sections_count if sections_count > 0 else 0
            print(f"\n📊 Content breakdown:")
            print(f"   📑 Total sections: {sections_count}")
            print(f"   📏 Average section size: {avg_section_size/1024:.1f} KB")
            
        except Exception as e:
            print(f"\n❌ Error writing file: {e}")
            return None
            
        return output_path

def validate_content_structure(self):
    """ตรวจสอบโครงสร้างไฟล์ content"""
    print("\n🔍 Validating content structure...")
    
    issues = []
    
    # ตรวจสอบโฟลเดอร์หลัก
    if not self.content_dir.exists():
        issues.append(f"❌ Content directory missing: {self.content_dir}")
    
    if not self.th_dir.exists():
        issues.append(f"❌ Thai content directory missing: {self.th_dir}")
        
    if not self.en_dir.exists():
        issues.append(f"⚠️ English content directory missing: {self.en_dir}")
    
    # ตรวจสอบไฟล์ที่คาดหวัง
    expected_files = [
        "001-overview.md", "002-accommodation.md", "003-day1.md", "004-day2.md",
        "005-day3.md", "006-day4.md", "007-day5.md", "008-day6.md",
        "009-day7.md", "010-day8.md", "011-transportation.md", "012-weather.md",
        "013-budget.md", "014-tips.md"
    ]
    
    if self.th_dir.exists():
        for filename in expected_files:
            filepath = self.th_dir / filename
            if not filepath.exists():
                issues.append(f"⚠️ Missing Thai file: {filename}")
    
    if issues:
        print("📋 Issues found:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("✅ Content structure looks good!")
        
    return len(issues) == 0

def main():
    """Entry point สำหรับ script"""
    print("🎌 Tokyo Trip Generator - Starting...")
    print("🔧 Refactored version with improved error handling")
    print()
    
    try:
        # สร้าง generator instance
        generator = TokyoTripGenerator()
        
        # ตรวจสอบโครงสร้างไฟล์
        generator.validate_content_structure()
        
        # สร้าง HTML
        output_file = generator.generate_html()
        
        if output_file:
            print(f"\n🚀 Ready to use: {output_file}")
            print(f"🌐 Open the HTML file in your browser to view the guide!")
            print(f"📱 The guide is mobile-responsive and works offline!")
            
            # แสดงคำแนะนำการใช้งาน
            print(f"\n💡 Usage tips:")
            print(f"   🔄 Use language switcher (TH/EN) in top-right corner")
            print(f"   📅 Click day cards to jump to specific day plans")
            print(f"   🔍 Click 'รายละเอียด' buttons to expand timeline details")
            print(f"   ⬆ Use back-to-top button for easy navigation")
            
        else:
            print("\n❌ Failed to generate HTML file")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Generation cancelled by user")
        return 1
        
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
    