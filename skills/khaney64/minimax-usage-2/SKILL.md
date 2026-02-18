---
name: minimax-usage
description: 检查 MiniMax 编码计划的使用情况以及剩余的信用额度。需要 MINIMAX_API_KEY 环境变量。
metadata: {"openclaw":{"emoji":"💳","requires":{"bins":["curl","jq"],"env":["MINIMAX_API_KEY"]}}}
---
# MiniMax 使用说明

请查看您的 MiniMax 编码计划剩余的信用额度。

## 使用方法

```bash
# Check remaining credits
minimax-usage.sh

# Only alert when remaining drops below 20%
minimax-usage.sh --threshold 20
```

## 选项

| 标志 | 描述 |
|------|-------------|
| `--threshold <百分比>` | 仅当剩余信用额度低于此值时才输出警告。如果省略，则始终输出警告。 |

## 输出结果

返回一条符合 Discord 格式的消息：
- **标题**：包含模型名称（当信用额度低于阈值时显示警告图标）
- **剩余请求数**：总请求数及其对应的百分比
- **重置时间**（以东部时间显示）
- **剩余时间**：以小时:分钟:秒的形式显示

### 示例：当剩余信用额度低于阈值时触发警告

当剩余信用额度低于配置的阈值时，系统会触发警告：

```
⚠️ MiniMax Usage Alert — MiniMax-M1
Remaining: 42 of 500 requests (8.4%)
Resets: Feb 17, 2026 12:00 AM ET
Time left: 7:23:15
```

当信用额度高于阈值时，该命令不会输出任何内容，并以代码 0 结束执行。

## Cron 作业

`--threshold` 标志使得该命令非常适合用于定期执行的 Cron 作业：只有当可用信用额度低于指定百分比时，才会发送警告：

```bash
# Check every 30 minutes, alert if below 20%
# Requires MINIMAX_API_KEY to be set in the cron environment
*/30 * * * * minimax-usage.sh --threshold 20 | discord-webhook
```

当信用额度高于阈值时，系统不会输出任何内容，因此下游命令（例如 Webhook）仅会在信用额度较低时被触发。