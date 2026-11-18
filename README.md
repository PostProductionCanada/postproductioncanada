# Post Production Canada

Free, self-updating news aggregator for Canadian post-production, VFX and screen-industry news.

- `feeds.json` — the sources. Add or remove a feed here, nothing else needed.
- `build.py` — fetches every feed, filters for relevance, writes `public/` (Python 3 stdlib only).
- `.github/workflows/refresh.yml` — rebuilds and deploys every 3 hours on GitHub Pages (free).

Preview locally: `python3 build.py && open public/index.html`

## Go live on postproductioncanada.ca (about 15 minutes, $0)

1. Create a **public** GitHub repo (e.g. `postproductioncanada`) and push this folder to `main`.
2. Repo → Settings → Pages → Source: **GitHub Actions**. Run the "Refresh news and deploy" workflow once.
3. Settings → Pages → Custom domain: `postproductioncanada.ca`, tick Enforce HTTPS.
4. Squarespace → Domains → postproductioncanada.ca → DNS. Remove any default Squarespace website records on `@` and `www`, then add:
   - A `@` → 185.199.108.153
   - A `@` → 185.199.109.153
   - A `@` → 185.199.110.153
   - A `@` → 185.199.111.153
   - CNAME `www` → `<your-github-username>.github.io`
5. Wait for DNS (minutes to a few hours). HTTPS turns on automatically.

## Later: if it takes off

Ad-free for now. Options when traffic exists: a free weekly email digest (Buttondown/Beehiiv),
sponsored "Featured" slots for post houses and gear dealers, a paid job board (Canadian post jobs),
and a facility directory (listings are the usual money-maker for niche trade sites).
