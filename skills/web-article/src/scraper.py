#!/usr/bin/env python3
"""
Web Article Scraper - 使用 Browser Use 云端浏览器提取任意网页文章内容
支持 JS 渲染站点：微信公众号、知乎、微博、Medium 等
"""

import os
import sys
import time
import json
import argparse
import urllib.request
import ssl

# ── Browser Use 配置 ──────────────────────────────────────────
BROWSER_USE_BASE = "https://api.browser-use.com/api/v3"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def get_api_key():
    """从环境变量或 ~/.hermes/.env 获取 API Key"""
    key = os.environ.get("BROWSER_USE_API_KEY")
    if key:
        return key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() == "BROWSER_USE_API_KEY":
                    return v.strip().strip('"\'')
    return None


def api_request(method, path, data=None):
    """发送 HTTP 请求到 Browser Use API"""
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "未找到 BROWSER_USE_API_KEY！\n"
            "请设置环境变量或写入 ~/.hermes/.env：\n"
            "  BROWSER_USE_API_KEY=bu_your_key_here"
        )

    url = f"{BROWSER_USE_BASE}{path}"
    body = json.dumps(data).encode() if data else None
    headers = {
        "X-Browser-Use-API-Key": api_key,
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60, context=CTX) as resp:
        return json.loads(resp.read())


def create_session(url, task=None):
    """创建 Browser Use Session 并返回 session_id"""
    if task is None:
        task = (
            "Navigate to this URL and wait for the page to fully load. "
            "Extract: (1) the article title, (2) ALL article body text. "
            "Return the complete article title and full text content."
        )

    result = api_request("POST", "/sessions", {
        "url": url,
        "task": task,
        "maxCostUsd": "1.0",   # 限制费用，防止意外
    })
    return result["id"]


def wait_for_result(session_id, timeout=120, poll_interval=5):
    """轮询直到 session 完成，返回文章内容"""
    elapsed = 0
    while elapsed < timeout:
        time.sleep(poll_interval)
        elapsed += poll_interval

        result = api_request("GET", f"/sessions/{session_id}")
        status = result.get("status")

        if status == "success":
            return result.get("output", "")
        elif status == "failed":
            raise RuntimeError(
                f"Browser Use Session 失败: {result.get('lastStepSummary')}"
            )
        elif status == "running":
            print(f"  ⏳ 渲染中... ({elapsed}s)", flush=True)
        else:
            print(f"  状态: {status}", flush=True)

    raise TimeoutError(
        f"Session {session_id} 在 {timeout}s 内未完成，"
        "可稍后用 session_id 查询: GET /sessions/{id}"
    )


def scrape_article(url, timeout=120):
    """
    抓取网页文章内容
    返回: {"url": str, "title": str, "content": str}
    """
    print(f"🌐 正在创建 Browser Use Session...")
    print(f"   URL: {url}")

    sid = create_session(url)
    print(f"   Session ID: {sid}")
    print(f"   等待渲染结果（最多 {timeout}s）...")

    content = wait_for_result(sid, timeout=timeout)

    # 尝试从内容中分离标题和正文
    # Browser Use 通常返回格式: "标题\n\n正文" 或纯正文
    lines = content.strip().split("\n", 2)
    if len(lines) >= 2 and len(lines[0]) < 100:
        title = lines[0].strip()
        body = lines[1].strip()
    else:
        title = ""
        body = content.strip()

    return {
        "url": url,
        "title": title,
        "content": body,
        "raw": content,
        "session_id": sid,
    }


def get_title_only(url):
    """快速获取文章标题（不需要等待完整渲染）"""
    print(f"🔍 获取标题: {url}")
    sid = create_session(url, task="Extract only the article title. Return just the title text.")
    # 快速轮询，标题通常很快返回
    for i in range(6):  # 最多 30s
        time.sleep(5)
        result = api_request("GET", f"/sessions/{sid}")
        if result.get("status") == "success":
            return result.get("output", "").strip()
        if result.get("status") == "failed":
            break
    return ""


# ── CLI ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Web Article Scraper - Browser Use")
    parser.add_argument("url", nargs="?", help="文章 URL")
    parser.add_argument("--title-only", action="store_true", help="只提取标题")
    parser.add_argument("--timeout", type=int, default=120, help="最大等待秒数")
    parser.add_argument("--batch", metavar="FILE", help="批量文件（每行一个 URL）")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    # 批量模式
    if args.batch:
        urls = [u.strip() for u in open(args.batch) if u.strip()]
        results = []
        for url in urls:
            try:
                r = scrape_article(url, timeout=args.timeout)
                results.append(r)
                print(f"✅ [{len(results)}/{len(urls)}] {r['title'] or url}")
            except Exception as e:
                results.append({"url": url, "error": str(e)})
                print(f"❌ [{len(results)}/{len(urls)}] {url}: {e}")
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    # 单 URL 模式
    if not args.url:
        parser.print_help()
        return

    if args.title_only:
        title = get_title_only(args.url)
        print(f"\n📄 标题: {title}")
        return

    result = scrape_article(args.url, timeout=args.timeout)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"\n{'='*60}")
    print(f"📄 {result['title'] or '(无标题)'}")
    print(f"{'='*60}")
    print(result["content"])
    print(f"{'='*60}")
    print(f"\n🌐 原始页面: {result['url']}")
    print(f"🆔 Session ID: {result['session_id']}")


if __name__ == "__main__":
    main()
