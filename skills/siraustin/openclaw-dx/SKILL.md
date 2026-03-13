---
name: openclaw-dx
version: 1.7.0
license: MIT
description: >
  **诊断并修复 OpenClaw Gateway 的问题**  
  当 Gateway 出现卡顿、无法启动、陷入死循环或拒绝连接的情况时，请使用此方法。该方法适用于默认（main）配置以及使用 `--profile vesper` 配置的 Gateway。具体步骤包括：  
  1. 进行故障排查（triage）；  
  2. 应用相应的修复措施；  
  3. 将故障报告（incident report）保存到 `~/clawd/inbox` 目录中。
---
# OpenClaw Gateway DX

本文档用于诊断、修复和记录 OpenClaw Gateway 相关的问题，涵盖了主配置文件（端口 18789）以及 vesper 配置文件（端口 18999）中的问题。

## 使用场景

- Gateway 无法启动或进入死循环
- TUI/CLI 无法连接（需要配对、密码不匹配或设备令牌不匹配）
- Gateway 无响应或内存使用过高
- OpenClaw 版本升级后出现问题
- 用户报告“OpenClaw 卡住了”或其他类似问题

## 问题排查流程

请同时执行以下步骤以评估 Gateway 的状态：

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

# 12. Session token counts (context overflow check)
for dir in ~/.openclaw ~/.openclaw-vesper; do
  f="$dir/agents/main/sessions/sessions.json"
  [ -f "$f" ] && echo "=== $(basename $dir) ===" && python3 -c "
import json
data=json.load(open('$f'))
for k,v in data.items():
    t=v.get('contextTokens',0)
    pct=t/200000*100
    flag=' ⚠️ BLOATED' if pct>75 else ''
    print(f'  {k}: {t:,} tokens ({pct:.0f}%){flag}')
"
done

# 12. Verify plist profile alignment
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.gateway.plist
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.vesper.plist
```

## 常见故障模式

### 0. 故障转移级联（所有提供者均故障）
**症状：**“所有模型均失败”（N 个模型均失败），随后会显示每个提供者的具体错误信息。也可能出现“模型崩溃，无其他提示信息”（退出代码：null）。
**诊断方法：**检查完整的错误链——每次尝试都会依次尝试使用主配置、备用配置1、备用配置2。只有当所有配置都失败时，用户才会看到错误信息。常见提供者的错误信息如下：
- Anthropic：`AI 服务暂时过载`（可能是临时性问题或令牌过期）
- OpenAI Codex：`openai-codex 的 OAuth 令牌刷新失败` 或 `refresh_token_reused`（访问令牌过期或已使用的刷新令牌）
- Google/Gemini：`未找到提供者 "google" 的 API 密钥`（该提供者在 auth-profiles.json 中未配置）
- LM Studio：Python 错误，例如 `AttributeError: 'list' 对象没有 'swapaxes' 属性`（模型推理错误）
**修复方法：**确定哪个提供者出现了问题，并逐一修复：
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
- 对于 OAuth 令牌过期的问题（OpenAI Codex）：使用 `openclaw configure` 进行交互式重新认证。如果使用 vesper 配置文件，请添加 `--profile vesper` 参数。
- 对于缺少提供者密钥的问题（如 Google 等）：使用 `openclaw agents add <provider>` 命令添加相应的提供者，或从备用配置链中移除未配置的提供者。
**预防措施：**确保备用配置链中的所有提供者都已正确配置。对于容易出问题的情况，应使用相同类型的提供者作为备用选项。

### 1. 通道令牌过期（Slack xoxe.xoxb-）
**症状：**出现死循环，并显示错误信息：“Error: An API error occurred: token_expired”。
**修复方法：**
```bash
# Disable the channel
# Edit ~/.openclaw/openclaw.json: channels.slack.enabled → false AND plugins.entries.slack.enabled → false
openclaw gateway start
# Then rotate token at api.slack.com and re-enable
```

### 2. 配置信息在升级后被清除
**症状：**Gateway 启动失败，提示 `gateway.mode=local`（当前设置为未设置）。
**修复方法：**从备份中恢复配置信息：
```bash
ls -la ~/.openclaw/openclaw.json.bak*
# Find the largest/most recent backup with full config
cp ~/.openclaw/openclaw.json.bak-XXXX ~/.openclaw/openclaw.json
openclaw doctor --fix
openclaw gateway start
```

### 3. 旧锁定文件导致问题
**症状：**Gateway 无法启动，仍然使用旧的进程 ID（PID）。
**修复方法：**
```bash
ls ~/.openclaw/gateway.*.lock
cat ~/.openclaw/gateway.*.lock  # check PID
kill -0 <pid>  # verify dead
rm ~/.openclaw/gateway.*.lock
openclaw gateway start
```

### 4. 设备令牌不匹配/需要配对
**症状：**显示“unauthorized: device token mismatch”或“pairing required”。
**修复方法：**
```bash
openclaw devices list --json  # check for pending requests
openclaw devices approve "<requestId>" --password "$OPENCLAW_GATEWAY_PASSWORD"
# Or rotate existing device:
openclaw devices rotate --device <id> --role operator --password "$OPENCLAW_GATEWAY_PASSWORD"
```

### 5. 密码不匹配（多配置文件）
**症状：**显示“unauthorized: gateway password mismatch”。
**修复方法：**在所有配置文件中同步密码。所有配置文件都应使用环境变量 `$OPENCLAW_GATEWAY_PASSWORD`，以确保与 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）中的值一致。

### 6. 内存使用过高/ Gateway 无响应
**症状：**Gateway 处于监听状态但无响应，RSS（内存使用量）超过临界阈值（详见“内存阈值”部分）。
**修复方法：**
```bash
openclaw gateway stop
sleep 2
kill -9 <pid>  # if still lingering
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### 7. 插件配置无效
**症状：**显示“config invalid: plugins.entries.X: plugin not found”。
**修复方法：**从 `~/.openclaw/openclaw.json` 中删除无效的插件配置，然后重新启动 Gateway。
**预防措施：**从 2026.3.2 版本起，所有插件配置文件都必须包含 `configSchema` 字段。创建自定义插件后，请使用 `openclaw doctor --fix` 命令进行检查。

### 8. 配置文件中的 JSON 无效（手动编辑导致的问题）
**症状：**CLI 命令执行失败，提示 `json.decoder.JSONDecodeError` 或 `Unexpected token`。Gateway 可能已经启动，但 CLI/TUI 无法解析配置文件。
**修复方法：**验证并修复 JSON 文件中的错误内容。
**预防措施：**建议使用 `openclaw configure` 命令或支持 JSON 格式的编辑器进行编辑。手动编辑后，请使用上述 Python 代码片段进行验证。

### 9. 缺少 `gateway.remote.token`（使用令牌认证的模式）
**症状：**CLI/TUI 报错“gateway token missing”。
**修复方法：**设置 `gateway.remote.token` 使其与 `gateway.auth.token` 的值一致。
**注意：**仅在使用 `gateway.auth.mode: "token"` 的配置文件中需要设置 `gateway.remote.token`。使用密码认证（`$OPENCLAW_GATEWAY_PASSWORD`）的配置文件不受此影响。

### 10. 配置文件更新后导致重启失败
**症状：**Gateway 停止运行，端口无法监听，`launchctl print` 显示服务未找到。错误日志提示“config change requires gateway restart”，但重启失败。
**修复方法：**将多次对 `gateway.auth.*` 的配置更改合并为一次 `config.patch` 操作，以减少重启次数。
**预防措施：**
- 这是一个在 OpenClaw 2026.3.x 版本中反复出现的上游 bug——LaunchAgent 的重启机制在处理多种错误时不够可靠。
- 可以考虑使用 watchdog 或在 plist 中设置 `ThrottleInterval=30` 来防止重启频繁发生。
- 如果使用 Gateway 工具的 `config.patch` 功能，请将认证、插件配置和压缩配置合并为一次操作。

### 11. `OPENCLAW_GATEWAY_TOKEN` 环境变量覆盖了多配置文件中的令牌认证设置
**症状：**即使配置文件中的 `gateway.auth.token` 和 `gateway.remote.token` 值匹配，使用 `openclaw --profile vesper` 时仍显示“unauthorized: gateway token mismatch”。
**修复方法：**确保所有配置文件使用相同的认证令牌。
**预防措施：**当使用 `OPENCLAW_GATEWAY_TOKEN` 环境变量时，所有配置文件必须使用相同的令牌值。

### 12. LaunchAgent 配置文件被错误覆盖
**症状：**Gateway 停止运行，端口无法监听，`launchctl print` 显示服务未找到。错误日志提示“config change requires gateway restart”，但重启失败。
**修复方法：**检查 `ai.openclaw.gateway.plist` 文件，确保它指向正确的配置文件路径。
**预防措施：**运行 `openclaw --profile <name> gateway install` 命令后，请确认两个配置文件仍然指向正确的配置文件。

### 13. 会话上下文溢出导致问题
**症状：**接收到的消息无法被处理。机器人显示“typing”状态约 2 分钟后停止（“typing TTL reached”）。所有提供者（Anthropic、Codex、Gemini）都会出现此问题。切换提供者也无法解决问题。
**修复方法：**重置过大的会话数据。
**预防措施：**
- 确保所有配置文件都启用了 `contextPruning` 设置：`{"mode": "cache-ttl", "ttl": "1h", "keepLastAssistants": 5}`。
- 监控会话令牌的数量，当某个会话的大小超过 150K（75%）时发出警报。
- 对于长时间运行的会话，可以考虑定期执行 `reset` 操作（每周一次）。

### 14. 代理在 API 调用中卡住
**症状：**接收到的消息无法被处理。日志中没有任何错误信息。`lane wait exceeded` 指标未触发。
**修复方法：**重启 Gateway。
**预防措施：**
- 确保压缩模型提供者的认证设置有效（例如 `google-gemini-cli`）。
- 将 `timeoutSeconds` 从 1800（30 分钟）调整为 600（10 分钟），以便更快地检测到卡住的调用。
- 监控通道的输入/输出延迟情况——如果输出延迟超过输入超过 5 分钟，则说明代理卡住了。

### 15. 压缩模型超时（上下文退化）
**症状：**消息被处理，但上下文质量下降。代理“忘记”了最近的对话内容。
**修复方法：**更换压缩模型，选择更快/更可靠的压缩模型。
**推荐的压缩模型：**
- `anthropic/claude-sonnet-4-6`——可靠且处理速度快
- `anthropic/claude-sonnet-4-20250514`——性能类似
- `google-gemini-cli/gemini-2.5-flash`——价格较低，但容易超时

## 内存阈值

| RSS | 状态 | 处理措施 |
|-----|--------|--------|
| < 500MB | 正常 | 无需特殊处理 |
| 500MB-1.5GB | 内存使用量较高 | 监控内存使用情况 |
| 1.5GB-2.5GB | 内存使用量高 | 安排重启 |
| > 2.5GB | 内存使用量极高 | 立即重启 |

## Node.js 堆内存调优

Gateway 使用 Node.js 运行，默认的最大堆内存为 4GB。对于长时间运行的 Gateway 或加载了大量插件的情况，可以通过修改 LaunchAgent 配置文件中的 `--max-old-space-size` 参数来增加堆内存大小：

```xml
<string>--max-old-space-size=16384</string>
```

该参数应插入 `node` 可执行文件的路径之后、JS 配置文件之前。当前配置如下：
- **vesper**：`--max-old-space-size=16384`（16GB）——适用于处理 QMD/内存搜索任务
- **main**：未设置（Node.js 默认值为 4GB）

要修改配置，请直接编辑 plist 文件并重新加载：

```bash
# Edit the plist
nano ~/Library/LaunchAgents/ai.openclaw.gateway.plist
# Reload
launchctl bootout gui/501/ai.openclaw.gateway && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

如果 Gateway 在达到上述内存阈值之前就发生了 Out of Memory（OOM）错误，这可能是导致问题的原因。

## 配置文件路径

| 配置文件 | 配置内容 | 状态 | 使用端口 |
|---------|--------|-------|------|
| main | `~/.openclaw/openclaw.json` | `~/.openclaw/` | 18789 |
| vesper | `~/.openclaw-vesper/openclaw.json` | `~/.openclaw-vesper/` | 18999 |

**插件自动发现路径**（启动时会自动扫描，无需手动配置）：
- `~/.openclaw/extensions/<plugin-id>/` — 每个配置文件对应的自定义插件
- `plugins.loadpaths` 中列出的路径 — 显式指定的插件

## 认证设置

- Gateway 令牌：`$OPENCLAW_GATEWAY_TOKEN`（环境变量，位于 shell 配置文件 `~/.zshrc`/`~/.bashrc` 中）。此令牌的优先级高于 `gateway.remote.token`。所有配置文件都必须使用相同的令牌。
- Gateway 密码：`$OPENCLAW_GATEWAY_PASSWORD`（环境变量，位于 shell 配置文件 `~/.zshrc`/`~/.bashrc` 中）。
- CLI 的认证优先级：`$OPENCLAW_GATEWAY_TOKEN` > `gateway.remote.token`。
- `gateway.controlUi.dangerouslyDisableDeviceAuth`：仅绕过控制界面（Control UI），不影响 CLI/TUI 的认证过程。

### API 令牌的位置（2026.3.1 版本起）

`openclaw.json` 的顶级 `auth.profiles` 文件仅用于声明配置文件的类型/模式，不包含实际的令牌信息。实际的令牌信息存储在每个代理的配置文件中：

```
# Main profile
~/.openclaw/agents/main/agent/auth-profiles.json
~/.openclaw/agents/codex/agent/auth-profiles.json

# Vesper profile
~/.openclaw-vesper/agents/main/agent/auth-profiles.json
~/.openclaw-vesper/agents/codex/agent/auth-profiles.json
```

每个代理的配置文件中都有 `profiles.<provider>:default` 字段，其中包含 OAuth 令牌的 `access`/`refresh`/`expires` 属性，或 API 密钥的 `token` 属性。
`expires` 字段的值以秒为单位表示令牌的有效期（与 `Date.now()` 或 `time.time()*1000` 进行比较）。

Anthropic 的新令牌文件位于：`~/clawd/inbox/2026-03-03-anthropic-setup-tokens`

### `openclaw doctor --fix` 命令用于令牌迁移（2026.3.1 版本）

`openclaw doctor --fix` 会从 `openclaw.json` 的顶级 `auth.profiles` 文件中删除令牌字段。这不会影响每个代理的配置文件——这些文件仍然使用 `token` 作为令牌字段名。即使执行了该命令，Gateway 也能正常运行，因为它会在运行时从每个代理的配置文件中读取令牌信息。

### OpenAI Codex 的 OAuth 令牌刷新

**症状：**`openai-codex` 的 OAuth 令牌刷新失败或 `refresh_token_reused`——访问令牌过期或已使用。

**修复方法：**进行交互式重新认证：使用 `openclaw configure` 命令（如果使用 vesper 配置文件，请添加 `--profile vesper` 参数）。

### 未配置的备用提供者

**症状：**显示“未找到提供者 "<provider>" 的 API 密钥”。

**修复方法：**要么为该提供者配置相应的信息（使用 `openclaw agents add <provider>` 命令），要么从 `openclaw.json` 的备用配置链中移除该提供者。

## 内存搜索/QMD

在代理无法正常响应时，可以通过检查内存搜索状态来排查问题：

```bash
openclaw --profile vesper memory status
```

相关配置参数：`agents.defaults.memorySearch.enabled`，位于 `openclaw.json` 文件中。如果该参数设置为 `false`，即使 `tools.alsoAllow` 中列出了相关工具，这些工具也不会被启用。

启用内存搜索功能需要重启 Gateway（热加载可以加载新的配置，但工具的注册需要重启）。

## QMD / 内存搜索调试

`qmd` 在 **Node.js** 上运行（使用 `#!/usr/bin/env node`），而不是 Bun。`sqlite-vec` 扩展在 Node.js 的 `better-sqlite3` 环境下可以正常工作。之前关于 `sqlite-vec/Bun` 的问题对 OpenClaw 用户来说是不相关的。

如果 `qmd embed` 命令执行失败，可以使用以下命令进行调试：

```bash
# 1. Check Homebrew SQLite is installed
brew list sqlite

# 2. Rebuild better-sqlite3 if needed
npm rebuild better-sqlite3 --build-from-source
# Note: npm v11 warns about --build-from-source but the flag still works (cosmetic warning)

# 3. Check embedding status
qmd status  # Shows pending embedding count

# 4. Force re-embedding of all content
qmd embed -f

# 5. Update collections that may have new files
qmd update <collection>  # e.g., tool-heuristics collections after adding files
```

用于内存搜索调试的常用命令：
- `qmd status` — 显示集合信息、文档数量和待处理的嵌入操作
- `qmd embed` — 执行嵌入操作
- `qmd embed -f` — 强制重新嵌入所有内容
- `qmd update <collection>` — 重新扫描集合中的文件

## 根据配置文件重启 Gateway

| 配置文件 | LaunchAgent 配置文件 | 重启命令 |
|---------|-------------------|--------------|
| main | `~/Library/LaunchAgents/ai.openclaw.gateway.plist` | `openclaw gateway stop && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist` |
| vesper | `~/Library/LaunchAgents/ai.openclaw.vesper.plist` | `openclaw --profile vesper gateway stop && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.vesper.plist` |

如果 `gateway start` 命令显示“Gateway service not loaded”，可以直接使用 `launchctl bootstrap` 命令重启 Gateway。

## 问题修复后的后续操作

修复问题后，请执行以下操作：
1. 验证 Gateway 的运行状态：所有通道应显示为“running”状态。
2. 检查内存使用情况：使用 `ps -o pid,rss,pcpu,etime -p $(lsof -i :18789 -t | head -1)` 命令查看详细信息。
3. 将问题记录写入 `~/clawd/inbox/YYYY-MM-DD-<description>.md` 文件中。

## 问题报告模板

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

## OpenClaw 版本升级后的检查步骤

在升级 OpenClaw 版本后，请执行以下操作：

```bash
openclaw --version
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.pre-upgrade
openclaw doctor --fix
openclaw devices list --json | jq '.pending'
# Approve any pending pairings
openclaw channels status
```

## vesper 配置文件的命令使用方法

在使用 vesper 配置文件时，所有命令前需加上 `--profile vesper` 前缀：

```bash
openclaw --profile vesper channels status
openclaw --profile vesper gateway start
openclaw --profile vesper doctor --fix
```