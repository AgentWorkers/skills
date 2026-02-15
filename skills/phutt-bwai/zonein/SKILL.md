---
name: zonein
version: 1.2.0
description: |
  Fetch live smart money signals from Polymarket and HyperLiquid via Zonein API.
  Use PROACTIVELY when user asks about:
  (1) Prediction market signals, whales, smart bettors
  (2) Crypto perp trading signals, long/short sentiment
  (3) Leaderboard, top traders, wallet tracking
  (4) Trading agents management
  (5) Market overview, crypto sentiment, smart money flow
  Always use the bundled script — never call the API with inline code.
homepage: https://zonein.xyz
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"],"env":["ZONEIN_API_KEY"]},"primaryEnv":"ZONEIN_API_KEY","files":["scripts/*"],"installer":{"instructions":"1. Go to https://app.zonein.xyz/pm\n2. Log in with your refcode\n3. Click 'Get API Key' button\n4. Copy the key and paste it below"}}}
---

# Zonein — 智能资金情报

使用随附的脚本，从 Polymarket 和 HyperLiquid 智能资金钱包获取实时交易情报。

## 设置（凭据）

### 获取您的 API 密钥

1. 访问 **https://app.zonein.xyz/pm**
2. 使用您的账户登录（注册需要推荐码）
3. 点击 **“获取 API 密钥”** 按钮
4. 复制您的 API 密钥（以 `zn_` 开头）

### 在 OpenClaw 中设置 API 密钥

**选项 A — Gateway 控制面板（推荐）：**
1. 打开您的 **OpenClaw Gateway 控制面板**
2. 在侧边栏中导航到 **`/skills`**
3. 在工作区技能中找到 **“zonein”**，然后点击 **“启用”**
4. 输入您的 `ZONEIN_API_KEY` 并保存

**选项 B — 环境变量：**
```bash
export ZONEIN_API_KEY="zn_your_key_here"
```

**选项 C — 脚本也会自动从 `~/.openclaw/openclaw.json` 中读取配置（skills.entries.zonein.apiKey）。**

## 命令

所有命令都使用随附的 Python 脚本。**请始终使用这些命令，切勿直接编写内联 API 调用。**

### 预测市场（Polymarket）

**智能资金信号**（Polymarket 上的顶级交易者正在押注的内容）：
```bash
python3 skills/zonein/scripts/zonein.py signals --limit 10
python3 skills/zonein/scripts/zonein.py signals --categories POLITICS,CRYPTO --limit 10
python3 skills/zonein/scripts/zonein.py signals --period MONTH --min-wallets 5
```

**排行榜**（按利润排名前后的交易者）：
```bash
python3 skills/zonein/scripts/zonein.py leaderboard --period WEEK --limit 10
python3 skills/zonein/scripts/zonein.py leaderboard --category POLITICS --period MONTH
```

**共识**（多个智能投资者达成一致的交易头寸）：
```bash
python3 skills/zonein/scripts/zonein.py consensus --min-bettors 5
```

**交易者资料**（按钱包地址）：
```bash
python3 skills/zonein/scripts/zonein.py trader 0x1234...
```

### Perp Trading（HyperLiquid）

**Perp 交易信号**（智能资金交易者的多头/空头交易行为）：
```bash
python3 skills/zonein/scripts/zonein.py perp-signals --limit 10
python3 skills/zonein/scripts/zonein.py perp-signals --min-wallets 5 --min-score 60
```

**顶级交易者**（HyperLiquid 的大型交易者钱包）：
```bash
python3 skills/zonein/scripts/zonein.py perp-traders --limit 10
python3 skills/zonein/scripts/zonein.py perp-traders --min-score 70 --categories swing_trading
```

**表现最佳的交易者**（按利润排名）：
```bash
python3 skills/zonein/scripts/zonein.py perp-top --period week --limit 5
```

**币种分布**（每种币种的多头与空头情况）：
```bash
python3 skills/zonein/scripts/zonein.py perp-coins
```

**类别与交易者详情**：
```bash
python3 skills/zonein/scripts/zonein.py perp-categories
python3 skills/zonein/scripts/zonein.py perp-trader 0xabc...
```

### 代理与状态

```bash
python3 skills/zonein/scripts/zonein.py agents
python3 skills/zonein/scripts/zonein.py status
```

## 快速参考

| 用户请求... | 命令 |
|-------------|---------|
| “市场情况如何？” | `signals --limit 5` + `perp-signals --limit 5` |
| “显示与政治相关的 Polymarket 信号” | `signals --categories POLITICS --limit 10` |
| “大型交易者在加密货币上有什么操作？” | `perp-signals --limit 10` |
| “本周的顶级 Polymarket 交易者” | `leaderboard --period WEEK --limit 10` |
| “哪些币种被智能资金持有多头？” | `perp-coins` |
| “本月表现最佳的 Perp 交易者” | `perp-top --period month --limit 10` |
| “跟踪钱包 0x...” | `trader 0x...` 或 `perp-trader 0x...` |
| “智能资金流向何处？” | `signals --limit 10` + `perp-signals --limit 10` + `perp-coins` |

## 操作流程

### 市场概览

当用户询问市场状况时，按以下顺序运行命令：
1. `signals --limit 5` — 获取顶级 Polymarket 信号
2. `perp-signals --limit 5` — 获取顶级 Perp 信号
3. `perp-coins` — 获取每种币种的多头/空头情绪
4. 总结：哪些市场存在强烈共识，哪些币种受到大型交易者的看涨/看跌影响

### 交易信号

1. 询问：需要预测市场信号、Perp 信号，还是两者都需要？
2. 运行相应的命令
3. 按共识强度排序显示顶级信号
4. 解释每个信号，例如：“排名前 100 的交易者都对‘比特币是否会达到 10 万美元？’表示同意——当前价格为 42 美元”

### 跟踪钱包

1. `trader <wallet>` — 查看 Polymarket 交易者资料
2. `perp-trader <address>` — 查看 HyperLiquid 交易者资料
3. 显示：交易者的表现、持仓情况、胜率

## 输出字段

### Polymarket 信号
- `direction` — 是（YES）或否（NO）
- `consensus` — 0 到 1（1 表示所有人意见一致）
- `total_wallets` — 持有该币种的智能交易者数量
- `best_rank` — 在排行榜中的最佳位置
- `cur_yes_price` / `cur_no_price` — 当前价格

### Perp 信号
- `coin` — 币种（BTC、ETH、SOL、HYPE...）
- `direction` — 多头（LONG）或空头（SHORT）
- `consensus` — 一致比例（0-1）
- `long_wallets` / `short_wallets` — 每一方的交易者数量
- `long_value` / `short_value` — 每一方的交易金额（单位：美元）
- `best_trader_score` — 信誉分数

### 时间段与类别
- **Polymarket 时间段：** 日（DAY）、周（WEEK）、月（MONTH）、全部（ALL）
- **Polymarket 类别：** 全部（ALL）、政治（POLITICS）、体育（SPORTS）、加密货币（CRYPTO）、文化（CULTURE）、经济（ECONOMICS）、科技（TECH）、金融（FINANCE）
- **Perp 时间段：** 日（DAY）、周（WEEK）、月（MONTH）

## 如何展示结果

### Polymarket 信号
```
🔮 [market_title]
Smart money says: [YES/NO] | Agreement: [X]%
[N] top traders holding | Best ranked: #[rank]
Current price: YES [price] / NO [price]
```

### Perp 信号
```
📊 $[COIN]
Smart money says: [LONG/SHORT] | Agreement: [X]%
[N] whale traders | Top score: [score]
Long: $[X] | Short: $[X]
```

## 重要提示

- 信号显示的是智能资金的行为，并不保证未来的结果
- 过去的业绩不能预测未来的结果
- 投资金额切勿超过您能够承受的损失
- 请始终使用随附的脚本，切勿使用 curl 或内联 Python 直接构建 API 调用。

## 外部端点

| URL | 发送的数据 |
|-----|-----------|
| `https://mcp.zonein.xyz/api/v1/*` | API 密钥（X-API-Key 标头）+ 查询参数 |

## 安全与隐私

- 只有您的 API 密钥会被发送到外部（发送到 mcp.zonein.xyz）
- 除 API 密钥外，不会发送任何个人数据
- 所有数据均为只读（脚本仅进行 GET 请求）

## 信任声明

使用此功能时，您的 API 密钥和查询参数将被发送到 https://mcp.zonein.xyz。只有在您信任 Zonein 的情况下才进行安装。

## 链接

- **控制面板：** https://app.zonein.xyz/pm/
- **Perp 控制面板：** https://app.zonein.xyz/perp/
- **API 文档：** https://mcp.zonein.xyz/docs