#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lean-deck standalone deck builder — generates standalone 1920x1080 interactive presentation decks."""
import json
import pathlib
import sys

HTML_TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {{
  {css_vars}
}}
* {{ box-sizing: border-box; }}
html, body {{
  margin: 0; padding: 0; height: 100%; width: 100%;
  background: var(--ld-surface-page, #0b0c10);
  color: var(--ld-text-strong, #ffffff);
  font-family: var(--ld-font-body, 'Inter', 'Noto Sans KR', sans-serif);
  overflow: hidden;
  user-select: none;
}}
.stage {{
  position: absolute; left: 0; top: 0; width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
}}
.slide {{
  width: 1920px; height: 1080px; position: relative;
  background: var(--ld-surface-page, #0b0c10);
  border-radius: 8px; overflow: hidden;
  display: none; padding: 72px 96px;
  flex-direction: column;
}}
.slide.active {{
  display: flex;
}}
.eyebrow {{
  font-size: 18px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--ld-accent-primary, #6366f1); margin-bottom: 16px;
  display: flex; align-items: center; gap: 8px;
}}
.title {{
  font-size: 52px; font-weight: 800; line-height: 1.15; margin: 0 0 40px 0;
  color: var(--ld-text-strong, #ffffff); letter-spacing: -0.02em;
}}
.content-grid {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 32px; flex: 1; align-items: stretch;
}}
.card {{
  background: var(--ld-surface-raised, rgba(255,255,255,0.05));
  border: 1px solid var(--ld-surface-inset, rgba(255,255,255,0.1));
  border-radius: 16px; padding: 36px;
  display: flex; flex-direction: column; justify-content: space-between;
}}
.card-header {{
  font-size: 26px; font-weight: 700; margin-bottom: 16px;
  color: var(--ld-text-strong, #ffffff);
}}
.card-body {{
  font-size: 20px; line-height: 1.6; color: var(--ld-text-soft, rgba(255,255,255,0.75));
}}
.footer-bar {{
  position: fixed; bottom: 24px; left: 32px; right: 32px;
  display: flex; justify-content: space-between; align-items: center;
  font-family: 'JetBrains Mono', monospace; font-size: 14px;
  color: rgba(255,255,255,0.6); pointer-events: none;
}}
.footer-left {{
  display: flex; align-items: center; gap: 14px; pointer-events: auto;
}}
.laser-badge {{
  display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px;
  border-radius: 12px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.2);
  cursor: pointer; pointer-events: auto; font-size: 12px; font-weight: 600;
  transition: all 0.2s ease; user-select: none;
}}
.laser-badge:hover {{ background: rgba(255,255,255,0.16); border-color: rgba(255,255,255,0.35); }}
.laser-badge.mode-red {{
  background: rgba(255,42,85,0.2); border-color: rgba(255,42,85,0.6); color: #ff4d6d;
  box-shadow: 0 0 10px rgba(255,42,85,0.4);
}}
.laser-badge.mode-purple {{
  background: rgba(168,85,247,0.2); border-color: rgba(168,85,247,0.6); color: #c084fc;
  box-shadow: 0 0 10px rgba(168,85,247,0.4);
}}
#laser-pointer {{
  position: fixed; width: 14px; height: 14px; border-radius: 50%;
  pointer-events: none; transform: translate(-50%, -50%); z-index: 999999; display: none;
}}
#laser-pointer.laser-red {{
  display: block; background: radial-gradient(circle, #ffffff 15%, #ff2a55 55%, #e11d48 100%);
  box-shadow: 0 0 6px #fff, 0 0 12px #ff2a55, 0 0 24px #e11d48, 0 0 36px rgba(255,42,85,0.85);
}}
#laser-pointer.laser-purple {{
  display: block; background: radial-gradient(circle, #ffffff 15%, #c084fc 55%, #9333ea 100%);
  box-shadow: 0 0 6px #fff, 0 0 12px #c084fc, 0 0 24px #9333ea, 0 0 36px rgba(168,85,247,0.85);
}}
body.laser-active, body.laser-active * {{ cursor: none !important; }}
.controls {{
  position: fixed; right: 32px; bottom: 24px; display: flex; gap: 12px; pointer-events: auto;
}}
.btn {{
  background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
  color: #fff; padding: 8px 16px; border-radius: 8px; cursor: pointer;
  font-family: 'JetBrains Mono', monospace; font-size: 13px;
}}
.btn:hover {{ background: rgba(255,255,255,0.2); }}
</style>
</head>
<body>
<div id="laser-pointer"></div>
<div class="stage" id="stage">
{slides_html}
</div>
<div class="footer-bar">
  <div class="footer-left">
    <span>{title}</span>
    <span id="laser-indicator" class="laser-badge" onclick="cycleLaser()">● [L] 레이저: <span id="laser-text">OFF</span></span>
  </div>
  <div class="controls">
    <button class="btn" onclick="prev()">◀ Prev</button>
    <span id="counter" style="line-height:34px; padding:0 8px;">1 / {total_slides}</span>
    <button class="btn" onclick="next()">Next ▶</button>
    <button class="btn" onclick="toggleFS()">Fullscreen [F]</button>
  </div>
</div>
<script>
let cur = 0;
const slides = document.querySelectorAll('.slide');
const counter = document.getElementById('counter');
const total = slides.length;

function fit() {{
  const stage = document.getElementById('stage');
  const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  slides.forEach(s => {{
    s.style.transform = 'scale(' + scale + ')';
    s.style.transformOrigin = 'center center';
  }});
}}
window.addEventListener('resize', fit);
window.addEventListener('load', fit);

function show(idx) {{
  if (idx < 0) idx = 0;
  if (idx >= total) idx = total - 1;
  cur = idx;
  slides.forEach((s, i) => s.classList.toggle('active', i === cur));
  if (counter) counter.innerText = (cur + 1) + ' / ' + total;
}}

function next() {{ show(cur + 1); }}
function prev() {{ show(cur - 1); }}
function toggleFS() {{
  if (!document.fullscreenElement) document.documentElement.requestFullscreen();
  else document.exitFullscreen();
}}

let laserState = 0; // 0: OFF, 1: RED, 2: PURPLE
const laserEl = document.getElementById('laser-pointer');
const laserBadge = document.getElementById('laser-indicator');
const laserText = document.getElementById('laser-text');

function updateLaserUI() {{
  if (laserState === 1) {{
    document.body.classList.add('laser-active');
    laserEl.className = 'laser-red';
    laserBadge.className = 'laser-badge mode-red';
    laserText.textContent = 'RED';
  }} else if (laserState === 2) {{
    document.body.classList.add('laser-active');
    laserEl.className = 'laser-purple';
    laserBadge.className = 'laser-badge mode-purple';
    laserText.textContent = 'PURPLE';
  }} else {{
    document.body.classList.remove('laser-active');
    laserEl.className = '';
    laserBadge.className = 'laser-badge';
    laserText.textContent = 'OFF';
  }}
}}

function cycleLaser() {{
  laserState = (laserState + 1) % 3;
  updateLaserUI();
}}

window.addEventListener('mousemove', (e) => {{
  if (laserState !== 0) {{
    laserEl.style.left = e.clientX + 'px';
    laserEl.style.top = e.clientY + 'px';
  }}
}});

window.addEventListener('keydown', (e) => {{
  if (e.key === 'l' || e.key === 'L') {{
    e.preventDefault();
    cycleLaser();
  }} else if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
    next();
  }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
    prev();
  }} else if (e.key.toLowerCase() === 'f') {{
    toggleFS();
  }}
}});
fit();
show(0);
</script>
</body>
</html>
"""
