<script>
        document.addEventListener("DOMContentLoaded", function () {
            // --- Collapsible Sections ---
            document.querySelectorAll(".info-toggle, .note-toggle").forEach(button => {
                const detail = button.nextElementSibling;
                if (detail && (detail.classList.contains('info-detail') || detail.classList.contains('note-detail'))) {
                    // Start collapsed
                    button.classList.add("collapsed");
                    detail.classList.add("collapsed");

                    button.addEventListener("click", (e) => {
                        // Prevent link clicks inside toggle from triggering collapse
                        if (e.target.tagName === 'A') return;

                        button.classList.toggle("collapsed");
                        detail.classList.toggle("collapsed");
                    });

                    // Allow keyboard activation
                    button.setAttribute('role', 'button');
                    button.setAttribute('tabindex', '0');
                    button.addEventListener('keydown', (e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault(); // Prevent page scroll on Space
                            button.click();
                        }
                    });
                } else {
                    console.warn("Collapsible toggle found without a matching detail element:", button);
                }
            });

            // --- Language Switching ---
            const langButtons = document.querySelectorAll('.language-switcher button');
            const body = document.body;
            // Get saved language or default to Thai
            let currentLang = localStorage.getItem('tripLanguage') || 'th';

            function setLanguage(lang) {
                if (lang !== 'th' && lang !== 'en') lang = 'th'; // Fallback
                localStorage.setItem('tripLanguage', lang);
                currentLang = lang;
                body.className = `lang-${lang}`; // Set class on body

                // Update button active state
                langButtons.forEach(btn => {
                    btn.classList.toggle('active', btn.dataset.lang === lang);
                });

                // Update Back-to-Top text
                const backToTopBtn = document.querySelector('.back-to-top');
                if (backToTopBtn) {
                    // Find the correct span to update
                    const textSpan = backToTopBtn.querySelector(lang === 'th' ? '.th' : '.en');
                    if (textSpan) {
                        // No need to set textContent here, CSS handles visibility
                    }
                }
                // Update page title
                const titleTh = "เที่ยวญี่ปุ่น Porjai: Birthday Trip 2026";
                const titleEn = "Porjai's Japan Trip: Birthday Adventure 2026";
                document.title = lang === 'th' ? titleTh : titleEn;
            }

            langButtons.forEach(button => {
                button.addEventListener('click', () => {
                    setLanguage(button.dataset.lang);
                });
            });

            // Set initial language on load
            setLanguage(currentLang);

            // --- Currency Conversion (JPY to THB) ---
            const jpyToThbRate = 0.2346; // 100 JPY ≈ 23.46 THB (Update as needed)

            const convertCurrency = () => {
                document.querySelectorAll('[data-jpy]').forEach(el => {
                    const jpyString = el.dataset.jpy.replace(/,/g, ''); // Remove commas
                    const jpy = parseFloat(jpyString);
                    if (!isNaN(jpy)) {
                        const thb = (jpy * jpyToThbRate).toFixed(0); // Calculate and round to nearest Baht
                        // Display both JPY and THB
                        const jpyFormatted = `¥${jpy.toLocaleString('en-US')}`;
                        const thbFormatted = `฿${parseInt(thb).toLocaleString('en-US')}`;

                        // Find the right place to display THB. If a span exists, use it.
                        let thbSpan = el.querySelector('.thb-amount');
                        if (!thbSpan) {
                            // Check if the element itself should display the THB amount (e.g., in a table cell)
                            if (el.tagName === 'TD' || el.tagName === 'STRONG') {
                                el.innerHTML = `${thbFormatted}`; // Directly set THB if it's the main content
                            } else {
                                // Otherwise, append THB in parentheses after JPY
                                thbSpan = document.createElement('span');
                                thbSpan.className = 'thb-amount';
                                el.innerHTML = `${jpyFormatted} <span class="thb-amount">(${thbFormatted})</span>`;
                            }
                        } else {
                            // Update existing span if needed
                            el.innerHTML = `${jpyFormatted} <span class="thb-amount">(${thbFormatted})</span>`;
                        }

                    } else {
                        console.warn("Invalid JPY value found:", el.dataset.jpy);
                    }
                });
                // Update the rate display text
                const rateDisplay = document.getElementById('exchange-rate-info');
                if (rateDisplay) {
                    const rateTextTh = `อัตราแลกเปลี่ยน: 100 เยน ≈ ${(jpyToThbRate * 100).toFixed(2)} บาท (ตรวจสอบอัตราปัจจุบัน)`;
                    const rateTextEn = `Exchange Rate: 100 Yen ≈ ${(jpyToThbRate * 100).toFixed(2)} Baht (Check current rates)`;
                    rateDisplay.querySelector('.th').textContent = rateTextTh;
                    rateDisplay.querySelector('.en').textContent = rateTextEn;
                }
            };


            convertCurrency(); // Run on load

            // --- Back to Top Button Visibility ---
            const backToTopBtn = document.querySelector('.back-to-top');
            if (backToTopBtn) {
                window.addEventListener('scroll', () => {
                    if (window.scrollY > 300) { // Show after scrolling down 300px
                        backToTopBtn.classList.add('visible');
                    } else {
                        backToTopBtn.classList.remove('visible');
                    }
                });
            }

        }); // End DOMContentLoaded
    </script>
