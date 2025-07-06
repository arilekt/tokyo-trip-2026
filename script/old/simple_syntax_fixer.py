#!/usr/bin/env python3
"""
🔧 SIMPLE BUT EFFECTIVE SYNTAX FIXER
แก้ไข syntax errors แบบง่ายๆ ไม่ใช้ regex ซับซ้อน
"""

import os
from pathlib import Path

def simple_fix_python_syntax(file_path):
    """แก้ไข syntax errors แบบง่ายๆ"""
    
    print(f"🔧 Simple fixing syntax errors in: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    fixes_count = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Fix 1: หาบรรทัดที่ลงท้ายด้วย single quote แล้วบรรทัดถัดไปเป็น , line)
        if (i < len(lines) - 1 and 
            line.strip().endswith("'") and 
            "re.match" in line and
            lines[i + 1].strip() == ", line)"):
            
            # รวมสองบรรทัดเป็นบรรทัดเดียว
            combined_line = line + ", line)"
            fixed_lines.append(combined_line)
            print(f"✅ Fixed line {i+1}: Combined regex pattern")
            fixes_count += 1
            i += 2  # ข้ามบรรทัดถัดไป
            continue
            
        # Fix 2: หาบรรทัดที่มี re.match แต่ไม่มี closing
        elif (i < len(lines) - 1 and
              "re.match(r'" in line and 
              not line.endswith(", line)") and
              not line.endswith("')") and
              ", line)" in lines[i + 1]):
            
            combined_line = line + ", line)"
            fixed_lines.append(combined_line)
            print(f"✅ Fixed line {i+1}: Added missing , line)")
            fixes_count += 1
            i += 2
            continue
        
        # Fix 3: ลบบรรทัดที่เหลือแค่ , line) โดดๆ
        elif line.strip() == ", line)":
            print(f"⚠️  Removed orphaned line {i+1}: {line.strip()}")
            fixes_count += 1
            i += 1
            continue
        
        # Fix 4: แก้ไข specific broken patterns ที่รู้จัก
        elif "match = re.match(r'- \\*\\*([^*]+)\\*\\*:\\s*(.*)'" in line and not line.endswith(", line)"):
            fixed_line = line + ", line)"
            fixed_lines.append(fixed_line)
            print(f"✅ Fixed line {i+1}: Added missing , line) to timeline pattern")
            fixes_count += 1
            i += 1
            continue
            
        # Fix 5: header_match specific
        elif "header_match = re.match(r'^(#{1,6})\\s+(.+)'" in line and not line.endswith(", line)"):
            fixed_line = line + ", line)"
            fixed_lines.append(fixed_line)
            print(f"✅ Fixed line {i+1}: Added missing , line) to header pattern")
            fixes_count += 1
            i += 1
            continue
        
        else:
            # บรรทัดปกติ ไม่ต้องแก้
            fixed_lines.append(line)
            i += 1
    
    # รวมบรรทัดกลับเป็น string
    new_content = '\n'.join(fixed_lines)
    
    if new_content != original_content or fixes_count > 0:
        # สร้างไฟล์ backup
        backup_path = str(file_path) + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"📦 Backup saved: {backup_path}")
        
        # เขียนไฟล์ที่แก้ไขแล้ว
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"🎉 Fixed {fixes_count} syntax errors!")
        return True
    else:
        print("ℹ️  No syntax errors found to fix.")
        return False

def validate_python_syntax(file_path):
    """ตรวจสอบว่าไฟล์ Python มี syntax error หรือไม่"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ลองคอมไพล์
        compile(content, file_path, 'exec')
        print("✅ Python syntax validation: PASSED")
        return True
    except SyntaxError as e:
        print(f"❌ Python syntax error still exists:")
        print(f"   Line {e.lineno}: {e.text.strip() if e.text else 'N/A'}")
        print(f"   Error: {e.msg}")
        return False
    except Exception as e:
        print(f"⚠️  Other error during validation: {e}")
        return False

def show_problem_lines(file_path):
    """แสดงบรรทัดที่มีปัญหา"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"🔍 Checking for common problems...")
        problems = []
        
        for i, line in enumerate(lines, 1):
            # หาบรรทัดที่มี , line) โดดๆ
            if line.strip() == ", line)":
                problems.append(f"Line {i}: Orphaned ', line)'")
            
            # หา regex ที่ไม่สมบูรณ์
            elif "re.match(r'" in line and not line.strip().endswith(", line)") and not line.strip().endswith("')"):
                problems.append(f"Line {i}: Incomplete regex: {line.strip()[:50]}...")
        
        if problems:
            print(f"Found {len(problems)} potential problems:")
            for problem in problems[:5]:  # แสดงแค่ 5 อันแรก
                print(f"  - {problem}")
        else:
            print("No obvious problems found.")
            
    except Exception as e:
        print(f"Error checking file: {e}")

def main():
    """แก้ไขไฟล์แล้วตรวจสอบ"""
    script_dir = Path(__file__).parent
    target_file = script_dir / "claude-tokyo_trip_generator-final-20250618.py"
    
    if not target_file.exists():
        print(f"❌ File not found: {target_file}")
        return
    
    print("🔧 Starting simple syntax fixing...")
    
    # แสดงปัญหาที่เจอ
    show_problem_lines(target_file)
    
    # แก้ไข
    success = simple_fix_python_syntax(target_file)
    
    # ตรวจสอบ syntax
    print("\n🔍 Validating Python syntax...")
    if validate_python_syntax(target_file):
        print("🎉 SUCCESS! File is now syntactically correct!")
        print(f"🚀 Try running: python {target_file.name}")
    else:
        print("😔 Still has syntax errors.")
        print("🔄 You may need to check the file manually.")

if __name__ == "__main__":
    main()
