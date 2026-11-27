#!/usr/bin/env python3
"""Builds World Art Review from its three parts.

  content/site.json   the words and pictures (edited in Artiscope Digital Home)
  content/theme.json  the colours and typefaces (edited in Artiscope Digital Home)
  content/pages.json  the sections of each page, in order (edited in Artiscope Digital Home)
  src/index.html      the design and layout
  -> index.html       the finished page, written to the folder you name

Run:  python3 tools/build_site.py [output folder]
An entry with "hidden": true is left out of the finished page.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "/*@@CONTENT@@*/"
SECTION_TYPES = {"hero", "featured", "section-list", "explained", "numbers", "method",
                 "text", "text-picture", "picture", "quote", "articles", "faq", "button",
                 "page-heading", "long-text", "announcement", "columns", "space",
                 "picture-banner", "slideshow", "gallery", "logo-row",
                 "artworks", "exhibitions", "career", "press", "artist-cards",
                 "signup", "visit", "contact-form", "signup-popup"}
SHARED_TYPES = {"opening", "header", "footer"}


def check_pages(pages):
    """Refuses to build if the page list would not draw, so a bad edit
    cannot blank the site."""
    for key, part in (pages.get("shared") or {}).items():
        if not isinstance(part, dict) or part.get("type") not in SHARED_TYPES or not isinstance(part.get("settings"), dict):
            sys.exit("The shared part '%s' in content/pages.json is not something the site can draw." % key)
    for key in ("opening", "header", "footer"):
        if key not in (pages.get("shared") or {}):
            sys.exit("content/pages.json must have the shared part '%s'." % key)
    home = (pages.get("pages") or {}).get("home")
    if not home or not isinstance(home.get("sections"), list):
        sys.exit("content/pages.json must have a home page with a list of sections.")
    for key, page in (pages.get("pages") or {}).items():
        if not isinstance(page, dict) or not isinstance(page.get("sections"), list):
            sys.exit("The page '%s' in content/pages.json needs a list of sections." % key)
        seen = set()
        for sec in page["sections"]:
            if not isinstance(sec, dict) or sec.get("type") not in SECTION_TYPES:
                sys.exit("The page '%s' has a section of a kind the site cannot draw: %r" % (key, sec.get("type") if isinstance(sec, dict) else sec))
            sid = str(sec.get("id") or "")
            if not sid or not all(c.isalnum() or c in "-_" for c in sid) or sid in seen:
                sys.exit("Every section on the page '%s' needs its own id of letters, digits and hyphens: %r" % (key, sid))
            seen.add(sid)
            if not isinstance(sec.get("settings", {}), dict):
                sys.exit("The settings of section '%s' must be a list of fields." % sid)
    groups = pages.get("groups") or {}
    if not isinstance(groups, dict):
        sys.exit("The shared sections in content/pages.json must be a top and a bottom list.")
    gseen = set()
    for where in ("top", "popups", "bottom"):
        for sec in groups.get(where) or []:
            if not isinstance(sec, dict) or sec.get("type") not in SECTION_TYPES:
                sys.exit("A section shared by every page is of a kind the site cannot draw: %r" % (sec.get("type") if isinstance(sec, dict) else sec))
            sid = str(sec.get("id") or "")
            if not sid.startswith("every-") or sid in gseen:
                sys.exit("Every shared section needs its own id starting every-: %r" % sid)
            gseen.add(sid)
    # templates: the sections article and artist pages are drawn with, around their own content ("main")
    templates = pages.get("templates") or {}
    if not isinstance(templates, dict):
        sys.exit("The templates in content/pages.json must be grouped by kind of page.")
    for kind, tpls in templates.items():
        if kind not in ("article", "artist") or not isinstance(tpls, dict) or "default" not in tpls:
            sys.exit("Templates are for articles and artists, and each kind needs a default: %r" % kind)
        for tid, t in tpls.items():
            secs = t.get("sections") if isinstance(t, dict) else None
            if not isinstance(secs, list) or sum(1 for x in secs if isinstance(x, dict) and x.get("type") == "main") != 1:
                sys.exit("The template '%s' needs a list of sections with the page's own content in it once." % tid)
            for sec in secs:
                if not isinstance(sec, dict) or (sec.get("type") != "main" and sec.get("type") not in SECTION_TYPES):
                    sys.exit("The template '%s' has a section of a kind the site cannot draw." % tid)
                if sec.get("type") != "main" and not str(sec.get("id") or "").startswith("t-"):
                    sys.exit("Every section in a template needs its own id starting t-: %r" % sec.get("id"))
    if not isinstance(pages.get("assign", {}), dict):
        sys.exit("The templates chosen for articles and artists must be listed by kind.")
    if not isinstance(pages.get("lists", {}), dict):
        sys.exit("The list headings in content/pages.json must be a list of fields.")
    # changed fixed words, from Edit default text: plain words only
    words = pages.get("words", {})
    if not isinstance(words, dict) or any(not isinstance(v, str) for v in words.values()):
        sys.exit("The changed words in content/pages.json must be a list of plain words.")


def visible(items):
    return [x for x in items if not (isinstance(x, dict) and x.get("hidden") is True)]


def js(value):
    # Valid JavaScript, and safe to sit inside a <script> block.
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def theme_head(path):
    """The colours and typefaces chosen in Artiscope Digital Home, as a small
    block for the page head. Empty when the theme is the original one."""
    if not os.path.exists(path):
        return ""
    theme = json.load(open(path, encoding="utf-8"))
    out = ""
    for link in theme.get("font_links") or []:
        if isinstance(link, str) and link.startswith("https://fonts.googleapis.com/css2?") and not re.search(r'["<>\s]', link):
            out += '<link href="%s" rel="stylesheet">\n' % link.replace("&", "&amp;")
    css = theme.get("css") or ""
    if css and re.fullmatch(r":root\{[^<>{}]*\}", css):
        out += '<style id="theme">%s</style>\n' % css
    rules = theme.get("rules") or ""
    if isinstance(rules, str) and rules.strip() and "<" not in rules:
        out += '<style id="theme-rules">\n%s\n</style>\n' % rules
    icon = theme.get("favicon") or ""
    if isinstance(icon, str) and re.fullmatch(r"images/[A-Za-z0-9._-]{1,120}\.(png|jpe?g|svg|ico)", icon):
        out += '<link rel="icon" href="%s">\n' % icon
    return out


def theme_social(path):
    """The social media addresses chosen in the theme, for the footer and the menu."""
    if not os.path.exists(path):
        return {}
    theme = json.load(open(path, encoding="utf-8"))
    out = {}
    for k, v in (theme.get("social") or {}).items():
        if isinstance(v, dict) and isinstance(v.get("href"), str) and re.fullmatch(r"https://[^\s<>\"'`]+", v["href"]) and isinstance(v.get("label"), str):
            out[k] = {"label": v["label"][:20], "href": v["href"]}
    return out


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else ROOT
    data = json.load(open(os.path.join(ROOT, "content", "site.json"), encoding="utf-8"))
    pages = json.load(open(os.path.join(ROOT, "content", "pages.json"), encoding="utf-8"))
    check_pages(pages)
    template = open(os.path.join(ROOT, "src", "index.html"), encoding="utf-8").read()
    if template.count(MARK) != 1:
        sys.exit("The layout file must contain the content marker exactly once.")

    articles = visible(data["articles"])
    artists = []
    for a in data["artists"]:
        a = dict(a)
        if isinstance(a.get("works"), list):
            a["works"] = visible(a["works"])
        artists.append(a)

    block = "\n".join([
        "const SOURCES = " + js(data["sources"]) + ";",
        "const ARTISTS = " + js(artists) + ";",
        "const ARTICLES = " + js(articles) + ";",
        "const GUIDES = " + js(data["guides"]) + ";",
        "const QUIZ = " + js(data.get("quiz") or {"rounds": []}) + ";",
        "const PAGES = " + js(pages) + ";",
        "let SOCIAL = " + js(theme_social(os.path.join(ROOT, "content", "theme.json"))) + ";",
    ])
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        page = template.replace(MARK, block)
        theme = theme_head(os.path.join(ROOT, "content", "theme.json"))
        if 'rel="icon" href="images/' in theme:
            page = re.sub(r'<link rel="icon"[^>]*>\n?', "", page)
        if theme:
            if page.count("</head>") != 1:
                sys.exit("The layout file must contain one </head>.")
            page = page.replace("</head>", theme + "</head>")
        f.write(page)
    n = write_search_pages(out_dir, page, artists, articles, pages, data)
    print(f"Built index.html with {len(artists)} artists and {len(articles)} articles, and {n} pages of their own for search engines.")


# ----- pages of their own, so search engines can find each piece -----
# The site is one page that shows each portfolio and article behind a #link.
# Search engines treat #links as one address, so each published portfolio and
# article also gets its own address (artists/<slug>/ and articles/<slug>/).
# Each is the same page, opening straight on that piece, with its own title,
# description and structured data. A small script turns the #links on every
# page into these addresses. robots.txt and sitemap.xml list them all.
SITE_NAME = "World Art Review"
# Who may read the site. Everyone is welcome; the search engines and the AI search tools that
# link back to their sources are also named, so there is no doubt they are allowed in.
ROBOTS = ("User-agent: *\nAllow: /\n\nUser-agent: Googlebot\nUser-agent: Bingbot\nUser-agent: OAI-SearchBot\nUser-agent: ChatGPT-User\n"
          "User-agent: PerplexityBot\nUser-agent: Perplexity-User\nUser-agent: Claude-SearchBot\nUser-agent: Claude-User\n"
          "User-agent: Applebot\nUser-agent: DuckDuckBot\nAllow: /\n")


def site_url():
    try:
        host = open(os.path.join(ROOT, "CNAME"), encoding="utf-8").read().strip()
    except OSError:
        host = ""
    return "https://%s/" % host if host else "https://worldartreview.com/"


def attr(text):
    return (str(text).replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def plain(html, limit=155):
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(html or ""))).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit - 1].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "…"


def title_for(name):
    # Short enough not to be cut off in search results; the site name is added when it fits.
    full = "%s | %s" % (name, SITE_NAME)
    return full if len(full) <= 60 else name


def ld_json(data):
    return '<script type="application/ld+json">%s</script>\n' % json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


# Each page is the same one-page site, opening on its own piece. A small line at the top
# tells the page how many folders down it sits, so pictures and links are found from the top.
def depth_line(depth):
    return "<script>window.WAR_DEPTH=%d;</script>\n" % depth

# list pages and pages made in the console that get a plain address of their own
LIST_PAGES = {
    "artists": "Artists A to Z", "reviews": "Reviews", "explained": "Art Explained",
    "library": "Collector's Library", "guides": "Exhibition Guides", "play": "Whose Style Is It? An Art Quiz",
    "standards": "How we research", "research": "Research desk", "search": "Search",
}
# kept out of search results: a working list and an empty search page
NOINDEX = {"research", "search"}


def with_head(page, title, desc, canonical, extra, image=None, kind="website"):
    page = re.sub(r"<title>[^<]*</title>", lambda m: "<title>%s</title>" % attr(title), page, count=1)
    page = re.sub(r'<meta name="description" content="[^"]*">', lambda m: '<meta name="description" content="%s">' % attr(desc), page, count=1)
    head = ('<link rel="canonical" href="%s">\n<meta property="og:type" content="%s">\n<meta property="og:site_name" content="%s">\n'
            '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n'
            % (attr(canonical), kind, SITE_NAME, attr(title), attr(desc), attr(canonical)))
    if image:
        head += '<meta property="og:image" content="%s">\n<meta name="twitter:card" content="summary_large_image">\n' % attr(image)
    head += extra
    return page.replace("</head>", head + "</head>", 1)


# ----- a reading copy in the page itself -----
# The site draws each piece with JavaScript. Search engines that run it see the finished page,
# but many AI search tools (ChatGPT search, Perplexity and others) read only the page as sent.
# So each page also carries its piece as plain HTML inside <main>. The script replaces it with
# the designed page as soon as it runs, and a line in the <head> hides it until then, so
# visitors never see it. The words are the same ones the designed page shows.
CITE = re.compile(r'<sup class="cite">\s*<a data-src="([^"]+)">[^<]*</a>\s*</sup>')
HIDE_STATIC = ('<script>document.documentElement.className+=" js";</script>\n'
               '<style>.js .war-static{display:none}</style>\n')


def esc(text):
    return (str(text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def cited(html, order):
    """Turns the site's citation marks into plain numbered notes, counting each source once."""
    def num(m):
        key = m.group(1)
        if key not in order:
            order.append(key)
        return "<sup>[%d]</sup>" % (order.index(key) + 1)
    return CITE.sub(num, str(html or ""))


def source_list(order, sources):
    items = []
    for key in order:
        src = sources.get(key) or {}
        label = ", ".join(x for x in (src.get("title"), src.get("pub")) if x) or key
        url = src.get("url") or ""
        items.append('<li><a href="%s" rel="noopener">%s</a></li>' % (attr(url), esc(label)) if url.startswith("http") else "<li>%s</li>" % esc(label))
    return ("<h2>Sources</h2>\n<ol>\n%s\n</ol>\n" % "\n".join(items)) if items else ""


def static_artist(a, articles, sources, url):
    order = []
    out = ['<article class="war-static">', "<h1>%s</h1>" % esc(a["name"])]
    if a.get("dek"):
        out.append("<p>%s</p>" % esc(a["dek"]))
    if a.get("summary"):
        out.append("<p>%s</p>" % esc(a["summary"]))
    glance = [g for g in (a.get("glance") or []) if isinstance(g, list) and len(g) >= 2]
    if glance:
        out.append("<h2>At a glance</h2>\n<dl>")
        for g in glance:
            notes = "".join(cited('<sup class="cite"><a data-src="%s">[x]</a></sup>' % k, order) for k in (g[2] if len(g) > 2 else []))
            out.append("<dt>%s</dt><dd>%s%s</dd>" % (esc(g[0]), esc(g[1]), notes))
        out.append("</dl>")
    for sec in a.get("sections") or []:
        out.append("<h2>%s</h2>\n%s" % (esc(sec.get("title")), cited(sec.get("html"), order)))
    works = a.get("works") or []
    if works:
        out.append("<h2>Works</h2>\n<ul>")
        for w in works:
            bits = [x for x in (w.get("year"), w.get("medium"), w.get("size")) if isinstance(x, str) and x]
            notes = "".join(cited('<sup class="cite"><a data-src="%s">[x]</a></sup>' % k, order) for k in (w.get("src") or []))
            out.append("<li><i>%s</i>%s%s%s</li>" % (esc(w.get("title")), (", " + esc(", ".join(bits))) if bits else "",
                                                       (". " + esc(w.get("note"))) if w.get("note") else "", notes))
        out.append("</ul>")
    about = [x for x in articles if a["slug"] in (x.get("artists") or [])]
    if about:
        out.append("<h2>More on %s</h2>\n<ul>" % esc(a["name"]))
        out += ['<li><a href="%sarticles/%s/">%s</a></li>' % (url, x["slug"], esc(x.get("title"))) for x in about]
        out.append("</ul>")
    out.append(source_list(order, sources))
    out.append('<p><a href="%sartists/">All artists, A to Z</a></p>\n</article>' % url)
    return "\n".join(out)


def static_article(x, live_artists, sources, url):
    order = []
    out = ['<article class="war-static">', "<h1>%s</h1>" % esc(x.get("title"))]
    if x.get("dek"):
        out.append("<p>%s</p>" % esc(x["dek"]))
    out.append(cited(x.get("body"), order))
    named = [a for s in (x.get("artists") or []) for a in live_artists if a["slug"] == s]
    if named:
        out.append("<h2>Artists in this piece</h2>\n<ul>")
        out += ['<li><a href="%sartists/%s/">%s</a></li>' % (url, a["slug"], esc(a["name"])) for a in named]
        out.append("</ul>")
    # sources listed on the piece but not cited in the text still belong in the list
    for key in x.get("sources") or []:
        if key not in order:
            order.append(key)
    out.append(source_list(order, sources))
    out.append("</article>")
    return "\n".join(out)


def static_list(title, intro, links):
    out = ['<section class="war-static">', "<h1>%s</h1>" % esc(title)]
    if intro:
        out.append("<p>%s</p>" % esc(plain(intro, 600)))
    out.append("<ul>")
    out += ['<li><a href="%s">%s</a>%s</li>' % (attr(h), esc(t), (": " + esc(d)) if d else "") for h, t, d in links]
    out.append("</ul>\n</section>")
    return "\n".join(out)


def with_static(page, html):
    marker = '<main id="main" tabindex="-1" style="outline:none"></main>'
    if page.count(marker) != 1:
        return page
    page = page.replace(marker, marker[:-len("</main>")] + "\n" + html + "\n</main>", 1)
    return page.replace("</head>", HIDE_STATIC + "</head>", 1)


def write_search_pages(out_dir, page, artists, articles, pages, data=None):
    url = site_url()
    publisher = {"@type": "Organization", "name": "Artiscope", "url": "https://grovegallery.com/"}
    img = lambda p: url + p if isinstance(p, str) and p.startswith("images/") else None
    live_artists = [a for a in artists if a.get("published") is True]
    if page.count("</head>") != 1 or page.count("</body>") != 1:
        sys.exit("The layout file must contain one </head> and one </body>.")

    home_ld = ld_json({"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": url,
                       "description": "Researched artist portfolios, artwork reviews, collecting guides and techniques explained.",
                       "publisher": publisher})
    m = re.search(r'<meta name="description" content="([^"]*)">', page)
    home = with_head(page, SITE_NAME, m.group(1) if m else "", url, home_ld)
    site_data = data or {}
    sources = site_data.get("sources") or {}
    artist_links = [(url + "artists/%s/" % a["slug"], a["name"], plain(a.get("summary") or a.get("dek") or "", 200)) for a in live_artists]
    home_links = artist_links + [(url + "articles/%s/" % x["slug"], x.get("title") or "", plain(x.get("dek") or "", 200)) for x in articles if x.get("section") == "features"]
    home = with_static(home, static_list(SITE_NAME, m.group(1) if m else "", home_links))
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(home)

    addresses = [""]

    def write(folder, slug, hash_, title, desc, ld, image, kind, index=True, static=""):
        address = "%s/%s/" % (folder, slug) if folder else "%s/" % slug
        html = with_head(page, title, desc, url + address, ld, image, kind)
        if static:
            html = with_static(html, static)
        head = depth_line(address.count("/"))
        if not index:
            head += '<meta name="robots" content="noindex">\n'
        html = html.replace("<head>", "<head>\n" + head, 1)
        target = os.path.join(out_dir, folder, slug) if folder else os.path.join(out_dir, slug)
        os.makedirs(target, exist_ok=True)
        with open(os.path.join(target, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        if index:
            addresses.append(address)

    for a in live_artists:
        desc = plain(a.get("dek") or a.get("summary") or "")
        image = img(a.get("image"))
        here = url + "artists/%s/" % a["slug"]
        person = {"@type": "Person", "@id": here + "#artist", "name": a["name"], "url": here}
        if a.get("summary"):
            person["description"] = plain(a["summary"], 300)
        if image:
            person["image"] = image
        ld = ld_json({"@context": "https://schema.org", "@type": "ProfilePage", "name": a["name"] + ": artist portfolio",
                      "url": here, "description": desc, "mainEntity": person,
                      "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": url}, "publisher": publisher})
        # the works shown in the portfolio, each as an artwork by this artist
        for w in a.get("works") or []:
            if not w.get("title"):
                continue
            art = {"@context": "https://schema.org", "@type": "VisualArtwork", "name": plain(w["title"], 200),
                   "creator": {"@type": "Person", "@id": here + "#artist", "name": a["name"]}, "url": here}
            if re.fullmatch(r"\d{4}", str(w.get("year") or "")):
                art["dateCreated"] = w["year"]
            if isinstance(w.get("medium"), str) and w["medium"]:
                art["artMedium"] = w["medium"]
            ld += ld_json(art)
        write("artists", a["slug"], "artist-" + a["slug"], title_for(a["name"] + ": artist portfolio"), desc, ld, image, "profile",
              static=static_artist(a, articles, sources, url))

    for a in articles:
        desc = plain(a.get("dek") or a.get("body") or "")
        image = img(a.get("image"))
        data = {"@context": "https://schema.org", "@type": "Article", "headline": plain(a.get("title"), 110),
                "description": desc, "url": url + "articles/%s/" % a["slug"],
                "mainEntityOfPage": url + "articles/%s/" % a["slug"],
                "author": {"@type": "Organization", "name": SITE_NAME, "url": url}, "publisher": publisher,
                "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": url}}
        if image:
            data["image"] = image
        named = [x for s in (a.get("artists") or []) for x in live_artists if x["slug"] == s]
        if named:
            data["about"] = [{"@type": "Person", "name": x["name"], "url": url + "artists/%s/" % x["slug"]} for x in named]
        write("articles", a["slug"], "a-" + a["slug"], title_for(a.get("title") or SITE_NAME), desc, ld_json(data), image, "article",
              static=static_article(a, live_artists, sources, url))

    lists = pages.get("lists") or {}
    for key, name in LIST_PAGES.items():
        desc = plain((lists.get(key) or {}).get("intro") or "")
        if key == "standards":
            desc = "The rules every portfolio and article on World Art Review follows: sources, labels and corrections."
        if key == "play":
            desc = "A quick game: look at a close detail of a work and pick the artist who made it."
        ld = ld_json({"@context": "https://schema.org", "@type": "CollectionPage" if key not in ("play", "standards") else "WebPage",
                      "name": name, "url": url + key + "/", "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": url},
                      "publisher": publisher})
        links = []
        if key == "artists":
            links = artist_links
        elif key in ("reviews", "explained", "library"):
            links = [(url + "articles/%s/" % x["slug"], x.get("title") or "", plain(x.get("dek") or "", 200)) for x in articles if x.get("section") == key]
        elif key == "guides":
            links = [(g["url"], g.get("title") or "", ", ".join(v for v in (g.get("venue"), g.get("dates")) if v))
                     for g in (site_data.get("guides") or []) if isinstance(g.get("url"), str) and g["url"].startswith("http")]
        write("", key, key, title_for(name), desc or name, ld, None, "website", key not in NOINDEX,
              static=static_list(name, desc, links) if links else "")
    for key, pg in (pages.get("pages") or {}).items():
        if key in ("home",) or key in LIST_PAGES or not re.fullmatch(r"[a-z0-9-]+", key):
            continue
        name = pg.get("title") or key.capitalize()
        ld = ld_json({"@context": "https://schema.org", "@type": "WebPage", "name": name, "url": url + key + "/",
                      "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": url}, "publisher": publisher})
        write("", key, "page-" + key, title_for(name), "%s, World Art Review." % name, ld, None, "website")

    # The page GitHub Pages sends for an address that does not exist. It can be shown at any depth,
    # so pictures and links start from the top, and it is kept out of search results.
    missing = re.sub(r"<title>[^<]*</title>", "<title>Page not found | %s</title>" % SITE_NAME, page, count=1)
    missing = missing.replace("<head>", "<head>\n<meta name=\"robots\" content=\"noindex\">\n"
                              "<script>window.WAR_BASE=\"/\";</script>\n", 1)
    with open(os.path.join(out_dir, "404.html"), "w", encoding="utf-8") as f:
        f.write(missing)

    with open(os.path.join(out_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for address in addresses:
            f.write("<url><loc>%s%s</loc></url>\n" % (url, address))
        f.write("</urlset>\n")
    with open(os.path.join(out_dir, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(ROBOTS + "\nSitemap: %ssitemap.xml\n" % url)
    # llms.txt: a plain guide to the site for AI search tools, built from the same content as the pages
    lines = ["# " + SITE_NAME, "", "> " + plain(m.group(1) if m else "", 400), "",
             "Every portfolio and article lists its sources, and claims that come only from publicity are labelled as reported.", "", "## Artist portfolios", ""]
    lines += ["- [%s](%s): %s" % (n, h, d) if d else "- [%s](%s)" % (n, h) for h, n, d in artist_links]
    for key, heading in (("features", "Features"), ("reviews", "Reviews"), ("explained", "Art Explained"), ("library", "Collector's Library")):
        items = [x for x in articles if x.get("section") == key]
        if items:
            lines += ["", "## " + heading, ""]
            lines += ["- [%s](%sarticles/%s/): %s" % (x.get("title"), url, x["slug"], plain(x.get("dek") or "", 300)) for x in items]
    with open(os.path.join(out_dir, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(addresses) - 1


if __name__ == "__main__":
    main()
