---
name: katbot-trading
version: 0.2.16
description: 通过 Katbot.ai 在 Hyperliquid 平台上进行实时加密货币交易。该平台提供 BMI（市场分析工具）、代币选择功能以及基于人工智能的自动交易执行服务。
# Note: Homepage URL removed to avoid GitHub API rate limit errors during publish
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["python3"], "env": ["KATBOT_HL_AGENT_PRIVATE_KEY"] },
        "primaryEnv": "KATBOT_HL_AGENT_PRIVATE_KEY",
        "install": "pip install -r requirements.txt"
      }
  }
---
# Katbot交易技能

该技能教授代理如何使用Katbot.ai API来管理Hyperliquid交易投资组合。

## 功能

1. **市场分析**：检查BTC动量指数（BMI）以及24小时内的收益/亏损情况。
2. **代币选择**：根据当前市场趋势自动挑选最佳代币。
3. **交易建议**：获取基于AI的交易设置（入场价、止盈价、止损价、杠杆率）。
4. **执行交易**：在用户确认后，通过Hyperliquid平台执行和关闭交易。
5. **投资组合监控**：监控未平仓头寸、盈亏情况以及账户余额。
6. **聊天**：向投资组合代理发送自由格式的消息，并接收分析结果。

## 工具

所有工具脚本均存储在`{baseDir}/tools/`目录中——这是唯一的官方存储位置。项目中其他地方没有这些脚本的副本。请始终通过`{baseDir}/tools/<script>`引用工具，并设置`PYTHONPATH={baseDir}/tools`，以确保工具之间的导入能够正确进行。

依赖项列在`{baseDir}/requirements.txt`文件中：

- `ensure_env.sh`：在运行任何工具之前执行。检查当前技能版本所需的依赖项是否已安装，如有需要则重新安装。每次运行都是安全的——如果依赖项已经安装完毕，该脚本会立即退出。
- `katbot_onboard.py`：首次设置向导。通过SIWE使用您的钱包密钥进行身份验证，创建/选择投资组合，并将凭据保存到安全的身份目录中。
- `katbot_client.py`：核心API客户端。负责处理身份验证、代币刷新、投资组合管理、交易建议以及交易执行。也可以作为CLI脚本使用。
- `katbot_workflow.py`：端到端的交易工作流程（BMI → 代币选择 → 交易建议）。该脚本依赖于`katbot_client`和`token_selector`——需要设置`PYTHONPATH={baseDir}/tools`。
- `token_selector.py`：通过CoinGecko根据动量指标选择代币。

> **对贡献者的提示**：`scripts/`目录仅包含发布相关的工具（如`publish.sh`、`publish.py`等）。**请勿在该目录中添加工具脚本的副本**——所有交易逻辑都存储在`{baseDir}/tools/`中。

## 环境变量

**正常运行只需要`KATBOT_HL_AGENT_PRIVATE_KEY`。**该技能在完成首次设置后会自动从`katbot_secrets.json`文件中读取该密钥，因此在日常使用中无需在环境中设置它。

`WALLET_PRIVATE_KEY`不是运行时的必需项。它仅在访问令牌和刷新令牌都过期、需要完全重新建立会话时作为紧急备用方案使用。**切勿在环境中预先设置该密钥**——仅在首次设置或需要重新设置时才通过交互方式提供。

| 变量 | 使用场景 | 说明 |
|----------|-------------|-------------|
| `KATBOT_HL_AGENT_PRIVATE_KEY` | 仅首次运行时需要（如果尚未完成设置） | 用于Hyperliquid交易执行的代理私钥。设置完成后，该密钥会被保存到`katbot_secrets.json`文件中（权限设置为600）。之后，该技能会自动从该文件中加载该密钥——**日常运行无需设置环境变量**。 |
| `WALLET_PRIVATE_KEY` | 仅在紧急情况下需要重新认证时使用 | MetaMask钱包密钥。仅在会话令牌完全过期时用于SIWE登录。**切勿在环境中预先设置该密钥**。仅在需要重新设置时通过交互方式提供。 |
| `KATBOT_BASE_URL` | 可选覆盖项 | API基础URL。默认值：`https://api.katbot.ai` |
| `KATBOT_IDENTITY_DIR` | 可选覆盖项 | 身份文件目录的路径。默认值：`~/.openclaw/workspace/katbot-identity` |
| `CHAIN_ID` | 可选覆盖项 | EVM链ID。默认值：`42161`（Arbitrum） |

### `.env`文件加载器——仅用于CLI/开发环境

`katbot_client.py`包含一个`.env`文件加载器，用于OpenClaw之外的CLI环境（`tubman-bobtail-py`模式）。在导入时，它会搜索以下路径以查找`katbot_client.env`文件：

1. `{projectRoot}/env/local/katbot_client.env`
2. `{baseDir}/../env/local/katbot_client.env`
3. `{baseDir}/tools/katbot_client.env`

如果找到文件，它只会从中加载**非敏感配置**：`KATBOT_BASE_URL`、`KATBOT_IDENTITY_DIR`和`CHAIN_ID`。私钥（`WALLET_PRIVATE_KEY`和`KATBOT_HL_AGENT_PRIVATE_KEY`）**绝对不会**从`.env`文件中读取——它们必须来自环境或身份目录。

**代理规则：**
- **绝对不要**创建或建议创建包含私钥的`katbot_client.env`文件。
- **绝对不要**将`WALLET_PRIVATE_KEY`或`KATBOT_HL_AGENT_PRIVATE_KEY`放入任何`.env`文件中。
- `katbot_client.env`文件中只能包含非敏感配置（`KATBOT_BASE_URL`、`CHAIN_ID`、`KATBOT_IDENTITY_DIR`、`PORTFOLIO_ID`、`WALLET_ADDRESS`）。

## 身份文件

所有持久化凭据都存储在`KATBOT_IDENTITY_DIR`（默认路径：`~/.openclaw/workspace/katbot-identity/`）中。该目录**位于项目树之外**——其内容永远不会被提交到git仓库中。

| 文件 | 权限设置 | 内容 |
|------|------|----------|
| `katbot_config.json` | 644 | `base_url`、`wallet_address`、`portfolio_id`、`portfolio_name`、`chain_id` |
| `katbot_token.json` | 600 | `access_token`、`refresh_token` |
| `katbot_secrets.json` | 600 | `agent_private_key` |

`katbot_client.py`会自动读取这三个文件。如果环境中没有设置`KATBOT_HL_AGENT_PRIVATE_KEY`，则会从`katbot_secrets.json`中加载代理密钥。

**身份文件的安全属性：**
- `katbot_token.json`和`katbot_secrets.json`的权限设置为600（仅所有者可读写）。
- `WALLET_PRIVATE_KEY`（MetaMask密钥）**永远不会**被写入任何身份文件——它仅在设置和认证过程中以内存形式使用。
- 如果`~/.openclaw/workspace/katbot-identity/`目录被入侵，攻击者虽然可以获得代理的交易密钥和会话令牌，但**无法获取MetaMask钱包密钥**，从而将攻击范围限制在通过Hyperliquid代理钱包可访问的资金范围内。

## 认证流程

该技能通过`katbot_client.get_token()`自动管理代币。**切勿手动调用此函数**——所有API函数都会内部调用它。

1. **检查访问令牌**：从`katbot_token.json`中解码JWT的`exp`字段。如果有效（在60秒内未过期），则直接使用该令牌。
2. **令牌过期时刷新**：如果访问令牌过期，使用`{"refresh_token": "<token>"}`调用`POST /refresh`。API会在每次调用时更新刷新令牌——新的`access_token`和`refresh_token`会立即写入`katbot_token.json`文件（权限设置为600）。旧刷新令牌在响应返回后立即失效。
3. **刷新失败时重新认证**：如果刷新令牌丢失或`/refresh`调用失败，将通过`POST /login`进行完整的SIWE重新认证。这需要`WALLET_PRIVATE_KEY`。

**如果`/refresh`调用可以成功，请****切勿**调用`/login`。

刷新令牌是不可见的（非JWT格式），并且在**7天未使用后过期**。如果会话完全过期，则需要重新执行设置流程。

## 凭据传输说明

> **代理在首次运行设置或任何交易操作之前，必须向用户展示此说明并获得用户的确认。**

该技能会在某些调用中向远程Katbot API（`api.katbot.ai`）传输**代理的交易私钥**（`KATBOT_HL_AGENT_PRIVATE_KEY`）。这是API通过Hyperliquid在链上签署和提交交易所必需的。

**哪些凭据会离开您的机器以及何时传输：**

| 凭据 | 发送目标 | 传输场景 | 原因 |
|------------|---------|----------------|-----|
| `KATBOT_HL_AGENT_PRIVATE_KEY` | `api.katbot.ai` | `request_recommendation`、`execute_recommendation`——在`X-Agent-Private-Key`头部和JSON请求体中 | Katbot API使用该密钥代表您在链上签署Hyperliquid交易 |
| `access_token` / `refresh_token` | `api.katbot.ai` | 所有经过认证的API调用——在`Authorization: Bearer`头部中 | 用于会话认证 |
| `WALLET_PRIVATE_KEY` | 从不远程发送 | 仅在设置/重新认证过程中用于在本地签署SIWE消息 | 签名在本地计算；仅发送签名结果 |

**这意味着：**
- 代理的交易密钥是高价值的凭据。一旦传输，Katbot API服务器在整个请求期间都可以访问该密钥。
- MetaMask钱包密钥（`WALLET_PRIVATE_KEY**）**永远不会**被传输——它仅在设置和认证过程中以内存形式使用。
- 如果您不信任`api.katbot.ai`来处理您的代理交易密钥，请不要使用此技能。

**代理操作说明：**在首次运行设置或会话中的任何推荐/执行调用之前，务必告知用户：“此技能将把您的Hyperliquid代理私钥发送到api.katbot.ai以授权链上交易。您是否继续？”**未经用户明确确认，请勿继续。

## `katbot_client.py` API参考

所有函数都需要从`get_token()`获取的`token`参数。

**以下是用于说明密钥传输方式的标记：**
- `[key→remote]` — 代理私钥被发送到`api.katbot.ai`
- `[local only]` — 无需传输私钥；仅发送JWT承载令牌

### 认证 `[local only]`
```python
token = get_token()          # Returns valid access token (refreshes automatically)
config = get_config()        # Returns dict from katbot_config.json
```

### 投资组合 `[local only]`
```python
portfolios = list_portfolios(token)
portfolio  = get_portfolio(token, portfolio_id, window="1d")  # window: "1h","1d","7d","30d"
recs       = get_recommendations(token, portfolio_id)         # List existing recommendations
```

### 交易建议 `[key→remote]`
> 代理私钥会在`X-Agent-Private-Key`头部和`request_recommendation`的JSON体中发送到`api.katbot.ai`。在调用之前请确认用户同意。

```python
ticket = request_recommendation(token, portfolio_id, message)  # [key→remote]
# ticket = {"ticket_id": "..."}

result = poll_recommendation(token, ticket["ticket_id"], max_wait=60)  # [local only]
# result = {"status": "COMPLETED"|"FAILED", "recommendation": {...}}
```

### 交易执行 `[key→remote]`
> 代理私钥会在`X-Agent-Private-Key`头部和`execute_recommendation`的JSON体中发送到`api.katbot.ai`。调用之前必须获得用户的明确确认。

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
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py portfolio-state
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py recommendations
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py request-recommendation "Analyze and recommend"
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py poll-recommendation <ticket_id>
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py execute <rec_id>
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py close-position ETH
```

## 使用规则

- **在任何会话中的首次设置或交易操作之前，****必须**向用户展示凭据传输说明并获得用户的确认。
- **在建议新的交易之前，****必须**检查BMI。
- **未经用户明确确认，****绝对不要**执行交易（例如：“确认执行LONG AAVE？”）。
- **绝对不要**在聊天中记录、打印或显示任何私钥或代币信息。
- **必须**始终报告任何交易建议的风险/回报比率和杠杆率。
- **必须**始终让`get_token()`自动处理代币刷新——不要手动管理代币。
- **绝对不要**在环境中预先设置`WALLET_PRIVATE_KEY`。它仅用于紧急情况下的重新认证。如果代理发现环境中的`WALLET_PRIVATE_KEY`是在非活动设置/重新认证会话期间预先设置的，应警告用户并要求其取消设置。
- **绝对不要**创建包含`WALLET_PRIVATE_KEY`或`KATBOT_HL_AGENT_PRIVATE_KEY`的`katbot_client.env`文件。`.env`加载器不会将私钥注入进程，但将私钥保存在文件中仍然是一个不良做法，因为这会导致秘密信息不必要的存储。
- **绝对不要**建议将任何私钥导出到shell配置文件或持久化环境文件中。
- **绝对不要**读取、显示或总结`katbot_token.json`、`katbot_secrets.json`或身份目录中的任何文件内容。

## 环境管理

该技能使用`{baseDir}/.installed_version`文件来跟踪其安装的依赖项版本。当技能升级时，文件中的版本号将与技能版本不匹配，`ensure_env.sh`会自动重新运行`pip install`。

**代理在每次使用工具之前必须运行`ensure_env.sh`：**

```bash
bash {baseDir}/tools/ensure_env.sh {baseDir}
```

- 如果文件中的版本号与当前版本匹配：立即退出（快速完成，无需执行`pip`命令）。
- 如果技能已升级或从未安装：运行`pip install -r requirements.txt`并更新文件中的版本号。
- 如果缺少`python3`，会显示明确错误并退出（退出代码为1）。

如果某个工具因`ImportError`或`ModuleNotFoundError`而失败，请始终先运行`ensure_env.sh`以同步依赖项，然后再尝试。

## 首次设置（安装）

```bash
# 1. Install dependencies
bash {baseDir}/tools/ensure_env.sh {baseDir}

# 2. Run onboarding wizard (interactive)
python3 {baseDir}/tools/katbot_onboard.py
```

设置向导将：
1. 请求用户输入`WALLET_PRIVATE_KEY`（该密钥不会被保存到磁盘）。
2. 通过SIWE使用api.katbot.ai进行身份验证。
3. 列出现有的投资组合或创建一个新的Hyperliquid投资组合。
4. 将`KATBOT_HL_AGENT_PRIVATE_KEY`、`katbot_config.json`和`katbot_token.json`保存到`~/.openclaw/workspace/katbot-identity/`。
5. 显示在Hyperliquid上授权代理钱包的说明。

设置完成后，该技能将使用保存的凭据自动运行。除非会话完全过期，否则不再需要`WALLET_PRIVATE_KEY`。

## 升级

当技能更新（新版本发布到clawhub）时：

```bash
# Re-run ensure_env.sh — it detects the version change and re-installs dependencies
bash {baseDir}/tools/ensure_env.sh {baseDir}
```

升级时无需重新设置。`~/.openclaw/workspace/katbot-identity/`中的身份文件会在升级后保持不变。如果某个工具在升级后出现故障，请先运行`ensure_env.sh`。