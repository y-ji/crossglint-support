# CROSSGLINT Support

Official app-support website for CROSSGLINT, a Japan-based independent app
development brand.

## Live website

- Support: https://y-ji.github.io/crossglint-support/
- QR Maker privacy policy (日本語 / English): https://y-ji.github.io/crossglint-support/privacy.html

Hosted by GitHub Pages from `main` / root. Review content and assets in
pull requests **before merging**; merging to `main` publishes site changes.

## Site files

- `index.html` — CROSSGLINT-branded support homepage, QR Maker product card,
  contact address, English support note
- `privacy.html` — bilingual privacy policy, shared branding and navigation
- `style.css` — responsive styles; no JS, analytics, trackers, external fonts
- `assets/crossglint-mark-400.png` — official approved CG profile raster
- `assets/crossglint-header-1500x500.png` — approved quiet-horizon banner

## Brand asset provenance

The two PNGs are **unchanged copies** of selected approved raster exports from
the private brand-source repository `y-ji/crossglint-brand`:

| Public site asset | Private brand source | Git blob SHA |
| --- | --- | --- |
| `assets/crossglint-mark-400.png` | `assets/exports/x_profile_400.png` | `f36cce9749185d74fecb3efbe69c127fca46f57e` |
| `assets/crossglint-header-1500x500.png` | `assets/exports/x_header_1500x500.png` | `03b6774b3e40dab937fd238efa9c36b3182fb55f` |

The brand repo's `brand/BRAND_GUIDELINES.md` remains the **source of truth**
for brand decisions. Its SVG master and exact final color typography remain
undecided; this website uses existing raster images and guideline palette
direction, without claiming a final SVG master.

The image exports are deliberately copied into this **public** support repo
because a GitHub Pages browser cannot fetch assets from a private GitHub
repository. Do not change visibility of `ios-wifi-qr` or `crossglint-brand`.

## Local review

Open `index.html` and `privacy.html` in a browser, or run a local static
server to inspect the same relative assets and links:

```sh
python3 -m http.server 8000
```

Review at desktop and mobile widths, check the actual email link and both
language sections. Run `python3 scripts/check_site.py` for integrity checks.

## Publishing & app release

- Owner approval is required before PR merge to the published `main` branch.
- Pages deployment success and signed-out HTTPS access are verified separately.
- The app's privacy policy URL should match the public site.
- Public support contact (owner-approved): `crossglint.studio@gmail.com`.
- No private personal data, QR inputs, or app source files are included.
