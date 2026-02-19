---
name: emblem-ai-agent-wallet
description: 通过 Emblem AI - Agent Hustle 连接到 EmblemVault 并管理加密钱包。支持 Solana、Ethereum、Base、BSC、Polygon、Hedera 和 Bitcoin 等区块链平台。适用于用户需要进行加密货币交易、查看余额、交换代币或与区块链钱包交互的场景。
homepage: https://emblemvault.dev
user-invocable: true
metadata: {"openclaw":{"emoji":"🛡️","version":"3.0.8","homepage":"https://emblemvault.dev","primaryEnv":"EMBLEM_PASSWORD","requires":{"bins":["node","npm","emblemai"],"env":["EMBLEM_PASSWORD"]},"config_paths":["~/.emblemai/.env","~/.emblemai/.env.keys","~/.emblemai/session.json","~/.emblemai/history/"],"install":[{"id":"npm","kind":"npm","package":"@emblemvault/agentwallet","bins":["emblemai"],"label":"Install Agent Wallet CLI"}]}}
---
# Emblem Agent Wallet

**连接至** **Agent Hustle** – EmblemVault 的自主加密 AI，支持 7 个区块链上的 250 多种交易工具。支持浏览器身份验证、实时响应、插件系统以及无需配置的代理模式。

**需要安装 CLI：** `npm install -g @emblemvault/agentwallet`

---

## 快速入门 – 如何使用此技能

**步骤 1：安装 CLI**

```bash
npm install -g @emblemvault/agentwallet
```

该 CLI 提供一个命令：`emblemai`

**步骤 2：使用它**

当此技能加载后，您可以向 Agent Hustle 提出关于加密货币的任何问题：

- “我的钱包地址是什么？”
- “显示我在所有链上的余额”
- “Solana 上哪些代币正在上涨？”
- “将 20 美元的 SOL 换成 USDC”
- “向 0x... 发送 0.1 ETH”

**要调用此技能，请输入如下命令：**
- “使用我的 Emblem 钱包查看余额”
- “询问 Agent Hustle 我有哪些代币”
- “连接至 EmblemVault”
- “查看我的加密货币投资组合”

所有请求都会通过 `emblemai` 进行处理。

---

## 先决条件

- **Node.js** >= 18.0.0
- 支持 256 色显示的终端（iTerm2、Kitty、Windows Terminal 或任何兼容 xterm 的终端）
- **可选**：[glow](https://github.com/charmbracelet/glow) 用于丰富的 Markdown 渲染（在 macOS 上使用 `brew install glow`）

## 安装

### 通过 npm 安装（推荐）

```bash
npm install -g @emblemvault/agentwallet
```

### 从源代码安装

```bash
git clone https://github.com/EmblemCompany/EmblemAi-AgentWallet-Plugins.git
cd EmblemAi-AgentWallet-Plugins/cli
npm install
npm link   # makes `emblemai` available globally
```

## 首次运行

1. 安装：`npm install -g @emblemvault/agentwallet`
2. 运行：`emblemai`
3. 在浏览器中登录（或按提示输入密码）
4. 查看 `/plugins` 以查看已加载的插件
5. 输入 `/help` 以查看所有命令
6. 尝试输入：“我的钱包地址是什么？”以验证登录是否成功

---

## 身份验证

EmblemAI v3 支持两种身份验证方法：**浏览器身份验证**（用于交互式使用）和 **密码身份验证**（用于代理/脚本化使用）。

### 浏览器身份验证（交互模式）

当您不使用 `-p` 参数运行 `emblemai` 时，CLI 会：

1. 检查 `~/.emblemai/session.json` 文件中是否有保存的会话
2. 如果存在有效（未过期）的会话，则立即恢复会话——无需重新登录
3. 如果没有会话，则在 `127.0.0.1:18247` 上启动本地服务器并打开浏览器
4. 您通过浏览器中的 EmblemVault 身份验证模块进行身份验证
5. 会话 JWT 会被捕获并保存到磁盘上，然后 CLI 继续运行
6. 如果浏览器无法打开，会显示 URL 供您手动复制粘贴
7. 如果身份验证超时（5 分钟），则切换到密码输入界面

### 密码身份验证（代理模式）

**登录和注册是相同的操作。** 第一次使用密码会创建一个钱包；后续使用相同的密码会访问同一个钱包。不同的密码会生成不同的钱包。

在代理模式下，如果未提供密码，系统会自动生成一个安全的随机密码并通过 `.env` 文件加密存储。代理模式无需手动设置即可使用。

### 身份验证过程

1. **浏览器身份验证**：从浏览器接收 JWT 会话令牌并将其传递给 SDK
2. **密码身份验证**：密码会被发送到 `EmblemAuthSDK.authenticatePassword()`
3. 生成一个确定的钱包配置——相同的凭据始终会生成相同的钱包
4. 会话会提供多个链上的钱包地址：Solana、Ethereum、Base、BSC、Polygon、Hedera、Bitcoin
5. 使用会话配置初始化 `HustleIncognitoClient`

### 凭据获取方式

在发送请求之前，凭据的获取优先级如下：

| 方法 | 使用方式 | 优先级 |
|--------|-----------|----------|
| CLI 参数 | `emblemai -p "your-password"` | 1（最高优先级，已加密存储） |
| 环境变量 | `export EMBLEM_PASSWORD="your-password"` | 2（不存储） |
| `.env` 文件中的加密凭据 | `.env` 文件中的加密凭据 | 3 |
| 自动生成（代理模式） | 首次运行时自动生成 | 4 |
| 交互式提示 | 浏览器身份验证失败时的备用方式 | 5（最低优先级） |

如果找不到凭据，系统会提示用户：
> “我需要您的 EmblemVault 密码来连接至 Hustle AI。此密码必须至少包含 16 个字符。”

> **注意：** 如果这是您第一次使用，输入新密码将创建一个新的钱包。如果您之前使用过该服务，请使用相同的密码来访问现有钱包。
> “您是否要提供密码？”

- 密码必须包含 16 个或更多字符
- 丢失密码后无法恢复（请将其视为私钥）

---

## 执行注意事项

**请等待足够的时间。** 复杂操作（如交易、跨链查询）可能需要最多 2 分钟的时间。CLI 每 5 秒会显示一个进度点，以表明正在处理中。

**清晰地展示 Hustle AI 的响应。** 将 Hustle AI 的响应以 Markdown 代码块的形式显示给用户：

```markdown
**Hustle AI Response:**
\`\`\`
[response from Hustle]
\`\`\`
```

---

## 使用方法

### 代理模式（用于 AI 代理——单次查询）

使用 `--agent` 模式进行程序化、单条消息的查询：

```bash
# Zero-config -- auto-generates password on first run
emblemai --agent -m "What are my wallet addresses?"

# Explicit password
emblemai --agent -p "$PASSWORD" -m "Show my balances"

# Pipe output to other tools
emblemai -a -m "What is my SOL balance?" | jq .

# Use in scripts
ADDRESSES=$(emblemai -a -m "List my addresses as JSON")
```

任何可以调用 CLI 的系统都可以为其代理分配一个钱包：

```bash
# OpenClaw, CrewAI, AutoGPT, or any agent framework
emblemai --agent -m "Send 0.1 SOL to <address>"
emblemai --agent -m "Swap 100 USDC to ETH on Base"
emblemai --agent -m "What tokens do I hold across all chains?"
```

每个密码都会生成一个唯一的、确定的钱包。如果需要为多个代理分配不同的钱包，请使用不同的密码：

```bash
emblemai --agent -p "agent-alice-wallet-001" -m "My addresses?"
emblemai --agent -p "agent-bob-wallet-002" -m "My addresses?"
```

代理模式始终使用密码身份验证（从不使用浏览器身份验证），会保留调用之间的对话历史记录，并支持完整的 Hustle AI 工具集，包括交易、转账、投资组合查询和跨链操作。

### 交互模式（用于人类用户）

基于命令行的交互模式，支持实时 AI 响应、glow Markdown 渲染以及斜杠命令。

```bash
emblemai              # Browser auth (recommended)
emblemai -p "$PASSWORD"  # Password auth
```

### 重置对话记录

```bash
emblemai --reset
```

---

## 交互命令

所有命令都以 `/` 为前缀。在输入框中输入命令并按 Enter 键执行。

### 常用命令

| 命令 | 描述 |
|---------|-------------|
| `/help` | 显示所有可用命令 |
| `/settings` | 显示当前配置（钱包 ID、模型、实时显示、调试、工具） |
| `/exit` | 退出 CLI（也称为 `/quit` |

### 聊天和历史记录

| 命令 | 描述 |
|---------|-------------|
| `/reset` | 清除对话记录并重新开始 |
| `/clear` | `/reset` 的别名 |
| `/history on\|off` | 切换消息的历史记录保留状态 |
| `/history` | 显示历史记录状态和最近的消息 |

### 实时显示和调试

| 命令 | 描述 |
|---------|-------------|
| `/stream on\|off` | 切换实时显示模式（代币以生成的形式显示） |
| `/stream` | 显示当前的实时显示状态 |
| `/debug on\|off` | 切换调试模式（显示工具参数和意图上下文） |
| `/debug` | 显示当前的调试状态 |

### 模型选择

| 命令 | 描述 |
|---------|-------------|
| `/model <id>` | 通过 ID 设置活动模型 |
| `/model clear` | 重置为 API 默认模型 |
| `/model` | 显示当前选定的模型 |

### 工具管理

| 命令 | 描述 |
|---------|-------------|
| `/tools` | 列出所有工具及其启用状态 |
| `/tools add <id>` | 将工具添加到活动工具集中 |
| `/tools remove <id>` | 从活动工具集中移除工具 |
| `/tools clear` | 清除工具选择（启用自动工具模式） |

当没有选择工具时，AI 会自动选择合适的工具（**自动工具模式**）。

### 身份验证

| 命令 | 描述 |
|---------|-------------|
| `/auth` | 打开身份验证菜单 |
| `/wallet` | 显示钱包地址（EVM、Solana、BTC、Hedera） |
| `/portfolio` | 显示投资组合（以聊天查询的形式显示） |

`/auth` 菜单提供以下选项：

| 选项 | 描述 |
|--------|-------------|
| 1. 获取 API 密钥 | 获取您的钱包 API 密钥 |
| 2. 获取钱包信息 | 显示钱包 ID、地址、创建日期 |
| 3. 会话信息 | 显示当前会话详情（标识符、有效期、身份验证类型） |
| 4. 刷新会话 | 刷新身份验证会话令牌 |
| 5. EVM 地址 | 显示您的 Ethereum/EVM 地址 |
| 6. Solana 地址 | 显示您的 Solana 地址 |
| 7. BTC 地址 | 显示您的 Bitcoin 地址（P2PKH、P2WPKH、P2TR） |
| 8. 备份代理身份验证 | 将凭据导出到备份文件 |
| 9. 登出 | 清除会话并退出（下次运行时需要重新登录） |

### 支付（PAYG 计费）

| 命令 | 描述 |
|---------|-------------|
| `/payment` | 显示 PAYG 计费状态（是否启用、模式、债务、代币） |
| `/payment enable\|disable` | 切换按次计费模式 |
| `/payment token <TOKEN>` | 设置支付令牌（SOL、ETH、HUSTLE 等） |
| `/payment mode <MODE>` | 设置支付模式：`pay_per_request` 或 `debt_accumulation` |

### Markdown 渲染

| 命令 | 描述 |
|---------|-------------|
| `/glow on\|off` | 切换通过 glow 的 Markdown 渲染 |
| `/glow` | 显示 glow 的状态和版本 |

需要先安装 [glow](https://github.com/charmbracelet/glow)。

### 日志记录

| 命令 | 描述 |
|---------|-------------|
| `/log on\|off` | 切换日志记录到文件 |
| `/log` | 显示日志记录状态和文件路径 |

日志文件默认位于 `~/.emblemai-stream.log`。可以使用 `--log-file <path>` 来更改路径。

---

## 键盘快捷键

| 键 | 功能 |
|-----|--------|
| `Enter` | 发送消息 |
| `Up` | 回退上一条输入 |
| `Ctrl+C` | 退出 |
| `Ctrl+D` | 退出（结束文件） |

---

## CLI 标志

| 标志 | 别名 | 描述 |
|------|-------|-------------|
| `--password <pw>` | `-p` | 身份验证密码（至少 16 个字符）——跳过浏览器身份验证 |
| `--message <msg>` | `-m` | 代理模式的消息内容 |
| `--agent` | `-a` | 以代理模式运行（仅使用密码身份验证） |
| `--restore-auth <path>` | | 从备份文件恢复凭据并退出 |
| `--reset` | | 清除对话记录并退出 |
| `--debug` | | 以启用调试模式启动 |
| `--stream` | | 启用实时显示模式（默认为开启） |
| `--log` | | 启用日志记录 |
| `--log-file <path>` | | 更改日志文件路径（默认为 `~/.emblemai-stream.log`） |
| `--hustle-url <url>` | | 更改 Hustle API 的 URL |
| `--auth-url <url>` | | 更改身份验证服务的 URL |
| `--api-url <url>` | | 更改 API 服务的 URL |

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `EMBLEM_PASSWORD` | 身份验证密码 |

当提供 CLI 参数和环境变量时，CLI 参数会覆盖环境变量。

---

## 权限和安全模式

代理默认处于 **安全模式**。任何影响钱包的操作在执行前都需要用户的明确确认：

- **交易**（交换、发送、转账）——代理会显示详细信息并请求用户批准 |
- **签名**（消息签名、交易签名）——需要用户的明确同意 |
- **订单放置**（限价单、止损）——必须在提交前得到确认 |
- **DeFi 操作**（LP 存款、收益 farming）——用户必须批准每个操作

只读操作（查看余额、查看地址、市场数据、投资组合查询）无需确认，可以立即执行。

代理永远不会在未经用户审查和批准的情况下自动转移资金、签署交易或放置订单。

---

## 通信风格

**重要提示：使用详细、自然的语言。**

Hustle AI 会将简短的命令解释为 “$0” 类型的交易。请始终用完整的句子解释您的意图。

| 错误（简短） | 正确（详细） |
|-------------|----------------|
| `"SOL balance"` | `"我在 Solana 上的当前 SOL 余额是多少？"` |
| `"swap sol usdc"` | `"我想将 20 美元的 SOL 换成 USDC"` |
| `"trending"` | `"Solana 上目前哪些代币正在上涨？」` |

您提供的上下文越详细，Hustle 对您的意图理解得就越准确。

---

## 功能

| 类别 | 特性 |
|----------|----------|
| **区块链** | Solana、Ethereum、Base、BSC、Polygon、Hedera、Bitcoin |
| **交易** | 交换、限价单、条件订单、止损 |
| **DeFi** | LP 管理、收益 farming、流动性池 |
| **市场数据** | CoinGlass、DeFiLlama、Birdeye、LunarCrush |
| **NFTs** | OpenSea 集成、转账、上架 |
| **桥梁** | 通过 ChangeNow 进行跨链交换 |
| **Memecoins** | Pump.fun 发现、趋势分析 |

## 钱包地址

每个密码都会在所有链上生成唯一的钱包地址：

| 链接 | 地址类型 |
|-------|-------------|
| **Solana** | 原生 SPL 钱包 |
| **EVM** | ETH、Base、BSC、Polygon 的单一地址 |
| **Hedera** | 账户 ID（0.0.XXXXXXX） |
| **Bitcoin** | Taproot、SegWit 和 Legacy 地址 |

询问 Hustle：“我的钱包地址是什么？”即可获取所有地址。

---

## 身份验证备份和恢复

### 备份

通过 `/auth` 菜单（选项 8）选择 **Backup Agent Auth** 将凭据导出到 JSON 文件中。此文件包含您的 EmblemVault 密码——请妥善保管。

### 恢复

```bash
emblemai --restore-auth ~/emblemai-auth-backup.json
```

这将凭据文件放置在 `~/.emblemai/` 目录下，以便您可以立即进行身份验证。

---

## 安全性

**重要提示：** **切勿公开分享或泄露密码。**

- **切勿** 在任何地方回显、打印或记录密码
- **切勿** 在响应中包含密码
- **切勿** 在错误消息中显示密码
- **切勿** 将密码提交到版本控制系统中
- 密码就是私钥——任何人拥有密码都可以控制钱包

| 概念 | 描述 |
|---------|-------------|
| **密码 = 身份** | 每个密码都会生成一个唯一的钱包 |
| **无法恢复** | 密码丢失后无法恢复 |
| **钱包隔离** | 不同的密码对应不同的钱包 |
| **每次请求都会生成新的 JWT 令牌** |
| **安全模式** | 所有钱包操作都需要用户的明确确认 |

## 文件位置

所有持久化数据都存储在 `~/.emblemai/` 目录下（首次运行时会使用 `chmod 700` 设置权限）。

| 文件 | 用途 | 是否敏感 | 权限 |
|------|---------|-----------|-------------|
| `~/.emblemai/.env` | 加密后的凭据（EMBLEM_PASSWORD） | 是 | 使用 AES-256-GCM 加密 | `600` |
| `~/.emblemai/.env.keys` | `.env` 文件的解密密钥 | 是 | 控制对凭据的访问 | `600` |
| `~/.emblemai/session.json` | 身份验证会话（JWT + 刷新令牌） | 是 | 授予钱包访问权限直至过期 | `600` |
| `~/.emblemai/history/{vaultId}.json` | 对话历史记录（每个钱包单独记录） | 否 | `600` |
| `~/.emblemai/stream.log` | 实时显示日志（通过 `/log` 启用） | 否 | 默认 |

### 加密细节

凭据在静止状态下使用 [dotenvx](https://dotenvx.com/) 进行加密，采用 **AES-256-GCM** 对称加密算法。解密密钥存储在 `~/.emblemai/.env.keys` 文件中，加密后的数据存储在 `~/.emblemai/.env` 文件中。这两个文件的权限设置为 `chmod 600`（仅所有者可读/写）。解密密钥永远不会离开本地机器。

会话令牌（`session.json`）包含一个短期的 JWT（会自动刷新）和一个有效期为 7 天的刷新令牌。会话不会在磁盘上加密，但会使用 `chmod 600` 限制访问权限。通过 `/auth` > Logout 退出会删除会话文件。

旧的凭据（`~/.emblem-vault`）在首次运行时会自动转换为加密格式，并备份原始文件。

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| `emblemai: command not found` | 运行：`npm install -g @emblemvault/agentwallet` |
| “密码必须至少包含 16 个字符” | 使用更长的密码 |
| “身份验证失败” | 检查与身份验证服务的网络连接 |
| 浏览器无法打开进行身份验证 | 复制显示的 URL 并手动打开 |
| 会话过期 | 重新运行 `emblemai`——浏览器会打开新会话 |
| glow 无法渲染 | 安装 glow：`brew install glow`（可选，否则会使用纯文本显示） |
| 插件无法加载 | 确保已安装相应的 npm 包 |
| **响应缓慢** | 正常现象——查询可能需要最多 2 分钟 |

---

## 更新信息

```bash
npm update -g @emblemvault/agentwallet
```

---

## 快速参考

```bash
# Install
npm install -g @emblemvault/agentwallet

# Interactive mode (browser auth -- recommended)
emblemai

# Agent mode (zero-config -- auto-generates wallet)
emblemai --agent -m "What are my balances?"

# Agent mode with explicit password
emblemai --agent -p "your-password-16-chars-min" -m "What tokens do I have?"

# Use environment variable
export EMBLEM_PASSWORD="your-password-16-chars-min"
emblemai --agent -m "Show my portfolio"

# Reset conversation history
emblemai --reset
```

---

## 安全提示

本部分解释了信任模型、在您的机器上会发生什么以及如何安全地运行代理。

### 信任模型

Emblem Agent Wallet 是由 [EmblemCompany](https://github.com/EmblemCompany) 在 npm 和 GitHub 上发布的开源 CLI。在安装之前，您可以验证该包：

- **npm 注册表**：[`@emblemvault/agentwallet`](https://www.npmjs.com/package/@emblemvault/agentwallet)——查看发布者、版本历史和下载统计信息 |
- **源代码**：[github.com/EmblemCompany/EmblemAi-AgentWallet](https://github.com/EmblemCompany/EmblemAi-AgentWallet)——源代码公开且可审计 |
- **官方网站**：[emblemvault.dev](https://emblevault.dev)——项目官方网站，包含文档

npm 包和 GitHub 仓库由同一组织维护。您可以使用 `npm pack --dry-run` 或在安装后检查 `node_modules/@emblemvault/agentwallet` 来比较发布的包内容和源代码。

### 安装过程

`npm install -g @emblemvault/agentwallet` 会在您的机器上全局安装 CLI 可执行文件 `emblemai`。与所有全局 npm 包一样，该文件会在您的用户权限下运行。该包没有 `postinstall` 脚本——它仅安装 CLI 可执行文件及其依赖项。

### 身份验证过程

**浏览器身份验证**（推荐）：CLI 会在 `127.0.0.1:18247`（仅限本地访问，不支持网络访问）上启动一个临时本地服务器，以接收来自浏览器的身份验证回调。此服务器仅在登录过程中运行，并处理一个请求。浏览器会打开 EmblemVault 身份验证模块，您可以直接在其中与 EmblemVault 服务进行身份验证。成功后，会返回一个会话 JWT 并保存到磁盘上。

**密码身份验证**：密码会通过 HTTPS 发送到 EmblemVault 的身份验证 API。会返回一个会话 JWT。如果使用了 `-p` 标志，密码也会被加密并保存在本地以供后续会话使用。

在这两种情况下，都不会将凭据发送给第三方。身份验证严格发生在您的机器和 EmblemVault 身份验证服务之间。

### 存储在磁盘上的内容

所有文件都存储在 `~/.emblemai/` 目录下，并具有严格的权限设置：

| 文件 | 包含内容 | 保护方式 |
|------|-----------------|-------------------|
| `.env` | 您的 EMBLEM_PASSWORD | 使用 [dotenvx](https://dotenvx.com/) 通过 AES-256-GCM 加密 | 是 | `600` |
| `.env.keys` | `.env` 文件的解密密钥 | 是 | 仅所有者可访问 | `600` |
| `session.json` | JWT 访问令牌 + 刷新令牌 | 是 | `600`。JWT 有效期为 15 分钟，会自动刷新。刷新令牌有效期为 7 天。退出会删除此文件。 |
| `history/*.json` | 对话历史记录 | 是 | `600`。包含您与 AI 的聊天记录。历史记录中不存储凭据。 |

`~/.emblemai/` 目录本身使用 `chmod 700` 设置权限（仅所有者可访问）。

### 会话工作原理

身份验证会话使用短期有效的 JWT（有效期为 15 分钟），并通过 7 天的刷新令牌自动刷新。这意味着：

- 如果会话文件被泄露，攻击者最多只能访问 7 天（刷新令牌有效期） |
- JWT 会频繁更新，从而限制任何单个令牌的暴露时间 |
- 通过 `/auth` > Logout 退出会立即失效会话并删除会话文件 |
- 每次刷新都会生成一个新的刷新令牌并使之前的令牌失效

### 安全模式和交易确认

代理默认处于 **安全模式**。这意味着：

- **所有修改钱包的操作** 在执行前都需要用户的明确确认——包括交换、发送、转账、订单放置、签名和 DeFi 操作 |
- **只读操作** 可以立即执行——无需确认——例如查看余额、地址查询、市场数据、投资组合查看 |
- 代理会显示任何交易的全部详细信息（金额、地址、费用），并在提交前等待您的确认 |
- 没有 “自动执行” 模式——所有操作都需要人工确认

### 密码管理

您的 EMBLEM_PASSWORD 是您钱包的密钥。请像对待私钥或种子短语一样谨慎处理它：

- **使用强密码**（至少 16 个字符）。建议使用 4 个以上随机单词组成的密码 |
- **不要在其他服务中重复使用密码**。您的 EMBLEM_PASSWORD 应该是 EmblemVault 独有的 |
- **安全存储密码**：使用密码管理器进行存储。CLI 会在磁盘上加密密码，但您应该备份以防丢失访问权限 |
- **如果在自动化环境中使用 `EMBLEM_PASSWORD` 作为环境变量**，请确保主机环境安全——限制对机器的访问、使用进程隔离，并避免在环境变量中存储密码 |
- **对于交互式使用，建议使用浏览器身份验证**——这样可以避免在 shell 历史记录或环境变量中存储密码 |
- **不同的密码会生成不同的钱包**——这是设计意图，以便根据用途区分不同的资金 |

### 验证包内容

在安装之前或之后，您可以查看包的确切内容：

```bash
# View package contents without installing
npm pack @emblemvault/agentwallet --dry-run

# After installing, inspect the source
ls $(npm root -g)/@emblemvault/agentwallet/

# Compare against GitHub source
git clone https://github.com/EmblemCompany/EmblemAi-AgentWallet.git
diff -r node_modules/@emblemvault/agentwallet EmblemAi-AgentWallet/publish
```

### 报告安全问题

如果您发现安全漏洞，请负责任地报告：

- **GitHub**：在 [github.com/EmblemCompany/EmblemAi-AgentWallet/issues](https://github.com/EmblemCompany/EmblemAi-AgentWallet/issues) 提交问题 |
- **Discord**：在 [discord.gg/Q93wbfsgBj](https://discord.gg/Q93wbfsgBj) 的安全频道报告

---

## 链接

- [npm 包](https://www.npmjs.com/package/@emblemvault/agentwallet)
- [EmblemVault](https://emblevault.dev)
- [Hustle AI](https://agenthustle.ai)
- [GitHub](https://github.com/EmblemCompany/EmblemAi-AgentWallet)