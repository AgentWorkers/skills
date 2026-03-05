---
name: claude-oauth-renewal
description: "通过心跳机制自动检测并续期过期的 Claude Code OAuth 令牌。续期过程分为三个步骤：  
1. 刷新令牌；  
2. 使用 Chrome 浏览器执行自动化操作；  
3. 向用户发出提醒。"
homepage: https://github.com/anthropics/claude-code
metadata: { "openclaw": { "emoji": "🔑", "requires": { "bins": ["claude", "security", "python3"], "platform": "macos" } } }
---
# Claude Code OAuth 自动续期

在 OpenClaw 的心跳周期中，自动检测并续期过期的 Claude Code OAuth 令牌。这可以防止因令牌过期而导致代理程序停止运行。

## 适用场景

✅ **在以下情况下使用此功能：**

- 您的 OpenClaw 代理使用 Claude Code 作为 AI 提供者；
- 您希望代理程序能够持续运行，而无需手动续期令牌；
- 您在 macOS 上使用 Chrome 浏览器运行 OpenClaw。

## 工作原理

### 三层续期策略

```
Heartbeat triggers check-claude-oauth.sh
  │
  ├─ Token healthy (>6h remaining) → silent exit ✓
  │
  ├─ Tier 1: claude auth status (refresh token)
  │   ├─ Success → silent exit ✓
  │   └─ Fail ↓
  │
  ├─ Tier 2: Browser automation (osascript + Chrome JXA)
  │   ├─ Start claude auth login
  │   ├─ Auto-click "Authorize" on claude.ai
  │   ├─ Extract auth code from callback page
  │   ├─ Feed code back to CLI via expect
  │   ├─ Success → silent exit ✓
  │   └─ Fail ↓
  │
  └─ Tier 3: Alert user → agent notifies via configured channel
```

### 令牌存储

Claude Code 将 OAuth 令牌存储在 macOS 的 Keychain 中，服务名称为 `Claude Code-credentials`。令牌的 JSON 数据包含以下内容：

- `accessToken` — API 访问令牌（前缀为 `sk-ant-oat01-`）；
- `refreshToken` — 用于自动续期（前缀为 `sk-ant-ort01-`）；
- `expiresAt` — 以毫秒为单位的 Unix 时间戳，表示令牌的有效期。

### 先决条件

1. 安装了 macOS 并启用了 `security` CLI（用于访问 Keychain）；
2. 已安装并登录了 Claude Code；
3. 在 Google Chrome 浏览器中，启用了“开发者”选项卡下的“允许来自 Apple 事件的 JavaScript”功能（适用于第二层续期机制）；
4. 系统路径（PATH）中包含 `python3`；
5. 系统已安装 `expect` 工具（macOS 自带）。

## 设置步骤

### 1. 复制脚本

```bash
cp skills/claude-oauth-renewal/scripts/check-claude-oauth.sh scripts/check-claude-oauth.sh
chmod +x scripts/check-claude-oauth.sh
```

### 2. 添加到 HEARTBEAT.md 文件中

将此脚本作为心跳执行流程的第一步添加到您的 HEARTBEAT.md 文件中：

```markdown
## Execution Order

0. Run `bash scripts/check-claude-oauth.sh` — if output exists, relay as highest priority alert
1. (your other heartbeat checks...)
```

### 3. 测试

```bash
# Normal check (silent if token healthy)
bash scripts/check-claude-oauth.sh

# Force trigger by setting high threshold
WARN_HOURS=24 bash scripts/check-claude-oauth.sh
```

## 配置参数

| 环境变量 | 默认值 | 说明 |
|---------------------|---------|-------------|
| `WARN_HOURS` | `6` | 令牌过期前开始尝试续期的时间（以小时为单位） |

## 故障排除

### “无法读取 Claude Code 令牌”
- 手动运行 `claude auth login` 命令以建立初始登录凭据；
- 验证 Keychain 的访问权限：`security find-generic-password -s "Claude Code-credentials" -a "$(whoami)" -g`

### 第二层（浏览器自动化）无法工作
- 在 Chrome 浏览器中启用“允许来自 Apple 事件的 JavaScript”功能；
- 或通过 CLI 命令：`defaults write com.google.Chrome AppleScriptEnabled -bool true`（然后重启 Chrome）；
- 确保您已在 Chrome 中登录到 claude.ai。

### JSON 解析错误
- 该脚本使用正则表达式来解析 Keychain 中的令牌信息（而非直接使用 `json.loads`）；
- 如果 `security -w` 命令导致 Keychain 数据被截断，可以使用 `-g` 标志作为备用方案。

## 注意事项

- 第一层（使用 `refreshToken`）可以无声地处理大多数情况；
- 只有当 `refreshToken` 本身过期（通常需要几周时间）时，才需要使用第二层（浏览器自动化）；
- 第三层（显示警告）是最后的解决方案，仅在无法自动续期的情况下使用；
- 该脚本不会存储或记录实际的令牌值。