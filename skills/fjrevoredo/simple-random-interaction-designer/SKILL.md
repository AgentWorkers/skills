---
name: simple-random-interaction-designer
description: 决定是否在定期检查期间由 OpenClaw 向用户发送主动的 ping 请求；当需要发送 ping 请求时，选择一种随机的交互方式。此功能适用于安排或执行类似人类的主动检查行为。
metadata: {"homepage":"https://docs.openclaw.ai/tools/skills","env":[],"network":"optional","version":"1.0.0","notes":"Uses local randomness to decide interact/no-interact and select one interaction type from a fixed list"}
---
# 简单随机交互设计器

使用此技能在定期检查期间模拟自然、类似人类的交互行为。
默认执行路径为 `{baseDir}/scripts/random_interaction_designer.py`。

## 工作流程
1. 每个预定检查间隔运行一次脚本。
2. 从 JSON 输出中读取 `should_interact` 的值。
3. 如果 `should_interact` 的值为 `false`，则立即停止执行。
4. 如果 `should_interact` 的值为 `true`，则使用 `interaction_type` 生成相应的交互内容。
5. 对于依赖数据的交互类型，在起草消息之前，应使用所有可用的工具、技能或 MCP 集成来尽力获取所需数据。
6. 如果无法获取真实数据，将交互类型切换为 `Joke`，并发送一个不需要外部数据的简单交互内容。

## 主要工具
- 脚本路径：`{baseDir}/scripts/random_interaction_designer.py`
- 运行环境：Python 3，仅使用标准库。

推荐命令：
- `python {baseDir}/scripts/random_interaction_designer.py`

## 输出格式
- `should_interact`（`true` 或 `false`）
- `yes_probability_percent`（25 到 75 之间的整数）
- `roll_percent`（1 到 100 之间的整数）
- `interaction_type`（仅在 `should_interact` 为 `true` 时出现）

支持的交互类型：
1. `系统状态更新`
2. 天气更新
3. 基于用户性格的随机事实
4. 当前事件更新
5. 用户状态更新
6. 笑话
7. 日历提醒
8. 邮箱收件箱摘要
9. 交通或通勤情况更新
10. 金融或加密货币市场概览

## 真实数据政策
- 将 `系统状态更新`、`天气更新`、`当前事件更新`、`用户状态更新`、`日历提醒`、`邮箱收件箱摘要`、`交通或通勤情况更新` 和 `金融或加密货币市场概览` 视为依赖数据的类型。
- 尽力通过当前可用的工具和技能获取实时数据或账户支持的数据。
- 如果这些数据源不可用，不要编造外部信息。
- 如果数据获取失败、超时或未获授权，应切换到 `Joke` 类型的交互。

## 错误处理
- 如果执行失败，显示 Python 错误信息并重新运行脚本。
- 如果输出不是有效的 JSON 格式，视为严重错误并重新运行脚本。
- 如果在 `should_interact` 为 `true` 的情况下 `interaction_type` 缺失，重新运行脚本并忽略无效的结果。

## 最小示例

```bash
python {baseDir}/scripts/random_interaction_designer.py
python {baseDir}/scripts/random_interaction_designer.py --seed 42
```

```powershell
python "{baseDir}/scripts/random_interaction_designer.py"
python "{baseDir}/scripts/random_interaction_designer.py" --seed 42
```