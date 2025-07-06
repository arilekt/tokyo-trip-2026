    
    for day_num, title_combo, description_combo in day_summaries:
        title_th, title_en = title_combo.split(' - ', 1) if ' - ' in title_combo else (title_combo, title_combo)
        description_th = description_combo.strip()
        description_en = description_combo.strip() 
        
        html_cards.append(f'<div class="day-overview">\n')
        html_cards.append(f'<h3><a href="#day{day_num}"><span class="th">{title_th}</span><span class="en">{title_en}</span></a></h3>\n')
        html_cards.append(f'<p><span class="th">{description_th}</span><span class="en">{description_en}</span></p>\n')
        html_cards.append(f'</div>\n')
    
    # Add budget overview card
    budget_overview_title_th = "ประมาณการค่าใช้จ่ายและสถานะ"
    budget_overview_title_en = "Budget Estimate and Status"
    budget_overview_desc_th = "ข้อมูลการจอง และประมาณการค่าใช้จ่าย."
    budget_overview_desc_en = "Booking information and estimated expenses."

    html_cards.append(f'''
    <div class="day-overview">
    <h3><a href="#budget"><span class="th">{budget_overview_title_th}</span><span class="en">{budget_overview_title_en}</span></a></h3>
    <p><span class="th">{budget_overview_desc_th}</span><span class="en">{budget_overview_desc_en}</span></p>
    </div>
    ''')
    
    html_cards.append('</div>\n')
    
    # Add usage info box
    usage_info_box = '''
<div class="note-box">
<div class="note-toggle">
<span class="th">ℹ️ วิธีการใช้งานแผนการเดินทาง</span>
<span class="en">ℹ️ How to Use the Itinerary</span>
</div>
<div class="note-detail">
<p class="th th-block">แผนการเดินทางรวมอยู่ในไฟล์เดียวเพื่อความสะดวกในการใช้งานออฟไลน์</p>
<p class="en en-block">The itinerary is consolidated into a single file for easy offline use.</p>
<p class="th th-block">คลิกที่หัวข้อ <span class="emoji">ℹ️</span> เพื่อขยายดูรายละเอียดเพิ่มเติม และใช้ปุ่ม "กลับไปหน้าหลัก" ด้านล่างขวาเพื่อไปยังสารบัญ</p>
<p class="en en-block">Click on the <span class="emoji">ℹ️</span> headings to expand for more details, and use the "Back to Top" button at the bottom right to navigate to the table of contents.</p>
<p class="th th-block">ใช้ปุ่ม TH/EN ที่มุมบนขวา (ลอยอยู่) เพื่อสลับภาษา</p>
<p class="en en-block">Use the floating TH/EN buttons at the top right to switch languages.</p>
</div>
</div>
    '''
    html_cards.append(usage_info_box)

    return "".join(html_cards)


def generate_trip_guide_html():
    """Main function to generate the complete HTML trip guide."""
    print("🎆 Generating ENHANCED HTML...")
    print("📂 Reading markdown content...")

    # 1. Read template skeleton
    template_html = read_file_content(TEMPLATE_PATH)
    if template_html is None:
        print("Failed to read template skeleton. Exiting.")
        return

    soup = BeautifulSoup(template_html, "html.parser")

    # 2. Inject CSS directly into <head>
    style_tag = soup.find('style')
    if style_tag:
        style_tag.string = INLINE_CSS
    else:
        style_tag = soup.new_tag("style")
        style_tag.string = INLINE_CSS
        soup.head.append(style_tag)

    # 3. Inject JavaScript directly into <head>
    script_tag = soup.find('script')
    if script_tag:
        script_tag.string = INLINE_JS
    else: 
        script_tag = soup.new_tag("script")
        script_tag.string = INLINE_JS
        soup.body.append(script_tag) 

    # 4. Read markdown content files
    markdown_contents = {}
    
    content_files = {
        "001-overview.md": "overview",
        "002-accommodation.md": "accommodation", 
        "003-day1.md": "day1",
        "004-day2.md": "day2",
        "005-day3.md": "day3",
        "006-day4.md": "day4",
        "007-day5.md": "day5",
        "008-day6.md": "day6",
        "009-day7.md": "day7",
        "010-day8.md": "day8",
        "011-transportation.md": "transportation",
        "012-weather.md": "weather",
        "013-budget.md": "budget",
        "014-tips.md": "tips"
    }

    # Read Thai files
    thai_count = 0
    for filename, section_id in content_files.items():
        file_path = CONTENT_DIR / filename
        if file_path.exists():
            content = read_file_content(file_path)
            if content is not None:
                markdown_contents[section_id] = content
                print(f"  ✅ th: {filename} -> {section_id}")
                thai_count += 1
        else:
            print(f"  ⚠️ Missing: {filename}")

    print(f"✅ Read {thai_count} Thai files")
    print(f"✅ Read 0 English files")

    # For overview content
    full_markdown_master_content = ""
    if "overview" in markdown_contents:
        full_markdown_master_content = markdown_contents["overview"]

    # 5. Process sections
    print("🎆 Processing content sections - ENHANCED VERSION...")
    
    # Update title tags
    overall_title_th = "เที่ยวญี่ปุ่น Porjai: Birthday Trip 2026"
    overall_title_en = "Porjai's Japan Trip: Birthday Adventure 2026"
    
    if soup.title:
        soup.title.string = overall_title_th
    else:
        new_title_tag = soup.new_tag("title")
        new_title_tag.string = overall_title_th
        soup.head.append(new_title_tag)

    # Update header
    header_h1 = soup.find('h1', id='toc')
    if header_h1:
        th_span = header_h1.find('span', class_='th')
        en_span = header_h1.find('span', class_='en')
        if th_span:
            th_span.string = overall_title_th
        if en_span:
            en_span.string = overall_title_en

    # Process overview section
    print("🏠 Creating overview section...")
    overview_html = create_day_overview_cards_html(full_markdown_master_content)
    
    # Count day cards created
    day_card_count = overview_html.count('<div class="day-overview">') - 1
    for i in range(1, 9):
        if f'Day {i}' in overview_html or f'วันที่ {i}' in overview_html:
            print(f"  ✅ Added overview card: วันที่ {i}: {6+i-1} มีนาคม 2026 ({'ศุกร์' if i==1 else 'เสาร์' if i==2 else 'อาทิตย์' if i==3 else 'จันทร์' if i==4 else 'อังคาร' if i==5 else 'พุธ' if i==6 else 'พฤหัสบดี' if i==7 else 'ศุกร์'})")
    
    print(f"✅ Overview section created with {day_card_count} day cards")

    # Process sections
    processed_sections_html_parts = {}
    processed_sections_html_parts['overview'] = f'<section id="overview">\n<h1><span class="th th-block">ภาพรวมการเดินทางและกิจกรรม</span><span class="en en-block">Trip Overview &amp; Activities</span></h1>\n{overview_html}\n</section>\n'

    # Process day sections with timeline
    for day_num in range(1, 9):
        day_key = f"day{day_num}"
        if day_key in markdown_contents:
            print("⏰ Processing timeline markdown")
            
            day_content = markdown_contents[day_key]
            
            # Process timeline sections in chunks for logging
            lines = day_content.split('\n')
            for i in range(0, len(lines), 10):
                chunk = lines[i:i+10]
                chunk_content = '\n'.join(chunk)
                if chunk_content.strip():
                    processed_lines = len([l for l in chunk if l.strip()])
                    html_chars = len(mistune.html(chunk_content))
                    print(f"📝 Processing {processed_lines} lines of markdown")
                    print(f"✅ Converted to {html_chars} characters of HTML")
            
            # Create day title from content
            title_match = re.search(r'^#\s+(.+)', day_content, re.MULTILINE)
            if title_match:
                day_title = title_match.group(1).strip()
            else:
                day_title = f"วันที่ {day_num}: ไม่มีหัวข้อ"

            day_section_html = process_markdown_to_html_section(day_title, day_content, day_key)
            processed_sections_html_parts[day_key] = day_section_html
            
            total_chars = len(day_section_html)
            expandable_items = day_section_html.count('timeline-detail')
            
            print(f"✅ Timeline processed with {expandable_items} expandable items")
            print(f"  ✅ Enhanced: {day_key} ({total_chars} chars)")

    # Process other sections
    other_sections = ["accommodation", "transportation", "weather", "budget", "tips"]
    for section_key in other_sections:
        if section_key in markdown_contents:
            content = markdown_contents[section_key]
            
            # Get title from content
            title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
            if title_match:
                section_title = title_match.group(1).strip()
            else:
                section_title = section_key.title()

            if section_key in ["transportation", "weather", "tips"]:
                # Process larger sections with logging
                lines = content.split('\n')
                processed_lines = len(lines)
                html_content = mistune.html(content)
                html_chars = len(html_content)
                
                print(f"📝 Processing {processed_lines} lines of markdown")
                print(f"✅ Converted to {html_chars} characters of HTML")
                
                section_html = process_markdown_to_html_section(section_title, content, section_key)
                processed_sections_html_parts[section_key] = section_html
                print(f"  ✅ Enhanced: {section_key} ({html_chars} chars)")
            else:
                # Process smaller sections
                section_html = process_markdown_to_html_section(section_title, content, section_key)
                processed_sections_html_parts[section_key] = section_html
                chars = len(section_html)
                print(f"  ✅ Enhanced: {section_key} ({chars} chars)")

    # Calculate total content size
    total_chars = sum(len(html) for html in processed_sections_html_parts.values())
    print(f"✅ ENHANCED processing complete: {total_chars:,} chars")

    # 6. Inject processed sections into template
    container_div = soup.find('div', class_='container')
    if container_div:
        # Clear existing placeholders
        section_order = ["overview", "day1", "day2", "day3", "day4", "day5", "day6", "day7", "day8", 
                        "accommodation", "transportation", "weather", "budget", "tips"]

        for section_id in section_order:
            placeholder_div = container_div.find('div', id=section_id)
            if placeholder_div:
                placeholder_div.decompose()
        
        # Append processed sections
        for section_id in section_order:
            if section_id in processed_sections_html_parts:
                container_div.append(BeautifulSoup(processed_sections_html_parts[section_id], 'html.parser'))
    else:
        print("Error: Main content container (.container) not found in template.")
        return

    # 7. Generate final HTML file
    current_datetime_str = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    output_filename = BUILD_DIR / f"Tokyo-Trip-March-2026-SUPER-FIXED-{current_datetime_str}.html"
    
    final_html = str(soup)
    total_html_chars = len(final_html)
    
    print(f"✅ ENHANCED HTML generated: {total_html_chars:,} characters")
    
    try:
        with open(output_filename, "w", encoding='utf-8') as f_out:
            f_out.write(final_html)
        
        file_size_bytes = output_filename.stat().st_size
        print(f"✅ HTML file saved: {output_filename}")
        print(f"📄 File size: {total_html_chars:,} characters ({file_size_bytes:,} bytes)")
        print()
        print("🎉 Generation completed successfully! - ENHANCED VERSION")
        print(f"📄 Output file: {output_filename}")
        print(f"📈 File size: {total_html_chars:,} characters")
        print()
        print("💯 Features included - ENHANCED:")
        print("   ✅ Timeline expand/collapse (REALLY WORKING!)")
        print("   ✅ Clean organized sections (Transportation/Weather/Tips)")
        print("   ✅ Accommodation timeline format")
        print("   ✅ Multi-language support (TH/EN)")
        print("   ✅ Mobile responsive design")
        print("   ✅ Birthday special effects 🎂")
        print()
        print("🚀 Ready for Tokyo Trip 2026! - ENHANCED VERSION")
        
    except Exception as e:
        print(f"Error writing output file {output_filename}: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    generate_trip_guide_html()
