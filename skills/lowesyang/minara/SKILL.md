---
name: minara
description: "**加密货币交易功能：**  
- 交易对换（swap）  
- 持证交易者（perps）  
- 资金转移（transfer）  
- 支付（支付方式包括信用卡/加密货币）  
- 存款（deposit，支持信用卡/加密货币）  
- 提取（withdraw）  
- 人工智能聊天支持（AI chat）  
- 市场探索功能（market discovery）  
- 支付方式支持X402标准  
- 自动交易功能（autopilot）  
- 内置钱包，可通过Minara CLI进行管理  
- 支持EVM（以太坊虚拟机）和Solana区块链平台。"
homepage: https://minara.ai
metadata:
  { "openclaw": { "always": false, "primaryEnv": "MINARA_API_KEY", "requires": { "bins": ["minara"], "config": ["skills.entries.minara.enabled"] }, "emoji": "👩", "homepage": "https://minara.ai", "install": [{ "id": "node", "kind": "node", "package": "minara@latest", "global": true, "bins": ["minara"], "label": "Install Minara CLI (npm)" }] } }
---
# Minara — 加密交易与钱包技能

## 安全提示：  
本文件仅用于文档说明（Markdown格式），不包含可执行代码、脚本或二进制文件。它用于指导AI代理如何调用Minara命令行界面（CLI）。

**在以下情况下使用此技能**：  
- 用户的消息中提及以下内容时：  
  - **加密代币或股票代码**：ETH、BTC、SOL、USDC、BONK、PEPE、DOGE、ARB、OP、AVAX、MATIC、$TICKER或任何代币名称/合约地址  
  - **区块链/链名称**：Solana、Base、Ethereum、Arbitrum、Optimism、Polygon、BSC、Avalanche、Berachain、Hyperliquid  
  - **交易操作**：交换、购买、出售、交易、兑换、转换、做多、做空、永久合约（perps）、期货、杠杆交易、限价单  
  - **钱包/财务操作**：余额查询、投资组合管理、存款、取款、转账、支付  
  - **市场/研究**：市场趋势、价格信息、图表分析、去中心化金融（DeFi）、收益情况、流动性、市场情绪（恐惧与贪婪指数）、预测市场  
  - **明确提及**：Minara、minara、x402、MoonPay、自动交易功能  

**路由规则（防止冲突）：**  
仅当消息中同时包含**财务/交易操作**以及至少一个**与加密相关的内容（代币、链名称、DeFi术语或“Minara”）时，才使用此技能。如果缺少加密相关内容，请勿进行路由。  

**使用要求：**  
需要登录Minara CLI；未登录时，请执行 `minara login`（建议使用设备验证码）。如果设备登录需要验证URL或代码，请将其发送给用户并等待验证完成（切勿直接点击“确定”）。如果已设置 `MINARA_API_KEY`，CLI将自动进行身份验证。  

### 交易确认（至关重要）  
对于所有涉及资金转移的操作（`swap`、`transfer`、`withdraw`、`perps order`、`perps deposit`、`perps withdraw`、`limit-order create`、`deposit buy`）：  
1. **执行前**：向用户显示操作详情（操作类型、代币、金额、接收方/链名称），并**请求用户明确确认**。切勿自动确认。  
2. **CLI返回确认提示后**（例如：“您确定要继续吗？”），将详细信息再次传达给用户，并**等待用户同意后再回复“y”**。未经用户同意，切勿替用户回复“y”。  
3. **禁止自动确认**：除非用户明确要求跳过确认步骤，否则严禁使用 `-y` 或任何自动确认标志。  
4. **用户拒绝时**：立即中止操作。  

此规则适用于所有涉及资金转移的操作。仅读操作（如 `balance`、`assets`、`chat`、`discover` 等）无需确认。  

### 操作分类与匹配  
根据用户消息内容，匹配相应的操作命令：  

#### 代币交换/购买/出售  
触发条件：消息中包含代币名称/代码以及交易指令（如 `swap`、`buy`、`sell`、`convert`、`exchange`、`trade`）。  
链名称会自动从代币名称中识别。如果同一代币存在于多个链上，CLI会提示用户选择目标链（按交易费用排序）。  
示例命令：  
```
minara swap -s <buy|sell> -t '<token>' -a <amount>
minara swap -s sell -t '<token>' -a all
```

#### 转账/发送/支付/取款  
触发条件：消息中提及向钱包地址发送或转移加密代币。  
示例命令：  
```
minara transfer <amount> <recipient_address>
minara transfer USDC to <address>
```

#### 永久合约（Perpetual Futures, Hyperliquid）  
触发条件：消息中提及永久合约、杠杆交易、做多/做空操作。  
示例命令：  
```
minara perps order <parameters>
```

#### 限价单  
触发条件：消息中提及限价单相关指令。  
示例命令：  
```
minara limit-order create <parameters>
```

#### 加密钱包/投资组合/账户  
触发条件：消息中提及钱包余额、投资组合信息或账户相关内容。  
示例命令：  
```
minara balance
minara assets
minara assets perps
minara deposit <amount>
```

#### 加密AI聊天/市场分析  
触发条件：用户询问加密价格、代币分析、DeFi研究等相关内容。  
示例命令：  
```
minara chat "<user text>"
```

#### 加密与股票市场探索  
触发条件：用户查询市场趋势、代币信息等。  
示例命令：  
```
minara discover trending
minara discover search <query>
```

#### x402协议支付  
触发条件：系统收到HTTP 402错误响应或用户提及支付相关内容。  
示例命令：  
```
minara deposit <amount> <payment_method>
```

#### 登录/设置  
触发条件：用户提及登录或设置相关内容。  
示例命令：  
```
minara login
minara config
```

## 注意事项：  
- **代币输入**：支持 `$TICKER`（如 `$BONK`）、代币名称或合约地址。  
- **JSON输出**：使用 `--json` 参数可获取机器可读的输出格式。  
- **交易安全**：必须先获取用户确认，再执行任何交易操作。  

## 其他说明：  
- CLI会话通过 `minara login` 自动创建。  
- `MINARA_API_KEY` 可通过环境变量或OpenClaw配置文件设置（可选），设置后CLI可自动认证。  

**完整命令示例请参阅：`{baseDir}/examples.md`**