function initVerbPanel() {
  const escapeHtml = (value) => String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

  const renderVerbPanel = () => {
    const front = document.getElementById('card-front');
    const verbSection = document.getElementById('verb-section');
    const summaryBody = document.getElementById('verb-summary-body');
    const presentBody = document.getElementById('verb-present-body');
    const perfectBody = document.getElementById('verb-perfect-body');
    const pastBody = document.getElementById('verb-past-body');
    if (!front || !verbSection || !summaryBody || !presentBody || !perfectBody || !pastBody) return;

    const currentFront = front.textContent.trim();
    const card = (window.reviewCards || []).find((entry) => entry.front === currentFront);

    if (!card || !card.is_verb || !card.verb_forms_data || !card.verb_forms_data.meta) {
      verbSection.style.display = 'none';
      verbSection.classList.add('hidden');
      summaryBody.innerHTML = '';
      presentBody.innerHTML = '';
      perfectBody.innerHTML = '';
      pastBody.innerHTML = '';
      return;
    }

    const data = card.verb_forms_data;
    const meta = data.meta || {};
    const renderRows = (rows) => (rows || []).map((row) => `<tr class="border-b border-purple-100 last:border-b-0"><td class="px-3 py-2 font-medium">${escapeHtml(row.pronoun || '')}</td><td class="px-3 py-2">${escapeHtml(row.form || '')}</td></tr>`).join('');

    verbSection.style.display = '';
    verbSection.classList.remove('hidden');
    summaryBody.innerHTML = `
      <tr class="border-b border-purple-100"><th class="px-3 py-2 text-left bg-white/70">Verb</th><td class="px-3 py-2 bg-white">${escapeHtml(meta.verb || '')}</td></tr>
      <tr class="border-b border-purple-100"><th class="px-3 py-2 text-left bg-white/70">Meaning</th><td class="px-3 py-2 bg-white">${escapeHtml(meta.meaning || '')}</td></tr>
      <tr><th class="px-3 py-2 text-left bg-white/70">Type</th><td class="px-3 py-2 bg-white">${escapeHtml(meta.type || '')}</td></tr>
    `;
    presentBody.innerHTML = renderRows(data.present_rows);
    perfectBody.innerHTML = `
      <tr class="border-b border-purple-100"><td class="px-3 py-2 font-medium">Participle</td><td class="px-3 py-2">${escapeHtml(meta.participle || '')}</td></tr>
      <tr><td class="px-3 py-2 font-medium">Auxiliary</td><td class="px-3 py-2">${escapeHtml(meta.auxiliary || '')}</td></tr>
    `;
    pastBody.innerHTML = renderRows(data.past_rows);
  };

  const startObserver = () => {
    renderVerbPanel();
    const front = document.getElementById('card-front');
    if (!front) return;
    const observer = new MutationObserver(renderVerbPanel);
    observer.observe(front, { childList: true, characterData: true, subtree: true });
    setInterval(renderVerbPanel, 250);
  };

  startObserver();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initVerbPanel, { once: true });
} else {
  initVerbPanel();
}
