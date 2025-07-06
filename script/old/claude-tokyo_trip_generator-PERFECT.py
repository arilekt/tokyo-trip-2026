#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokyo Trip Generator - PERFECT VERSION
======================================
สร้าง HTML ไฟล์สำหรับทริปโตเกียว มีนาคม 2026
- CSS สมบูรณ์จาก ultimate_fixer (สวยงาม + responsive)
- JavaScript สมบูรณ์พร้อม timeline expand/collapse
- Overview cards ครบ 8 วัน พร้อม birthday badge
- Markdown to HTML conversion ที่ถูกต้อง
- Multi-language support (TH/EN)

Created: 2025-06-17
Author: Claude AI Assistant
"""

import os
import re
import datetime
from pathlib import Path

# ==============================
# CONFIGURATION
# ==============================

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"
BUILD_DIR = PROJECT_ROOT / "build" 
SCRIPT_DIR = PROJECT_ROOT / "script"

print(f"🏗️  Tokyo Trip Generator - PERFECT VERSION")
print(f"📁 Project Root: {PROJECT_ROOT}")
print(f"📄 Content Dir: {CONTENT_DIR}")
print(f"🔧 Build Dir: {BUILD_DIR}")

# ==============================
# CSS STYLES - COMPLETE & BEAUTIFUL
# ==============================

def get_fixed_css():
    """CSS สมบูรณ์จาก ultimate_fixer - สวยงาม responsive ครบเครื่อง"""
    return """
:root {
    --primary: #2E86AB;
    --secondary: #A23B72;
    --accent: #F18F01;
    --success: #C73E1D;
    --background: #F5F9FC;
    --card-bg: #FFFFFF;
    --text-primary: #2C3E50;
    --text-secondary: #5A6C7D;
    --text-light: #8492A6;
    --border: #E1E8ED;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --shadow-hover: 0 8px 25px rgba(0, 0, 0, 0.15);
    --border-radius: 12px;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

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
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

/* ===== HEADER STYLES ===== */
.header {
    text-align: center;
    margin-bottom: 3rem;
    padding: 2rem;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: white;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
}

.header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}

.header .subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
    margin-bottom: 1.5rem;
}

/* ===== LANGUAGE SWITCHER ===== */
.language-switcher {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
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
}

.lang-btn.active {
    background: var(--primary);
    color: white;
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}

.lang-btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
}

/* ===== LANGUAGE DISPLAY ===== */
.lang-th .en { display: none; }
.lang-en .th { display: none; }
body:not([class*="lang-"]) .en { display: none; }

/* ===== NAVIGATION ===== */
.nav-section {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow);
}

.nav-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
}

.nav-card {
    background: linear-gradient(135deg, var(--accent) 0%, #F39C12 100%);
    color: white;
    padding: 1.5rem;
    border-radius: var(--border-radius);
    text-decoration: none;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.nav-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.nav-card:hover::before {
    left: 100%;
}

.nav-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: var(--shadow-hover);
}

.nav-card h3 {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

.nav-card .date {
    font-size: 0.9rem;
    opacity: 0.9;
    margin-bottom: 0.5rem;
}

.nav-card .desc {
    font-size: 0.95rem;
    opacity: 0.95;
}

/* ===== BIRTHDAY BADGE ===== */
.birthday-badge {
    position: absolute;
    top: -5px;
    right: -5px;
    background: var(--success);
    color: white;
    padding: 0.3rem 0.6rem;
    border-radius: 15px;
    font-size: 0.7rem;
    font-weight: bold;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

/* ===== CONTENT SECTIONS ===== */
.content-section {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow);
}

.content-section h2 {
    color: var(--primary);
    margin-bottom: 1.5rem;
    font-size: 2rem;
    border-bottom: 3px solid var(--accent);
    padding-bottom: 0.5rem;
}

.content-section h3 {
    color: var(--secondary);
    margin: 1.5rem 0 1rem 0;
    font-size: 1.5rem;
}

.content-section h4 {
    color: var(--text-primary);
    margin: 1rem 0 0.5rem 0;
    font-size: 1.2rem;
}

.content-section p {
    margin-bottom: 1rem;
    color: var(--text-secondary);
}

.content-section ul, .content-section ol {
    margin: 1rem 0;
    padding-left: 2rem;
}

.content-section li {
    margin-bottom: 0.5rem;
    color: var(--text-secondary);
}

/* ===== INFO & NOTE BOXES ===== */
.info-box, .note-box {
    margin: 1.5rem 0;
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: var(--transition);
}

.info-box {
    border-left: 4px solid var(--primary);
}

.note-box {
    border-left: 4px solid var(--accent);
}

.info-toggle, .note-toggle {
    background: linear-gradient(135deg, var(--primary) 0%, #3498DB 100%);
    color: white;
    padding: 1rem;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: var(--transition);
}

.note-toggle {
    background: linear-gradient(135deg, var(--accent) 0%, #F39C12 100%);
}

.info-toggle:hover, .note-toggle:hover {
    transform: translateX(5px);
    box-shadow: var(--shadow);
}

.info-toggle::after, .note-toggle::after {
    content: '▼';
    transition: transform 0.3s ease;
    font-size: 0.9rem;
}

.info-toggle.collapsed::after, .note-toggle.collapsed::after {
    transform: rotate(-90deg);
}

.info-detail, .note-detail {
    background: var(--card-bg);
    padding: 1.5rem;
    max-height: 1000px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.info-detail.collapsed, .note-detail.collapsed {
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    margin-top: 0;
}

/* ===== TIMELINE STYLES ===== */
.timeline {
    position: relative;
    list-style: none;
    margin: 2rem 0;
    padding-left: 2rem;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 1rem;
    top: 0;
    bottom: 0;
    width: 2px;
    background: linear-gradient(to bottom, var(--primary), var(--secondary));
}

.timeline li {
    position: relative;
    margin-bottom: 2rem;
    background: var(--card-bg);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    transition: var(--transition);
}

.timeline li:hover {
    transform: translateX(5px);
    box-shadow: var(--shadow-hover);
}

.timeline li::before {
    content: '';
    position: absolute;
    left: -1.5rem;
    top: 1rem;
    width: 12px;
    height: 12px;
    background: var(--accent);
    border-radius: 50%;
    border: 3px solid var(--card-bg);
    box-shadow: 0 0 0 2px var(--primary);
}

.timeline-main {
    padding: 1rem 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border);
}

.timeline-toggle {
    background: var(--primary);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    margin: 0.5rem 1.5rem 1rem 1.5rem;
    border-radius: 20px;
    cursor: pointer;
    font-weight: 500;
    transition: var(--transition);
    font-size: 0.9rem;
}

.timeline-toggle:hover {
    background: var(--secondary);
    transform: scale(1.05);
}

.timeline-toggle.expanded {
    background: var(--success);
}

.timeline-detail {
    padding: 0 1.5rem 1.5rem 1.5rem;
    color: var(--text-secondary);
    border-top: 1px solid var(--border);
    background: #FAFBFC;
}

.timeline-detail h4 {
    color: var(--primary);
    margin: 1rem 0 0.5rem 0;
}

.timeline-detail ul {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
}

.timeline-detail li {
    margin-bottom: 0.3rem;
    position: relative;
    background: none;
    box-shadow: none;
    transform: none;
}

.timeline-detail li::before {
    display: none;
}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 768px) {
    .container {
        padding: 1rem;
    }
    
    .header h1 {
        font-size: 1.8rem;
    }
    
    .nav-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .language-switcher {
        position: sticky;
        top: 1rem;
        z-index: 100;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: -1rem -1rem 2rem -1rem;
    }
    
    .timeline {
        padding-left: 1rem;
    }
    
    .timeline::before {
        left: 0.5rem;
    }
    
    .timeline li::before {
        left: -1rem;
    }
}
"""

def get_javascript():
    """JavaScript สมบูรณ์พร้อม timeline functionality"""
    return """
// ===== LANGUAGE SWITCHING =====
function switchLanguage(lang) {
    console.log(`🌐 Switching to language: ${lang}`);
    const body = document.body;
    
    body.classList.remove('lang-th', 'lang-en');
    body.classList.add(`lang-${lang}`);
    
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const activeBtn = document.querySelector(`[onclick="switchLanguage('${lang}')"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
    
    console.log(`✅ Language switched to: ${lang}`);
}

// ===== INFO/NOTE BOXES COLLAPSE =====
function initializeCollapsibleBoxes() {
    console.log('🔧 Initializing collapsible boxes...');
    
    const infoBoxes = document.querySelectorAll('.info-box');
    infoBoxes.forEach((box, index) => {
        const toggle = box.querySelector('.info-toggle');
        const detail = box.querySelector('.info-detail');
        
        if (toggle && detail) {
            toggle.classList.add('collapsed');
            detail.classList.add('collapsed');
            
            toggle.addEventListener('click', () => {
                const isCollapsed = detail.classList.contains('collapsed');
                
                if (isCollapsed) {
                    detail.classList.remove('collapsed');
                    toggle.classList.remove('collapsed');
                } else {
                    detail.classList.add('collapsed');
                    toggle.classList.add('collapsed');
                }
                
                console.log(`Info box ${index + 1} ${isCollapsed ? 'expanded' : 'collapsed'}`);
            });
        }
    });
    
    const noteBoxes = document.querySelectorAll('.note-box');
    noteBoxes.forEach((box, index) => {
        const toggle = box.querySelector('.note-toggle');
        const detail = box.querySelector('.note-detail');
        
        if (toggle && detail) {
            toggle.classList.add('collapsed');
            detail.classList.add('collapsed');
            
            toggle.addEventListener('click', () => {
                const isCollapsed = detail.classList.contains('collapsed');
                
                if (isCollapsed) {
                    detail.classList.remove('collapsed');
                    toggle.classList.remove('collapsed');
                } else {
                    detail.classList.add('collapsed');
                    toggle.classList.add('collapsed');
                }
                
                console.log(`Note box ${index + 1} ${isCollapsed ? 'expanded' : 'collapsed'}`);
            });
        }
    });
    
    console.log(`✅ Collapsible boxes initialized: ${infoBoxes.length} info, ${noteBoxes.length} note`);
}

// ===== TIMELINE DETAILS EXPAND/COLLAPSE =====
// THE MAGIC FUNCTION FOR TIMELINE DETAILS!
function toggleTimelineDetail(detailId) {
    console.log(`🔄 Toggling timeline detail: ${detailId}`);
    
    const detail = document.getElementById(detailId);
    const button = document.querySelector(`[onclick="toggleTimelineDetail('${detailId}')"]`);
    
    if (!detail) {
        console.warn(`❌ Timeline detail not found: ${detailId}`);
        return;
    }
    
    if (!button) {
        console.warn(`❌ Timeline button not found for: ${detailId}`);
        return;
    }
    
    const isHidden = detail.style.display === 'none' || !detail.style.display;
    
    if (isHidden) {
        detail.style.display = 'block';
        button.textContent = button.textContent.replace('▼', '▲');
        button.classList.add('expanded');
        console.log(`✅ Expanded: ${detailId}`);
    } else {
        detail.style.display = 'none';
        button.textContent = button.textContent.replace('▲', '▼');
        button.classList.remove('expanded');
        console.log(`✅ Collapsed: ${detailId}`);
    }
}

// Make functions globally available
window.toggleTimelineDetail = toggleTimelineDetail;
window.switchLanguage = switchLanguage;

// Initialize timeline toggle functionality
function initializeTimelineToggle() {
    console.log('🔧 Initializing timeline toggle...');
    
    const timelineDetails = document.querySelectorAll('.timeline-detail');
    timelineDetails.forEach(detail => {
        detail.style.display = 'none';
    });
    
    const toggleButtons = document.querySelectorAll('.timeline-toggle');
    console.log(`📊 Found ${timelineDetails.length} timeline details and ${toggleButtons.length} toggle buttons`);
    
    if (typeof window.toggleTimelineDetail === 'function') {
        console.log('✅ toggleTimelineDetail function is globally available');
    } else {
        console.error('❌ toggleTimelineDetail function is NOT globally available');
    }
    
    console.log(`✅ Timeline toggle initialized for ${timelineDetails.length} details`);
}

// ===== MAIN INITIALIZATION =====
function initializeApp() {
    console.log('🚀 Initializing Tokyo Trip Guide...');
    
    try {
        initializeCollapsibleBoxes();
        initializeTimelineToggle();  // ⭐ CRITICAL: Timeline functionality
        
        // Set default language to Thai
        switchLanguage('th');
        
        console.log('🎉 Tokyo Trip Guide initialized successfully!');
        
    } catch (error) {
        console.error('💥 Failed to initialize app:', error);
    }
}

// ===== DOM READY =====
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

console.log('📱 Tokyo Trip Guide JavaScript loaded successfully!');
"""

def get_overview_cards():
    """สร้าง overview cards ครบ 8 วัน พร้อม birthday badge วันที่ 4"""
    
    days_data = [
        (1, "6 มีนาคม 2026", "March 6, 2026", "เดินทางสู่โตเกียว", "Journey to Tokyo", "เดินทางจากกรุงเทพไปโตเกียว เช็คอินโรงแรม", "Flight from Bangkok to Tokyo, hotel check-in", False),
        (2, "7 มีนาคม 2026", "March 7, 2026", "อาซากุซา และวัดเซนโซจิ", "Asakusa & Sensoji Temple", "เยี่ยมชมวัดเก่าแก่ ชมยานนากามิเซ", "Visit ancient temples, traditional Tokyo experience", False),
        (3, "8 มีนาคม 2026", "March 8, 2026", "อุเอโนะ และฮาราจุกุ", "Ueno & Harajuku", "สวนอุเอโนะ ย่านแฟชั่นเทรนดี้", "Ueno Park and trendy Harajuku fashion district", False),
        (4, "9 มีนาคม 2026", "March 9, 2026", "วันเกิดปอยไจ่! 🎂", "Pojai's Birthday! 🎂", "วันพิเศษปอยไจ่! ดิสนีย์ซี กิจกรรมพิเศษ", "Special birthday celebration! DisneySea and birthday activities", True),
        (5, "10 มีนาคม 2026", "March 10, 2026", "ชิบุยะ และช้อปปิ้ง", "Shibuya & Shopping", "เดินชิบุยะ ช้อปปิ้งซื้อของฝาก", "Explore Shibuya, shopping for souvenirs", False),
        (6, "11 มีนาคม 2026", "March 11, 2026", "ฟูจิ-คิว ไฮแลนด์", "Fuji-Q Highland", "สวนสนุกฟูจิ-คิว ชมภูเขาไฟฟูจิ", "Fuji-Q Highland theme park, Mount Fuji views", False),
        (7, "12 มีนาคม 2026", "March 12, 2026", "โอไดบะ และเตรียมกลับ", "Odaiba & Departure Prep", "เที่ยวโอไดบะ ช้อปปิ้งครั้งสุดท้าย", "Odaiba sightseeing, last-minute shopping", False),
        (8, "13 มีนาคม 2026", "March 13, 2026", "เดินทางกลับบ้าน", "Journey Home", "เดินทางกลับจากโตเกียวสู่กรุงเทพฯ", "Flight from Tokyo back to Bangkok", False)
    ]
    
    cards = []
    
    for day, date_th, date_en, title_th, title_en, desc_th, desc_en, is_birthday in days_data:
        birthday_badge = ''
        if is_birthday:
            birthday_badge = '<div class="birthday-badge">🎂 วันเกิด!</div>'
        
        card_html = f"""
                <a href="#day-{day}" class="nav-card">
                    {birthday_badge}
                    <h3>
                        <span class="th">วันที่ {day}: {title_th}</span>
                        <span class="en">Day {day}: {title_en}</span>
                    </h3>
                    <div class="date">
                        <span class="th">{date_th}</span>
                        <span class="en">{date_en}</span>
                    </div>
                    <div class="desc">
                        <span class="th">{desc_th}</span>
                        <span class="en">{desc_en}</span>
                    </div>
                </a>"""
        
        cards.append(card_html)
    
    return '\n'.join(cards)

if __name__ == "__main__":
    main() rotate(-90deg);
}

.info-detail, .note-detail {
    background: var(--card-bg);
    padding: 1.5rem;
    max-height: 1000px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.info-detail.collapsed, .note-detail.collapsed {
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    margin-top: 0;
}

/* ===== TIMELINE STYLES ===== */
.timeline {
    position: relative;
    list-style: none;
    margin: 2rem 0;
    padding-left: 2rem;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 1rem;
    top: 0;
    bottom: 0;
    width: 2px;
    background: linear-gradient(to bottom, var(--primary), var(--secondary));
}

.timeline li {
    position: relative;
    margin-bottom: 2rem;
    background: var(--card-bg);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    transition: var(--transition);
}

.timeline li:hover {
    transform: translateX(5px);
    box-shadow: var(--shadow-hover);
}

.timeline li::before {
    content: '';
    position: absolute;
    left: -1.5rem;
    top: 1rem;
    width: 12px;
    height: 12px;
    background: var(--accent);
    border-radius: 50%;
    border: 3px solid var(--card-bg);
    box-shadow: 0 0 0 2px var(--primary);
}

.timeline-main {
    padding: 1rem 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border);
}

.timeline-toggle {
    background: var(--primary);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    margin: 0.5rem 1.5rem 1rem 1.5rem;
    border-radius: 20px;
    cursor: pointer;
    font-weight: 500;
    transition: var(--transition);
    font-size: 0.9rem;
}

.timeline-toggle:hover {
    background: var(--secondary);
    transform: scale(1.05);
}

.timeline-toggle.expanded {
    background: var(--success);
}

.timeline-detail {
    padding: 0 1.5rem 1.5rem 1.5rem;
    color: var(--text-secondary);
    border-top: 1px solid var(--border);
    background: #FAFBFC;
}

.timeline-detail h4 {
    color: var(--primary);
    margin: 1rem 0 0.5rem 0;
}

.timeline-detail ul {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
}

.timeline-detail li {
    margin-bottom: 0.3rem;
    position: relative;
    background: none;
    box-shadow: none;
    transform: none;
}

.timeline-detail li::before {
    display: none;
}

/* ===== BACK TO TOP BUTTON ===== */
.back-to-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    cursor: pointer;
    box-shadow: var(--shadow);
    transition: var(--transition);
    z-index: 1000;
    display: none;
}

.back-to-top:hover {
    background: var(--success);
    transform: scale(1.1);
}

.back-to-top.visible {
    display: block;
    animation: fadeInUp 0.3s ease;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 768px) {
    .container {
        padding: 1rem;
    }
    
    .header h1 {
        font-size: 1.8rem;
    }
    
    .header .subtitle {
        font-size: 1rem;
    }
    
    .nav-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .language-switcher {
        position: sticky;
        top: 1rem;
        z-index: 100;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: -1rem -1rem 2rem -1rem;
    }
    
    .timeline {
        padding-left: 1rem;
    }
    
    .timeline::before {
        left: 0.5rem;
    }
    
    .timeline li::before {
        left: -1rem;
    }
    
    .timeline-main {
        padding: 1rem;
    }
    
    .timeline-toggle {
        margin: 0.5rem 1rem 1rem 1rem;
    }
    
    .timeline-detail {
        padding: 0 1rem 1rem 1rem;
    }
}

@media (max-width: 480px) {
    .header {
        padding: 1.5rem 1rem;
    }
    
    .header h1 {
        font-size: 1.5rem;
    }
    
    .content-section {
        padding: 1.5rem;
    }
    
    .nav-card {
        padding: 1rem;
    }
    
    .back-to-top {
        bottom: 1rem;
        right: 1rem;
        width: 45px;
        height: 45px;
    }
}

@media print {
    .language-switcher,
    .back-to-top {
        display: none !important;
    }
    
    .info-detail,
    .note-detail,
    .timeline-detail {
        max-height: none !important;
        display: block !important;
        padding: 1rem !important;
    }
    
    .timeline li {
        break-inside: avoid;
    }
    
    .content-section {
        break-inside: avoid;
        box-shadow: none;
        border: 1px solid var(--border);
    }
}
"""
    padding-left: 2rem;
}

.content-section li {
    margin-bottom: 0.5rem;
    color: var(--text-secondary);
}

/* ===== INFO & NOTE BOXES ===== */
.info-box, .note-box {
    margin: 1.5rem 0;
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: var(--transition);
}

.info-box {
    border-left: 4px solid var(--primary);
}

.note-box {
    border-left: 4px solid var(--accent);
}

.info-toggle, .note-toggle {
    background: linear-gradient(135deg, var(--primary) 0%, #3498DB 100%);
    color: white;
    padding: 1rem;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: var(--transition);
}

.note-toggle {
    background: linear-gradient(135deg, var(--accent) 0%, #F39C12 100%);
}

.info-toggle:hover, .note-toggle:hover {
    transform: translateX(5px);
    box-shadow: var(--shadow);
}

.info-toggle::after, .note-toggle::after {
    content: '▼';
    transition: transform 0.3s ease;
    font-size: 0.9rem;
}

.info-toggle.collapsed::after, .note-toggle.collapsed::after {
    transform: rotate(-90deg);
}

.info-detail, .note-detail {
    background: var(--card-bg);
    padding: 1.5rem;
    max-height: 1000px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.info-detail.collapsed, .note-detail.collapsed {
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    margin-top: 0;
}

/* ===== TIMELINE STYLES ===== */
.timeline {
    position: relative;
    list-style: none;
    margin: 2rem 0;
    padding-left: 2rem;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 1rem;
    top: 0;
    bottom: 0;
    width: 2px;
    background: linear-gradient(to bottom, var(--primary), var(--secondary));
}

.timeline li {
    position: relative;
    margin-bottom: 2rem;
    background: var(--card-bg);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    transition: var(--transition);
}

.timeline li:hover {
    transform: translateX(5px);
    box-shadow: var(--shadow-hover);
}

.timeline li::before {
    content: '';
    position: absolute;
    left: -1.5rem;
    top: 1rem;
    width: 12px;
    height: 12px;
    background: var(--accent);
    border-radius: 50%;
    border: 3px solid var(--card-bg);
    box-shadow: 0 0 0 2px var(--primary);
}

.timeline-main {
    padding: 1rem 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border);
}

.timeline-toggle {
    background: var(--primary);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    margin: 0.5rem 1.5rem 1rem 1.5rem;
    border-radius: 20px;
    cursor: pointer;
    font-weight: 500;
    transition: var(--transition);
    font-size: 0.9rem;
}

.timeline-toggle:hover {
    background: var(--secondary);
    transform: scale(1.05);
}

.timeline-toggle.expanded {
    background: var(--success);
}

.timeline-detail {
    padding: 0 1.5rem 1.5rem 1.5rem;
    color: var(--text-secondary);
    border-top: 1px solid var(--border);
    background: #FAFBFC;
}

.timeline-detail h4 {
    color: var(--primary);
    margin: 1rem 0 0.5rem 0;
}

.timeline-detail ul {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
}

.timeline-detail li {
    margin-bottom: 0.3rem;
    position: relative;
    background: none;
    box-shadow: none;
    transform: none;
}

.timeline-detail li::before {
    display: none;
}

/* ===== BACK TO TOP BUTTON ===== */
.back-to-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    cursor: pointer;
    box-shadow: var(--shadow);
    transition: var(--transition);
    z-index: 1000;
    display: none;
}

.back-to-top:hover {
    background: var(--success);
    transform: scale(1.1);
}

.back-to-top.visible {
    display: block;
    animation: fadeInUp 0.3s ease;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 768px) {
    .container {
        padding: 1rem;
    }
    
    .header h1 {
        font-size: 1.8rem;
    }
    
    .header .subtitle {
        font-size: 1rem;
    }
    
    .nav-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .language-switcher {
        position: sticky;
        top: 1rem;
        z-index: 100;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: -1rem -1rem 2rem -1rem;
    }
    
    .timeline {
        padding-left: 1rem;
    }
    
    .timeline::before {
        left: 0.5rem;
    }
    
    .timeline li::before {
        left: -1rem;
    }
    
    .timeline-main {
        padding: 1rem;
    }
    
    .timeline-toggle {
        margin: 0.5rem 1rem 1rem 1rem;
    }
    
    .timeline-detail {
        padding: 0 1rem 1rem 1rem;
    }
}

@media (max-width: 480px) {
    .header {
        padding: 1.5rem 1rem;
    }
    
    .header h1 {
        font-size: 1.5rem;
    }
    
    .content-section {
        padding: 1.5rem;
    }
    
    .nav-card {
        padding: 1rem;
    }
    
    .back-to-top {
        bottom: 1rem;
        right: 1rem;
        width: 45px;
        height: 45px;
    }
}

/* ===== PRINT STYLES ===== */
@media print {
    .language-switcher,
    .back-to-top {
        display: none !important;
    }
    
    .info-detail,
    .note-detail,
    .timeline-detail {
        max-height: none !important;
        display: block !important;
        padding: 1rem !important;
    }
    
    .timeline li {
        break-inside: avoid;
    }
    
    .content-section {
        break-inside: avoid;
        box-shadow: none;
        border: 1px solid var(--border);
    }
}

/* ===== LOADING ANIMATION ===== */
@keyframes shimmer {
    0% { background-position: -200px 0; }
    100% { background-position: calc(200px + 100%) 0; }
}

.loading {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200px 100%;
    animation: shimmer 1.5s infinite;
}
"""

# ==============================
# JAVASCRIPT - COMPLETE & FUNCTIONAL
# ==============================

def get_fixed_js():
    """JavaScript สมบูรณ์พร้อม timeline expand/collapse ทุกฟีเจอร์"""
    return """
// ===== LANGUAGE SWITCHING =====
function switchLanguage(lang) {
    console.log(`🌐 Switching to language: ${lang}`);
    const body = document.body;
    
    // Remove existing language classes
    body.classList.remove('lang-th', 'lang-en');
    
    // Add new language class
    body.classList.add(`lang-${lang}`);
    
    // Update active button
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const activeBtn = document.querySelector(`[onclick="switchLanguage('${lang}')"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
    
    // Store language preference
    try {
        localStorage.setItem('preferred-language', lang);
    } catch (e) {
        console.warn('LocalStorage not available:', e);
    }
    
    console.log(`✅ Language switched to: ${lang}`);
}

// ===== INFO/NOTE BOXES COLLAPSE =====
function initializeCollapsibleBoxes() {
    console.log('🔧 Initializing collapsible boxes...');
    
    // Info boxes
    const infoBoxes = document.querySelectorAll('.info-box');
    infoBoxes.forEach((box, index) => {
        const toggle = box.querySelector('.info-toggle');
        const detail = box.querySelector('.info-detail');
        
        if (toggle && detail) {
            // Start collapsed
            toggle.classList.add('collapsed');
            detail.classList.add('collapsed');
            
            toggle.addEventListener('click', () => {
                const isCollapsed = detail.classList.contains('collapsed');
                
                if (isCollapsed) {
                    detail.classList.remove('collapsed');
                    toggle.classList.remove('collapsed');
                } else {
                    detail.classList.add('collapsed');
                    toggle.classList.add('collapsed');
                }
                
                console.log(`Info box ${index + 1} ${isCollapsed ? 'expanded' : 'collapsed'}`);
            });
        }
    });
    
    // Note boxes
    const noteBoxes = document.querySelectorAll('.note-box');
    noteBoxes.forEach((box, index) => {
        const toggle = box.querySelector('.note-toggle');
        const detail = box.querySelector('.note-detail');
        
        if (toggle && detail) {
            // Start collapsed
            toggle.classList.add('collapsed');
            detail.classList.add('collapsed');
            
            toggle.addEventListener('click', () => {
                const isCollapsed = detail.classList.contains('collapsed');
                
                if (isCollapsed) {
                    detail.classList.remove('collapsed');
                    toggle.classList.remove('collapsed');
                } else {
                    detail.classList.add('collapsed');
                    toggle.classList.add('collapsed');
                }
                
                console.log(`Note box ${index + 1} ${isCollapsed ? 'expanded' : 'collapsed'}`);
            });
        }
    });
    
    console.log(`✅ Collapsible boxes initialized: ${infoBoxes.length} info, ${noteBoxes.length} note`);
}

// ===== TIMELINE DETAILS EXPAND/COLLAPSE =====
// THE MAGIC FUNCTION FOR TIMELINE DETAILS!
function toggleTimelineDetail(detailId) {
    console.log(`🔄 Toggling timeline detail: ${detailId}`);
    
    const detail = document.getElementById(detailId);
    const button = document.querySelector(`[onclick="toggleTimelineDetail('${detailId}')"]`);
    
    if (!detail) {
        console.warn(`❌ Timeline detail not found: ${detailId}`);
        return;
    }
    
    if (!button) {
        console.warn(`❌ Timeline button not found for: ${detailId}`);
        return;
    }
    
    const isHidden = detail.style.display === 'none' || !detail.style.display;
    
    if (isHidden) {
        // Show detail
        detail.style.display = 'block';
        button.textContent = button.textContent.replace('▼', '▲');
        button.classList.add('expanded');
        console.log(`✅ Expanded: ${detailId}`);
    } else {
        // Hide detail
        detail.style.display = 'none';
        button.textContent = button.textContent.replace('▲', '▼');
        button.classList.remove('expanded');
        console.log(`✅ Collapsed: ${detailId}`);
    }
}

// Make toggleTimelineDetail globally available
window.toggleTimelineDetail = toggleTimelineDetail;

// Initialize timeline toggle functionality
function initializeTimelineToggle() {
    console.log('🔧 Initializing timeline toggle...');
    
    // Find all timeline detail elements and hide them initially
    const timelineDetails = document.querySelectorAll('.timeline-detail');
    timelineDetails.forEach(detail => {
        detail.style.display = 'none';
    });
    
    // Verify toggle buttons exist
    const toggleButtons = document.querySelectorAll('.timeline-toggle');
    console.log(`📊 Found ${timelineDetails.length} timeline details and ${toggleButtons.length} toggle buttons`);
    
    // Test function availability
    if (typeof window.toggleTimelineDetail === 'function') {
        console.log('✅ toggleTimelineDetail function is globally available');
    } else {
        console.error('❌ toggleTimelineDetail function is NOT globally available');
    }
    
    console.log(`✅ Timeline toggle initialized for ${timelineDetails.length} details`);
}

// ===== SMOOTH SCROLLING =====
function initializeSmoothScrolling() {
    console.log('🔧 Initializing smooth scrolling...');
    
    // Find all internal links (links starting with #)
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    
    internalLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                console.log(`📍 Scrolled to: ${targetId}`);
            } else {
                console.warn(`❌ Target element not found: ${targetId}`);
            }
        });
    });
    
    console.log(`✅ Smooth scrolling initialized for ${internalLinks.length} internal links`);
}

// ===== BACK TO TOP BUTTON =====
function initializeBackToTop() {
    console.log('🔧 Initializing back to top button...');
    
    // Create back to top button if it doesn't exist
    let backToTopBtn = document.querySelector('.back-to-top');
    
    if (!backToTopBtn) {
        backToTopBtn = document.createElement('button');
        backToTopBtn.className = 'back-to-top';
        backToTopBtn.innerHTML = '↑';
        backToTopBtn.title = 'กลับไปหน้าหลัก';
        document.body.appendChild(backToTopBtn);
    }
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });
    
    // Click handler for back to top
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        console.log('📍 Scrolled to top');
    });
    
    console.log('✅ Back to top button initialized');
}

// ===== CURRENCY DISPLAY =====
function updateCurrencyDisplay() {
    console.log('🔧 Updating currency display...');
    
    // Find all currency elements and format them nicely
    const currencyElements = document.querySelectorAll('.currency, .price, .cost');
    
    currencyElements.forEach(element => {
        const text = element.textContent;
        // Add comma separators to numbers
        const formatted = text.replace(/\d+/g, (match) => {
            return parseInt(match).toLocaleString();
        });
        element.textContent = formatted;
    });
    
    console.log(`✅ Currency display updated for ${currencyElements.length} elements`);
}

// ===== MAIN INITIALIZATION =====
function initializeApp() {
    console.log('🚀 Initializing Tokyo Trip Guide...');
    
    try {
        // Initialize all features
        initializeCollapsibleBoxes();
        initializeTimelineToggle();  // ⭐ CRITICAL: Timeline functionality
        initializeSmoothScrolling();
        initializeBackToTop();
        updateCurrencyDisplay();
        
        // Set default language to Thai
        switchLanguage('th');
        
        console.log('🎉 Tokyo Trip Guide initialized successfully!');
        
    } catch (error) {
        console.error('💥 Failed to initialize app:', error);
    }
}

// ===== DOM READY =====
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    // DOM is already ready
    initializeApp();
}

// Make functions globally available
window.switchLanguage = switchLanguage;
window.debugTimeline = function() {
    console.log('🔍 Debug: Timeline functionality check');
    
    const timelineDetails = document.querySelectorAll('.timeline-detail');
    const timelineButtons = document.querySelectorAll('.timeline-toggle');
    
    console.log(`Timeline details found: ${timelineDetails.length}`);
    console.log(`Timeline buttons found: ${timelineButtons.length}`);
    
    timelineButtons.forEach((button, index) => {
        const onclick = button.getAttribute('onclick');
        console.log(`Button ${index + 1}: ${onclick}`);
    });
    
    console.log(`toggleTimelineDetail function: ${typeof window.toggleTimelineDetail}`);
};

console.log('📱 Tokyo Trip Guide JavaScript loaded successfully!');
"""

# ==============================
# OVERVIEW CARDS GENERATOR
# ==============================

def generate_overview_cards():
    """สร้าง overview cards ครบ 8 วัน พร้อม birthday badge วันที่ 4"""
    
    # ข้อมูลแต่ละวัน
    days_data = [
        {
            "day": 1,
            "date": "6 มีนาคม 2026",
            "date_en": "March 6, 2026",
            "title_th": "เดินทางสู่โตเกียว",
            "title_en": "Journey to Tokyo",
            "desc_th": "เดินทางจากกรุงเทพไปโตเกียว เช็คอินโรงแรม เดินเล่นรอบชิบุยะ",
            "desc_en": "Flight from Bangkok to Tokyo, hotel check-in, explore Shibuya district",
            "birthday": False
        },
        {
            "day": 2,
            "date": "7 มีนาคม 2026",
            "date_en": "March 7, 2026",
            "title_th": "อาซากุซา และวัดเซนโซจิ",
            "title_en": "Asakusa & Sensoji Temple",
            "desc_th": "เยี่ยมชมวัดเก่าแก่ ชมยานนากามิเซ",
            "desc_en": "Visit ancient temples, experience traditional Tokyo, Nakamise shopping street",
            "birthday": False
        },
        {
            "day": 3,
            "date": "8 มีนาคม 2026",
            "date_en": "March 8, 2026",
            "title_th": "อุเอโนะ และฮาราจุกุ",
            "title_en": "Ueno & Harajuku",
            "desc_th": "สวนอุเอโนะ และย่านแฟชั่นเทรนดี้ของฮาราจุกุ",
            "desc_en": "Ueno Park and Zoo, trendy Harajuku fashion district",
            "birthday": False
        },
        {
            "day": 4,
            "date": "9 มีนาคม 2026",
            "date_en": "March 9, 2026",
            "title_th": "วันเกิดปอยไจ่",
            "title_en": "Pojai's Birthday!",
            "desc_th": "วันพิเศษปอยไจ่! ดิสนีย์แลนด์ และกิจกรรมพิเศษ",
            "desc_en": "Special birthday celebration! DisneySea and birthday activities",
            "birthday": True
        },
        {
            "day": 5,
            "date": "10 มีนาคม 2026",
            "date_en": "March 10, 2026",
            "title_th": "ชิบุยะ และช้อปปิ้ง",
            "title_en": "Shibuya & Shopping",
            "desc_th": "เดินชิบุยะ ช้อปปิ้งซื้อของฝาก",
            "desc_en": "Explore Shibuya, shopping for souvenirs and gifts",
            "birthday": False
        },
        {
            "day": 6,
            "date": "11 มีนาคม 2026",
            "date_en": "March 11, 2026",
            "title_th": "ฟูจิ-คิว ไฮแลนด์",
            "title_en": "Fuji-Q Highland",
            "desc_th": "สวนสนุกฟูจิ-คิว ไฮแลนด์ ชมภูเขาไฟฟูจิ",
            "desc_en": "Fuji-Q Highland theme park, Mount Fuji views",
            "birthday": False
        },
        {
            "day": 7,
            "date": "12 มีนาคม 2026",
            "date_en": "March 12, 2026",
            "title_th": "โอไดบะ และ ท่าอากาศยาน",
            "title_en": "Odaiba & Airport",
            "desc_th": "เที่ยวโอไดบะ ช้อปปิ้งครั้งสุดท้าย เตรียมเดินทางกลับ",
            "desc_en": "Odaiba sightseeing, last-minute shopping, prepare for departure",
            "birthday": False
        },
        {
            "day": 8,
            "date": "13 มีนาคม 2026",
            "date_en": "March 13, 2026",
            "title_th": "เดินทางกลับบ้าน",
            "title_en": "Journey Home",
            "desc_th": "เดินทางกลับจากโตเกียวสู่กรุงเทพฯ",
            "desc_en": "Flight from Tokyo back to Bangkok",
            "birthday": False
        }
    ]
    
    html_cards = []
    
    for day_info in days_data:
        birthday_badge = ''
        if day_info['birthday']:
            birthday_badge = '<div class="birthday-badge">🎂 วันเกิด!</div>'
        
        card_html = f"""
        <a href="#day-{day_info['day']}" class="nav-card">
            {birthday_badge}
            <h3>
                <span class="th">วันที่ {day_info['day']}: {day_info['title_th']}</span>
                <span class="en">Day {day_info['day']}: {day_info['title_en']}</span>
            </h3>
            <div class="date">
                <span class="th">{day_info['date']}</span>
                <span class="en">{day_info['date_en']}</span>
            </div>
            <div class="desc">
                <span class="th">{day_info['desc_th']}</span>
                <span class="en">{day_info['desc_en']}</span>
            </div>
        </a>"""
        
        html_cards.append(card_html)
    
    return '\n'.join(html_cards)

# ==============================
# MARKDOWN TO HTML CONVERTER
# ==============================

def convert_markdown_to_html(markdown_content):
    """แปลง markdown เป็น HTML พร้อม info/note boxes และ timeline processing"""
    
    html_content = markdown_content
    
    # Convert headers
    html_content = re.sub(r'^### (.+)

, r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)

, r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)

, r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    
    # Convert info boxes: > **Title** | **Title EN**
    def convert_info_box(match):
        title_th = match.group(1)
        title_en = match.group(2) if match.group(2) else title_th
        content = match.group(3)
        
        return f"""
<div class="info-box">
    <div class="info-toggle">
        <span class="th">{title_th}</span>
        <span class="en">{title_en}</span>
    </div>
    <div class="info-detail">
        {content}
    </div>
</div>"""
    
    html_content = re.sub(
        r'^> \*\*(.+?)\*\*(?: \| \*\*(.+?)\*\*)?\n([\s\S]*?)(?=\n\n|\n> |$)', 
        convert_info_box, 
        html_content, 
        flags=re.MULTILINE
    )
    
    # Convert note boxes: 📝 **Title** | **Title EN**
    def convert_note_box(match):
        title_th = match.group(1)
        title_en = match.group(2) if match.group(2) else title_th
        content = match.group(3)
        
        return f"""
<div class="note-box">
    <div class="note-toggle">
        <span class="th">{title_th}</span>
        <span class="en">{title_en}</span>
    </div>
    <div class="note-detail">
        {content}
    </div>
</div>"""
    
    html_content = re.sub(
        r'^📝 \*\*(.+?)\*\*(?: \| \*\*(.+?)\*\*)?\n([\s\S]*?)(?=\n\n|\n📝 |$)', 
        convert_note_box, 
        html_content, 
        flags=re.MULTILINE
    )
    
    # Convert bold and italic text
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)
    
    # Convert lists
    html_content = re.sub(r'^- (.+)

, r'<li>\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'</ul>\s*<ul>', '', html_content)
    
    # Convert line breaks
    html_content = re.sub(r'\n\n', '</p><p>', html_content)
    html_content = f'<p>{html_content}</p>'
    
    # Clean up empty paragraphs
    html_content = re.sub(r'<p>\s*</p>', '', html_content)
    
    return html_content

# ==============================
# TIMELINE PROCESSING
# ==============================

def process_timeline_content(content):
    """ประมวลผล timeline content เพื่อเพิ่ม expand/collapse buttons"""
    
    timeline_counter = 0
    
    def add_timeline_button(match):
        nonlocal timeline_counter
        timeline_counter += 1
        
        time_text = match.group(1)
        detail_id = f"timeline-{timeline_counter}"
        
        return f"""
    <li>
        <div class="timeline-main">{time_text}</div>
        <button class="timeline-toggle" onclick="toggleTimelineDetail('{detail_id}')">
            <span class="th">รายละเอียด ▼</span>
            <span class="en">Details ▼</span>
        </button>
        <div class="timeline-detail" id="{detail_id}" style="display: none;">
"""
    
    # หา timeline items และเพิ่ม buttons
    content = re.sub(
        r'<li>(.+?)</li>',
        lambda m: add_timeline_button(m) + m.group(1) + '</div></li>',
        content,
        flags=re.DOTALL
    )
    
    return content

# ==============================
# CONTENT FILES READER
# ==============================

def read_content_files():
    """อ่านไฟล์ content ทั้งหมดจาก content folder"""
    
    content_files = {
        'overview': '',
        'day1': '',
        'day2': '',
        'day3': '',
        'day4': '',
        'day5': '',
        'day6': '',
        'day7': '',
        'day8': '',
        'budget': '',
        'tips': ''
    }
    
    print(f"📂 Reading content files from: {CONTENT_DIR}")
    
    if not CONTENT_DIR.exists():
        print(f"❌ Content directory not found: {CONTENT_DIR}")
        return content_files

if __name__ == "__main__":
    main()

# ==============================
# MAIN HTML GENERATOR
# ==============================

def generate_html():
    """สร้าง HTML ไฟล์สมบูรณ์สำหรับทริปโตเกียว"""
    
    print(f"🎆 Starting HTML generation...")
    
    # อ่านไฟล์ content ทั้งหมด
    content_files = read_content_files()
    
    # สร้าง overview cards
    overview_cards = generate_overview_cards()
    
    # เตรียม timestamp สำหรับ filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    
    # HTML template หลัก
    html_template = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ทริปโตเกียว มีนาคม 2026 - พ่อลูกเที่ยวรู้</title>
    <meta name="description" content="คู่มือทริปโตเกียว 8 วัน 7 คืน สำหรับพ่อลูก - Arilek & Pojai">
    <style>
{get_fixed_css()}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>
                <span class="th">ทริปโตเกียว มีนาคม 2026</span>
                <span class="en">Tokyo Trip March 2026</span>
            </h1>
            <div class="subtitle">
                <span class="th">8 วัน 7 คืน พ่อลูกเที่ยวรู้ - Arilek & Pojai</span>
                <span class="en">8 Days 7 Nights Father-Daughter Adventure - Arilek & Pojai</span>
            </div>
            
            <!-- LANGUAGE SWITCHER -->
            <div class="language-switcher">
                <button class="lang-btn" onclick="switchLanguage('th')">TH</button>
                <button class="lang-btn" onclick="switchLanguage('en')">EN</button>
            </div>
        </div>
        
        <!-- OVERVIEW SECTION -->
        <div class="nav-section">
            <h2>
                <span class="th">ภาพรวมการเดินทาง</span>
                <span class="en">Trip Overview</span>
            </h2>
            <div class="nav-grid">
{overview_cards}
            </div>
        </div>
"""
    
    # เพิ่ม content แต่ละส่วน
    content_sections = []
    
    # Overview section
    if content_files.get('overview'):
        overview_html = convert_markdown_to_html(content_files['overview'])
        content_sections.append(f"""
        <div class="content-section" id="overview">
            <h2>
                <span class="th">ข้อมูลทั่วไป</span>
                <span class="en">General Information</span>
            </h2>
            {overview_html}
        </div>""")
    
    # Day sections
    for day_num in range(1, 9):
        day_key = f'day{day_num}'
        if content_files.get(day_key):
            day_html = convert_markdown_to_html(content_files[day_key])
            day_html = process_timeline_content(day_html)  # เพิ่ม timeline buttons
            
            content_sections.append(f"""
        <div class="content-section" id="day-{day_num}">
            <h2>
                <span class="th">วันที่ {day_num}</span>
                <span class="en">Day {day_num}</span>
            </h2>
            {day_html}
        </div>""")
    
    # Budget section
    if content_files.get('budget'):
        budget_html = convert_markdown_to_html(content_files['budget'])
        content_sections.append(f"""
        <div class="content-section" id="budget">
            <h2>
                <span class="th">งบประมาณ</span>
                <span class="en">Budget</span>
            </h2>
            {budget_html}
        </div>""")
    
    # Tips section
    if content_files.get('tips'):
        tips_html = convert_markdown_to_html(content_files['tips'])
        content_sections.append(f"""
        <div class="content-section" id="tips">
            <h2>
                <span class="th">เคล็ดลับและข้อแนะนำ</span>
                <span class="en">Tips & Recommendations</span>
            </h2>
            {tips_html}
        </div>""")
    
    # ลิสต์ไฟล์ที่มีอยู่
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith('.md'):
            file_path = CONTENT_DIR / filename
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # กำหนด key จากชื่อไฟล์
                filename_lower = filename.lower()
                if 'overview' in filename_lower:
                    content_files['overview'] = content
                elif 'day-1' in filename_lower or 'day1' in filename_lower:
                    content_files['day1'] = content
                elif 'day-2' in filename_lower or 'day2' in filename_lower:
                    content_files['day2'] = content
                elif 'day-3' in filename_lower or 'day3' in filename_lower:
                    content_files['day3'] = content
                elif 'day-4' in filename_lower or 'day4' in filename_lower:
                    content_files['day4'] = content
                elif 'day-5' in filename_lower or 'day5' in filename_lower:
                    content_files['day5'] = content
                elif 'day-6' in filename_lower or 'day6' in filename_lower:
                    content_files['day6'] = content
                elif 'day-7' in filename_lower or 'day7' in filename_lower:
                    content_files['day7'] = content
                elif 'day-8' in filename_lower or 'day8' in filename_lower:
                    content_files['day8'] = content
                elif 'budget' in filename_lower:
                    content_files['budget'] = content
                elif 'tips' in filename_lower:
                    content_files['tips'] = content
                
                print(f"✅ Read: {filename} ({len(content)} chars)")
                
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")
    
    # ตรวจสอบว่าไฟล์สำคัญครบหรือไม่
    loaded_files = [key for key, content in content_files.items() if content]
    missing_files = [key for key, content in content_files.items() if not content]
    
    print(f"✅ Loaded files: {', '.join(loaded_files)}")
    if missing_files:
        print(f"⚠️ Missing files: {', '.join(missing_files)}")
        print(f"📝 Available files in {CONTENT_DIR}:")
        for filename in os.listdir(CONTENT_DIR):
            print(f"   - {filename}")
    
    return content_files

