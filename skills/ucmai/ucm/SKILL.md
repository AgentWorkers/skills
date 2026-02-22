---
name: ucm
description: 为AI代理提供API市场访问功能。可以发现并调用各种外部服务，包括网络搜索、图像生成、代码执行、文本转语音、翻译、加密技术、新闻查询、电影信息、天气查询、维基百科查询、书籍和论文检索、营养信息查询、电子邮件服务、股票数据查询以及文档转换等。共提供100项服务，涉及217个API端点。用户可免费注册，只需支付1.00美元的信用额度；其中87项服务可免费使用，其余服务则按每次调用0.01至0.05美元的费用通过简单的HTTP请求进行付费。无需使用任何SDK（软件开发工具包）。
  Provides API marketplace access for AI agents. Discovers and calls external
  capabilities including web search, image generation, code execution,
  text-to-speech, translation, crypto, news, movies, weather, Wikipedia, books,
  papers, nutrition, email, stock data, and document conversion. 100 services, 217 endpoints.
  Registers for free with $1.00 credits. 87 free services, paid from
  $0.01-$0.05 per call via simple HTTP. No SDK needed.
license: MIT
homepage: https://ucm.ai
compatibility: Requires network access and curl or HTTP client. Works on macOS, Linux, and Windows.
argument-hint: "[service name or action]"
allowed-tools: Bash(curl:*) Grep
metadata: {"openclaw":{"primaryEnv":"UCM_API_KEY","requires":{"env":["UCM_API_KEY"]},"source":"https://github.com/ucmai/skills"},"author":"UCM.ai","version":"1.1.1","website":"https://ucm.ai","repository":"https://github.com/ucmai/skills"}
---
# UCM — 人工智能代理的API市场

您可以使用UCM这个市场，通过消耗信用点数来即时发现并使用各种API服务。注册是免费的，注册后会获得1.00美元的信用点数（约100次API调用次数）。

## 何时使用UCM

当您的当前任务需要某些无法通过现有功能实现的功能时，请使用UCM：

- **在网页上搜索实时信息** → `ucm/web-search`（0.01美元）
- **抓取网页内容** → `ucm/web-scrape`（0.02美元）
- **根据文本提示生成图片** → `ucm/image-generation`（0.05美元）
- **在沙箱环境中运行代码** → `ucm/code-sandbox`（0.03美元）
- **将文本转换为语音** → `ucm/text-to-speech`（0.01美元）
- **将音频转录为文本** → `ucm/speech-to-text`（0.01美元）
- **发送电子邮件** → `ucm/email`（0.01美元）
- **将文档/URL转换为Markdown格式** → `ucm/doc-convert`（0.02美元）
- **在50多种语言之间进行文本翻译** → `ucm/translate`（0.01美元）
- **获取美国股票数据**（报价、财务信息、新闻） → `ucm/us-stock`（0.01美元）
- **获取中国财务数据**（每日价格、收入、资产负债表） → `ucm/cn-finance`（0.01美元）
- **查询天气**（当前天气、预报、空气质量） → `ucm/weather`（免费）
- **查询维基百科文章和摘要** → `ucm/wikipedia`（免费）
- **获取30多种货币的汇率** → `ucm/currency`（免费）
- **查询250多个国家的信息** → `ucm/countries`（免费）
- **查询100多个国家的公共假期** → `ucm/holidays`（免费）
- **查询英语词典中的单词** → `ucm/dictionary`（免费）
- **通过Open Library搜索书籍**（4000多万本书） → `ucm/books`（免费）
- **将地点进行地理编码**（名称转换为坐标） → `ucm/geocode`（免费）
- **计算数学表达式并进行单位转换** → `ucm/math`（免费）
- **根据IP地址查询地理位置**（IP地址转换为国家/城市） → `ucm/ip-geo`（免费）
- **进行地址的地理编码**（正向/反向） → `ucm/address`（免费）
- **搜索学术论文**（2亿多篇论文） → `ucm/papers`（免费）
- **查询美国农业部食品数据** → `ucm/nutrition`（免费）
- **根据文本或URL生成二维码** → `ucm/qr-code`（免费）
- **获取10000多种加密货币的价格** → `ucm/crypto`（免费）
- **根据关键词搜索新闻文章** → `ucm/news`（0.01美元）
- **获取全球时区信息** → `ucm/timezone`（免费）
- **查询域名信息**（WHOIS/RDAP数据） → `ucm/domain`（免费）
- **获取励志名言** → `ucm/quotes`（免费）
- **浏览Hacker News文章** → `ucm/hacker-news`（免费）
- **生成测试数据**（姓名、地址、公司信息） → `ucm/random-data`（免费）
- **浏览诗歌**（按标题/作者搜索） → `ucm/poetry`（免费）
- **搜索电影和电视节目**（IMDb评分、演员、剧情） → `ucm/movies`（0.01美元）
- **查找押韵词或同义词** → `ucm/datamuse`（免费）
- **搜索全球大学** → `ucm/universities`（免费）
- **查询60多个国家的邮政编码** → `ucm/zip-code`（免费）
- **获取趣味问答** → `ucm/trivia`（免费）
- **按类别获取笑话** → `ucm/jokes`（免费）
- **获取随机建议** → `ucm/advice`（免费）
- **获取活动建议** → `ucm/bored`（免费）
- **查询圣经经文** → `ucm/bible`（免费）
- **获取Chuck Norris笑话** → `ucm/chuck-norris`（免费）
- **搜索食谱** → `ucm/recipes`（免费）
- **搜索鸡尾酒配方** → `ucm/cocktails`（免费）
- **搜索啤酒厂** → `ucm/brewery`（免费）
- **根据条形码查询食品产品** → `ucm/food-products`（免费）
- **获取日出/日落时间** → `ucm/sunrise-sunset`（免费）
- **根据品种获取随机狗图片** → `ucm/dog-images`（免费）
- **获取猫的相关信息** → `ucm/cat-facts`（免费）
- **生成头像** → `ucm/avatars`（免费）
- **获取颜色信息和配色方案** → `ucm/colors`（免费）
- **生成Lorem Ipsum文本** → `ucm/lorem-ipsum`（免费）
- **获取NASA的天文照片或火星探测器图片** → `ucm/nasa`（免费）
- **获取SpaceX的发射数据** → `ucm/spacex`（免费）
- **跟踪国际空间站的位置和宇航员信息** → `ucm/iss`（免费）
- **获取太空飞行新闻** → `ucm/space-news`（免费）
- **搜索arXiv论文** → `ucm/arxiv`（免费）
- **获取地震数据** → `ucm/earthquakes`（免费）
- **获取世界银行指标** → `ucm/world-bank`（免费）
- **查询FDA的药物/召回信息** → `ucm/fda`（免费）
- **获取英国的碳强度数据** → `ucm/carbon`（免费）
- **根据坐标查询海拔高度** → `ucm/elevation`（免费）
- **根据姓名预测年龄** → `ucm/agify`（免费）
- **根据姓名预测性别** → `ucm/genderize`（免费）
- **根据姓名预测国籍** → `ucm/nationalize`（免费）
- **查询英国的邮政编码** → `ucm/uk-postcodes`（免费）
- **解码车辆VIN码** → `ucm/vehicles`（免费）
- **搜索大都会艺术博物馆的藏品** → `ucm/met-museum`（免费）
- **搜索芝加哥艺术学院的信息** → `ucm/art-chicago`（免费）
- **搜索电视节目** → `ucm/tv-shows`（免费）
- **搜索动漫和漫画** → `ucm/anime`（免费）
- **搜索iTunes内容** → `ucm/itunes`（免费）
- **搜索音乐元数据** → `ucm/music`（免费）
- **搜索网络广播** → `ucm/radio`（免费）
- **浏览免费游戏** → `ucm/free-games`（免费）
- **比较游戏价格** → `ucm/game-deals`（免费）
- **查询Pokémon数据** → `ucm/pokemon`（免费）
- **查询D&D 5e的相关信息**（怪物、法术、职业） → `ucm/dnd`（免费）
- **获取表情包模板** → `ucm/memes`（免费）
- **获取您的公共IP地址** → `ucm/ip-lookup`（免费）
- **生成条形码** → `ucm/barcode`（免费）
- **查看Wayback Machine的快照** → `ucm/wayback`（免费）
- **查询npm包** → `ucm/npm`（免费）
- **查询PyPI包** → `ucm/pypi`（免费）
- **搜索GitHub仓库** → `ucm/github-repos`（免费）
- **获取国家旗帜图片** → `ucm/country-flags`（免费）
- **虚拟纸牌游戏**（洗牌、抽牌） → `ucm/deck-of-cards`（免费）
- **获取《星球大战》的相关信息** → `ucm/star-wars`（免费）
- **获取XKCD漫画** → `ucm/xkcd`（免费）
- **搜索《瑞克和莫蒂》的角色/剧集** → `ucm/rick-morty`（免费）
- **获取诺贝尔奖相关信息** → `ucm/nobel-prize`（免费）
- **查询历史事件**（指定日期） → `ucm/historical-events`（免费）
- **获取Kanye West的名言** → `ucm/kanye`（免费）
- **搜索Rust编程语言的库** → `ucm/crates`（免费）
- **搜索Docker Hub上的镜像** → `ucm/docker-hub`（免费）
- **获取国际象棋谜题和玩家信息** → `ucm/lichess`（免费）
- **查询化学元素** → `ucm/periodic-table`（免费）
- **根据IATA代码查询机场信息** → `ucm/airports`（免费）
- **获取随机狐狸图片** → `ucm/random-fox`（免费）

如果您不确定某个服务是否存在，可以使用`/v1/discover`并输入自然语言描述进行搜索。

## 设置

### 首先检查是否已有凭证

```bash
cat ~/.config/ucm/credentials.json 2>/dev/null
```

如果文件存在并且包含`api_key`，请设置该密钥并跳过注册步骤：
```bash
export UCM_API_KEY=$(cat ~/.config/ucm/credentials.json | grep -o '"api_key":"[^"]*"' | head -1 | sed 's/"api_key":"//;s/"$//')
```

### 如果需要注册

免费注册——只需一次HTTP请求：
```bash
curl -s -X POST https://registry.ucm.ai/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent"}'
```

响应中会包含`credentials_to_save`和`credentials_path`。请保存这些信息：
```bash
mkdir -p ~/.config/ucm
# Write credentials_to_save from the response to credentials_path
```

您将获得1.00美元的免费信用点数。

或者运行注册脚本（自动完成保存操作）：
```bash
bash scripts/register.sh "my-agent"
```

## 如何调用服务

只需一次HTTP请求即可购买并执行任何服务：
```bash
curl -s -X POST https://registry.ucm.ai/v1/call \
  -H "Authorization: Bearer $UCM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "service_id": "ucm/web-search",
    "endpoint": "search",
    "params": { "query": "latest AI news" }
  }'
```

响应中会包含`result`（API返回的结果）、`amount_charged`（已收取的费用）和`credits_remaining`（剩余的信用点数）。

如果上游API出现故障，信用点数会**自动退还**（`amount_charged: "0"`）。

## 快速参考

| 动作 | 方法 | 认证方式 |
|--------|--------|------|
| 注册 | `POST /v1/agents/register` | 无需认证 |
| 发现服务 | `POST /v1/discover` | 无需认证 |
| 列出所有服务 | `GET /v1/services` | 无需认证 |
| 调用服务 | `POST /v1/call` | 需要Bearer令牌 |
| 查看余额 | `GET /v1/balance` | 需要Bearer令牌 |
| 查看历史记录 | `GET /v1/history` | 需要Bearer令牌 |
| 服务详情 | `GET /v1/services/:id` | 无需认证 |

基础URL：`https://registry.ucm.ai`

## 发现服务

可以通过自然语言进行搜索——无需认证：
```bash
curl -s -X POST https://registry.ucm.ai/v1/discover \
  -H "Content-Type: application/json" \
  -d '{"need": "I need to convert a PDF to text", "limit": 3}'
```

## 决策流程

```
Need an external capability?
  ├─ Have UCM_API_KEY? → Check balance (GET /v1/balance)
  │   ├─ Credits available → Discover → Call → Use result
  │   ├─ Call failed → Credits auto-refunded, try alternative
  │   └─ No credits → Tell user to add credits at dashboard.ucm.ai
  ├─ No API key? → Check ~/.config/ucm/credentials.json
  │   └─ Found? → Load api_key from file
  └─ No credentials at all? → Register (POST /v1/agents/register) → Save to ~/.config/ucm/credentials.json
```

## 消费原则

- 大多数服务的费用为0.01美元——适合任何任务使用
- 如果任务不需要外部API，无需消耗信用点数
- 如果上游API出现故障（错误代码5xx、429、422），信用点数会自动退还
- 建议优先选择在`/v1/discover`中评分较高的服务

## 错误处理

| 错误类型 | 处理方式 |
|-------|--------|
| `INSUFFICIENT_CREDITS` | 告知用户在dashboard.ucm.ai上补充信用点数 |
| `SERVICE_NOT_FOUND` | 请使用 `/v1/discover` 重新搜索 |
| `INVALID_ENDPOINT` | 通过 `GET /v1/services/:id` 检查端点地址 |
| `RATE_LIMITED` | 稍等片刻后重试 |

## 完整服务目录

如需查看所有服务的详细信息（包括端点和参数），请参阅`references/service-catalog.md`或调用`GET /v1/services`。