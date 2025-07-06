#!/usr/bin/env python3
"""
🔧 Simple Python Syntax Fixer
แก้ไข syntax errors แบบง่ายๆ
"""

import re
import os
from pathlib import Path

def fix_python_syntax_errors(file_path):
    """แก้ไข syntax errors ที่พบบ่อย"""
    
    print(f"🔧 Fixing syntax errors in: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Simple find and replace for orphaned ", line)"
    # แก้ไขทีละบรรทัด
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # ถ้าเจอบรรทัดที่ลงท้ายด้วย single quote และบรรทัดถัดไปเป็น ", line)"
        if (i < len(lines) - 1 and 
            line.strip().endswith("'") and 
            lines[i + 1].strip() == ", line)"):
            
            # รวมสองบรรทัดเป็นบรรทัดเดียว
            combined_line = line + ", line)"
            fixed_lines.append(combined_line)
            i += 2  # ข้ามบรรทัดถัดไป
            print(f"✅ Fixed line {i}: Combined regex pattern")
            
        elif line.strip() == ", line)":
            # ข้ามบรรทัดที่เหลือแค่ ", line)" โดดๆ
            print(f"⚠️  Skipped orphaned line {i + 1}: {line.strip()}")
            i += 1
            
        else:
            fixed_lines.append(line)
            i += 1
    
    # รวมบรรทัดกลับเป็น string
    content = '\n'.join(fixed_lines)
    
    if content != original_content:
        # สร้างไฟล์ backup
        backup_path = str(file_path) + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"📦 Backup saved: {backup_path}")
        
        # เขียนไฟล์ที่แก้ไขแล้ว
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed syntax errors!")
        return True
    else:
        print("ℹ️  No syntax errors found.")
        return False

def main():
    """แก้ไขไฟล์"""
    script_dir = Path(__file__).parent
    target_file = script_dir / "claude-tokyo_trip_generator-final-20250618.py"
    
    if target_file.exists():
        success = fix_python_syntax_errors(target_file)
        if success:
            print(f"🎯 Try running the file again!")
            print(f"python {target_file.name}")
        else:
            print("🤔 File might have other issues. Check manually.")
    else:
        print(f"❌ File not found: {target_file}")

if __name__ == "__main__":
    main()
