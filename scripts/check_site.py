#!/usr/bin/env python3
"""Offline integrity checks for CROSSGLINT GitHub Pages sources."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import re
import struct
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
ARTWORK = {
    "assets/crossglint-mark-400.png": (400, 400, "f36cce9749185d74fecb3efbe69c127fca46f57e"),
    "assets/crossglint-header-1500x500.png": (1500, 500, "03b6774b3e40dab937fd238efa9c36b3182fb55f"),
}

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.images = []
        self.page_titles = 0
        self.main_count = 0
        self.lang = False
        self.ids = set()
        self.desc = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "html":
            self.lang = bool(attrs.get("lang"))
        if tag == "main":
            self.main_count += 1
        if tag == "title":
            self.page_titles += 1
        if tag == "meta" and attrs.get("name") == "description":
            self.desc = bool(attrs.get("content"))
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag in ("a", "link") and attrs.get("href"):
            self.refs.append(attrs["href"])
        if tag == "img":
            self.images.append(attrs)
            if attrs.get("src"):
                self.refs.append(attrs["src"])

def git_sha(blob):
    contents = b"blob " + str(len(blob)).encode() + b"\0" + blob
    return hashlib.sha1(contents).hexdigest()

def check():
    for name, (w, h, expected_sha) in ARTWORK.items():
        data = (ROOT / name).read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n"), f"{name}: invalid PNG"
        width, height = struct.unpack(">II", data[16:24])
        assert (width, height) == (w, h), f"{name}: unexpected image dimensions"
        assert git_sha(data) == expected_sha, f"{name}: approved brand export was modified"

    for filename in ("index.html", "privacy.html"):
        source = (ROOT / filename).read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(source)
        assert parser.lang and parser.page_titles == 1 and parser.main_count == 1 and parser.desc, filename
        assert parser.images and all("alt" in img for img in parser.images), f"{filename}: missing image alt"
        assert "CROSSGLINT" in source and "crossglint.studio@gmail.com" in source
        assert "assets/crossglint-mark-400.png" in source
        assert 'href="style.css"' in source
        for ref in parser.refs:
            parsed = urlsplit(ref)
            if parsed.scheme in ("mailto", "https", "http") or ref.startswith("#"):
                if ref.startswith("#"):
                    assert ref[1:] in parser.ids, f"{filename}: missing fragment {ref}"
                continue
            assert not parsed.scheme and not parsed.netloc, f"{filename}: unexpected scheme {ref}"
            path = unquote(parsed.path)
            local = (ROOT / (path or "./")).resolve()
            assert local == ROOT or ROOT in local.parents, f"{filename}: escapes root {ref}"
            if path.endswith("/") or not path or path == "./":
                local = local / "index.html"
            assert local.is_file(), f"{filename}: missing local asset/link {ref}"
            if parsed.fragment and local.suffix == ".html":
                target = PageParser()
                target.feed(local.read_text(encoding="utf-8"))
                assert parsed.fragment in target.ids, f"{filename}: bad fragment {ref}"
    assert 'id="english"' in (ROOT / "privacy.html").read_text(encoding="utf-8")
    print("Site HTML, accessibility basics, local links and approved brand assets: OK")

if __name__ == "__main__":
    check()
