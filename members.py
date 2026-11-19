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
.gate{max-width:420px;margin:60px auto;text-align:center}.gate input{width:100%;padding:12px 14px;font:16px ui-sans-serif,sans-serif;border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--ink)}
.gate button{margin-top:12px;border:0;background:var(--red);color:#fff;border-radius:999px;padding:10px 22px;font:700 15px ui-sans-serif,sans-serif;cursor:pointer}
#err{color:var(--red);min-height:1.5em;font:14px ui-sans-serif,sans-serif;margin-top:10px}
details{border-bottom:1px solid var(--line);padding:14px 0}summary{cursor:pointer;font:700 19px ui-sans-serif,sans-serif}
</style></head><body>
<header><div class="wrap top"><span class="brand"><span class="logo">{{LEAF}}</span>Post Production <b>Canada</b></span></div></header>
<main class="wrap"><div class="gate" id="gate"><h1 style="font-size:28px">Members</h1><p class="note">Enter the password to read the original articles.</p>
<form id="f"><input id="pw" type="password" autocomplete="current-password" aria-label="Password" autofocus><button type="submit">Unlock</button></form><div id="err" role="alert"></div></div>
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
document.getElementById('f').addEventListener('submit',async function(ev){
  ev.preventDefault();var err=document.getElementById('err');err.textContent='Unlocking…';
  try{var arts=await unlock(document.getElementById('pw').value);
    var h='<h1>Originals</h1><p class="meta">Original writing on Canadian post-production. Private.</p>';
    arts.forEach(function(a){h+='<details><summary>'+esc(a.title)+'</summary><p class="meta">'+esc(a.byline)+' · '+esc(a.date)+'</p>'+a.html+(a.disclosure?'<p class="disc"><b>Disclosure:</b> '+esc(a.disclosure)+'</p>':'')+'</details>'});
    var o=document.getElementById('out');o.innerHTML=h;o.hidden=false;document.getElementById('gate').hidden=true;
  }catch(e){err.textContent='That password did not work.'}
});
</script></body></html>"""


def write(out, root, leaf, favicon):
    enc, meta = Path(root) / "data" / "members.enc", Path(root) / "data" / "members.json"
    if not (enc.exists() and meta.exists()):
        return
    m = json.loads(meta.read_text())
    page = (PAGE.replace("{{FAVICON}}", favicon).replace("{{LEAF}}", leaf)
            .replace("{{ENC}}", enc.read_text().strip()).replace("{{ITER}}", str(m["iter"])))
    (Path(out) / f'{m["slug"]}.html').write_text(page, encoding="utf-8")
