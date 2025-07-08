# Tokyo Trip Generator Project - Context Summary
## 📋 Project Overview
Goal: Project สำหรับเตรียมแผนการเดินทางไปเที่ยว Tokyo ช่วงเดือน มีนาคม 2026 โดย สร้าง HTML guide แบบ offline สำหรับทริปโตเกียว

📊 Project Analysis Summary
🎯 โครงสร้างหลัก:
พี่สร้าง Tokyo Trip Generator ที่เทพมาก! 🚀 ระบบแปลง .md files เป็น HTML แบบ offline สำหรับทริปโตเกียวมีนาคม 2026
✅ จุดแข็งที่ทำได้แล้ว:

Script หลัก claude-tokyo_trip_generator-20250707.py ทำงานได้ 100% แล้ว
Template System ใช้ skeleton_template.html ที่มี CSS/JS สมบูรณ์
Multi-language Support TH/EN switching
Content Structure มี 14 ไฟล์ .md ครบทุกวัน + อื่นๆ
Responsive Design รองรับทุกอุปกรณ์
Timeline System รองรับหลายรูปแบบ (time-based, highlight, step)
Version Control มี git พร้อม backup files หลายเวอร์ชัน

🔥 Features เด็ด:

Placeholder Strategy แก้ปัญหา double processing
Multiple Timeline Formats (เวลา/ไฮไลต์/ขั้นตอน)
Table & Info Box responsive
Birthday Badge สำหรับวันเกิด (day 4)
Back to Top Button
Collapsible Sections

📁 File Status:

✅ Script: ทำงานได้แล้ว (v3.1)
✅ Template: สมบูรณ์ (skeleton_template.html)
✅ Content: ครบ 14 files (TH ภาษาหลัก, EN ยังไม่มี)
✅ Build: มีไฟล์ output หลายเวอร์ชัน
✅ Git: track การเปลี่ยนแปลงได้

🎯 สิ่งที่พี่อาจต้องการปรับปรุง:

English Content - ยังไม่มีไฟล์ EN เลย
Final Testing - อาจต้องรัน script ใหม่เพื่อ verify
Content Updates - update เนื้อหาล่าสุด

## 🔧 Technical Requirements
### Core Features ที่ต้องมี:
1. อ่าน *.md files จาก content/ folder และ process เป็น HTML
2. Inline CSS/JS รวมทุกอย่างในไฟล์ HTML เดียวสำหรับใช้งาน offline
3. Multi-language support TH/EN โดยใช้ content/th/.md เป็นหลักสำหรับเนื่อหาภาษาไทย ถ้า en/.md ไม่มีให้ใช้ภาษาไทยก่อน ถ้ามีให้ใช้ en ในส่วน en
4. Responsive design ใช้งานได้บน iPad, Android, Mobile
5. Generate ลง build/ folder ตามรูปแบบ Tokyo-Trip-March-2026-*-YYYYMMDD.html
6. ผู้ใช้จะทำการ update เนื้อหาลงใน content/th/.md และหรือ content/en/.md เพื่อ build updated guide อยู่เสมอ
7. script จะอ่านเนื้อหา ใน content แล้ว generate ออกมาเป็น html ไฟล์เดียว ที่มีทั้ง css, js, html เพื่อเอาไว้เปิดดูตอนไปเที่ยว
## 📁 Project Structure 
D:\DEV_WORKSPACE\tokyo-trip-2026 --> Allow Claude Desktop read/write/list dir etc.

tokyo-trip-2026/
├── .git/                               # Git repository initialized
├── ai-instructions-20250706.md         # คำแนะนำสำหรับ AI --> This file
├── context_summary.md                  # สรุป context ทริป
├── script/
│   ├── old                              # script ที่ไม่ใช้แล้ว แต่ไม่อยากลบ เก็บไว้อ้างอิง
│   ├── claude-tokyo_trip_generator-20250707.py                # script ที่ดึงเนื้อหาออกมาครบ ทำงานครบ 100%
│   ├── template
│        ├── template.html.old               # template output ที่ final โดยมี html, css, js สมบูรณ์แบบ แต่เนื้อหาเป็น mock        
│        ├── skeleton_template.html      # template output ที่ final โดยมี html, css, js สมบูรณ์แบบใช้ gen output     
├── content/
│   ├── th/*.md files                   # ภาษาไทยหลัก (14 files)
│   └── en/                             # ภาษาอังกฤษ ตอนนี้ยังไม่ได้ทำ แต่ให้ script ลองอ่าน ถ้ามีให้ใช้ตามชื่อไฟล์
└── build/
    └── final-plan-merged.html          # ⭐ ไฟล์ HTML สำเร็จรูป (124KB) --> เอาไว้อ้างอิงเฉย ๆ

### Current Status and task:
🚀 ฟีเจอร์ที่ทำได้:
✅ Core Features:

📚 *อ่าน .md files จาก content/th/ และ content/en/
🔄 แปลง Markdown เป็น HTML (headers, lists, tables, timeline)
🌐 Multi-language support TH/EN (ถ้าไม่มี EN ใช้ TH)
📱 Responsive design ใช้ template.html เดิม
📁 Generate ลง build/ ตามรูปแบบ Tokyo-Trip-March-2026-*-YYYYMMDD.html
📋 Navigation cards grid (8 วัน) พร้อม birthday badge
📄 Content sections จาก markdown files
⏰ Timeline functionality พร้อม expand/collapse
🌐 Multi-language TH/EN support
⬆️ Back to top button เมื่อ scroll ลง
📱 Responsive design ใช้งานได้ทุกอุปกรณ์
🗺️ Navigation section จาก 001-overview.md
📄 Content sections จาก 002-014-*.md
📊 Table conversion markdown → HTML tables
⏰ Timeline conversion สำหรับ - **เวลา**: เนื้อหา
⬆️ Back to top button แสดงเมื่อ scroll ลง
🎨 Template integration ใช้ CSS/JS เดิมครบ
📝 Markdown Support:
# → <h1>
## → <h2> 
### → <h3>
#### → <h4>
**text** → <strong>text</strong>
*text* → <em>text</em>
- item → <li>item</li>
| table | → HTML table
- **10:00**: activity → timeline item

 ให้น้อง analyst แล้วส่ง code snippet เฉพาะส่วนที่แก้ออกมาใน canvas โดยพี่สามารถเอา code ส่วนนั้นไป replace แทน