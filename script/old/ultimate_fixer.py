#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokyo Trip 2026 - Ultimate Expand/Collapse Fixer
================================================
แก้ไขปัญหา expand/collapse ที่ไม่ทำงาน โดยใช้วิธีง่าย ๆ ที่ได้ผลจริง

Author: Claude (AI Assistant) 
Date: June 2025
Version: Ultimate Fixer
For: Arilek & Pojai's Tokyo Trip 2026
"""

import os
import re
import datetime
from pathlib import Path


class UltimateFixer:
    """แก้ไข expand/collapse ให้ทำงานได้"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.build_dir = self.script_dir.parent / "build"
    
    def get_fixed_css(self) -> str:
        """CSS ที่ทำงานได้จริง"""
        return """
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
            max-height: 3000px;
            margin-top: 0.5rem;
        }

        .info-detail.collapsed, .note-detail.collapsed {
            max-height: 0;
            margin-top: 0;
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
        }

        .back-to-top:hover {
            background: var(--primary-dark);
            transform: translateY(-2px);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container { padding: 0.5rem; }
            header { padding: 1rem; }
            header h1 { font-size: 1.5rem; }
            section { padding: 1rem; }
            .day-overviews { grid-template-columns: 1fr; }
            .lang-switcher, .language-switcher { top: 0.5rem; right: 0.5rem; }
            .back-to-top { bottom: 1rem; right: 1rem; padding: 0.75rem; }
        }
        """

    def get_fixed_js(self) -> str:
        """JavaScript ที่ทำงานได้จริง"""
        return """
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
            
            console.log(`Language switched to: ${lang}`);
        }

        // THE MAGIC FUNCTION THAT MAKES EXPAND/COLLAPSE WORK
        function initializeCollapsibleBoxes() {
            console.log('🔧 Initializing collapsible boxes...');
            
            const toggles = document.querySelectorAll('.info-toggle, .note-toggle');
            console.log(`Found ${toggles.length} toggle elements`);
            
            toggles.forEach((toggle, index) => {
                // Start collapsed
                toggle.classList.add('collapsed');
                const detail = toggle.nextElementSibling;
                
                if (detail && (detail.classList.contains('info-detail') || detail.classList.contains('note-detail'))) {
                    detail.classList.add('collapsed');
                    
                    console.log(`Setting up toggle ${index + 1}`);
                    
                    // Remove any existing click handlers
                    toggle.replaceWith(toggle.cloneNode(true));
                    const newToggle = document.querySelectorAll('.info-toggle, .note-toggle')[index];
                    const newDetail = newToggle.nextElementSibling;
                    
                    newToggle.addEventListener('click', function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        const isCollapsed = newDetail.classList.contains('collapsed');
                        
                        console.log(`Toggle clicked: ${isCollapsed ? 'expanding' : 'collapsing'}`);
                        
                        if (isCollapsed) {
                            newDetail.classList.remove('collapsed');
                            newToggle.classList.remove('collapsed');
                        } else {
                            newDetail.classList.add('collapsed');
                            newToggle.classList.add('collapsed');
                        }
                    });
                } else {
                    console.warn(`No matching detail element for toggle ${index + 1}`);
                }
            });
            
            console.log('✅ Collapsible boxes initialized!');
        }

        // THE MAGIC FUNCTION FOR TIMELINE DETAILS EXPAND/COLLAPSE
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
                console.log(`Timeline detail expanded: ${detailId}`);
            } else {
                detail.style.display = 'none';
                button.textContent = button.textContent.replace('▲', '▼');
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
            }
        }

        // Currency conversion
        function updateCurrencyDisplay() {
            const yenToThb = 0.23;
            const yenElements = document.querySelectorAll('[data-yen]');
            
            yenElements.forEach(element => {
                const yenAmount = parseInt(element.dataset.yen);
                if (!isNaN(yenAmount)) {
                    const thbAmount = Math.round(yenAmount * yenToThb);
                    element.textContent = `¥${yenAmount.toLocaleString()} (฿${thbAmount.toLocaleString()})`;
                }
            });
        }

        // Main initialization
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🇯🇵 Tokyo Trip 2026 Ultimate Fixer - Loading...');
            
            // Language setup
            try {
                const savedLang = localStorage.getItem('tokyo-trip-lang');
                if (savedLang && (savedLang === 'th' || savedLang === 'en')) {
                    switchLanguage(savedLang);
                } else {
                    switchLanguage('th');
                }
            } catch (e) {
                switchLanguage('th');
            }
            
            // Setup language switcher buttons
            document.querySelectorAll('[data-lang]').forEach(btn => {
                btn.addEventListener('click', function() {
                    switchLanguage(this.getAttribute('data-lang'));
                });
            });
            
            // Initialize all features
            initializeCollapsibleBoxes();
            initializeTimelineToggle();
            initializeSmoothScrolling();
            initializeBackToTop();
            updateCurrencyDisplay();
            
            // Debug info
            const infoBoxes = document.querySelectorAll('.info-box, .note-box');
            const toggles = document.querySelectorAll('.info-toggle, .note-toggle');
            console.log(`📊 Found ${infoBoxes.length} info/note boxes, ${toggles.length} toggles`);
            
            console.log('✅ Tokyo Trip 2026 Ultimate Fixer - READY WITH WORKING EXPAND/COLLAPSE!');
        });
        """

    def find_latest_html(self) -> Path:
        """หาไฟล์ HTML ล่าสุด"""
        html_files = list(self.build_dir.glob("Tokyo-Trip-March-2026-*.html"))
        
        if not html_files:
            raise FileNotFoundError("❌ No HTML files found to fix!")
        
        latest = max(html_files, key=lambda f: f.stat().st_mtime)
        print(f"📖 Found latest file: {latest.name}")
        return latest

    def fix_html_file(self, html_path: Path) -> str:
        """แก้ไขไฟล์ HTML ให้ทำงานได้"""
        print(f"🔧 Fixing {html_path.name}...")
        
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace CSS
        css_pattern = r'<style>(.*?)</style>'
        new_css = f"<style>{self.get_fixed_css()}</style>"
        content = re.sub(css_pattern, new_css, content, flags=re.DOTALL)
        print("✅ Fixed CSS")
        
        # Replace JavaScript  
        js_pattern = r'<script>(.*?)</script>'
        new_js = f"<script>{self.get_fixed_js()}</script>"
        content = re.sub(js_pattern, new_js, content, flags=re.DOTALL)
        print("✅ Fixed JavaScript")
        
        # Fix language switcher buttons
        content = re.sub(
            r'<button[^>]*data-lang="th"[^>]*>',
            '<button data-lang="th" class="active">',
            content
        )
        content = re.sub(
            r'<button[^>]*data-lang="en"[^>]*>',
            '<button data-lang="en">',
            content
        )
        print("✅ Fixed language switcher")
        
        return content

    def save_fixed_file(self, content: str) -> Path:
        """บันทึกไฟล์ที่แก้ไขแล้ว"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        filename = f"Tokyo-Trip-March-2026-FIXED-{timestamp}.html"
        output_path = self.build_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Saved fixed file: {output_path}")
        return output_path

    def run(self):
        """รันการแก้ไข"""
        print("🇯🇵 Tokyo Trip 2026 - Ultimate Expand/Collapse Fixer")
        print("=" * 60)
        print("🎯 Mission: Fix the broken expand/collapse functionality")
        print()
        
        try:
            # หาไฟล์ล่าสุด
            latest_html = self.find_latest_html()
            
            # แก้ไข
            fixed_content = self.fix_html_file(latest_html)
            
            # บันทึก
            output_path = self.save_fixed_file(fixed_content)
            
            print()
            print("🎉 MISSION ACCOMPLISHED!")
            print(f"📄 Fixed file: {output_path}")
            print(f"📊 Size: {len(fixed_content):,} characters")
            print()
            print("✅ What's fixed:")
            print("   🔧 Expand/collapse info boxes (NOW WORKING)")
            print("   🌐 Language switching (TH/EN)")
            print("   📱 Mobile responsive")
            print("   🔄 Smooth scrolling")
            print("   💱 Currency conversion")
            print()
            print("🚀 Open the HTML file and test the expand/collapse!")
            print("   Try clicking on the blue info box headers")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    fixer = UltimateFixer()
    fixer.run()
