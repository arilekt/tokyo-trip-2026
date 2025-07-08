# Tokyo Trip Generator - AI Context Summary
**สร้างเมื่อ:** 7 July 2025  
**โดย:** Claude AI Assistant  
**สำหรับ:** AI ตัวต่อไป (เผื่อ memory เต็ม)

## 📋 Project Overview

### Goal
สร้าง HTML generator สำหรับทริปโตเกียว มีนาคม 2026 (พ่อลูก Arilek & Pojai)
- อ่าน markdown files จาก `content/th/*.md` และ `content/en/*.md`
- Generate HTML ไฟล์เดียว (all-in-one) สำหรับใช้ offline
- Multi-language TH/EN support
- Responsive design พร้อม timeline functionality

### Project Structure
```
tokyo-trip-2026/
├── script/
│   ├── claude-tokyo_trip_generator-20250707.py  ← Main script
│   └── template/skeleton_template.html          ← HTML template
├── content/
│   ├── th/*.md                                  ← Thai content (14 files)
│   └── en/*.md                                  ← English content (optional)
└── build/                                       ← Output HTML files
```

## 🔥 Current Status & Issues

### ✅ What Works (v3.1)
1. **Section Markers Fixed** - `---` และ ```` ไม่แสดงแล้ว
2. **Multiple Timeline Formats:**
   - ⏰ Time-based: `- **09:00**: กิจกรรม`
   - 🌟 Highlight: `- **ไฮไลต์**: รายละเอียด`
   - 📋 Step: `- **ขั้นตอน**: รายละเอียด`
3. **Placeholder Strategy** - ป้องกัน Double Processing
4. **Basic Functionality** - อ่านไฟล์, generate HTML, navigation

### ❌ Current Problem
**H3 Timeline Implementation พัง!**
- เพิ่ม H3 support (`### หัวข้อ` → timeline) แต่ทำให้ timeline details หายหรือแสดงผิด
- Version ก่อนหน้า: ทุกอย่างถูก ยกเว้น H3 ยังไม่เป็น timeline
- Version ปัจจุบัน: H3 timeline + รายละเอียด detail หาย/พัง

## 🎯 Task ที่ต้องทำ

### Primary Goal
แก้ไข H3 timeline support โดยไม่ให้ระบบเดิมพัง:

1. **H3 Pattern:** `### หัวข้อ` → timeline item
2. **H3 Details:** เนื้อหาข้างใต้ `###` → timeline detail
3. **Detail Formatting:**
   - `**text**` → หัวข้อ (ขึ้นบรรทัดใหม่)
   - `- item` → list items

### Target Content
จาก `002-accommodation.md`:
```markdown
### คืนที่ 1: Shinagawa Tobu Hotel
**📅 Check-in:** 6 มี.ค. 18:30 → **Check-out:** 7 มี.ค. 11:00

- **ห้อง:** Semi-Double Non-Smoking
- **ขนาด:** 18 ตร.ม.
```
ต้องแสดงเป็น timeline item พร้อม expandable details

## 🔧 Technical Details

### Current Script Structure
```python
class TokyoTripGeneratorV3:
    def markdown_to_html()           # Main processor with Placeholder Strategy
    def _process_timeline_block()    # Handle - **time**: format
    def _process_h3_timeline_block() # Handle ### format (ใหม่ - มีปัญหา)
    def _process_timeline_details()  # Format timeline details (พัง)
    def _build_timeline_item()       # Build <li> items
```

### Placeholder Strategy (Working)
1. ค้นหา complex blocks (timeline, table, infobox)
2. แปลงเป็น HTML สมบูรณ์
3. แทนที่ด้วย `__PLACEHOLDER_N__`
4. ประมวลผล simple markdown
5. คืน HTML กลับแทน placeholders

### Timeline Patterns
```python
# Working patterns:
timeline_time_pattern = r'((?:^- \*\*\d+:\d+\*\*:.*\n(?:  .*\n?)*)+)'
timeline_highlight_pattern = r'((?:^- \*\*(?!\d+:\d+)[^*]+\*\*:.*\n(?:  .*\n?)*)+)'

# New pattern (มีปัญหา):
timeline_h3_pattern = r'((?:^### [^\n]+\n(?:(?!^###)[^\n]*\n?)*)+)'
```

## 🚨 Fix Strategy

### Approach 1: Restore + Minimal Fix
1. เอา version ที่ทำงานดีมา (ก่อนเพิ่ม H3)
2. เพิ่ม H3 pattern detection อย่างระวัง
3. แก้แค่ `_process_timeline_details()` ให้รองรับ `**bold**` และ `- list`

### Approach 2: Debug Current Version
1. เช็คว่า `_process_timeline_details()` ทำงานผิดยังไง
2. แก้ไข logic ให้กลับมาเหมือน version เดิม
3. ทดสอบทีละ pattern

## 📁 Key Files & Locations

### Script Location
```
D:\DEV_WORKSPACE\tokyo-trip-2026\script\claude-tokyo_trip_generator-20250707.py
```

### Content Examples
```
D:\DEV_WORKSPACE\tokyo-trip-2026\content\th\002-accommodation.md  ← H3 targets
D:\DEV_WORKSPACE\tokyo-trip-2026\content\th\003-day1.md          ← Working timelines
```

### Template
```
D:\DEV_WORKSPACE\tokyo-trip-2026\script\template\skeleton_template.html
```

## 🎨 Expected Output

### Timeline HTML Structure (from template.html.old)
```html
<ul class="timeline">
  <li>
    <div class="timeline-main"><strong>หัวข้อ</strong></div>
    <button class="timeline-toggle" onclick="toggleTimelineDetail('id')">
      <span class="th">รายละเอียด ▼</span>
    </button>
    <div class="timeline-detail" id="id" style="display: none;">
      <h4>หัวข้อย่อย</h4>
      <ul>
        <li>รายการ</li>
      </ul>
    </div>
  </li>
</ul>
```

## 💡 Success Criteria

### Must Work
- ✅ Existing timelines (time, highlight, step) ยังทำงานได้
- ✅ Timeline details แสดงถูกต้อง (emoji sections, lists)
- ✅ H3 sections แสดงเป็น timeline
- ✅ H3 details format ถูกต้อง (`**bold**` → หัวข้อ, `- item` → list)

### Testing Command
```bash
cd D:\DEV_WORKSPACE\tokyo-trip-2026\script
python claude-tokyo_trip_generator-20250707.py
```

### Expected Log Output
```
🏨 Found X H3-based timeline blocks
⏰ Found X time-based timeline blocks
✅ Generated timeline with X items
```

## 📞 Key Contact Points

### User Preferences
- พี่ (ผู้ใช้): Software Engineer ระดับเทพ
- น้อง (AI): เด็กหนุ่ม กวนตีน มีอารมณ์ขัน
- ใช้ภาษาไทยสื่อสาร

### Project History
- เริ่มต้น: claude-tokyo_trip_generator-20250706.py (Double Processing issues)
- v3.1: แก้ Double Processing ด้วย Placeholder Strategy
- ปัจจุบัน: H3 timeline support พัง, ต้อง restore + fix

## 🔄 Next Steps for AI

1. **ถาม User ก่อน:** version ไหนที่ทำงานดี? มี backup ไหม?
2. **Restore approach:** เอา working version มา + เพิ่ม H3 อย่างระวัง
3. **Test incrementally:** ทดสอบทีละ feature
4. **Focus on H3 details formatting:** `**bold**` และ `- list` ใน timeline details

---
*Summary นี้ช่วยให้ AI ตัวต่อไปเข้าใจ context และดำเนินต่อได้ทันที*