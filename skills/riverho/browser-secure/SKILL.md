---
name: browser-secure
description: 使用 Chrome 配置文件支持、安全存储库集成、审批机制以及全面的审计日志记录功能，实现安全的浏览器自动化操作。适用于需要身份验证的网站、敏感操作或符合合规性要求的场景。
allowed-tools: Bash
---

# 浏览器安全（Browser Secure）

通过基于加密库（vault）的凭证管理、审批流程和审计日志，实现安全的浏览器自动化。

## 哲学理念

> **“永远不要轻信，始终验证；对所有数据进行加密；记录所有操作。”**

## 快速入门

```bash
# Open the welcome page (default when no URL provided)
browser-secure navigate

# Navigate to a public site
browser-secure navigate https://example.com

# Navigate with auto-vault credential discovery
browser-secure navigate https://app.neilpatel.com/ --auto-vault

# Navigate to an authenticated site (pre-configured)
browser-secure navigate https://nytimes.com --site=nytimes

# Perform actions (fully automated)
browser-secure act "click the login button"
browser-secure extract "get the article headlines"

# Use interactive mode (with approval prompts)
browser-secure navigate https://bank.com --interactive

# Close and cleanup
browser-secure close
```

## 自动发现凭证

`--auto-vault` 标志允许从您的密码管理器中交互式地发现凭证：

```bash
browser-secure navigate https://app.neilpatel.com/ --auto-vault
```

该功能将：
1. 从 URL 中提取域名（例如 `app.neilpatel.com` → 提取 `neilpatel`）
2. **首先在 Bitwarden 中搜索**（免费，默认选项），如果可用的话，也会在 1Password 中搜索
3. 以交互方式显示匹配的凭证：

```
🔍 Auto-discovering credentials for app.neilpatel.com...

📋 Found 2 matching credential(s) in Bitwarden:

  1) Neil Patel Account
     Username: user@example.com
  2) Ubersuggest API Key

  n) None of these - try another vault
  m) Manually enter credentials

Select credential to use (1-2, n, or m): 1
🔐 Retrieving credentials for neilpatel...

Save this credential mapping for future use? (y/n): y
✅ Saved credential mapping for "neilpatel" to ~/.browser-secure/config.yaml
   Default vault provider set to: Bitwarden
```

保存设置后，下次您可以使用更简洁的命令：

```bash
browser-secure navigate https://app.neilpatel.com/ --site=neilpatel
```

## 配置个人资料

创建独立的 Chrome 个人资料以进行安全自动化，并自动设置欢迎页面：

```bash
# Create a new profile with welcome page
browser-secure profile --create "Funny Name"

# Create and immediately launch Chrome
browser-secure profile --create "The Crustacean Station 🦞" --launch

# List all Chrome profiles
browser-secure profile --list
```

### 欢迎页面的内容

创建新个人资料时，系统会打开一个自定义的欢迎页面，引导您完成以下步骤：
1. **📖 个人资料的作用** - 解释独立自动化系统的目的
2. **🔌 必需安装的扩展程序** - 提供直接链接以安装：
   - Bitwarden 密码管理器
   - OpenClaw 浏览器中继（Browser Relay）
3. **🗝️ 加密库设置** - 逐步指导您完成 Bitwarden 或 1Password 的配置
4. **✅ 设置检查表** - 交互式检查表，用于跟踪设置进度
5. **🛡️ 安全信息** - 显示“您的加密库是安全的”信息，并介绍其主要功能

### 为什么需要单独的个人资料？

| 特性 | 个人资料 | 自动化个人资料 |
|--------|------------------|-------------------|
| 扩展程序 | 个人使用的扩展程序 | 仅包含自动化相关的扩展程序 |
| Cookies | 个人登录信息 | 会话状态被隔离 |
| 安全性 | 与日常浏览共享 | 会话状态受到严格保护 |
| 清理 | 需手动操作 | 会话会自动定时清除 |

## 对 Chrome 个人资料的支持

Browser Secure 可以使用您现有的 Chrome 个人资料，让您能够访问已保存的 Cookies、会话状态以及现有的网站登录信息。

### 查看可用的个人资料
```bash
browser-secure navigate https://example.com --list-profiles
```

### 使用特定的个人资料
```bash
# By profile ID
browser-secure navigate https://gmail.com --profile "Default"
browser-secure navigate https://gmail.com --profile "Profile 1"

# Interactively select
browser-secure navigate https://gmail.com --profile select
```

### 个人资料与无痕模式（Incognito Mode）的比较

| 模式 | Cookies | 登录信息 | 扩展程序 | 使用场景 |
|------|---------|--------|------------|----------|
| **无痕模式（默认）** | ❌ 无 | ❌ 无 | ❌ 无 | 适用于安全的隔离测试 |
| **Chrome 个人资料** | ✅ 有 | ✅ 有 | ✅ 有 | 可访问现有的会话 |

**安全提示**：Browser Secure 会为自动化创建独立的个人资料，而不会修改您现有的 Chrome 个人资料。当使用 `--profile` 选项时，它只会读取现有资料，而不会写入新数据。

## 设置

### 方式 1：通过 Clawdbot 安装（推荐）

最简单的方法是使用 Clawdbot：

```
Hey Clawdbot, install browser-secure for me
```

Clawdbot 会处理所有步骤：检查先决条件、自动安装依赖项、构建并配置工具。

### 方式 2：从 GitHub 安装

```bash
# Clone and install
curl -fsSL https://raw.githubusercontent.com/openclaw/openclaw/main/scripts/install-browser-secure.sh | bash
```

### 方式 3：手动设置（高级）

如果您希望完全控制工具的开发过程，可以选择这种方式：

```bash
# Clone the repository
git clone https://github.com/openclaw/openclaw.git
cd openclaw/skills/browser-secure

# Run interactive setup
npm run setup
```

该过程将：
1. ✅ 检查所需的系统要求（Node.js 18.0 及更高版本、Chrome 浏览器）
2. 📦 **自动安装缺失的依赖项**（如 Playwright 浏览器插件或可选的加密库 CLI）
3. 🔨 全局安装并链接 CLI 工具
4. 📝 创建默认配置文件

### 自动安装的内容

设置过程中会自动安装以下内容：
- **Playwright Chromium** - 必需的浏览器二进制文件（约 50MB）
- **Bitwarden CLI**（如果系统支持 `brew`，推荐使用）
- **1Password CLI**（如果系统支持 `brew`，可选）

### 配置加密库（可选）

设置完成后，您可以使用 **环境变量**（推荐）或直接通过 CLI 登录来配置您喜欢的加密库：

#### 方式 A：.env 文件（便于自动化）

> ⚠️ **安全提示**：.env 文件以明文形式存储凭证。请仅在可信赖的私有机器上使用此方法。建议使用 Bitwarden 或 1Password 这样的加密库进行安全存储。

```bash
cd ~/.openclaw/workspace/skills/browser-secure
cp .env.example .env
# Edit .env with your credentials
```

**完全自动化（API 密钥 + 密码）：**
```bash
# .env - For fully automated vault access
BW_CLIENTID=user.xxx-xxx
BW_CLIENTSECRET=your-secret-here
BW_PASSWORD=your-master-password
```

**工作原理：**
1. `BW_CLIENTID/BW_CLIENTSECRET` — 用于通过 Bitwarden 进行身份验证（替代用户名/密码）
2. `BW_PASSWORD` — 用于解密您的加密库中的凭证（自动化访问时必需）

**替代方案：会话令牌（Session Token）**
```bash
# If you prefer not to store your master password:
export BW_SESSION=$(bw unlock --raw)
# Then add to .env:
# BW_SESSION=xxx...
```

#### 方式 B：直接通过 CLI 登录

```bash
# Bitwarden (recommended - free)
brew install bitwarden-cli  # if not auto-installed
bw login
export BW_SESSION=$(bw unlock --raw)

# 1Password (if you have a subscription)
brew install 1password-cli  # if not auto-installed
op signin

# Test vault access
browser-secure vault --list
```

### 验证安装是否成功

```bash
browser-secure --version
browser-secure navigate https://example.com
browser-secure screenshot
browser-secure close
```

## 加密库提供商

### Bitwarden（默认，免费）⭐

**推荐** — 适用于个人免费使用，开源且跨平台支持。

```bash
# Install
brew install bitwarden-cli

# Setup .env file
cd ~/.openclaw/workspace/skills/browser-secure
cp .env.example .env
# Edit .env and add:
#   BW_CLIENTID=your-api-key-id
#   BW_CLIENTSECRET=your-api-key-secret  
#   BW_PASSWORD=your-master-password

# Use - credentials auto-loaded from .env
browser-secure navigate https://app.neilpatel.com/ --auto-vault
```

**身份验证与解密方式：**
- **API 密钥** (`BW_CLIENTID/BW_CLIENTSECRET`) — 用于登录 Bitwarden
- **主密码** (`BW_PASSWORD`) — 用于解密加密库中的数据
- 两种方式都是实现完全自动化工作流程的必要条件

**获取 API 密钥：** https://vault.bitwarden.com/#/settings/security/keys

### 1Password（付费服务）

**替代方案** — 如果您已经订阅了 1Password 服务。

```bash
# Install
brew install 1password-cli

# Login
op signin
eval $(op signin)

# Use
browser-secure navigate https://app.neilpatel.com/ --auto-vault
```

### macOS Keychain（本地存储）

**备用方案** — 将凭证存储在 macOS 的 Keychain 中（不进行云同步）。

### 环境变量

**紧急情况下的备用方案** — 通过环境变量设置凭证：

```bash
export BROWSER_SECURE_NEILPATEL_USERNAME="user@example.com"
export BROWSER_SECURE_NEILPATEL_PASSWORD="secret"
browser-secure navigate https://app.neilpatel.com/
```

## 常用命令

| 命令 | 功能 |
|---------|-------------|
| `navigate` | **打开欢迎页面**（未提供 URL 时默认操作） |
| `navigate <url>` | 导航到指定 URL |
| `navigate <url> --profile <id>` | 使用特定的 Chrome 个人资料 |
| `navigate <url> --profile select` | 交互式选择 Chrome 个人资料 |
| `navigate <url> --list-profiles` | 列出所有可用的 Chrome 个人资料 |
| `navigate <url> --auto-vault` | 自动发现凭证（依次尝试 Bitwarden、1Password，最后手动输入） |
| `navigate <url> --site=<name>` | 使用预配置的站点凭证 |
| `profile --create <name>` | 创建新的 Chrome 个人资料并启动浏览器 |
| `profile --create <name> --launch` | 创建个人资料并立即打开浏览器 |
| `profile --list` | 列出所有 Chrome 个人资料 |
| `act "<instruction>"` | 执行特定操作 |
| `extract "<instruction>"` | 从页面中提取数据 |
| `screenshot` | 截取屏幕截图 |
| `close` | 关闭浏览器并清理临时文件 |
| `status` | 显示当前会话状态 |
| `audit` | 查看审计日志 |

## 欢迎页面（默认设置）

当您运行 `browser-secure navigate` 且未提供 URL 时，系统会打开位于以下地址的欢迎页面：

```
~/.openclaw/workspace/skills/browser-secure/assets/welcome.html
```

欢迎页面包含：
- 📖 **入门指南** — 介绍 browser-secure 的用途和工作原理
- 🔌 **扩展程序安装链接** — 提供 Bitwarden 和 OpenClaw Browser Relay 的安装指南
- 🗝️ **加密库设置** — 逐步指导您完成 Bitwarden 或 1Password 的配置
- ✅ **设置检查表** | 交互式检查表，帮助您完成设置
- 🛡️ **安全信息** | 显示“您的加密库是安全的”信息，并介绍其主要功能

**小贴士**：新用户可以从欢迎页面开始使用该工具：

```bash
# Create a profile, then immediately open welcome page
browser-secure profile --create "Work Automation" --launch
# Then in another terminal:
browser-secure navigate  # Opens welcome page in the active session
```

## 审批流程（混合设计）

Browser Secure 默认以 **无人值守模式** 运行，非常适合自动化任务，同时保留了必要的安全防护措施。

### 默认模式：无人值守（自动化优先）

```bash
# All commands run unattended by default - no interactive prompts
browser-secure navigate https://example.com
browser-secure act "fill the search form"
browser-secure extract "get all links"
```

在该模式下：
- ✅ 所有非破坏性操作会立即执行
- ✅ 凭证会自动从加密库中获取
- ✅ 所有操作都会自动记录审计日志
- ⚠️ 破坏性操作（如删除、购买等）需要使用 `--skip-approval` 或 `--interactive` 选项

### 交互模式（人工干预）

对于敏感操作，可以使用 `--interactive` 选项来启用审批流程：

```bash
# Enable tiered approval gates
browser-secure navigate https://bank.com --interactive

# Approve individual actions
browser-secure act "transfer $1000" --interactive
```

**交互模式下的审批层级：**

| 功能 | 执行操作 | 是否需要审批 |
|------|---------|----------|
| 仅读取数据 | 导航、截图、提取数据 | 无需审批 |
| 填写表单 | 输入信息、选择选项、点击按钮 | 需要审批 |
| 身份验证 | 输入密码、提交登录信息 | 必须审批 |
| 破坏性操作 | 删除数据、执行购买等操作 | 需要双重身份验证（2FA） |

### 强制覆盖设置（紧急情况下使用）

```bash
# Skip ALL approvals including destructive (DANGEROUS)
browser-secure act "delete account" --skip-approval
```

**警告**：`--skip-approval` 选项会绕过所有安全检查。请仅在完全自动化的、隔离的环境中使用此选项。

### 会话安全设置
- 会话具有时间限制（默认为 30 分钟，过期后自动清除）
- 使用基于 UUID 的隔离工作目录
- **无痕模式**（无持久化的个人资料数据）
- **支持使用 Chrome 个人资料**（可选项，需通过 `--profile` 参数启用）
- 安全清理机制（会自动覆盖和删除临时文件）
- 对网络访问有限制（禁止访问本地主机和私有 IP 地址）

### 审计日志

```json
{
  "event": "BROWSER_SECURE_SESSION",
  "sessionId": "bs-20260211054500-abc123",
  "site": "nytimes.com",
  "actions": [...],
  "chainHash": "sha256:..."
}
```

## 环境变量

| 变量 | 用途 |
|----------|---------|
| `BROWSERSecure_CONFIG` | 配置文件的路径 |
| `BW_CLIENTID` | 用于自动化的 Bitwarden API 密钥 ID |
| `BW_CLIENTSECRET` | 用于自动化的 Bitwarden API 密钥密钥 |
| `BW_PASSWORD` | 用于自动化的 Bitwarden 主密码 |
| `BW_SESSION` | 旧版本的 Bitwarden 会话令牌 |
| `OP_SERVICE_ACCOUNT_TOKEN` | 1Password 服务账户的访问令牌 |
| `BROWSERSecure_{SITE}_PASSWORD` | 基于环境变量的凭证信息 |

## 与普通浏览器自动化工具的比较

| 特性 | 普通浏览器自动化工具 | Browser Secure |
|---------|-------------------|----------------|
| 凭证管理 | 通过 CLI 进行管理（凭证可能暴露） | 基于加密库进行管理 |
| Chrome 个人资料 | 不支持 | 支持使用 Chrome 个人资料（包括 Cookies 和登录信息） |
| 审批流程 | 无审批机制 | 提供多层次的审批流程 |
| 审计记录 | 无审计功能 | 提供完整的操作记录 |
| 会话超时设置 | 无默认超时设置 | 默认超时为 30 分钟 |
| 网络访问限制 | 无限制 | 只允许访问指定网站 |
| 适用场景 | 适合简单任务 | 适用于需要身份验证的敏感操作 |

## 常见问题解决方法

**首次运行时出现 Chrome Keychain 提示**：这是正常现象！当 Playwright 首次启动 Chrome 时，macOS 会询问是否允许 Chrome 访问 Keychain。您可以点击“拒绝”，因为 Browser Secure 实际上是通过加密库来管理凭证的，而非使用 Chrome 的内置存储机制。

**无法找到加密库**：请为您选择的加密库安装相应的 CLI 工具：
- Bitwarden：`brew install bitwarden-cli`
- 1Password：`brew install 1password-cli`

**Bitwarden 显示“加密库被锁定”**：
- 如果使用了 `.env` 文件，请确认 `BW_CLIENTID` 和 `BW_CLIENTSECRET` 的值是否设置正确
- 或者运行命令：`export BW_SESSION=$(bw unlock --raw)`

**Bitwarden API 密钥无法使用**：请确保您的 API 密钥具有访问所需加密库数据的权限。API 密钥可以在以下链接获取：https://vault.bitwarden.com/#/settings/security/keys

**站点配置问题**：使用 `--auto-vault` 选项进行交互式设置，或手动将站点配置信息添加到 `~/.browser-secure/config.yaml` 文件中

**会话过期**：会话默认在 30 分钟后过期，可以使用 `--timeout` 参数重新启动程序

**需要审批**：对于非交互式操作，请使用 `-y` 参数来忽略审批流程（请谨慎使用）

**找不到个人资料**：运行 `browser-secure navigate https://example.com --list-profiles` 命令查看可用的个人资料列表

**使用 Chrome 个人资料时出现问题**：在使用 `--profile` 选项之前，请先关闭 Chrome 浏览器（Chrome 会在使用该选项时锁定相关个人资料）