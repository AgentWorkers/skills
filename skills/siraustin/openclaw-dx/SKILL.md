---
name: openclaw-dx
version: 1.4.0
license: MIT
description: 诊断并修复 OpenClaw 网关问题。当网关卡住、无法启动、陷入死循环或拒绝连接时，请使用此方法。该方法适用于主网关（main gateway）以及使用 `--profile vesper` 配置的网关（vesper gateway）。执行故障排查（triage），应用相应的修复措施，并将故障报告写入 `~/clawd/inbox` 文件夹中。
---
# OpenClaw Gateway DX

本文档用于诊断、修复并记录与 OpenClaw Gateway 相关的问题。它涵盖了主配置文件（端口 18789）以及 Vesper 配置文件（端口 18999）中的问题。

## 使用场景

- Gateway 无法启动或陷入死循环
- TUI/CLI 无法连接（需要配对、密码不匹配或设备令牌不匹配）
- Gateway 无响应或内存使用量过高
- 在 OpenClaw 版本升级后出现问题
- 用户报告 “OpenClaw 停滞” 等类似情况

## 故障排查流程

请同时执行以下操作以评估系统状态：

```bash
# 1. What's listening?
lsof -i :18789 -i :18999 2>/dev/null | grep LISTEN

# 2. Process health (memory, CPU, uptime)
ps -o pid,rss,pcpu,lstart,etime -p $(lsof -i :18789 -t 2>/dev/null | head -1)

# 3. Recent errors
tail -30 ~/.openclaw/logs/gateway.err.log

# 4. Recent activity
tail -20 ~/.openclaw/logs/gateway.log

# 5. Channel status
openclaw channels status

# 6. Version
openclaw --version

# 7. Pending device pairings
openclaw devices list --json | head -20

# 8. Model config + fallback chain (use affected profile's config dir)
# Main: ~/.openclaw/openclaw.json | Vesper: ~/.openclaw-vesper/openclaw.json
cat ~/.openclaw/openclaw.json | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['agents']['defaults']['model'], indent=2))"

# 9. Per-agent auth token status + expiry check
# Main: ~/.openclaw/agents/main/agent/auth-profiles.json
# Vesper: ~/.openclaw-vesper/agents/main/agent/auth-profiles.json
python3 -c "
import sys,json,time
data=json.load(open('$HOME/.openclaw/agents/main/agent/auth-profiles.json'))
now=time.time()*1000
for k,v in data.get('profiles',{}).items():
    exp=v.get('expires',0)
    expired='EXPIRED' if exp and exp<now else 'valid'
    has_token='yes' if v.get('access') or v.get('token') else 'NO'
    print(f'{k}: type={v.get(\"type\",\"?\")} token={has_token} expires={expired}')
"

# 10. Memory search / QMD (use --profile if vesper)
openclaw memory status

# 11. Check OPENCLAW_GATEWAY_TOKEN env var (multi-profile foot-gun)
echo "OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN:-unset}"

# 12. Verify plist profile alignment
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.gateway.plist
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.vesper.plist
```

## 常见故障类型

### 0. 故障转移级联（所有提供者均失败）

**症状：** 所有模型均失败（N），随后显示各个提供者的具体错误信息。也可能出现 “模型崩溃，无其他提示信息”（退出代码：null）。
**诊断方法：** 检查完整的错误链——每次尝试都会依次尝试使用主配置、备用配置1、备用配置2。只有当所有配置都失败时，用户才会看到错误信息。常见提供者的错误信息如下：
- Anthropic：`AI 服务暂时过载`（可能是临时问题或令牌过期）
- OpenAI Codex：`openai-codex 的 OAuth 令牌刷新失败` 或 `refresh_token_reused`（访问令牌过期或已使用的刷新令牌）
- Google/Gemini：`未找到提供者 “google” 的 API 密钥`（该提供者在 auth-profiles.json 中未配置）
- LM Studio：Python 错误，例如 `AttributeError: 'list' 对象没有 'swapaxes' 属性`（模型推理错误）
**解决方法：** 确定哪些提供者出现了问题，并逐一修复：
```bash
# Check fallback config (use affected profile's config dir)
cat ~/.openclaw/openclaw.json | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['agents']['defaults']['model'], indent=2))"
# Check per-agent auth tokens + expiry
python3 -c "
import sys,json,time
data=json.load(open('$HOME/.openclaw/agents/main/agent/auth-profiles.json'))
now=time.time()*1000
for k,v in data.get('profiles',{}).items():
    exp=v.get('expires',0)
    expired='EXPIRED' if exp and exp<now else 'valid'
    has_token='yes' if v.get('access') or v.get('token') else 'NO'
    print(f'{k}: type={v.get(\"type\",\"?\")} token={has_token} expires={expired}')
"
```
- 对于 OAuth 令牌过期的情况（OpenAI Codex）：使用 `openclaw configure` 进行交互式重新认证。如果使用 Vesper 配置文件，请添加 `--profile vesper` 参数。
- 对于缺少提供者密钥的情况（如 Google）：使用 `openclaw agents add <provider>` 命令添加相应的提供者，或从备用配置链中移除未配置的提供者。
**预防措施：** 确保备用配置链中的所有提供者都已正确配置。对于可预测的故障模式，应使用相同类型的提供者作为备用选项（例如，使用不同版本的 Anthropic 模型）。

### 1. 通道令牌过期（Slack xoxe.xoxb-）

**症状：** 系统陷入死循环，并显示错误信息 “Unhandled promise rejection: Error: An API error occurred: token_expired”。
**解决方法：**
```bash
# Disable the channel
# Edit ~/.openclaw/openclaw.json: channels.slack.enabled → false AND plugins.entries.slack.enabled → false
openclaw gateway start
# Then rotate token at api.slack.com and re-enable
```

### 2. 配置信息在升级后被清除

**症状：** Gateway 无法启动，显示 `gateway.mode=local`（当前设置为未设置）。
**解决方法：** 从备份中恢复配置信息：
```bash
ls -la ~/.openclaw/openclaw.json.bak*
# Find the largest/most recent backup with full config
cp ~/.openclaw/openclaw.json.bak-XXXX ~/.openclaw/openclaw.json
openclaw doctor --fix
openclaw gateway start
```

### 3. 旧锁文件导致问题

**症状：** Gateway 无法启动，尝试使用旧的进程 ID（PID）。
**解决方法：**
```bash
ls ~/.openclaw/gateway.*.lock
cat ~/.openclaw/gateway.*.lock  # check PID
kill -0 <pid>  # verify dead
rm ~/.openclaw/gateway.*.lock
openclaw gateway start
```

### 4. 设备令牌不匹配/需要配对

**症状：** 显示 “unauthorized: device token mismatch” 或 “pairing required”。
**解决方法：**
```bash
openclaw devices list --json  # check for pending requests
openclaw devices approve "<requestId>" --password "$OPENCLAW_GATEWAY_PASSWORD"
# Or rotate existing device:
openclaw devices rotate --device <id> --role operator --password "$OPENCLAW_GATEWAY_PASSWORD"
```

### 5. 密码不匹配（多配置文件）

**症状：** 显示 “unauthorized: gateway password mismatch”。
**解决方法：** 同步所有配置文件中的密码。所有配置文件都应使用环境变量 `$OPENCLAW_GATEWAY_PASSWORD` 以匹配 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）中的设置。

### 6. 内存占用过高/系统无响应

**症状：** Gateway 处于监听状态但无响应，RSS 值超过临界阈值（详见内存阈值部分）。
**解决方法：**
```bash
openclaw gateway stop
sleep 2
kill -9 <pid>  # if still lingering
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### 7. 插件配置无效

**症状：** 显示 “config invalid: plugins.entries.X: plugin not found”。
**解决方法：** 从 `~/.openclaw/openclaw.json` 中删除无效的插件条目，然后重新启动 Gateway：
```json
"configSchema": {
  "type": "object",
  "additionalProperties": false,
  "properties": {}
}
```
之后重新启动系统：`launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist`。

### 8. 端口冲突/存在孤儿进程

**症状：** 端口 18789 被其他进程占用，或者存在多个 Gateway 进程。
**解决方法：**
```bash
ps aux | grep openclaw-gateway | grep -v grep
kill <orphan-pids>
openclaw gateway start
```

### 9. 自定义插件缺少配置文件

**症状：** 系统陷入死循环，并显示 “plugins: plugin: plugin manifest requires configSchema”。
**诊断方法：** 检查 `~/.openclaw/extensions/` 目录下的插件文件（自动检测到的插件）或 `plugins.loadpaths` 文件中的插件配置。如果某个插件缺少 `configSchema` 字段，运行 `openclaw doctor --fix` 命令（该命令会指出问题插件）。**解决方法：** 在插件配置文件中添加空的 `configSchema` 字段：
```json
"configSchema": {
  "type": "object",
  "additionalProperties": false,
  "properties": {}
}
```
之后重新启动系统：`launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist`。
**预防措施：** 自 2026.3.2 版本起，所有插件配置文件都必须包含 `configSchema` 字段（即使该字段为空）。在创建自定义插件后，务必运行 `openclaw doctor` 命令进行验证。

### 10. 配置文件中的 JSON 无效（手动编辑导致的问题）

**症状：** CLI 命令执行失败，显示 `json.decoder.JSONDecodeError` 或 “Unexpected token” 错误。Gateway 可能已经启动，但 CLI/TUI 无法解析配置文件以建立连接。
**诊断方法：** 有人手动编辑了 `openclaw.json` 文件，导致 JSON 格式错误（例如未加引号的键、多余的逗号等）。**解决方法：** 验证并修复 JSON 文件的内容：
```bash
python3 -c "import json; json.load(open('$HOME/.openclaw/openclaw.json'))"
# Fix the reported line — common issues: unquoted keys, trailing commas
```
**预防措施：** 使用 `openclaw configure` 命令或支持 JSON 格式的编辑器进行编辑。手动编辑后，务必使用上述 Python 代码进行验证。

### 11. 缺少 `gateway.remote.token`（使用令牌认证的模式）

**症状：** CLI/TUI 报错 “gateway token missing”（需要设置 `gateway.remote.token` 以匹配 `gateway.auth.token`）。
**诊断方法：** Gateway 使用 `gateway.auth.mode: "token"` 进行认证，但 `gateway.remote.token` 未设置。CLI 会尝试使用 `gateway.remote.token` 进行身份验证，如果该字段未设置，则所有连接都会被拒绝。**解决方法：** 设置 `gateway.remote.token` 使其与 `gateway.auth.token` 值一致：
```bash
# In openclaw.json, inside the "gateway" section:
"remote": {
  "token": "<same value as gateway.auth.token>"
}
```
之后重新启动 Gateway。
**注意：** 使用 `gateway.auth.mode: "token"` 的配置文件需要设置 `gateway.remote.token`。使用密码认证（`$OPENCLAW_GATEWAY_PASSWORD`）的配置文件不受此影响。

### 12. 配置文件更新后引发重启问题（LaunchAgent 未正确加载）

**症状：** Gateway 停止运行，端口无法监听，`launchctl print` 显示服务未找到。错误日志显示 “config change requires gateway restart”，但重启失败。
**诊断方法：** 多次执行 `config.patch` 操作（例如通过 Gateway 工具）修改了 `gateway.auth.*` 等配置项，导致重启失败。重启机制可能遇到以下问题：
- `spawnSync launchctl ETIMEDOUT`
- `Bootstrap failed: 5: Input/output error`
这会导致 Gateway 重新启动失败，系统变得不稳定，最终收到 SIGTERM 信号，LaunchAgent 保持未加载状态。
**解决方法：**
```bash
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```
**预防措施：**
- 将涉及 `gateway.auth.*` 的配置更改集中在一个 `config.patch` 操作中，以减少重启次数。
- 这是 OpenClaw 2026.3.x 版本中的一个已知问题——LaunchAgent 的重启机制在处理多种故障时不够可靠。
- 可以考虑使用 watchdog 或在 plist 文件中设置 `ThrottleInterval=30` 来防止频繁重启。
- 如果使用 Gateway 工具的 `config.patch` 功能，应将认证配置、插件配置和压缩配置更新合并为一个操作。

### 13. `OPENCLAW_GATEWAY_TOKEN` 环境变量覆盖了多配置文件中的令牌认证设置

**症状：** 即使在配置文件中设置了 `gateway.auth.token` 和 `gateway.remote.token`，使用 `openclaw --profile vesper` 时仍显示 “unauthorized: gateway token mismatch”。**解决方法：** CLI 会优先使用 `OPENCLAW_GATEWAY_TOKEN` 环境变量来解析认证信息。**解决方法：** 同步所有配置文件，使它们使用相同的认证令牌（即 `$OPENCLAW_GATEWAY_TOKEN`）：
```bash
# Check env var
echo $OPENCLAW_GATEWAY_TOKEN
# In each profile's openclaw.json, set gateway.auth.token AND gateway.remote.token to match
```
**另一种解决方法：** 从 shell 配置文件中删除 `OPENCLAW_GATEWAY_TOKEN` 环境变量，仅依赖配置文件中的令牌设置。这样每个配置文件都可以使用独立的令牌。
**预防措施：** 在使用 `OPENCLAW_GATEWAY_TOKEN` 环境变量时，所有配置文件必须使用相同的认证令牌值。

### 14. LaunchAgent 的 plist 文件被错误地覆盖

**症状：** 使用主配置文件时出现 “unauthorized: gateway token mismatch” 错误。虽然主 Gateway 似乎正在运行（端口处于监听状态），但实际上使用的是错误的配置信息。Vesper 配置文件可能影响了主 Gateway 的行为。**解决方法：** 检查 `ai.openclaw.gateway.plist` 文件是否被错误地覆盖（可能是通过 `openclaw --profile vesper gateway install` 或代理配置更新命令造成的），并修复文件中的配置路径：
```bash
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.gateway.plist
# Should show ~/.openclaw, NOT ~/.openclaw-vesper
grep OPENCLAW_PROFILE ~/Library/LaunchAgents/ai.openclaw.gateway.plist
# Should NOT be present (main is the default profile)
```
之后重新启动系统：`launchctl bootout gui/501/ai.openclaw.gateway && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist`。
**预防措施：** 在运行 `openclaw --profile <name> gateway install` 命令后，务必检查两个 plist 文件是否仍然指向正确的配置文件。该命令可能会覆盖默认配置文件的内容。

## 内存阈值

| RSS | 状态 | 处理措施 |
|-----|--------|--------|
| < 500MB | 正常 | 无需特殊处理 |
| 500MB-1.5GB | 内存使用量较高 | 监控系统状态 |
| 1.5GB-2.5GB | 内存使用量过高 | 安排重启 |
| > 2.5GB | 内存使用量严重过高 | 立即重启 |

## Node.js 堆内存调优

Gateway 使用 Node.js 运行，默认情况下堆内存的最大使用量为 4GB。对于长时间运行的 Gateway 或加载了大量插件的情况，可以通过修改 LaunchAgent plist 文件中的 `ProgramArguments` 选项 `--max-old-space-size` 来增加堆内存大小：
```xml
<string>--max-old-space-size=16384</string>
```

请将此代码段插入 `node` 可执行文件的路径之后、JS 配置文件之前。当前设置如下：
- **vesper**：`--max-old-space-size=16384`（16GB）——用于处理 QMD/内存搜索等高负载场景
- **main**：未设置（Node.js 默认值为 4GB）

如需添加或修改配置，请直接编辑 plist 文件并重新加载系统：
```bash
# Edit the plist
nano ~/Library/LaunchAgents/ai.openclaw.gateway.plist
# Reload
launchctl bootout gui/501/ai.openclaw.gateway && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

如果 Gateway 在达到上述内存阈值之前就出现了内存不足的情况，这可能是问题的根源。

## 配置文件路径

| 配置文件 | 配置内容 | 状态 | 使用端口 |
|---------|--------|-------|------|
| main | `~/.openclaw/openclaw.json` | `~/.openclaw/` | 18789 |
| vesper | `~/.openclaw-vesper/openclaw.json` | `~/.openclaw-vesper/` | 18999 |

**插件自动检测路径**（系统启动时会自动扫描这些路径，无需手动配置）：
- `~/.openclaw/extensions/<plugin-id>/` — 各配置文件中的自定义插件
- `plugins.loadpaths` 文件中列出的路径 — 显式指定的插件

## 认证设置

- Gateway 令牌：`$OPENCLAW_GATEWAY_TOKEN`（环境变量，位于 shell 配置文件 `~/.zshrc`/`~/.bashrc` 中）。**此令牌的优先级高于 `gateway.remote.token`。**所有配置文件都必须使用相同的令牌。

- Gateway 密码：`$OPENCLAW_GATEWAY_PASSWORD`（环境变量，位于 shell 配置文件 `~/.zshrc`/`~/.bashrc` 中）。
- CLI 的认证顺序：`$OPENCLAW_GATEWAY_TOKEN` > `gateway.remote.token`（配置文件中的优先级）
- `gateway.controlUi.dangerouslyDisableDeviceAuth: true` — 仅绕过控制界面（Control UI）的认证机制，不影响 CLI/TUI 的认证流程。

### API 令牌的位置（2026.3.1 版本及以上）

`openclaw.json` 文件的 `auth.profiles` 部分仅用于声明配置文件的类型/模式——不包含实际的令牌信息。
实际的令牌信息存储在每个代理的配置文件中：
```
# Main profile
~/.openclaw/agents/main/agent/auth-profiles.json
~/.openclaw/agents/codex/agent/auth-profiles.json

# Vesper profile
~/.openclaw-vesper/agents/main/agent/auth-profiles.json
~/.openclaw-vesper/agents/codex/agent/auth-profiles.json
```
每个代理的配置文件中都有 `profiles.<provider>:default` 字段，其中包含 OAuth 令牌的 `access`/`refresh`/`expires` 属性，或 API 密钥的 `token` 属性。
`expires` 字段表示令牌的有效期（以毫秒为单位）。可以通过 `Date.now()` 或 `time.time()*1000` 来判断令牌是否过期。

Anthropic 的新令牌文件路径：`~/clawd/inbox/2026-03-03-anthropic-setup-tokens`

### 使用 `openclaw doctor --fix` 进行令牌迁移（2026.3.1 版本）

`openclaw doctor --fix` 命令会从 `openclaw.json` 文件的顶层 `auth.profiles` 中删除令牌相关字段（这是配置文件的更新）。此操作不会影响每个代理的配置文件——这些文件的令牌字段仍然保留原来的名称。

### OpenAI Codex 的 OAuth 令牌刷新

**症状：** 显示 “OAuth token refresh failed for openai-codex” 或 “refresh_token_reused” 错误，表示访问令牌过期或已使用的刷新令牌无效。**解决方法：** 检查 `auth-profiles.json` 文件中的 `expires` 字段——如果令牌的有效期已过，则需要重新认证。**解决方法：** 使用 `openclaw configure` 进行交互式重新认证（如果使用 Vesper 配置文件，请添加 `--profile vesper` 参数）。

### 未配置的备用提供者

**症状：** 显示 “No API key found for provider "<provider>"”，但配置文件中显示了相应的提供者路径。**解决方法：** 要么为该提供者配置相应的信息（使用 `openclaw agents add <provider>` 命令），要么将其从备用配置链中移除（`openclaw.json` 文件中的 `agentsdefaults.model.fallbacks` 配置项）。

## 内存搜索/QMD 功能

在排查故障时，需要检查内存搜索功能的状态：
```bash
openclaw --profile vesper memory status
```
关键配置项：`agentsdefaults.memorySearch.enabled`（位于 `openclaw.json` 文件中）。如果该值为 `false`，即使 `tools.alsoAllow` 中允许使用内存搜索功能，相关工具也不会被启用。
启用该功能需要重启 Gateway（热加载可以加载新的配置，但工具的注册操作仍需要重启系统）。

## 根据配置文件重启 Gateway

| 配置文件 | LaunchAgent plist 文件 | 重启命令 |
|---------|-------------------|--------------|
| main | `~/Library/LaunchAgents/ai.openclawgateway.plist` | `openclaw gateway stop && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist` |
| vesper | `~/Library/LaunchAgents/ai.openclaw.vesper.plist` | `openclaw --profile vesper gateway stop && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.vesper.plist` |

如果 `gateway start` 命令显示 “Gateway service not loaded”，可以直接使用 `launchctl bootstrap` 命令重启 Gateway。

## 问题修复后的后续操作

修复问题后，请执行以下操作：
1. 验证系统状态：使用 `openclaw channels status` 命令查看所有通道的运行状态。
2. 检查系统内存使用情况：使用 `ps -o pid,rss,pcpu,etime -p $(lsof -i :18789 -t | head -1` 命令获取详细信息。
3. 将故障报告写入 `~/clawd/inbox/YYYY-MM-DD-<description>.md` 文件中。

## 故障报告模板

```markdown
# Incident: <Title> — YYYY-MM-DD

## Summary
<1-2 sentences>

## Symptoms
- <what the user saw>

## Root Cause
<what went wrong and why>

## Fix
<what was done>

## Config Changes
| File | Change |
|------|--------|

## Prevention
<how to avoid next time>
```

## 开发版本升级后的检查步骤

在每次升级 OpenClaw 版本后，请执行以下操作：
```bash
openclaw --version
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.pre-upgrade
openclaw doctor --fix
openclaw devices list --json | jq '.pending'
# Approve any pending pairings
openclaw channels status
```

## Vesper 配置文件的命令使用方法

在使用 Vesper 配置文件时，所有命令前需加上 `--profile vesper` 前缀：
```bash
openclaw --profile vesper channels status
openclaw --profile vesper gateway start
openclaw --profile vesper doctor --fix
```