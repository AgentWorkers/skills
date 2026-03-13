---
name: katbot-trading
version: 0.2.25
description: 通过 Katbot.ai 在 Hyperliquid 上进行实时加密货币交易。该平台提供 BMI（市场分析工具）、代币选择功能以及基于人工智能的交易执行服务。
# Note: Homepage URL removed to avoid GitHub API rate limit errors during publish
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["python3", "openclaw"], "env": ["KATBOT_HL_AGENT_PRIVATE_KEY"] },
        "primaryEnv": "KATBOT_HL_AGENT_PRIVATE_KEY",
        "install": "pip install -r requirements.txt"
      }
  }
---
# Katbot交易技能

该技能教导代理如何使用Katbot.ai API来管理Hyperliquid交易投资组合。

## 功能

1. **订阅监控**：在会话开始时检查订阅状态、到期时间以及功能使用限制。
2. **市场分析**：检查BTC动量指数（BMI）和24小时内的盈利/亏损情况。
    - `btc_momentum.py`：根据趋势、MACD、价格波动幅度、成交量和RSI计算BMI（BTC动量指数），并返回信号（牛市、熊市、中性）。
    - `bmi_alert.py`：运行`btc_momentum.py`，如果市场方向发生变化，则通过Telegram发送警报。使用`portfolio_tokens.json`文件来跟踪自定义代币。
3. **代币选择**：根据当前市场方向自动选择最佳代币。
4. **推荐**：获取基于AI的交易设置（入场价、止盈价、止损价、杠杆率）。
5. **执行**：在用户确认后，在Hyperliquid平台上执行和关闭交易。
6. **投资组合跟踪**：监控未平仓头寸、未实现利润（uPnL）和余额。
7. **绩效图表**：生成累计未实现利润图表（24小时/7天/30天），以PNG图像格式保存，以便通过Telegram分享。
8. **聊天**：向投资组合代理发送自由格式的消息并接收分析结果。

## 工具

**所有工具脚本仅保存在`{baseDir}/tools/`目录中**——这是唯一的官方存储位置。项目中其他地方没有副本。始终通过`{baseDir}/tools/<script>`引用工具，并设置`PYTHONPATH={baseDir}/tools`，以确保工具之间的导入能够正确进行。

依赖项列在`{baseDir}/requirements.txt`文件中。

- `ensure_env.sh`：**在任何工具运行之前执行**。检查当前技能版本所需的依赖项是否已安装，如需安装则重新安装。每次运行都是安全的——如果已经是最新的，则立即退出。
- `katbot_onboard.py**：**首次设置向导**。通过SIWE使用您的钱包密钥进行身份验证，创建/选择投资组合，并将凭据保存到安全的身份目录中。
- `katbot_client.py`：核心API客户端。处理身份验证、代币刷新、投资组合管理、推荐、交易执行、聊天和订阅监控。也可作为CLI脚本使用。
- `katbot_workflow.py**：端到端的交易工作流程（BMI -> 代币选择 -> 推荐）。导入`katbot_client`和`token_selector`——需要`PYTHONPATH={baseDir}/tools`。
- `token_selector.py`：通过CoinGecko基于动量选择代币。
- `btc_momentum.py`：计算BTC动量指数（BMI）。
- `bmi_alert.py`：用于BMI变化的Telegram警报工作流程。
- `portfolio_chart.py`：获取投资组合交易历史记录，使用FIFO代币级别匹配重新计算累计未实现利润，并保存800×450像素的暗主题PNG图表，以便通过Telegram分享。支持`--window 24H|7D|30D`、`--output PATH`和`--json`参数。

### BMI分析工具的使用

BMI（BTC动量指数）是一个专有指标，用于确定市场趋势。

- **检查BMI**：`PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/btc_momentum.py --json`
- **通过openclaw发送BMI**：`OPENCLAW_NOTIFY_CHANNEL=<channel> OPENCLAW_NOTIFY_TARGET=<target> PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/btc_momentum.py --send`
- **运行警报工作流程**：`OPENCLAW_NOTIFY_CHANNEL=<channel> OPENCLAW_NOTIFY_TARGET=<target> PYTHONPATH={baseDir}/tools/bmi_alert.py`（如果市场方向发生变化，则发送警报）
- 如果`OPENCLAW_NOTIFY_CHANNEL`或`OPENCLAW_NOTIFY_TARGET`未设置，`--send`参数和`bmi_alert.py`会将消息打印到标准输出（stdout）。

`bmi_alert.py`脚本会读取`~/.openclaw/workspace/portfolio_tokens.json`文件，以便在警报消息中包含特定代币的表现。

### 投资组合图表工具的使用

`portfolio_chart.py`从原始交易历史记录生成累计未实现利润曲线，并保存适合Telegram分享的暗主题PNG图表（800×450像素）。投资组合ID会自动从`katbot_config.json`文件中加载。

- **生成7天图表（默认）**：
  ```bash
  PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/portfolio_chart.py
  ```
- **生成24小时图表**：
  ```bash
  PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/portfolio_chart.py --window 24H
  ```
- **生成30天图表**：
  ```bash
  PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/portfolio_chart.py --window 30D
  ```
- **JSON输出（供代理使用）**：
  ```bash
  PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/portfolio_chart.py --window 7D --json
  ```
  JSON输出包括：`chart_path`、`total_pnl_usd`、`total_pnl_pct`、`trade_fees_usd`、`trade_count`。
- **自定义输出路径**：
  ```bash
  PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/portfolio_chart.py --output /tmp/chart.png
  ```

默认输出路径：`~/.openclaw/workspace/portfolio_chart_{window}.png`

> **对贡献者的提示**：`scripts/`目录仅包含发布工具（`publish.sh`、`publish.py`等）。**不要**将工具脚本的副本添加到该目录中——所有交易逻辑都保存在`{baseDir}/tools/`中。

## 环境变量

**正常运行只需要`KATBOT_HL_AGENT_PRIVATE_KEY`。**该技能在首次设置后会自动从`katbot_secrets.json`文件中读取此密钥，因此在日常使用中无需在环境中设置。

`WALLET_PRIVATE_KEY` **不是**运行时的必需项**。它仅在访问令牌和刷新令牌都过期且需要完全重新建立会话时作为紧急备用方案使用。**绝不要**在环境中预先设置它——仅在首次设置或需要重新设置时交互式提供。

| 变量 | 需要时 | 描述 |
|----------|-------------|-------------|
| `KATBOT_HL_AGENT_PRIVATE_KEY` | 仅首次运行时（如果尚未设置） | 用于Hyperliquid交易执行的代理私钥。设置后，该密钥会保存到`katbot_secrets.json`文件中（权限设置为600）。之后，该技能会自动从秘密文件中加载它——**日常运行不需要环境变量**。 |
| `WALLET_PRIVATE_KEY` | 仅在紧急重新认证时使用 | MetaMask钱包密钥。仅在会话令牌完全过期时用于SIWE登录。**绝不要**在环境中预先设置它。仅在需要重新设置时交互式提供。 |
| `KATBOT_BASE_URL` | 可选覆盖 | API基础URL。默认值：`https://api.katbot.ai` |
| `KATBOT_IDENTITY_DIR` | 可选覆盖 | 身份文件目录路径。默认值：`~/.openclaw/workspace/katbot-identity` |
| `CHAIN_ID` | 可选覆盖 | EVM链ID。默认值：`42161`（Arbitrum） |
| `OPENCLAW_NOTIFY_CHANNEL` | 警报所需 | `btc_momentum.py --send`和`bmi_alert.py`的openclaw通道名称（例如`telegram`、`slack`、`discord`）。如果未设置，这两个工具会将消息打印到标准输出（stdout）并跳过发送。 |
| `OPENCLAW_NOTIFY_TARGET` | 警报所需 | 通道内的目标ID（例如聊天ID或用户昵称）。必须与`OPENCLAW_NOTIFY_CHANNEL`一起设置。 |

### `.env`文件加载器——仅用于CLI/开发

`katbot_client.py`包含一个`.env`文件加载器，用于OpenClaw之外的CLI使用（`tubman-bobtail-py`模式）。在导入时，它会搜索以下路径中的`katbot_client.env`文件：

1. `{projectRoot}/env/local/katbot_client.env`
2. `{baseDir}/../env/local/katbot_client.env`
3. `{baseDir}/tools/katbot_client.env`

如果找到文件，它只会从中加载**非敏感配置**：`KATBOT_BASE_URL`、`KATBOT_IDENTITY_DIR`和`CHAIN_ID`。私钥（`WALLET_PRIVATE_KEY`和`KATBOT_HL_AGENT_PRIVATE_KEY`）**绝不会**从`.env`文件中读取——它们必须来自环境或身份目录。

**代理规则：**
- **绝对**不要创建或建议创建包含私钥的`katbot_client.env`文件。
- **绝对**不要将`WALLET_PRIVATE_KEY`或`KATBOT_HL_AGENT_PRIVATE_KEY`放入任何`.env`文件中。
- `katbot_client.env`文件仅用于存储非敏感配置（`KATBOT_BASE_URL`、`CHAIN_ID`、`KATBOT_IDENTITY_DIR`、`PORTFOLIO_ID`、`WALLET_ADDRESS`）。

## 身份文件

所有持久性凭据都存储在`KATBOT_IDENTITY_DIR`（默认值：`~/.openclaw/workspace/katbot-identity/`）中。这个目录**故意**位于项目树之外——其内容永远不会被提交到git中。

| 文件 | 模式 | 内容 |
|------|------|----------|
| `katbot_config.json` | 644 | `base_url`、`wallet_address`、`portfolio_id`、`portfolio_name`、`chain_id` |
| `katbot_token.json` | 600 | `access_token`、`refresh_token` |
| `katbot_secrets.json` | 600 | `agent_private_key` |

`katbot_client.py`会自动读取这三个文件。如果环境中没有设置`KATBOT_HL_AGENT_PRIVATE_KEY`，则会从`katbot_secrets.json`文件中加载代理密钥。

**身份文件的安全属性：**
- `katbot_token.json`和`katbot_secrets.json`的权限设置为600（仅所有者可读/写）。
- `WALLET_PRIVATE_KEY`（MetaMask密钥）**永远不会**写入任何身份文件——它仅在设置和认证过程中使用于内存中。
- 如果`~/.openclaw/workspace/katbot-identity/`被泄露，攻击者将获得代理的交易密钥和会话令牌，但**不会**获得MetaMask钱包密钥，从而将攻击范围限制在通过Hyperliquid代理钱包可访问的资金范围内。

## 认证流程

该技能通过`katbot_client.get_token()`自动管理代币。**绝对不要**手动调用此函数——所有API函数都会在内部调用它。

1. **检查访问令牌**：从`katbot_token.json`中解码JWT的`exp`声明。如果有效（在60秒内未过期），则直接使用它。
2. **如果过期，则刷新**：如果访问令牌过期，请调用`POST /refresh`并传入`{"refresh_token": "<token>"`。API会在每次调用时**更新**刷新令牌——新的`access_token`和`refresh_token`会立即写入`katbot_token.json`（权限设置为600）。旧的刷新令牌在响应到达后立即失效。
3. **如果刷新失败，则重新认证**：如果刷新令牌缺失或`/refresh`调用失败，则通过`POST /login`进行完整的SIWE重新认证。这需要`WALLET_PRIVATE_KEY`。

**如果`/refresh`可以成功，则**绝对不要调用 `/login`。

刷新令牌是不可见的（不是JWT），并且在**7天不活动**后过期。如果会话完全过期，则需要重新进行设置。

## 凭据传输通知

> **代理必须在首次运行设置或任何交易操作之前向用户展示此通知并获得确认。**

该技能在某些调用中会将**代理的交易私钥**（`KATBOT_HL_AGENT_PRIVATE_KEY`）传输到远程Katbot API（`api.katbot.ai`）。这是为了让API能够代表您在Hyperliquid链上签署和提交交易。

**哪些凭据会离开您的机器以及何时传输：**

| 凭据 | 发送至 | 在哪些调用中 | 原因 |
|------------|---------|----------------|-----|
| `KATBOT_HL_AGENT_PRIVATE_KEY` | `api.katbot.ai` | `request_recommendation`、`execute_recommendation` — 在`X-Agent-Private-Key`头部和JSON请求体中 | Katbot API使用它来代表您在链上签署Hyperliquid交易 |
| `access_token` / `refresh_token` | `api.katbot.ai` | 所有经过认证的API调用 — 在`Authorization: Bearer`头部 | 用于会话认证 |
| `WALLET_PRIVATE_KEY` | 绝不会**远程发送** | 仅在设置或重新认证期间用于在本地签署SIWE消息 | 签名在本地计算；仅发送签名 |

**这意味着：**
- 代理的交易密钥是一个高价值的凭据。一旦传输，Katbot API服务器在整个请求期间都可以访问它。
- MetaMask钱包密钥（`WALLET_PRIVATE_KEY`）**永远不会**被传输——它仅在本地签名消息，并且只发送签名。
- 如果您不信任`api.katbot.ai`来处理您的代理交易密钥，请不要使用此技能。

**代理指令：**在首次运行设置或任何推荐/执行调用之前，告知用户：“此技能将把您的Hyperliquid代理私钥发送到api.katbot.ai以授权链上的交易。您是否继续？”在没有得到明确确认之前，请勿继续。

## `katbot_client.py` API参考

所有函数都需要一个从`get_token()`获取的`token`参数。

**下面使用的密钥传输说明：**
- `[key→remote]` — 代理私钥被发送到`api.katbot.ai`
- `[local only]` — 不传输私钥；仅发送JWT bearer令牌

### 认证 `[local only]`
```python
token = get_token()          # Returns valid access token (refreshes automatically)
config = get_config()        # Returns dict from katbot_config.json
```

### 用户账户 `[local only]`
```python
user_data = get_user(token)                       # Full user info: subscription, plan, feature_usage
status    = check_subscription_status(user_data)  # Evaluates subscription health + returns warnings
# status = {
#   "is_active": bool,
#   "is_expired": bool,
#   "expires_soon": bool,
#   "expires_very_soon": bool,
#   "days_remaining": int | None,
#   "hours_remaining": int | None,
#   "plan_tier": str,
#   "feature_usage": [{"feature_type": str, "usage_count": int,
#                      "limit_count": int, "limit_pct": float, "near_limit": bool}],
#   "warning_message": str | None,   # human-readable, None if healthy
#   "warnings": [str],               # individual warning strings
# }
```

### 投资组合 `[local only]`
```python
portfolios = list_portfolios(token)
portfolio  = get_portfolio(token, portfolio_id, window="1d")  # window: "1h","1d","7d","30d"
recs       = get_recommendations(token, portfolio_id)         # List existing recommendations

# For charting/PnL reconstruction — passes all three query params:
history = get_portfolio_history(
    token, portfolio_id,
    window="7D",       # "24H", "7D", or "30D"
    granularity="4h",  # "1h", "4h", "1d"
    limit=100,
)
# Returns: trades[], total_pnl_usd, total_pnl_pct, trade_fees_usd, etc.
```

### 推荐 `[key→remote]`
> 代理私钥在`X-Agent-Private-Key`头部和`request_recommendation`的JSON体中都被发送到`api.katbot.ai`。在调用之前请确认用户同意。

```python
ticket = request_recommendation(token, portfolio_id, message)  # [key→remote]
# ticket = {"ticket_id": "..."}

result = poll_recommendation(token, ticket["ticket_id"], max_wait=60)  # [local only]
# result = {"status": "COMPLETED"|"FAILED", "recommendation": {...}}
```

### 交易执行 `[key→remote]`
> 代理私钥在`X-Agent-Private-Key`头部和`execute_recommendation`的JSON体中都被发送到`api.katbot.ai`。在调用之前始终需要用户的明确确认。

```python
# [key→remote] — requires user confirmation
result = execute_recommendation(
    token, portfolio_id, rec_id,
    execute_onchain=False,        # True to submit directly to Hyperliquid
    user_master_address=None      # Optional: override wallet address
)

# [local only] — agent key sent only in header, not body
result = close_position(
    token, portfolio_id, "ETH",
    user_master_address=None      # Optional: override wallet address
)
```

### 聊天 `[local only]`
```python
ticket = chat(token, portfolio_id, "What's the market looking like?")
result = poll_chat(token, ticket["ticket_id"], max_wait=60)
# result = {"status": "COMPLETED"|"FAILED", "response": "..."}
```

### CLI模式
`katbot_client.py`可以作为独立脚本运行（从`.env`文件或环境中读取`PORTFOLIO_ID`）：

```bash
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py subscription-status
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py portfolio-state
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py recommendations
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py request-recommendation "Analyze and recommend"
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py poll-recommendation <ticket_id>
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py execute <rec_id>
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py close-position ETH
```

## 使用规则

- **每次会话开始时**始终检查订阅状态：先调用`get_user(token)`，然后调用`check_subscription_status(user_data)`。如果`is_expired`为True，告知用户他们的订阅已过期，并引导他们前往https://katbot.ai进行续订。如果`expires_very_soon`为True，紧急警告用户并引导他们前往https://katbot.ai。如果`expires_soon`为True，警告用户并引导他们前往https://katbot.ai进行扩展或升级。即使在自动化会话中，也不要抑制这些警告。
- **始终**从订阅状态中检查`feature_usage`——如果任何功能的`near_limit`为True，警告用户：“您已经使用了X/Y [feature]。请访问https://katbot.ai来升级您的计划。”
- **在每次设置或任何交易操作之前**始终展示凭据传输通知并获得用户的确认。
- **在建议新的交易之前**始终检查BMI。
- **要在Telegram上分享投资组合绩效**，运行`portfolio_chart.py --json`以获取图表PNG路径，然后使用`openclaw message send --channel <channel> --target <target> --file <chart_path>`发送。始终优先使用`--json`格式，以便代理可以读取路径。例如：`PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/portfolio_chart.py --window 7D --json`
- **绝对不要**在未经用户明确确认的情况下执行交易（例如，“确认执行LONG AAVE？”）。
- **绝对不要**在聊天中记录、打印或显示任何私钥或令牌值。
- **始终**报告任何推荐的收益/风险比率和杠杆率。
- **始终**让`get_token()`自动处理令牌刷新——不要手动管理令牌。
- **绝对不要**在环境中预先设置`WALLET_PRIVATE_KEY`。它仅用于紧急重新认证。如果代理在非活动设置/重新认证会话之外检测到环境中有此密钥，请警告用户并建议取消设置它。
- **绝对不要**创建包含`WALLET_PRIVATE_KEY`或`KATBOT_HL_AGENT_PRIVATE_KEY`的`katbot_client.env`文件。`.env`加载器不会将私钥注入进程，但在文件中存储私钥仍然是不好的做法，因为这会将秘密存储在磁盘上。
- **绝对不要**建议将任何私钥导出到shell配置文件或持久化环境文件中。
- **绝对不要**读取、显示或总结`katbot_token.json`、`katbot_secrets.json`或身份目录中的任何文件的内容。

## 环境管理

该技能使用`{baseDir}/.installed_version`文件来跟踪其安装的依赖项版本。当技能升级时，版本戳将不再与技能版本匹配，`ensure_env.sh`会自动重新运行`pip install`。

**代理必须在每次调用工具之前运行`ensure_env.sh`：**

```bash
bash {baseDir}/tools/ensure_env.sh {baseDir}
```

- 如果版本戳与当前版本匹配：立即退出（快速，无需调用pip）。
- 如果技能已升级或从未安装：运行`pip install -r requirements.txt`并写入新的版本戳。
- 如果缺少`python3`：显示清晰的错误并退出，代码为1。

如果某个工具因`ImportError`或`ModuleNotFoundError`而失败，请始终先运行`ensure_env.sh`以同步依赖项，然后再尝试。

## 首次设置（安装）

```bash
# 1. Install dependencies
bash {baseDir}/tools/ensure_env.sh {baseDir}

# 2. Run onboarding wizard (interactive)
python3 {baseDir}/tools/katbot_onboard.py
```

向导将：
1. 请求`WALLET_PRIVATE_KEY`（隐藏输入——永远不会存储到磁盘）。
2. 通过SIWE与api.katbot.ai进行身份验证。
3. 列出现有的投资组合或创建一个新的Hyperliquid投资组合。
4. 将`KATBOT_HL_AGENT_PRIVATE_KEY`、`katbot_config.json`和`katbot_token.json`保存到`~/.openclaw/workspace/katbot-identity/`。
5. 打印在Hyperliquid上授权代理钱包的说明。

设置完成后，该技能将使用保存的凭据自动运行。除非会话完全过期，否则不再需要`WALLET_PRIVATE_KEY`。

## 升级

当技能更新（新版本发布到clawhub）时：

```bash
# Re-run ensure_env.sh — it detects the version change and re-installs dependencies
bash {baseDir}/tools/ensure_env.sh {baseDir}
```

升级不需要重新设置。`~/.openclaw/workspace/katbot-identity/`中的身份文件将在升级过程中保持不变。如果某个工具在升级后失败，请先运行`ensure_env.sh`。