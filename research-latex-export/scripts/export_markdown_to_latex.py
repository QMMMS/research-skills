from __future__ import annotations

import argparse
import re
from pathlib import Path


HEADING_MAP = {
    1: "section",
    2: "subsection",
    3: "subsubsection",
    4: "paragraph",
}
ARXIV_ID_RE = re.compile(r"^\d{4}\.\d{4,5}(v\d+)?$", re.IGNORECASE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
NUMBERED_HEADING_PREFIX_RE = re.compile(r"^(?:\d+(?:\.\d+)*\.?\s+)+")


def to_safe_arxiv_key(value: str) -> str:
    match = re.match(r"^(\d{4})\.(\d{4,5})(v(\d+))?$", value, re.IGNORECASE)
    if not match:
        return value
    yymm = match.group(1)
    number = match.group(2)
    version = match.group(4)
    if version:
        return f"arxiv_{yymm}_{number}_v{version}"
    return f"arxiv_{yymm}_{number}"


def escape_text(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def strip_numbered_heading_prefix(text: str) -> str:
    return NUMBERED_HEADING_PREFIX_RE.sub("", text.strip())


def normalize_heading_key(text: str) -> str:
    text = strip_numbered_heading_prefix(text).lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def convert_citations(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        inner = match.group(1)
        parts = re.split(r"[;,]", inner)
        keys = []
        for part in parts:
            key = part.strip()
            if key.startswith("@"):
                key = key[1:]
            if key:
                keys.append(key)
        if not keys:
            return match.group(0)
        return r"\cite{" + ",".join(keys) + "}"

    return re.sub(r"\[@([^\]]+)\]", repl, text)


def convert_inline(text: str) -> str:
    placeholders: list[str] = []

    def store(value: str) -> str:
        placeholders.append(value)
        return f"<<TOKEN{len(placeholders) - 1}>>"

    def save_code(match: re.Match[str]) -> str:
        return store(r"\texttt{" + escape_text(match.group(1)) + "}")

    def save_citation(match: re.Match[str]) -> str:
        inner = match.group(1)
        parts = re.split(r"[;,]", inner)
        keys = []
        for part in parts:
            key = part.strip()
            if key.startswith("@"):
                key = key[1:]
            if key.lower().startswith("arxiv:"):
                key = key.split(":", 1)[1].strip()
            # Normalize bare arXiv IDs into BibTeX-safe keys.
            if ARXIV_ID_RE.match(key):
                key = to_safe_arxiv_key(key)
            if key:
                keys.append(key)
        if not keys:
            return match.group(0)
        return store(r"\cite{" + ",".join(keys) + "}")

    def save_bold(match: re.Match[str]) -> str:
        return store(r"\textbf{" + escape_text(match.group(1)) + "}")

    def save_italic(match: re.Match[str]) -> str:
        return store(r"\emph{" + escape_text(match.group(1)) + "}")

    text = re.sub(r"`([^`]+)`", save_code, text)
    text = re.sub(r"\[@([^\]]+)\]", save_citation, text)
    text = re.sub(r"\*\*([^*]+)\*\*", save_bold, text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", save_italic, text)
    text = escape_text(text)

    for index, value in enumerate(placeholders):
        token = f"<<TOKEN{index}>>"
        text = text.replace(token, value)

    return text


def build_heading_plan(markdown: str, title: str) -> tuple[set[int], int]:
    lines = markdown.splitlines()
    headings: list[tuple[int, int, str]] = []
    for idx, raw in enumerate(lines):
        match = HEADING_RE.match(raw.rstrip())
        if not match:
            continue
        level = len(match.group(1))
        text = match.group(2).strip()
        headings.append((idx, level, text))

    skip_indexes: set[int] = set()
    if headings:
        first_idx, first_level, first_text = headings[0]
        if first_level == 1 and normalize_heading_key(first_text) == normalize_heading_key(title):
            skip_indexes.add(first_idx)

    remaining_levels = [level for idx, level, _ in headings if idx not in skip_indexes]
    min_level = min(remaining_levels) if remaining_levels else 1
    return skip_indexes, min_level


def markdown_to_latex(markdown: str, title: str = "") -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    in_list = False
    skip_heading_indexes, min_heading_level = build_heading_plan(markdown, title)

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(part.strip() for part in paragraph if part.strip())
            if text:
                out.append(convert_inline(text))
                out.append("")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append(r"\end{itemize}")
            out.append("")
            in_list = False

    for idx, raw in enumerate(lines):
        line = raw.rstrip()

        heading = HEADING_RE.match(line)
        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)

        if heading:
            if idx in skip_heading_indexes:
                continue
            flush_paragraph()
            close_list()
            raw_level = len(heading.group(1))
            effective_level = raw_level - min_heading_level + 1
            effective_level = max(1, min(effective_level, 4))
            heading_text = strip_numbered_heading_prefix(heading.group(2))
            heading_text = convert_inline(heading_text)
            cmd = HEADING_MAP.get(effective_level, "subparagraph")
            out.append(rf"\{cmd}{{{heading_text}}}")
            if cmd == "paragraph":
                out[-1] += " "
            else:
                out.append("")
            continue

        if bullet:
            flush_paragraph()
            if not in_list:
                out.append(r"\begin{itemize}[leftmargin=*]")
                in_list = True
            out.append(r"\item " + convert_inline(bullet.group(1).strip()))
            continue

        if not line.strip():
            flush_paragraph()
            close_list()
            continue

        paragraph.append(line)

    flush_paragraph()
    close_list()
    return "\n".join(out).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a Markdown research report into LaTeX.")
    parser.add_argument("--input", required=True, help="Input Markdown file")
    parser.add_argument("--output", required=True, help="Output .tex path")
    parser.add_argument("--template", required=True, help="Template file path")
    parser.add_argument("--title", default="Research Survey Draft", help="Document title")
    parser.add_argument("--author", default="Codex", help="Document author")
    parser.add_argument("--abstract", default="This draft was exported from a structured research-writing workflow.", help="Abstract text")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    template_path = Path(args.template)

    markdown = input_path.read_text(encoding="utf-8")
    body = markdown_to_latex(markdown, title=args.title)
    template = template_path.read_text(encoding="utf-8")
    rendered = (
        template.replace("<<TITLE>>", escape_text(args.title))
        .replace("<<AUTHOR>>", escape_text(args.author))
        .replace("<<ABSTRACT>>", escape_text(args.abstract))
        .replace("<<BODY>>", body)
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote LaTeX manuscript to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
