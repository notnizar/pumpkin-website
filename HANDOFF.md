# Handoff: Pumpkin Group website

Context for continuing this project in a new session. Everything below is current as of the last push.

## What this is

A one-page bilingual (English / Arabic) marketing site for **Pumpkin Group LLC**, a branding, marketing, advertising and digital agency in Khilda, Amman, Jordan (founded 2020, 11–50 staff). The owner (Nizar) built it as a portfolio piece to show the agency what his web work looks like. Real facts about the company came from public LinkedIn/Behance listings. The "Selected work" projects are real, with their Behance covers and gallery links; the quote and contact details are still placeholders.

Repository: https://github.com/notnizar/pumpkin-website (public, branch `main`)
Intended live URL: https://notnizar.github.io/pumpkin-website/
Preview artifact (Claude): https://claude.ai/artifact/SymUDGcwCajvjDa71KvuWt

## Files

| File | Purpose |
|---|---|
| `index.html` | The complete standalone page. This is what GitHub Pages serves. Edit this one. |
| `artifact.html` | Same content minus the `<!doctype>/<html>/<head>/<body>` skeleton. Used only for the Claude artifact host. Regenerate with `python3 scripts/build-artifact.py` after editing `index.html`. |
| `scripts/build-artifact.py` | The three-line derivation above. |
| `scripts/work-backdrop.py` | Makes the blurred backdrop (`NAME-bg.webp`) for a Selected work cover. Needs Pillow. |
| `.github/workflows/pages.yml` | Deploys the repo root to GitHub Pages on every push to `main`. |
| `.nojekyll` | Tells Pages not to run Jekyll. |
| `README.md` | Public description, run and deploy notes. |
| `assets/favicon.svg` | Favicon: the nav logo mark with literal colours. |
| `assets/favicon-32.png`, `assets/apple-touch-icon.png` | PNG icons for browsers that ignore SVG favicons (Safari, older ones) and for iOS home screens. Rendered from `assets/icon.html`. |
| `assets/og-image.png` | 1200×630 Open Graph / Twitter card image. Rendered from `assets/og-image.html`, a still of the hero's particle pumpkin drawn on a canvas. |
| `assets/work/` | Selected work covers from Behance (`NAME.webp`, 808×632) and their tiny blurred backdrops (`NAME-bg.webp`). |

No build step, no dependencies to install (Pillow only if you regenerate a work backdrop). Open `index.html` in a browser or run `npx serve .`.

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

Single HTML file. Sections in order: sticky nav, hero (Three.js canvas), orange marquee, About, Services (4 cards), Process (4 steps), Selected work (6 Behance projects), "Why Pumpkin" band, Contact (info + form), footer, and up to 900 px a floating dock with a bottom-sheet menu (see "Phones and small tablets").

**Theming.** All colors are CSS custom properties on `:root`. Dark is the default; light is applied via `@media (prefers-color-scheme: light)` and `:root[data-theme="light"]`. The nav button toggles `data-theme` and saves to `localStorage` key `pk-theme`.

**i18n.** Every translatable element has `data-i18n="key"` (innerHTML) or `data-i18n-ph="key"` (placeholder). English is read from the DOM at startup; Arabic lives in the `AR` object inside the main `<script>`. `setLang('ar')` swaps text, sets `dir="rtl"` and `lang="ar"` on `<html>`, changes `document.title`, and saves to `localStorage` key `pk-lang`. RTL-specific CSS is under `[dir="rtl"]` selectors. Icons that should mirror carry class `flip`. To add a string: give the element a `data-i18n` key and add the key to `AR`.

**Fonts.** Google Fonts: Bricolage Grotesque (Latin display), Figtree (Latin body), Cairo (Arabic display), IBM Plex Sans Arabic (Arabic body).

**Three.js hero.** `three.min.js` r128 (UMD) is loaded `defer` from cdnjs; `initHero()` runs on its `load` event. The scene is a `Group` containing a `Points` pumpkin (Fibonacci sphere, 10 cosine ribs, flattened, dimpled poles), a green stem `Points` cluster, a thin `RingGeometry` orbit, plus a separate dust `Points` cloud. Point sprites are a radial-gradient `CanvasTexture`. `layout()` reads the hero's real pixel geometry and places/scales the pumpkin: on ≥1000 px it fills the right 42.5% column beside the text (left column in RTL); below 1000 px the hero `.wrap` reserves a top band (`padding-top: clamp(170px,46vw,260px)`) and the pumpkin sits in it, aligned to the end side. Colors are re-read from CSS variables on theme change. Performance guards: DPR capped at 1.5, 2,600 points on phones vs 6,000 on desktop, no antialias, render loop runs only while the hero intersects the viewport and the tab is visible, mouse parallax only on hover-capable devices, reduced-motion renders one static frame.

**Motion system (added 2026-10-20).** The client asked for a visually rich, animation-heavy site. Everything moves only when `<html class="anim">` is present. A tiny inline script in `<head>` sets it before first paint when `prefers-reduced-motion` is not set and `IntersectionObserver` exists, and adds `html.intro` on the first visit of a browser session (`sessionStorage` key `pk-intro`). Without `.anim` nothing is hidden and the CSS marquee keyframes run as before, so no-JS, reduced-motion and old browsers get the finished page. The `<head>` script also carries a 4.5 s safety timer that adds `html.hero-in` and drops `html.intro` should the main script ever fail. Pieces, all in `index.html`:

- *Preloader* (`.preloader`, `html.intro`): orange curtain with the mark, wordmark and a progress line (`--pp`). Waits for `document.fonts.ready` and the Three.js `load`, minimum 1.4 s, maximum 2.6 s, then slides up with a rounded bottom edge and is removed from the DOM.
- *Hero entrance* (`html.hero-in`): `[data-hero]` elements fade and rise with `--i` stagger; the `h1` is split into words (`.split .w > .wi`, mask reveal). `heroIn()` also starts the fact counters (`[data-count]`) and fires the registered `onHeroIn` callbacks (the pumpkin assembly).
- *Word splitting* (`wrapWords`): wraps words, never letters, so Arabic shaping and ligatures survive. Keeps inline children (`<span class="o">`, `<em>`, `<strong>`). `setLang` replaces `innerHTML`, so `splitAll()` and `setupQuote()` run again after every language switch. Masks use `overflow:hidden` with padding/negative-margin compensation (`.14em .16em .3em`) so descenders, the dots under a final yeh, diacritics and the synthesized italic overhang are not clipped; the per-word delay is capped at 480 ms (560 ms in the hero) so long headlines finish together. Headings are split on fine-pointer devices only (`fine`): phones reveal each heading as one block, which keeps the number of simultaneous transitions low while scrolling.
- *Scroll reveals*: `[data-reveal]` elements and every child of a `[data-stagger]` container start at `opacity:0; translate:0 28px` and get `.in` from one IntersectionObserver. `data-fx="pop"` scales instead. Inside the phone work carousel the tiles scale rather than translate so the scroller gets no vertical overflow. Entrances use the individual `translate`/`scale` properties so hover effects can still own `transform`.
- *Scroll engine* (`onScroll`, rAF-throttled, trackers only active while their section is near the viewport): nav `.scrolled` and `.nav-hidden` (hide on scroll-down past 180 px, show on scroll-up, never while the sheet is open or within 1.5 s of a nav or sheet link; hidden with `clip-path` rather than a transform so the bar's box stays put and keyboard focus into it never scrolls the page; `:focus-within` reveals it), `#progress` and the dock's ring (`--sp`), hero parallax (`--hp` on `#hero`, also read by the Three.js loop; on phones it tracks the pumpkin band, 320 px, and the copy fade/parallax applies only from 1000 px up, where the hero fits the viewport), process line `--p` on `#steps` plus `.is-active` on each `.step` once its top passes 62 % of the viewport, the scroll-lit quote (`--n` on `#quote`; each `.qw` word has `--i`, opacity is `clamp(.16, --n - --i + 1, 1)`), the footer word (`--fp` on `#footBig`), work-tile art parallax (`--py` on `.art`, desktop only), and on phones how far each service card is covered by the next (`--sd`). Scroll spy uses a second IntersectionObserver with a thin root band at 40 to 45 % of the viewport; it drives the nav underline, the dock label and the sheet's highlighted link, and runs with reduced motion too.
- *Marquee*: under `.anim` it is moved by JS (`translate3d` plus a small `skewX`): base 72 px/s, up to +640 px/s with scroll velocity. Runs only while on screen and the tab is visible. The loop width is re-measured by a ResizeObserver on the track and on `document.fonts.ready`, since the track is `max-content` and changes width when the web fonts swap in. `rebuildMarquee()` now also translates the live spans from `AR`/`EN` (the i18n pass only sees the original spans, which the rebuild detaches), which fixes a pre-existing bug where the band stayed English in Arabic mode.
- *Pointer effects* (`(hover:hover) and (pointer:fine)` only): `.service` cards tilt (`--rx/--ry`, max 7°) and carry a spotlight (`--mx/--my`); `.btn` outside the form pulls toward the cursor (inline `transform`, springs back on leave); `#cursor` is a ring that follows with a lag, grows over links (`.is-link`), fills with an arrow over work tiles (`.is-view`) and hides over text fields (`.is-text`). Desktop ≥ 900 px only. The native cursor stays visible.
- *Three.js additions*: a `scatter` twin of every point, an eased `disp` buffer and a `live` buffer that is drawn. `mix` eases toward `max(intro, scroll²)`: the intro runs 1 → 0 over 2.2 s from `hero-in` (with an extra 1.8 rad spin and 25 % scale-up), scroll is a smoothstep of `heroScroll`. Cursor repel: the pointer ray is transformed into pumpkin space with `group.worldToLocal`, and points within 1.05 units of the ray are pushed away from it. Burst (added with the phone pass): a click on the pumpkin (desktop) or a tap (touch) gives every point a kick away from the tap ray and out from the centre, strongest near the tap; `kick`/`kvel` are a damped spring per point (frame-rate independent via `fdt`), so the pumpkin puffs out, overshoots inward and wobbles back in about 1.3 s, with a small spin and a 12 ms vibration where supported. Touch spin adds `spinA` (with `spinV` inertia) to the Y rotation. The position buffer is re-uploaded only while `mix`, the pointer or the decaying displacement is changing, so an idle pumpkin costs what it did before. Particle count, DPR cap and the pause-when-off-screen logic are unchanged.
- *View transitions*: the theme button runs `document.startViewTransition` with a circular `clip-path` wipe from the button (`[data-vt="theme"]`), the language button a 0.45 s crossfade. Browsers without the API just apply the change. The target state is read inside the deferred callback, so a quick double tap still toggles twice.
- *Small things*: eyebrow line draws in, nav underline travels (origin flips in RTL), logo stem wiggles on hover, theme icon rotates between sun and moon, pill dot pings, hero glows drift (`.glow-a/.glow-b`) over a faint grid (`.grid-bg`), tile art drifts slowly (`.art::before`) with a shine sweep on hover, process dots light up, `.band-ring` spins behind the quote, chips pop, form fields glow on focus, submit shows a 0.9 s sending spinner and the success check draws itself with a small particle burst, copy button bumps, and `.grain` (an SVG `feTurbulence` tile stepping through eight positions) sits over everything on desktop at 7 % (5 % in light). Infinite animations pause while their section is off screen: `#hero` and `.band` get `.is-on` from an IntersectionObserver (glows, pill ping, ring), each `.tile` gets `.is-on` from the tile observer (art drift), and the scroll cue's line pauses once it has faded. On coarse pointers the tile drift and ring spin are off and the quote words have no opacity transition.

To add a revealed block: give the container `data-stagger` (children animate in sequence) or the element `data-reveal`. To add a split headline: add its selector to `SPLIT_SEL`. To turn everything off for a test: remove `anim` from `<html>` in DevTools.

**Selected work (added 2026-10-20; real covers and gallery links added the same day).** Six real projects from https://www.behance.net/PumpkinGroup, each tile showing the project's Behance cover and opening its gallery in a new tab:

| Tile | Behance project | Cover |
|---|---|---|
| DAMITCI | https://www.behance.net/gallery/115886219/DAMITCI-Restaurant-Food-Photography | `damitci.webp` |
| Smokey Burger | https://www.behance.net/gallery/117975989/Smokey-Outdoor-Videography | `smokey.webp` |
| Shaban | https://www.behance.net/gallery/235733203/Social-media-design-Shaban-rice | `shaban.webp` |
| Angelina’s Oven | https://www.behance.net/gallery/122865929/Angelinas-Oven | `angelinas-oven.webp` |
| Issa Ayyad Auto Trading | https://www.behance.net/gallery/234579661/Social-media-designs-Issa-Ayyad-Auto-trading | `issa-ayyad.webp` |
| Uncle Osaka | https://www.behance.net/gallery/117974685/Uncle-Osaca-Videography | `uncle-osaka.webp` |

Where a client has two projects, the tile links the one its tag names: Smokey's videography (its social media project is 117987605), Shaban rice (Shaban oil is 235661863), DAMITCI's food photography (DAMITCI social media is 116803729). Other projects on the profile: Stem social media, Chef House social media, Cedar. The Behance title says "Uncle Osaca", but the project's own description and its cover say Uncle Osaka, so the tile does too. Uncle Osaka sits last so the two videography covers (same TV-set design) are not stacked in one column. The copy says only what the project titles and descriptions support: no results, numbers or client quotes. The project descriptions would support sharper lines if wanted: DAMITCI is "an Italian restaurant located in Amman, Jordan" (its logo reads D'Amici Italian Kitchen); Uncle Osaka is "a Japanese cake shop based in Amman, Jordan"; Angelina's Oven is filed under Graphic Design and its cover is the brand's logo.

- *Markup*: each `.tile` is `.art` (ambient backdrop, first child, which the parallax code relies on), then `img.cover`, `.arrow` and `.meta`. The cover has `alt=""` because the tile's caption already names the project, and `loading="lazy"` with `width`/`height` so nothing shifts. Client names that are Arabic in origin (Shaban → شعبان, Issa Ayyad → عيسى عياد) have `data-i18n` on the `h3`; Latin brand names have none and stay Latin in Arabic mode. "See all projects on Behance" (`.work-more`) under the grid links the profile.
- *Layout*: Behance covers are 808×632 landscape title cards lettered almost to the edges, so they are never cropped. The cover sits whole at the top of the 4:5 tile, inset 12 px with a shadow, and the caption sits below it. Behind it, `.art-NAME::before` stretches `NAME-bg.webp`, a 48×38 pre-blurred copy of the cover (a few hundred bytes), into a soft colour field that matches each cover. The blur is baked into the file so the drifting layer carries no CSS `filter`.
- *Motion*: the backdrop keeps the shared slow drift (`artDrift`, paused off screen, off on touch) and the desktop scroll parallax, and scales up on hover; the cover lifts 4 px on hover, alongside the existing shine sweep, arrow fill and caption lift.
- *Swapping a project*: save its Behance cover (the 808 px WebP from the profile's project card) as `assets/work/NAME.webp`, run `python3 scripts/work-backdrop.py assets/work/NAME.webp`, then point the tile's `href`, its `img` and its `.art-*` rule in the stylesheet at the new files. Behance project pages sit behind a JavaScript challenge, so fetch them with a real browser (headless Chromium works); the profile page and the image CDN answer plain requests.

The CSS illustrations that stood in for the covers (viewfinder, REC frame, phone feed, oven, film strip, speedometer) were removed with their keyframes. One of those keyframes reused the name `bob` and had been overriding the logo's hover wiggle; the logo has its own squash-and-stretch back.

**Other performance choices.** `content-visibility: auto` on every section after the hero (class `lazy`), nav `backdrop-filter` only ≥900 px, marquee animates `transform` only, scroll handler throttled with `requestAnimationFrame`.

**Phones and small tablets (added 2026-10-20).** The client asked for mobile to have its own design and animations. Everything is in the block at the end of the stylesheet ("Phones and small tablets") plus the nav/dock/sheet, carousel, ripple and in-page link sections of the script; desktop above 900 px is unchanged apart from the pumpkin burst.

- *Dock* (`#dock`, up to 900 px, replaces the old top Menu dropdown and the sticky "Start a project" bar): a floating pill at the bottom (safe-area aware, max 560 px wide). Left: `#dockMenu`, the pumpkin mark inside a scroll-progress ring (SVG circle, `pathLength=100`, `--sp` from the scroll engine), the current section's name (`#dockNow`, slides in on change via `.swap`) and its index (`#dockIdx`, wrapped in LRI/PDI so RTL keeps "01 / 06"). Right: the orange CTA, which folds away (`.at-contact`) while the contact section is on screen. It slides up after `hero-in`. Without JavaScript only the CTA shows, full width. The top bar keeps the logo, language and theme buttons; the top progress line is hidden up to 900 px (the ring replaces it).
- *Sheet* (`#sheet`, `role="dialog"`, `hidden` until opened): slides up from the bottom, links stagger in (numbered, the current section in orange), then "Say hello" with the email and four social icons. While open, `html.sheet-lock` stops page scroll and the nav, `main`, footer and dock are `inert`; focus goes to × and comes back to the dock button; Tab wraps; Esc, the scrim, × or a swipe down on the header close it (past 110 px or a quick flick; it follows the finger and resists upward pulls). A section link closes it and the browser follows the anchor. It closes itself if the viewport grows past 900 px.
- *In-page links*: sections use `content-visibility: auto`, so before they render they are laid out at an estimated height and a long smooth scroll could land short (a sheet link to Work ended 140 px off). After any `#` link, `settleOn()` waits for the page to stop moving and re-aims if the target is more than 4 px from its `scroll-margin-top` (up to three times; not at the page end). This fixes desktop nav links too.
- *Phone hero* (up to 699 px): the pumpkin sits centred in a taller band (`--band`, `clamp(250px,70vw,310px)`) and the copy is centred under it; the facts sit in one row of three. The headline gets the per-word mask reveal on phones too (only the hero `h1` is split on touch). `.pk-hit`, a circle placed over the pumpkin by the Three.js `layout()`, takes touch with `touch-action: pan-y`: a sideways swipe spins the pumpkin with inertia and the finger parts the points, a tap bursts it, vertical swipes still scroll the page. A hint pill ("Swipe to spin · tap to burst", `#pkHint`) appears 2.6 s after the pumpkin assembles and goes on first touch or after 9.5 s; once played it stays hidden for the session (`sessionStorage` key `pk-played`). Without JavaScript the band collapses.
- *Services* (up to 699 px): the cards are `position: sticky`, each 14 px lower than the last (`--k`), so they pile up as you scroll; a covered card shrinks up to 7 % and its content dims (`--sd`).
- *Process* (all widths with motion, previously 800 px up): the rail fills as you scroll and each dot lights up; on phones the steps slide in from the rail's side and the dot pings when it lights.
- *Work carousel* (up to 699 px): tiles snap to the centre; while the row scrolls each tile turns away, shrinks and dims by its distance from the centre (`--cr`, `--cs`, `--cd`, set in `carousel()`); page dots under the row stretch toward the nearest tile (`--a`); the first time the row is 60 % in view it peeks at the next tile (`.peek`), unless it was already swiped; the swipe hint fades after the first touch.
- *Headings* (up to 699 px): each section heading rises out of a mask as one block. The mask is a keyframe (`maskUp`) that starts with `.in`, because a `clip-path` on the hidden state also hides the heading from the reveal observer (Chrome counts the target's own clip).
- *Touch feedback*: buttons and the dock pieces shrink slightly while pressed (`hover: none`), and a ripple spreads from the finger on buttons and the dock CTA (`.ripple`, removed after 0.7 s).
- Unchanged from before: buttons go full width below 520 px, all inputs are 16 px to stop iOS zoom, tap targets are at least 44 px. `scroll-padding-bottom: 96px` keeps focused fields clear of the dock, and the footer word leaves room for it.

**Form.** `#contactForm` validates name and email client-side, then swaps `#formFields` for `#formSuccess` in place. It does not submit anywhere. To make it real, POST the fields to Formspree/Netlify Forms/your API inside the `submit` handler before showing success.

## Placeholders to replace before the client sees it

- `hello@pumpkinllc.com` (guessed from their Behance domain) and the studio hours
- The quote in the "Why Pumpkin" band (written as a brand promise, not a testimonial)
- "Taking new clients for Q1 2027" pill
- Social links point to: instagram.com/pumpkin.llc, facebook.com/Pumpkin.groupllc, linkedin.com/company/pumpkin-group-llc, behance.net/PumpkinGroup (these are the real public profiles)

## Testing done

Phone design pass (2026-10-20), headless Chromium via Playwright with real touch input (CDP touch events), local server: 360×740, 390×844, 430×932, 768×1024 and 1400×900, English and Arabic, light and dark, plus reduced-motion and JavaScript-disabled runs. No console errors and no horizontal overflow in any run. Checked: dock label and index follow the sections (Arabic included, index reads 01 / 06); the ring fills; the CTA folds away at Contact; the sheet opens (lock, inert, focus on ×, aria-expanded), its Work, Process, Contact and About links land exactly at the section top and update the hash, swipe-down and Esc close it, Shift+Tab wraps inside it and focus returns to the dock; a tap bursts the pumpkin and hides the hint, a sideways swipe on it does not scroll the page while a vertical one does; the carousel turns tiles in 3D mid-swipe and the dots follow; the service cards stack (`--sd` near 0.95 on covered cards); headings reveal; the desktop click-burst works, the cursor turns to a pointer over the pumpkin, and the dock and sheet stay hidden above 900 px. Not tested on real devices: iOS Safari's handling of `overflow: hidden` for the sheet lock and of the `touch-action: pan-y` target are worth a check on an iPhone.

Covers and links pass (2026-10-20), headless Chromium via Playwright, local server: 1400×1000, 820×1180, 390×844 and 360×740, English and Arabic, light and dark, plus reduced-motion and JavaScript-disabled runs. No console errors and no horizontal overflow in any run. Checked: every tile's `href` is its Behance gallery; all six covers load on desktop, and on the phone carousel the lazy ones load as you swipe; the covers are uncropped in the 3- and 2-column grids and the phone carousel and clear of the caption fade on phones; backdrops show behind each cover; hover lifts the cover; the no-JS and reduced-motion renders show every cover.

Selected work pass (2026-10-20), headless Chromium via Playwright, local server, fonts and cdnjs blocked: 1400×900 and 390×844, English and Arabic, light and dark, plus reduced-motion and JavaScript-disabled runs. No console errors and no horizontal overflow in any run. Checked: all six tiles linked to the Behance profile in a new tab (since replaced by gallery links); Arabic round trip through the language button (tags, Arabic client names, button and heading switch and switch back); every tile's hover state; scene animations (since removed) were paused while their tile was off screen, running once it is on screen, absent on a touch device and with reduced motion; the static no-JS render shows every scene; the phone swipe hint now displays.

Pre-deploy review (2026-10-20): four independent reviewers (JS runtime, cross-browser CSS, RTL/i18n/a11y, mobile performance) over the diff, each finding adversarially re-checked against the code. Ten confirmed, all fixed before merging: hero copy faded while still mid-screen on phones; a double tap on the theme or language button re-applied the same state because the target was computed before the deferred view-transition callback; the marquee loop width was measured before web fonts loaded, so the band snapped at every wrap; the marquee never switched to Arabic (pre-existing); word masks clipped the dots under a final yeh and the italic `y`; tabbing into the scroll-hidden nav scrolled the page; too many simultaneous transitions on phones (word masks, tile drift) and infinite animations ticking while off screen. Three findings were refuted (no `color-mix` fallback in Safari 16.0, read/write interleaving in the scroll handler, paint-layer churn on the quote words).

Motion pass (2026-10-20), headless Chromium via Playwright with Three.js served from a local copy (cdnjs was not reachable from the test container) at 1400×900 and 390×844, English and Arabic, light and dark, plus reduced-motion and JavaScript-disabled runs: no console errors, no horizontal overflow in any run, headline word masks confirmed to animate (sampled every 180 ms after `hero-in`), process line and active steps, quote word lighting, nav hide/show, progress bar, cursor repel (visible hole through the pumpkin), card tilt and spotlight, magnetic button, theme wipe mid-transition, language switch re-splitting the headings, form sending state and success panel. Reduced motion renders the static page with one Three.js frame; the no-JS run shows the full page with no preloader.

Earlier pass:

Rendered in headless Chromium at 1400×900 and 390×844, English and Arabic, light theme: no horizontal overflow, no console errors, Three.js scene draws in all four combinations. Dark theme was checked visually only via the artifact preview.

## Ideas not yet done

- Wire the form to a backend
- Optional: a custom domain in Pages settings
- Optional: a second Three.js moment on the contact section (keep it paused off-screen like the hero)
- Optional: tune motion for the client. Durations and easings are in the `:root` tokens (`--ease-out`, `--ease-in-out`) and the Motion system block at the end of the stylesheet; the preloader timing is `preMin`/`preMax` in the script.

## Git conventions used so far

Author: Nizar Zaid <nizar-zaid@4thtechjo.com>. Commits went straight to `main`, which is what deploys. The motion pass was developed on branch `claude/festive-volta-us5qvo`; merge it into `main` to deploy.
