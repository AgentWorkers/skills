---
name: web-search-plus
version: 2.9.0
description: 统一搜索功能结合智能自动路由技术。通过多信号分析，能够自动在以下搜索引擎之间进行切换：Serper（谷歌）、Tavily（研究型搜索引擎）、Querit（多语言AI搜索引擎）、Exa（基于神经网络的搜索引擎）、Perplexity（AI问答平台）、You.com（实时问答系统）以及SearXNG（注重隐私保护的自主托管搜索引擎），并为用户提供相应的信心评分（即搜索结果的可靠性评估）。
tags: [search, web-search, serper, tavily, querit, exa, perplexity, you, searxng, google, multilingual-search, research, semantic-search, auto-routing, multi-provider, shopping, rag, free-tier, privacy, self-hosted, kilo]
metadata: {"openclaw":{"requires":{"bins":["python3","bash"],"env":{"SERPER_API_KEY":"optional","TAVILY_API_KEY":"optional","QUERIT_API_KEY":"optional","EXA_API_KEY":"optional","YOU_API_KEY":"optional","SEARXNG_INSTANCE_URL":"optional","KILOCODE_API_KEY":"optional — required for Perplexity provider (via Kilo Gateway)"},"note":"Only ONE provider key needed. All are optional."}}}
---
# Web Search Plus

**别再手动选择搜索服务了，让这个工具来帮你吧！**

这个工具可以连接7个搜索服务（Serper、Tavily、Querit、Exa、Perplexity、You.com、SearXNG），并自动为每个查询选择最合适的搜索服务。需要查找商品价格？→ 使用Google搜索结果。需要进行深度研究？→ 使用专业的研究引擎。想要直接获得带有引用信息的答案？→ 由AI生成。注重隐私保护？→ 可选择自托管版本。

---

## ✨ 这个工具的独特之处：

- **简单搜索**：无需考虑使用哪个搜索服务
- **智能路由**：自动分析你的查询并选择最佳的服务
- **7个服务，一个界面**：Google搜索结果、专业研究引擎、AI生成的答案（附带引用）、基于RAG（Retrieval, Aggregation, and Generation）的优化结果，以及注重隐私的保护功能，全部集成在一个工具中
- **只需一个API密钥**：可以先使用任意一个服务，之后再添加更多服务
- **免费选项可用**：SearXNG完全免费（支持自托管）

---

## 🚀 快速入门

```bash
# Interactive setup (recommended for first run)
python3 scripts/setup.py

# Or manual: copy config and add your keys
cp config.example.json config.json
```

向导会逐一介绍每个搜索服务，收集API密钥，并配置默认设置。

---

## 🔑 API密钥

你只需要**一个**密钥即可开始使用。之后可以根据需要添加更多服务以获得更全面的搜索体验。

| 服务 | 免费 tier | 适用场景 | 注册链接 |
|------|-----------|----------|---------|
| **Serper** | 每月2,500次查询 | 商品价格、本地信息、新闻 | [serper.dev](https://serper.dev) |
| **Tavily** | 每月1,000次查询 | 研究资料、解释性内容、学术搜索 | [tavily.com](https://tavily.com) |
| **Querit** | 需联系客服获取免费 tier 详情 | 多语言AI搜索、国际资讯 | [querit.ai](https://querit.ai) |
| **Exa** | 每月1,000次查询 | 类似X平台的搜索服务、初创企业信息、论文搜索 | [exa.ai](https://exa.ai) |
| **Perplexity** | 需通过Kilo平台使用 | 带有引用的直接答案 | [kilo.ai](https://kilo.ai) |
| **You.com** | 有限次数 | 实时信息、AI生成的上下文信息 | [api.you.com](https://api.you.com) |
| **SearXNG** | **完全免费** ✅ | 注重隐私保护、多源数据、零费用 | 支持自托管 |

**设置API密钥：**

```bash
# Option A: .env file (recommended)
export SERPER_API_KEY="your-key"
export TAVILY_API_KEY="your-key"
export QUERIT_API_KEY="your-key"

# Option B: config.json
{ "serper": { "api_key": "your-key" } }
```

---

## 🎯 何时使用哪个服务？

| 需要... | 服务 | 示例查询 |
|------|----------|---------------|
| 查找商品价格 | **Serper** | “iPhone 16 Pro Max的价格” |
| 查找附近的餐厅/商店 | **Serper** | “我附近的最佳披萨店” |
| 了解某事物的工作原理 | **Tavily** | “HTTPS加密的原理是什么” |
| 进行深度研究 | **Tavily** | “2024年的气候变化研究” |
| 跨语言搜索/获取国际资讯 | **Querit** | “德国的最新AI政策动态” |
| 查找类似的公司 | **Exa** | “类似Notion的初创企业” |
| 查找研究论文 | **Exa** | “Transformer架构相关的论文” |
| 获得带有来源的直接答案 | **Perplexity** | “本周末柏林的活动安排” |
| 了解某事物的最新状态 | **Perplexity** | “以太坊升级的现状” |
| 获取实时信息 | **You.com** | “最新的AI法规新闻” |
| 在不被追踪的情况下进行搜索 | **SearXNG** | 任何查询，且完全私密 |

**小贴士：** 普通搜索即可！系统会自动选择最佳服务。如有需要，可以使用`-p 服务名`来指定搜索服务。**

---

## 🧠 自动路由的工作原理

该工具会分析你的查询内容，并自动选择最适合的搜索服务：

```bash
"iPhone 16 price"              → Serper (shopping keywords)
"how does quantum computing work" → Tavily (research question)
"latest AI policy updates in Germany" → Querit (multilingual + recency)
"companies like stripe.com"    → Exa (URL detected, similarity)
"events in Graz this weekend"  → Perplexity (local + direct answer)
"latest news on AI"            → You.com (real-time intent)
"search privately"             → SearXNG (privacy keywords)
```

**如果选错了服务怎么办？** 可通过以下命令进行手动覆盖：`python3 scripts/search.py -p tavily -q “你的查询内容”`

**查看路由逻辑：`python3 scripts/search.py --explain-routing -q “你的查询内容”`

---

## 📖 使用示例

### 推荐使用自动路由

```bash
python3 scripts/search.py -q "Tesla Model 3 price"
python3 scripts/search.py -q "explain machine learning"
python3 scripts/search.py -q "latest AI policy updates in Germany"
python3 scripts/search.py -q "startups like Figma"
```

### 强制使用特定服务

```bash
python3 scripts/search.py -p serper -q "weather Berlin"
python3 scripts/search.py -p tavily -q "quantum computing" --depth advanced
python3 scripts/search.py -p querit -q "latest AI policy updates in Germany"
python3 scripts/search.py -p exa --similar-url "https://stripe.com" --category company
python3 scripts/search.py -p you -q "breaking tech news" --include-news
python3 scripts/search.py -p searxng -q "linux distros" --engines "google,bing"
```

---

## ⚙ 配置设置

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

| 功能 | Serper | Tavily | Exa | Perplexity | You.com | SearXNG |
|---------|------:|:------:|:---:|:----------:|:-------:|:-------:|
| 搜索速度 | ⚡⚡⚡ | ⚡⚡ | ⚡⚡ | ⚡⚡ | ⚡⚡⚡ | ⚡⚡ |
| 直接提供答案 | ✗ | ✗ | ✗ | ✓✓ | ✗ | ✗ |
| 提供引用 | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| 事实准确性 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 语义理解能力 | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| 提供完整页面内容 | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 支持购物/本地搜索 | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ |
| 查找相似页面 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| 基于RAG的优化 | ✗ | ✓ | ✗ | ✗ | ✓✓ | ✗ |
| 注重隐私保护 | ✗ | ✗ | ✗ | ✗ | ✗ | ✓✓ |
| API费用 | $$ | $$ | $$ | 需通过Kilo平台 | $ | **免费** |

---

## ❓ 常见问题

### 所有服务都需要API密钥吗？
**不需要。** 只需要为你使用的服务获取密钥。建议从Serper开始使用，之后再添加其他服务。

### 应该从哪个服务开始使用？
**Serper**：搜索速度最快，免费 tier的查询次数最多（每月2,500次），且能很好地处理大多数查询。

### 如果免费查询次数用完了怎么办？
系统会自动切换到其他已配置的服务。或者你可以选择SearXNG（支持无限次查询且支持自托管）。

### 这个工具的费用是多少？
- **免费 tier**：Serper每月2,500次查询；Tavily每月1,000次查询；Exa每月1,000次查询，共计每月4,500次免费查询。
- **SearXNG**：完全免费（如果自己托管在VPS上，每月费用约为5美元）。
- **付费计划**：费用因服务而异，通常在每月10-50美元之间。

### SearXNG真的安全吗？
**如果自己托管的话，是非常安全的。** 你可以控制服务器，不会被追踪或收集个人数据。公开使用的SearXNG实例则受服务提供商政策的影响。

### 如何设置SearXNG？
```bash
# Docker (5 minutes)
docker run -d -p 8080:8080 searxng/searxng
```
在`settings.yml`文件中启用JSON API功能。详情请参考[docs.searxng.org](https://docs.searxng.org/admin/installation.html)。

### 为什么我的查询被路由到了错误的服务器？
有时查询内容比较模糊。可以使用`--explain-routing`选项查看原因，如有需要，可以使用`-p 服务名`来指定搜索服务。

---

## 🔄 自动回退机制

如果某个服务出现故障（如请求次数限制、超时或错误），系统会自动尝试下一个服务。在这种情况下，响应中会显示`routing.fallback_used: true`。

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

## ⚠ 重要提示

**Tavily、Serper和Exa并非OpenClaw的核心服务。**

❌ 不要修改`~/.openclaw/openclaw.json`文件来配置这些服务。
✅ 请使用该工具提供的脚本进行配置，密钥会自动从`.env`文件中加载。

---

## 🔒 安全性

**SearXNG的安全措施：**
- 仅允许使用`http`/`https`协议
- 阻止访问云服务相关的元数据端点（如169.254.169.254、metadata.google.internal）
- 解析域名并阻止访问私有/内部IP地址（如loopback、RFC1918、link-local、reserved等）
- 如果你选择在私有网络中托管SearXNG，可以设置`SEARXNG_ALLOW_PRIVATE=1`来启用额外的安全保护。

## 📚 更多文档

- **[FAQ.md]** — 更多问题的详细解答
- **[TROUBLESHOOTING.md]** — 常见问题的解决方法
- **[README.md]** — 完整的技术文档

---

## 🔗 快速链接

- [Serper](https://serper.dev) — Google搜索API
- [Tavily](https://tavily.com) — AI研究搜索服务
- [Exa](https://exa.ai) — 神经网络搜索服务
- [Perplexity](https://www.perplexity.ai) — 通过Kilo Gateway提供AI生成答案的服务
- [You.com](https://api.you.com) — 基于RAG技术的实时搜索服务
- [SearXNG](https://docs.searxng.org) — 注重隐私保护的元搜索服务