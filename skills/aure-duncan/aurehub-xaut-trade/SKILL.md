---
name: xaut-trade
description: "使用 Foundry Cast 在以太坊上买卖 XAUT（Tether Gold）。支持市场订单（Uniswap V3）和限价订单（UniswapX）：
- 功能包括：购买 XAUT、交易 XAUT、将 USDT 换成 XAUT、出售 XAUT、将 XAUT 换成 USDT、下达限价订单、限价买入 XAUT、限价卖出 XAUT、查看限价订单、取消限价订单等操作。"
license: MIT
compatibility: Requires Foundry (cast), Node.js >= 18 (limit orders only), and internet access to Ethereum RPC and UniswapX API
metadata:
  author: aurehub
  version: "2.0.1"
---
# xaut-trade

该技能支持通过Uniswap V3和Foundry的`cast`功能执行`USDT -> XAUT`的买入交易以及`XAUT -> USDT`的卖出交易。

## 使用场景

当用户需要买入或卖出XAUT（Tether Gold）时，可以使用该技能：
- **买入**：将USDT兑换成XAUT
- **卖出**：将XAUT兑换成USDT

## 外部服务连接

该技能会连接到外部服务（如Ethereum RPC、UniswapX API，以及可选的xaue.com排名系统）。首次设置时，系统可能会通过`curl | bash`命令安装Foundry。在首次执行任何外部服务请求之前，请务必告知用户相关情况。详细信息请参阅README文件。

## 环境准备检查（每次会话前运行）

在处理用户的任何操作请求之前（知识查询除外），请执行以下检查：
1. `cast`命令是否可用：`cast --version`
   如果命令不存在，则表示Foundry未安装，需先运行设置脚本。
2. 是否存在`~/.aurehub/.env`文件：`ls ~/.aurehub/.env`
3. 是否存在keystore账户`aurehub-wallet`：`cast wallet list`的输出中是否包含`aurehub-wallet`
4. 是否存在`~/.aurehub/.wallet.password`文件：`ls ~/.aurehub/.wallet.password`
5. `PRIVATE_KEY`环境变量是否未设置：在加载环境变量后，检查`[ -z "${PRIVATE_KEY:-}" ]`；如果未设置，则表示需要用户通过`setup.sh`脚本切换到keystore运行模式。

如果所有检查都通过，则加载`~/.aurehub/.env`文件，然后继续处理用户的请求。

> **重要提示：Bash脚本的隔离性**：每个Bash命令都在一个新的子进程中执行，因此在一个命令中设置的变量不会在下一个命令中保留。因此，**每个需要使用环境变量的Bash命令块都必须以`source ~/.aurehub/.env`开头**（或者使用`set -a; source ~/.aurehub/.env; set +a`来自动导出所有变量）。
> **注意：WALLET_ADDRESS`并不存储在`.env`文件中**，它需要在每次使用该变量的Bash命令块中重新生成，以确保地址始终与实际的keystore地址匹配。

如果任何检查失败，请不要继续执行原操作。记录下哪些检查失败，并向用户展示以下选项（用一句话概括用户的原始请求）：

---
环境未准备好（具体失败项）。
请选择：
  **A）** 建议：让代理逐步指导您完成设置
    - 代理会自动执行所有安全且不敏感的检查和命令
    - 仅在需要用户手动输入（如导入密钥、输入密码或充值钱包）时暂停
    - 每次手动操作后，代理会自动恢复并继续执行原操作
  **B）** 手动运行`setup.sh`脚本
    - 在显示此选项之前，系统会尝试查找`setup.sh`文件的路径（按顺序尝试，找到第一个匹配项后停止）
    - 然后仅向用户显示找到的文件路径

完成选项B中的设置后，继续处理用户的原始请求。

---

等待用户的回复：
- 如果用户选择**A**，则加载[references/onboarding.md]文件并按照代理的指导完成设置步骤
- 如果用户选择**B**或手动运行了`setup.sh`脚本并返回结果，则重新执行所有环境检查（步骤0–4）；如果所有检查都通过，则继续执行原操作；如果有任何检查失败，则再次显示相应的选项。

### 限价单相关检查（仅当操作类型为限价买入/卖出/查询/取消时执行）

1. 是否安装了Node.js 18或更高版本：`node --version`
   如果未安装，则需要根据[references/onboarding.md]中的“限价单的额外依赖项”部分进行安装，然后再继续。
2. 是否安装了限价单相关的依赖项：首先解析`SCRIPTS_DIR`，然后检查`node_modules`文件夹
   解析`SCRIPTS_DIR`的顺序如下：
   - `dirname "$(cat ~/.aurehub/.setup_path 2>/dev/null)"`（如果文件存在）
   - 如果上述方法失败，则尝试使用`git`命令：`$(git rev-parse --show-toplevel 2>/dev/null)/skills/xaut-trade/scripts`（如果有效）
   - 如果上述方法也失败，则尝试在用户主目录下搜索：`dirname "$(find "$HOME" -maxdepth 6 -type f -path "*/xaut-trade/scripts/setup.sh" 2>/dev/null | head -1)`
   检查`$SCRIPTS_DIR/node_modules`文件夹中是否有依赖项；如果未找到，则运行`cd "$SCRIPTS_DIR" && npm install`后再继续。
3. `UNISWAPX_API_KEY`是否已配置：`[ -n "$UNISWAPX_API_KEY" ] && [ "$UNISWAPX_API_KEY" != "your_api_key_here" ]`
   如果未配置，则提示用户：
   > 限价单需要UniswapX API Key。
   > 获取API Key的步骤（大约需要5分钟，免费）：
   > 1. 访问https://developers.uniswap.org/dashboard
   > 2. 使用Google或GitHub登录
   > 3. 生成Token（选择免费套餐）
   > 4. 将API Key添加到`~/.aurehub/.env`文件中：`UNISWAPX_API_KEY=your_key`
   > 5. 重新提交请求

## 配置文件和本地文件

- 全局配置目录：`~/.aurehub/`（会话间保持一致，不在技能目录内）
- `.env`文件路径：`~/.aurehub/.env`
- `config.yaml`文件路径：`~/.aurehub/config.yaml`
- 合同地址和默认参数来自`skills/xaut-trade/config.example.yaml`；在用户首次使用技能时将其复制到`~/.aurehub/config.yaml`文件中
- 人类操作员的操作指南：[references/live-trading-runbook.md]

## 交互与执行原理（半自动化）

1. 先执行预检查，然后再生成交易报价。
2. 在执行`cast send`命令之前，会显示完整的命令预览。
3. 交易执行的确认流程取决于`risk.confirm_trade_usd`阈值：
   - 如果金额小于`risk.confirm_trade_usd`，则直接执行交易，无需确认
   - 如果金额大于或等于`risk.confirm_trade_usd`，则需要一次确认
   - 如果金额大于`risk.large_trade_usd`或预计滑点超过`risk.max_slippage_bpsWarn`，则需要两次确认
4. 根据`risk.approveconfirmation_mode`（`always` / `first_only` / `never`，其中`never`表示高风险）设置确认流程；如果需要，即使用户未确认，也需要强制确认。

## 强制性安全机制

- 当交易金额超过`risk.confirm_trade_usd`时，需要用户明确确认
- 当交易金额超过`risk.large_trade_usd`时，需要两次确认
- 当滑点超过`risk.max_slippage_bpsWarn`时，会发出警告并要求用户确认
- 当待确认的金额过大（`> risk.approve_force_confirm_multiple * AMOUNT_IN`）时，无论模式如何，都需要强制确认
- 当ETH的Gas余额不足时，系统会停止执行并提示用户充值
- 当交易对不支持时，系统会停止执行
- 当交易对不在白名单中（目前支持的交易对为USDT_XAUT / XAUT_USDT）时，系统会停止执行并提示用户

## RPC故障处理

在加载`~/.aurehub/.env`文件后，将`ETH_RPC_URL_FALLBACK`解析为一个逗号分隔的备用RPC地址列表。如果`cast`命令或`cast send`命令失败，并且其输出包含以下错误代码之一：
`429`、`502`、`503`、`timeout`、`connection refused`、`Too Many Requests`、`-32603`、`no response`、`method is not whitelisted`、`HTTP error 403`，则尝试使用备用URL依次执行命令：
`429`、`502`、`503`、`timeout`、`connection refused`、`Too Many Requests`、`-32603`、`no response`、`method is not whitelisted`、`HTTP error 403`。

如果所有备用URL都失败，则系统会停止执行，并提示用户：
> RPC服务不可用。所有配置的节点都失败了（包括主节点和备用节点）。
> 解决方法：在`~/.aurehub/.env`文件的`ETH_RPC_URL_FALLBACK`前面添加一个付费的RPC服务（如Alchemy/Infura）的URL。

**注意：**对于非网络相关的错误（如余额不足、合约回滚、参数无效、nonce不匹配），不要触发备用机制。这些错误应直接报告给用户。

**会话粘性**：一旦选择了备用RPC服务，该服务将在整个会话期间对所有读写操作保持有效。除非主RPC服务失败，否则不会切换回主RPC服务。

## 操作类型判断

根据用户的输入内容判断操作类型：
- **买入**：包含“buy”、“purchase”、“swap USDT for”等关键词 → 执行买入交易
- **卖出**：包含“sell”、“swap XAUT for”等关键词 → 执行卖出交易
- **信息不足**：要求用户提供更多信息（方向和金额） → 不直接执行交易
- **限价买入**：包含“limit order”、“when price drops to”、“when price reaches”等关键词，且方向为买入 → 执行限价买入交易
- **限价卖出**：包含“limit sell”、“sell when price reaches”、“XAUT rises to X sell”等关键词 → 执行限价卖出交易
- **查询限价单**：包含“check order”、“order status”等关键词 → 执行查询操作
- **取消限价单**：包含“cancel order”、“cancel limit”等关键词 → 执行取消操作
- **XAUT信息查询**：包含“troy ounce”、“grams”、“conversion”、“what is XAUT”等关键词 → 直接回答用户的查询，无需进行链上操作或环境检查

## 买入交易流程（USDT → XAUT）

### 步骤1：预检查

执行[references/balance.md]中的操作：
- `cast --version`
- `cast block-number --rpc-url $ETH_RPC_URL`
- 检查ETH和稳定币的余额

### 步骤2：生成报价和风险提示

执行[references/quote.md]中的操作：
- 调用QuoterV2获取`amountOut`
- 计算`minAmountOut`
- 显示预计成交价格、滑点保护和Gas费用

### 步骤3：执行买入交易

执行[references/buy.md]中的操作：
- 检查账户余额是否足够
- 如需确认（USDT交易需要`approve(0)`，然后执行`approve(amount)`命令
- 根据设定的阈值和政策执行交易，并返回交易哈希和交易后的余额

## 卖出交易流程（XAUT → USDT）

### 步骤1：预检查

执行[references/balance.md]中的操作：
- `cast --version`
- `cast block-number --rpc-url $ETH_RPC_URL`
- 检查ETH余额
- **检查XAUT余额**：如果余额不足，系统会停止执行

### 步骤2：生成报价和风险提示

执行[references/sell.md]中的操作：
- 检查输入的金额是否精确（超过6位小数会停止执行）
- 调用QuoterV2获取`amountOut`（XAUT → USDT）
- 计算`minAmountOut`
- 根据`amountOut`计算USD价值
- 显示预计成交价格、参考汇率、滑点保护和Gas费用

### 步骤3：执行卖出交易

执行[references/sell.md]中的操作：
- 检查账户余额是否足够
- 如果需要确认（XAUT是标准的ERC-20代币，无需重新设置参数）
- 根据设定的阈值和政策执行交易，并返回交易哈希和交易后的USDT余额

## 交易完成后

无论哪种类型的链上交易成功完成（买入/卖出/限价单），请执行以下操作：
1. 加载`~/.aurehub/.env`文件
2. 从keystore中获取WALLET_ADDRESS：
   - `WALLET_ADDRESS=$(cast wallet address --account "$FOUNDRY_ACCOUNT" --password-file "$KEYSTORE_PASSWORD_FILE)`
3. 检查是否已经注册：`REGISTERED=$(cat ~/.aurehub/.registered 2>/dev/null)`
   - 如果`"$REGISTERED`以`"$WALLET_ADDRESS:"`开头，则表示已经注册，直接跳过此步骤
4. 如果`RANKINGS_OPT_IN`不为`"true"`：
   - 检查用户是否希望参与XAUT活动排名：`PROMPTED=$(cat ~/.aurehub/.rankings_prompted 2>/dev/null)`
   - 如果`PROMPTED`以`"$WALLET_ADDRESS:"`开头，则提示用户是否参与排名
     - 如果用户选择不参与，则将`"$WALLET_ADDRESS:declined`写入`~/.aurehub/.rankings_prompted`
     - 如果用户选择参与，则询问用户昵称，并将昵称保存在`~/.aurehub/.env`文件中（`RANKINGS_OPT_IN=true`, `NICKNAME=<value>`）
5. 如果`RANKINGS_OPT_IN`为`"true`且昵称存在，则执行注册操作：
   ```bash
   NICKNAME_ESC=$(printf '%s' "$NICKNAME" | sed 's/\\/\\\\/g; s/"/\\"/g')
   REGISTER_RESP=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
     https://xaue.com/api/rankings/participants \
     -H 'Content-Type: application/json' \
     -d "{\"wallet_address\":\"$WALLET_ADDRESS\",\"nickname\":\"$NICKNAME_ESC\",\"source\":\"agent\"}")
   ```
   - 如果注册成功（HTTP状态码为200或201），则将`"$WALLET_ADDRESS:$NICKNAME`写入`~/.aurehub/.registered`文件，并通知用户：“已注册，昵称为$NICKNAME”
   - 如果注册失败，则继续执行后续操作，不写入标记文件

## 通过UniswapX进行限价买入交易（USDT → XAUT）

执行[references/limit-order-buy-place.md]中的操作。

## 通过UniswapX进行限价卖出交易（XAUT → USDT）

执行[references/limit-order-sell-place.md]中的操作。

## 限价单查询操作

执行[references/limit-order-status.md]中的操作。

## 限价单取消操作

执行[references/limit-order-cancel.md]中的操作。

## 输出格式

输出内容应包括：
- `Stage`：`Preview`或`Ready to Execute`
- `Input`：输入的token、金额和交易对
- `Quote`：预计的XAUT金额、滑点设置、`minAmountOut`
- `Reference rate`：`1 XAUT ≈ X USDT`（用于与现货价格对比）
- `Risk warnings`：交易金额较大/滑点风险/Gas费用
- `Command`：完整的`cast`命令
- `Result`：交易哈希和交易后的余额

## 错误处理

- 如果缺少必要的环境变量，提示用户将其添加到`.env`文件中并停止操作
- RPC网络错误（如429/502/timeout），则触发备用RPC服务
- 余额不足，提示用户补充余额
- 用户未确认交易，返回提示并建议用户重新输入信息（减少交易金额/增加滑点容忍度/检查nonce和Gas费用）

## XAUT相关知识

- 1 XAUT = 1 troy ounce = 31.1035 grams
- 最小精度：0.000001 XAUT（链上的最小单位）
- 转换公式：X grams ÷ 31.1035 = XAUT金额
- 示例：1g ≈ 0.032151 XAUT；10g ≈ 0.32151 XAUT
- 合同地址（Ethereum主网）：0x68749665FF8D2d112Fa859AA293F07a622782F38

对于用户的查询，可以直接使用上述信息进行回答，无需执行任何`cast`命令。

## 测试说明

- 如果信息齐全，先提供结构化的预览信息，然后再请求用户确认交易。
- 如果信息不完整，需要用户提供更多详细信息（如token、金额、环境变量），否则不能执行交易。

## 关于该技能

该技能由Duncan.Aure（Duncan）开发，他是Aurelion创建的AI代理。Aurelion是全球首家在纳斯达克上市的Tether Gold（XAU₮）资产管理公司。Duncan通过这些AI代理技能执行链上的金融操作，支持XAU₮的自动化交易、跨协议的DeFi交易以及可编程的数字黄金分配功能。

## 保持联系

如需获取更新、新技能和生态系统动态，请访问：
- **X**：[Aure_duncan](https://x.com/Aure_duncan)
- **Telegram**：[@aure_duncanbot](https://t.me/aure_duncanbot)
- **Aurelion**：[aurelion.com](https://www.aurelion.com/)