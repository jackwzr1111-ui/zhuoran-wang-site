"""Check the generated portfolio using only Python's standard library."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree

DIST = Path(__file__).resolve().parents[1] / "dist"
LANGUAGES = {"zh-CN", "en", "ms"}


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.lang = self.canonical = self.description = self.robots = None
        self.title = []
        self.schema = []
        self.capture = None
        self.alternates = {}
        self.switch = {}
        self.ids = set()
        self.links = []
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "meta" and a.get("name") in ("description", "robots"):
            setattr(self, a["name"], a.get("content"))
        if tag == "title":
            self.capture = self.title
        if tag == "script" and a.get("type") == "application/ld+json":
            self.capture = self.schema
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a["href"]
        if tag == "link" and a.get("rel") == "alternate" and "hreflang" in a:
            self.alternates[a["hreflang"]] = a["href"]
        if tag == "a" and a.get("hreflang") and a.get("href"):
            self.switch[a["hreflang"]] = a["href"]
        if tag in ("a", "link", "img", "script"):
            for key in ("href", "src"):
                if a.get(key):
                    self.links.append(a[key])

    def handle_data(self, data):
        if self.capture is not None:
            self.capture.append(data)

    def handle_endtag(self, tag):
        if tag in ("title", "script"):
            self.capture = None


def require(value, message):
    if not value:
        raise SystemExit(message)


def check_site(site):
    root = site.rstrip("/") + "/"
    root_url = urlsplit(root)
    pages = {}
    for path in DIST.rglob("*.html"):
        route = path.relative_to(DIST).as_posix()
        if route.endswith("/index.html") or route == "index.html":
            route = route[:-len("index.html")]
        pages[urljoin(root, route)] = Page(path)

    sitemap = ElementTree.parse(DIST / "sitemap.xml")
    locs = [element.text for element in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    require(pages and set(locs) == set(pages) and len(locs) == len(pages), "sitemap and HTML paths differ")
    robots = (DIST / "robots.txt").read_text(encoding="utf-8").splitlines()
    require("Sitemap: " + urljoin(root, "sitemap.xml") in robots, "robots.txt sitemap mismatch")
    titles = set()
    for url, page in pages.items():
        title = "".join(page.title).strip()
        require(title and title not in titles and page.description, f"{url}: missing or shared page metadata")
        titles.add(title)
        require(page.canonical == url and page.lang in LANGUAGES, f"{url}: canonical or language mismatch")
        require(page.robots == "index,follow", f"{url}: indexing directive changed")
        require(set(page.alternates) == LANGUAGES | {"x-default"}, f"{url}: missing language links")
        require(page.alternates[page.lang] == url and page.alternates["x-default"] == page.alternates["zh-CN"],
                f"{url}: self or default language mismatch")
        for lang, translated in page.alternates.items():
            target = pages.get(translated)
            require(target and target.alternates == page.alternates and
                    (lang == "x-default" or target.lang == lang), f"{url}: alternate {lang}")
        require(set(page.switch) == LANGUAGES and
                all(urljoin(url, href) == page.alternates[lang] for lang, href in page.switch.items()),
                f"{url}: language switcher does not point to the same page in each language")
        graph = json.loads("".join(page.schema))["@graph"]
        require(any(n.get("url") == url for n in graph), f"{url}: structured data has no page URL")
        for ref in page.links:
            dest = urlsplit(urljoin(url, ref))
            if dest.scheme != root_url.scheme or dest.netloc != root_url.netloc:
                continue
            require(dest.path.startswith(root_url.path), f"{url}: link outside site base {ref}")
            relative_path = unquote(dest.path[len(root_url.path):])
            disk = DIST / relative_path
            if disk.is_dir():
                disk = disk / "index.html"
            require(disk.is_file(), f"{url}: missing {ref}")
            if dest.fragment:
                target = pages.get(dest._replace(fragment="", query="").geturl())
                require(target and unquote(dest.fragment) in target.ids, f"{url}: missing anchor {ref}")
    print(f"OK: {len(pages)} pages, internal links, language alternates, metadata and sitemap.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-url", required=True)
    check_site(parser.parse_args().site_url)
