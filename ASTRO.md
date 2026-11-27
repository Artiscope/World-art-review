# How Astro builds this site

Since the move to Astro, nothing about the pages, their addresses or how
they are edited has changed.

- The words still live in `content/site.json`, the home page sections in
  `content/pages.json` and the design in `src/index.html`. Artiscope
  Digital Home reads and writes the content files as before, and its
  preview still matches the published page, because the pages are still
  made by `tools/build_site.py` (gathered by `.github/scripts/assemble.sh`).
- Every page still carries its piece as plain HTML inside `<main>`, so
  search engines and AI search tools can read it without running scripts.
- Checks run before every build and stop it with a plain list of what to
  fix:
  - `src/lib/checks.mjs`: every numbered source used in an article,
    portfolio or quiz clue is listed under sources; every quiz round uses
    a photo already in `images/`, a known artist, three published artists
    as the other choices, and sourced clues.
  - `src/content.config.ts`: every source has a title and, where it is
    online, a working-looking link; every article has a known section and
    its words; every portfolio has a name and a web address.
- `src/lib/site.mjs` hands the pages to Astro and puts everything else
  (pictures, assets, sitemap, robots.txt, llms.txt) into `public/`
  unchanged. It adds two things to the head of each page: a short
  cross-fade between pages with the top bar held still, and fetching of a
  page in the background as soon as a reader presses on its link. That
  waits for a press, not a hover, because each page here carries the
  whole site and is large. Browsers that cannot do either simply change
  page as before.
- `src/index.html` is still the design. Astro's own files sit beside it in
  `src/lib/` and `src/pages/`.

Commands: `npm ci` once, then `npx astro dev` for a local copy that
reloads as you edit (content, pictures and the design included), or
`npx astro build` to build into `_site`.
