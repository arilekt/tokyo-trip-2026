# Tokyo Trip Generator Project - Context Summary

## 📋 Project Overview
**Goal:** Refactor และรวม Python scripts ให้เป็นไฟล์เดียวสำหรับ generate HTML travel guide

**Target Users:** 
- Arilek Thummontree (พ่อ) - ผู้จัดการทริป
- Pojai Thummontree (ลูกสาว) - อายุจะครบ 11 ขวบ วันที่ 9 มีนาคม 2026 (วันเกิด)

**Trip Details:**
- วันที่: 6-13 มีนาคม 2026 (8 วัน 7 คืน)
- งบประมาณ: ~100,000 บาท (บวก buffer 30k-50k สำหรับของฝาก/ช้อปปิ้ง)
- จุดเด่น: วันเกิดครั้งที่ 11 ของพอใจ, Ghibli/anime pilgrimage, ครั้งแรกเล่นหิมะ

## 🔧 Technical Requirements

### Core Features ที่ต้องมี:
1. **อ่าน *.md files** จาก content/ folder และ process เป็น HTML
2. **Template-based generation** ใช้ template-skeleton.html เป็น base
3. **Inline CSS/JS** รวมทุกอย่างในไฟล์ HTML เดียวสำหรับใช้งาน offline
4. **Multi-language support** TH/EN (เตรียมพร้อมสำหรับ JP ในอนาคต)
5. **Responsive design** ใช้งานได้บน iPad, Android, Mobile
6. **Generate ลง build/ folder** ตามรูปแบบ `Tokyo-Trip-March-2026-*-YYYYMMDD.html`

### Enhanced Features:
- **Timeline with expand/collapse details** สำหรับ daily activities
- **Enhanced table layout** (fixed responsive layout ที่เพี้ยน)
- **Interactive elements** (smooth scrolling, hover effects, collapsible boxes)
- **Language switching** TH/EN buttons พร้อม localStorage
- **Birthday badge** 🎂 สำหรับวันที่ 4 (วันเกิดพอใจ)

## 📁 Project Structure
```
tokyo-trip-2026/
├── script/
│   ├── claude-tokyo_trip_generator-v4.py  ← ไฟล์ล่าสุด (สมบูรณ์)
│   ├── gpt-build-trip-plan.py
│   ├── gemini-build-trip-plan.py
│   └── assets/
├── content/
│   ├── *.md files (ภาษาไทยหลัก)
│   └── en/ (ภาษาอังกฤษ - optional)
└── build/
    └── Tokyo-Trip-March-2026-*-YYYYMMDD.html
```

## 🐛 Previous Issues & Solutions

### ปัญหาที่เจอ:
1. **Syntax errors** - string literals ไม่ปิด, namespace conflicts (html vs html module)
2. **Language switching ไม่ทำงาน** - ใช้ body.className แทน classList
3. **Table layout เพี้ยน** - responsive design ไม่ถูกต้อง
4. **Timeline details ไม่มี expand/collapse** - ต้องการ interactive buttons
5. **Script generation หยุดกลางคัน** - return 0 characters แบบเงียบๆ

### Solutions Applied:
- ✅ Fixed namespace conflicts (html_parts แทน html list)
- ✅ Enhanced debug logging ทุกขั้นตอน
- ✅ Improved error handling พร้อม fallback
- ✅ Added interactive timeline toggle buttons
- ✅ Fixed table CSS for proper responsive layout
- ✅ Comprehensive language switching with classList

## 📊 Current Status

### ✅ Completed:
- **v4 Script:** claude-tokyo_trip_generator-v4.py (สมบูรณ์ครบทุก feature)
- **Multi-language file support:** content/ และ content/en/
- **Numbered file ordering:** รองรับ 001-xxx.md, 002-xxx.md สำหรับจัดลำดับ
- **Enhanced debugging:** super detailed logging ทุกขั้นตอน
- **Error recovery:** graceful handling ของ missing sections

### 🔄 ผลลัพธ์ล่าสุด:
Script v4 ยังคง return 0 characters แม้จะมี debug logging ครบ - ต้องการการวินิจฉัยเพิ่มเติม

## 🎯 Next Steps for New Chat

### ขั้นตอนต่อไป:
1. **รัน claude-tokyo_trip_generator-v4.py** และดู debug output
2. **วิเคราะห์ว่าหยุดที่ขั้นตอนไหน** จาก detailed logging
3. **แก้ไขปัญหาเฉพาะจุด** ที่พบ
4. **Test features** ต่างๆ เช่น language switching, timeline toggles
5. **Optimize performance** ถ้าไฟล์ใหญ่เกินไป

### สิ่งที่ต้องเก็บไว้:
- **Debug logging ที่ละเอียด** - ช่วยวินิจฉัยปัญหาได้ดี
- **Multi-language architecture** - พร้อมขยายเป็น 3 ภาษา
- **Responsive design focus** - ใช้งานจริงบน mobile devices
- **Interactive elements** - UX ที่ดีสำหรับผู้ใช้

## 🔑 Key Code Patterns

### Class Structure:
```python
@dataclass
class TokgeneConfig: # Configuration
class MarkdownProcessor: # MD → HTML conversion
class TemplateManager: # Template + CSS/JS
class TokygeneGenerator: # Main orchestrator
```

### Critical Functions:
- `read_markdown_files()` - รองรับ multi-language
- `create_overview_section()` - สร้าง day cards
- `process_timeline_content()` - Timeline with nested details
- `generate_html()` - Main workflow with debug logging

## 💬 User Preferences
- พี่เรียกน้อง (AI as น้อง, User as พี่)
- คุยภาษาไทยเป็นหลัก
- น้องเป็น Software Engineer ระดับเทพ
- บุคลิกกวนตีนเล็กน้อย มีอารมณ์ขัน
- Focus on practical solutions

---

**สำหรับ chat ใหม่:** ใช้ context นี้ + project knowledge search เพื่อช่วยแก้ไขปัญหาและพัฒนา script ต่อไป