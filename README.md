# Driver Decider

A one-page site that shows the used cars from the "First car comparison" sheet as movie posters.
Built for iPhone first. It lives at **zombe.es/driverdecider**.

- One poster per car generation. Tap it for every version (year and trim) with price, 5-year cost,
  insurance, MPG, safety and reliability ratings, and links to KBB, NHTSA, IIHS, Consumer Reports,
  RepairPal and an Autotrader search for that model and year.
- Filter chips across the top (Simon's picks, body, size, fuel, all-wheel drive, high safety, high
  reliability), a price cap and a sort.
- Highlight a car to keep it at the top, or banish it to get it out of the list. Both are kept in the
  browser's local storage (`driverdecider.v1`). Banished cars wait at the bottom with a Bring back button.

## Layout

| Path | What it is |
| --- | --- |
| `web/page.html` | The page itself: HTML, CSS and JS in one file, no build step or framework. |
| `public/driverdecider/` | What Cloudflare serves: `index.html` (made from `web/page.html`), `data.js`, `img/`. |
| `data/sheet-rows.json` | The Comparison sheet's cells, as read from the Claude Sheet. |
| `tools/build_data.py` | Groups the sheet rows into generations and writes `data.js` and the resized photos. |
| `tools/build_page.py` | Wraps `web/page.html` into `public/driverdecider/index.html`. |
| `wrangler.jsonc` | The Cloudflare Worker (static assets only, no script). |

## Updating

1. Change the page in `web/page.html`, then run `python3 tools/build_page.py`.
2. When the sheet changes, refresh `data/sheet-rows.json` and run `python3 tools/build_data.py`
   (needs Pillow, and reads the full-size photos from the project's `car-comparison/photos` folder).
3. Commit and push. Cloudflare deploys `main`.

## Hosting on Cloudflare (one time)

1. dash.cloudflare.com > Workers & Pages > Create > Import a repository, and pick `driverdecider`.
   Branch `main`, no build command, deploy command `npx wrangler deploy`, root directory `/`.
2. The `routes` in `wrangler.jsonc` put the Worker on `zombe.es/driverdecider` and everything under it.
   This needs `zombe.es` to be a zone in the same Cloudflare account. The rest of zombe.es is untouched.
3. Static assets don't count against the Workers free plan's request limit.
