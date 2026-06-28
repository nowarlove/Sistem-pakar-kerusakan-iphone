/* ── JS utama NST Phone Repair ── */

// ============================================================
// Navigasi halaman
// ============================================================
document.querySelectorAll('.nav-item').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.page;
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('page-' + target).classList.add('active');

    // Muat info model saat halaman dev pertama kali dibuka
    if (target === 'dev' && !window._modelLoaded) {
      loadModelInfo();
    }
  });
});

// ============================================================
// Diagnosis
// ============================================================
const keluhanInput  = document.getElementById('keluhan-input');
const btnDiagnosa   = document.getElementById('btn-diagnosa');
const spinner       = document.getElementById('spinner');
const btnText       = document.getElementById('btn-text');
const normPreview   = document.getElementById('normalized-preview');
const featuresBody  = document.getElementById('features-body');
const resultPanel   = document.getElementById('result-panel');
const fallbackNotice= document.getElementById('fallback-notice');

// State terakhir untuk log pengembangan
window._lastResult = null;

btnDiagnosa.addEventListener('click', runDiagnosis);
keluhanInput.addEventListener('keydown', e => {
  if (e.ctrlKey && e.key === 'Enter') runDiagnosis();
});

async function runDiagnosis() {
  const keluhan = keluhanInput.value.trim();
  if (!keluhan) {
    keluhanInput.focus();
    return;
  }

  // Loading state
  btnDiagnosa.disabled = true;
  spinner.style.display = 'block';
  btnText.textContent = 'Menganalisis...';

  try {
    const res = await fetch('/diagnosa', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ keluhan }),
    });
    const data = await res.json();

    if (!data.success) {
      alert('Error: ' + (data.error || 'Terjadi kesalahan.'));
      return;
    }

    window._lastResult = data;
    renderFeatures(data.features);
    renderResult(data);
    renderNormalized(data.input.normalized);

    // Jika halaman dev sudah terbuka, refresh log
    if (document.getElementById('page-dev').classList.contains('active')) {
      renderLastLog(data);
    }

  } catch (err) {
    alert('Koneksi ke server gagal: ' + err.message);
  } finally {
    btnDiagnosa.disabled = false;
    spinner.style.display = 'none';
    btnText.textContent = 'Diagnosa';
  }
}

// ---- Normalized text preview ----
function renderNormalized(normalized) {
  normPreview.style.display = 'block';
  normPreview.innerHTML = `Teks ternormalisasi: <span>${escHtml(normalized)}</span>`;
}

// ---- Features table ----
function renderFeatures(features) {
  const NORMAL_VALS = ['Normal', '0,8 - 2,2'];
  featuresBody.innerHTML = '';
  Object.entries(features).forEach(([col, val]) => {
    const isActive = !NORMAL_VALS.includes(val);
    const badgeClass = isActive ? 'badge-active' : 'badge-normal';
    featuresBody.innerHTML += `
      <tr>
        <td>${escHtml(col)}</td>
        <td><span class="badge ${badgeClass}">${escHtml(val)}</span></td>
      </tr>`;
  });
}

// ---- Result panel ----
function renderResult(data) {
  fallbackNotice.style.display = data.used_fallback ? 'block' : 'none';

  const topPct   = data.top_percentage;
  const allDiag  = data.all_diagnoses;
  const maxPct   = allDiag[0].percentage;

  let barsHtml = allDiag.map((d, i) => {
    const pct  = d.percentage;
    const w    = maxPct > 0 ? (pct / maxPct * 100).toFixed(1) : 0;
    const cls  = i === 0 ? 'bar-top' : 'bar-low';
    return `
      <div class="bar-row">
        <span class="bar-label" title="${escHtml(d.damage)}">${escHtml(d.damage)}</span>
        <div class="bar-track">
          <div class="bar-fill ${cls}" style="width:${w}%"></div>
        </div>
        <span class="bar-pct">${pct.toFixed(1)}%</span>
      </div>`;
  }).join('');

  resultPanel.innerHTML = `
    <div class="fallback-notice" id="fallback-notice" ${data.used_fallback ? '' : 'style="display:none"'}>
      ⚠ Tidak ada gejala yang terdeteksi. Hasil berdasarkan probabilitas prior empiris.
    </div>
    <div class="top-diagnosis-box">
      <div class="top-diag-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
             fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
      </div>
      <div>
        <div class="top-diag-label">Diagnosis Utama</div>
        <div class="top-diag-name">${escHtml(data.top_diagnosis)}</div>
        <div class="top-diag-pct">Keyakinan: ${topPct.toFixed(1)}% · ${data.active_rules_count} aturan aktif</div>
      </div>
    </div>
    <div class="card-title" style="font-size:12px; color:var(--gray-500); margin-bottom:10px;">
      Distribusi Probabilitas Semua Kelas
    </div>
    <div class="bar-list">${barsHtml}</div>`;
}

// ============================================================
// Model Info (Halaman Pengembangan)
// ============================================================
async function loadModelInfo() {
  window._modelLoaded = true;
  try {
    const res  = await fetch('/model-info');
    const data = await res.json();
    renderModelStats(data);
    renderBeliefTable(data.rules);
    renderPriorTable(data.class_priors);
    // Render log terakhir jika ada
    if (window._lastResult) renderLastLog(window._lastResult);
  } catch (err) {
    document.getElementById('dev-content').innerHTML =
      `<p style="color:var(--danger)">Gagal memuat info model: ${err.message}</p>`;
  }
}

function renderModelStats(data) {
  document.getElementById('stat-rules').textContent   = data.total_rules;
  document.getElementById('stat-classes').textContent = data.total_classes;
  // Hitung total dimensi (total hypotheses)
  const dims = data.rules.reduce((s, r) => s + r.hypotheses.length, 0);
  document.getElementById('stat-dims').textContent    = dims;
}

function renderBeliefTable(rules) {
  const tbody = document.getElementById('belief-tbody');
  tbody.innerHTML = '';
  rules.forEach(rule => {
    rule.hypotheses.forEach((hyp, i) => {
      tbody.innerHTML += `
        <tr>
          ${i === 0 ? `<td rowspan="${rule.hypotheses.length}"><b>${escHtml(rule.symptom_col)}</b><br>
            <small style="color:var(--gray-400)">${escHtml(rule.symptom_val)}</small></td>` : ''}
          <td>${escHtml(hyp.damage)}</td>
          <td class="belief-val">${hyp.optimal_belief.toFixed(4)}</td>
          ${i === 0 ? `<td rowspan="${rule.hypotheses.length}" class="theta-val">${rule.uncertainty_theta.toFixed(4)}</td>` : ''}
        </tr>`;
    });
  });
}

function renderPriorTable(priors) {
  const tbody   = document.getElementById('prior-tbody');
  const sorted  = Object.entries(priors).sort((a, b) => b[1] - a[1]);
  const maxPrior = sorted[0][1];
  tbody.innerHTML = sorted.map(([cls, p]) => {
    const w = (p / maxPrior * 100).toFixed(1);
    const pct = (p * 100).toFixed(2);
    return `
      <tr>
        <td>${escHtml(cls)}</td>
        <td style="width:150px">
          <div style="display:flex;align-items:center;gap:6px">
            <div class="prior-bar-track" style="flex:1">
              <div class="prior-bar-fill" style="width:${w}%"></div>
            </div>
          </div>
        </td>
        <td style="font-weight:600;color:var(--success)">${pct}%</td>
      </tr>`;
  }).join('');
}

// ---- Log Inferensi Terakhir ----
function renderLastLog(data) {
  const container = document.getElementById('last-inference-log');
  const devLog    = data.dev_log;

  // Teks masuk & fitur
  let html = `
    <div class="log-card">
      <div class="log-header">📋 Log Inferensi Terakhir</div>
      <div class="log-body">

        <div class="log-section-title">Input</div>
        <div class="mass-grid">
          <div class="mass-row"><span class="mass-key">Teks asli</span>
            <span class="mass-val">${escHtml(data.input.raw)}</span></div>
          <div class="mass-row"><span class="mass-key">Ternormalisasi</span>
            <span class="mass-val">${escHtml(data.input.normalized)}</span></div>
        </div>

        <div class="log-section-title">Gejala Aktif (${devLog.active_rules.length} aturan terpicu)</div>`;

  if (devLog.active_rules.length === 0) {
    html += `<div style="color:var(--gray-400);font-size:12px;padding:4px 0">
               Tidak ada gejala aktif — menggunakan prior empiris sebagai fallback.
             </div>`;
  } else {
    devLog.active_rules.forEach(rule => {
      html += `<div class="log-rule-item">
        <div class="rule-head">${escHtml(rule.symptom_col)} = ${escHtml(rule.symptom_val)}</div>`;
      rule.hypotheses.forEach(hyp => {
        html += `<div class="hyp-row">
          <span>${escHtml(hyp.damage)}</span>
          <span class="belief-val">m = ${hyp.optimal_belief.toFixed(4)}</span>
        </div>`;
      });
      html += `<div class="hyp-row" style="color:var(--gray-400)">
                 <span>Θ (Uncertainty)</span>
                 <span>m = ${rule.uncertainty_theta.toFixed(4)}</span>
               </div>
             </div>`;
    });
  }

  // Langkah kombinasi DS
  if (devLog.combination_steps.length > 1) {
    html += `<div class="log-section-title">Langkah Kombinasi Dempster-Shafer</div>
             <div class="mass-grid">`;
    devLog.combination_steps.forEach((step, i) => {
      html += `<div class="mass-row" style="flex-direction:column;align-items:flex-start;gap:3px">
                 <span class="mass-key" style="font-weight:600">Sumber ${i+1}: ${escHtml(step.source)}</span>`;
      Object.entries(step.mass_function).forEach(([k, v]) => {
        html += `<span style="color:var(--gray-500)">  m(${escHtml(k)}) = <b style="color:var(--primary-dark)">${v}</b></span>`;
      });
      html += `</div>`;
    });
    html += `</div>`;
  }

  // Mass function gabungan akhir
  if (Object.keys(devLog.final_mass_combined).length > 0) {
    html += `<div class="log-section-title">Fungsi Massa Gabungan (Setelah Kombinasi DS)</div>
             <div class="mass-grid">`;
    Object.entries(devLog.final_mass_combined).forEach(([k, v]) => {
      html += `<div class="mass-row">
                 <span class="mass-key">m(${escHtml(k)})</span>
                 <span class="mass-val">${v}</span>
               </div>`;
    });
    html += `</div>`;
  }

  // Probabilitas Pignistik
  html += `<div class="log-section-title">Probabilitas Pignistik BetP (Hasil Akhir)</div>
           <div class="mass-grid">`;
  const sortedProbs = Object.entries(devLog.pignistic_probabilities)
                            .sort((a, b) => b[1] - a[1]);
  sortedProbs.forEach(([cls, p]) => {
    html += `<div class="mass-row">
               <span class="mass-key">${escHtml(cls)}</span>
               <span class="mass-val">${(p * 100).toFixed(2)}%</span>
             </div>`;
  });
  html += `</div>
      </div>
    </div>`;

  container.innerHTML = html;
}

// ============================================================
// Utilities
// ============================================================
function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
