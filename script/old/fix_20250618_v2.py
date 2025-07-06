#!/usr/bin/env python3
"""
🔧 FIXED SYNTAX FIXER FOR 20250618
แก้ไข syntax errors ในไฟล์ 20250618 โดยเฉพาะ (แก้ไข TypeError แล้ว)
"""

import re
from pathlib import Path

def fix_20250618_syntax_errors(source_file, target_file):
    """แก้ไข syntax errors ในไฟล์ 20250618 โดยเฉพาะ"""
    
    print(f"🔧 Fixing 20250618 syntax errors...")
    print(f"📂 Source: {source_file}")
    print(f"📂 Target: {target_file}")
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_lines = len(content.split('\n'))
    print(f"📄 Original file: {original_lines} lines")
    
    # สำรองไฟล์เดิม - แก้ไข TypeError
    backup_file = str(source_file) + '.backup'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📦 Backup saved: {backup_file}")
    
    fixes_applied = 0
    
    # Fix 1: แก้ไข regex patterns ที่แยกออกเป็น 2 บรรทัด
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Pattern 1: regex ที่ลงท้ายด้วย single quote แล้วบรรทัดถัดไปเป็น , line)
        if (i < len(lines) - 1 and 
            're.match(r\'' in line and 
            line.rstrip().endswith('\'') and
            lines[i + 1].strip() == ', line)'):
            
            # รวมสองบรรทัด
            combined_line = line + ', line)'
            fixed_lines.append(combined_line)
            print(f"✅ Fix 1 - Line {i+1}-{i+2}: Combined regex pattern")
            fixes_applied += 1
            i += 2  # ข้ามบรรทัดถัดไป
            continue
        
        # Pattern 2: regex ที่ไม่สมบูรณ์
        elif (i < len(lines) - 1 and
              're.match(r\'' in line and 
              not line.endswith(', line)') and
              not line.endswith('\', line)') and
              ', line)' in lines[i + 1]):
            
            combined_line = line + ', line)'
            fixed_lines.append(combined_line)
            print(f"✅ Fix 2 - Line {i+1}-{i+2}: Added missing , line)")
            fixes_applied += 1
            i += 2
            continue
        
        # Pattern 3: บรรทัดที่เหลือแค่ , line) โดดๆ
        elif line.strip() == ', line)':
            print(f"⚠️  Removed orphaned line {i+1}: {line.strip()}")
            fixes_applied += 1
            i += 1
            continue
        
        # Pattern 4: function definition ที่ขาด indentation
        elif (line.strip().startswith('def ') and 
              line.strip().endswith(':') and
              i < len(lines) - 1 and
              lines[i + 1].strip().startswith('"""') and
              not lines[i + 1].startswith('    ')):
            
            fixed_lines.append(line)
            # แก้ไข indentation ของ docstring
            next_line = '    ' + lines[i + 1].lstrip()
            fixed_lines.append(next_line)
            print(f"✅ Fix 4 - Line {i+2}: Fixed function docstring indentation")
            fixes_applied += 1
            i += 2
            continue
        
        else:
            fixed_lines.append(line)
            i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Fix 5: ตรวจสอบและแก้ไข parentheses ที่ไม่สมดุล
    open_parens = content.count('(')
    close_parens = content.count(')')
    if open_parens != close_parens:
        print(f"⚠️  Parentheses imbalance: {open_parens} open, {close_parens} close")
        # หาและแก้ไข regex patterns ที่ขาด closing parenthesis
        content = re.sub(r're\.match\(r\'([^\']+)\'\s*$', r're.match(r\'\1\', line)', content, flags=re.MULTILINE)
        fixes_applied += 1
        print(f"✅ Fix 5: Fixed parentheses balance")
    
    # เขียนไฟล์ที่แก้ไขแล้ว
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    new_lines = len(content.split('\n'))
    print(f"📄 Fixed file: {new_lines} lines")
    print(f"🔧 Applied {fixes_applied} fixes")
    
    return fixes_applied > 0

def validate_python_syntax(file_path):
    """ตรวจสอบ Python syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        compile(content, str(file_path), 'exec')
        print("✅ Python syntax validation: PASSED")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error still exists:")
        print(f"   Line {e.lineno}: {e.text.strip() if e.text else 'N/A'}")
        print(f"   Error: {e.msg}")
        return False
    except Exception as e:
        print(f"⚠️  Other error: {e}")
        return False

def main():
    """แก้ไขไฟล์ 20250618"""
    script_dir = Path(__file__).parent
    
    # ไฟล์ต้นฉบับ 20250618
    source_file = script_dir / "claude-tokyo_trip_generator-final-20250618.py"
    target_file = script_dir / "claude-tokyo_trip_generator-FINAL-FIXED.py"
    
    if source_file.exists():
        print(f"🎯 Target file: {source_file}")
        print(f"📊 File size: {source_file.stat().st_size:,} bytes")
        print()
        
        success = fix_20250618_syntax_errors(source_file, target_file)
        
        print(f"\n🔍 Validating fixed file...")
        if validate_python_syntax(target_file):
            print(f"\n🎉 SUCCESS! File is now ready to run!")
            print(f"🚀 Try running: python {target_file.name}")
            print(f"📄 Fixed file: {target_file}")
        else:
            print(f"\n😔 Still has syntax errors. Let me check what's wrong...")
            # หาข้อมูลเพิ่มเติมเกี่ยวกับ error
            try:
                with open(target_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                compile(content, str(target_file), 'exec')
            except SyntaxError as e:
                print(f"📍 Specific error at line {e.lineno}: {e.msg}")
                if e.lineno and e.lineno <= len(content.split('\n')):
                    error_line = content.split('\n')[e.lineno - 1]
                    print(f"📝 Problem line: {error_line}")
            
    else:
        print(f"❌ Source file not found: {source_file}")
        print("Available files:")
        for f in script_dir.glob("claude-tokyo_trip_generator*.py"):
            print(f"  - {f.name}")

if __name__ == "__main__":
    main()
