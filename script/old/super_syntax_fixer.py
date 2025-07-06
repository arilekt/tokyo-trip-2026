#!/usr/bin/env python3
"""
🚀 SUPER PYTHON SYNTAX FIXER
แก้ไข syntax errors ทุกแบบ รวมถึง regex ที่เสีย
"""

import re
import os
from pathlib import Path

def super_fix_python_syntax(file_path):
    """แก้ไข syntax errors แบบครอบจักรวาล"""
    
    print(f"🚀 SUPER FIXING syntax errors in: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    fixes_count = 0
    
    while i < len(lines):
        line = lines[i]
        original_line = line
        
        # Fix 1: Regex ที่ขาด closing parenthesis
        if 'match = re.match(r\'' in line and not line.count('(') == line.count(')'):
            # หาบรรทัดถัดไปที่มี , line)
            if i < len(lines) - 1 and ', line)' in lines[i + 1]:
                # รวมบรรทัด
                combined = line + ', line)'
                fixed_lines.append(combined)
                print(f"✅ Fix 1 - Line {i+1}: Combined regex pattern")
                fixes_count += 1
                i += 2
                continue
        
        # Fix 2: header_match regex ที่ขาด closing
        if 'header_match = re.match(r\'' in line and not line.endswith(', line)'):
            if i < len(lines) - 1 and lines[i + 1].strip() == ', line)':
                combined = line + ', line)'
                fixed_lines.append(combined)
                print(f"✅ Fix 2 - Line {i+1}: Fixed header_match regex")
                fixes_count += 1
                i += 2
                continue
        
        # Fix 3: ลบบรรทัดที่เหลือแค่ , line) โดดๆ
        if line.strip() == ', line)':
            print(f"⚠️  Skipped orphaned line {i+1}: {line.strip()}")
            fixes_count += 1
            i += 1
            continue
        
        # Fix 4: แก้ไข regex patterns ที่เสียอื่นๆ
        if 're.match(r\'' in line and line.count('\'') == 1:
            # ขาด closing quote
            if i < len(lines) - 1 and lines[i + 1].strip().startswith(', line)'):
                combined = line + '\', line)'
                fixed_lines.append(combined)
                print(f"✅ Fix 4 - Line {i+1}: Added missing quote")
                fixes_count += 1
                i += 2
                continue
        
        # Fix 5: แก้ไข specific patterns ที่เจอ
        fixes = [
            # Pattern 1: Timeline regex
            (r'match = re\.match\(r\'- \\*\\*\(\[^*\]\+\)\\*\\*:\\s\*\(\.\*\)\'$',
             r'match = re.match(r\'- \\*\\*([^*]+)\\*\\*:\\s*(.*)\', line)'),
            
            # Pattern 2: Header regex  
            (r'header_match = re\.match\(r\'\^\(#\{1,6\}\)\\s\+\(\.\+\)\'$',
             r'header_match = re.match(r\'^(#{1,6})\\s+(.+)\', line)'),
        ]
        
        modified = False
        for pattern, replacement in fixes:
            if re.search(pattern, line):
                line = re.sub(pattern, replacement, line)
                print(f"✅ Fix 5 - Line {i+1}: Applied pattern fix")
                fixes_count += 1
                modified = True
                break
        
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
        
        print(f"🎉 SUPER FIXED {fixes_count} syntax errors!")
        return True
    else:
        print("ℹ️  No syntax errors found.")
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
        print(f"❌ Python syntax error found:")
        print(f"   Line {e.lineno}: {e.text}")
        print(f"   Error: {e.msg}")
        return False
    except Exception as e:
        print(f"⚠️  Other error: {e}")
        return False

def main():
    """แก้ไขไฟล์แล้วตรวจสอบ"""
    script_dir = Path(__file__).parent
    target_file = script_dir / "claude-tokyo_trip_generator-final-20250618.py"
    
    if not target_file.exists():
        print(f"❌ File not found: {target_file}")
        return
    
    print("🔧 Starting SUPER syntax fixing...")
    
    # แก้ไขครั้งแรก
    success = super_fix_python_syntax(target_file)
    
    # ตรวจสอบ syntax
    if validate_python_syntax(target_file):
        print("🎉 SUCCESS! File is now syntactically correct!")
        print(f"🚀 Try running: python {target_file.name}")
    else:
        print("🔄 Still has errors, trying one more time...")
        # แก้ไขครั้งที่ 2
        super_fix_python_syntax(target_file)
        if validate_python_syntax(target_file):
            print("🎉 SUCCESS on second attempt!")
        else:
            print("😔 Still has syntax errors. Manual intervention needed.")

if __name__ == "__main__":
    main()
