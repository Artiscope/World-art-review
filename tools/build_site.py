#!/usr/bin/env python3
"""Builds World Art Review from its three parts.

  content/site.json   the words and pictures (edited in Artiscope Digital Home)
  content/theme.json  the colours and typefaces (edited in Artiscope Digital Home)
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
