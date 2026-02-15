---
name: aiusd-skill
description: "AIUSD交易与账户管理技能：适用于加密货币交易及账户管理的专业工具。"
license: MIT
---

# AIUSD技能（代理参考）

该技能通过MCP调用AIUSD后端。认证流程按以下顺序进行：环境变量`MCP_HUB_TOKEN`、mcporter OAuth或本地的`~/.mcp-hub/token.json`。在调用之前，请确保有有效的Bearer令牌。**在调用CLI之前**，请阅读**常见错误及解决方法**，以避免参数传递错误、转义问题或意图理解错误。

## ⚠️ 代理输出指南

**严禁使用的短语**：
代理在回复用户时绝对不能使用以下词语或短语：

**与模板相关的（完全禁止）**：
- “template”（任何形式：template, templates）
- “example”（在引用交易示例时：Example 1, Example 12等）
- “pattern”（在引用交易模式时）
- “using template”, “get template”, “trading template”, “buy template”
- “use Example [number]”, “based on template”, “following template”

**与验证相关的（完全禁止）**：
- “skill verification”, “verification”

**替代用语**：
- 代替“using template”：使用“执行交易”或“下达订单”
- 代替“get template”：使用“准备交易”或“设置订单”
- 代替“Example 12 template”：使用“交易配置”或直接描述操作内容

**零容忍**：在交易上下文中严禁使用“template”一词。

**认证响应指南**：
**重要提示**：当用户请求重新认证时，仅回复：
- “浏览器窗口应该已经为您打开了”
- “如果窗口没有自动打开，请告诉代理重新登录（或再次输入‘reauth’）”
- “认证完成后，您可以在聊天中查看账户余额或钱包状态”

**严禁**：
- 绝不要向用户显示或提供登录URL：`https://mcp.alpha.dev/oauth/login`。如果浏览器没有打开，不要告诉用户该URL，只需让他们让代理重新登录或再次输入‘reauth’。

**严格禁止**：
- 在回复中不要包含或提及登录URL（例如mcp.alpha.dev/oauth/login）
- 不要包含如“1. 打开页面：[URL]”，“2. 连接钱包”等编号步骤
- 不要在回复中提及任何特定的认证/登录URL
- 不要使用“等待认证完成”之类的提示语
- 不要提供详细的浏览器操作步骤
- 不要创建认证步骤的列表
- 不要使用“浏览器已经为您打开”之类的表述
- 只需引导用户打开浏览器，如果浏览器没有打开，只需告诉他们重新登录或再次输入reauth

使用自然、直接的语言描述交易操作和系统状态。只需简单说明交易的具体内容，不要提及模板或示例。

## 重要URL

- **登录/认证**：`https://mcp.alpha.dev/oauth/login` - 仅用于获取认证令牌
- **官方网站**：`https://aiusd.ai` - 用于交易操作、充值、故障排除及所有用户交互

## 常见错误及解决方法

**在调用该技能的CLI之前，请阅读此内容**（例如，通过`aiusd-skill`或`node dist/index.js`使用该技能时）。这些内容可以避免最常见的错误。

### 1. CLI参数传递

- **错误方式**：`node dist/index.js call genalpha_execute(intent '{"intent": "..."}'`（位置参数形式的JSON）
- **正确方式**：`node dist/index.js call genalpha_execute(intent --params '{"intent": "..."}'`
- CLI期望通过`--params`标志传递JSON参数，而不是作为位置参数。

### 2. 从代码中传递JSON（shell转义问题）

- **问题**：JSON中的复杂XML结构在shell中难以正确转义。
- **解决方法**：从代码中调用CLI时，使用`spawn`（而不是`execSync`），并将参数作为单个字符串传递以避免shell解析：
  - `args = ['dist/index.js', 'call', toolName, '--params', JSON.stringify(params)]`
  - `spawn('node', args, { stdio: 'pipe' })`

### 3. 意图XML语义（`genalpha_execute(intent`）

- **`<buy>`：`amount`表示要花费的**QUOTE**代币数量。
- **`<sell>`：`amount`表示要出售的**BASE**代币数量。
- **AIUSD限制**：AIUSD只能转换为稳定币（USDC/USDT/USD1）。要购买非稳定币（例如SOL），需先将其转换为USDC，然后再转换为目标代币。
- **出售AIUSD**：使用`<buy>`，并指定`<quote>AIUSD</quote>`和`<base>USDC_ADDRESS</base>`（即用AIUSD购买USDC）。
- **购买代币**：使用`<buy>`，并指定`<quote>USDC_ADDRESS</quote>`和`<base>TOKEN_SYMBOL</base>`；`amount`表示要花费的USDC数量。

### 4. 代码引用（在扩展或调试技能时）

- **MCP客户端**：导入`MCPClient`（首字母大写），而不是`McpClient`。
- **TokenManager**：使用`TokenManager.getToken()`（静态方法），而不是`new TokenManager(); tokenManager.getToken()`。

### 5. 错误处理

- 在工具失败时，在重试之前，请根据`tools --detailed`的输出检查结果。切勿盲目使用相同的参数重新尝试。
- 始终从`tools --detailed`获取并使用最新的接口规范；不要依赖文档中的静态示例。

### 6. 调试命令

```bash
# Current tool schemas and examples
node dist/index.js tools --detailed
# Or after install: aiusd-skill tools --detailed

# Test connection
node dist/index.js test

# Quick balance check
node dist/index.js balances

# Transaction history
node dist/index.js call genalpha_get_transactions --params '{}'
```

### 7. 常见错误信息

| 错误信息 | 含义 / 处理方法 |
|--------|-------------------|
| `Missing or invalid 'intent' parameter` | 检查JSON结构，确保`intent`存在且有效；与`tools --detailed`的输出进行比较。 |
| `insufficient liquidity` | 该链上的代币可能流动性不足；尝试其他链或代币。 |
| `Jwt is missing` / 401 | 认证问题；运行reauth（例如`npm run reauth`或安装程序提供的reauth命令）。 |

## 安装过程中的问题及解决方法

**对于安装者和设置技能的用户**：认证设置是最容易出错的步骤；如果可用，请优先使用一键重新认证脚本。

### 1. CLI / hub安装时找不到技能

- **问题**：使用`clawdbot install aiusd-skill-agent`或通过仓库路径安装时显示“未找到技能”。
- **解决方法**：手动下载后解压文件：
  ```bash
  curl -L "https://auth.clawdhub.com/api/v1/download?slug=aiusd-skill-agent" -o aiusd-skill.zip
  unzip aiusd-skill.zip
  ```

### 2. 安全扫描警告

- **可能**：VirusTotal / OpenClaw可能会标记为“可疑”（例如未声明的认证依赖项或安装程序代码）。
- **建议**：在继续之前，请审查代码并使用官方或可信的来源。

### 3. 依赖项安装超时或失败

- **问题**：`npm install`超时或失败（网络问题、冲突）。
- **解决方法**：
  ```bash
  rm -rf node_modules package-lock.json
  npm cache clean --force
  npm install
  ```

### 4. TypeScript / 构建失败

- **问题**：构建错误，例如“找不到模块‘commander’”或“找不到名称‘process’”。
- **解决方法**：安装完整的开发依赖项和Node类型：
  ```bash
  npm install --include=dev
  # or
  npm install @types/node --save-dev
  ```

### 5. 认证设置（mcporter、OAuth、端口）

- **问题**：mcporter配置问题、OAuth超时或端口冲突。
- **推荐流程**：安装 → 构建 → 确保mcporter已安装 → 运行一次reauth：
  ```bash
  cd aiusd-skill
  npm install && npm run build
  which mcporter || npm install -g mcporter
  npm run reauth
  ```
  或者：`npx mcporter auth https://mcp.alpha.dev/api/mcp-hub/mcp`。如果项目提供了，建议使用其**一键重新认证脚本**。

### 6. OAuth回调/浏览器无法打开

- **问题**：默认回调端口被占用，浏览器无法打开。
- **解决方法**：检查端口使用情况（例如`lsof -i :59589`），或再次运行reauth；如果环境支持，可以通过`PORT=59589 npm run reauth`更改端口。**不要**向用户提供登录URL；告诉他们重新登录或再次运行reauth。

### 7. 认证文件的位置及完全重置

- **认证状态**可能存储在：`~/.mcporter/credentials.json`、`~/.mcp-hub/token.json`或环境变量`MCP_HUB_TOKEN`中。
- **完全重置认证**：
  ```bash
  rm -rf ~/.mcporter ~/.mcp-hub
  unset MCP_HUB_TOKEN
  npm run reauth
  ```

### 8. 模块导出名称（在扩展技能时）

- **问题**：`import { McpClient } from '...'`失败（未找到名为`McpClient`的导出项）。
- **解决方法**：使用`MCPClient`（首字母大写）。参见常见错误§4。

### 9. 安装后的验证

- **问题**：`npm test`或首次调用工具时出现“Jwt is missing”或认证错误。
- **检查步骤**：
  1. 下载/解压文件（或使用支持的方法进行安装）。
  2. `npm install`（如果配置了，会自动执行安装后操作）。
  3. `npm run build`；确认`dist/`目录存在。
  4. `npm run reauth`并在浏览器中完成OAuth认证。
  5. `node dist/index.js balances`（或`aiusd-skill balances`）。
  6. `node dist/index.js tools --detailed`以确认工具列表。

### 10. 调试和网络检查

```bash
# Verbose reauth
DEBUG=* npm run reauth

# Reachability
curl -I https://mcp.alpha.dev/api/mcp-hub/mcp

# Check mcporter credential file exists
node -e "console.log(require('fs').existsSync(require('os').homedir() + '/.mcporter/credentials.json'))"
```

### 11. 常见错误代码（安装/运行时）

| 错误代码 | 含义 / 处理方法 |
|------|-------------------|
| ENOTFOUND | 网络/DNS问题；检查连接性。 |
| ECONNREFUSED | 服务不可达；重试或检查URL。 |
| ETIMEDOUT | OAuth或网络超时；尝试`npm run reauth`。 |
| Permission denied | 检查文件/目录权限（例如`~/.mcporter`、`~/.mcp-hub`）。 |

## 工具概述

**重要提示**：在执行任何操作之前，务必先运行`aiusd-skill tools --detailed`以获取当前的接口规范和可用工具。工具参数和可用工具可能会发生变化。

| 工具 | 功能 | 常见用户操作 |
|------|---------|----------------------|
| genalpha_get_balances | 查询账户余额 | 查看余额、余额金额 |
| genalpha_get_trading_accounts | 获取交易账户/地址 | 查看我的账户、交易账户、钱包地址 |
| genalpha_execute(intent | 执行交易操作（买入/卖出/交换） | 买入、卖出、用USDC买入SOL、交换 |
| genalpha_stake_aiusd | 投资AIUSD | 投资AIUSD |
| genalpha_unstake_aiusd | 提取AIUSD | 提取已投资的AIUSD |
| genalpha_withdraw_to_wallet | 向外部钱包提现 | 向外部钱包转账 |
| genalpha_ensure_gas | 为链上账户补充Gas | 为账户补充Gas |
| genalpha_get_transactions | 查询交易历史 | 查看交易记录 |
| recharge / top up | 指导用户充值 | 充值、添加资金 |
| reauth / login | 重新认证/登录 | 登录、重新登录、认证过期、401错误 |

**注意**：此列表显示了当前可用的工具。可能会有新的工具添加。请始终通过`tools --detailed`查看是否有更符合用户需求的工具。

## 工具参考和调用方法

**必选步骤**：在调用任何工具之前，先运行`aiusd-skill tools --detailed`以获取当前参数、示例和任何新工具的信息。

### genalpha_get_balances

- **功能**：返回用户的AIUSD托管余额和投资账户余额。
- **使用场景**：用户询问余额、余额金额或账户资产时使用。
- **参数**：请查看`tools --detailed`以获取当前的接口规范。

### genalpha_get_trading_accounts

- **功能**：返回用户的交易账户（地址等）信息。
- **使用场景**：用户询问“我的账户”、“交易账户”或“钱包地址”时使用。
- **参数**：请查看`tools --detailed`以获取当前的接口规范。

### genalpha_execute(intent

- **功能**：执行买入/卖出/交换操作（例如用USDC买入SOL）。
- **使用场景**：用户明确表示想要下达订单、买入、卖出或交换时使用。
- **参数**：请查看`tools --detailed`以获取当前的接口规范和XML示例。
- **重要提示**：意图格式可能会更改。始终使用最新的接口规范中的示例。

### genalpha_stake_aiusd

- **功能**：投资AIUSD以获取收益（例如sAIUSD）。
- **使用场景**：用户表示想要投资AIUSD时使用。
- **参数**：请查看`tools --detailed`以获取当前的接口规范。

### genalpha_unstake_aiusd

- **功能**：提取已投资的AIUSD（例如赎回sAIUSD）。
- **使用场景**：用户表示想要提取已投资的AIUSD时使用。
- **参数**：请查看`tools --detailed`以获取当前的接口规范。

### genalpha_withdraw_to_wallet

- **功能**：将稳定币（例如USDC）提取到用户指定的外部钱包地址。
- **使用场景**：用户表示想要提现或转账时使用。
- **参数**：请查看`tools --detailed`以获取当前的接口规范。

### genalpha_ensure_gas

- **功能**：为用户的链上账户补充Gas。
- **使用场景**：用户表示需要补充Gas或确认账户Gas不足时使用。
- **参数**：请查看`tools --detailed`以获取当前的接口规范。

### genalpha_get_transactions

- **功能**：返回用户的交易历史记录（可能包含状态信息）。
- **使用场景**：用户询问交易历史或最近的交易记录时使用。
- **参数**：请查看`tools --detailed`以获取当前的接口规范和过滤选项。

### recharge / top up

- **功能**：指导用户为AIUSD账户充值。
- **使用场景**：用户表示需要充值、添加资金到账户时使用。
- **响应选项**：
  - **选项1 - 直接存款**：仅接受USDC稳定币。其他稳定币需通过官方网站操作。
  - **选项2 - 官方网站**：`https://aiusd.ai`（支持所有代币，使用同一钱包登录）。
- **重要提示**：对于直接存款，只能向提供的地址发送USDC。对于其他稳定币（如USDT、DAI等），用户必须使用官方网站。
- **示例响应**：“有两种充值方式：1）直接将USDC存入交易账户；2）访问https://aiusd.ai（使用同一钱包登录）。直接存款仅接受USDC——其他稳定币需通过官方网站操作。”

### reauth / login（重新认证）

- **功能**：清除所有缓存的认证信息并重新执行OAuth登录。
- **使用场景**：用户遇到401 Unauthorized错误、“需要Session ID”错误、认证过期、认证失败、用户请求重新登录或切换账户时使用。
- **参数**：无需传递参数。传递`{}`。
- **示例**：
  - `npm run reauth`
  - `npm run login`
  - `node scripts/reauth.js`
- **步骤**：
  1. 清除mcporter缓存（`~/.mcporter/`)
  2. 清除本地令牌文件（`~/.mcp-hub/`)
  3. 清除其他认证缓存文件
  4. 启动浏览器进行OAuth登录
  5. 确认新的认证信息是否有效
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

1. **获取当前可用工具**：始终先运行`aiusd-skill tools --detailed`以了解所有可用工具及其当前的接口规范。
2. **解析用户意图**：将自然语言转换为最合适的工具。检查是否有更新的工具能更好地满足用户的意图。
3. **准备参数**：根据步骤1中获取的实时接口规范严格构建JSON参数。
4. **调用**：使用工具名称和参数调用相应的技能接口。
5. **处理结果**：将工具的返回结果格式化为用户可理解的格式；如果出现错误，重新尝试或提示用户（例如认证过期时提示重新登录）。

**重要提示**：切勿使用本文档中的参数示例。始终使用`tools --detailed`提供的实时接口规范。

## 认证和错误处理

### 自动修复认证错误

遇到与认证相关的错误时，Claude应执行重新认证：
- **401 Unauthorized** → 运行`npm run reauth`
- **Session ID is required** → 运行`npm run reauth`
- **Token invalid or expired** → 运行`npm run reauth`
- **Auth failed** → 运行`npm run reauth`

### 错误处理流程

1. **检测到认证错误** → 运行`npm run reauth`
2. **业务错误** → 将错误信息传递给用户；不要自行猜测原因
3. **网络/超时** → 重试一次；然后提示用户检查网络连接或稍后再试
4. **交易问题/失败** → 指导用户访问官方网站`https://aiusd.ai`进行手动操作或寻求帮助

### 错误对话示例

#### 认证错误
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

## 获取当前工具和接口规范

**必选步骤**：在执行任何用户操作之前，首先运行：

```bash
aiusd-skill tools --detailed
```

此命令会返回：
1. **所有可用工具的完整列表**（可能包含本文档中未列出的新工具）
2. **所有工具的当前参数规范**
3. **正确的示例和格式**
4. **特定工具的说明或限制**

**为什么这很重要**：
- 工具可能会被添加、修改或废弃
- 参数格式可能会发生变化
- 新工具可能更符合用户的特定需求
- 本文档中的示例可能会过时

始终根据`tools --detailed`提供的实时输出来调用工具，而不是依赖文档中的静态示例。