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

## ⚠️ 首次使用配置

**必须设置 API Key，否则无法使用。**

### Step 1: 获取 Browser Use API Key

1. 打开 https://cloud.browser-use.com/settings?tab=api-keys&new=1
2. 登录/注册账号
3. 创建一个新的 API Key
4. 复制 Key（格式：`bu_xxx`）

### Step 2: 写入配置文件

```bash
# 复制配置文件模板
cp skills/web-article/.env.example ~/.hermes/.env

# 编辑 ~/.hermes/.env，填入你的 API Key：
# BROWSER_USE_API_KEY=bu_your_key_here
```

### Step 3: 验证安装

```bash
python3 skills/web-article/src/scraper.py "https://example.com" --title-only
```

---

## 支持场景

| 站点类型 | 示例 | 状态 |
|---------|------|------|
| 微信公众号 | mp.weixin.qq.com | ✅ |
| 知乎 | zhihu.com | ✅ |
| 微博 | weibo.com | ✅ |
| Medium / Dev.to | medium.com | ✅ |
| 新闻站点 | 任意 JS 渲染站 | ✅ |
| 普通 HTML 站 | 任意静态站 | ✅ |

## 使用方法

### 作为 Hermes Skill 使用

```
你: 帮我抓取这篇文章的内容 https://mp.weixin.qq.com/s/xxxxx
Hermes: 加载 web-article skill，使用 Browser Use 提取内容
```

### 作为 Python 脚本使用

```bash
# 基本用法
python3 skills/web-article/src/scraper.py "https://mp.weixin.qq.com/s/xxxxx"

# 只提取标题
python3 skills/web-article/src/scraper.py "https://mp.weixin.qq.com/s/xxxxx" --title-only

# 批量抓取
python3 skills/web-article/src/scraper.py --batch urls.txt
```

## Python API

```python
import sys
sys.path.insert(0, "skills/web-article/src")
from scraper import scrape_article

result = scrape_article("https://mp.weixin.qq.com/s/xxxxx")
print(result["title"])
print(result["content"])
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
