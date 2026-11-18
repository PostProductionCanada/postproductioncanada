#!/usr/bin/env python3
"""Fetch two public pages from filmincanada.com and keep only aggregate numbers.

Polite by design: two requests per run, identifying User-Agent, no production titles stored.
Credit and link-back are shown wherever the numbers appear. Output: data/filmincanada.json.
If the fetch fails, the previous file is kept.
"""
import json, re, sys, time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).parent
OUT = ROOT / "data" / "filmincanada.json"
UA = "Mozilla/5.0 (compatible; PostProductionCanadaBot/1.0; +https://postproductioncanada.ca)"
BASE = "https://filmincanada.com"


def get(path):
    with urlopen(Request(BASE + path, headers={"User-Agent": UA}), timeout=30) as r:
        return r.read().decode("utf8", "ignore")


def productions(html):
    i = html.index("const productions = ") + len("const productions = ")
    arr, _ = json.JSONDecoder().raw_decode(html[i:])
    return arr


def incentives(html):
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style).*?</\1>", "", html, flags=re.S)))
    out = {}
    # e.g. "QC 27.7% Quebec — 27.7%"  /  "NU Nunavut — no service incentive"
    for code, name, tail in re.findall(r"\b([A-Z]{2}) (?:[\d.]+% )?([A-Z][A-Za-z .]+?) — (no service incentive|[\d.]+%)", txt):
        out[code] = {"name": name.strip(), "net_effective": None if tail.startswith("no") else float(tail.rstrip("%"))}
    return out, txt


def main():
    try:
        now_html = get("/now-shooting")
        time.sleep(2)
        inc_html = get("/incentives")
        prods = productions(now_html)
        inc, _ = incentives(inc_html)
        m = re.search(r"last run (\d{4}-\d{2}-\d{2})", re.sub(r"\s+", " ", now_html))
        by_prov = {}
        for p in prods:
            d = by_prov.setdefault(p["province"], Counter())
            d[p["status"]] += 1
            d["total"] += 1
        data = {
            "source": "filmincanada.com",
            "source_urls": {"now_shooting": BASE + "/now-shooting", "incentives": BASE + "/incentives"},
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "now_shooting_last_run": m.group(1) if m else None,
            "records": len(prods),
            "by_province": {k: dict(v) for k, v in sorted(by_prov.items(), key=lambda kv: -kv[1]["total"])},
            "by_type": dict(Counter(p["type"] for p in prods)),
            "by_status": dict(Counter(p["status"] for p in prods)),
            "incentives_net_effective_12m_series": inc,
        }
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False))
        print(f"filmincanada: {len(prods)} records, {len(inc)} incentive rows, last run {data['now_shooting_last_run']}")
    except Exception as e:
        print(f"filmincanada refresh failed, keeping previous data: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
