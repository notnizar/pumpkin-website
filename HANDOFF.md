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
| `artifact.html` | Same content minus the `<!doctype>/<html>/<head>/<body>` skeleton. Used only for the Claude artifact host. Regenerate with `python3 scripts/build-artifact.py` after editing `index.html`. |
| `scripts/build-artifact.py` | The three-line derivation above. No other tooling. |
| `.github/workflows/pages.yml` | Deploys the repo root to GitHub Pages on every push to `main`. |
| `.nojekyll` | Tells Pages not to run Jekyll. |
| `README.md` | Public description, run and deploy notes. |
| `assets/favicon.svg` | Favicon: the nav logo mark with literal colours. |
| `assets/favicon-32.png`, `assets/apple-touch-icon.png` | PNG icons for browsers that ignore SVG favicons (Safari, older ones) and for iOS home screens. Rendered from `assets/icon.html`. |
| `assets/og-image.png` | 1200×630 Open Graph / Twitter card image. Rendered from `assets/og-image.html`, a still of the hero's particle pumpkin drawn on a canvas. |

No build step, no dependencies to install. Open `index.html` in a browser or run `npx serve .`.

## Deployment (live since 2026-10-15)

Pages is enabled with **Source: GitHub Actions** (created through the REST API with `build_type: workflow`, because the first workflow run could not enable it itself) and HTTPS is enforced. Every push to `main` redeploys. https://notnizar.github.io/pumpkin-website/ is live.

Gotcha for the future: the account's user site, `notnizar/notnizar.github.io`, used to carry a `CNAME` for `roommates-jo.me`. GitHub redirects every project site under an account to the user site's custom domain, and that domain now points at Vercel, so this site returned a 404 until the CNAME file and the custom domain were removed from the user site. Do not add a custom domain to the user site again unless its DNS points back at GitHub, or this site breaks again.

## Icons and the Open Graph image

`index.html` links `assets/favicon.svg` (primary), `assets/favicon-32.png` (browsers without SVG favicon support) and `assets/apple-touch-icon.png` (iOS), and carries `og:*` / `twitter:*` tags that point at `assets/og-image.png` (1200×630). The `theme-color` meta follows the active theme (`#141210` dark, `#fbf7f1` light); the theme toggle keeps it in sync.

The PNGs are rendered from two source pages with headless Chrome. From the repo root in PowerShell:

```powershell
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$root = (Get-Location).Path
$url = "file:///" + $root.Replace('\', '/')
$opts = "--headless=new", "--disable-gpu", "--hide-scrollbars", "--user-data-dir=$env:TEMP\pk-chrome"
& $chrome $opts --window-size=1200,630 --virtual-time-budget=10000 --screenshot="$root\assets\og-image.png" "$url/assets/og-image.html"
& $chrome $opts --window-size=180,180 --virtual-time-budget=3000 --screenshot="$root\assets\apple-touch-icon.png" "$url/assets/icon.html?size=180"
& $chrome $opts --default-background-color=00000000 --window-size=32,32 --virtual-time-budget=3000 --screenshot="$root\assets\favicon-32.png" "$url/assets/icon.html?size=32&bg=none"
```

`og-image.html` loads the Google Fonts, so it needs network access; the virtual-time budget lets the fonts arrive before the capture. Edit the headline or sub-line there if the hero copy changes. The `og:image` and `og:url` values are absolute, so they must change if the site moves to a custom domain.

## Architecture of the page

Single HTML file, ~68 KB. Sections in order: sticky nav, hero (Three.js canvas), orange marquee, About, Services (4 cards), Process (4 steps), Selected work (6 tiles), "Why Pumpkin" band, Contact (info + form), footer, phone-only sticky CTA.

**Theming.** All colors are CSS custom properties on `:root`. Dark is the default; light is applied via `@media (prefers-color-scheme: light)` and `:root[data-theme="light"]`. The nav button toggles `data-theme` and saves to `localStorage` key `pk-theme`.

**i18n.** Every translatable element has `data-i18n="key"` (innerHTML) or `data-i18n-ph="key"` (placeholder). English is read from the DOM at startup; Arabic lives in the `AR` object inside the main `<script>`. `setLang('ar')` swaps text, sets `dir="rtl"` and `lang="ar"` on `<html>`, changes `document.title`, and saves to `localStorage` key `pk-lang`. RTL-specific CSS is under `[dir="rtl"]` selectors. Icons that should mirror carry class `flip`. To add a string: give the element a `data-i18n` key and add the key to `AR`.

**Fonts.** Google Fonts: Bricolage Grotesque (Latin display), Figtree (Latin body), Cairo (Arabic display), IBM Plex Sans Arabic (Arabic body).

**Three.js hero.** `three.min.js` r128 (UMD) is loaded `defer` from cdnjs; `initHero()` runs on its `load` event. The scene is a `Group` containing a `Points` pumpkin (Fibonacci sphere, 10 cosine ribs, flattened, dimpled poles), a green stem `Points` cluster, a thin `RingGeometry` orbit, plus a separate dust `Points` cloud. Point sprites are a radial-gradient `CanvasTexture`. `layout()` reads the hero's real pixel geometry and places/scales the pumpkin: on ≥1000 px it fills the right 42.5% column beside the text (left column in RTL); below 1000 px the hero `.wrap` reserves a top band (`padding-top: clamp(170px,46vw,260px)`) and the pumpkin sits in it, aligned to the end side. Colors are re-read from CSS variables on theme change. Performance guards: DPR capped at 1.5, 2,600 points on phones vs 6,000 on desktop, no antialias, render loop runs only while the hero intersects the viewport and the tab is visible, mouse parallax only on hover-capable devices, reduced-motion renders one static frame.

**Motion system (added 2026-10-20).** The client asked for a visually rich, animation-heavy site. Everything moves only when `<html class="anim">` is present. A tiny inline script in `<head>` sets it before first paint when `prefers-reduced-motion` is not set and `IntersectionObserver` exists, and adds `html.intro` on the first visit of a browser session (`sessionStorage` key `pk-intro`). Without `.anim` nothing is hidden and the CSS marquee keyframes run as before, so no-JS, reduced-motion and old browsers get the finished page. The `<head>` script also carries a 4.5 s safety timer that adds `html.hero-in` and drops `html.intro` should the main script ever fail. Pieces, all in `index.html`:

- *Preloader* (`.preloader`, `html.intro`): orange curtain with the mark, wordmark and a progress line (`--pp`). Waits for `document.fonts.ready` and the Three.js `load`, minimum 1.4 s, maximum 2.6 s, then slides up with a rounded bottom edge and is removed from the DOM.
- *Hero entrance* (`html.hero-in`): `[data-hero]` elements fade and rise with `--i` stagger; the `h1` is split into words (`.split .w > .wi`, mask reveal). `heroIn()` also starts the fact counters (`[data-count]`) and fires the registered `onHeroIn` callbacks (the pumpkin assembly).
- *Word splitting* (`wrapWords`): wraps words, never letters, so Arabic shaping and ligatures survive. Keeps inline children (`<span class="o">`, `<em>`, `<strong>`). `setLang` replaces `innerHTML`, so `splitAll()` and `setupQuote()` run again after every language switch. Masks use `overflow:hidden` with padding/negative-margin compensation so descenders, diacritics and italic overhang are not clipped.
- *Scroll reveals*: `[data-reveal]` elements and every child of a `[data-stagger]` container start at `opacity:0; translate:0 28px` and get `.in` from one IntersectionObserver. `data-fx="pop"` scales instead. Inside the phone work carousel the tiles scale rather than translate so the scroller gets no vertical overflow. Entrances use the individual `translate`/`scale` properties so hover effects can still own `transform`.
- *Scroll engine* (`onScroll`, rAF-throttled, trackers only active while their section is near the viewport): nav `.scrolled` and `.nav-hidden` (hide on scroll-down past 180 px, show on scroll-up, never while the phone menu is open or within 1.5 s of a nav click), `#progress` (`--sp`), hero parallax (`--hp` on `#hero`, also read by the Three.js loop), process line `--p` on `#steps` plus `.is-active` on each `.step` once its top passes 62 % of the viewport, the scroll-lit quote (`--n` on `#quote`; each `.qw` word has `--i`, opacity is `clamp(.16, --n - --i + 1, 1)`), the footer word (`--fp` on `#footBig`), and work-tile art parallax (`--py` on `.art`, desktop only). Scroll spy uses a second IntersectionObserver with a thin root band at 40 to 45 % of the viewport.
- *Marquee*: under `.anim` it is moved by JS (`translate3d` plus a small `skewX`): base 72 px/s, up to +640 px/s with scroll velocity. Runs only while on screen and the tab is visible; `measureMarquee()` after rebuilds and resizes.
- *Pointer effects* (`(hover:hover) and (pointer:fine)` only): `.service` cards tilt (`--rx/--ry`, max 7°) and carry a spotlight (`--mx/--my`); `.btn` outside the form pulls toward the cursor (inline `transform`, springs back on leave); `#cursor` is a ring that follows with a lag, grows over links (`.is-link`), fills with an arrow over work tiles (`.is-view`) and hides over text fields (`.is-text`). Desktop ≥ 900 px only. The native cursor stays visible.
- *Three.js additions*: a `scatter` twin of every point, an eased `disp` buffer and a `live` buffer that is drawn. `mix` eases toward `max(intro, scroll²)`: the intro runs 1 → 0 over 2.2 s from `hero-in` (with an extra 1.8 rad spin and 25 % scale-up), scroll is a smoothstep of `heroScroll`. Cursor repel: the pointer ray is transformed into pumpkin space with `group.worldToLocal`, and points within 1.05 units of the ray are pushed away from it. The position buffer is re-uploaded only while `mix`, the pointer or the decaying displacement is changing, so an idle pumpkin costs what it did before. Particle count, DPR cap and the pause-when-off-screen logic are unchanged.
- *View transitions*: the theme button runs `document.startViewTransition` with a circular `clip-path` wipe from the button (`[data-vt="theme"]`), the language button a 0.45 s crossfade. Browsers without the API just apply the change.
- *Small things*: eyebrow line draws in, nav underline travels (origin flips in RTL), logo stem wiggles on hover, theme icon rotates between sun and moon, pill dot pings, hero glows drift (`.glow-a/.glow-b`) over a faint grid (`.grid-bg`), tile art drifts slowly (`.art::before`) with a shine sweep on hover, process dots light up, `.band-ring` spins behind the quote, chips pop, form fields glow on focus, submit shows a 0.9 s sending spinner and the success check draws itself with a small particle burst, copy button bumps, phone menu links stagger in, sticky phone CTA slides in, and `.grain` (an SVG `feTurbulence` tile stepping through eight positions) sits over everything on desktop at 7 % (5 % in light).

To add a revealed block: give the container `data-stagger` (children animate in sequence) or the element `data-reveal`. To add a split headline: add its selector to `SPLIT_SEL`. To turn everything off for a test: remove `anim` from `<html>` in DevTools.

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

Motion pass (2026-10-20), headless Chromium via Playwright with Three.js served from a local copy (cdnjs was not reachable from the test container) at 1400×900 and 390×844, English and Arabic, light and dark, plus reduced-motion and JavaScript-disabled runs: no console errors, no horizontal overflow in any run, headline word masks confirmed to animate (sampled every 180 ms after `hero-in`), process line and active steps, quote word lighting, nav hide/show, progress bar, cursor repel (visible hole through the pumpkin), card tilt and spotlight, magnetic button, theme wipe mid-transition, language switch re-splitting the headings, form sending state and success panel. Reduced motion renders the static page with one Three.js frame; the no-JS run shows the full page with no preloader.

Earlier pass:

Rendered in headless Chromium at 1400×900 and 390×844, English and Arabic, light theme: no horizontal overflow, no console errors, Three.js scene draws in all four combinations. Dark theme was checked visually only via the artifact preview.

## Ideas not yet done

- Replace tile art with real campaign images (WebP, lazy-loaded)
- Wire the form to a backend
- Optional: a custom domain in Pages settings
- Optional: a second Three.js moment on the contact section (keep it paused off-screen like the hero)
- Optional: tune motion for the client. Durations and easings are in the `:root` tokens (`--ease-out`, `--ease-in-out`) and the Motion system block at the end of the stylesheet; the preloader timing is `preMin`/`preMax` in the script.

## Git conventions used so far

Author: Nizar Zaid <nizar-zaid@4thtechjo.com>. Commits went straight to `main`, which is what deploys. The motion pass was developed on branch `claude/festive-volta-us5qvo`; merge it into `main` to deploy.
