#!/usr/bin/env python3
"""由 series.yaml 產生 README 索引表與 days/day-NN.md 表頭。

--check：不寫檔，只要有任何輸出會變動就回傳 1。
"""
import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- INDEX:START -->", "<!-- INDEX:END -->"
DAY_START, DAY_END = "<!-- DAY:START -->", "<!-- DAY:END -->"
STATUS_LABEL = {"planned": "即將發表", "draft": "撰寫中"}


def load():
    with open(ROOT / "series.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def gh(repo, ref, path=""):
    url = f"https://github.com/{repo}/tree/{ref}"
    return f"{url}/{path}" if path else url


def article_cell(d):
    if d["status"] == "published" and d.get("article"):
        return f"[閱讀]({d['article']})"
    return STATUS_LABEL.get(d["status"], d["status"])


def code_cell(d):
    items = []
    for p in d.get("projects") or []:
        name = p["repo"].split("/", 1)[1]
        if p.get("tag"):
            items.append(f"[{name}@{p['tag']}]({gh(p['repo'], p['tag'])})")
        else:
            items.append(f"[{name}]({gh(p['repo'], 'HEAD')})")
    return "<br>".join(items) if items else " "


def render_index(data):
    out = []
    for part, name in data["parts"].items():
        out.append(f"### 第{'一二三'[int(part) - 1]}段：{name}\n")
        out.append("| Day | 主題 | 類別 | 文章 | 程式碼 |")
        out.append("|---:|---|---|---|---|")
        for d in data["days"]:
            if d["part"] != int(part):
                continue
            nn = f"{d['day']:02d}"
            out.append(
                f"| [{nn}](days/day-{nn}.md) | {d['title']} | `{d['category']}` "
                f"| {article_cell(d)} | {code_cell(d)} |"
            )
        out.append("")
    return "\n".join(out)


def render_day_header(d):
    nn = f"{d['day']:02d}"
    lines = [f"# Day {nn}：{d['title']}", ""]
    lines.append(f"- 狀態：{STATUS_LABEL.get(d['status'], '已發表')}")
    if d.get("date"):
        lines.append(f"- 發表日期：{d['date']}")
    if d.get("article"):
        lines.append(f"- 文章：{d['article']}")
    lines.append(f"- 類別：`{d['category']}`")
    projects = d.get("projects") or []
    if projects:
        lines += ["", "| 專案 | tag | commit | 重點檔案 |", "|---|---|---|---|"]
        for p in projects:
            ref = p.get("sha") or p.get("tag") or "HEAD"
            short = p["sha"][:7] if p.get("sha") else " "
            paths = "<br>".join(
                f"[{x}]({gh(p['repo'], ref, x)})" for x in p.get("paths") or []
            ) or " "
            tag = f"[{p['tag']}]({gh(p['repo'], p['tag'])})" if p.get("tag") else " "
            lines.append(
                f"| [{p['repo']}](https://github.com/{p['repo']}) | {tag} | `{short}` | {paths} |"
            )
    return "\n".join(lines)


def replace_block(text, start, end, body):
    head, sep1, rest = text.partition(start)
    _, sep2, tail = rest.partition(end)
    if not (sep1 and sep2):
        raise SystemExit(f"找不到標記 {start} / {end}")
    return f"{head}{start}\n{body}\n{end}{tail}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    data = load()
    targets = {}

    readme = ROOT / "README.md"
    old = readme.read_text(encoding="utf-8")
    targets[readme] = (old, replace_block(old, START, END, render_index(data)))

    for d in data["days"]:
        path = ROOT / "days" / f"day-{d['day']:02d}.md"
        if path.exists():
            old = path.read_text(encoding="utf-8")
        else:
            old = f"{DAY_START}\n{DAY_END}\n\n## 摘要\n\n## 怎麼跑\n\n## 延伸閱讀\n"
        targets[path] = (
            old if path.exists() else "",
            replace_block(old, DAY_START, DAY_END, render_day_header(d)),
        )

    changed = [p for p, (a, b) in targets.items() if a != b]
    if args.check:
        for p in changed:
            print(f"未同步：{p.relative_to(ROOT)}")
        return 1 if changed else 0

    for p in changed:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(targets[p][1], encoding="utf-8")
        print(f"已更新：{p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
