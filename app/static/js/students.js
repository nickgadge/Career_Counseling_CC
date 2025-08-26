// static/js/students.js
(function () {
  const steps = Array.from(document.querySelectorAll('.step'));
  const total = steps.length;
  const nextBtn = document.getElementById('nextBtn');
  const prevBtn = document.getElementById('prevBtn');
  const submitBtn = document.getElementById('submitBtn');
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');
  const liveHint = document.getElementById('liveHint');

  const catHints = {
    logic: "Tip: Logical thinking builds engineering/data strengths.",
    arts: "Tip: Creativity suits design, media & performing arts.",
    science: "Tip: Curiosity → science, medical & research pathways.",
    social: "Tip: Communication & leadership → teaching/civil services.",
    commerce: "Tip: Money & markets → finance, business & management."
  };

  let curr = 0;

  function showStep(i) {
    steps.forEach((s, idx) => {
      s.style.display = (idx === i) ? 'block' : 'none';
    });
    prevBtn.disabled = (i === 0);
    nextBtn.classList.toggle('d-none', i === total - 1);
    submitBtn.classList.toggle('d-none', i !== total - 1);
    updateProgress();
  }

  function updateProgress() {
    const pct = Math.round(((curr + 1) / (total + 1)) * 100); // +1 accounts info card
    progressBar.style.width = pct + '%';
    progressText.textContent = pct + '%';
  }

  function answered(stepEl) {
    // check if current step has any selected/filled input
    const name = stepEl.querySelector('input[type="radio"][name^="q"]');
    const slider = stepEl.querySelector('input[type="range"][name^="q"]');
    const checks = stepEl.querySelectorAll('input[type="checkbox"][name^="q"]');

    let ok = false;
    if (name) ok = stepEl.querySelector('input[type="radio"]:checked') !== null;
    else if (slider) ok = true; // slider always has a value
    else if (checks && checks.length) {
      ok = Array.from(checks).some(c => c.checked);
    }
    return ok;
  }

  nextBtn.addEventListener('click', () => {
    const stepEl = steps[curr];
    if (!answered(stepEl)) {
      // glow warning
      stepEl.classList.add('step-shake');
      setTimeout(() => stepEl.classList.remove('step-shake'), 500);
      return;
    }
    curr = Math.min(curr + 1, total - 1);
    showStep(curr);
  });

  prevBtn.addEventListener('click', () => {
    curr = Math.max(curr - 1, 0);
    showStep(curr);
  });

  // Live glow + hint on change
  steps.forEach(step => {
    step.addEventListener('change', () => {
      step.classList.add('answered');
      const cat = step.getAttribute('data-category');
      step.classList.add('cat-' + cat);
      if (catHints[cat]) liveHint.textContent = catHints[cat];
      setTimeout(() => (liveHint.textContent = ""), 2500);
    });
  });

  // init
  showStep(curr);
})();
