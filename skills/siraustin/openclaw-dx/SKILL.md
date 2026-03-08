---
name: openclaw-dx
description: >
  **诊断并修复 OpenClaw Gateway 的问题**  
  当 Gateway 出现卡顿、无法启动、陷入死循环或拒绝连接的情况时，请使用此方法。该方法适用于主 Gateway 以及使用 `--profile vesper` 配置的 Gateway。具体步骤包括：  
  1. 进行故障排查（triage）；  
  2. 应用相应的修复措施；  
  3. 将故障报告写入 `~/clawd/inbox` 文件夹。
---
# OpenClaw Gateway DX

本文档用于诊断、修复和记录 OpenClaw Gateway 相关的问题，涵盖了主配置文件（端口 18789）以及 vesper 配置文件（端口 18999）中的故障。

## 使用场景

- Gateway 无法启动或陷入死循环
- TUI/CLI 无法连接（需要设备配对、密码不匹配或设备令牌不匹配）
- Gateway 无响应或内存使用过高
- OpenClaw 版本升级后出现问题
- 用户报告 “OpenClaw 卡住了” 等类似情况

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
```

## 常见故障类型

### 0. 故障转移级联（所有提供者均失败）
**症状：** 所有模型均失败（错误代码：`N`），随后会显示每个提供者的具体错误信息。也可能出现 “模型崩溃，无其他提示” 的情况。
**诊断方法：** 检查完整的错误日志链——每个尝试过程依次会尝试使用主配置、备用配置1、备用配置2。只有当所有配置都失败时，用户才会看到错误信息。常见错误示例：
- Anthropic：`AI 服务暂时过载`（可能是临时问题或令牌过期）
- OpenAI Codex：`openai-codex 的 OAuth 令牌刷新失败` 或 `refresh_token_reused`（访问令牌过期或已使用的刷新令牌）
- Google/Gemini：`未找到提供者 “google” 的 API 密钥`（该提供者在 auth-profiles.json 中未配置）
- LM Studio：Python 错误，例如 `AttributeError: 'list' 对象没有 'swapaxes' 属性`（模型推理错误）
**解决方法：** 确定哪个提供者出现了问题并逐一修复：
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
- 对于 OAuth 令牌过期的情况（OpenAI Codex）：使用 `openclaw configure` 进行交互式重新认证。如果使用 vesper 配置文件，请添加 `--profile vesper` 参数。
- 对于缺少提供者密钥的情况（如 Google 等）：使用 `openclaw agents add <provider>` 命令添加相应的提供者，或从备用配置链中移除未配置的提供者。
**预防措施：** 确保备用配置链中的所有提供者都已正确配置。对于可预测的故障模式，应使用相同类型的提供者作为备用选项（例如，使用不同版本的 Anthropic 模型）。

### 1. 通道令牌过期（Slack xoxe.xoxb-）
**症状：** 系统陷入死循环，并显示错误信息 “Error: An API error occurred: token_expired”。
**解决方法：**
```bash
# Disable the channel
# Edit ~/.openclaw/openclaw.json: channels.slack.enabled → false AND plugins.entries.slack.enabled → false
openclaw gateway start
# Then rotate token at api.slack.com and re-enable
```

### 2. 配置信息在升级后被清除
**症状：** Gateway 无法启动，提示 `gateway.mode=local`（当前设置为未设置）。
**解决方法：** 从备份中恢复配置信息：
```bash
ls -la ~/.openclaw/openclaw.json.bak*
# Find the largest/most recent backup with full config
cp ~/.openclaw/openclaw.json.bak-XXXX ~/.openclaw/openclaw.json
openclaw doctor --fix
openclaw gateway start
```

### 3. 旧的锁文件导致问题
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
**症状：** 显示 “unauthorized: device token mismatch” 或 “pairing required” 的错误。
**解决方法：**
```bash
openclaw devices list --json  # check for pending requests
openclaw devices approve "<requestId>" --password "$OPENCLAW_GATEWAY_PASSWORD"
# Or rotate existing device:
openclaw devices rotate --device <id> --role operator --password "$OPENCLAW_GATEWAY_PASSWORD"
```

### 5. 密码不匹配（多配置文件）
**症状：** 显示 “unauthorized: gateway password mismatch” 的错误。
**解决方法：** 在所有配置文件中统一密码设置。所有配置文件都应使用环境变量 `$OPENCLAW_GATEWAY_PASSWORD` 以保持一致。

### 6. 内存占用过高/系统无响应
**症状：** Gateway 处于监听状态但无响应，RSS（内存使用量）超过临界阈值（详见内存阈值部分）。
**解决方法：**
```bash
openclaw gateway stop
sleep 2
kill -9 <pid>  # if still lingering
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### 7. 插件配置无效
**症状：** 显示 “config invalid: plugins.entries.X: plugin not found” 的错误。
**解决方法：** 从 `~/.openclaw/openclaw.json` 中删除无效的插件条目，然后重新启动 Gateway。
**预防措施：** 自 2026.3.2 版本起，所有插件配置文件都必须包含 `configSchema` 字段（即使该字段为空）。创建自定义插件后，请使用 `openclaw doctor --fix` 命令进行检查。

### 8. 端口冲突/存在孤儿进程
**症状：** 端口 18789 被其他程序占用，或者系统中存在多个 Gateway 进程。
**解决方法：**
```bash
ps aux | grep openclaw-gateway | grep -v grep
kill <orphan-pids>
openclaw gateway start
```

### 9. 自定义插件缺少配置文件
**症状：** 系统出现 “plugins: plugin: plugin manifest requires configSchema” 的错误。
**诊断方法：** 检查 `~/.openclaw/extensions/` 目录下的插件文件或 `plugins.loadpaths` 文件，确认插件文件是否缺少 `configSchema` 字段。使用 `openclaw doctor --fix` 命令进行修复。
**解决方法：** 为插件文件添加空的 `configSchema` 字段，然后重启 Gateway：`launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist`。
**预防措施：** 自 2026.3.2 版本起，所有插件配置文件都必须包含 `configSchema` 字段。创建自定义插件后，请务必使用该命令进行验证。

### 10. 配置文件中的 JSON 数据无效（手动编辑导致的问题）
**症状：** CLI 命令执行失败，显示 `json.decoder.JSONDecodeError` 或 “Unexpected token” 的错误。Gateway 可能已经启动，但 CLI/TUI 无法解析配置文件。
**诊断方法：** 有人手动编辑了 `openclaw.json` 文件，导致 JSON 数据无效（例如添加了未加引号的键、多余的逗号等）。请验证并修复 JSON 数据。
**解决方法：** 使用 `openclaw configure` 命令或支持 JSON 格式的编辑器进行修复。手动编辑后，请使用以下 Python 代码验证 JSON 数据的有效性。

### 11. 缺少 `gateway.remote.token`（使用令牌认证的模式）
**症状：** CLI/TUI 报错 “gateway token missing”。
**诊断方法：** Gateway 使用 `gateway.auth.mode: "token"` 进行认证，但未设置 `gateway.remote.token`。CLI 会尝试读取 `remote.token` 进行验证，如果该字段未设置，则所有连接都会被拒绝。
**解决方法：** 设置 `gateway.remote.token` 使其与 `gateway.auth.token` 值一致：
```bash
# In openclaw.json, inside the "gateway" section:
"remote": {
  "token": "<same value as gateway.auth.token>"
}
```
然后重启 Gateway。
**注意：** 使用 `gateway.auth.mode: "token"` 的配置文件需要设置 `gateway.remote.token`。使用密码认证（`$OPENCLAW_GATEWAY_PASSWORD`）的配置文件不受此影响。

### 12. 配置文件更新后引发重启问题（LaunchAgent 未正确加载）
**症状：** Gateway 停止运行，端口未处于监听状态，`launchctl print` 显示服务未找到。错误日志显示 “config change requires gateway restart”，但重启失败。
**诊断方法：** 多次执行 `config.patch` 操作（例如通过 Gateway 工具）修改了 `gateway.auth.*` 等配置项，导致重启失败。重启机制可能因以下原因失败：
- `spawnSync launchctl ETIMEDOUT`
- `Bootstrap failed: 5: Input/output error`

在这种情况下，Gateway 会尝试在进程中重启，但可能导致系统不稳定，最终接收 SIGTERM 信号，从而导致 LaunchAgent 未正确加载。
**解决方法：**
```bash
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```
**预防措施：**
- 将涉及 `gateway.auth.*` 的配置更改集中到一个 `config.patch` 操作中，以减少重启次数。
- 这是 OpenClaw 2026.3.x 版本中的一个已知问题——LaunchAgent 的重启机制在多种故障情况下都可能不可靠。
- 可以考虑使用 watchdog 或在 plist 文件中设置 `ThrottleInterval=30` 来防止频繁重启。
- 如果使用 Gateway 工具的 `config.patch` 功能，请将认证、插件配置和压缩操作合并到一个请求中。

## 内存阈值

| RSS | 状态 | 处理方式 |
|-----|--------|--------|
| < 500MB | 正常 | 无需特殊处理 |
| 500MB-1.5GB | 内存使用量较高 | 监控内存使用情况 |
| 1.5GB-2.5GB | 内存使用量过高 | 安排重启 |
| > 2.5GB | 内存使用量严重过高 | 立即重启 |

## Node.js 内存优化

Gateway 使用 Node.js 运行，默认情况下最大允许使用 4GB 的内存空间。对于长时间运行的 Gateway 或加载了大量插件的情况，可以通过修改 LaunchAgent plist 文件中的 `ProgramArguments` 参数来增加内存限制：
```xml
<string>--max-old-space-size=16384</string>
```

将以下代码插入 `node` 可执行文件的路径之后、JS 文件之前：
- **vesper** 配置：`--max-old-space-size=16384`（16GB）——适用于处理 QMD 或内存搜索等任务
- **main** 配置：未设置（默认值为 4GB）

如需添加或修改配置，请直接编辑 plist 文件并重新加载：
```bash
# Edit the plist
nano ~/Library/LaunchAgents/ai.openclaw.gateway.plist
# Reload
launchctl bootout gui/501/ai.openclaw.gateway && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

如果 Gateway 在达到上述内存阈值之前就因内存不足而崩溃，尝试此方法可能有助于解决问题。

## 配置文件路径

| 配置文件 | 文件路径 | 状态 | 使用端口 |
|---------|--------|-------|------|
| main | `~/.openclaw/openclaw.json` | `~/.openclaw/` | 18789 |
| vesper | `~/.openclaw-vesper/openclaw.json` | `~/.openclaw-vesper/` | 18999 |

**插件自动发现路径**（启动时会自动扫描，无需手动配置）：
- `~/.openclaw/extensions/<plugin-id>/` — 各配置文件下的自定义插件
- `plugins.loadpaths` 文件中列出的路径 — 显式指定的插件

## 认证设置

- Gateway 密码：`$OPENCLAW_GATEWAY_PASSWORD`（环境变量，位于 shell 配置文件 `~/.zshrc` 中 [macOS] 或 `~/.bashrc` 中 [Linux/Bash]）
- `gateway.controlUi.dangerouslyDisableDeviceAuth: true` — 仅禁用控制界面（CLI/TUI）的认证功能
- 自 2026.2.25 版本起，CLI/TUI 必须进行设备配对

### API 令牌存储位置（v2026.3.1 及更高版本）

在 `openclaw.json` 的顶级配置文件 `auth.profiles` 中仅声明配置文件的类型/模式——实际的令牌信息存储在每个代理的配置文件中：
```
# Main profile
~/.openclaw/agents/main/agent/auth-profiles.json
~/.openclaw/agents/codex/agent/auth-profiles.json

# Vesper profile
~/.openclaw-vesper/agents/main/agent/auth-profiles.json
~/.openclaw-vesper/agents/codex/agent/auth-profiles.json
```
每个代理的配置文件中包含 `profiles.<provider>:default` 字段，其中包含 OAuth 令牌的 `access`/`refresh`/`expires` 属性，或 API 密钥的 `token` 属性。
`expires` 字段的值表示令牌的有效时间（以毫秒为单位），可通过 `Date.now()` 或 `time.time()*1000` 进行验证。

新的 Anthropic 设置令牌文件路径：`~/clawd/inbox/2026-03-03-anthropic-setup-tokens`

### 使用 `openclaw doctor --fix` 进行令牌迁移（v2026.3.1）

`openclaw doctor --fix` 命令会从 `openclaw.json` 的顶级配置文件中删除 `token` 字段。此操作不会影响每个代理的配置文件——这些文件的令牌字段仍保留原样。即使执行了此命令，Gateway 仍能正常运行，因为它会在运行时从代理的配置文件中读取令牌信息。

### OpenAI Codex 的 OAuth 令牌刷新

**症状：** `openai-codex` 的 OAuth 令牌刷新失败或 `refresh_token_reused`（访问令牌过期或已使用）。
**解决方法：** 检查 `auth-profiles.json` 文件中的 `expires` 字段——如果该字段的值表示令牌已过期，则需要重新认证。可以使用 `openclaw configure` 进行交互式重新认证（如果使用 vesper 配置文件，请添加 `--profile vesper` 参数）。

### 未配置的备用提供者

**症状：** 显示 “No API key found for provider "<provider>"” 的错误。
**诊断方法：** 配置文件中的备用提供者路径指向一个从未在 auth-profiles.json 中配置的提供者。
**解决方法：** 要么为该提供者配置相应的信息（使用 `openclaw agents add <provider>` 命令），要么从 `openclaw.json` 文件的备用配置链中移除该提供者。

## 内存搜索/QMD 功能

在排查故障时，请检查内存搜索功能的状态：
```bash
openclaw --profile vesper memory status
```
关键配置参数：`agentsdefaults.memorySearch.enabled` 在 `openclaw.json` 中。如果该参数设置为 `false`，即使插件在 `tools.alsoAllow` 列表中，相关功能也不会被启用。
启用该功能需要重启 Gateway（热加载可以更新配置，但插件注册仍需重启）。

## 根据配置文件重启 Gateway

| 配置文件 | LaunchAgent plist 文件 | 重启命令 |
|---------|-------------------|--------------|
| main | `~/Library/LaunchAgents/ai.openclaw.gateway.plist` | `openclaw gateway stop && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist` |
| vesper | `~/Library/LaunchAgents/ai.openclaw.vesper.plist` | `openclaw --profile vesper gateway stop && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.vesper.plist` |

如果 `gateway start` 命令显示 “Gateway service not loaded”，可以直接使用 `launchctl bootstrap` 命令重启 Gateway。

## 问题修复后的后续操作

修复问题后，请执行以下步骤：
1. 验证系统状态：使用 `openclaw channels status` 命令确认所有通道是否正常运行。
2. 检查内存使用情况：使用 `ps -o pid,rss,pcpu,etime -p $(lsof -i :18789 -t | head -1` 命令查看进程信息。
3. 将故障详情记录到 `~/clawd/inbox/YYYY-MM-DD-<description>.md` 文件中。

## 事故报告模板

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

## vesper 配置文件的命令前缀

在使用 vesper 配置文件时，所有命令前需加上 `--profile vesper` 前缀：
```bash
openclaw --profile vesper channels status
openclaw --profile vesper gateway start
openclaw --profile vesper doctor --fix
```