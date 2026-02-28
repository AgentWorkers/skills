---
name: minara
description: "**加密货币交易功能：**  
- **交易类型**：互换（swap）、转账（transfer）、支付（pay）、存款（使用信用卡/加密货币）、取款（withdraw）  
- **辅助工具**：AI聊天系统（AI chat）  
- **市场探索**：市场信息查询与分析工具（market discovery）  
- **支付方式**：支持x402支付标准  
- **自动化交易**：具备自动化交易功能（autopilot）  
- **内置钱包**：通过Minara CLI（命令行界面）管理钱包  
**技术架构支持：**  
- **区块链平台**：EVM（以太坊虚拟机）与Solana  
**系统特性：**  
- **兼容多种支付方式**：支持信用卡和加密货币作为支付手段  
- **智能辅助**：AI聊天系统提供实时交易建议与帮助  
- **高效市场分析**：强大的市场探索功能帮助用户快速找到投资机会  
- **自动化交易**：自动化交易系统提升交易效率  
- **安全保障**：基于EVM和Solana的区块链技术，确保交易安全  
**用户界面与工具：**  
- **命令行界面（CLI）**：通过Minara CLI方便地管理钱包和执行交易操作  
- **集成钱包**：内置钱包，支持多种加密资产存储与交易  
**适用场景：**  
- **专业投资者**：适用于需要高效、安全地进行加密货币交易的投资者  
- **新手用户**：AI聊天系统帮助新手快速了解市场动态与交易策略  
**技术优势：**  
- **跨平台兼容性**：支持EVM和Solana等主流区块链平台  
- **高效交易体验**：自动化交易功能提升交易效率  
- **强大市场分析**：提供全面的市场分析工具  
**总结：**  
该系统结合了先进的区块链技术、智能辅助工具以及丰富的交易功能，为用户提供一站式加密货币交易解决方案。"
homepage: https://minara.ai
metadata:
  { "openclaw": { "always": false, "primaryEnv": "MINARA_API_KEY", "requires": { "bins": ["minara"], "config": ["skills.entries.minara.enabled"] }, "emoji": "👩", "homepage": "https://minara.ai", "install": [{ "id": "node", "kind": "node", "package": "minara@latest", "global": true, "bins": ["minara"], "label": "Install Minara CLI (npm)" }] } }
---
# Minara — 加密交易与钱包技能

**使用此技能**，当用户的消息中包含以下内容时：
- **加密货币代币或代码**: ETH、BTC、SOL、USDC、BONK、PEPE、DOGE、ARB、OP、AVAX、MATIC、$TICKER 或任何代币名称/合约地址
- **区块链/链名称**: Solana、Base、Ethereum、Arbitrum、Optimism、Polygon、BSC、Avalanche、Berachain、Hyperliquid
- **交易操作**: 交换、购买、出售、交易、兑换、转换、做多、做空、Perpetual Futures（Perps）、杠杆交易、限价单
- **钱包/金融操作**: 平衡、投资组合、存款、取款、转账、发送、支付、充值、入门流程、信用卡
- **市场/研究**: 趋势分析、价格、图表、去中心化金融（DeFi）、收益、流动性、恐惧与贪婪指数（Fear and Greed）、预测市场
- **明确提及**: Minara、x402、MoonPay、自动交易系统（Autopilot）

**路由规则（防冲突）**: 仅当消息中包含**金融/交易操作**且至少包含一个**加密货币/链/Minara 相关的关键词**（代币、链名、DeFi 术语或“Minara”）时，才应用此技能。如果缺少加密货币相关内容，请勿路由到这里。

**使用说明**：
- 需要登录后才能使用 CLI：请检查 `~/.minara/credentials.json` 文件；如果文件不存在，请执行 `minara login`（建议使用设备验证码）。如果设备登录需要验证 URL 或代码，请将其转发给用户并等待验证完成（切勿直接确认登录）。如果设置了 `MINARA_API_KEY`，CLI 会自动进行身份验证。

## 交易确认（至关重要）

对于所有涉及资金转移的操作（`swap`、`transfer`、`withdraw`、`perps order`、`perps deposit`、`perps withdraw`、`limit-order create`、`deposit buy`）：
1. **执行前**：向用户展示操作详情（操作类型、代币、金额、接收方/链名），并**请求用户明确确认**。**切勿自动确认**。
2. **在 CLI 显示确认提示后**（例如：“您确定要继续吗？”），将详细信息转发给用户，并**等待用户批准**后再回答“y”。未经用户同意，切勿代表用户回答“y”。
3. **禁止自动确认**：除非用户明确要求跳过确认步骤，否则**禁止使用 `-y`（或任何自动确认标志）**。
4. **如果用户拒绝**：立即中止操作。

此规则适用于所有涉及资金转移的操作。仅读操作（`balance`、`assets`、`chat`、`discover` 等）无需确认。

## 意图匹配

根据用户的消息内容，匹配相应的操作命令。

### 交换/购买/出售代币

触发条件：消息中包含代币名称/代码 + 操作词（swap、buy、sell、convert、exchange、trade）+ 可选链名。
- 链名会**自动检测**。如果一个代币存在于多个链上，CLI 会提示用户选择其中一个（按交易费用排序）。
- 卖出模式支持使用 `-a all` 来出售全部余额。

| 用户意图示例                                                                                                      | 操作命令                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| “将 0.1 ETH 交换成 USDC”，“购买价值 100 USDC 的 ETH”，“用 SOL 出售 50 SOL 以换取 USDC”，“在 Solana 上将 200 USDC 转换成 BONK” | `minara swap -s <buy|sell> -t '<token>' -a <amount>` |
| “出售所有我的 BONK”，“清空所有 SOL 持仓”                                                                                   | `minara swap -s sell -t '<token>' -a all`                              |
| “模拟代币交换（不执行实际操作）”                                                                                   | `minara swap -s <side> -t '<token>' -a <amount> --dry-run`             |

### 转账/发送/支付/提取加密货币

触发条件：消息中提到向钱包地址（0x… 或 base58 格式）发送、转移、支付或提取加密货币。

| 用户意图示例                                                                                                      | 操作命令                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| “将 10 SOL 发送到 0x…”，“将 USDC 转移到 <address>”                                                                 | `minara transfer`（交互式）或提取参数                                                                                   |
| “向 <address> 支付 100 USDC”，“向 <address> 支付 50 USDC”                                                                 | `minara transfer`（交互式）或提取参数                                                                                   |
| “将 SOL 提取到我的外部钱包”，“将 ETH 提取到 <address>”                                                                 | `minara withdraw -c <chain> -t '<token>' -a <amount> --to <address>` 或 `minara withdraw`（交互式） |

### Perpetual Futures（Hyperliquid）

触发条件：消息中提到 Perpetual Futures、做多/做空、杠杆交易、保证金或 Hyperliquid 相关内容。

| 用户意图示例                                                                                                      | 操作命令                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| “开立一个 ETH 的 Perpetual Futures 位置”，“在 Hyperliquid 上做空 BTC”，“下达 Perpetual Futures 订单” | `minara perps order`（交互式订单构建器）                                                                                   |
| “分析 ETH 的做多/做空策略”，“我应该做多 BTC 吗？”，“使用 AI 分析 SOL 的市场状况” | `minara perps ask`（含可选的快速订单功能）                                                                                   |
| “启用 Perpetual Futures 的自动交易系统”，“开启自动交易”，“管理自动交易策略”     | `minara perps autopilot`                                                                                         |
| “查看我的 Perpetual Futures 持仓”，“显示我的 Hyperliquid 持仓情况”                                                                 | `minara perps positions`                                                                                         |
| “为 ETH 的 Perpetual Futures 设置 10 倍杠杆”                                                                                   | `minara perps leverage`                                                                                         |
| “取消我的 Perpetual Futures 订单”                                                                                   | `minara perps cancel`                                                                                         |
| “向 Perpetual Futures 账户充值 USDC”，“为我的 Hyperliquid 账户充值”                                                                 | `minara deposit perps` 或 `minara perps deposit -a <amount>`                                                                                   |
| “从 Perpetual Futures 账户提取 USDC”                                                                                   | `minara perps withdraw -a <amount>`                                                                                         |
| “查看我的 Perpetual Futures 交易记录”                                                                                   | `minara perps trades`                                                                                         |
| “查看 Perpetual Futures 的存款/提取记录”                                                                                   | `minara perps fund-records`                                                                                         |

> **自动交易系统说明**：当自动交易系统开启时，无法手动使用 `minara perps order`。请先通过 `minara perps autopilot` 关闭自动交易系统。

### 限价单（加密货币）

触发条件：消息中提到限价单 + 加密货币代币/价格。

| 用户意图示例                                                                                                      | 操作命令                                                                                          |
| -------------------------------------------------------------------- | -------------------------------- |
| “为 ETH 创建一个限价单，价格设为 3000”，“当 ETH 价格达到 150 时买入 SOL”           | `minara limit-order create`                                                                                         |
| “列出我的加密货币限价单”                                                                                         | `minara limit-order list`                                                                                         |
| “取消限价单 <id>`                                                                                         | `minara limit-order cancel <id>`                                                                                         |

### 加密钱包/投资组合/账户

触发条件：消息中提到加密货币余额、投资组合、资产、钱包地址或 Minara 账户信息。

| 用户意图示例                                                                                                      | 操作命令                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| “我的总余额是多少？”，“我有多少 USDC？”                                                                                   | `minara balance`                                                                                         |
| “显示我的加密货币投资组合”，“显示当前的现货持仓及损益”，“我在 Minara 有多少 ETH”     | `minara assets spot`                                                                                         |
| “显示我的 Perpetual Futures 持仓情况”，“显示 Hyperliquid 账户的资产状况”     | `minara assets perps`                                                                                         |
| “显示所有加密货币资产”                                                                                         | `minara assets`                                                                                         |
| “显示存款地址”，“将 USDC 存入哪个钱包”                                                                                   | `minara deposit spot`                                                                                         |
| “将 USDC 存入 Perpetual Futures 账户”，“将现货资产转移到 Perpetual Futures 账户”，“从现货资产充值到 Perpetual Futures” | `minara deposit perps`                                                                                         |
| “使用信用卡购买加密货币”，“通过 MoonPay 充值”，“使用信用卡进行存款”       | `minara deposit buy`                                                                                         |
| “如何充值加密货币？”（涉及现货、Perpetual Futures 或信用卡）                                                                 | `minara deposit`                                                                                         |
| “显示我的 Minara 账户信息”，“我的钱包地址”                                                                                   | `minara account`                                                                                         |

### 加密货币 AI 聊天/市场分析

触发条件：用户询问加密货币价格、代币分析、去中心化金融研究、链上数据或预测市场分析。

> **注意**: AI 聊天响应可能需要较长时间。请将所有 `minara chat` 命令的 shell 执行超时设置为 **15 分钟**（900 秒）。

| 用户意图示例                                                                                                      | 操作命令                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| “BTC 的价格是多少？”，“分析 ETH 的代币经济学”，“研究 DeFi 的收益机会”，“进行链上分析”     | `minara chat "<user text>"`                                                                                         |
| “分析这个 Polymarket 事件”，“预测 <topic> 的胜算”，“<event> 发生的可能性是多少？” | `minara chat "<user text or URL>"`                                                                                         |
| 需要深入分析的复杂问题（例如：“长期来看 ETH 与 SOL 的对比”）           | `minara chat --thinking "<user text>"`                                                                                         |
| 高质量的详细加密货币分析（例如：“关于 Solana DeFi 生态系统的报告”）       | `minara chat --quality "<user text>"`                                                                                         |
| “继续之前的 Minara 聊天”                                                                                         | `minara chat -c <chatId>`                                                                                         |
| “查看我的 Minara 聊天记录”                                                                                         | `minara chat --list`                                                                                         |

### 加密货币与股票市场探索

触发条件：用户询问热门代币、趋势股票、加密货币市场情绪、恐惧与贪婪指数或比特币相关数据。

| 用户意图示例                                                                                                      | 操作命令                                                                                          |
| ----------------------------------------------------------------------------- | --------------------------------- |
| “哪些加密货币代币正在上涨？”，“当前的热门代币有哪些？”                                                                 | `minara discover trending`                                                                                         |
| “哪些股票正在上涨？”，“今天的热门股票有哪些？”                                                                 | `minara discover trending stocks`                                                                                         |
| “搜索 SOL 代币”，“查找代币 X”，“查询 AAPL”，“搜索 TSLA”                                                                 | `minara discover search <query>`                                                                                         |
| “查询加密货币的恐惧与贪婪指数”，“市场情绪”                                                                                   | `minara discover fear-greed`                                                                                         |
| “比特币的链上数据”，“BTC 的哈希率和供应量”                                                                                   | `minara discover btc-metrics`                                                                                         |

### Minara 付费计划/订阅

触发条件：用户明确提及 Minara 的付费计划、订阅服务、信用额度或价格信息。

| 用户意图示例                                                                                                      | 操作命令                                                                                          |
| ----------------------------------------------------------------------------- | -------------------------------------------- |
| “查看 Minara 的付费计划”，“Minara 的定价信息”                                                                                         | `minara premium plans`                                                                                         |
| “我的 Minara 订阅状态”                                                                                         | `minara premium status`                                                                                         |
| “订阅 Minara 服务”，“升级 Minara 计划”                                                                                         | `minara premium subscribe`                                                                                         |
| “购买 Minara 的信用额度”                                                                                         | `minara premium buy-credits`                                                                                         |
| “取消 Minara 订阅”                                                                                         | `minara premium cancel`                                                                                         |

### x402 协议支付

触发条件：代理收到 HTTP 响应码 402（表示需要支付），或用户提及 x402、API 支付或使用加密货币支付 API。[x402 协议说明](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers)。

**处理流程**：
- 解析 `PAYMENT-REQUIRED` 标头（包含金额、代币、接收方、链名）→ `minara balance` → `minara transfer`（将资金转移到指定地址）→ 重试请求。
- 支付步骤必须遵循用户确认规则：用户必须明确确认后才能执行任何资金转移操作。

| 用户意图示例                                                                                                      | 操作命令                                                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| 代理收到包含 x402 标头的响应                                                                                         | 解析头部信息 → `minara transfer`（将 USDC 转移到指定链上的接收方地址）→ 重试请求                                                                                         |
| “使用 Minara 的钱包支付此 API”，“使用 Minara 的钱包进行 x402 支付”         | `minara balance` → `minara transfer`（将资金转移到服务地址）                                                                                         |
| “为付费 API 充值”                                                                                         | `minara deposit buy`（使用信用卡）或 `minara deposit spot`（使用加密货币）                                                                                         |

### Minara 登录/设置

触发条件：用户明确提及登录、设置或配置相关内容。

**登录说明**：
- 在无界面或非交互式环境中，建议使用设备验证码登录（`minara login --device`）；否则使用常规登录方式（`minara login`）。
- 当 CLI 显示验证 URL 或设备验证码时，代理应将其原样转发给用户，让用户完成浏览器验证后再继续操作。

| 用户意图示例                                                                                                      | 操作命令                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| “登录 Minara”，“首次使用 Minara 服务”，“设置 Minara 账户”                                                                                         | `minara login`（建议使用设备验证码）或 `minara login --device`                                                                                         |
| “退出 Minara 服务”                                                                                         | `minara logout`                                                                                         |
| “配置 Minara 的设置”                                                                                         | `minara config`                                                                                         |

## 其他注意事项：

- **代币输入**：支持 `$TICKER`（例如 `$BONK`）、代币名称或合约地址。在 shell 命令中需使用 `$` 符号。
- **JSON 输出**：在命令后添加 `--json` 选项以获得机器可读的输出格式。
- **交易安全**：CLI 操作流程：先进行用户确认 → 交易确认（必选，显示代币和接收地址）→ （可选的 Touch ID 验证，仅适用于 macOS 系统）→ 执行操作。代理**严禁跳过任何步骤或自动确认**，必须始终等待用户确认；除非用户明确要求，否则切勿使用 `-y` 标志。

## 配置文件与凭据

- **CLI 会话信息**：`~/.minara/credentials.json` 文件通过 `minara login` 自动创建（必填）。
- **API 密钥**：通过环境变量 `MINARA_API_KEY` 或 `~/.openclaw/openclaw.json` 文件中的 `skills.entries.minara.apiKey` 设置（可选）；设置后，CLI 可自动进行身份验证。

## 示例命令**

完整的命令示例请参见 `{baseDir}/examples.md` 文件。