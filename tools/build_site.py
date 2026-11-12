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
                 "text", "text-picture", "picture", "quote", "articles", "faq", "button"}
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
    seen = set()
    for sec in home["sections"]:
        if not isinstance(sec, dict) or sec.get("type") not in SECTION_TYPES:
            sys.exit("The home page has a section of a kind the site cannot draw: %r" % (sec.get("type") if isinstance(sec, dict) else sec,))
        sid = str(sec.get("id") or "")
        if not sid or not all(c.isalnum() or c in "-_" for c in sid) or sid in seen:
            sys.exit("Every home page section needs its own id of letters, digits and hyphens: %r" % sid)
        seen.add(sid)
        if not isinstance(sec.get("settings", {}), dict):
            sys.exit("The settings of section '%s' must be a list of fields." % sid)


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
        "const PAGES = " + js(pages) + ";",
    ])
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        page = template.replace(MARK, block)
        theme = theme_head(os.path.join(ROOT, "content", "theme.json"))
        if theme:
            if page.count("</head>") != 1:
                sys.exit("The layout file must contain one </head>.")
            page = page.replace("</head>", theme + "</head>")
        f.write(page)
    print(f"Built index.html with {len(artists)} artists and {len(articles)} articles.")


if __name__ == "__main__":
    main()
