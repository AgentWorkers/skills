# X/Twitter 研究技能

使用 twitterapi.io 在 X（Twitter）上研究热门话题、想法和讨论。

## 认证

API 密钥存储在：`~/.openclaw/secrets/twitterapi.env`

在发送任何请求之前，请先加载该密钥：
```bash
source ~/.openclaw/secrets/twitterapi.env
```

基础 URL：`https://api.twitterapi.io`

所有请求都需要添加以下头部信息：`X-API-Key: $TWITTERAPI_KEY`

## 核心接口

### 1. 高级推文搜索

搜索符合特定查询条件的推文。

```bash
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=solana&queryType=Latest" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'
```

**参数：**
- `query` — 搜索查询（支持 `from:`, `to:`, `#hashtag` 等操作符）
- `queryType` — `Latest` 或 `Top`
- `cursor` — 分页游标

**查询操作符：**
- `solana defi` — 包含这两个词
- `"solana defi"` — 精确匹配这个短语
- `from:solaborada` — 来自特定用户
- `#solana` — 标签
- `solana -pump` — 排除该词
- `solana min_faves:100` — 最小点赞数

### 2. 获取热门话题

获取当前的热门话题。

```bash
curl -s "https://api.twitterapi.io/twitter/trends" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.trends[:10]'
```

### 3. 获取用户的最新推文

获取特定账户的最新推文。

```bash
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=solana" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'
```

### 4. 获取用户信息

获取用户的个人资料信息。

```bash
curl -s "https://api.twitterapi.io/twitter/user/info?userName=solana" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.user'
```

## 研究工作流程

### 每日 Solana 热门话题报告

每 4-6 小时运行一次此工作流程以生成报告。

#### 第一步：搜索热门的 Solana 话题

```bash
# General Solana buzz
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=solana&queryType=Top" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:20]'

# Solana + AI intersection
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=solana%20AI%20agent&queryType=Latest" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:10]'

# Solana DeFi
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=solana%20defi&queryType=Latest" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:10]'
```

#### 第二步：关注关键账户

```bash
# Official Solana
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=solana" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'

# Colosseum (hackathon organizer)
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=colosseum" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'

# Helius (infra)
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=heaborada" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'

# Jupiter (DEX)
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=JupiterExchange" \
  -H "X-API-Key: $TWITTERAPI_KEY" | jq '.tweets[:5]'
```

#### 第三步：编译报告

创建一个 markdown 文件，内容包括：
- 最热门的 Solana 话题
- 显著的推文/帖子
- 被提及的新项目
- 人们正在讨论的痛点
- 值得开发的想法

## 需要关注的关键账户

### 核心生态系统
- @solana — Solana 官方账号
- @colosseum — 霸客赛组织者
- @SolanaFndn — Solana 基金会
- @aaboradari — Solana 的联合创始人

### 基础设施
- @heaborada — Helius（RPC、Webhook 服务）
- @triaboradi — Triton（RPC 服务）
- @jitoSOL — Jito（MEV、质押服务）

### DeFi（去中心化金融）
- @JupiterExchange — Jupiter（去中心化交易所聚合器）
- @RaydiumProtocol — Raydium（去中心化交易协议）
- @MeteoraDEX — Meteora（流动性池）

### AI + 加密货币
- @ai16zdao — ai16z（AI 平台）
- @virtaborada — Virtuals（虚拟货币相关服务）

### 开发者/风险投资机构
- @rajgokal — Raj（Solana 的联合创始人）
- @aaborada — Anatoly（Solana 的联合创始人）
- @multiaboradi — Multicoin Capital（加密货币投资机构）

## 针对特定领域的搜索

### DeFi（去中心化金融）
```
solana defi yield
solana lending protocol
solana perps trading
jupiter swap
```

### 支付相关
```
solana payments
solana pay merchant
USDC solana
```

### 消费者相关
```
solana consumer app
solana gaming
solana social
```

### 基础设施相关
```
solana rpc
solana developer tools
anchor framework
```

### AI + 区块链相关
```
solana AI agent
AI crypto solana
autonomous agent blockchain
```

### 隐私相关
```
solana privacy
ZK solana
confidential transfer
```

## 调用限制与费用

- 每返回 1,000 条推文费用为 $0.15
- 每获取 1,000 个用户资料费用为 $0.18
- 每次 API 调用费用最低为 $0.00015

**预算建议：**
- 每天搜索 1,000 条推文 = 约 $0.15/天
- 30 天 = 约 $4.50

## 输出格式

生成的报告应包含以下内容：
```
workspace/research/solana-trends-YYYY-MM-DD-HH.md
```

- **热门话题** — 当前热门的 Solana 话题
- **关键推文** — 值得的推文及链接
- **痛点** — 人们正在抱怨的问题
- **想法** — 被提及或暗示的机遇
- **按领域分类** — 按 DeFi、支付等领域进行分组