---
name: aiusd-skill
description: AIUSD交易与账户管理技能：通过MCP调用后端服务，实现余额查询、交易操作、质押功能、提款、燃气（gas）充值以及交易历史记录的查询。认证优先级如下：首先使用MCP_HUB_TOKEN环境变量进行认证，若该环境变量无效，则使用mcporter OAuth或本地令牌文件进行认证。
---

# AIUSD技能（代理参考）

该技能通过MCP调用AIUSD后端。身份验证的顺序如下：环境变量`MCP_HUB_TOKEN`、mcporter OAuth或本地文件`~/.mcp-hub/token.json`。在调用之前，请确保有有效的Bearer令牌。

## ⚠️ 代理输出指南

**严禁使用的短语**：
代理在回应用户时绝对不能使用以下词语或短语：

**与模板相关的（完全禁止）**：
- “template”（任何形式：template, templates）
- “example”（在引用交易示例时：Example 1, Example 12等）
- “pattern”（在引用交易模式时）
- “using template”, “get template”, “trading template”, “buy template”
- “use Example [number]”, “based on template”, “following template”

**与验证相关的（完全禁止）**：
- “skill verification”, “verification”

**替代用语**：
- 代替“using template”使用“执行交易”或“下单”
- 代替“get template”使用“准备交易”或“设置订单”
- 代替“Example 12 template”使用“交易配置”或直接描述操作

**零容忍**：在交易场景中严禁使用“template”一词。

**身份验证响应指南**：
**重要**：当用户请求重新认证时，仅回复：
- “请在浏览器中完成身份验证”
- “如果浏览器没有自动打开，请再次输入‘reauth’”
- “完成身份验证后，您可以在聊天中查看账户余额或钱包状态”

**严格禁止**：
- 不要包含如“1. 打开页面：[URL]”之类的编号步骤
- 不要在响应中提及任何特定URL（URL可能不正确）
- 不要使用“等待身份验证完成”之类的等待语句
- 不要提供详细的浏览器操作步骤
- 不要创建带编号的身份验证步骤列表
- 不要使用“浏览器已为您打开”之类的表述
- 直接引导用户到浏览器，并告知他们完成操作后可以做什么

使用自然、直接的语言描述交易操作和系统状态。只需简单描述交易内容，不要提及模板或示例。

## 重要URL

- **登录/身份验证**：`https://mcp.alpha.dev/oauth/login` - 仅用于获取身份验证令牌
- **官方网站**：`https://aiusd.ai` - 用于交易操作、充值、故障排除及所有用户交互

## 工具概述

**重要**：在调用任何工具之前，务必先运行`aiusd-skill tools --detailed`以获取当前的实时架构和可用工具。工具参数和可用工具可能会发生变化。

| 工具 | 用途 | 常见用户意图 |
|------|---------|----------------------|
| genalpha_get_balances | 查询账户余额 | 余额、金额、账户资产 |
| genalpha_get_trading_accounts | 获取交易账户/地址 | 我的账户、交易账户、钱包地址 |
| genalpha_execute(intent | 执行交易意图（买入/卖出/交换） | 买入、卖出、用USDC买入SOL、交换 |
| genalpha_stake_aiusd | 投资AIUSD | 投资AIUSD |
| genalpha_unstake_aiusd | 提取AIUSD | 提取投资 |
| genalpha_withdraw_to_wallet | 提取到外部钱包 | 提取资金 |
| genalpha_ensure_gas | 为链上账户补充Gas | 补充Gas、确保Gas足够 |
| genalpha_get_transactions | 查询交易历史 | 历史记录、最近的交易 |
| recharge / top up | 指导用户充值账户 | 充值、添加资金 |
| reauth / login | 重新认证/登录 | 登录、重新登录、认证过期、401错误 |

**注意**：此列表显示了常用的工具。可能会有新的工具添加。请始终运行`tools --detailed`以发现可能更符合用户特定需求的工具。

## 工具参考和调用用法

**强制要求**：在调用任何工具之前，先运行`aiusd-skill tools --detailed`以获取当前参数、示例和任何新工具的信息。

### genalpha_get_balances

- **用途**：返回用户的AIUSD托管余额和投资账户余额。
- **使用场景**：用户询问余额、金额或账户资产。
- **参数**：请查看`tools --detailed`以获取当前参数格式。

### genalpha_get_trading_accounts

- **用途**：返回用户的交易账户（地址等）。
- **使用场景**：用户询问“我的账户”、“交易账户”或“钱包地址”。
- **参数**：请查看`tools --detailed`以获取当前参数格式。

### genalpha_execute(intent

- **用途**：执行买入/卖出/交换操作（例如用USDC买入SOL、卖出ETH）。
- **使用场景**：用户明确表示想要下单、买入、卖出或交换。
- **参数**：请查看`tools --detailed`以获取当前参数格式和XML示例。
- **重要**：意图格式可能会更改。始终使用实时架构中的示例。

### genalpha_stake_aiusd

- **用途**：投资AIUSD以获取收益（例如sAIUSD）。
- **使用场景**：用户表示想要投资AIUSD。
- **参数**：请查看`tools --detailed`以获取当前参数格式。

### genalpha_unstake_aiusd

- **用途**：提取AIUSD投资（例如赎回sAIUSD）。
- **使用场景**：用户表示想要提取投资。
- **参数**：请查看`tools --detailed`以获取当前参数格式。

### genalpha_withdraw_to_wallet

- **用途**：将稳定币（例如USDC）提取到用户指定的外部钱包地址。
- **使用场景**：用户表示想要提取资金。
- **参数**：请查看`tools --detailed`以获取当前参数格式。

### genalpha_ensure_gas

- **用途**：为用户的链上账户补充Gas。
- **使用场景**：用户表示需要补充Gas或链上的Gas不足。
- **参数**：请查看`tools --detailed`以获取当前参数格式。

### genalpha_get_transactions

- **用途**：返回用户的交易历史记录（可能包含状态）。
- **使用场景**：用户询问历史记录、最近的交易或订单状态。
- **参数**：请查看`tools --detailed`以获取当前参数格式和过滤选项。

### recharge / top up

- **用途**：指导用户为AIUSD账户充值。
- **使用场景**：用户表示想要充值、添加资金到账户。
- **响应选项**：
  - **选项1 - 直接存款**：仅接受USDC稳定币。其他稳定币需通过官方网站操作。
  - **选项2 - 官方网站**：`https://aiusd.ai`（支持所有代币，使用同一钱包登录）。
- **重要**：对于直接存款，仅接受USDC到提供的地址。对于其他稳定币（USDT、DAI等），用户必须使用官方网站。
- **示例响应**：“您有两种充值方式：1）直接将USDC存入交易账户；2）访问https://aiusd.ai（使用同一钱包登录）。直接存款仅接受USDC——其他稳定币需通过官方网站操作。”

### reauth / login（重新认证）

- **用途**：清除所有缓存的身份验证信息并重新运行OAuth登录。
- **使用场景**：用户遇到401 Unauthorized错误、“需要Session ID”、令牌过期、认证失败、用户请求重新登录或切换账户时使用。
- **参数**：无需传递参数。传递`{}`。
- **示例**：
  - `npm run reauth`
  - `npm run login`
  - `node scripts/reauth.js`
- **步骤**：
  1. 清除mcporter缓存（`~/.mcporter/`)
  2. 清除本地令牌文件（`~/.mcp-hub/`)
  3. 清除其他身份验证缓存文件
  4. 开始浏览器OAuth登录
  5. 验证新的身份验证是否生效
- **示例对话**：
  ```
  User: "I'm getting 401"
  Claude: Looks like an auth issue; re-authenticating...
  [Run: npm run reauth]
  Claude: Re-auth done; you can use the skill again.

  User: "Re-login"
  Claude: Clearing cache and re-logging in...
  [Run: npm run login]
  ```

## 使用流程（代理推理）

1. **获取当前工具**：始终先运行`aiusd-skill tools --detailed`以了解所有可用工具及其当前参数格式。
2. **解析意图**：将自然语言转换为最合适的工具。检查是否有新的工具更符合用户的意图。
3. **准备参数**：严格根据步骤1中获取的实时参数格式构建JSON参数。
4. **调用**：使用工具名称和参数调用技能接口。
5. **处理结果**：将工具的JSON或文本结果格式化后提供给用户；如果出现错误，重试或提示用户（例如认证过期 → 提示重新登录）。

**重要**：切勿使用本文档中的参数示例。始终使用`tools --detailed`提供的实时参数格式。

## 身份验证和错误处理

### 自动修复身份验证错误

在身份验证相关错误时，Claude应执行重新认证：
- **401 Unauthorized** → 运行`npm run reauth`
- **Session ID is required** → 运行`npm run reauth`
- **Token invalid or expired** → 运行`npm run reauth`
- **Auth failed** → 运行`npm run reauth`

### 错误处理流程

1. **检测身份验证错误** → 运行`npm run reauth`
2. **业务错误** → 将服务器错误告知用户；不要自行猜测原因
3. **网络/超时** → 重试一次；然后提示用户检查网络或稍后再试
4. **交易问题/失败** → 将用户引导至官方网站`https://aiusd.ai`进行手动操作和支持

### 错误对话示例

#### 身份验证错误
```
User: "Check balance"
[Tool returns 401]
Claude: Auth expired; re-authenticating...
[Run: npm run reauth]
Claude: Re-auth done. Fetching balance...
[Call: genalpha_get_balances]
```

#### 交易错误
```
User: "Buy 100 USDC worth of SOL"
[Tool returns trading error]
Claude: I encountered an issue with the trade execution. For manual trading operations, please visit https://aiusd.ai and use the same wallet you use for authentication.
```

## 获取当前工具和参数格式

**必先执行的步骤**：在执行任何用户操作之前，运行：

```bash
aiusd-skill tools --detailed
```

该命令返回：
1. **所有可用工具的完整列表**（可能包含本文档中未列出的新工具）
2. **所有工具的当前参数格式**
3. **有效的示例和正确的格式**
4. **特定工具的说明或限制**

**为什么这很重要**：
- 工具可能会被添加、修改或弃用
- 参数格式可能会更改
- 新工具可能更适合特定的用户需求
- 本文档中的示例可能会过时

始终根据`tools --detailed`提供的实时输出来调用工具，而不是依赖文档中的静态示例。