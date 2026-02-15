---
name: web-search-plus
version: 2.6.5
description: 统一搜索功能，结合智能自动路由技术。通过多信号分析，能够自动在 Serper（谷歌）、Tavily（研究型搜索引擎）、Exa（基于神经网络的搜索引擎）、You.com（混合式搜索引擎/实时更新）以及 SearXNG（注重隐私的、自托管的搜索引擎）之间进行选择，并为每种搜索方式提供置信度评分。
tags: [search, web-search, serper, tavily, exa, you, searxng, google, research, semantic-search, auto-routing, multi-provider, shopping, rag, free-tier, privacy, self-hosted]
metadata: {"openclaw":{"requires":{"bins":["python3","bash"],"env":{"SERPER_API_KEY":"optional","TAVILY_API_KEY":"optional","EXA_API_KEY":"optional","YOU_API_KEY":"optional","SEARXNG_INSTANCE_URL":"optional"},"note":"Only ONE provider key needed. All are optional."}}}
---

# Web Search Plus

**别再手动选择搜索服务了，让这个工具来帮你吧！**

该工具可以连接5个搜索服务（Serper、Tavily、Exa、You.com、SearXNG），并自动为每个查询选择最合适的搜索服务。需要查找购物信息？→ 使用Google；需要做研究？→ 使用专业的研究引擎；注重隐私？→ 可选择自托管服务。

---

## ✨ 这个工具的独特之处是什么？

- **简单搜索**：无需考虑使用哪个搜索服务；
- **智能路由**：会根据你的查询内容自动选择最佳的服务；
- **多服务合一**：Google搜索结果、专业研究引擎、神经搜索、基于RAG（Retrieval, Augmentation, and Generation）的搜索功能，以及注重隐私的搜索服务，全部整合在一个工具中；
- **只需一个API密钥**：可以先使用任意一个服务，之后再添加更多；
- **免费选项可用**：SearXNG完全免费（支持自托管）。

---

## 🚀 快速入门

```bash
# Interactive setup (recommended for first run)
python3 scripts/setup.py

# Or manual: copy config and add your keys
cp config.example.json config.json
```

向导会介绍每个搜索服务，帮助你获取API密钥，并配置默认设置。

---

## 🔑 API密钥

你只需要一个API密钥即可开始使用。之后可以根据需要添加更多服务以获得更全面的搜索体验。

| 服务 | 免费 tier | 适用场景 | 注册链接 |
|------|---------|---------|---------|
| **Serper** | 2,500/月 | 购物、价格查询、本地信息、新闻 | [serper.dev](https://serper.dev) |
| **Tavily** | 1,000/月 | 研究、解释性内容、学术资料 | [tavily.com](https://tavily.com) |
| **Exa** | 1,000/月 | 类似X平台的搜索服务、初创企业信息、论文搜索 | [exa.ai](https://exa.ai) |
| **You.com** | 有限免费量 | 实时信息、AI辅助的搜索结果 | [api.you.com](https://api.you.com) |
| **SearXNG** | **完全免费** ✅ | 注重隐私、多源信息、零费用 | 支持自托管 |

**如何设置API密钥：**

```bash
# Option A: .env file (recommended)
export SERPER_API_KEY="your-key"
export TAVILY_API_KEY="your-key"

# Option B: config.json
{ "serper": { "api_key": "your-key" } }
```

---

## 🎯 何时使用哪个服务？

| 需要做什么 | 适用服务 | 示例查询 |
|---------|---------|---------|
| 查找产品价格 | **Serper** | “iPhone 16 Pro Max的价格” |
| 查找附近的餐厅/商店 | **Serper** | “我附近的最好披萨店” |
| 了解某事物的工作原理 | **Tavily** | “HTTPS加密的原理是什么” |
| 进行深入研究 | **Tavily** | “2024年的气候变化研究” |
| 查找类似的公司 | **Exa** | “与Notion类似的初创企业” |
| 查找研究论文 | **Exa** | “Transformer架构相关的论文” |
| 获取实时信息 | **You.com** | “最新的AI法规新闻” |
| 隐私搜索 | **SearXNG** | 任何查询，且不记录用户信息 |

**小贴士：** 直接正常搜索即可！系统会自动选择最佳服务；如需手动指定服务，可使用 `-p service` 参数。

---

## 🧠 自动路由机制

该工具会分析你的查询内容，并自动选择最合适的搜索服务：

```bash
"iPhone 16 price"              → Serper (shopping keywords)
"how does quantum computing work" → Tavily (research question)
"companies like stripe.com"    → Exa (URL detected, similarity)
"latest news on AI"            → You.com (real-time intent)
"search privately"             → SearXNG (privacy keywords)
```

**如果选择错误怎么办？** 可使用以下命令进行手动指定：`python3 scripts/search.py -p tavily -q "你的查询内容"`  
**查看路由逻辑**：`python3 scripts/search.py --explain-routing -q "你的查询内容"`  

---

## 📖 使用示例

### 推荐：让系统自动选择服务

```bash
python3 scripts/search.py -q "Tesla Model 3 price"
python3 scripts/search.py -q "explain machine learning"
python3 scripts/search.py -q "startups like Figma"
```

### 强制使用特定服务

```bash
python3 scripts/search.py -p serper -q "weather Berlin"
python3 scripts/search.py -p tavily -q "quantum computing" --depth advanced
python3 scripts/search.py -p exa --similar-url "https://stripe.com" --category company
python3 scripts/search.py -p you -q "breaking tech news" --include-news
python3 scripts/search.py -p searxng -q "linux distros" --engines "google,bing"
```

---

## ⚙️ 配置设置

```json
{
  "auto_routing": {
    "enabled": true,
    "fallback_provider": "serper",
    "confidence_threshold": 0.3,
    "disabled_providers": []
  },
  "serper": {"country": "us", "language": "en"},
  "tavily": {"depth": "advanced"},
  "exa": {"type": "neural"},
  "you": {"country": "US", "include_news": true},
  "searxng": {"instance_url": "https://your-instance.example.com"}
}
```

---

## 📊 各服务对比

| 功能 | Serper | Tavily | Exa | You.com | SearXNG |
|---------|------:|:------:|:---:|:-------:|:-------:|
| 搜索速度 | ⚡⚡⚡ | ⚡⚡ | ⚡⚡ | ⚡⚡⚡ | ⚡⚡ |
| 事实准确性 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 语义理解能力 | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| 提供完整页面内容 | ✗ | ✓ | ✓ | ✓ | ✗ |
| 购物/本地信息搜索 | ✓ | ✗ | ✗ | ✗ | ✓ |
| 查找相似页面 | ✗ | ✗ | ✓ | ✗ | ✗ |
| 基于RAG的搜索优化 | ✗ | ✓ | ✗ | ✓✓ | ✗ |
| 隐私保护 | ✗ | ✗ | ✗ | ✗ | ✓✓ |
| API费用 | $$ | $$ | $$ | $ | **免费** |

---

## ❓ 常见问题

### 所有服务都需要API密钥吗？
**不需要**。只需为你使用的服务获取密钥。建议从Serper开始使用，之后再添加其他服务。

### 应该从哪个服务开始使用？
**Serper**：搜索速度最快，免费 tier的查询量最多（每月2,500次），且适用范围较广。

### 如果免费查询次数用完了怎么办？
系统会自动切换到其他已配置的服务；或者你可以选择SearXNG（完全免费，支持自托管）。

### 这个工具的费用是多少？
- **免费 tier**：Serper每月2,500次查询；Tavily每月1,000次查询；Exa每月1,000次查询；
- **SearXNG**：完全免费（自托管时每月费用约5美元）；
- **付费计划**：费用因服务而异，通常每月10-50美元。

### SearXNG真的安全吗？
**如果选择自托管版本，确实非常安全**。你可以控制服务器，不会被追踪或分析用户数据；公共版本的安全性取决于服务提供商的政策。

### 如何设置SearXNG？
```bash
# Docker (5 minutes)
docker run -d -p 8080:8080 searxng/searxng
```
在`settings.yml`文件中启用JSON API功能。详情请参考[docs.searxng.org](https://docs.searxng.org/admin/installation.html)。

### 为什么我的查询被错误地路由到了其他服务？
有时查询内容可能比较模糊。可以使用`--explain-routing`参数查看路由逻辑；如需手动指定服务，可使用`-p service`参数。

---

## 🔄 自动备用机制

如果某个服务出现故障（如请求次数限制、超时或错误），系统会自动尝试下一个服务。此时，响应中会显示`routing.fallback_used: true`。

---

## 📤 输出格式

```json
{
  "provider": "serper",
  "query": "iPhone 16 price",
  "results": [{"title": "...", "url": "...", "snippet": "...", "score": 0.95}],
  "routing": {
    "auto_routed": true,
    "provider": "serper",
    "confidence": 0.78,
    "confidence_level": "high"
  }
}
```

---

## ⚠️ 重要提示

**Tavily、Serper和Exa并非OpenClaw的核心服务。**

❌ 不要修改`~/.openclaw/openclaw.json`文件来配置这些服务；
✅ 请使用该工具提供的脚本，API密钥会自动从`.env`文件中加载。

---

## 📚 更多文档

- **[FAQ.md]** — 更多问题的详细解答
- **[TROUBLESHOOTING.md]** — 常见问题的解决方法
- **[README.md]** — 完整的技术文档

---

## 🔗 快速链接

- [Serper](https://serper.dev) — Google搜索API
- [Tavily](https://tavily.com) — 人工智能研究搜索服务
- [Exa](https://exa.ai) — 神经搜索服务
- [You.com](https://api.you.com) — 基于RAG的实时搜索服务
- [SearXNG](https://docs.searxng.org) — 注重隐私的元搜索服务