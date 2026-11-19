# Driver Decider

A one-page site that shows the used cars from the "First car comparison" sheet as cards, built for iPhone first.
It is published with GitHub Pages and is meant to live at **driverdecider.zombe.es**.

- One card per car generation, or one per model year with the By model / By year switch. Simon's picks carry a gold star.
- Tap a card for every version (year and trim) with price, 5-year cost, insurance, MPG, safety and reliability ratings,
  and links to KBB, NHTSA, IIHS, Consumer Reports, RepairPal and an Autotrader search for that model and year.
- Dropdowns for shape, drivetrain, fuel type, safety level, reliability, sort and a price cap.
- Add a car to My Picks (bookmark) to keep it at the top and compare your picks in a table, or banish it to get it out
  of the list. Both are kept in the browser's local storage (`driverdecider.v1`). A first visit starts with the
  Impreza and Corolla in My Picks.

## Layout

| Path | What it is |
| --- | --- |
| `web/page.html` | The page itself: HTML, CSS and JS in one file, no build step or framework. |
| `site/` | What GitHub Pages publishes: `index.html` (made from `web/page.html`), `data.js`, `img/`. |
| `data/sheet-rows.json` | The Comparison sheet's cells, as read from the Claude Sheet. |
| `tools/build_data.py` | Groups the sheet rows into generations and writes `site/data.js` and the resized photos. |
| `tools/build_page.py` | Wraps `web/page.html` into `site/index.html`. |
| `.github/workflows/pages.yml` | Publishes `site/` to GitHub Pages on every push to `main`. |

## Updating

1. Change the page in `web/page.html`, then run `python3 tools/build_page.py`.
2. When the sheet changes, refresh `data/sheet-rows.json` and run `python3 tools/build_data.py`
   (needs Pillow, and reads the full-size photos from the project's `car-comparison/photos` folder).
3. Commit and push to `main`. The Pages workflow deploys it in about a minute.

## Hosting on GitHub Pages (one time)

1. In this repository: Settings > Pages > Build and deployment > Source: **GitHub Actions**.
   The first push to `main` (or Actions > Deploy to GitHub Pages > Run workflow) publishes it at
   `https://simonkuhn.github.io/driverdecider/`.
2. At the DNS host for zombe.es, add one record: CNAME `driverdecider` to `simonkuhn.github.io`
   (the target has no `/driverdecider` part and no `https://`).
3. Back in Settings > Pages, set Custom domain to `driverdecider.zombe.es` and save. When the DNS check passes,
   tick **Enforce HTTPS** (the certificate can take up to an hour to appear).
4. Recommended: verify zombe.es under your GitHub account's Settings > Pages > Verified domains (a TXT record),
   so no one else can point a GitHub Pages site at it.

With a custom domain set in Settings, an Actions-deployed site needs no `CNAME` file. All paths in `site/` are
relative, so the page works both at `simonkuhn.github.io/driverdecider/` and at `driverdecider.zombe.es`.
