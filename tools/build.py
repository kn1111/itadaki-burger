"""サイトを生成する: 各言語の index.html / sitemap.xml / 見出しフォントのサブセット。

  python tools/build.py

文言は tools/content.py。画像は tools/import_assets.py で取り込み済みの assets/ を参照する。
フォントの元ファイルはゲームのリポジトリから読む (環境変数 BURGER、既定 C:/Users/knoza/burger)。
"""
import html
import json
import os
import re
import string
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import ALL_NAMES, LANG_NAMES, LANGS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://kn1111.github.io/itadaki-burger/"
APP = "5161560"
BURGER = os.environ.get("BURGER", "C:/Users/knoza/burger")
MAIL = "nozworks2027@gmail.com"
LASTMOD = "2026-09-14"

# 見出しフォントの系統 → (元ファイル, 出力名, 書き出す形式)
FONTS = {
    "mplus": (BURGER + "/assets/fonts/pixelmplus/PixelMplus12-Regular.ttf", "pixelmplus12-subset", ("woff2", "woff")),
    "sc": (BURGER + "/assets/fonts/fusion-pixel/fusion-pixel-12px-proportional-zh_hans.woff2", "fusion-sc-subset", ("woff2",)),
    "tc": (BURGER + "/assets/fonts/fusion-pixel/fusion-pixel-12px-proportional-zh_hant.woff2", "fusion-tc-subset", ("woff2",)),
    "ko": (BURGER + "/assets/fonts/fusion-pixel/fusion-pixel-12px-proportional-ko.woff2", "fusion-ko-subset", ("woff2",)),
}


def a(s):
    """属性値用のエスケープ (content の値はプレーンテキスト)。"""
    return html.escape(s, quote=True)


def rel(frm, to):
    """frm のページから to のページへの相対リンク。ディレクトリは 1 段だけ。"""
    r = "../" if frm["dir"] else ""
    return (r + to["dir"]) or "./"


def languages_row(L):
    names = [n for code, n in LANG_NAMES]
    mine = [n for code, n in LANG_NAMES if code == L["hreflang"]]
    return " / ".join(mine + [n for n in names if n not in mine])


def render(L):
    r = "../" if L["dir"] else ""
    url = BASE + L["dir"]
    store = "https://store.steampowered.com/app/%s/?l=%s" % (APP, L["steam"])
    og_image = BASE + "assets/og-%s.png" % L["ss"]
    en = next(x for x in LANGS if x["hreflang"] == "en")

    alternates = "".join('<link rel="alternate" hreflang="%s" href="%s">\n' % (x["hreflang"], BASE + x["dir"]) for x in LANGS)
    alternates += '<link rel="alternate" hreflang="x-default" href="%s">\n' % (BASE + en["dir"])
    og_alt = "".join('<meta property="og:locale:alternate" content="%s">\n' % x["og_locale"] for x in LANGS if x is not L)

    ld = {
        "@context": "https://schema.org",
        "@type": "VideoGame",
        "name": L["name"],
        "alternateName": [n for n in ALL_NAMES if n != L["name"]],
        "url": url,
        "image": og_image,
        "description": L["ld_description"],
        "genre": L["genres"],
        "gamePlatform": "PC",
        "operatingSystem": L["os"],
        "applicationCategory": "Game",
        "inLanguage": [code for code, _ in LANG_NAMES],
        "author": {"@type": "Organization", "name": "NoZworks"},
        "publisher": {"@type": "Organization", "name": "NoZworks"},
        "sameAs": ["https://store.steampowered.com/app/%s/" % APP],
    }
    ld_json = json.dumps(ld, ensure_ascii=False, indent=2).replace("</", "<\\/")

    menu = []
    for x in LANGS:
        cur = ' aria-current="page"' if x is L else ""
        menu.append('<li><a href="%s" hreflang="%s" lang="%s"%s>%s</a></li>' % (rel(L, x), x["hreflang"], x["hreflang"], cur, x["menu"]))

    w, h = L["ss_size"]

    def shot_src(n):
        return "%sassets/ss/%s-%d.png" % (r, L["ss"], n)

    steps = []
    for n, title, text, alt in L["steps"]:
        steps.append(
            '        <div class="step">\n'
            '          <img class="shot px" src="%s" width="%d" height="%d" loading="lazy" alt="%s">\n'
            '          <div>\n'
            '            <span class="num">STEP %d</span>\n'
            '            <h3>%s</h3>\n'
            '            <p>%s</p>\n'
            '          </div>\n'
            '        </div>' % (shot_src(n), w, h, a(alt), len(steps) + 1, title, text))

    features = "\n".join('        <li><b>%s</b><span>%s</span></li>' % (b, s) for b, s in L["features"])
    shots = "\n".join(
        '        <a href="%s"><figure><img class="shot px" src="%s" width="%d" height="%d" loading="lazy" alt="%s"><figcaption>%s</figcaption></figure></a>'
        % (shot_src(n), shot_src(n), w, h, a(alt), cap) for n, cap, alt in L["shots"])
    facts = "\n".join(
        '        <dt>%s</dt><dd>%s</dd>' % (k, v if v is not None else languages_row(L)) for k, v in L["facts"])
    about = "\n".join("        <p>%s</p>" % p for p in L["about"])

    return f"""<!doctype html>
<html lang="{L['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(L['title'])}</title>
<meta name="description" content="{a(L['description'])}">
<link rel="canonical" href="{url}">
{alternates}<link rel="icon" type="image/png" sizes="32x32" href="{r}assets/icon-32.png">
<link rel="apple-touch-icon" href="{r}assets/icon-256.png">
<meta name="theme-color" content="#1d2333">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{a(L['name'])}">
<meta property="og:title" content="{a(L['og_title'])}">
<meta property="og:description" content="{a(L['og_description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="{L['og_locale']}">
{og_alt}<meta name="twitter:card" content="summary_large_image">

<script type="application/ld+json">
{ld_json}
</script>
<link rel="stylesheet" href="{r}style.css">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./"><img class="px" src="{r}assets/icon-32.png" alt="" width="28" height="28"><span class="brand-name">{L['name']}</span></a>
    <nav class="nav">
      <details class="langs">
        <summary aria-label="{a(L['lang_label'])}">{L['menu']}</summary>
        <ul>
          {chr(10).join('          ' + m for m in menu).strip()}
        </ul>
      </details>
      <a class="btn small" href="{store}">Steam</a>
    </nav>
  </div>
</header>

<main>
  <div class="hero">
    <div class="wrap">
      <h1>
        <img class="logo px" src="{r}assets/logo-{L['ss']}.png" alt="{a(L['name'])}">
      </h1>
      <p class="tagline">{L['tagline']}</p>
      <p class="alt-name">{L['subtitle']}</p>
      <a class="btn" href="{store}">{L['cta']}</a>
      <p class="release">{L['release']}</p>
    </div>
  </div>

  <section id="about">
    <div class="wrap">
      <h2>{L['about_h']}</h2>
      <div class="lead">
{about}
      </div>
      <!-- trailer: embed the YouTube video here once it is uploaded
      <div class="trailer"><iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID" title="{a(L['name'])}" allowfullscreen></iframe></div>
      -->
      <div class="steam-widget">
        <iframe src="https://store.steampowered.com/widget/{APP}/?l={L['steam']}" title="{a(L['name'])} (Steam)" loading="lazy"></iframe>
      </div>
    </div>
  </section>

  <section id="flow" class="alt">
    <div class="wrap">
      <h2>{L['flow_h']}</h2>
      <div class="steps">
{chr(10).join(steps)}
      </div>
    </div>
  </section>

  <section id="features">
    <div class="wrap">
      <h2>{L['feat_h']}</h2>
      <ul class="features">
{features}
      </ul>
      <div class="challenge">
        <h3>{L['challenge_h']}</h3>
        <p>{L['challenge']}</p>
      </div>
    </div>
  </section>

  <section id="screenshots" class="alt">
    <div class="wrap">
      <h2>{L['shots_h']}</h2>
      <div class="gallery">
{shots}
      </div>
    </div>
  </section>

  <section id="info">
    <div class="wrap">
      <h2>{L['info_h']}</h2>
      <dl class="facts">
{facts}
      </dl>
    </div>
  </section>

  <!-- demo: announce the Next Fest (October 2026) demo here once it is live -->

  <div class="cta-bottom">
    <p>{L['cta_text']}</p>
    <a class="btn" href="{store}">{L['cta_btn']}</a>
  </div>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div>
      <p class="maker"><img class="px" src="{r}assets/nozworks-gear.png" alt="" width="24" height="24">NoZworks</p>
      <p>{L['contact']}: <a href="mailto:{MAIL}">{MAIL}</a></p>
    </div>
    <div>
      <p>&copy; 2026 NoZworks</p>
      <p>{L['trademark']}</p>
      <p>{L['font_label']}: PixelMplus (M+ FONT LICENSE) / Fusion Pixel Font (SIL OFL 1.1)</p>
    </div>
  </div>
</footer>

</body>
</html>
"""


def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    en = next(x for x in LANGS if x["hreflang"] == "en")
    for L in LANGS:
        out.append("  <url>")
        out.append("    <loc>%s</loc>" % (BASE + L["dir"]))
        for x in LANGS:
            out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (x["hreflang"], BASE + x["dir"]))
        out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % (BASE + en["dir"]))
        out.append("    <lastmod>%s</lastmod>" % LASTMOD)
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def visible_text(page):
    page = re.sub(r"<script.*?</script>|<!--.*?-->", " ", page, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", page))


def subset_fonts(pages):
    from fontTools import subset
    from fontTools.ttLib import TTFont
    for group, (src, name, flavors) in FONTS.items():
        text = "".join(visible_text(p) for L, p in pages if L["font"] == group)
        chars = set(text) | set(string.ascii_letters + string.digits + string.punctuation + " ")
        chars = "".join(sorted(c for c in chars if c == " " or not c.isspace()))
        cmap = TTFont(src).getBestCmap()
        missing = "".join(c for c in chars if ord(c) not in cmap)
        for flavor in flavors:
            opts = subset.Options()
            opts.flavor = flavor
            opts.layout_features = ["*"]
            opts.ignore_missing_glyphs = True
            f = TTFont(src)
            sub = subset.Subsetter(opts)
            sub.populate(text=chars)
            sub.subset(f)
            f.flavor = flavor
            out = os.path.join(ROOT, "fonts", "%s.%s" % (name, flavor))
            f.save(out)
            print("font %-5s %-24s %4d KB  (字数 %d、未収録 %d)" % (group, os.path.basename(out), os.path.getsize(out) // 1024, len(chars), len(missing)))


def main():
    pages = []
    for L in LANGS:
        page = render(L)
        d = os.path.join(ROOT, L["dir"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as fp:
            fp.write(page)
        for n in {s[0] for s in L["steps"]} | {s[0] for s in L["shots"]}:
            p = os.path.join(ROOT, "assets", "ss", "%s-%d.png" % (L["ss"], n))
            if not os.path.exists(p):
                print("  ** 画像が無い: " + p)
        for p in ("assets/logo-%s.png" % L["ss"], "assets/og-%s.png" % L["ss"]):
            if not os.path.exists(os.path.join(ROOT, p)):
                print("  ** 画像が無い: " + p)
        pages.append((L, page))
        print("page %-9s %s" % (L["hreflang"], os.path.join(L["dir"], "index.html")))
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as fp:
        fp.write(sitemap())
    subset_fonts(pages)


if __name__ == "__main__":
    main()
