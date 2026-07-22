from html.parser import HTMLParser
from pathlib import Path
import json
import os


class FirstNewsCard(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_card = False
        self.done = False
        self.in_h3 = False
        self.in_p = False
        self.card_depth = 0
        self.url = ""
        self.title_parts = []
        self.body_parts = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        classes = values.get("class", "").split()
        if not self.done and not self.in_card and tag == "article" and "event-card" in classes:
            self.in_card = True
            self.card_depth = 1
            return
        if not self.in_card:
            return
        self.card_depth += 1
        if tag == "h3":
            self.in_h3 = True
        elif tag == "p":
            self.in_p = True
        elif tag == "a" and self.in_h3 and not self.url:
            self.url = values.get("href", "")

    def handle_endtag(self, tag):
        if not self.in_card:
            return
        if tag == "h3":
            self.in_h3 = False
        elif tag == "p":
            self.in_p = False
        self.card_depth -= 1
        if self.card_depth <= 0:
            self.in_card = False
            self.done = True

    def handle_data(self, data):
        if self.in_h3:
            self.title_parts.append(data)
        elif self.in_p:
            self.body_parts.append(data)

    def result(self):
        return {
            "url": self.url.strip(),
            "title": " ".join("".join(self.title_parts).split()),
            "body": " ".join("".join(self.body_parts).split()),
        }


def parse(path):
    parser = FirstNewsCard()
    if Path(path).exists():
        parser.feed(Path(path).read_text(encoding="utf-8"))
    return parser.result()


current = parse("xeberler.html")
previous = parse(os.environ.get("BEFORE_NEWS_FILE", "/tmp/xeberler-before.html"))
changed = bool(current["url"] and previous["url"] and current["url"] != previous["url"])

if current["url"] and not current["url"].startswith("http"):
    current["url"] = f"https://founderclub.az/{current['url'].lstrip('/')}"

output_path = os.environ.get("GITHUB_OUTPUT")
if output_path:
    with open(output_path, "a", encoding="utf-8") as output:
        output.write(f"changed={'true' if changed else 'false'}\n")
        output.write(f"title={current['title'][:120]}\n")
        output.write(f"body={current['body'][:220]}\n")
        output.write(f"url={current['url']}\n")

print(json.dumps({"changed": changed, **current}, ensure_ascii=True))
