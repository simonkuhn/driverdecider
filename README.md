# Driver Decider

A one-page site that shows the used cars from the "First car comparison" sheet as cards, built for iPhone first.
It is published with GitHub Pages and is meant to live at **zombe.es/driverdecider**.

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
| `site/` | What GitHub Pages publishes: `index.html` (made from `web/page.html`), `data.js`, `img/`. All paths are relative, so it works under `/driverdecider/`. |
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
   Without a custom domain the site is at `https://simonkuhn.github.io/driverdecider/`.
2. To serve it at `zombe.es/driverdecider`, give the account's user site the custom domain `zombe.es`.
   A project site like this one then appears under that domain at `/driverdecider/` automatically.
   - Create the public repository `simonkuhn.github.io` with an `index.html`, and in its Settings > Pages
     publish from the `main` branch and set Custom domain to `zombe.es`.
   - At the DNS host for zombe.es, add these records for the apex (`zombe.es`):
     - A: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
     - AAAA (optional, for IPv6): `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
     - CNAME `www` to `simonkuhn.github.io` (optional, so www.zombe.es redirects to zombe.es)
   - Once the DNS check passes, tick **Enforce HTTPS** in the user site's Pages settings.
   - Recommended: verify zombe.es under your GitHub account's Settings > Pages, so no one else can claim it.
