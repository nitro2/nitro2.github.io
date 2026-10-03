#!/usr/bin/env python3
"""Build the static blog: index.html, feed.xml, sitemap.xml from posts/*.html.

Each post is a self-contained HTML file and must have in <head>:
  <title>…</title>
  <meta name="description" content="…">
  <meta name="date" content="YYYY-MM-DD">
The script also injects a small "back to home" link into each post (idempotent).
Usage:  python3 build.py        (standard library only)
"""
import html, re, datetime as dt
from pathlib import Path
from email.utils import format_datetime

SITE_TITLE = "Ghi chép kinh tế"
SITE_DESC = "Ghi chép về kinh tế, dòng tiền và thị trường tài chính Việt Nam. Mang tính giáo dục, không phải khuyến nghị đầu tư."
SITE_URL = "https://nitro2.github.io"
AUTHOR = "Nhân Ngô"

ROOT = Path(__file__).parent
POSTS = ROOT / "posts"
HOME_LINK = ('<a class="home-link" href="/" style="display:inline-block;margin-bottom:18px;font-size:14px;'
             'text-decoration:none">← ' + html.escape(SITE_TITLE) + "</a>")


def meta(src, name):
    m = re.search(r'<meta\s+name="%s"\s+content="([^"]*)"' % name, src, re.I)
    return html.unescape(m.group(1)) if m else ""


def load_posts():
    posts = []
    for f in sorted(POSTS.glob("*.html")):
        src = f.read_text(encoding="utf-8")
        t = re.search(r"<title>(.*?)</title>", src, re.S | re.I)
        date = meta(src, "date")
        if not (t and date):
            raise SystemExit(f'{f.name}: thiếu <title> hoặc <meta name="date">')
        if 'class="home-link"' not in src:
            src = re.sub(r"(<main[^>]*>)", lambda m: m.group(1) + "\n" + HOME_LINK, src, count=1)
            f.write_text(src, encoding="utf-8")
        posts.append(dict(file=f.name, url=f"/posts/{f.name}", title=html.unescape(t.group(1).strip()),
                          desc=meta(src, "description"), date=dt.date.fromisoformat(date)))
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def build_index(posts):
    items = "\n".join(
        f'<article><time datetime="{p["date"]}">{p["date"]:%d/%m/%Y}</time>'
        f'<h2><a href="{p["url"]}">{html.escape(p["title"])}</a></h2><p>{html.escape(p["desc"])}</p></article>'
        for p in posts) or "<p>Chưa có bài viết.</p>"
    return f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(SITE_TITLE)}</title><meta name="description" content="{html.escape(SITE_DESC)}">
<link rel="alternate" type="application/rss+xml" title="{html.escape(SITE_TITLE)}" href="/feed.xml">
<style>
:root{{--bg:#fbfaf7;--fg:#1f1e1c;--muted:#6b6a65;--line:#e4e2dc;--accent:#2f6fb7}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1b1b1a;--fg:#ecebe6;--muted:#a3a19a;--line:#3a3936;--accent:#6aa5e6}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:17px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}}
main{{max-width:760px;margin:0 auto;padding:56px 22px 80px}}
header h1{{font-size:34px;margin:0 0 6px;font-weight:650}}header p{{color:var(--muted);margin:0 0 30px}}
article{{padding:22px 0;border-top:1px solid var(--line)}}
article h2{{font-size:22px;margin:4px 0 6px;font-weight:620;line-height:1.35}}
article h2 a{{color:var(--fg);text-decoration:none}}article h2 a:hover{{color:var(--accent)}}
article p{{margin:0;color:var(--muted)}}time{{font-size:14px;color:var(--muted)}}
footer{{margin-top:40px;padding-top:18px;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}}a{{color:var(--accent)}}
</style></head><body><main>
<header><h1>{html.escape(SITE_TITLE)}</h1><p>{html.escape(SITE_DESC)}</p>
<p style="margin:-14px 0 28px"><a href="/monitor/">📊 Theo dõi dòng tiền chứng khoán Việt Nam (cập nhật mỗi phiên)</a><br>
<a href="/stablecoin/">💵 Theo dõi vốn hóa stablecoin (cập nhật hằng ngày)</a></p></header>
{items}
<footer>© {dt.date.today().year} {html.escape(AUTHOR)} · <a href="/feed.xml">RSS</a></footer>
</main></body></html>
"""


def build_feed(posts):
    def rfc(d):
        return format_datetime(dt.datetime(d.year, d.month, d.day, 8, tzinfo=dt.timezone(dt.timedelta(hours=7))))
    items = "".join(
        f"<item><title>{html.escape(p['title'])}</title><link>{SITE_URL}{p['url']}</link><guid>{SITE_URL}{p['url']}</guid>"
        f"<pubDate>{rfc(p['date'])}</pubDate><description>{html.escape(p['desc'])}</description></item>" for p in posts)
    return (f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{html.escape(SITE_TITLE)}</title>'
            f"<link>{SITE_URL}/</link><description>{html.escape(SITE_DESC)}</description><language>vi</language>{items}"
            "</channel></rss>\n")


def build_sitemap(posts):
    urls = [f"<url><loc>{SITE_URL}/</loc></url>"] + [
        f"<url><loc>{SITE_URL}{p['url']}</loc><lastmod>{p['date']}</lastmod></url>" for p in posts]
    return ('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + "".join(urls) + "</urlset>\n")


if __name__ == "__main__":
    posts = load_posts()
    (ROOT / "index.html").write_text(build_index(posts), encoding="utf-8")
    (ROOT / "feed.xml").write_text(build_feed(posts), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(build_sitemap(posts), encoding="utf-8")
    (ROOT / ".nojekyll").write_text("")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    print(f"Built {len(posts)} post(s):", *[f"  {p['date']}  {p['title']}" for p in posts], sep="\n")
