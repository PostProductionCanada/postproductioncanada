"""Writes the password-locked Originals page, if data/members.enc exists.

The page holds only scrambled text. The browser unscrambles it with the password the reader types.
It is not linked from anywhere, not in the sitemap, and marked noindex. Nothing here sees any password.
"""
import json, html
from pathlib import Path
import originals

PAGE = """<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive"><title>Members — Post Production Canada</title><link rel="icon" href="{{FAVICON}}">
<style>""" + originals.CSS + """
.pn{color:#1a6fb5;font-weight:600}@media (prefers-color-scheme:dark){.pn{color:#6cb4f0}}.co{color:#8a3fc0;font-weight:600}@media (prefers-color-scheme:dark){.co{color:#c79bf2}}.hlkey{font-size:13.5px;color:var(--mute);margin:6px 0 12px}
.hero-art{display:block;width:100%;height:150px;border-radius:10px;margin:10px 0 14px}
.gate{max-width:420px;margin:60px auto;text-align:center}.gate input{width:100%;padding:12px 14px;font:16px ui-sans-serif,sans-serif;border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--ink)}
.gate button{margin-top:12px;border:0;background:var(--red);color:#fff;border-radius:999px;padding:10px 22px;font:700 15px ui-sans-serif,sans-serif;cursor:pointer}
#err{color:var(--red);min-height:1.5em;font:14px ui-sans-serif,sans-serif;margin-top:10px}
details{border-bottom:1px solid var(--line);padding:14px 0}summary{cursor:pointer;font:700 19px ui-sans-serif,sans-serif}
</style></head><body>
<header><div class="wrap top"><span class="brand"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></span></div></header>
<main class="wrap"><div class="gate" id="gate" style="max-width:560px;text-align:left">
<p class="note" style="margin:0 0 4px"><a href="index.html">← Back to the news</a></p>
<h1 style="font-size:30px;margin:6px 0 8px">🔑 Subscribers' corner</h1>
<p><b>Always free to join. Unsubscribe any time.</b> Subscribers get our original articles and bonus material as we add it, and the newsletter in their inbox.</p>
<div class="box" style="border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:14px 0">
<p style="margin:0 0 6px"><b>Already a subscriber?</b> Enter the password from your welcome email.</p>
<form id="f" style="text-align:center"><input id="pw" type="password" autocomplete="current-password" aria-label="Password" autofocus><button type="submit">Unlock</button></form><div id="err" role="alert"></div>
<p class="note" style="margin:6px 0 0">Lost it? Email <a href="mailto:hello@postproductioncanada.ca?subject=Subscriber%20password">hello@postproductioncanada.ca</a> from the address you subscribed with.</p></div>
<div class="box" style="border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:14px 0">
<p style="margin:0 0 6px"><b>Not subscribed yet?</b> Join free. We will send you the password and the newsletter, and you can leave with one click.</p>
<p style="margin:0"><a class="btn" style="display:inline-block;background:var(--red);color:#fff;border-radius:999px;padding:9px 20px;text-decoration:none;font-weight:700" href="{{JOIN}}">Subscribe free →</a></p></div>
<p class="note">The password is a light gate to keep originals for our readers. It is not bank-grade security, so please do not share it around.</p></div>
<div id="out" hidden></div></main>
<script>
var ENC="{{ENC}}",ITER={{ITER}};
function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML}
async function unlock(pw){
  var raw=Uint8Array.from(atob(ENC),function(c){return c.charCodeAt(0)});
  var salt=raw.slice(8,16),ct=raw.slice(16);
  var base=await crypto.subtle.importKey('raw',new TextEncoder().encode(pw),'PBKDF2',false,['deriveBits']);
  var bits=await crypto.subtle.deriveBits({name:'PBKDF2',hash:'SHA-256',salt:salt,iterations:ITER},base,384);
  var key=await crypto.subtle.importKey('raw',bits.slice(0,32),'AES-CBC',false,['decrypt']);
  var pt=await crypto.subtle.decrypt({name:'AES-CBC',iv:bits.slice(32,48)},key,ct);
  var t=new TextDecoder().decode(pt);if(t.indexOf('PPC1\\n')!==0)throw new Error('bad');
  return JSON.parse(t.slice(5));
}

function hs(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))>>>0;return h}
var PAL=[['#7a0f1a','#e4572e'],['#0f3b66','#2aa9c9'],['#2b1b5e','#7a5af8'],['#0e4b3a','#46b97a'],['#5a2a0a','#e8730c'],['#1c1c28','#b3202a']];
function art(a){
  var t=(a.title||'').toLowerCase(),seed=hs(a.title||'x'),p=PAL[seed%PAL.length],W=1200,H=260,i,x,y,w;
  var rnd=function(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296};
  var s='<svg class="hero-art" viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="g'+seed%9973+'" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="'+p[0]+'"/><stop offset="1" stop-color="'+p[1]+'"/></linearGradient></defs><rect width="'+W+'" height="'+H+'" fill="url(#g'+seed%9973+')"/><g fill="none" stroke="#fff" fill-opacity=".18" stroke-opacity=".55" stroke-width="3">';
  if(/two people|director|relationship/.test(t)){
    s+='<circle cx="500" cy="130" r="95" fill="#fff"/><circle cx="700" cy="130" r="95" fill="#fff"/><circle cx="500" cy="130" r="95"/><circle cx="700" cy="130" r="95"/><path d="M0 130H405M795 130H1200" stroke-dasharray="6 10" stroke-opacity=".3"/>';
  }else if(/agent|\bai\b|assistant|tool/.test(t)){
    var pts=[];for(i=0;i<10;i++)pts.push([80+i*115+rnd()*40,40+rnd()*180]);
    for(i=0;i<9;i++)s+='<path d="M'+pts[i][0]+' '+pts[i][1]+'L'+pts[i+1][0]+' '+pts[i+1][1]+'"/>';
    for(i=0;i<10;i++)s+='<circle cx="'+pts[i][0]+'" cy="'+pts[i][1]+'" r="'+(8+rnd()*12)+'" fill="#fff"/>';
  }else if(/music|sound|reset/.test(t)){
    for(i=0;i<70;i++){var bh=20+Math.abs(Math.sin(i/5))*90*(0.4+rnd());s+='<rect x="'+(30+i*16)+'" y="'+(130-bh/2)+'" width="8" height="'+bh+'" rx="4" fill="#fff" stroke="none" fill-opacity=".5"/>'}
  }else if(/vfx|tax|credit/.test(t)){
    for(i=0;i<5;i++)s+='<path d="M'+(160+i*40)+' '+(200-i*34)+'L'+(560+i*40)+' '+(200-i*34)+'L'+(720+i*40)+' '+(240-i*34)+'L'+(320+i*40)+' '+(240-i*34)+'Z" fill="#fff"/>';
  }else if(/documentary|film lab|century|history|labs/.test(t)){
    for(i=0;i<8;i++){x=30+i*146;s+='<rect x="'+x+'" y="60" width="124" height="140" rx="6" fill="#fff"/>';for(var j=0;j<4;j++)s+='<rect x="'+(x+8+j*30)+'" y="28" width="16" height="16" rx="3" fill="#fff" stroke="none" fill-opacity=".5"/><rect x="'+(x+8+j*30)+'" y="216" width="16" height="16" rx="3" fill="#fff" stroke="none" fill-opacity=".5"/>'}
  }else{
    for(var r2=0;r2<3;r2++){x=20+rnd()*60;y=50+r2*62;while(x<W-100){w=70+rnd()*190;s+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="44" rx="6" fill="#fff"/>';x+=w+10}}
  }
  return s+'</g></svg>';
}
document.getElementById('f').addEventListener('submit',async function(ev){
  ev.preventDefault();var err=document.getElementById('err');err.textContent='Unlocking…';
  try{var arts=await unlock(document.getElementById('pw').value);
    var h='<h1>Originals</h1><p class="meta">Original writing on Canadian post-production. Private.</p>';
    var DISC='<p class="disc legal"><b>About these articles.</b> We write from published, linked sources and say when something is our own reading or opinion. We try to be right, and we correct errors quickly: <a href="mailto:hello@postproductioncanada.ca?subject=Correction">tell us about one</a>. Nothing here is legal, financial, tax or career advice. Names and trademarks belong to their owners, and we have no commercial relationship with anyone named unless a piece says so.</p>';
    h+=DISC+'<p class="hlkey">To help you connect the dots as you read: <span class="pn">blue</span> is a person, <span class="co">purple</span> is a company or organization.</p>';arts.forEach(function(a){var ty=(a.type||'').toLowerCase();var bd=ty==='editorial'?'<span class="badge ed">Editorial</span>':(ty?'<span class="badge">'+esc(ty.charAt(0).toUpperCase()+ty.slice(1))+'</span>':'');var en=ty==='editorial'?'<p class="disc"><b>This is an editorial.</b> It is our opinion, not reporting. Facts in it are sourced below; the conclusions are ours.</p>':'';h+='<details><summary>'+bd+esc(a.title)+'</summary><p class="meta">'+esc(a.byline)+' · '+esc(a.date)+'</p>'+art(a)+en+a.html+(a.disclosure?'<p class="disc"><b>Disclosure:</b> '+esc(a.disclosure)+'</p>':'')+'</details>'});
    var o=document.getElementById('out');o.innerHTML=h;o.hidden=false;document.getElementById('gate').hidden=true;
  }catch(e){err.textContent='That password did not work.'}
});
</script></body></html>"""


def write(out, root, leaf, favicon):
    enc, meta = Path(root) / "data" / "members.enc", Path(root) / "data" / "members.json"
    if not (enc.exists() and meta.exists()):
        return
    m = json.loads(meta.read_text())
    try:
        cfg = json.loads((Path(root) / "site.json").read_text())
    except Exception:
        cfg = {}
    join = "index.html#subscribe" if (cfg.get("subscribe_form_action") or cfg.get("subscribe_embed_html")) else "mailto:" + (cfg.get("contact_email") or "hello@postproductioncanada.ca") + "?subject=Subscribe%20me%20to%20Post%20Production%20Canada"
    page = (PAGE.replace("{{JOIN}}", join).replace("{{FAVICON}}", favicon).replace("{{LEAF}}", leaf)
            .replace("{{ENC}}", enc.read_text().strip()).replace("{{ITER}}", str(m["iter"])))
    (Path(out) / f'{m["slug"]}.html').write_text(page, encoding="utf-8")
