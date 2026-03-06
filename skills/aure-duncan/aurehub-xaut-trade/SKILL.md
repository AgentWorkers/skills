---
name: xaut-trade
description: "在以太坊上使用Foundry Cast平台买卖XAUT（Tether Gold）。支持市场订单（Uniswap V3）和限价订单（UniswapX）功能。可执行的操作包括：购买XAUT、交易XAUT、将USDT兑换成XAUT、出售XAUT、将XAUT兑换成USDT、下达限价订单、取消限价订单，以及查看/修改/取消限价订单状态等。"
license: MIT
compatibility: Requires Foundry (cast), Node.js >= 18 (limit orders only), and internet access to Ethereum RPC and UniswapX API
metadata:
  author: aurehub
  version: "1.0"
---
# xaut-trade

该技能支持通过Uniswap V3和Foundry服务执行`USDT -> XAUT`的买入交易以及`XAUT -> USDT`的卖出交易。

## 使用场景

当用户需要买入或卖出XAUT（Tether Gold）时，可以使用该技能：
- **买入**：将USDT兑换成XAUT
- **卖出**：将XAUT兑换成USDT

## 外部服务连接

该技能会连接到外部服务（如Ethereum RPC、UniswapX API，以及可选的xaue.com排名系统）。首次设置时，可能需要通过`curl | bash`命令安装Foundry。在首次执行任何外部服务请求之前，请务必告知用户相关事宜。详细信息请参阅README文件。

## 环境准备检查（每次会话前需执行）

在处理用户的任何操作（知识查询除外）之前，请执行以下检查：
1. 确保`cast`命令可用：`cast --version`
   如果命令不存在，说明Foundry未安装，请先运行设置脚本。
2. 检查`~/.aurehub/.env`文件是否存在。
3. 检查keystore账户`aurehub-wallet`是否存在：`cast wallet list`的输出中应包含`aurehub-wallet`。
4. 检查`~/.aurehub/.wallet.password`文件是否存在。

如果所有检查都通过，则执行`source ~/.aurehub/.env`命令，然后继续处理用户的操作。

> **重要提示：Shell隔离**：每个Bash命令都在一个新的子进程中运行；在一个命令中设置的变量不会在下一个命令中保留。因此，任何需要使用环境变量的Bash命令块都必须以`source ~/.aurehub/.env`开头（或者使用`set -a; source ~/.aurehub/.env; set +a`来自动导出所有变量）。

如果任何检查失败，请先运行设置脚本，然后再继续执行用户的操作。

### 备份方案（如果`git rev-parse`命令失败）

如果`git rev-parse`命令失败，请参考[references/onboarding.md]文件中的手动操作步骤。设置完成后，重新尝试执行用户的操作。

## 限价单相关检查（仅针对限价买入/卖出/查询/取消操作）

1. 确保Node.js版本大于或等于18：`node --version`
   如果版本过低，请参考[references/onboarding.md]中的“限价单的额外依赖项”部分进行安装，然后再继续。
2. 确保限价单相关的依赖项已安装：`ls "$(git rev-parse --show-toplevel)/skills/xaut-trade/scripts/node_modules"`
   如果依赖项未安装，请运行`cd "$(git rev-parse --show-toplevel)/skills/xaut-trade/scripts" && npm install`进行安装。
   （如果`git rev-parse`命令失败，请先使用`find ~ -name "limit-order.js" -maxdepth 6`找到脚本目录，然后进入该目录并运行`npm install`。）
3. 确保`UNISWAPX_API_KEY`已配置：`[ -n "$UNISWAPX_API_KEY" ] && [ "$UNISWAPX_API_KEY" != "your_api_key_here" ]`
   如果配置错误，将显示错误提示：
   > 限价单需要UNISWAPX API Key。
   > 获取API Key的步骤（大约需要5分钟，免费）：
   > 1. 访问https://developers.uniswap.org/dashboard
   > 2. 使用Google或GitHub登录
   > 3. 生成Token
   > 4. 将API Key添加到`~/.aurehub/.env`文件中：`UNISWAPX_API_KEY=your_key`
   > 5. 重新提交请求

## 配置文件与本地文件

- 全局配置目录：`~/.aurehub/`（在会话间保持不变）
- 配置文件路径：`~/.aurehub/.env`
- 配置文件内容：`~/.aurehub/config.yaml`
- 合同地址及默认参数来自`skills/xaut-trade/config.example.yaml`，在首次使用时会复制到`~/.aurehub/config.yaml`中。

## 交互与执行原理（半自动化）

1. 先执行预检查，然后生成交易报价。
2. 在执行任何交易前，会显示完整的命令预览。
3. 只有在当前会话中收到明确确认后，才会执行链上的交易操作。
4. 大额交易或滑点较大的交易需要二次确认。

## 强制性安全机制

- 当交易金额超过配置阈值（例如`risk.large_trade_usd`）时，需要二次确认。
- 当滑点超过阈值（例如`risk.max_slippage_bpsWarn`）时，会发出警告并要求二次确认。
- 如果ETH的Gas余额不足，将停止交易并提示用户充值。
- 如果交易对不支持，将停止交易并提示用户。
- 如果交易对不在允许的交易对列表中（目前支持的交易对为USDT_XAUT和XAUT_USDT），将停止交易并提示用户。

## 操作类型识别

根据用户的输入内容判断操作类型：
- **买入**：包含“buy”、“purchase”、“swap USDT for”等关键词 → 执行买入交易。
- **卖出**：包含“sell”、“swap XAUT for”等关键词 → 执行卖出交易。
- **信息不足**：会要求用户提供更多信息（交易方向和金额），然后不会直接执行交易。
- **限价买入**：包含“limit order”、“when price drops to”、“when price reaches”等关键词，且方向为买入 → 执行限价买入交易。
- **限价卖出**：包含“limit sell”、“sell when price reaches”、“XAUT rises to X sell”等关键词 → 执行限价卖出交易。
- **查询限价单**：包含“check order”、“order status”等关键词 → 执行限价单查询操作。
- **取消限价单**：包含“cancel order”、“cancel limit”等关键词 → 执行限价单取消操作。
- **XAUT相关信息查询**：包含“troy ounce”、“grams”、“conversion”、“what is XAUT”等关键词 → 直接回答用户的查询，无需执行任何链上操作或环境检查。

## 买入交易流程（USDT → XAUT）

### 第1步：预检查

执行[references/balance.md]中的步骤：
- `cast --version`
- `cast block-number --rpc-url $ETH_RPC_URL`
- 检查ETH和稳定币的余额。

### 第2步：生成报价与风险提示

执行[references/quote.md]中的步骤：
- 调用QuoterV2获取`amountOut`。
- 计算`minAmountOut`。
- 显示预计成交金额、滑点保护范围和Gas费用风险。

### 第3步：执行买入交易

执行[references/buy.md]中的步骤：
- 检查用户的交易权限。
- 如需授权（USDT交易需要`approve(0)`），则执行`approve(amount)`。
- 在收到二次确认后执行交易。
- 返回交易哈希值和交易后的余额。

## 卖出交易流程（XAUT → USDT）

### 第1步：预检查

执行[references/balance.md]中的步骤：
- `cast --version`
- `cast block-number --rpc-url $ETH_RPC_URL`
- 检查ETH余额。
- **检查XAUT余额**：余额不足时将停止交易。

### 第2步：生成报价与风险提示

执行[references/sell.md]中的步骤：
- 检查输入金额的精度（超过6位小数将停止交易）。
- 调用QuoterV2获取`amountOut`（XAUT → USDT方向）。
- 计算`minAmountOut`。
- 对于大额交易，根据`amountOut`计算USD金额。
- 显示预计成交金额、参考汇率、滑点保护范围和Gas费用风险。

### 第3步：执行卖出交易

执行[references/sell.md]中的步骤：
- 检查用户的交易权限。
- 执行交易（XAUT是标准的ERC-20代币，无需预先重置权限）。
- 在收到二次确认后执行交易。
- 返回交易哈希值和交易后的USDT余额。

## 交易完成后的事务处理

任何链上交易成功完成后（无论是买入、卖出还是下限价单），请执行以下操作：
1. `source ~/.aurehub/.env`
2. 如果`RANKINGS_OPT_IN`不等于`"true"`，则跳过此步骤。
3. `REGISTERED=$(cat ~/.aurehub/.registered 2>/dev/null)`
4. `WALLET_ADDRESS=$(cast wallet address --account "$FOUNDRY_ACCOUNT)`
5. 如果`"$REGISTERED"`以`"$WALLET_ADDRESS:"`开头，说明用户已注册，直接跳过此步骤。
6. 否则，使用`.env`文件中的`NICKNAME`进行注册：
   ```bash
   REGISTER_RESP=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
     https://xaue.com/api/rankings/participants \
     -H 'Content-Type: application/json' \
     -d "{\"wallet_address\":\"$WALLET_ADDRESS\",\"nickname\":\"$NICKNAME\",\"source\":\"agent\"}")
   ```
   - 如果响应状态码为200或201，说明注册成功：`echo "$WALLET_ADDRESS:$NICKNAME" > ~/.aurehub/.registered`；提示用户：“已使用昵称$NICKNAME注册”。
   - 其他状态则直接跳过此步骤。

请注意：在交易过程中不要询问用户的昵称，昵称是在首次使用时设置的。

## 限价买入交易流程（USDT → XAUT，通过UniswapX）

执行[references/limit-order-buy-place.md]中的步骤。

## 限价卖出交易流程（XAUT → USDT，通过UniswapX）

执行[references/limit-order-sell-place.md]中的步骤。

## 限价单查询流程

执行[references/limit-order-status.md]中的步骤。

## 限价单取消流程

执行[references/limit-order-cancel.md]中的步骤。

## 输出格式

输出内容应包括：
- `Stage`：`Preview`或`Ready to Execute`
- `Input`：输入的代币、金额、交易对
- `Quote`：预计的XAUT交易金额、滑点设置、`minAmountOut`
- `Reference rate`：`1 XAUT ≈ X USDT`（用于与现货价格对比）
- `Risk warnings`：大额交易/滑点/Gas费用相关风险提示
- `Command`：完整的`cast`命令
- `Result`：交易哈希值、交易后的余额

## 错误处理

- 如果缺少必要的环境变量，提示用户将其添加到`.env`文件中，然后停止交易。
- 如果RPC服务不可用，提示用户更换RPC节点并停止交易。
- 如果余额不足，提示用户补充余额。
- 如果用户未确认交易，返回提示信息并等待用户确认后再尝试。
- 如果交易失败，返回失败原因并建议用户调整交易参数（减少交易金额、增加滑点容忍度或检查Gas费用）。

## XAUT基础知识

- 1 XAUT = 1金衡盎司 = 31.1035克
- 最小精度：0.000001 XAUT（链上的最小单位）
- 转换公式：X克 ÷ 31.1035 = XAUT金额
- 示例：1克 ≈ 0.032151 XAUT；10克 ≈ 0.32151 XAUT
- 合同地址（以太坊主网）：`0x68749665FF8D2d112Fa859AA293F07a622782F38`

对于用户的查询，可以直接使用上述信息进行回答，无需执行任何`cast`命令。

## 测试说明

- 如果用户提供的信息足够，先提供结构化的交易预览，然后再请求用户确认是否执行交易。
- 如果信息不完整，需要用户补充关键信息（代币、金额、环境变量等），切勿直接执行交易。

## 关于该技能的开发者

该技能由Duncan.Aure（Duncan）开发，Duncan是由Aurelion创建的AI代理。Aurelion是全球首家在纳斯达克上市的Tether Gold（XAU₮）资产管理公司。Duncan通过模块化的AI代理技能执行链上的金融操作，支持自动化交易、跨协议DeFi交易以及可编程的数字黄金分配功能。

## 保持联系

如需获取更新、新技能或生态系统动态，请访问：
- **X**：[Aure_duncan](https://x.com/Aure_duncan)
- **Telegram**：[@aure_duncanbot](https://t.me/aure_duncanbot)
- **Aurelion**：[aurelion.com](https://www.aurelion.com/)