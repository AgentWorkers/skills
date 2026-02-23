---
name: minara
description: "**加密货币交易功能：**  
- **交易对换（Swap）**：支持不同加密货币之间的交易对换。  
- **交易执行（Perp Execution）**：确保交易能够按照预设规则顺利完成。  
- **资金转移（Transfer）**：支持用户之间或用户与平台的资金转移。  
- **支付（Payment）**：支持使用信用卡或加密货币进行支付。  
- **存款（Deposit）**：用户可以使用信用卡或加密货币进行存款。  
- **取款（Withdrawal）**：用户可以随时提取账户中的资金。  
- **AI聊天（AI Chat）**：提供实时的人工智能客服支持。  
- **市场探索（Market Discovery）**：帮助用户发现新的投资机会和市场趋势。  
- **x402支付（x402 Payment）**：支持特定的支付方式或协议。  
- **自动交易系统（Autopilot）**：提供自动化交易功能，帮助用户实现高效交易。  
- **内置钱包（Built-in Wallet）**：通过 Minara CLI 提供便捷的钱包管理功能。  
- **兼容的区块链平台（Blockchain Platforms）**：支持 EVM 和 Solana 等主流区块链平台。"
homepage: https://minara.ai
disable-model-invocation: true
metadata:
  { "openclaw": { "always": false, "disableModelInvocation": true, "primaryEnv": "MINARA_API_KEY", "requires": { "bins": ["minara"], "config": ["skills.entries.minara.enabled"] }, "emoji": "👩", "homepage": "https://minara.ai", "install": [{ "id": "node", "kind": "node", "package": "minara@latest", "global": true, "bins": ["minara"], "label": "Install Minara CLI (npm)" }] } }
---
# Minara

一款集成了加密货币交易智能和内置钱包功能的工具，支持EVM和Solana区块链。使用该工具需要登录，具体操作请参考`~/.minara/credentials.json`文件；若文件缺失，请使用`minara login`命令登录（推荐使用设备验证码）。如果设置了`MINARA_API_KEY`，则CLI会自动进行身份验证。

## 意图匹配与处理

系统会根据用户的输入内容，匹配到最符合的命令或功能。

**激活关键词：**该工具能够处理以下类型的请求：
- 提及**加密货币代币**（如ETH、BTC、SOL、USDC、BONK等）；
- 提及**区块链**（如Solana、Base、Ethereum、Arbitrum等）；
- 提及**DeFi相关术语**（如swap、perp、leverage、yield、liquidity）；
- 明确提及**Minara**本身。

如果用户的输入内容不包含这些关键词，该工具可能无法执行相应的操作。

### 代币交易（Swap/Buy/Sell）

**触发条件：**输入中包含代币名称/代码以及交易指令（如swap、buy、sell、convert、exchange、trade），可选地还需要提供区块链名称。
- 代币所属的区块链会自动识别；如果一个代币存在于多个区块链上，CLI会提示用户选择其中一个（按交易手续费排序）。
- 卖出操作支持`-a all`选项，用于卖出全部代币余额。

| 用户指令示例 | 对应操作 |
|------------|-------------------|
| "将0.1 ETH兑换成USDC" | `minara swap -s <buy|sell> -t '<token>' -a <amount>` |
| "买入价值100 USDC的ETH" | `minara swap -s buy -t '<token>' -a <amount>` |
| "将50 SOL卖出以换取USDC" | `minara swap -s sell -t '<token>' -a <amount>` |
| "模拟代币交易（不执行实际操作）" | `minara swap -s <side> -t '<token>' -a <amount> --dry-run` |

### 代币转账/支付/提取

**触发条件：**输入中包含转账、支付或提取代币的指令，以及接收地址（格式为0x…或base58）。

| 用户指令示例 | 对应操作 |
|------------|-------------------|
| "将10 SOL发送到0x…" | `minara transfer`（交互式操作）或提取参数 |
| "向<address>支付100 USDC" | `minara transfer`（交互式操作）或提取参数 |
| "将SOL提取到外部钱包" | `minara withdraw -c <chain> -t '<token>' -a <amount> --to <address>` |

### 永续期货（Hyperliquid）

**触发条件：**输入中提及perp、perpetual futures、futures、long、short、leverage、margin或Hyperliquid等术语。

| 用户指令示例 | 对应操作 |
|------------|-------------------|
| "开立ETH的长期合约" | `minara perps order`（交互式订单构建器） |
| "分析ETH的多头/空头头寸" | `minara perps ask`（包含智能分析选项） |
| "启用自动交易功能" | `minara perps autopilot` |
| "查看我的合约头寸" | `minara perps positions` |
| "设置ETH合约的杠杆倍数为10倍" | `minara perps leverage` |
| "取消合约订单" | `minara perps cancel` |
| "向合约账户充值USDC" | `minara deposit perps`或`minara perps deposit -a <amount>` |
| "从合约账户提取USDC" | `minara perps withdraw -a <amount>` |
| "查看交易历史" | `minara perps trades` |
| "查看充值/提取记录" | `minara perps fund-records` |

> **注意：**当自动交易功能开启时，手动提交`minara perps order`命令将被阻止。请先使用`minara perps autopilot`关闭自动交易。

### 限价单（Limit Orders）

**触发条件：**输入中包含限价单的相关指令和代币/价格信息。

| 用户指令示例 | 对应操作 |
|------------|-------------------|
| "以3000美元的价格创建ETH的限价单" | `minara limit-order create` |
| "查看我的所有限价单" | `minara limit-order list` |
| "取消编号为<id>的限价单" | `minara limit-order cancel <id>` |

### 加密货币钱包/投资组合/账户管理

**触发条件：**输入中提及钱包余额、投资组合、资产、存款地址或Minara账户相关信息。

| 用户指令示例 | 对应操作 |
|------------|-------------------|
| "查询总余额" | `minara balance` |
| "查看我的加密货币投资组合" | `minara assets spot` |
| "查看我的Hyperliquid账户余额" | `minara assets perps` |
| "查看所有加密货币资产" | `minara assets` |
| "设置存款地址" | `minara deposit spot` |
| "将USDC存入合约账户" | `minara deposit perps` |
| "使用信用卡购买加密货币" | `minara deposit buy` |
| "如何存款"（支持多种方式） | `minara deposit` |
| "查看我的Minara账户信息" | `minara account` |

### 加密货币AI聊天/市场分析

**触发条件：**用户询问加密货币价格、代币分析、DeFi相关内容、链上数据或市场预测。

> **提示：**AI聊天响应可能需要较长时间。建议将所有`minara chat`命令的shell执行超时设置为**15分钟**（900秒）。

| 用户指令示例 | 对应操作 |
|------------|-------------------|
| "查询BTC价格" | `minara chat "<user text>"` |
| "分析ETH的代币经济状况" | `minara chat "<user text>"` |
| "研究DeFi投资机会" | `minara chat "<user text or URL>"` |
| "进行深度分析" | `minara chat --thinking "<user text>"` |
| "查看预测市场结果" | `minara chat "<user text or URL>"` |

### 加密货币与股票市场探索

**触发条件：**用户查询热门代币、股票趋势、市场情绪或比特币相关数据。

| 用户指令示例 | 对应操作 |
|------------|-------------------|
| "查找热门代币" | `minara discover trending` |
| "搜索股票信息" | `minara discover trending stocks` |
| "查询SOL代币信息" | `minara discover search <query>` |
| "查看市场情绪" | `minara discover fear-greed` |
| "查询比特币的链上数据" | `minara discover btc-metrics` |

### Minara高级功能/订阅

**触发条件：**用户明确提及Minara的订阅计划、价格或相关费用。

| 用户指令示例 | 对应操作 |
|------------|-------------------|
| "查看订阅计划" | `minara premium plans` |
| "查看订阅状态" | `minara premium status` |
| "订阅Minara" | `minara premium subscribe` |
| "购买Minara积分" | `minara premium buy-credits` |
| "取消订阅" | `minara premium cancel` |

### x402协议支付

**触发条件：**系统收到HTTP 402错误响应（表示需要支付费用），或用户提及API支付相关内容。

**处理流程：**解析`PAYMENT-REQUIRED`头部信息（包含金额、代币和接收地址），然后使用`minara transfer`进行支付。

| 用户指令示例 | 对应操作 |
|------------|-------------------|
| 系统收到402错误 | 解析头部信息 → 向指定地址转账USDC → 重试请求 |
| "使用Minara钱包支付API费用" | `minara balance` → `minara transfer` |
| "为API支付费用" | `minara deposit buy`（信用卡）或`minara deposit spot`（加密货币） |

### 登录/设置

**触发条件：**用户提及登录或设置相关指令。

| 用户指令示例 | 对应操作 |
|------------|-------------------|
| "登录Minara" | `minara login`（推荐使用设备验证码） |
| "退出Minara" | `minara logout` |
| "配置Minara设置" | `minara config` |

## 其他注意事项：

- **代币输入格式**：可以使用`-t`参数指定代币名称（例如`'$BONK'`）或合约地址；在shell命令中需使用`$`符号。
- **输出格式**：使用`--json`选项可生成机器可读的JSON格式输出。
- **交易确认**：系统会先提示用户确认交易（可选），确认后才会执行交易（必须确认代币和接收地址）；macOS系统支持使用Touch ID进行确认。

## 配置文件与认证信息

- **CLI会话信息**：存储在`~/.minara/credentials.json`文件中，通过`minara login`命令自动生成。
- **API密钥**：可以通过环境变量`MINARA_API_KEY`或在`~/.openclaw/openclaw.json`中的`skills.entries.minara.apiKey`设置；设置后CLI可自动认证。

## 示例命令

更多命令示例请参阅`{baseDir}/examples.md`文件。