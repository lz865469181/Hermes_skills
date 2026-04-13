# hermes-web-article

> 使用 Browser Use 云端浏览器自动化，通用网页文章内容提取工具。支持微信公众号、知乎、微博、Medium 等所有 JS 渲染站点。Hermes Agent Skill 开源版。

English | [中文](README.md)

## ✨ 功能

- 🌐 **支持所有 JS 渲染站点**：微信公众号、知乎、微博、Medium、Dev.to 等
- ⚡ **无需本地浏览器**：云端渲染，直接返回文章内容
- 🐍 **Python 脚本**：独立运行，不依赖 Hermes
- 🤖 **Hermes Skill**：丢链接给 Hermes，直接提取+处理
- 📦 **零配置**：API Key 写入 `~/.hermes/.env` 即可

## 🚀 快速开始

### 1. 获取 API Key

注册 [Browser Use](https://browser-use.com)（Hermes Agent 用户免费）：

```bash
# 登录 cloud.browser-use.com
# Settings → API Keys → Create
# 将 Key 写入配置
echo "BROWSER_USE_API_KEY=bu_your_key_here" >> ~/.hermes/.env
```

### 2. 安装 & 运行

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/hermes-web-article.git
cd hermes-web-article

# 运行
pip install requests
python3 src/scraper.py "https://mp.weixin.qq.com/s/xxxxx"
```

### 3. 作为 Hermes Skill 使用

将 `SKILL.md` 复制到你的 Hermes skills 目录：

```bash
cp SKILL.md ~/.hermes/skills/productivity/web-article/
```

然后直接丢链接给 Hermes：

```
你: 帮我抓取这篇文章 https://mp.weixin.qq.com/s/xxxxx
```

## 📖 使用方法

### 命令行

```bash
# 基本用法
python3 src/scraper.py "https://mp.weixin.qq.com/s/xxxxx"

# 只提取标题（更快）
python3 src/scraper.py "https://mp.weixin.qq.com/s/xxxxx" --title-only

# 批量抓取
python3 src/scraper.py --batch urls.txt

# JSON 输出
python3 src/scraper.py "https://mp.weixin.qq.com/s/xxxxx" --json
```

### Python API

```python
from scraper import scrape_article

result = scrape_article("https://mp.weixin.qq.com/s/xxxxx")
print(result["title"])   # 文章标题
print(result["content"]) # 文章正文
```

## 🏗️ 项目结构

```
hermes-web-article/
├── SKILL.md              # Hermes Skill 定义文件
├── src/
│   └── scraper.py        # 核心爬虫脚本
├── tests/
│   └── test_scraper.py   # 单元测试
└── examples/
    └── demo.py           # 使用示例
```

## 🔧 Browser Use API

```
POST https://api.browser-use.com/api/v3/sessions
GET  https://api.browser-use.com/api/v3/sessions/{id}
```

**免费额度（2026-04）**：
- ✅ 无限时长
- ✅ 免费 proxy（美国节点）
- ✅ 持久化鉴权

## 🐏 薅羊毛

Browser Use 官方 2026-04-09 宣布：Hermes Agent 用户可**免费试用**。

[立即申请 →](https://cloud.browser-use.com/settings?tab=api-keys&new=1)

## � alternatives

不想用云服务？

- **[CamoFox](https://github.com/dracohu2025-cloud/draco-skills-collection)** - 纯本地浏览器，无云费用

## 📄 License

MIT License

## 🤝 Contributing

Issues 和 PR 欢迎！

---

> 配套 Hermes Skill 集合：[dracohu2025-cloud/draco-skills-collection](https://github.com/dracohu2025-cloud/draco-skills-collection)
