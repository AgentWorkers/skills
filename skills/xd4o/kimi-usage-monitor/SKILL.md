---
name: kimi-usage-monitor
description: 通过 Kimi 控制台监控 Kimi K2.5 API 的使用情况和配额。在以下情况下需要使用该功能：  
(1) 查看剩余使用百分比并重置计时器；  
(2) 根据可用配额自主决定任务优先级；  
(3) 在开始密集型操作前监控速率限制状态；  
(4) 记录使用情况以用于资源规划。  
对于在配额限制下运行的自主管理代理而言，此功能至关重要。
---

# Kimi 使用监控

通过 Kimi 控制台监控 Kimi K2.5 的使用配额，以便更明智地决定任务优先级和资源分配。

## 何时使用此功能

- **在密集操作之前**：在开始多步骤研究或编码任务之前，检查配额情况。
- **自主规划**：根据剩余使用百分比自行安排任务优先级。
- **了解速率限制**：知道何时可以重新使用配额来处理高优先级任务。
- **使用跟踪**：记录使用模式以进行长期容量规划。

## 快速入门

**先决条件**：安装了 OpenClaw 扩展程序的 Chrome 浏览器
1. 打开 Chrome → `https://www.kimi.com/code/console?from=membership`
2. 点击 OpenClaw 扩展程序图标（图标应显示为“开启”状态）。
3. 确保已登录 Kimi。

```bash
# Check current usage (Linux/macOS/WSL)
./check_usage.sh

# Windows native
check_usage.bat           # CMD
.\check_usage.ps1         # PowerShell

# JSON output for automation (all platforms)
python3 scripts/fetch_usage.py --json
```

**平台支持**：Linux ✅ | macOS ✅ | Windows (WSL) ✅ | Windows (Native) ✅

## 可用的使用数据

Kimi 控制台显示以下信息：

| 指标 | 描述 | 决策阈值 |
|--------|-------------|-------------------|
| **每周使用量** | 占用每周配额的百分比 | >75% = 优先处理 |
| **每周重置时间** | 配额重置前的剩余时间 | 在重置后安排繁重任务 |
| **速率限制** | 额外的速率限制配额 | 作为备用资源 |
| **速率限制重置时间** | 速率限制重置前的剩余时间 | 作为短期缓冲 |

## 自主决策指南

在自主操作时，参考以下规则：

**🟢 容量充足（剩余 >50%）**
- 全力执行任务
- 接受多步骤研究任务
- 根据需要创建子代理
- 启用详细推理功能

**🟡 容量适中（剩余 25-50%）**
- 批量处理相似操作
- 优先选择简洁的输出结果
- 少量使用子代理
- 关闭非必要的推理功能

**🔴 容量不足（剩余 <25%）**
- 仅执行必要任务
- 仅执行单步操作
- 避免创建子代理
- 优先处理用户直接指定的任务，而非主动发起的任务

## 在执行密集操作前的检查

在创建子代理或开始多步骤任务之前，请先检查系统容量：

```bash
# Check if operation should proceed
python3 scripts/preflight_check.py [light|standard|intensive]

# Light: single query, simple task (needs 10%)
# Standard: normal subagent, research (needs 25%)
# Intensive: multi-subagent, deep research (needs 50%)
```

如果检查通过，返回退出代码 0；否则返回 1。可在脚本中使用此代码：

```bash
if python3 scripts/preflight_check.py intensive; then
    # Proceed with intensive operation
    sessions_spawn "Complex research task..."
fi
```

## 子代理监控

在创建子代理之前，请进行以下检查：

```bash
python3 scripts/subagent_guard.py
```

返回一个包含 `can_spawn` 值的 JSON 对象：
```json
{
  "can_spawn": true,
  "usage_percent": 45,
  "remaining_percent": 55,
  "resets_hours": 36
}
```

## 集成建议

- **每小时监控任务**：使用 cron 任务进行监控。
- **任务执行前验证**：在执行任务前进行额外检查。

## 脚本参考

| 脚本 | 用途 |
|--------|---------|
| `scripts/fetch_usage.py` | 主要的使用量采集脚本（基于浏览器） |
| `scripts/usage_logger.py` | 自动记录使用情况并辅助决策 |
| `scripts/preflight_check.py` | 在执行任务前进行验证 |
| `scripts/subagent_guard.py` | 在创建子代理前进行检查 |
| `check_usage.sh` | 快速的命令行工具 |

**注意**：对于非 OpenClaw 环境，也有基于 Playwright 的替代脚本（`fetch_kimi_usage.py`），但需要额外的系统依赖。

## 故障排除

- **“浏览器不可用”**：确保已安装 OpenClaw 扩展程序，并且图标显示为“开启”状态。
- **“无法检测到使用情况”**：确认已登录 Kimi，并检查控制台页面是否已完全加载。
- **身份验证错误**：在 `https://www.kimi.com/code/console` 重新登录。
- 该浏览器工具会使用您现有的 Chrome 会话。

## 输出格式

- **人类可读格式（默认）**：适合直接查看。
- **JSON 格式（使用 `--json` 标志）**：适用于脚本处理。

## 许可证

MIT 许可证——您可以自由修改和分发此代码。