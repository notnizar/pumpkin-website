# Pumpkin Group — Agency Website

Bilingual (English / Arabic) marketing site for **Pumpkin Group LLC**, a branding, marketing, advertising and digital agency based in Khilda, Amman, Jordan.

**Live preview:** https://claude.ai/artifact/SymUDGcwCajvjDa71KvuWt

## Features

- **English and Arabic** with a one-tap language switch. Arabic mode flips to right-to-left, swaps to Arabic typefaces (Cairo + IBM Plex Sans Arabic) and mirrors icons.
- **Three.js hero**: a particle pumpkin (~6k points, 10 ribs, stem, orbit ring and dust) that rotates, breathes and follows the mouse on desktop. Colors follow the site theme.
- **Light and dark themes** with a toggle; follows the visitor's system setting by default.
- **Phone-first layout**: pumpkin gets its own band above the headline, work tiles become a swipeable carousel, sticky "Start a project" bar, 44px+ tap targets, no horizontal scroll.
- **Performance**: pixel ratio capped at 1.5, fewer particles on phones, render loop pauses when the hero is off screen or the tab is hidden, `content-visibility: auto` on below-the-fold sections, Three.js loaded deferred from cdnjs, reduced-motion respected.
- Single self-contained HTML file. No build step.

## Files

| File | Purpose |
|---|---|
| `pumpkin-site.html` | Complete standalone page. Open in a browser or deploy as-is. |
| `index.html` | Same page without the `<html>/<head>/<body>` skeleton, for the Claude artifact host. |

## Run locally

Open `pumpkin-site.html` in any browser, or serve the folder:

```bash
npx serve .
```

Then visit `http://localhost:3000/pumpkin-site.html`.

## Deploy

Any static host works (GitHub Pages, Netlify, Vercel, Cloudflare Pages). Rename `pumpkin-site.html` to `index.html` at the deploy root, or point the host at it.

## Before sending to the client

These are placeholders and should be replaced with real content:

- Email address (`hello@pumpkinllc.com`) and studio hours
- The six "Selected work" tiles (generic sector examples, no real client names)
- The quote in the "Why Pumpkin" band
- The "Taking new clients for Q1 2027" pill
- The contact form shows a confirmation but does not send anywhere yet. Wire it to a form service (Formspree, Netlify Forms, etc.) or your own backend.

## Credits

Fonts via Google Fonts: Bricolage Grotesque, Figtree, Cairo, IBM Plex Sans Arabic. 3D via [three.js](https://threejs.org/) r128.
