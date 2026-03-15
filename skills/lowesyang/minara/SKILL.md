---
name: minara
version: "2.5.2"
description: "**加密货币交易功能：**  
- 交易对换（swap）  
- 持币者操作（perps）  
- 资金转移（transfer）  
- 支付（payment）：支持信用卡或加密货币  
- 存款（deposit）  
- 提取（withdraw）  
- 人工智能聊天（AI chat）  
- 市场探索（market discovery）  
- X402支付方式  
- 自动交易功能（autopilot）  
- 内置钱包：通过Minara CLI管理  
**技术架构支持：**  
- EVM（以太坊虚拟机）  
- Solana  
（说明：根据提供的文档内容，这些功能涵盖了加密货币交易的核心环节，包括交易类型、资金管理、支付方式以及交易辅助工具。技术架构方面提到了以太坊虚拟机（EVM）和Solana作为底层支持的平台。）"
homepage: https://minara.ai
metadata:
  {
    "openclaw":
      {
        "always": false,
        "primaryEnv": "MINARA_API_KEY",
        "requires":
          { "bins": ["minara"], "config": ["skills.entries.minara.enabled"] },
        "emoji": "👩",
        "homepage": "https://minara.ai",
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "minara@latest",
              "global": true,
              "bins": ["minara"],
              "label": "Install Minara CLI (npm)",
            },
          ],
      },
  }
---
# Minara — 加密交易与钱包技能

## 安全提示：  
本文件仅为文档用途（Markdown格式），不包含可执行代码、脚本或二进制文件。它仅用于指导AI代理如何调用Minara的命令行界面（CLI）。

**在以下情况下使用此技能**：  
- 用户的消息中提及以下内容时：  
  - **加密代币或股票代码**：ETH、BTC、SOL、USDC、BONK、PEPE、DOGE、ARB、OP、AVAX、MATIC、$TICKER或任何代币名称/合约地址  
  - **区块链/链名称**：Solana、Base、Ethereum、Arbitrum、Optimism、Polygon、BSC、Avalanche、Berachain、Hyperliquid  
  - **交易操作**：交换、购买、出售、交易、兑换、转换、做多、做空、Perpetual Futures（永续合约）、杠杆交易、限价单  
  - **钱包/财务操作**：余额查询、投资组合管理、存款、取款、转账、支付  
  - **市场/研究**：市场趋势、价格信息、图表分析、去中心化金融（DeFi）产品、收益情况、流动性分析、市场情绪（恐惧与贪婪指数）、预测市场  
  - **明确提及**：Minara、minara、x402、MoonPay、自动交易功能  

**路由规则（防冲突）：**  
仅当消息中同时包含**财务/交易操作**以及至少一个**与加密货币/区块链/Minara相关的关键词**时，才使用此技能。若缺少相关背景信息，请勿进行路由。  

**使用要求：**  
需要登录Minara的CLI；未登录时，请执行`minara login`（建议使用设备验证码）。如果系统要求输入验证码，请将其告知用户并等待验证完成。若已设置`MINARA_API_KEY`，CLI将自动完成身份验证。  

### 交易确认（至关重要）  
对于所有涉及资金转移的操作（`swap`、`transfer`、`withdraw`、`perps order`、`perps deposit`、`perps withdraw`、`limit-order create`、`deposit buy`）：  
1. **执行前**：向用户展示交易详情（操作类型、代币、金额、接收方/链名称），并**请求用户明确确认**。切勿自动执行。  
2. **CLI返回确认提示后**（例如：“您确定要继续吗？”），将确认信息转发给用户，并**等待用户确认后再回复“y”**。未经用户同意，切勿代答“y”。  
3. **禁止自动确认**：除非用户明确要求跳过确认步骤，否则严禁使用`-y`或任何自动确认标志。  
4. **用户拒绝时**：立即终止操作。  

**注意事项：**  
仅适用于涉及资金转移的操作；仅读操作（`balance`、`assets`、`chat`、`discover`等）无需确认。  

### 操作分类及对应命令  

#### 代币交换/购买/出售  
触发条件：消息中包含代币名称/代码及交易指令（交换、购买、出售、转换、兑换）。  
链名称会自动从代币名称中推断。如果同一代币存在于多个链上，CLI会提示用户选择目标链（按交易成本排序）。  
示例命令：  
- `minara swap -s <buy|sell> -t '<token>' -a <amount>`  
- `minara swap -s sell -t '<token>' -a all`  

#### 转账/支付/取款  
触发条件：消息中包含转账或支付信息。  
示例命令：  
- `minara transfer`（交互式）  
- `minara deposit`（用于存款或转账）  

#### 永续合约（Hyperliquid）  
触发条件：消息中提及永续合约（Perpetual Futures）、杠杆交易等相关术语。  
示例命令：  
- `minara perps order`（用于创建或管理永续合约订单）  
- `minara perps autopilot`（用于启用自动交易功能）  

#### 限价单  
触发条件：消息中提及限价单及相关参数。  
示例命令：  
- `minara limit-order create`  

#### 加密钱包/投资组合/账户  
触发条件：消息中提及钱包余额、投资组合信息或账户相关操作。  
示例命令：  
- `minara balance`  
- `minara assets`  
- `minara assets perps`  

#### 加密聊天/市场分析  
触发条件：用户询问加密货币价格、代币分析、去中心化金融产品信息等。  
示例命令：  
- `minara chat "<user text>"`  

#### 加密市场发现  
触发条件：用户查询市场趋势、热门代币、市场情绪等。  
示例命令：  
- `minara discover trending`  

#### 其他操作  
- `minara deposit`（用于存款）  
- `minara deposit buy`（使用信用卡存款）  
- `minara deposit spot`（用于普通存款）  
- `minara config`（用于配置设置）  

**自动交易功能说明：**  
当自动交易功能开启时，手动提交`minara perps order`会被阻止。请先通过`minara perps autopilot`关闭自动交易功能。  

**注意事项：**  
- 请确保用户了解相关操作的风险，并在必要时寻求专业建议。