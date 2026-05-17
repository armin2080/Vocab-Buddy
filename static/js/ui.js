// Minimal UI helpers for the server-rendered frontend
document.addEventListener('DOMContentLoaded', function () {
  // Flashcards (weighted selection)
  let rawCards = window.reviewCards || [];
  // If server embedded JSON as a string, try to parse it
  if (typeof rawCards === 'string') {
    try {
      rawCards = JSON.parse(rawCards);
    } catch (e) {
      console.warn('reviewCards JSON parse failed', e);
      rawCards = [];
    }
  }
  const cards = Array.isArray(rawCards) ? rawCards : [];
  let currentCard = null;
  let currentIndex = -1;
  let deck = [];
  let deckPos = -1;
  let flipped = false;
  let autoplayId = null;
  const reviewedSet = new Set();
  let historyStack = [];

  function totalWeight() {
    try {
      return cards.reduce((s, c) => s + (c.weight || 1), 0);
    } catch (e) {
      console.warn('totalWeight error', e);
      return cards.length || 0;
    }
  }

  function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }

  function buildDeck() {
    const built = [];
    cards.forEach((c, idx) => {
      const w = Math.max(1, Math.min(10, Number(c.weight) || 1));
      for (let i = 0; i < w; i++) built.push(idx);
    });
    deck = shuffle(built);
    deckPos = -1;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function renderExamples(lines) {
    const list = document.getElementById('card-examples');
    if (!list) return;
    const items = Array.isArray(lines) ? lines.slice(0, 2) : [];
    list.innerHTML = items.map((line) => `<li class="rounded-md bg-white/70 px-3 py-2 border border-green-100">${escapeHtml(line)}</li>`).join('');
  }

  function renderVerbForms(data) {
    const verbSection = document.getElementById('verb-section');
    const summaryBody = document.getElementById('verb-summary-body');
    const presentBody = document.getElementById('verb-present-body');
    const perfectBody = document.getElementById('verb-perfect-body');
    const pastBody = document.getElementById('verb-past-body');
    window.__verbRenderState = {
      isVerb: !!currentCard.is_verb,
      hasData: !!currentCard.verb_forms_data,
      hasMeta: !!(currentCard.verb_forms_data && currentCard.verb_forms_data.meta),
      hasBodies: !!(summaryBody && presentBody && perfectBody && pastBody),
      front: currentCard.front,
    };

    if (!verbSection || !summaryBody || !presentBody || !pastBody || !perfectBody) return;

    if (!data || !data.meta) {
      verbSection.classList.add('hidden');
      verbSection.style.display = 'none';
      summaryBody.innerHTML = '';
      presentBody.innerHTML = '';
      pastBody.innerHTML = '';
      perfectBody.innerHTML = '';
      return;
    }

    verbSection.classList.remove('hidden');
    verbSection.style.display = '';
    const meta = data.meta || {};
    summaryBody.innerHTML = `
      <tr class="border-b border-purple-100"><th class="px-3 py-2 text-left bg-white/70">Verb</th><td class="px-3 py-2 bg-white">${escapeHtml(meta.verb || '')}</td></tr>
      <tr class="border-b border-purple-100"><th class="px-3 py-2 text-left bg-white/70">Meaning</th><td class="px-3 py-2 bg-white">${escapeHtml(meta.meaning || '')}</td></tr>
      <tr><th class="px-3 py-2 text-left bg-white/70">Type</th><td class="px-3 py-2 bg-white">${escapeHtml(meta.type || '')}</td></tr>
    `;

    const renderRows = (rows) => rows.map((row) => `<tr class="border-b border-purple-100 last:border-b-0"><td class="px-3 py-2 font-medium">${escapeHtml(row.pronoun || '')}</td><td class="px-3 py-2">${escapeHtml(row.form || '')}</td></tr>`).join('');
    presentBody.innerHTML = renderRows(data.present_rows || []);
    perfectBody.innerHTML = `
      <tr class="border-b border-purple-100"><td class="px-3 py-2 font-medium">Participle</td><td class="px-3 py-2">${escapeHtml(meta.participle || '')}</td></tr>
      <tr><td class="px-3 py-2 font-medium">Auxiliary</td><td class="px-3 py-2">${escapeHtml(meta.auxiliary || '')}</td></tr>
    `;
    pastBody.innerHTML = renderRows(data.past_rows || []);
  }

  function showCardByIndex(i, pushHistory = true) {
    if (!cards.length) return;
    currentIndex = i % cards.length;
    currentCard = cards[currentIndex];
    flipped = false;
    const frontEl = document.getElementById('card-front');
    const backEl = document.getElementById('card-back');
    const idxEl = document.getElementById('card-index');
    const pctEl = document.getElementById('card-percent');
    const verbSection = document.getElementById('verb-section');
    const summaryBody = document.getElementById('verb-summary-body');
    const presentBody = document.getElementById('verb-present-body');
    const perfectBody = document.getElementById('verb-perfect-body');
    const pastBody = document.getElementById('verb-past-body');
    frontEl.textContent = currentCard.front;
    backEl.textContent = currentCard.back;
    if (verbSection) {
      verbSection.style.display = currentCard.is_verb ? '' : 'none';
      verbSection.classList.toggle('hidden', !currentCard.is_verb);
    }
    renderExamples(currentCard.examples || []);
    if (currentCard.is_verb && currentCard.verb_forms_data && currentCard.verb_forms_data.meta && summaryBody && presentBody && perfectBody && pastBody) {
      const data = currentCard.verb_forms_data;
      const meta = data.meta || {};
      summaryBody.innerHTML = `
        <tr class="border-b border-purple-100"><th class="px-3 py-2 text-left bg-white/70">Verb</th><td class="px-3 py-2 bg-white">${escapeHtml(meta.verb || '')}</td></tr>
        <tr class="border-b border-purple-100"><th class="px-3 py-2 text-left bg-white/70">Meaning</th><td class="px-3 py-2 bg-white">${escapeHtml(meta.meaning || '')}</td></tr>
        <tr><th class="px-3 py-2 text-left bg-white/70">Type</th><td class="px-3 py-2 bg-white">${escapeHtml(meta.type || '')}</td></tr>
      `;

      const renderRows = (rows) => rows.map((row) => `<tr class="border-b border-purple-100 last:border-b-0"><td class="px-3 py-2 font-medium">${escapeHtml(row.pronoun || '')}</td><td class="px-3 py-2">${escapeHtml(row.form || '')}</td></tr>`).join('');
      presentBody.innerHTML = renderRows(data.present_rows || []);
      perfectBody.innerHTML = `
        <tr class="border-b border-purple-100"><td class="px-3 py-2 font-medium">Participle</td><td class="px-3 py-2">${escapeHtml(meta.participle || '')}</td></tr>
        <tr><td class="px-3 py-2 font-medium">Auxiliary</td><td class="px-3 py-2">${escapeHtml(meta.auxiliary || '')}</td></tr>
      `;
      pastBody.innerHTML = renderRows(data.past_rows || []);
    } else if (summaryBody && presentBody && perfectBody && pastBody) {
      summaryBody.innerHTML = '';
      presentBody.innerHTML = '';
      perfectBody.innerHTML = '';
      pastBody.innerHTML = '';
    }
    // show level as small label
    idxEl.textContent = `${reviewedSet.size + 1} / ${cards.length}`;
    const reviewedPct = Math.round(((reviewedSet.size + 1) / cards.length) * 100);
    if (pctEl) pctEl.textContent = `${reviewedPct}% Complete`;
    document.getElementById('progress-bar').style.width = `${reviewedPct}%`;
    // mark reviewed
    if (currentCard && currentCard.pk) reviewedSet.add(currentCard.pk);
    if (pushHistory) {
      // avoid pushing duplicate consecutive indices
      if (historyStack.length === 0 || historyStack[historyStack.length - 1] !== currentIndex) {
        historyStack.push(currentIndex);
      }
    }
    const reviewedInput = document.getElementById('reviewed-pks-input');
    if (reviewedInput) reviewedInput.value = Array.from(reviewedSet).join(',');
    // reset flip state visually
    const container = document.getElementById('card-container');
    const inner = document.getElementById('card-inner');
    if (container) container.classList.remove('is-flipped');
    if (inner) inner.style.transform = 'rotateY(0deg)';
    const levelBadge = document.getElementById('card-level-badge');
    if (levelBadge) levelBadge.textContent = currentCard.level || '';
  }

  function showPreviousCard() {
    if (!deck.length) return;
    deckPos = Math.max(0, deckPos - 1);
    showCardByIndex(deck[deckPos], false);
  }

  function pickAndShow() {
    if (!cards.length) return;
    if (!deck.length) buildDeck();
    deckPos = (deckPos + 1) % deck.length;
    showCardByIndex(deck[deckPos]);
  }

  function flipCard() {
    if (!currentCard) return;
    flipped = !flipped;
    const container = document.getElementById('card-container');
    const inner = document.getElementById('card-inner');
    if (!container || !inner) return;
    // toggle class for CSS animation
    container.classList.toggle('is-flipped', flipped);
    // also set transform directly for robustness
    if (flipped) {
      inner.style.transform = 'rotateY(180deg)';
    } else {
      inner.style.transform = 'rotateY(0deg)';
    }
  }

  document.getElementById('card-next')?.addEventListener('click', function () { flipCardIfNeeded(false); pickAndShow(); });
  document.getElementById('card-prev')?.addEventListener('click', function () { flipCardIfNeeded(false); showPreviousCard(); });
  document.getElementById('card-flip-zone')?.addEventListener('click', flipCard);

  function flipCardIfNeeded(flag) {
    flipped = flag;
    const container = document.getElementById('card-container');
    const inner = document.getElementById('card-inner');
    if (container) container.classList.remove('is-flipped');
    if (inner) inner.style.transform = 'rotateY(0deg)';
  }

  // Play / Pause autoplay
  // autoplay removed

  // Initial render if cards exist
  try {
    if (cards.length) {
      buildDeck();
      pickAndShow();
    }
  } catch (err) {
    console.error('Flashcards initialization error:', err);
  }

  // Simple search focus for vocabulary page
  const searchInput = document.querySelector('input[name="search"]');
  if (searchInput) {
    const focusBtn = document.getElementById('focus-search');
    if (focusBtn) focusBtn.addEventListener('click', () => searchInput.focus());
  }

  // Quiz form enable/selection handling
  const quizForm = document.getElementById('quiz-form');
  if (quizForm) {
    const submitBtn = document.getElementById('quiz-submit');
    const radios = Array.from(quizForm.querySelectorAll('.option-radio'));
    const labels = Array.from(quizForm.querySelectorAll('.option-label'));

    radios.forEach((r, idx) => {
      r.addEventListener('change', () => {
        if (submitBtn) submitBtn.disabled = false;
        labels.forEach((lab, i) => {
          lab.classList.toggle('ring-ring', i === idx);
        });
      });
    });
  }
});

/* Small CSS helper appended via JS is avoided; styles live in theme.css */
