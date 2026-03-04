---
name: kryptogo-meme-trader
version: "2.5.6"
description: 使用 KryptoGO 的链上集群分析平台来分析和交易模因币（meme coins）。该平台支持钱包聚类（wallet clustering）、地址标签（address labels）的识别、资金积累/分配情况的检测，以及通过代理交易 API（Agent Trading API）实现自动化交易执行。
author: KryptoGO
license: MIT
homepage: https://www.kryptogo.xyz
docs:
  user_guide:
    en: https://kryptogo.notion.site/Product-Guide-EN-26c3499de8a28179aafacb68304458ea
    zh-tw: https://kryptogo.notion.site/kryptogo-xyz-usage-guide
    zh-cn: https://kryptogo.notion.site/kryptogo-xyz-productguide-zhcn
  whitepaper: https://wallet-static.kryptogo.com/public/whitepaper/kryptogo-xyz-whitepaper-v1.0.pdf
tags:
  - solana
  - trading
  - meme-coins
  - defi
  - agent-trading
  - on-chain-analysis
  - cluster-analysis
  - kryptogo
platform: solana
api_base: https://wallet-data.kryptogo.app
metadata:
  openclaw:
    requires:
      env:
        - KRYPTOGO_API_KEY
        - SOLANA_PRIVATE_KEY
        - SOLANA_WALLET_ADDRESS
      bins:
        - python3
        - pip
        - openclaw
      network:
        - wallet-data.kryptogo.app
      permissions:
        - filesystem:write:~/.openclaw/workspace/.env
        - filesystem:write:~/.openclaw/workspace/memory/
      runtime_installs:
        - "pip: solders, requests (installed by scripts/setup.py on first run)"
      primaryEnv: KRYPTOGO_API_KEY
    security:
      default_mode: supervised
      trade_confirmation: required_by_default
      autonomous_trading: opt_in
      credential_access: environment_variables_only
      credential_file_read: setup_script_only
      credential_file_read_note: "Only scripts/setup.py reads and writes ~/.openclaw/workspace/.env for initial keypair generation and address repair. All other scripts access credentials exclusively via pre-loaded environment variables."
      local_signing_only: true
---
# KryptoGO 蜜币交易代理技能

## 概述

该技能使 AI 代理能够通过 KryptoGO 平台 **分析并交易** 蜜币，结合了深度的链上集群分析与交易执行。

**分析**（支持多链：Solana、BSC、Base、Monad）：钱包集群分析、资金积累/分配检测、地址行为标签识别、全网范围内的资金积累信号（适用于 Pro/Alpha 级别用户）。

**交易**（仅限 Solana）：监控投资组合并跟踪盈亏（PnL），通过 DEX 代理执行交易，所有本地交易签名操作（私钥不会离开设备）。

**默认模式为监督模式**——所有交易都需要用户确认。如需开启自主交易模式，请参阅 `references/autonomous-trading.md`，了解相关设置与学习系统详情。

---

## 使用场景

- 用户请求分析 Solana/BSC/Base/Monad 上的蜜币或代币
- 用户请求买卖代币
- 用户请求扫描热门代币或市场机会
- 用户请求监控投资组合持仓或查看盈亏情况
- 通过 Cron 定时任务自动监控投资组合和扫描市场信号

## 不适用场景

- BTC/ETH/主要 L1 代币的宏观分析
- NFT 交易
- 跨链交易
- 非 DEX 平台的交易

---

## 设置流程

### 1. 获取 API 密钥

1. 访问 [kryptogo.xyz/account](https://www.kryptogo.xyz/account) 并创建 API 密钥
2. 将密钥添加到 `~/.openclaw/workspace/.env` 文件中：
   ```bash
   echo 'KRYPTOGO_API_KEY=sk_live_YOUR_KEY' >> ~/.openclaw/workspace/.env && chmod 600 ~/.openclaw/workspace/.env
   ```

> **请勿直接在聊天中输入 API 密钥**。务必通过 `.env` 文件来设置敏感信息。

### 2. 生成代理钱包

```bash
python3 scripts/setup.py
```

生成一个 Solana 密钥对，将其保存到 `.env` 文件中并设置权限为 600，然后打印出公钥以用于资金转移。

### 3. 为钱包充值

将 SOL 代币发送到代理的公钥地址（最低要求 0.1 SOL）。

### 安全规则

- **严禁** 在任何消息或 CLI 参数中打印或泄露私钥
- **严禁** 直接在聊天中接收敏感信息——请让用户通过 `.env` 文件设置密钥
- **严禁** 使用 `read` 命令读取 `.env` 文件中的内容——必须通过 `source` 命令加载配置信息
- 运行时脚本不能直接读取 `.env` 文件——所有配置信息只能通过环境变量获取，且必须由调用者预先加载（`source ~/.openclaw/workspace/.env`）
- **例外情况**：`scripts/setup.py` 脚本在初始密钥对生成和地址修复时需要读取和写入 `.env` 文件——这是唯一会修改配置文件的脚本
- 私钥仅在本地签名时存在于内存中——绝不会发送到任何服务器

---

## 认证

所有 API 请求都需要提供以下认证信息：`Authorization: Bearer sk_live_<48 hex chars>`

| 级别 | 每日 API 请求次数 | 交易费用 | 信号仪表盘 | KOL 寻找功能 |
|-------|-----------------|-------------|------------------|------------|
| 免费 | 100 次/天 | 1%          | 无               | 无         |
| Pro   | 1,000 次/天 | 0.5%        | 有              | 有        |
| Alpha | 5,000 次/天 | 0%          | 有              | 有        |

---

## 代理行为

### 会话初始化

在每次会话开始时（包括心跳请求和定时任务），代理必须在运行任何脚本之前加载配置信息：

```bash
source ~/.openclaw/workspace/.env
```

这是强制性的要求——脚本不能直接读取 `.env` 文件，所有配置信息都必须通过环境变量获取。

### 默认模式：监督模式

代理默认处于 **监督模式**：它会分析代币情况，提供交易建议，并在执行任何交易前等待用户确认。止损/止盈条件会报告给用户，但不会自动执行。

如需开启自主交易模式，请在设置中将 `require_trade_confirmation` 设置为 `false`。详情请参阅 `references/autonomous-trading.md`。

### 持久化（至关重要）

**交易完成后，代理必须立即执行以下操作：**
1. 将交易详情写入 `memory/trading-journal.json` 文件，状态设置为 "OPEN"
2. 包含以下信息：`token_symbol`（代币符号）、`token_address`（地址）、`entry_price`（入场价格）、`position_size_sol`（持仓规模，单位 SOL）、`tx_hash`（交易哈希）、`timestamp`（时间戳）

### 用户设置

用户设置保存在 `memory/trading-preferences.json` 文件中：

| 设置项 | 默认值 | 说明 |
|------------|---------|-------------|
| `max_position_size` | 0.1 SOL | 每次交易的最大持仓规模 |
| `max_open_positions` | 5 | 同时持有的最大开放仓位数量 |
| `max_daily_trades` | 20 | 每天的最大交易次数 |
| `stop_loss_pct` | 30% | 损失超过此比例时触发通知/卖出 |
| `take_profit pct` | 100% | 盈利超过此比例时触发通知/卖出 |
| `min_market_cap` | $500K | 跳过市值低于此值的代币 |
| `scan_count` | 10 | 每次扫描的热门代币数量 |
| `risk_tolerance` | "conservative" | "保守"（跳过中等风险）、"moderate"（询问中等风险）、"aggressive"（自动交易中等风险） |
| `require_tradeconfirmation` | true | 设置为 `false` 以启用自主交易模式 |
| `chains` | ["solana"] | 需要扫描的链 |

---

## 安全防护措施

### 交易限制（硬性上限）

| 限制 | 默认值 | 是否可修改？ |
|-------|---------|--------------------|
| 单次交易最大金额 | 0.1 SOL | 可通过 `max_position_size` 修改 |
| 同时持有的最大仓位数量 | 5 | 可通过 `max_open_positions` 修改 |
| 每天最大交易次数 | 20 | 可通过 `max_daily_trades` 修改 |
| 价格波动超过一定比例时中止交易 | >10% | 必须中止 |
| 价格波动超过一定比例时发出警告 | >5% | 必须发出警告 |

如果达到任何限制，代理必须立即停止交易并通知用户。

### 凭据隔离

该技能中的运行时脚本不能直接读取 `.env` 文件。所有配置信息只能通过环境变量获取，且必须由调用者预先加载（`source ~/.openclaw/workspace/.env`）。这确保了没有运行时脚本能够独立访问或泄露敏感信息。

**例外情况**：`scripts/setup.py` 脚本在初始密钥对生成和地址修复时需要读取和写入 `.env` 文件——这是唯一会修改配置文件的脚本，且仅在初始化或明确执行 `--force` 重新生成操作时运行。

---

## 自动监控（Cron 定时任务）

### 快速设置

```bash
# Supervised mode (default): analysis + notifications, no auto-execution
source ~/.openclaw/workspace/.env && bash scripts/cron-examples.sh setup-default

# Autonomous mode (opt-in): auto-buys and auto-sells
source ~/.openclaw/workspace/.env && bash scripts/cron-examples.sh setup-autonomous

# Remove all cron jobs
bash scripts/cron-examples.sh teardown
```

| 任务 | 定时间隔 | 默认行为 |
|-----|----------|---------|
| `stop-loss-tp` | 5 分钟 | 报告触发条件，但不自动卖出 |
| `discovery-scan` | 1 小时 | 分析并发送交易建议，但不自动买入 |

有关完整的 Cron 配置、手动设置、心跳任务替代方案和监控工作流程的详细信息，请参阅 `references/autonomous-trading.md`。

---

## 链上分析框架（7 步流程）

### 第 1 步：代币概览与市值过滤

`/token-overview?address=<mint>&chain_id=<id>` — 获取代币名称、价格、市值、持有者信息及风险等级。如果市值低于 `min_market_cap`，则跳过此步骤。

### 第 2 步：集群分析

`/analyze/<mint>?chain_id=<id>` — 分析钱包集群、主要持有者及元数据：
- 如果持有者占比 ≥30-35%，则认为该代币受控；
- 如果持有者占比 ≥50%，则存在高风险；
- 如果单个集群的持有者占比超过 50%，则可能存在欺诈风险（需谨慎处理）。

> **免费等级限制**：集群分析仅返回前 2 个集群。如需查看完整集群数据，请升级到 [kryptogo.xyz/pricing](https://www.kryptogo.xyz/pricing)。

### 第 3 步：集群趋势分析（多时间框架）

`/analyze-cluster-change/<mint>` — 分析 15 分钟/1 小时/4 小时/1 天/7 天内的集群变化情况。

关键判断依据：**价格与集群持有比例的走势**：
- 价格上涨且集群持有比例下降 = 市场看跌；
- 价格下跌且集群持有比例上升 = 市场看涨。

### 第 4 步：地址标签验证及卖出压力检测

1. 使用 `/token-wallet-labels` 查看开发者/狙击手/批量交易者的钱包；
2. 使用 `/balance-history` 检查每个高风险地址的持有情况；
3. 计算 `risky_ratio`（高风险持仓占总持仓的比例）：
  - >30% = 高风险；
  - 10-30% = 中等风险；
  - <10% = 低风险。

> 标签仅代表历史行为，并不反映当前持有情况。务必通过 `/balance-history` 验证实际持有情况。

### 第 5 步：深入分析（可选）

使用 `/balance-history`、`/balance-increase/<mint>`、`/top-holders-snapshot/<mint>`、`/analyze-dca-limit-orders/<mint>`、`/cluster-wallet-connections` 进行进一步分析。

### 第 6 步：决策制定

根据 `references/decision-framework.md` 中提供的看涨/看跌判断标准做出决策。

### 第 7 步：执行交易

使用 `scripts/swap.py` 执行交易——该脚本负责处理钱包地址的注入、错误检查及交易日志记录。

```bash
source ~/.openclaw/workspace/.env && python3 scripts/swap.py <token_mint> 0.1
source ~/.openclaw/workspace/.env && python3 scripts/swap.py <token_mint> <amount> --sell
```

---

## API 快速参考

| API 端点 | 方法 | 功能 |
|----------|--------|---------|
| `/agent/account` | GET | 获取用户等级和每日使用额度 |
| `/agent/trending-tokens` | GET | 扫描热门代币 |
| `/agent/portfolio` | GET | 查看投资组合及盈亏情况 |
| `/agent/swap` | POST | 创建未签名的交易请求（仅限 Solana） |
| `/agent/submit` | POST | 提交已签名的交易请求（仅限 Solana） |
| `/token-overview` | GET | 获取代币元数据和市场信息 |
| `/analyze/:token_mint` | GET | 进行完整集群分析 |
| `/analyze-cluster-change/:token_mint` | GET | 查看集群持有比例变化 |
| `/balance-history` | POST | 提交时间序列余额数据 |
| `/wallet-labels` | POST | 设置钱包行为标签 |
| `/token-wallet-labels` | POST | 为特定代币设置标签 |
| `/signal-dashboard` | GET | 提供精选的积累信号（Pro+ 级别用户可用） |

> 完整的请求/响应格式详情请参阅 `references/api-reference.md`。

---

## 多链支持

| 链接 | chain_id | 分析功能 | 交易功能 |
|-------|----------|----------|---------|
| Solana | `501` | 支持 | 支持 |
| BSC | `56` | 支持 | 不支持 |
| Base | `8453` | 支持 | 不支持 |
| Monad | `143` | 支持 | 不支持 |

---

## 错误处理

| 错误代码 | 含义 | 处理方式 |
|------|---------|--------|
| 400 | 请求错误 | 检查参数是否正确 |
| 401 | 未经授权 | 请检查 API 密钥 |
| 402 | 使用额度超出 | 等待每日重置或升级 |
| 403 | 被禁止访问 | 需要更高权限等级 |
| 502/504 | 服务器错误 | 10 秒后重试一次 |

---

## 运行时脚本要求

所有脚本在运行前都需要预先加载配置信息：`source ~/.openclaw/workspace/.env`。

```bash
source ~/.openclaw/workspace/.env && bash scripts/portfolio.sh              # Portfolio check
source ~/.openclaw/workspace/.env && bash scripts/trending.sh               # Trending tokens
source ~/.openclaw/workspace/.env && bash scripts/analysis.sh               # Full analysis dashboard
source ~/.openclaw/workspace/.env && python3 scripts/swap.py <mint> 0.1     # Buy
source ~/.openclaw/workspace/.env && python3 scripts/swap.py <mint> <amt> --sell  # Sell
source ~/.openclaw/workspace/.env && bash scripts/test-api.sh               # API connectivity test
```

## 学习与优化

代理通过记录交易数据、分析结果并调整策略来不断提升性能。每次交易都会被记录到 `memory/trading-journal.json` 文件中，亏损情况会触发事后分析，定期评估会提出参数调整建议。

有关学习系统、交易日志格式、事后分析流程和策略调整的详细信息，请参阅 `references/autonomous-trading.md`。

---

## 核心概念

| 概念 | 关键要点 |
|---------|-------------|
| **集群** | 由同一实体控制的钱包集合 |
| **集群持有比例** | 集群持有的代币占总供应量的比例。≥30% 表示受控；≥50% 表示高风险 |
| **开发者** | 发布该代币的实体，通常具有最高风险 |
| **狙击手** | 在代币创建后 1 秒内买入的投资者；若未卖出则可能构成卖出压力 |
| **聪明资金** | 实现利润超过 $100K 的投资者；通常在价格波动前会有资金积累 |
| **资金积累** | 集群持有比例上升且价格稳定 = 市场看涨 |
| **资金分布** | 价格上升且集群持有比例下降 = 市场看跌 |

> 完整的概念说明请参阅 `references/concepts.md`。

---

## 最佳实践

1. 首先访问 `/agent/account` 以确认用户等级和每日使用额度；
2. 启动时务必查看 `/agent/portfolio` 以了解当前持仓情况；
3. 绝不要在日志、消息或 CLI 参数中暴露私钥；
4. 在提交交易前验证价格波动情况——超过 10% 时中止交易；超过 5% 时发出警告；
5. 及时签名并提交交易请求——区块哈希在 60 秒后失效；
6. 每次操作后都将状态信息保存到 `memory/trading-state.json` 文件；
7. 将所有交易记录到日志文件中，避免重复错误操作；
8. 在执行交易前请阅读 `memory/trading-lessons.md` 以了解常见错误模式。

---

## 文件结构

```
kryptogo-meme-trader/
├── SKILL.md                       ← You are here
├── package.json
├── .env.example
├── references/
│   ├── api-reference.md           ← Full API docs
│   ├── concepts.md                ← Core concepts
│   ├── decision-framework.md      ← Entry/exit strategies
│   └── autonomous-trading.md      ← Autonomous mode, cron, learning system
├── scripts/
│   ├── setup.py                   ← First-time setup
│   ├── cron-examples.sh           ← Cron configurations
│   ├── portfolio.sh / trending.sh / analysis.sh / test-api.sh
│   ├── swap.py                    ← Swap executor
│   └── trading-preferences.example.json
└── examples/
    ├── trading-workflow.py
    └── deep-analysis-workflow.py
```