# Sign-ups, analytics and the newsletter: how it all fits

Everything here keeps your identity off the public site. Accounts use the project's own Proton address.

## 1. Analytics (free, no cookies, no consent banner needed)
1. Create a free Cloudflare account with the project email. You do not need to move your domain to Cloudflare.
2. Dashboard → **Web Analytics** → **Add a site** → hostname `postproductioncanada.ca` → copy the token from the JavaScript snippet (the long code after `"token":`).
3. Paste the token into `site.json` as `analytics_token`, run `python3 build.py`, commit and push.
4. You will see visits, top pages and referrers in the Cloudflare dashboard within a few hours.

## 2. How sign-ups work
- A visitor enters an email in the box on the site. The box posts straight to your newsletter service. **Your site never stores emails.**
- Turn on **double opt-in** in the service: the visitor gets a confirmation email and must click it. That gives you proof of consent.
- The service holds the list, sends the welcome email, and adds the unsubscribe link to every message.
- To show the box on the site, paste the service's form address into `site.json` as `subscribe_form_action` (or its embed code as `subscribe_embed_html`).

### Which service
| | Free tier | Notes |
|---|---|---|
| Beehiiv | Up to 2,500 subscribers, unlimited sends | Most headroom, built-in landing page. Sponsorship and automation tools need a paid plan. |
| Buttondown | Up to 100 subscribers | Simple and privacy-first. About US$9/month at 1,000 subscribers. |
Prices change often. Check each pricing page before you commit.

## 3. Canada's anti-spam law (CASL)
Every marketing email needs three things: **consent, sender identification, and an unsubscribe mechanism.**
- **Consent:** the sign-up box and its confirmation email cover this. Keep any consent tick-box unticked by default.
- **Identification:** each email must show who is sending it and a mailing address. Use a **PO box or virtual mailbox**, not your home. Put it in `site.json` as `mailing_address`.
- **Unsubscribe:** one click, honoured within 10 business days.
This is general information, not legal advice. The CRTC publishes a CASL FAQ if you want to read the source.

## 4. The weekly newsletter (keep it short)
Small on purpose: **about 200 words, 3 sections, every one pointing back to the site.**
1. Pick of the week (one story, with why it matters)
2. Wrapping soon, post next (3 productions, links to the Post Buzz page)
3. Also this week (3 headlines, plus "all N Canadian stories" back to the site)

Run `python3 build.py` then `python3 make_newsletter.py`. It writes a draft to `drafts/`. Read it, fix anything, paste it into your service and send. Nothing sends automatically.

Cadence: weekly, same day and time. Start with Thursday morning.

Sponsor slot: one clearly labelled line, only once you have a sponsor.

## 5. Checklist before the first send
- [ ] Newsletter account created with the project email
- [ ] Double opt-in switched on
- [ ] PO box or virtual mailbox chosen and added to `site.json`
- [ ] Form address added to `site.json`, site rebuilt, sign-up tested with your own address
- [ ] Contact email confirmed working, then added to `site.json`
- [ ] Analytics token added
