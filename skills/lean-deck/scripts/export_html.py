#!/usr/bin/env python3
"""lean-deck HTML export — collect the rendered slide markup from a browser and bundle it into one standalone HTML deck.

Usage
  python3 export_html.py --out <folder> --origin http://localhost:3000 \
      --deck "demo=demo-deck|Demo deck" --deck "viz=viz-deck|Viz deck"

  --deck format: <viewer deck key>=<file name without extension>|<browser tab title>

How it works
  1. Waits for POSTs on 127.0.0.1:<port> (CORS allows only the viewer origin).
  2. Run capture.js in the browser once per deck; each run posts {deck, slides[]}.
  3. When every registered deck has arrived, it writes the HTML files, prints slide counts and exits.

Why this way
  - Slides render with inline styles, so the captured DOM becomes crisp vector HTML with no build step.
  - Headless screenshotting a dev server is slow; the running viewer already has the pixels.
"""
import argparse, html, http.server, json, pathlib, sys

TPL = '''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
html,body{margin:0;height:100%;background:#000;overflow:hidden}
.slide{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform-origin:center center}
.slide[hidden]{display:none}
#hud{position:fixed;right:20px;bottom:16px;font:13px ui-monospace,monospace;color:rgba(255,255,255,.45);z-index:9;user-select:none}
#help{position:fixed;left:20px;bottom:16px;font:12px ui-monospace,monospace;color:rgba(255,255,255,.5);z-index:9;user-select:none;display:flex;align-items:center;gap:10px}
.laser-badge{display:inline-flex;align-items:center;gap:5px;padding:2px 8px;border-radius:12px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);cursor:pointer;pointer-events:auto;transition:all .2s ease;font-weight:600}
.laser-badge:hover{background:rgba(255,255,255,0.16);border-color:rgba(255,255,255,0.3)}
.laser-badge.mode-red{background:rgba(255,42,85,0.2);border-color:rgba(255,42,85,0.6);color:#ff4d6d;box-shadow:0 0 10px rgba(255,42,85,0.4)}
.laser-badge.mode-purple{background:rgba(168,85,247,0.2);border-color:rgba(168,85,247,0.6);color:#c084fc;box-shadow:0 0 10px rgba(168,85,247,0.4)}
#laser-pointer{position:fixed;width:12px;height:12px;border-radius:50%;pointer-events:none;transform:translate(-50%,-50%);z-index:999999;display:none}
#laser-pointer.laser-red{display:block;background:radial-gradient(circle,#ffffff 15%,#ff2a55 55%,#e11d48 100%);box-shadow:0 0 6px #fff,0 0 12px #ff2a55,0 0 24px #e11d48,0 0 36px rgba(255,42,85,0.85)}
#laser-pointer.laser-purple{display:block;background:radial-gradient(circle,#ffffff 15%,#c084fc 55%,#9333ea 100%);box-shadow:0 0 6px #fff,0 0 12px #c084fc,0 0 24px #9333ea,0 0 36px rgba(168,85,247,0.85)}
body.laser-active,body.laser-active *{cursor:none !important}
</style></head><body>
__SLIDES__
<div id="laser-pointer"></div>
<div id="hud"></div>
<div id="help">
  <span>← → 이동 · [F] 전체화면</span>
  <span id="laser-indicator" class="laser-badge" onclick="cycleLaser()">● [L] 레이저: <span id="laser-text">OFF</span></span>
</div>
<script>
const S=[...document.querySelectorAll('.slide')];let i=Math.max(0,Math.min(S.length-1,(parseInt(location.hash.slice(1))||1)-1));
function fit(){const k=Math.min(innerWidth/1920,innerHeight/1080);S.forEach(s=>s.style.transform=`translate(-50%,-50%) scale(${k})`)}
function go(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,j)=>s.hidden=j!==i);document.getElementById('hud').textContent=`${String(i+1).padStart(2,'0')} / ${S.length}`;history.replaceState(null,'','#'+(i+1))}
addEventListener('resize',fit);

let laserState = 0; // 0: OFF, 1: RED, 2: PURPLE
const laserEl = document.getElementById('laser-pointer');
const laserBadge = document.getElementById('laser-indicator');
const laserText = document.getElementById('laser-text');

function updateLaserUI(){
  if(laserState === 1){
    document.body.classList.add('laser-active');
    laserEl.className = 'laser-red';
    laserBadge.className = 'laser-badge mode-red';
    laserText.textContent = 'RED';
  } else if(laserState === 2){
    document.body.classList.add('laser-active');
    laserEl.className = 'laser-purple';
    laserBadge.className = 'laser-badge mode-purple';
    laserText.textContent = 'PURPLE';
  } else {
    document.body.classList.remove('laser-active');
    laserEl.className = '';
    laserBadge.className = 'laser-badge';
    laserText.textContent = 'OFF';
  }
}

function cycleLaser(){
  laserState = (laserState + 1) % 3;
  updateLaserUI();
}

window.addEventListener('mousemove', e => {
  if(laserState !== 0){
    laserEl.style.left = e.clientX + 'px';
    laserEl.style.top = e.clientY + 'px';
  }
});

addEventListener('keydown',e=>{if(e.metaKey||e.ctrlKey||e.altKey)return;
 if(e.key==='l'||e.key==='L'){e.preventDefault();cycleLaser()}
 else if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){e.preventDefault();go(i+1)}
 else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();go(i-1)}
 else if(e.key==='Home')go(0);else if(e.key==='End')go(S.length-1);
 else if(e.key==='f'||e.key==='F'||e.key==='\\\\'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen?.()}});
addEventListener('click',e=>{if(e.target.closest('#help')||e.target.closest('#hud'))return;go(e.clientX<innerWidth/3?i-1:i+1)});
fit();go(i);
</script></body></html>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--port', type=int, default=18765)
    ap.add_argument('--origin', default='http://localhost:3000', help='origin of the running viewer')
    ap.add_argument('--deck', action='append', required=True)
    a = ap.parse_args()

    decks = {}
    for d in a.deck:
        key, rest = d.split('=', 1)
        name, title = rest.split('|', 1)
        decks[key] = (name, title)
    out = pathlib.Path(a.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    done = {}

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def cors(self):
            self.send_header('Access-Control-Allow-Origin', a.origin)
            self.send_header('Access-Control-Allow-Headers', 'content-type')

        def do_OPTIONS(self):
            self.send_response(204); self.cors(); self.end_headers()

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers['content-length'])))
            key, slides = str(body['deck']), body['slides']
            if key not in decks or not slides:
                self.send_response(400); self.cors(); self.end_headers(); return
            name, title = decks[key]
            doc = TPL.replace('__TITLE__', html.escape(title)).replace(
                '__SLIDES__', '\n'.join(f'<div class="slide" hidden>{s}</div>' for s in slides))
            p = out / f'{name}.html'
            p.write_text(doc, encoding='utf-8')
            done[key] = len(slides)
            print(f'{p} · {len(slides)} slides · {p.stat().st_size // 1024}KB', flush=True)
            self.send_response(200); self.cors(); self.end_headers(); self.wfile.write(b'ok')

    for port in range(a.port, a.port + 20):          # if the port is taken, try the next one — set PORT in capture.js to the printed value
        try:
            srv = http.server.HTTPServer(('127.0.0.1', port), H); break
        except OSError:
            continue
    else:
        print(f'no free port in {a.port}-{a.port + 19}'); return 1
    print(f'listening on 127.0.0.1:{port} · decks {", ".join(decks)}', flush=True)
    while len(done) < len(decks):
        srv.handle_request()
    print('done', json.dumps(done, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    sys.exit(main())
