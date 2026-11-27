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
    n = write_search_pages(out_dir, page, artists, articles)
    print(f"Built index.html with {len(artists)} artists and {len(articles)} articles, and {n} pages of their own for search engines.")


# ----- pages of their own, so search engines can find each piece -----
# The site is one page that shows each portfolio and article behind a #link.
# Search engines treat #links as one address, so each published portfolio and
# article also gets its own address (artists/<slug>/ and articles/<slug>/).
# Each is the same page, opening straight on that piece, with its own title,
# description and structured data. A small script turns the #links on every
# page into these addresses. robots.txt and sitemap.xml list them all.
SITE_NAME = "World Art Review"


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


LINKS_SCRIPT = """<script>/* turns #links to portfolios and articles into their own addresses */
(function(){var root=%s;function fix(n){var as=n.querySelectorAll?n.querySelectorAll('a[href^="#a-"],a[href^="#artist-"]'):[];for(var i=0;i<as.length;i++){var h=as[i].getAttribute('href');var m=/^#(a|artist)-([a-z0-9-]+)$/.exec(h);if(!m)continue;if(m[1]==='artist'&&ARTISTS.every(function(x){return x.slug!==m[2]||!x.published;}))continue;if(m[1]==='a'&&ARTICLES.every(function(x){return x.slug!==m[2];}))continue;as[i].setAttribute('href',root+(m[1]==='a'?'articles/':'artists/')+m[2]+'/');}}
fix(document);new MutationObserver(function(rs){rs.forEach(function(r){r.addedNodes.forEach(function(n){if(n.nodeType===1)fix(n.parentNode||n);});});}).observe(document.body,{childList:true,subtree:true});})();
</script>
"""


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


def write_search_pages(out_dir, page, artists, articles):
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
    home = home.replace("</body>", LINKS_SCRIPT % '""' + "</body>", 1)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(home)

    # one folder down two levels: pictures and the page's own links are found from the top
    deep = (page.replace('"images/', '"../../images/').replace("'images/'", "'../../images/'")
                .replace('href="images/', 'href="../../images/'))
    deep = deep.replace("</body>", LINKS_SCRIPT % '"../../"' + "</body>", 1)
    addresses = [""]

    def write(folder, slug, hash_, title, desc, ld, image, kind):
        address = "%s/%s/" % (folder, slug)
        boot = ("<script>if(!location.hash)history.replaceState(null,'',location.pathname+location.search+'#%s');</script>\n" % hash_)
        html = with_head(deep, title, desc, url + address, ld, image, kind)
        html = html.replace("<head>", "<head>\n" + boot, 1)
        target = os.path.join(out_dir, folder, slug)
        os.makedirs(target, exist_ok=True)
        with open(os.path.join(target, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        addresses.append(address)

    for a in live_artists:
        desc = plain(a.get("dek") or a.get("summary") or "")
        image = img(a.get("image"))
        person = {"@type": "Person", "name": a["name"]}
        if image:
            person["image"] = image
        ld = ld_json({"@context": "https://schema.org", "@type": "ProfilePage", "name": a["name"] + ": artist portfolio",
                      "url": url + "artists/%s/" % a["slug"], "description": desc, "mainEntity": person,
                      "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": url}, "publisher": publisher})
        write("artists", a["slug"], "artist-" + a["slug"], title_for(a["name"] + ": artist portfolio"), desc, ld, image, "profile")

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
        names = [x["name"] for s in (a.get("artists") or []) for x in live_artists if x["slug"] == s]
        if names:
            data["about"] = [{"@type": "Person", "name": n} for n in names]
        write("articles", a["slug"], "a-" + a["slug"], title_for(a.get("title") or SITE_NAME), desc, ld_json(data), image, "article")

    # The page GitHub Pages sends for an address that does not exist. It can be shown at any depth,
    # so pictures and links start from the top, and it is kept out of search results.
    missing = (page.replace('"images/', '"/images/').replace("'images/'", "'/images/'")
                   .replace('href="images/', 'href="/images/'))
    missing = missing.replace("</body>", LINKS_SCRIPT % '"/"' + "</body>", 1)
    missing = re.sub(r"<title>[^<]*</title>", "<title>Page not found | %s</title>" % SITE_NAME, missing, count=1)
    missing = missing.replace("<head>", "<head>\n<meta name=\"robots\" content=\"noindex\">\n"
                              "<script>if(!location.hash)history.replaceState(null,'',location.pathname+location.search+'#not-found');</script>\n", 1)
    with open(os.path.join(out_dir, "404.html"), "w", encoding="utf-8") as f:
        f.write(missing)

    with open(os.path.join(out_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for address in addresses:
            f.write("<url><loc>%s%s</loc></url>\n" % (url, address))
        f.write("</urlset>\n")
    with open(os.path.join(out_dir, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % url)
    return len(addresses) - 1


if __name__ == "__main__":
    main()
