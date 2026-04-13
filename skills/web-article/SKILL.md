---
name: web-article
description: 使用 Browser Use 云端浏览器自动化抓取任意网页的完整文章内容（支持 JS 渲染站点）
triggers:
  - 抓取网页文章
  - 爬取文章
  - scrape article
  - extract article content
  - 微信公众号文章
  - wechat article
  - 知乎文章
  - zhihu
---

# Web Article Scraper

通用网页文章内容提取工具。使用 Browser Use 云端浏览器自动化，**无需本地浏览器**，支持所有 JS 渲染站点。

## 支持场景

| 站点类型 | 示例 | 状态 |
|---------|------|------|
| 微信公众号 | mp.weixin.qq.com | ✅ |
| 知乎 | zhihu.com | ✅ |
| 微博 | weibo.com | ✅ |
| Medium / Dev.to | medium.com | ✅ |
| 新闻站点 | 任意 JS 渲染站 | ✅ |
| 普通 HTML 站 | 任意静态站 | ✅ |

## 环境要求

```bash
# 设置 API Key
echo "BROWSER_USE_API_KEY=bu_your_key_here" >> ~/.hermes/.env
```

## 使用方法

### 作为 Hermes Skill 使用

```
你: 帮我抓取这篇文章的内容 https://mp.weixin.qq.com/s/xxxxx
Hermes: 加载 web-article skill，使用 Browser Use 提取内容
```

### 作为 Python 脚本使用

```bash
# 基本用法
python3 src/scraper.py "https://mp.weixin.qq.com/s/xxxxx"

# 只提取标题
python3 src/scraper.py "https://mp.weixin.qq.com/s/xxxxx" --title-only

# 批量抓取
python3 src/scraper.py --batch urls.txt
```

## Python API

```python
from scraper import scrape_article

result = scrape_article("https://mp.weixin.qq.com/s/xxxxx")
print(result["title"])
print(result["content"])
```

## Browser Use API 原理

```
POST /sessions → 创建渲染任务
     ↓
轮询 GET /sessions/{id} 直到 status = success
     ↓
返回提取的文本内容
```

### 直接调用

```python
import requests, time, os

API_KEY = os.environ["BROWSER_USE_API_KEY"]
BASE = "https://api.browser-use.com/api/v3"
HEADERS = {
    "X-Browser-Use-API-Key": API_KEY,
    "Content-Type": "application/json",
}

def create_session(url, task):
    resp = requests.post(
        f"{BASE}/sessions",
        headers=HEADERS,
        json={"url": url, "task": task},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["id"]

def wait_for_result(session_id, timeout=120):
    for _ in range(timeout // 5):
        resp = requests.get(
            f"{BASE}/sessions/{session_id}",
            headers=HEADERS,
            timeout=60,
        )
        result = resp.json()
        if result["status"] == "success":
            return result["output"]
        elif result["status"] == "failed":
            raise RuntimeError(f"Failed: {result.get('lastStepSummary')}")
        time.sleep(5)
    raise TimeoutError(f"Session {session_id} timed out")

url = "https://mp.weixin.qq.com/s/xxxxx"
task = "Extract the article title and full text content."
content = wait_for_result(create_session(url, task))
```

## 免费额度（2026-04）

Browser Use 官方为 Hermes Agent 用户提供**免费试用**：
- ✅ 无限时长
- ✅ 免费 proxy（美国节点）
- ✅ 持久化鉴权

获取 API Key: https://cloud.browser-use.com/settings?tab=api-keys&new=1

## 本地替代方案

不想用云服务？用 **CamoFox**（纯本地）：

```bash
pip install camofox
```

参考: https://github.com/dracohu2025-cloud/draco-skills-collection
