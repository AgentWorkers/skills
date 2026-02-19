---
name: token-monitor
description: Monitor OpenClaw token/quota usage and alert when any quota drops below a threshold (default 20%). Uses `openclaw models status` and writes only a local state file to avoid duplicate alerts. **Does not handle secrets.** **Token cost:** Script itself: 0 tokens (pure bash). Heartbeat integration: ~1k-2k tokens/hour (reading HEARTBEAT.md + executing script). Alert delivery: ~500-1k tokens/alert. **Optimization:** Use system cron instead of heartbeat to reduce to ~0 tokens (except alerts).
---

# 令牌监控器（Token Monitor）

该工具用于监控 OpenClaw 的令牌使用情况及配额消耗情况，并在配额使用量降至可配置的阈值（默认为 20%）以下时发出警报。

## 主要功能

- **支持多种提供者**：监控所有已配置的提供者（如 openai-codex、github-copilot、google-antigravity 等）。
- **多配额跟踪**：跟踪多种类型的配额（5 小时、每日、高级、聊天等）。
- **智能警报机制**：仅在新出现配额不足的情况时发出警报，避免频繁的干扰。
- **配额恢复通知**：当配额使用量回升至阈值以上时发送通知。
- **状态持久化**：在多次运行过程中保留之前的警告记录。

## 安装/更新（通过 ClawHub）

安装：
```bash
clawhub install token-monitor
```

更新：
```bash
clawhub update token-monitor
```

（您也可以运行 `clawhub update --all` 来更新所有技能。）

---

## 禁用/卸载

### 如果通过 `HEARTBEAT.md` 启用
只需从 `HEARTBEAT.md` 中删除相关配置即可（或将其注释掉），无需额外进行卸载操作。

### 如果通过 OpenClaw 的 cron 作业启用
禁用/删除相应的 cron 作业：
```bash
openclaw cron list
openclaw cron remove <jobId>
```

### 可选的状态清理操作
```bash
rm -f ~/.openclaw/workspace/skills/token-monitor/.token-state.json
```

---

## 使用方法

### 手动检查
直接运行监控脚本：
```bash
skills/token-monitor/scripts/check-quota.sh
```

如果该工具已安装到 `~/.openclaw/skills` 目录下，可运行以下命令：
```bash
~/.openclaw/skills/token-monitor/scripts/check-quota.sh
```

### 使用自定义阈值（默认为 20%）
```bash
skills/token-monitor/scripts/check-quota.sh --threshold 10
```

### 自动监控（通过 Heartbeat）
将以下代码添加到 `HEARTBEAT.md` 中以实现定期检查：
```markdown
## Token Monitor (every ~60min, rotate)

Check model quotas and alert if below threshold.

**Instructions:**
1. Run `output=$(skills/token-monitor/scripts/check-quota.sh 2>&1)`
2. If output non-empty → send wake event with output text
3. If empty → all quotas OK, continue silently

**Rotate check:** Only run every ~4th heartbeat (once/hour if heartbeat is 15min)

**Example integration:**
```
bash
output=$(skills/token-monitor/scripts/check-quota.sh 2>&1)
if [[ -n "$output" ]]; then
  openclaw cron wake --text "$output" --mode now
fi
```
```

### 自动监控（通过 Cron 作业）
创建一个专门的 cron 作业以实现定时检查：
```bash
openclaw cron add --schedule "*/30 * * * *" \
  --payload '{"kind":"systemEvent","text":"Run quota monitor: skills/token-monitor/scripts/check-quota.sh"}' \
  --name "Token Monitor (30min)"
```

## 输出结果

- **配额不足警报**：```
⚠️ Model Quota Alert (<20%):
• openai-codex Day: 0% left
• github-copilot Premium: 5% left
```
- **配额恢复警报**：```
✅ Quota Recovered (>=20%):
• openai-codex 5h: 100% left
```

## 状态文件
该脚本会将监控状态保存在以下文件中：
```
~/.openclaw/workspace/skills/token-monitor/.token-state.json
```

示例状态文件内容：
```json
{
  "warned": [
    "openai-codex Day: 0% left",
    "github-copilot Premium: 5% left"
  ],
  "current": [
    "openai-codex:5h=100",
    "openai-codex:Day=0",
    "github-copilot:Premium=5",
    "github-copilot:Chat=100"
  ],
  "lastCheck": "2026-02-15T09:30:00Z",
  "threshold": 20
}
```

## 配置参数

- `QUOTA_THRESHOLD`：警报阈值百分比（默认：20%）
- `QUOTA_STATE_FILE`：状态文件的路径（默认：`~/.openclaw/workspace/skills/token-monitor/.token-state.json`）

### 命令行参数
- `--threshold <pct>`：设置警报阈值（会覆盖 `QUOTA_THRESHOLD` 的默认值）
- `--state-file <path>`：设置状态文件的路径（会覆盖 `QUOTA_STATE_FILE` 的默认值）

## 工作原理

1. **解析配额数据**：运行 `openclaw models status` 命令并提取所有关于配额剩余量的信息。
2. **识别配额不足的情况**：找出所有低于阈值的配额。
3. **与历史状态进行比较**：判断是否有新的配额不足事件或配额已恢复。
4. **发送警报**：使用 `openclaw cron wake` 命令发送通知。
5. **更新状态**：保存当前的状态信息以供下一次运行时使用。

## 所需依赖库/工具

- `openclaw` 命令行工具（用于获取模型状态和触发 cron 作业）
- `jq`（用于解析 JSON 数据）
- `bash` 4.0 或更高版本

## 常见问题排查

- **未收到警报**：
  - 确认配额使用量确实低于阈值：运行 `openclaw models status` 命令。
  - 检查状态文件的权限设置：`cat ~/.openclaw/workspace/skills/token-monitor/.token-state.json`。
  - 手动运行脚本查看输出结果：`skills/token-monitor/scripts/check-quota.sh`。

- **收到重复警报**：
  - 可能是状态文件损坏或被删除，请检查文件内容（使用 `jq .warned ~/.openclaw/workspace/skills/token-monitor/.token-state.json`）。
- **脚本执行失败**：
  - 确保已安装 `jq`：`jq --version`。
  - 检查脚本的权限设置：`ls -l skills/token-monitor/scripts/check-quota.sh`。
  - 以详细输出模式运行脚本：`bash -x skills/token-monitor/scripts/check-quota.sh`。