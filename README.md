# CROSSGLINT Support

Public-facing static support website for CROSSGLINT iOS applications.

## Pages

- `index.html` — QR Maker support page (Japanese, brief English)
- `privacy.html` — QR Maker privacy policy (Japanese and English)
- `style.css` — local responsive styling

No JavaScript, external fonts, analytics, tracking pixels, or runtime dependencies.

## Publishing

This pull request stages the site for **review before public GitHub Pages deployment**.
Do not enable GitHub Pages or merge until the site copy and privacy claims have been reviewed.
This repository is public, so content on branches and pull requests is publicly readable
even before Pages deployment. The iOS application source repository stays private.

After approval and merge:

1. In repository **Settings > Pages**, choose **Deploy from a branch**, `main`,
   folder `/(root)`, then Save.
2. Check the **actual** deployed Support and Privacy Policy HTTPS URLs in a
   signed-out browser. Do not assume a URL is live until confirmed.
3. Put the verified support and privacy URLs into App Store Connect.
4. Add the privacy policy URL to QR Maker's in-app UI via a separate pull request
   before submitting v1.0 for review.

Public support contact, approved by the project owner: crossglint.studio@gmail.com.

Do not upload real QR payloads, private Wi-Fi information, user-provided photos,
or proprietary app code to this repository.
