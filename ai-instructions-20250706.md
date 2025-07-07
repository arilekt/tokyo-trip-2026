

# Tokyo Trip Generator Project - Context Summary
## 📋 Project Overview
Goal: Project สำหรับเตรียมแผนการเดินทางไปเที่ยว Tokyo ช่วงเดือน มีนาคม 2026 โดย สร้าง HTML guide แบบ offline สำหรับทริปโตเกียว
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

tokyo-trip-2026/
├── .git/                               # Git repository initialized
├── ai-instructions-20250706.md         # คำแนะนำสำหรับ AI --> This file
├── context_summary.md                  # สรุป context ทริป
├── script/
│   ├── old                              # script ที่ไม่ใช้แล้ว แต่ไม่อยากลบ เก็บไว้อ้างอิง
│   ├── claude-tokyo_trip_generator-20250706.py                # script ที่ดึงเนื้อหาออกมาครบ แต่แสดงผลไม่ถูก 
│   ├── template
│        ├── template.html               # template output ที่ final โดยมี html, css, js สมบูรณ์แบบ แต่เนื้อหาเป็น mock        
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

# On Progress Task:
* table ตีเส้นด้วย ทำเป็น flex สามารถ scroll ได้ ถ้ากว้างเกิน
* ส่วนของ timeline ต้องแสดงเป็นเส้น timeline
* ส่วน detail ใส่ใน timeline-detail ที่สามารถ expand/collapse ได้
* ยังมี ``` และ --- อยู่ ถ้าเจอเครื่องหมายนี้ หมายถึงเริ่ม/จบ section นะ


สรุปปัญหาและการแก้ไขสำหรับ AI Prompt: การสร้าง Tokyo Trip Generator
1. ภาพรวมโปรเจกต์ (Project Goal)
เป้าหมายหลัก: สร้างสคริปต์ Python (claude-tokyo_trip_generator-20250706.py) ที่สามารถอ่านไฟล์ Markdown จากโฟลเดอร์ content/ แล้วนำมาสร้างเป็นไฟล์ HTML แบบ All-in-One ที่สวยงาม, Responsive, และทำงานได้สมบูรณ์แบบออฟไลน์ โดยใช้ skeleton_template.html เป็นโครงสร้างหลัก

2. ปัญหาที่พบและเส้นทางการแก้ไข (Problem & Solution Journey)
2.1. ปัญหาเริ่มต้น: Regex ไม่สมบูรณ์ (Initial Problem: Broken Regex)
อาการ: สคริปต์ทำงานผิดพลาด, Markdown ไม่ถูกแปลงเป็น HTML หรือแปลงออกมาผิดเพี้ยนอย่างมาก
สาเหตุ: เกิดจากการคัดลอกและวางโค้ด (Copy-Paste Error) ในไฟล์ claude-tokyo_trip_generator-20250706.py ทำให้ Regular Expression ที่ใช้แปลง Markdown (เช่น Headers, Lists) มีข้อความ CSS ที่ไม่เกี่ยวข้องปนเข้ามา ทำให้ Pattern Matching ล้มเหลว
การแก้ไข: ลบส่วนที่ไม่เกี่ยวข้องออกจาก Regex และแก้ไข Pattern ให้ถูกต้องตามมาตรฐานการแปลง Markdown
2.2. ปัญหาหลัก: การประมวลผลซ้ำซ้อน (Core Problem: Double Processing / Processing Interference)
อาการ: หลังจากแก้ Regex แล้ว พบว่าส่วนที่ซับซ้อนที่สุดอย่าง Timeline แสดงผลไม่ถูกต้อง (ไม่เป็นเส้น, ไม่มีจุดบอกเวลา) แม้ว่าโค้ด HTML ที่สร้างในขั้นตอนแรกจะดูถูกต้องแล้วก็ตาม
สาเหตุที่แท้จริง (Root Cause): สคริปต์ทำงานแบบสายพาน (Pipeline) ทำให้เกิดการรบกวนกันเองระหว่างฟังก์ชัน ตัวอย่างเช่น:
ฟังก์ชัน _convert_timeline สร้าง <li> สำหรับแต่ละรายการใน Timeline อย่างถูกต้อง
แต่ฟังก์ชัน _convert_lists ที่ทำงานในลำดับถัดมา ถูกออกแบบมาเพื่อแปลง List ทั่วไป (- item) ให้เป็น <ul><li>...</li></ul>
ฟังก์ชัน _convert_lists จึงเข้าใจผิดว่า <li> ของ Timeline เป็น List ธรรมดา และเข้าไปห่อด้วย <ul> อีกชั้นหนึ่ง ทำให้โครงสร้าง HTML ของ Timeline ผิดเพี้ยนไปจากที่ skeleton_template.html คาดหวัง
เมื่อโครงสร้าง HTML ผิด, CSS ที่ออกแบบไว้สำหรับ .timeline > li จึงไม่สามารถทำงานได้ถูกต้อง
การแก้ไข (ที่ไม่สำเร็จในตอนแรก): พยายามปรับแก้ CSS หรือ JavaScript ซึ่งเป็นการแก้ที่ปลายเหตุและไม่ได้ผล เพราะต้นตอของปัญหาคือโครงสร้าง HTML ที่ไม่ถูกต้อง
2.3. الحل النهائي: กลยุทธ์ Placeholder (Final Solution: Placeholder Strategy)
หลักการ: เปลี่ยนจากการประมวลผลแบบสายพานที่เสี่ยงต่อการรบกวนกัน มาเป็นการ "แยกส่วนและแทนที่" (Isolate and Replace) ซึ่งเป็นวิธีที่ปลอดภัยและแม่นยำกว่ามาก
ขั้นตอนการทำงานใหม่ที่สมบูรณ์:
ค้นหาบล็อกซับซ้อน: สคริปต์จะค้นหาบล็อกที่มีโครงสร้างเฉพาะก่อน (Timeline, Table, Info Box)
แปลงและเก็บ: แปลงบล็อกนั้นๆ เป็น HTML ที่สมบูรณ์ แล้วเก็บผลลัพธ์ไว้ใน Dictionary (placeholders)
แทนที่ด้วยป้ายชื่อ: แทนที่ Markdown บล็อกเดิมในข้อความหลักด้วย "ป้ายชื่อ" ชั่วคราวที่ไม่ซ้ำกัน (เช่น __PLACEHOLDER_0__, __PLACEHOLDER_1__)
ประมวลผลส่วนที่เหลือ: ประมวลผล Markdown ที่เหลือ (ซึ่งตอนนี้ปลอดภัยแล้ว เพราะไม่มีบล็อกซับซ้อนปนอยู่) เช่น Lists และ Paragraphs ทั่วไป
นำกลับมาแทนที่: ในขั้นตอนสุดท้าย นำ HTML ที่สมบูรณ์ที่เก็บไว้ใน placeholders กลับมาแทนที่ "ป้ายชื่อ" ทั้งหมด
ผลลัพธ์: ได้ไฟล์ HTML ที่มีโครงสร้างถูกต้อง 100% ตามที่ skeleton_template.html ต้องการ ทำให้ CSS และ JavaScript ทั้งหมดทำงานได้อย่างสมบูรณ์
3. สรุป Key Takeaways สำหรับ AI
ลำดับการประมวลผล (Order of Operations) มีความสำคัญอย่างยิ่ง ในการเขียน Parser หรือตัวแปลงข้อความ การทำงานแบบ Pipeline อาจก่อให้เกิดการรบกวนกันเองได้
Placeholder Strategy เป็นวิธีที่แข็งแกร่งและแนะนำอย่างยิ่งในการป้องกันปัญหาการประมวลผลซ้ำซ้อน (Double Processing)
การแก้ไขปัญหาต้องเริ่มจากการทำความเข้าใจ Root Cause (โครงสร้าง HTML ผิด) ไม่ใช่แค่ปลายเหตุ (หน้าตาเว็บเพี้ยน)
การมี Template เป้าหมาย (skeleton_template.html) ที่สมบูรณ์และทำงานได้ เป็นสิ่งสำคัญที่ช่วยให้ทิศทางการแก้ไขโค้ด Python ชัดเจนและตรงเป้าหมาย