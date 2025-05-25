// GPT Trip Utility JS

function toggleLang() {
  const body = document.body;
  body.classList.toggle('lang-th');
  body.classList.toggle('lang-en');
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function convertJPYtoTHB(rate = 0.25) {
  document.querySelectorAll('[data-jpy]').forEach(el => {
    const jpy = parseFloat(el.getAttribute('data-jpy'));
    if (!isNaN(jpy)) {
      const thb = Math.round(jpy * rate).toLocaleString();
      const span = document.createElement('span');
      span.className = 'thb-estimate';
      span.style.marginLeft = '0.5em';
      span.style.color = '#666';
      span.textContent = `(~฿${thb})`;
      el.appendChild(span);
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  convertJPYtoTHB();
});
