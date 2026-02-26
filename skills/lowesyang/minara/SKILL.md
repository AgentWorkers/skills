---
name: minara
description: "加密货币交易功能包括：交换（swap）、转账（transfer）、支付（pay）、存款（支持信用卡或加密货币）、取款（withdraw）、AI聊天（AI chat）、市场探索（market discovery）、x402支付方式（x402 payment method）以及自动交易功能（autopilot）。内置钱包可通过Minara CLI进行管理。该平台支持EVM（以太坊虚拟机）和Solana区块链。"
homepage: https://minara.ai
metadata:
  { "openclaw": { "always": false, "primaryEnv": "MINARA_API_KEY", "requires": { "bins": ["minara"], "config": ["skills.entries.minara.enabled"] }, "emoji": "👩", "homepage": "https://minara.ai", "install": [{ "id": "node", "kind": "node", "package": "minara@latest", "global": true, "bins": ["minara"], "label": "Install Minara CLI (npm)" }] } }
---
# Minara — 加密交易与钱包技能

**使用此技能**，当用户消息中包含以下内容时：
- **加密代币或股票代码：** ETH、BTC、SOL、USDC、BONK、PEPE、DOGE、ARB、OP、AVAX、MATIC、$TICKER 或任何代币名称/合约地址
- **区块链/链名称：** Solana、Base、Ethereum、Arbitrum、Optimism、Polygon、BSC、Avalanche、Berachain、Hyperliquid
- **交易操作：** 交换、购买、出售、交易、兑换、转换、多头、空头、Perpetual Futures（永续合约）、杠杆、限价单
- **钱包/金融操作：** 平衡、投资组合、存款、取款、转账、发送、支付、充值
- **市场/研究：** 趋势分析、价格、图表、DeFi（去中心化金融）、收益、流动性、恐惧与贪婪指数、预测市场
- **明确提及：** Minara、minara、x402、MoonPay、自动交易
- **与加密货币相关的股票代码：** AAPL、TSLA、NVDAx、热门股票

**路由规则（防冲突）：** 仅当消息中包含**金融/交易操作** *且* 至少一个**加密/链/Minara 相关的关键词**（代币、链名称、DeFi 术语或“Minara”）时，才应用此技能。如果缺少加密相关内容，请勿路由到这里。

**使用说明：**
- 需要登录才能使用 CLI：请检查 `~/.minara/credentials.json`；如果文件不存在，请执行 `minara login`（建议使用设备验证码）。如果设备登录需要验证 URL 或代码，请将其转发给用户并等待验证完成（切勿直接确认登录成功）。
- 如果设置了 `MINARA_API_KEY`，CLI 会自动进行身份验证。

## 交易确认（至关重要）

对于所有涉及资金转移的操作（`swap`、`transfer`、`withdraw`、`perps order`、`perps deposit`、`perps withdraw`、`limit-order create`、`deposit buy`）：
1. **执行前：** 向用户展示操作详情（操作类型、代币、金额、接收方/链名称），并**请求用户明确确认**。**切勿自动确认**。
2. **CLI 返回确认提示后（例如：“您确定要继续吗？”）：将确认信息转发给用户，并**等待用户批准**后再回答“y”。未经用户同意，切勿代表用户回答“y”。
3. **禁止自动确认：** 除非用户明确要求跳过确认步骤，否则**严禁使用 `-y`（或任何自动确认标志）**。
4. **如果用户拒绝：** 立即终止操作。

此规则适用于所有涉及资金转移的操作。仅读操作（`balance`、`assets`、`chat`、`discover` 等）无需确认。

## 意图匹配

根据用户消息内容，匹配相应的操作命令。

### 交换/购买/出售代币

**触发条件：** 消息中包含代币名称/代码 + 操作词（swap、buy、sell、convert、exchange、trade）+ 可选链名称。
- 链名称会**自动检测**。如果一个代币存在于多个链上，CLI 会提示用户选择其中一个（按gas成本排序）。
- 卖出模式支持 `-a all` 以出售全部余额。

| 用户意图示例                                                                 | 操作命令                                                                 |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| “将 0.1 ETH 交换成 USDC”，“购买价值 100 USDC 的 ETH”，“用 SOL 出售 50 SOL 以换取 USDC”，“在 Solana 上将 200 USDC 转换成 BONK” | `minara swap -s <buy\|sell> -t '<token>' -a <amount>` |
| “出售所有我的 BONK”，“清空所有 SOL 持仓”                                                                 | `minara swap -s sell -t '<token>' -a all`                              |
| 模拟代币交换（不执行实际操作）                                                                                                                 | `minara swap -s <side> -t '<token>' -a <amount> --dry-run`             |

### 转账/发送/支付/提取加密货币

**触发条件：** 消息中提到向钱包地址（0x… 或 base58 格式）发送、转账或支付加密货币。

| 用户意图示例                                                                                                                   | 操作命令                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| “将 10 SOL 发送到 0x…”，“将 USDC 转账到 <address>”                                                                 | `minara transfer` （交互式）或提取参数                                                       |
| “向 <address> 支付 100 USDC”，“帮我向 <address> 支付 100 USDC”                                                                 | `minara transfer` （交互式）或提取参数                                                       |
| “将 SOL 提取到我的外部钱包”，“将 ETH 提取到 <address>”                                                                 | `minara withdraw -c <chain> -t '<token>' -a <amount> --to <address>` 或 `minara withdraw` （交互式） |

### 永续合约（Hyperliquid）

**触发条件：** 消息中提及 Perpetual Futures、杠杆、保证金或 Hyperliquid 相关术语。

| 用户意图示例                                                                 | 操作命令                                                                 |
| ------------------------------------------------------------------------- | ------------------------------------------------------------ |
| “开立一个 ETH 的多头永续合约”，“在 Hyperliquid 上做空 BTC”，“下达永续合约订单”                                                                 | `minara perps order` （交互式订单构建器）             |
| “分析 ETH 的多头或空头头寸”，“我应该做多 BTC 吗？”，“使用 AI 分析 SOL 的市场状况”                                                                 | `minara perps ask` — 提供 AI 分析及快速订单选项           |
| “启用永续合约的自动交易功能”，“开启自动交易”，“管理自动交易策略”                                                                 | `minara perps autopilot`                                     |
| “查看我的永续合约头寸”，“显示我的 Hyperliquid 头寸”                                                                 | `minara perps positions`                                     |
| “为 ETH 永续合约设置 10 倍杠杆”                                                                 | `minara perps leverage`                                      |
| “取消我的永续合约订单”                                                                 | `minara perps cancel`                                        |
| “向永续合约账户充值 USDC”，“为我的 Hyperliquid 账户充值”                                                                 | `minara deposit perps` 或 `minara perps deposit -a <amount>` |
| “从永续合约账户提取 USDC”                                                                 | `minara perps withdraw -a <amount>`                          |
| “查看我的永续合约交易记录”                                                                 | `minara perps trades`                                        |
| “查看永续合约的充值/提取记录”                                                                 | `minara perps fund-records`                                  |

> **自动交易注意事项：** 当自动交易功能开启时，手动下达 `minara perps order` 命令将被阻止。请先通过 `minara perps autopilot` 关闭自动交易功能。

### 限价单（加密货币）

**触发条件：** 消息中提及限价单 + 加密代币/价格。

| 用户意图示例                                                                 | 操作命令                                                                 |
| -------------------------------------------------------------------- | -------------------------------- |
| “为 ETH 创建一个限价单，价格设为 3000 美元”，“当 ETH 价格达到 150 美元时买入 SOL”                                                                 | `minara limit-order create`      |
| “列出我的所有加密货币限价单”                                                                 | `minara limit-order list`        |
| “取消限价单 <id>`                                                                 | `minara limit-order cancel <id>`                         |

### 加密钱包/投资组合/账户

**触发条件：** 消息中提及加密货币余额、投资组合、资产、钱包地址或 Minara 账户。

| 用户意图示例                                                                 | 操作命令                                                                 |
| ------------------------------------------------------------------------ | ---------------------- |
| “我的总余额是多少？”，“我有多少 USDC？”                                                                 | `minara balance`       |
| “显示我的加密货币投资组合”，“显示带有盈亏的现货持仓”，“我在 Minara 有多少 ETH？”                                                                 | `minara assets spot`   |
| “显示我的永续合约余额”，“显示 Hyperliquid 账户的资产状况”                                                                 | `minara assets perps`  |
| “显示所有加密货币资产”                                                                 | `minara assets`        |
| “显示存款地址”，“将 USDC 存入哪个钱包”                                                                 | `minara deposit spot`  |
| “将 USDC 存入永续合约账户”，“将 USDC 从现货账户转移到永续合约账户”，“从现货账户为永续合约账户充值”                                                                 | `minara deposit perps` |
| “使用信用卡购买加密货币”，“用信用卡充值”，“通过 MoonPay 充值”                                                                 | `minara deposit buy`   |
| “如何充值加密货币？”（涉及现货、永续合约或信用卡）                                                                 | `minara deposit`       |
| “显示我的 Minara 账户信息”，“我的钱包地址”                                                                 | `minara account`       |

### 加密货币 AI 聊天/市场分析

**触发条件：** 消息中询问加密货币价格、代币分析、DeFi 研究、链上数据或预测市场分析。

> **注意：** AI 聊天响应可能需要较长时间。对于所有 `minara chat` 命令，将 shell 执行超时设置为 **15 分钟**（900 秒）。

| 用户意图示例                                                                 | 操作命令                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| “BTC 的价格是多少？”，“分析 ETH 的代币经济学”，“DeFi 的收益机会”，“进行链上分析”                                                                 | `minara chat "<user text>"`            |
| “分析这个 Polymarket 事件”，“预测 <topic> 的市场概率”，“<事件> 发生的可能性是多少？”                                                                 | `minara chat "<user text or URL>"`     |
| 需要深入分析的复杂问题（例如：“长期来看 ETH 与 SOL 的对比”）                                                                 | `minara chat --thinking "<user text>"` |
| 高质量的详细加密货币分析（例如：“Solana DeFi 生态系统的详细报告”）                                                                 | `minara chat --quality "<user text>"`  |
| “继续之前的 Minara 聊天”                                                                                                 | `minara chat -c <chatId>`              |
| “查看我的 Minara 聊天记录”                                                                                                        | `minara chat --list`                   |

### 加密货币与股票市场探索

**触发条件：** 消息中提及热门代币、热门股票、加密货币市场情绪、恐惧与贪婪指数或比特币相关数据。

| 用户意图示例                                                                 | 操作命令                                                                 |
| ----------------------------------------------------------------------------- | --------------------------------- |
| “哪些加密货币代币正在上涨？”，“当前的热门代币有哪些？”                                                                 | `minara discover trending`        |
| “哪些股票正在上涨？”，“今天的热门股票有哪些？”                                                                 | `minara discover trending stocks` |
| “搜索 SOL 代币”，“查找代币 X”，“查询 AAPL”，“搜索 TSLA”                                                                 | `minara discover search <query>`  |
| “查询加密货币的恐惧与贪婪指数”，“市场情绪”                                                                 | `minara discover fear-greed`      |
| “比特币的链上数据”，“BTC 的哈希率和供应量”                                                                 | `minara discover btc-metrics`     |

### Minara 付费计划/订阅

**触发条件：** 消息中明确提及 Minara 的付费计划、订阅服务、信用额度或价格信息。

| 用户意图示例                                                                 | 操作命令                                                                 |
| ---------------------------------------------------------------------------- | ---------------------------- |
| “查看 Minara 的付费计划”，“Minara 的定价信息”                                                                 | `minara premium plans`       |
| “我的 Minara 订阅状态”                                                                 | `minara premium status`      |
| “订阅 Minara 服务”，“升级 Minara 订阅计划”                                                                 | `minara premium subscribe`   |
| “购买 Minara 的信用额度”                                                                 | `minara premium buy-credits`                         |
| “取消 Minara 订阅”                                                                 | `minara premium cancel`      |

### x402 协议支付

**触发条件：** 代理收到 HTTP 响应码 402（表示需要支付），或用户提及 x402、API 支付方式，或使用加密货币支付 API 访问费用。[x402 规范](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers)。

**处理流程：** 解析 `PAYMENT-REQUIRED` 头部信息（金额、代币、接收方、链名称），然后执行 `minara transfer` 进行支付；之后重试请求。

**支付注意事项：** 用户必须明确确认后才能执行任何资金转移操作。

| 用户意图示例                                                                 | 操作命令                                                                 |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| 代理收到包含 x402 头部的响应                                                                 | 解析头部信息 → 将 USDC 转账到指定链路的接收方 → 重试请求                                                                 |
| “使用 Minara 服务进行支付”，“使用 Minara 钱包支付 API 费用”                                                                 | `minara balance` → `minara transfer` 到服务地址                         |
| “为付费 API 充值”                                                                 | `minara deposit buy`（使用信用卡）或 `minara deposit spot`（使用加密货币）             |

### Minara 登录/设置

**触发条件：** 消息中提及 Minara 的登录、设置或配置相关内容。

**登录说明：** 在无界面或非交互式环境中，建议使用设备验证码登录（`minara login --device`）；否则使用常规登录方式（`minara login`）。
- **登录流程：** 当 CLI 显示验证 URL 或设备验证码时，代理应将其原样转发给用户，让用户完成浏览器验证，确认完成后再继续操作。

| 用户意图示例                                                                 | 操作命令                                                                 |
| --------------------------------------------------------------- | -------------------------------------------------------------- |
| “登录 Minara”，“首次使用 Minara 服务”，“配置 Minara 设置”                                                                 | `minara login`（建议使用设备验证码）或 `minara login --device` |
| “退出 Minara 服务”                                                                 | `minara logout`                                                |
| “配置 Minara 的设置”                                                                 | `minara config`                                                |

## 其他注意事项：

- **代币输入（`-t` 参数）：** 支持 `$TICKER`（例如 `$BONK`）、代币名称或合约地址。在 shell 命令中需使用 `$` 符号。
- **JSON 输出：** 在需要机器可读输出的命令后添加 `--json` 参数。
- **交易安全：** CLI 操作流程：先进行确认 → 交易确认（必经步骤，显示代币和接收方地址）→ （可选的 Touch ID 验证，仅限 macOS 系统）→ 执行操作。代理**严禁跳过任何步骤或自动确认**，必须始终等待用户确认；除非用户明确要求，否则不得使用 `-y` 参数。

## 配置文件与认证信息：

- **CLI 会话信息：** `~/.minara/credentials.json` — 通过 `minara login` 自动创建（必需文件）。
- **API 密钥：** 通过环境变量 `MINARA_API_KEY` 或 `~/.openclaw/openclaw.json` 中的 `skills.entries.minara.apiKey` 设置；如果已设置，CLI 会自动进行身份验证。

## 示例命令：**

完整命令示例请参考 `{baseDir}/examples.md` 文件。