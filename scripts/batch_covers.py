#!/usr/bin/python3
"""批量生成封面脚本"""
import subprocess
import os
import re
import json
from pathlib import Path

BLOG_DIR = "/root/myweb/src/content/blog"
SCRIPT = "/root/myweb/scripts/cover_generator.py"

articles = []
for file in sorted(Path(BLOG_DIR).glob("*.mdx")):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        continue
    fm_text = match.group(1)
    title = ""
    category = "general"
    has_cover = False
    for line in fm_text.split("\n"):
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip("'\"")
        elif line.startswith("category:"):
            category = line.split(":", 1)[1].strip().strip("'\"")
        elif line.startswith("cover:"):
            has_cover = True
    if not has_cover:
        articles.append({"file": str(file), "slug": file.stem, "title": title, "category": category})

print(f"开始生成 {len(articles)} 篇封面", flush=True)

results = []
for i, article in enumerate(articles):
    print(f"[{i+1}/{len(articles)}] {article['title'][:30]}...", flush=True)
    try:
        result = subprocess.run(
            ["/usr/bin/python3", SCRIPT, article["category"], article["title"]],
            capture_output=True, text=True, timeout=180
        )
        if result.returncode == 0:
            cover_url = result.stdout.strip()
            results.append({"slug": article["slug"], "url": cover_url, "status": "ok"})
            print(f"   OK: {cover_url}", flush=True)
        else:
            err = result.stderr.strip().split("\n")[-1] if result.stderr else "fail"
            results.append({"slug": article["slug"], "url": None, "status": "fail", "error": err})
            print(f"   FAIL: {err}", flush=True)
    except Exception as e:
        results.append({"slug": article["slug"], "url": None, "status": "error", "error": str(e)})
        print(f"   ERROR: {e}", flush=True)

with open("/tmp/cover_results.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

ok = len([r for r in results if r["status"] == "ok"])
print(f"完成: 成功 {ok}/{len(articles)}", flush=True)
