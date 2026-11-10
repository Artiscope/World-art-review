# World Art Review

Discover Artists. Understand Art.

An editorial site of researched artist portfolios, artwork reviews, collecting guides and technique explainers. Starts with Zara Muse and Konn Artiss, and grows to cover the Grove Gallery artists.

## What is here

- `index.html`: the whole site in one file. The content lives in four lists at the top of the script (SOURCES, ARTISTS, ARTICLES, GUIDES). Add an entry to add an artist, artwork, article or source. Each artist can carry an `image`, `alt` and four `ghostWords`; each article an `image` and `alt`.
- `design/`: the design canvas files from the first homepage and portfolio sample.
- `.github/workflows/pages.yml`: publishes the site to GitHub Pages on every push to `main`.

## Running it

Open `index.html` in a browser. There is no build step.

## Publishing

Pushes to `main` publish automatically to GitHub Pages. Turn Pages on once in the repository settings (Settings, then Pages, then set Source to GitHub Actions).

## House rules for the design

- Colours: Oatmilk #EEE5D4 for pages and cards (about 60%), Calm Green #1D4A35 for bands, buttons and labels (about 30%), brick #B5392B for links and highlights (about 10%). Text is charcoal #1D1D1B.

- Typefaces: Castoro for the name and headlines, Literata for reading text, Libre Franklin for small text and buttons. Logo and colours follow the World Art Review logo guidelines (version 2.0, November 2026).
- No long dashes, no long dividing lines, no spaced capital labels, no rounded corners. Eyebrows are sentence case with a small square.
- Motion: a spring helper and three reveal behaviours (line and word reveals, in-view reveals, hover springs), plus Lenis smooth scrolling on the homepage. All of it switches off for people who prefer reduced motion.
- UK spelling throughout.
- Every fact in a portfolio carries a numbered source. Claims that come only from publicity are marked Reported.
