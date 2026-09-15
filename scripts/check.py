#!/usr/bin/env python3
"""驗證 series.yaml 與 repo 內文字。

離線檢查：欄位格式、天數連續、published 必填欄位、破折號、私有 IP、家目錄路徑、
          以及 .pii-patterns（不進版控，一行一個 regex）列出的個人字串。
線上檢查：repo 為公開、tag 存在且指向記錄的 SHA、paths 在該 SHA 存在、文章連結可達。

GitHub API 會讀取 GITHUB_TOKEN 或 GH_TOKEN；沒有 token 時每小時限 60 次。
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = {"overview", "packaging", "node-guard", "storage-backup", "change-mgmt"}
STATUSES = {"planned", "draft", "published"}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".txt"}
SKIP_DIRS = {".git", "__pycache__", ".venv"}
BUILTIN_PATTERNS = [
    ("破折號", re.compile(chr(0x2014))),
    ("私有 IP", re.compile(r"\b(10\.\d{1,3}|192\.168|172\.(1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b")),
    ("家目錄路徑", re.compile(r"/(home|Users)/[A-Za-z0-9_.-]+/")),
]

errors = []


def err(msg):
    errors.append(msg)
    print(f"  錯誤：{msg}")


def check_schema(data):
    print("欄位檢查")
    days = data.get("days") or []
    nums = [d.get("day") for d in days]
    if nums != list(range(1, len(nums) + 1)):
        err(f"day 必須從 1 起連續遞增，目前為 {nums}")
    parts = {int(k) for k in (data.get("parts") or {})}
    for d in days:
        tag = f"Day {d.get('day')}"
        if d.get("part") not in parts:
            err(f"{tag} part 不在 parts 內")
        if d.get("category") not in CATEGORIES:
            err(f"{tag} category 不合法：{d.get('category')}")
        if d.get("status") not in STATUSES:
            err(f"{tag} status 不合法：{d.get('status')}")
        if not d.get("title"):
            err(f"{tag} 缺 title")
        if d.get("status") == "published":
            for key in ("date", "article"):
                if not d.get(key):
                    err(f"{tag} 已發表但缺 {key}")
            if "暫定" in (d.get("title") or ""):
                err(f"{tag} 已發表但標題仍標暫定")
        for p in d.get("projects") or []:
            if not re.fullmatch(r"[\w.-]+/[\w.-]+", p.get("repo") or ""):
                err(f"{tag} repo 格式應為 owner/name：{p.get('repo')}")
            sha = p.get("sha")
            if sha is not None and not isinstance(sha, str):
                err(f"{tag} {p.get('repo')} 的 sha 被 YAML 解析成數字，請加引號")
            elif p.get("tag") and not re.fullmatch(r"[0-9a-f]{40}", sha or ""):
                err(f"{tag} {p.get('repo')} 有 tag 但 sha 不是 40 碼")
            if d.get("status") == "published" and not p.get("tag"):
                err(f"{tag} 已發表但 {p.get('repo')} 沒有釘 tag")


def check_text():
    print("文字檢查")
    patterns = list(BUILTIN_PATTERNS)
    extra = ROOT / ".pii-patterns"
    if extra.exists():
        for line in extra.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(("個人字串", re.compile(line)))
    for path in sorted(ROOT.rglob("*")):
        if path.suffix not in TEXT_SUFFIXES or SKIP_DIRS & set(path.parts):
            continue
        rel = path.relative_to(ROOT)
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for label, rx in patterns:
                if rx.search(line):
                    err(f"{rel}:{n} 含{label}")


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None


def resolve_tag(repo, tag):
    status, ref = api(f"/repos/{repo}/git/ref/tags/{tag}")
    if status != 200 or not isinstance(ref, dict):
        return None
    obj = ref["object"]
    while obj["type"] == "tag":  # annotated tag 要再解一層
        status, t = api(f"/repos/{repo}/git/tags/{obj['sha']}")
        if status != 200:
            return None
        obj = t["object"]
    return obj["sha"]


def url_ok(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 series-index-check"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status < 400
    except (urllib.error.URLError, TimeoutError):
        return False


def check_remote(data):
    print("線上檢查")
    seen_repos = {}
    for d in data["days"]:
        tag = f"Day {d['day']}"
        for p in d.get("projects") or []:
            repo = p["repo"]
            if repo not in seen_repos:
                status, info = api(f"/repos/{repo}")
                seen_repos[repo] = status == 200 and not info.get("private")
                if not seen_repos[repo]:
                    err(f"{tag} {repo} 不存在或不是公開 repo（HTTP {status}）")
            if not seen_repos[repo] or not p.get("tag"):
                continue
            sha = resolve_tag(repo, p["tag"])
            if sha is None:
                err(f"{tag} {repo} 找不到 tag {p['tag']}")
                continue
            if sha != p.get("sha"):
                err(f"{tag} {repo}@{p['tag']} 指向 {sha}，與記錄的 {p.get('sha')} 不符")
                continue
            before = len(errors)
            for path in p.get("paths") or []:
                status, _ = api(f"/repos/{repo}/contents/{path}?ref={sha}")
                if status != 200:
                    err(f"{tag} {repo}@{sha[:7]} 沒有 {path}")
            if len(errors) == before:
                print(f"  通過：{tag} {repo}@{p['tag']}")
        if d["status"] == "published" and d.get("article") and not url_ok(d["article"]):
            err(f"{tag} 文章連結無法開啟：{d['article']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="略過 GitHub API 與連結檢查")
    args = ap.parse_args()
    with open(ROOT / "series.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    check_schema(data)
    check_text()
    if not args.offline:
        check_remote(data)
    print(f"\n{'失敗' if errors else '全部通過'}（{len(errors)} 項錯誤）")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
