import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NeuroScan AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide all default Streamlit chrome
st.markdown("""
<style>
#MainMenu, header, footer, [data-testid="stToolbar"],
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }
.stApp { background: #070d1a; }
.block-container { padding: 0 !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>NeuroScan AI</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
:root {
  --bg:        #070d1a;
  --surface:   #0b1628;
  --elevated:  #0f1e38;
  --border:    #112240;
  --border-hi: #1a3560;
  --cyan:      #00d4ff;
  --cyan-dim:  #0090b3;
  --cyan-glow: rgba(0,212,255,.18);
  --green:     #00e5a0;
  --amber:     #ffb547;
  --red:       #ff5e7a;
  --text-1:    #e8f4ff;
  --text-2:    #7a99c2;
  --text-3:    #3a5070;
  --mono:      'IBM Plex Mono', monospace;
  --sans:      'DM Sans', sans-serif;
  --r-sm:      8px;
  --r-md:      14px;
  --r-lg:      20px;
}
*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
html { font-size:16px; }
body {
  font-family: var(--sans);
  background: var(--bg);
  color: var(--text-1);
  min-height: 100vh;
  overflow-x: hidden;
}
.shell {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}
body::before {
  content:'';
  position: fixed; inset:0;
  background-image:
    linear-gradient(rgba(0,212,255,.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,.04) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  z-index: 0;
}
body::after {
  content:'';
  position: fixed;
  top:-30%; left:50%; transform:translateX(-50%);
  width:900px; height:600px;
  background: radial-gradient(ellipse at center, rgba(0,212,255,.07) 0%, transparent 65%);
  pointer-events: none;
  z-index: 0;
}
.shell { position: relative; z-index:1; }
nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 0;
  border-bottom: 1px solid var(--border);
}
.nav-brand { display: flex; align-items: center; gap:.75rem; }
.nav-logo {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, var(--cyan-dim), var(--cyan));
  border-radius: 10px;
  display: flex; align-items:center; justify-content:center;
  font-size:1.1rem;
}
.nav-title { font-size: 1.05rem; font-weight: 700; letter-spacing: -.01em; color: var(--text-1); }
.nav-title em { color: var(--cyan); font-style:normal; }
.nav-badges { display:flex; gap:.5rem; flex-wrap:wrap; }
.badge {
  font-family: var(--mono);
  font-size: .65rem; font-weight: 500;
  padding: .22rem .65rem;
  border-radius: 99px;
  border: 1px solid var(--border-hi);
  background: var(--surface);
  color: var(--text-2);
  letter-spacing: .04em;
}
main {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  padding: 2rem 0;
  align-items: start;
}
@media(max-width:820px) {
  main { grid-template-columns:1fr; }
  .shell { padding:0 1rem; }
}
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  overflow: hidden;
}
.card-header {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border);
  display: flex; align-items:center; gap:.6rem;
}
.card-header-icon {
  font-size:.8rem; width:28px; height:28px;
  background: var(--elevated); border-radius: 8px;
  display:flex; align-items:center; justify-content:center;
}
.card-header-title {
  font-size:.78rem; font-weight:700;
  letter-spacing:.1em; text-transform:uppercase; color: var(--text-2);
}
.card-body { padding:1.25rem; }
.upload-zone {
  position: relative;
  border: 1.5px dashed var(--border-hi);
  border-radius: var(--r-md);
  background: var(--elevated);
  cursor: pointer;
  transition: border-color .2s, background .2s;
  overflow: hidden;
  min-height: 200px;
  display: flex; align-items:center; justify-content:center;
}
.upload-zone:hover, .upload-zone.drag-over {
  border-color: var(--cyan);
  background: rgba(0,212,255,.04);
}
.upload-zone::after {
  content:'';
  position:absolute;
  top:0; left:0; right:0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--cyan), transparent);
  animation: scanline 2.8s ease-in-out infinite;
  opacity: 0;
  transition: opacity .3s;
}
.upload-zone.active-scan::after { opacity:1; }
@keyframes scanline {
  0%   { top:0%;   opacity:0; }
  5%   { opacity:1; }
  95%  { opacity:1; }
  100% { top:100%; opacity:0; }
}
.upload-idle {
  display:flex; flex-direction:column;
  align-items:center; gap:.75rem;
  padding:2.5rem 1.5rem; text-align:center;
}
.upload-icon {
  width:56px; height:56px;
  background: linear-gradient(135deg, rgba(0,212,255,.12), rgba(0,212,255,.04));
  border: 1px solid rgba(0,212,255,.2);
  border-radius: 14px;
  display:flex; align-items:center; justify-content:center;
  font-size:1.5rem;
}
.upload-idle h3 { font-size:.95rem; font-weight:600; color:var(--text-1); }
.upload-idle p  { font-size:.78rem; color:var(--text-3); font-family:var(--mono); }
.btn-browse {
  margin-top:.25rem; padding:.45rem 1.1rem;
  border:1px solid var(--cyan-dim); background:transparent;
  color:var(--cyan); font-family:var(--sans);
  font-size:.8rem; font-weight:600; border-radius:8px;
  cursor:pointer; transition:background .15s, color .15s;
}
.btn-browse:hover { background:var(--cyan); color:var(--bg); }
#fileInput { display:none; }
.preview-wrap { width:100%; position:relative; display:none; }
.preview-wrap img { width:100%; display:block; border-radius: var(--r-md); }
.preview-overlay {
  position:absolute; inset:0;
  background:linear-gradient(to top, rgba(7,13,26,.85) 0%, transparent 50%);
  border-radius: var(--r-md);
  display:flex; align-items:flex-end; padding:.85rem;
}
.preview-filename { font-family:var(--mono); font-size:.72rem; color:var(--cyan); letter-spacing:.04em; word-break:break-all; }
.btn-clear {
  position:absolute; top:.6rem; right:.6rem;
  width:28px; height:28px;
  background:rgba(7,13,26,.7); border:1px solid var(--border-hi);
  border-radius:6px; color:var(--text-2); font-size:.85rem;
  cursor:pointer; display:flex; align-items:center; justify-content:center;
  transition:background .15s;
}
.btn-clear:hover { background:var(--red); color:#fff; border-color:var(--red); }
.btn-predict {
  width:100%; margin-top:1rem; padding:.8rem;
  background:linear-gradient(135deg, #0369a1 0%, var(--cyan) 100%);
  color:#fff; font-family:var(--sans);
  font-size:.9rem; font-weight:700;
  letter-spacing:.06em; text-transform:uppercase;
  border:none; border-radius:var(--r-sm);
  cursor:pointer; transition:opacity .15s, transform .1s;
  position:relative; overflow:hidden;
}
.btn-predict:disabled { opacity:.4; cursor:not-allowed; }
.btn-predict:not(:disabled):hover { opacity:.9; }
.btn-predict:not(:disabled):active { transform:scale(.99); }
.btn-predict.loading::after {
  content:'';
  position:absolute; inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.25),transparent);
  animation: shimmer 1.2s infinite;
}
@keyframes shimmer { 0%{transform:translateX(-100%)} 100%{transform:translateX(100%)} }
#resultPanel { display:none; }
.diag-card {
  background: var(--elevated); border:1px solid var(--border-hi);
  border-radius:var(--r-md); padding:1.25rem;
  display:grid; grid-template-columns:1fr auto;
  align-items:center; gap:1rem; margin-bottom:1rem;
}
.diag-label { font-size:.68rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; color:var(--text-3); margin-bottom:.35rem; }
.diag-name { font-size:1.6rem; font-weight:700; color:var(--text-1); letter-spacing:-.02em; text-transform:capitalize; }
.diag-sub  { font-size:.75rem; color:var(--text-2); margin-top:.25rem; }
.gauge-wrap { text-align:center; flex-shrink:0; }
.gauge-svg  { display:block; }
.gauge-num  { font-family:var(--mono); font-size:.9rem; font-weight:600; fill: var(--text-1); }
.gauge-unit { font-size:.55rem; fill:var(--text-3); font-family:var(--mono); }
.conf-pill {
  display:inline-flex; align-items:center; gap:.4rem;
  padding:.3rem .75rem; border-radius:99px;
  font-size:.72rem; font-weight:600; letter-spacing:.04em; margin-top:.5rem;
}
.conf-pill.high { background:rgba(0,229,160,.12); color:var(--green); border:1px solid rgba(0,229,160,.25); }
.conf-pill.mid  { background:rgba(255,181,71,.12); color:var(--amber); border:1px solid rgba(255,181,71,.25); }
.conf-pill.low  { background:rgba(255,94,122,.12); color:var(--red);   border:1px solid rgba(255,94,122,.25); }
.prob-section { margin-bottom:1rem; }
.prob-row { display:grid; grid-template-columns:90px 1fr 48px; align-items:center; gap:.75rem; margin-bottom:.65rem; }
.prob-cls  { font-size:.75rem; font-weight:500; color:var(--text-2); text-align:right; text-transform:capitalize; }
.prob-cls.active { color:var(--text-1); font-weight:700; }
.prob-track { background:var(--border); border-radius:99px; height:6px; position:relative; overflow:hidden; }
.prob-fill  { position:absolute; top:0; left:0; height:100%; border-radius:99px; background:linear-gradient(90deg, var(--cyan-dim), var(--cyan)); transition: width .6s cubic-bezier(.4,0,.2,1); }
.prob-fill.active { background:linear-gradient(90deg, #0369a1, var(--cyan)); }
.prob-pct  { font-family:var(--mono); font-size:.7rem; color:var(--text-3); text-align:right; }
.prob-pct.active { color:var(--cyan); font-weight:600; }
#explanationSection { grid-column: 1 / -1; display:none; }
.img-compare { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
@media(max-width:600px){ .img-compare { grid-template-columns:1fr; } }
.img-panel { position:relative; }
.img-panel img { width:100%; display:block; border-radius:var(--r-sm); }
.img-panel-label {
  position:absolute; bottom:0; left:0; right:0;
  padding:.6rem .85rem;
  background:linear-gradient(to top, rgba(7,13,26,.9) 0%, transparent 100%);
  border-radius:0 0 var(--r-sm) var(--r-sm);
  font-size:.7rem; font-weight:600; letter-spacing:.1em; text-transform:uppercase; color:var(--text-2);
  display:flex; align-items:center; gap:.4rem;
}
.img-panel-dot { width:6px; height:6px; border-radius:50%; }
.heatmap-legend { margin-top:.75rem; display:flex; align-items:center; gap:.75rem; }
.legend-bar { flex:1; height:6px; border-radius:99px; background:linear-gradient(90deg,#0000ff,#00ffff,#00ff00,#ffff00,#ff0000); }
.legend-label { font-size:.65rem; font-family:var(--mono); color:var(--text-3); }
#loadingOverlay {
  display:none; position:fixed; inset:0;
  background:rgba(7,13,26,.7); backdrop-filter:blur(6px); z-index:100;
  flex-direction:column; align-items:center; justify-content:center; gap:1.25rem;
}
#loadingOverlay.show { display:flex; }
.spinner { width:60px; height:60px; border-radius:50%; border: 3px solid var(--border-hi); border-top-color: var(--cyan); animation: spin .8s linear infinite; }
@keyframes spin { to { transform:rotate(360deg); } }
.loading-steps { display:flex; flex-direction:column; align-items:center; gap:.35rem; }
.loading-step { font-size:.7rem; font-family:var(--mono); color:var(--text-3); opacity:0; transition: opacity .3s, color .3s; }
.loading-step.done   { opacity:1; color:var(--green); }
.loading-step.active { opacity:1; color:var(--cyan); }
.toast {
  position:fixed; bottom:1.5rem; right:1.5rem;
  background:var(--surface); border:1px solid var(--border-hi); border-radius:10px;
  padding:.85rem 1.1rem; display:flex; align-items:center; gap:.65rem;
  font-size:.82rem; font-weight:500;
  box-shadow:0 8px 32px rgba(0,0,0,.5);
  transform:translateY(20px); opacity:0; transition:transform .3s, opacity .3s;
  z-index:200; pointer-events:none; max-width:360px;
}
.toast.show { transform:translateY(0); opacity:1; }
.toast.success { border-color:rgba(0,229,160,.3); }
.toast.error   { border-color:rgba(255,94,122,.3); }
.disclaimer {
  grid-column:1/-1;
  background:rgba(255,181,71,.05); border:1px solid rgba(255,181,71,.15);
  border-radius:var(--r-sm); padding:.75rem 1rem;
  font-size:.72rem; color: #a07830;
  display:flex; align-items:flex-start; gap:.6rem; line-height:1.6;
}
footer {
  border-top:1px solid var(--border); padding:1.25rem 0;
  display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:.5rem;
}
.footer-left { font-size:.72rem; color:var(--text-3); font-family:var(--mono); }
.footer-right { display:flex; gap:1rem; }
.footer-stat  { font-size:.68rem; font-family:var(--mono); color:var(--text-3); display:flex; align-items:center; gap:.35rem; }
.footer-dot   { width:5px; height:5px; border-radius:50%; background:var(--green); animation: pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(.8)} }
.empty-state { display:flex; flex-direction:column; align-items:center; justify-content:center; padding:3rem 1.5rem; text-align:center; gap:.75rem; }
.empty-icon  { font-size:2rem; opacity:.25; }
.empty-text  { font-size:.8rem; color:var(--text-3); max-width:200px; line-height:1.6; }
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--border-hi); border-radius:99px; }
</style>
</head>
<body>

<div id="loadingOverlay">
  <div class="spinner"></div>
  <div class="loading-steps">
    <div class="loading-step" id="step1">&#x2B21; Preprocessing MRI image&hellip;</div>
    <div class="loading-step" id="step2">&#x2B21; Running CNN inference&hellip;</div>
    <div class="loading-step" id="step3">&#x2B21; Computing Grad-CAM heatmap&hellip;</div>
    <div class="loading-step" id="step4">&#x2B21; Assembling results&hellip;</div>
  </div>
</div>

<div class="toast" id="toast">
  <span id="toastIcon"></span>
  <span id="toastMsg"></span>
</div>

<div class="shell">

  <nav>
    <div class="nav-brand">
      <div class="nav-logo">&#x1F9E0;</div>
      <div class="nav-title">Neuro<em>Scan</em> AI</div>
    </div>
    <div class="nav-badges">
      <span class="badge">TensorFlow</span>
      <span class="badge">FastAPI</span>
      <span class="badge">Grad-CAM</span>
      <span class="badge">v1.0</span>
    </div>
  </nav>

  <main>

    <!-- LEFT -->
    <div style="display:flex;flex-direction:column;gap:1rem;">

      <div class="card">
        <div class="card-header">
          <div class="card-header-icon">&#x1F4E4;</div>
          <div class="card-header-title">MRI Input</div>
        </div>
        <div class="card-body">
          <div class="upload-zone" id="uploadZone"
               onclick="document.getElementById('fileInput').click()"
               ondragover="handleDragOver(event)"
               ondragleave="handleDragLeave(event)"
               ondrop="handleDrop(event)">
            <div class="upload-idle" id="uploadIdle">
              <div class="upload-icon">&#x1FAF1;</div>
              <h3>Drop MRI scan here</h3>
              <p>JPG &middot; JPEG &middot; PNG &middot; Max 200 MB</p>
              <button class="btn-browse" onclick="event.stopPropagation();document.getElementById('fileInput').click()">Browse files</button>
            </div>
            <div class="preview-wrap" id="previewWrap">
              <img id="previewImg" src="" alt="MRI preview"/>
              <div class="preview-overlay">
                <span class="preview-filename" id="previewFilename"></span>
              </div>
              <button class="btn-clear" id="clearBtn" onclick="event.stopPropagation();clearFile()" title="Remove">&#x2715;</button>
            </div>
          </div>
          <input type="file" id="fileInput" accept=".jpg,.jpeg,.png" onchange="handleFile(this.files[0])"/>
          <button class="btn-predict" id="predictBtn" disabled onclick="runPrediction()">Run Analysis</button>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-header-icon">&#x2139;&#xFE0F;</div>
          <div class="card-header-title">Classification Classes</div>
        </div>
        <div class="card-body" style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem;">
          <div style="background:var(--elevated);border-radius:8px;padding:.65rem .85rem;"><div style="font-size:.65rem;color:var(--text-3);font-family:var(--mono);letter-spacing:.06em;margin-bottom:.2rem;">01</div><div style="font-size:.82rem;font-weight:600;">Glioma</div></div>
          <div style="background:var(--elevated);border-radius:8px;padding:.65rem .85rem;"><div style="font-size:.65rem;color:var(--text-3);font-family:var(--mono);letter-spacing:.06em;margin-bottom:.2rem;">02</div><div style="font-size:.82rem;font-weight:600;">Meningioma</div></div>
          <div style="background:var(--elevated);border-radius:8px;padding:.65rem .85rem;"><div style="font-size:.65rem;color:var(--text-3);font-family:var(--mono);letter-spacing:.06em;margin-bottom:.2rem;">03</div><div style="font-size:.82rem;font-weight:600;">Pituitary</div></div>
          <div style="background:var(--elevated);border-radius:8px;padding:.65rem .85rem;"><div style="font-size:.65rem;color:var(--text-3);font-family:var(--mono);letter-spacing:.06em;margin-bottom:.2rem;">04</div><div style="font-size:.82rem;font-weight:600;">No Tumor</div></div>
        </div>
      </div>

    </div>

    <!-- RIGHT -->
    <div style="display:flex;flex-direction:column;gap:1rem;">

      <div class="card" id="emptyCard">
        <div class="card-body">
          <div class="empty-state">
            <div class="empty-icon">&#x1F52C;</div>
            <div class="empty-text">Upload an MRI scan and click Run Analysis to see results here.</div>
          </div>
        </div>
      </div>

      <div id="resultPanel">
        <div class="card" style="margin-bottom:1rem;">
          <div class="card-header">
            <div class="card-header-icon">&#x1F4CB;</div>
            <div class="card-header-title">Diagnosis</div>
          </div>
          <div class="card-body">
            <div class="diag-card">
              <div>
                <div class="diag-label">Predicted Class</div>
                <div class="diag-name" id="diagName">&#x2014;</div>
                <div class="diag-sub" id="diagSub"></div>
                <div id="confPill" class="conf-pill high" style="margin-top:.65rem;">
                  <span id="confPillIcon">&#x25CF;</span>
                  <span id="confPillText">&#x2014;</span>
                </div>
              </div>
              <div class="gauge-wrap">
                <svg class="gauge-svg" width="110" height="80" viewBox="0 0 110 80">
                  <path d="M15,70 A40,40 0 0,1 95,70" fill="none" stroke="#112240" stroke-width="7" stroke-linecap="round"/>
                  <path id="gaugeFill" d="M15,70 A40,40 0 0,1 95,70" fill="none" stroke="#00d4ff" stroke-width="7" stroke-linecap="round" stroke-dasharray="126" stroke-dashoffset="126" style="transition:stroke-dashoffset .8s cubic-bezier(.4,0,.2,1),stroke .4s"/>
                  <text id="gaugeNum" x="55" y="62" text-anchor="middle" class="gauge-num">0%</text>
                  <text x="55" y="73" text-anchor="middle" class="gauge-unit">CONFIDENCE</text>
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-header-icon">&#x1F4CA;</div>
            <div class="card-header-title">Class Probabilities</div>
          </div>
          <div class="card-body prob-section" id="probSection"></div>
        </div>
      </div>

    </div>

    <!-- FULL WIDTH: Explanation -->
    <div class="card" id="explanationSection">
      <div class="card-header">
        <div class="card-header-icon">&#x1F50D;</div>
        <div class="card-header-title">Model Explanation &mdash; Grad-CAM</div>
      </div>
      <div class="card-body">
        <p style="font-size:.78rem;color:var(--text-2);margin-bottom:1rem;line-height:1.6;">
          Gradient-weighted Class Activation Mapping highlights regions the model focused on.
          Warmer colours (red &rarr; yellow) indicate higher activation.
        </p>
        <div class="img-compare">
          <div class="img-panel">
            <img id="origImg" src="" alt="Original MRI"/>
            <div class="img-panel-label"><span class="img-panel-dot" style="background:var(--cyan)"></span>Original MRI</div>
          </div>
          <div class="img-panel">
            <img id="camImg" src="" alt="Grad-CAM"/>
            <div class="img-panel-label"><span class="img-panel-dot" style="background:var(--red)"></span>Grad-CAM Heatmap</div>
          </div>
        </div>
        <div class="heatmap-legend">
          <span class="legend-label">Low</span>
          <div class="legend-bar"></div>
          <span class="legend-label">High activation</span>
        </div>
      </div>
    </div>

    <!-- Disclaimer -->
    <div class="disclaimer">
      <span>&#x26A0;</span>
      <span><strong>Research use only.</strong> This tool is not a substitute for professional medical diagnosis. Always consult a qualified radiologist or physician for clinical decisions.</span>
    </div>

  </main>

  <footer>
    <div class="footer-left">NeuroScan AI &nbsp;&middot;&nbsp; Final Year Engineering Project &nbsp;&middot;&nbsp; 2024</div>
    <div class="footer-right">
      <div class="footer-stat"><div class="footer-dot"></div>Backend connected</div>
      <div class="footer-stat">4 classes &nbsp;&middot;&nbsp; ResNet50 + Grad-CAM</div>
    </div>
  </footer>

</div>

<script>
let currentFile = null;
let currentBlob = null;

const API_URL =
    "https://your-render-backend.onrender.com";

function handleFile(file) {
  if (!file) return;
  if (!['image/jpeg','image/jpg','image/png'].includes(file.type)) {
    showToast('error','&#x274C;','Only JPG / JPEG / PNG files are supported.');
    return;
  }
  currentFile = file;
  if (currentBlob) URL.revokeObjectURL(currentBlob);
  currentBlob = URL.createObjectURL(file);
  document.getElementById('previewImg').src = currentBlob;
  document.getElementById('previewFilename').textContent = file.name;
  document.getElementById('uploadIdle').style.display  = 'none';
  document.getElementById('previewWrap').style.display = 'block';
  const zone = document.getElementById('uploadZone');
  zone.classList.add('active-scan');
  setTimeout(() => zone.classList.remove('active-scan'), 3000);
  document.getElementById('predictBtn').disabled = false;
}

function clearFile() {
  currentFile = null;
  if (currentBlob) { URL.revokeObjectURL(currentBlob); currentBlob = null; }
  document.getElementById('fileInput').value = '';
  document.getElementById('previewImg').src  = '';
  document.getElementById('uploadIdle').style.display  = 'flex';
  document.getElementById('previewWrap').style.display = 'none';
  document.getElementById('predictBtn').disabled = true;
  hideResults();
}

function handleDragOver(e) { e.preventDefault(); document.getElementById('uploadZone').classList.add('drag-over'); }
function handleDragLeave(e){ document.getElementById('uploadZone').classList.remove('drag-over'); }
function handleDrop(e) {
  e.preventDefault();
  document.getElementById('uploadZone').classList.remove('drag-over');
  const f = e.dataTransfer.files[0];
  if (f) handleFile(f);
}

let stepTimers = [];
function animateSteps() {
  ['step1','step2','step3','step4'].forEach((id,i) => {
    stepTimers.push(setTimeout(() => {
      if (i > 0) {
        const prev = document.getElementById('step'+i);
        prev.classList.remove('active'); prev.classList.add('done');
        prev.textContent = prev.textContent.replace('\u2B21','\u2713');
      }
      document.getElementById(id).classList.add('active');
    }, i * 900));
  });
}
function clearSteps() {
  stepTimers.forEach(clearTimeout); stepTimers = [];
  ['step1','step2','step3','step4'].forEach(id => {
    const el = document.getElementById(id);
    el.className = 'loading-step';
    el.textContent = el.textContent.replace('\u2713','\u2B21');
  });
}

async function runPrediction() {
  if (!currentFile) return;
  const btn = document.getElementById('predictBtn');
  btn.disabled = true; btn.classList.add('loading'); btn.textContent = 'Analysing\u2026';
  clearSteps();
  const overlay = document.getElementById('loadingOverlay');
  overlay.classList.add('show');
  animateSteps();
  const formData = new FormData();
  formData.append('file', currentFile, currentFile.name);
  try {
    const res = await fetch(
        `${API_URL}/predict`,
        {
            method:'POST',
            body:formData
        }
    );
    if (!res.ok) throw new Error('HTTP ' + res.status + ': ' + res.statusText);
    const data = await res.json();
    if (data.error) throw new Error(data.error);
    await delay(500);
    overlay.classList.remove('show');
    renderResults(data);
    showToast('success', '\u2705', 'Prediction complete.');
  } catch(err) {
    overlay.classList.remove('show');
    let msg = err.message;
    if (msg.includes('Failed to fetch') || msg.includes('NetworkError')) {
      msg = 'Cannot reach the FastAPI backend. Make sure it is running on port 8000.';
    }
    showToast('error', '\u274C', msg);
    hideResults();
  } finally {
    btn.disabled = false; btn.classList.remove('loading'); btn.textContent = 'Run Analysis';
  }
}

const CLASS_META = {
  glioma:     { desc: 'Glial cell tumour \u2014 most common primary brain tumour.' },
  meningioma: { desc: 'Tumour arising from the meninges (brain membranes).' },
  pituitary:  { desc: 'Tumour in the pituitary gland at the base of the brain.' },
  notumor:    { desc: 'No tumour detected in the scan.' },
};

function renderResults(data) {
  const prediction = data.prediction  || 'Unknown';
  const confidence = parseFloat(data.confidence || 0);
  const probs      = data.probabilities || {};
  const gradcamUrl = data.gradcam_url  || '';

  document.getElementById('diagName').textContent = prediction;
  const meta = CLASS_META[prediction.toLowerCase()] || {};
  document.getElementById('diagSub').textContent  = meta.desc || '';

  const pill = document.getElementById('confPill');
  const pillText = document.getElementById('confPillText');
  pill.className = 'conf-pill';
  if (confidence >= 80)      { pill.classList.add('high'); pillText.textContent = 'High confidence \u2014 ' + confidence.toFixed(1) + '%'; }
  else if (confidence >= 50) { pill.classList.add('mid');  pillText.textContent = 'Moderate confidence \u2014 ' + confidence.toFixed(1) + '%'; }
  else                        { pill.classList.add('low');  pillText.textContent = 'Low confidence \u2014 ' + confidence.toFixed(1) + '%'; }

  const TOTAL_ARC = 126;
  const offset = TOTAL_ARC * (1 - confidence / 100);
  const fill = document.getElementById('gaugeFill');
  const num  = document.getElementById('gaugeNum');
  const colour = confidence >= 80 ? '#00e5a0' : confidence >= 50 ? '#ffb547' : '#ff5e7a';
  fill.style.stroke = colour;
  requestAnimationFrame(() => {
    fill.style.strokeDashoffset = offset;
    let startTime = null;
    const end = confidence;
    function step(ts) {
      if (!startTime) startTime = ts;
      const p = Math.min((ts - startTime) / 900, 1);
      num.textContent = Math.round(end * easeOut(p)) + '%';
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  });

  const container = document.getElementById('probSection');
  const labelMap = { glioma:'Glioma', meningioma:'Meningioma', notumor:'No Tumor', pituitary:'Pituitary' };
  const sorted = Object.entries(probs).sort((a,b) => b[1]-a[1]);
  const predKey = prediction.toLowerCase().replace(' ','');
  container.innerHTML = sorted.map(([cls,prob]) => {
    const pct   = (prob * 100).toFixed(1);
    const isAct = cls.toLowerCase() === predKey;
    return '<div class="prob-row">' +
      '<div class="prob-cls'+(isAct?' active':'')+'">'+( labelMap[cls]||cls)+'</div>' +
      '<div class="prob-track"><div class="prob-fill'+(isAct?' active':'')+'" style="width:0%" data-width="'+pct+'"></div></div>' +
      '<div class="prob-pct'+(isAct?' active':'')+'">'+pct+'%</div>' +
      '</div>';
  }).join('');
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      container.querySelectorAll('.prob-fill').forEach(el => { el.style.width = el.dataset.width + '%'; });
    });
  });

  document.getElementById('emptyCard').style.display   = 'none';
  document.getElementById('resultPanel').style.display = 'block';

  if (gradcamUrl) {
    document.getElementById('origImg').src = currentBlob;
    document.getElementById('camImg').src  = gradcamUrl;
    document.getElementById('explanationSection').style.display = 'block';
  }
}

function hideResults() {
  document.getElementById('emptyCard').style.display          = 'block';
  document.getElementById('resultPanel').style.display        = 'none';
  document.getElementById('explanationSection').style.display = 'none';
}

let toastTimer;
function showToast(type, icon, msg) {
  const toast = document.getElementById('toast');
  document.getElementById('toastIcon').innerHTML = icon;
  document.getElementById('toastMsg').textContent = msg;
  toast.className = 'toast ' + type + ' show';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toast.className = 'toast ' + type; }, 4500);
}

function delay(ms) { return new Promise(r => setTimeout(r, ms)); }
function easeOut(t) { return 1 - Math.pow(1-t, 3); }
</script>
</body>
</html>
"""

components.html(HTML, height=1100, scrolling=True)