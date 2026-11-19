#!/usr/bin/env python3
"""Lock the private Originals behind a password. Run this on YOUR Mac, in Terminal.

  python3 lock_originals.py

It reads the articles in ../drafts-private/originals/ (outside the public repo), asks you to TYPE a password
(nothing is shown, and nobody else, including Claude, sees it), encrypts the articles, and writes only the
scrambled result to data/members.enc. Only that scrambled file goes in the public repo. Readers unlock it
in their browser with the password; the site never stores or sees the password.

Re-run it any time you add or edit an article. Use the same password or choose a new one.
"""
import base64, getpass, json, os, secrets, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import originals, style

SRC = ROOT.parent / "drafts-private" / "originals"
ITER = 600000


def main():
    arts = []
    for p in sorted(SRC.glob("*.md")):
        if p.name.startswith("_"):
            continue
        a = originals.parse(p)
        if not a.get("title") or not a.get("date"):
            continue
        arts.append({"title": a["title"], "date": a["date"], "type": a.get("type", ""), "byline": a.get("byline", "Post Production Canada"),
                     "summary": a.get("summary", ""), "disclosure": a.get("disclosure", ""), "html": originals.md(a["body"])})
        arts[-1] = {k: (style.cap_text(v) if k in ("title", "html", "disclosure", "summary") else v) for k, v in arts[-1].items()}
    arts.sort(key=lambda a: a["date"], reverse=True)
    if not arts:
        sys.exit("No articles found in " + str(SRC))
    pw = os.environ.get("PPC_TEST_PASSWORD")
    if not pw:
        pw = getpass.getpass("Choose a password (14+ characters, a few words works well): ")
        if getpass.getpass("Type it again: ") != pw:
            sys.exit("Passwords did not match. Nothing was changed.")
    if len(pw) < 14 and not os.environ.get("PPC_TEST_PASSWORD"):
        sys.exit("Too short. Use at least 14 characters, for example four random words. Nothing was changed.")
    plain = ("PPC1\n" + json.dumps(arts, ensure_ascii=False)).encode("utf-8")
    env = dict(os.environ, PPC_PW=pw)
    r = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", str(ITER), "-md", "sha256", "-salt", "-a", "-A", "-pass", "env:PPC_PW"],
                       input=plain, capture_output=True, env=env)
    if r.returncode:
        sys.exit("Encryption failed: " + r.stderr.decode())
    meta_f = ROOT / "data" / "members.json"
    slug = None
    if meta_f.exists():
        slug = json.loads(meta_f.read_text()).get("slug")
    slug = slug or "members-" + secrets.token_hex(6)
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "members.enc").write_text(r.stdout.decode().strip())
    meta_f.write_text(json.dumps({"slug": slug, "iter": ITER}))
    print(f"Locked {len(arts)} article(s). Private page address once published: https://postproductioncanada.ca/{slug}.html")
    print("Tell Claude 'locked' and it will build and publish the page. Keep that address and the password to yourself.")


main()
