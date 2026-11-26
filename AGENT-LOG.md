# Agent log

A record of what the website agent did on each run, newest first.

## Thursday 26 November 2026, home page matched to the site brief (draft)
Published: nothing. The owner sent a new brief for all five sites. The home page now opens with "Discover the Artists. Understand the Art." and the brief's introduction, and the Read by section list is back on, under the featured artists, with Artist A to Z, Art Explained, Collector's Library, Recent Reviews and Exhibition Guides. The tagline in the page description and CLAUDE.md is updated to match.
Checked: the site builds, the home page holds at 390 pixels and desktop width.
Needs you: a yes on the pull request.

## Wednesday 25 November 2026, tiles for Reviews and Art Explained (draft)
Published: nothing. Design change the owner asked for: the Reviews and Art Explained pages now show their pieces as tiles (picture or colour block, kind of piece, title, summary, reading time), three across on a computer, two on a tablet and one on a phone. Collector's Library is unchanged.
Checked: the site builds, both pages hold at 390 pixels and desktop width with no page errors.
Needs you: a yes on the pull request.

## Wednesday 25 November 2026, filling the gaps across the site (draft)
Published: nothing. Prepared as a draft after the owner asked for every missing piece of content to be researched and filled.
Drafts waiting: new Life and career sections for 16 portfolios and In their own words for 14, Explore more for three, about 20 artwork details and many timeline dates, eight exhibition guides, an Our relationships paragraph on the standards page, and a site byline in place of the author placeholder. Pull request: https://github.com/Artiscope/World-art-review/pull/19
Checked: every citation points to a listed source, no placeholder text is left apart from photos and a few artwork details no source gives, and the site builds with 34 artists and works at phone and desktop width.
Needs you: confirm the Our relationships wording. The pull request lists what could not be sourced.

## Wednesday 25 November 2026, pages search engines can find (draft)
Published: nothing. Prepared after the owner asked for the SEO problems found on 25 November to be fixed.
Changed: every published portfolio and article now also has its own web address (artists/<name>/ and articles/<name>/), opening straight on that piece with its own title, search description and structured data. The links on every page lead to these addresses. The site now has a robots.txt and a sitemap listing the home page and all 97 addresses. The look, words and layout are unchanged, and src/index.html is untouched: all of this is done by tools/build_site.py.
Checked: the site builds, a portfolio and an article open on their own address with no page errors, and links between pieces work.
Needs you: a yes on the pull request, then adding the site to Google Search Console and sending it the sitemap.

## Wednesday 25 November 2026, reviews and artwork explainers (draft)
Published: nothing. Added as a draft after the owner asked for more reviews and art explained pieces for every artist.
Drafts waiting: 20 new reviews and 22 artwork explainers, one or both for every published artist, plus a short feature introducing them at the top of the homepage list. 59 new numbered sources, all opened and read: named reviews in The Art Newspaper, Apollo, The Arts Desk, Studio International, Frieze, e-flux, The Brooklyn Rail, The New York Times and others, plus museum and gallery pages. Review and Art Explained list introductions updated. Pull request: https://github.com/Artiscope/World-art-review/pull/16
Checked: every citation points to a listed source, every internal link works, the site builds with 23 artists and 62 articles, and pages hold at phone and desktop width with no page errors. No long dashes or words from the banned list.
Left alone: Zen Xander (not yet published) and the artists being added in a separate change. Zara Muse and Konn Artiss get an explainer each but no new review, as no independent published criticism could be found. The research desk now says so.
Needs you: photographs for the new pieces (41 empty spots added to image-slots.json). Two explainers reuse photos already on the site.

## Wednesday 25 November 2026, fuller artist portfolios
Published: on the owner's go ahead, after the owner asked for more detailed information about each artist on every site.
Changed: nineteen portfolios gain three new parts each: Life and career, In their own words (short named quotes) and Explore more (links to related portfolios on this site). Some also gain works and timeline dates. 36 new numbered sources, all interviews, museum pages, letters or press releases that were opened and read.
Checked: every new citation points to a listed source. The site builds with 22 artists. Portfolios hold at phone and desktop width with no page errors. No long dashes.
Left alone: Konn Artiss, Zen Xander and Zara Muse (nothing new found that could be checked). No interview quote could be confirmed for Rene Matić, so that portfolio has no quotes. Andy Warhol has his own portfolio from a separate change.
Needs you: nothing.

## Wednesday 25 November 2026, Andy Warhol (draft)
Published: nothing. Andy Warhol portfolio added as a draft after the owner asked for him on all five sites.
Drafts waiting: portfolio (biography, style, three works, timeline, research desk items), a short feature "Andy Warhol: a portfolio of the artist who made repetition the subject" at the top of the homepage list, and a public domain 1977 White House portrait. Branch draft/2026-11-25-andy-warhol.
Checked: MoMA, Tate, Wikipedia, The Art Newspaper, e-flux, Sotheby's lot page.
Needs you: nothing beyond review.

## Wednesday 25 November 2026, Mohamed L'Ghacham (draft)
Published: the five portfolios for Rene Matić, Raven Halfmoon, Ana Segovia, Dana Awartani and Jes Fan went live on the owner's go ahead (pull request 12).
Drafts waiting: portfolio for Mohamed L'Ghacham, a muralist from the emerging artists research. Homepage count now twenty-two.
Checked: festival pages (Nuart Aberdeen, North West Walls, Vision Art Festival, Calle Libre), Colossal, Street Art United States, The Crystal Ship and the artist's website. No auction results found.
Needs you: photographs for the portfolio and its three works (spots added to image-slots.json).

## Wednesday 25 November 2026
Published: nothing yet.
Drafts waiting: five new portfolios (Rene Matić, Raven Halfmoon, Ana Segovia, Dana Awartani, Jes Fan) and a short feature introducing them. The research desk picks up their open questions. Pull request: https://github.com/Artiscope/World-art-review/pull/16
Checked: gallery, museum, biennale and auction pages for all five artists.
Needs you: photographs for the five portfolios and their works (spots added to image-slots.json).

## Wednesday 25 November 2026, Kandinsky record price (draft)
Published: nothing. Prepared as a draft after the price check on Global Art Monitor.
Drafts waiting: Kandinsky: exact record price from Christie's lot page, https://github.com/Artiscope/World-art-review/pull/11
Checked: Christie's lot page for Betonte Ecken (lot 12 A, US$85,780,000, 130 x 130 cm). The other auction figures in the portfolios already read as reported and agree with what was confirmed.
Needs you: nothing.

## Monday 23 November 2026, Van Gogh and Kandinsky portfolios
Published: portfolios for Vincent van Gogh and Wassily Kandinsky, whose paintings set auction records in New York in November 2026. The artists list now says sixteen artists. Published on the owner's instruction in a conversation ("once everything is done. merge and publish").
Drafts waiting: none from this change.
Checked: Kröller-Müller Museum, Guggenheim Bilbao, Art Gallery of NSW and Tate pages; Sotheby's lot page for Châtaigniers en fleurs; The Art Newspaper, Artsy and Art Insider for the sales. The Van Gogh Museum pages gave little text to automated visits. Image spots added; no images placed.
Needs you: photographs, if you would like them. Both artists' paintings are old enough to be out of copyright, so museum photos in the public domain could be used.

## Monday 23 November 2026, images for the new street artists (draft)
Published: nothing. Prepared as a draft on the owner's request in a conversation to add images for the five new street artists.
Drafts waiting: portfolio images for Vhils, OSGEMEOS and Faith XLVII (link in the pull request list).
Checked: each licence on the photo's own Wikimedia Commons page. The wide OSGEMEOS mural is shown whole on an oatmilk mount, so no part of the work is cut off. The portfolios build and hold at phone and desktop width.
Needs you: these photos come from the web, not the inbox, and each shows the artist's work, so they wait for your yes. Nothing usable was found for KAWS or Eko Nugroho.

## Monday 23 November 2026, museum shows and prizes (draft)
Published: nothing. Prepared as a draft under the owner's standing rule for artist research.
Drafts waiting: museum shows, collections and prizes added to eleven portfolios (link in the pull request list).
Checked: Tate press releases (El Anatsui, Richter, Street Art 2008), Tate Modern's Kusama page, the Praemium Imperiale site, The Art Newspaper (Raza at the Pompidou, Love Is in the Bin), MASP, Artdaily, the Brooklyn Museum, MAAT, Euronews, the Biennial Foundation and Wikipedia for honours. 15 new numbered sources. The site builds with 14 artists; touched portfolios hold at phone and desktop width with no page errors.
Needs you: a yes or no on the draft. Nothing new was found for Zara Muse, Konn Artiss or Zen Xander.

## Monday 23 November 2026, portfolio images (draft)
Published: nothing. Prepared as a draft on the owner's request in a conversation to add images to the sites.
Drafts waiting: main images for the Banksy, Yayoi Kusama, El Anatsui, S.H. Raza and Gerhard Richter portfolios (link in the pull request list).
Checked: every image comes from Wikimedia Commons under a licence that allows reuse, read on the file's own page. Each carries the photographer and licence as its credit, and the full caption with the Commons link is in `content/files.json`. Kusama, Raza and Richter are portraits; Banksy is his 2026 Waterloo Place statue; El Anatsui is a public sculpture from his design in Nsukka, as no free portrait exists. The site builds with 9 artists and the pages hold at phone and desktop width.
Needs you: (1) this site's brief says images come only from the inbox, so these wait for your yes. (2) On phones the credit line on a main image is cut short by the name label, as it already is for Konn Artiss. Free licences ask for the credit to be readable, so tell me if you want that fixed. (3) No usable image was found for Beatriz Milhazes; her portfolio keeps the "Artwork image to supply" frame.

## Monday 23 November 2026, whole site brought up to date (published)
Published: on the owner's yes in a conversation. A new article introducing the eleven new artists, now first on the homepage. Five explainers and collecting guides use the new artists as sourced examples. The research desk lists all fourteen artists A to Z. Privacy and terms text written to match what the site actually does. https://github.com/Artiscope/World-art-review/pull/6
Drafts waiting: images for five portfolios. https://github.com/Artiscope/World-art-review/pull/5
Checked: the site builds with 14 artists and 17 articles; touched pages hold at phone and desktop width; every citation resolves. No long dashes or banned words.
Needs you: the "Our relationships" wording, and the footer's Instagram, X and LinkedIn addresses. Please also read the new privacy and terms text and check it suits you legally.

## Monday 23 November 2026, five street artist portfolios (draft)
Published: nothing. Prepared as a draft under the owner's standing rule for artist research.
Drafts waiting: portfolios for OSGEMEOS, Vhils, KAWS, Eko Nugroho and Faith XLVII, on branch draft/2026-11-23-street-artists.
Checked: the site builds with 14 artists; the new portfolios hold at phone and desktop width with no page errors. No long dashes or banned words. Sources: Artsy, Hyperallergic, Hookedblog, the Singapore Art Museum, the artist's own site for Vhils (marked as reported), and lot pages at Christie's, Phillips, Bonhams, Artcurial and Strauss & Co.
Needs you: a yes or no on the draft, and photographs with permission to publish.

## Monday 23 November 2026, five international portfolios (draft)
Published: nothing. Prepared as a draft on the owner's instruction in a conversation.
Drafts waiting: portfolios for Yayoi Kusama, El Anatsui, Beatriz Milhazes, S.H. Raza and Gerhard Richter. https://github.com/Artiscope/World-art-review/pull/3
Checked: the site builds with 9 artists, and the Raza portfolio holds at phone width. No long dashes or banned words. Sources: Wikipedia for biographies, plus auction lot pages (Sotheby's, Phillips, Saffronart, AstaGuru) and press reports (The Art Newspaper, TheValue, HENI News, Artsy).
Needs you: a yes or no on the draft, and photographs with permission to publish, if you want pictures on these portfolios.

## Thursday 19 November 2026
Published: fuller picture descriptions for people who cannot see the images. The Konn Artiss picture on his portfolio was described only as "Konn Artiss", and the picture on "Understanding palette-knife painting" as "Looking close on the strokes". Both now say what the picture shows. Nothing visible on the page changed.
Drafts waiting: none.
Checked: the site builds and the pages hold at phone and desktop width. No long dashes, US spellings or banned words. No photos in the inbox. Searched for news on Zara Muse, Konn Artiss and Zen Xander and read FAD Magazine, Art Plugged, Tate Ward and Roseberys: nothing new since 11 November. I could not open every source link from here this time, so the full link check is carried over. Monday's run was missed, so the first topic idea is added today: a first Zen Xander portfolio.
Needs you: (1) A yes or no on the Zen Xander idea in the content calendar. (2) The Konn Artiss picture is now a collage work, but its caption still reads "ANTI-FRIEZE, London, October 2025. Courtesy Konn Artiss". Please send the right title and credit. (3) Still open from 11 November: the "Our relationships" wording that tells readers Artiscope sells these artists' work, the privacy and terms text, and the footer's Instagram, X and LinkedIn links, which lead nowhere.

## Wednesday 11 November 2026, after your merge
Published: the Zara Muse image, with the caption "Image: painting by Zara Muse. Supplied by Grove Gallery". You merged the draft at 15:39. It shows on the homepage, Artists A to Z and her portfolio. https://github.com/Artiscope/World-art-review/pull/1
Drafts waiting: none.
Checked: the publishing run finished without errors and the site loads. The photo has left `inbox/`. I could not view the picture itself on the live site from here, so please glance at the homepage.
Needs you: the painting's title and year for the caption, if you want them shown. Points 2 and 3 below still stand.

## Wednesday 11 November 2026, first weekday run
Published: one link fix. Source "Zara Muse: The Art of Healing, the Power of Becoming" (Art Plugged) pointed to an address that now opens a different article, about Zen Xander. It now points to the right page: https://artplugged.co.uk/artist-zara-muse-art-healing-power-becoming/
Drafts waiting: Place the Zara Muse image from the inbox, with a corrected caption. https://github.com/Artiscope/World-art-review/pull/1
Checked: every page loads at phone and desktop width. No long dashes, US spellings, banned words or dividing lines found. All 20 source links opened: 19 work and match, and the Grove Gallery Chiswick site refuses automated visits so could not be checked. Searched for news on Zara Muse, Konn Artiss and Zen Xander: nothing new for this site. Content calendar: no answers to act on, new ideas come Monday.
Needs you: (1) `zara-muse-portrait.jpg` is a painting, not a photo of the artist, and its spot was captioned "the artist in the studio". It is held as a draft so you can confirm the painting is by Zara Muse and give its title. The file stays in `inbox/` until you merge. (2) The "Our relationships" section on the Editorial standards page still shows placeholder text, so readers are not yet told that the site is published by Artiscope, which sells these artists' work. Please send the wording. (3) Privacy and terms are also placeholders, and the Instagram, X and LinkedIn links in the footer lead nowhere. Send the addresses or tell me to draft their removal.

## Wednesday 11 November 2026
Also added: the voice guide (`VOICE.md`) and the content calendar (`CONTENT-CALENDAR.md`). First topic ideas arrive Monday 16 November.
Published: the agent's instructions (`CLAUDE.md`), this log and the `inbox/` folder for photos. Nothing on the site itself changed.
Drafts waiting: none.
Checked: nothing yet. The first weekday run does the first full check.
Needs you: photos, when you have them. Upload them to the `inbox/` folder.
