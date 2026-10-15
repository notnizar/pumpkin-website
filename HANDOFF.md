# Handoff: Pumpkin Group website

Context for continuing this project in a new session. Everything below is current as of the last push.

## What this is

A one-page bilingual (English / Arabic) marketing site for **Pumpkin Group LLC**, a branding, marketing, advertising and digital agency in Khilda, Amman, Jordan (founded 2020, 11–50 staff). The owner (Nizar) built it as a portfolio piece to show the agency what his web work looks like. Real facts about the company came from public LinkedIn/Behance listings; all client work, quotes and contact details are placeholders.

Repository: https://github.com/notnizar/pumpkin-website (public, branch `main`)
Intended live URL: https://notnizar.github.io/pumpkin-website/
Preview artifact (Claude): https://claude.ai/artifact/SymUDGcwCajvjDa71KvuWt

## Files

| File | Purpose |
|---|---|
| `index.html` | The complete standalone page. This is what GitHub Pages serves. Edit this one. |
| `artifact.html` | Same content minus the `<!doctype>/<html>/<head>/<body>` skeleton. Used only for the Claude artifact host. Regenerate from `index.html` if both need to stay in sync (or ignore it). |
| `.github/workflows/pages.yml` | Deploys the repo root to GitHub Pages on every push to `main`. |
| `.nojekyll` | Tells Pages not to run Jekyll. |
| `README.md` | Public description, run and deploy notes. |

No build step, no dependencies to install. Open `index.html` in a browser or run `npx serve .`.

## Immediate next step (blocked on a settings click)

The Pages workflow ran once and failed at "Configure Pages" because the Actions token can't enable Pages on its own.

1. Go to https://github.com/notnizar/pumpkin-website/settings/pages
2. Set **Source** to **GitHub Actions**.
3. Re-run the workflow: Actions tab → "Deploy to GitHub Pages" → "Run workflow", or just push any commit.
4. Confirm https://notnizar.github.io/pumpkin-website/ loads.

## Architecture of the page

Single HTML file, ~68 KB. Sections in order: sticky nav, hero (Three.js canvas), orange marquee, About, Services (4 cards), Process (4 steps), Selected work (6 tiles), "Why Pumpkin" band, Contact (info + form), footer, phone-only sticky CTA.

**Theming.** All colors are CSS custom properties on `:root`. Dark is the default; light is applied via `@media (prefers-color-scheme: light)` and `:root[data-theme="light"]`. The nav button toggles `data-theme` and saves to `localStorage` key `pk-theme`.

**i18n.** Every translatable element has `data-i18n="key"` (innerHTML) or `data-i18n-ph="key"` (placeholder). English is read from the DOM at startup; Arabic lives in the `AR` object inside the main `<script>`. `setLang('ar')` swaps text, sets `dir="rtl"` and `lang="ar"` on `<html>`, changes `document.title`, and saves to `localStorage` key `pk-lang`. RTL-specific CSS is under `[dir="rtl"]` selectors. Icons that should mirror carry class `flip`. To add a string: give the element a `data-i18n` key and add the key to `AR`.

**Fonts.** Google Fonts: Bricolage Grotesque (Latin display), Figtree (Latin body), Cairo (Arabic display), IBM Plex Sans Arabic (Arabic body).

**Three.js hero.** `three.min.js` r128 (UMD) is loaded `defer` from cdnjs; `initHero()` runs on its `load` event. The scene is a `Group` containing a `Points` pumpkin (Fibonacci sphere, 10 cosine ribs, flattened, dimpled poles), a green stem `Points` cluster, a thin `RingGeometry` orbit, plus a separate dust `Points` cloud. Point sprites are a radial-gradient `CanvasTexture`. `layout()` reads the hero's real pixel geometry and places/scales the pumpkin: on ≥1000 px it fills the right 42.5% column beside the text (left column in RTL); below 1000 px the hero `.wrap` reserves a top band (`padding-top: clamp(170px,46vw,260px)`) and the pumpkin sits in it, aligned to the end side. Colors are re-read from CSS variables on theme change. Performance guards: DPR capped at 1.5, 2,600 points on phones vs 6,000 on desktop, no antialias, render loop runs only while the hero intersects the viewport and the tab is visible, mouse parallax only on hover-capable devices, reduced-motion renders one static frame.

**Other performance choices.** `content-visibility: auto` on every section after the hero (class `lazy`), nav `backdrop-filter` only ≥900 px, marquee animates `transform` only, scroll handler throttled with `requestAnimationFrame`.

**Phone layout.** Work tiles become a horizontal snap-scroll row below 700 px (`.work-scroller`), with a "swipe" hint. A fixed bottom "Start a project" bar (`#stickyCta`) shows below 900 px and hides when the contact section is in view. Buttons go full width below 520 px; all inputs are 16 px to stop iOS zoom; tap targets ≥ 44 px.

**Form.** `#contactForm` validates name and email client-side, then swaps `#formFields` for `#formSuccess` in place. It does not submit anywhere. To make it real, POST the fields to Formspree/Netlify Forms/your API inside the `submit` handler before showing success.

## Placeholders to replace before the client sees it

- `hello@pumpkinllc.com` (guessed from their Behance domain) and the studio hours
- The six work tiles: generic sector examples with CSS-gradient art, no real clients
- The quote in the "Why Pumpkin" band (written as a brand promise, not a testimonial)
- "Taking new clients for Q1 2027" pill
- Social links point to: instagram.com/pumpkin.llc, facebook.com/Pumpkin.groupllc, linkedin.com/company/pumpkin-group-llc, behance.net/PumpkinGroup (these are the real public profiles)

## Testing done

Rendered in headless Chromium at 1400×900 and 390×844, English and Arabic, light theme: no horizontal overflow, no console errors, Three.js scene draws in all four combinations. Dark theme was checked visually only via the artifact preview.

## Ideas not yet done

- Replace tile art with real campaign images (WebP, lazy-loaded)
- Wire the form to a backend
- Add `<meta property="og:*">` tags and a favicon file
- Optional: a custom domain in Pages settings
- Optional: a second Three.js moment on the contact section (keep it paused off-screen like the hero)

## Git conventions used so far

Author: Nizar Zaid <nizar-zaid@4thtechjo.com>. Three commits on `main`. No branches, no PRs.
