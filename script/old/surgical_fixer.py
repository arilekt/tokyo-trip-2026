#!/usr/bin/env python3
"""
🔧 SURGICAL SYNTAX FIXER
แก้ไข syntax errors ในไฟล์เดิมโดยไม่เปลี่ยนแปลงอะไรอื่น
"""

import re
from pathlib import Path

def surgical_fix_syntax_errors(source_file, target_file):
    """แก้ไข syntax errors อย่างระมัดระวัง"""
    
    print(f"🔧 Surgical fixing: {source_file} -> {target_file}")
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_lines = len(content.split('\n'))
    print(f"📄 Original file: {original_lines} lines")
    
    # แก้เฉพาะ syntax errors ที่รู้จัก
    fixes_applied = 0
    
    # Fix 1: แก้ไข regex patterns ที่มี syntax error
    if ", line)" in content and not content.count("re.match") == content.count(", line)"):
        print("⚠️  Found potential syntax errors with ', line)'")
        
        # แก้ไขเฉพาะบรรทัดที่มีปัญหา
        lines = content.split('\n')
        fixed_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # หา pattern ที่เสีย: บรรทัดที่มี re.match และบรรทัดถัดไปมี , line) โดดๆ
            if ("re.match(r'" in line and 
                i < len(lines) - 1 and 
                lines[i + 1].strip() == ", line)"):
                
                # รวมสองบรรทัด
                fixed_line = line + ", line)"
                fixed_lines.append(fixed_line)
                print(f"✅ Fixed line {i+1}-{i+2}: Combined regex pattern")
                fixes_applied += 1
                i += 2  # ข้ามบรรทัดถัดไป
                continue
            
            # หา pattern อื่นที่เสีย
            elif line.strip() == ", line)" and i > 0:
                # ข้ามบรรทัดที่เหลือแค่ , line) โดดๆ
                print(f"⚠️  Removed orphaned line {i+1}: {line.strip()}")
                fixes_applied += 1
                i += 1
                continue
            
            fixed_lines.append(line)
            i += 1
        
        content = '\n'.join(fixed_lines)
    
    # Fix 2: แก้ไข indentation errors
    if "IndentationError" in str(content) or content.count('"""') % 2 != 0:
        print("⚠️  Checking for indentation issues...")
        # ตรวจสอบ function definitions ที่ไม่มี proper indentation
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') and line.strip().endswith(':'):
                if i < len(lines) - 1:
                    next_line = lines[i + 1]
                    if next_line.strip().startswith('"""') and not next_line.startswith('    '):
                        lines[i + 1] = '    ' + next_line.lstrip()
                        print(f"✅ Fixed indentation at line {i+2}")
                        fixes_applied += 1
        
        content = '\n'.join(lines)
    
    # เขียนไฟล์ใหม่
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    new_lines = len(content.split('\n'))
    print(f"📄 Fixed file: {new_lines} lines")
    print(f"🔧 Applied {fixes_applied} fixes")
    
    return fixes_applied > 0

def main():
    """แก้ไขไฟล์ต้นฉบับ"""
    script_dir = Path(__file__).parent
    
    # ใช้ไฟล์ที่ทำงานได้จาก old/
    source_file = script_dir / "old" / "claude-tokyo_trip_generator-final-20250617.py"
    target_file = script_dir / "claude-tokyo_trip_generator-SURGICAL-FIXED-20250620.py"
    
    if source_file.exists():
        success = surgical_fix_syntax_errors(source_file, target_file)
        if success:
            print(f"🎉 Successfully created: {target_file}")
            print(f"🚀 Try running: python {target_file.name}")
        else:
            print(f"ℹ️  No fixes needed, copied as-is: {target_file}")
    else:
        print(f"❌ Source file not found: {source_file}")

if __name__ == "__main__":
    main()
