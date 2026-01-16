from __future__ import annotations

from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup  # type: ignore[import]


INPUT_PATH = Path(__file__).with_name("input.txt")
OUTPUT_PATH = Path(__file__).with_name("toc.md")


def _iter_topics(soup: BeautifulSoup) -> Iterable[str]:
    """Yield markdown bullet lines for pattern > subpattern > article."""
    for section in soup.select("section[id^='toc-pattern-']"):
        pattern = section.select_one("p.Toc_patternTitle__Zk5Fr")
        if not pattern:
            continue
        lines = [f"- {pattern.get_text(strip=True)}"]

        for subpattern in section.select("div.Toc_subpattern__bP146"):
            sub_title = subpattern.select_one("p.Toc_subpatternTitle__bscHy")
            if not sub_title:
                continue
            lines.append(f"  - {sub_title.get_text(strip=True)}")

            for li in subpattern.select("ul.Toc_articleList__aDF0z li"):
                link = li.find("a")
                text = link.get_text(strip=True) if link else li.get_text(" ", strip=True)
                if text:
                    lines.append(f"    - {text}")

        for line in lines:
            yield line


def build_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return "\n".join(_iter_topics(soup)) + "\n"


def create_markdown(
    input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH
) -> str:
    html = Path(input_path).read_text(encoding="utf-8")
    markdown = build_markdown(html)
    Path(output_path).write_text(markdown, encoding="utf-8")
    print(markdown)
    return markdown


if __name__ == "__main__":
    create_markdown()

