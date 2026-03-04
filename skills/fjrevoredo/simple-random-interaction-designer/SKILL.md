---
name: simple-random-interaction-designer
description: 决定是否在定期检查期间由 OpenClaw 自动发送一条非正式的聊天消息；如果决定发送，需选择一种自然的互动方式，并提供简洁的指导来说明如何发送该消息。此功能适用于安排或执行类似人类的主动聊天检查（proactive chat checks）。
metadata: {"homepage":"https://docs.openclaw.ai/tools/skills","env":[],"network":"optional","version":"2.0.0","notes":"Uses local randomness to return only a final yes/no decision and, on yes, an interaction type plus interaction description for natural outreach, including grounded OpenClaw-accessible real-world context when relevant"}
---
# 简单随机交互设计器

使用此技能来决定是否发送一条随意的主动消息，如果决定是“是”，则确定要发送哪种类型的交互信息。
默认的执行路径为 `{baseDir}/scripts/random_interaction_designer.py`。

## 工作流程
1. 每个预定检查间隔运行一次脚本。
2. 从 JSON 输出中读取 `decision` 的值。
3. 如果 `decision` 的值为 `no`，则立即停止执行。
4. 如果 `decision` 的值为 `yes`，则使用 `interaction_type` 和 `interaction_description` 来起草发送的消息。
5. 如果选定的交互类型需要获取数据，可以使用 OpenClaw 提供的相关工具、技能或集成来获取实时上下文信息，然后再起草消息。
6. 保持最终消息简短、随意，且不会给用户带来社交压力。
7. 当聊天记录中存在相关内容时，优先使用这些信息。
8. 不要提及随机选择的过程、预定的检查间隔，或选择该交互的原因。

## 主要工具
- 脚本路径：`{baseDir}/scripts/random_interaction_designer.py`
- 运行环境：Python 3，仅使用标准库。

推荐命令：
`python3 {baseDir}/scripts/random_interaction_designer.py`

## 输出格式
当结果为 `no` 时：

```json
{"decision":"no"}
```

当结果为 `yes` 时：

```json
{
  "decision": "yes",
  "interaction_type": "Playful opener",
  "interaction_description": "Send a brief playful line that feels spontaneous and easy to ignore."
}
```

**格式规范**：
- `decision` 总是存在的，其值为 `yes` 或 `no`。
- 当 `decision` 的值为 `yes` 时，`interaction_type` 才会存在。
- 当 `decision` 的值为 `yes` 时，`interaction_description` 才会存在。
- 不需要包含调试字段、概率值、随机生成的数值或备用元数据。

## 交互设计规则
- 将 JSON 数据视为执行指南，而非直接展示给用户的文本。
- 最终消息应控制在一两行简短的聊天内容内。
- 采用非正式的表述方式，避免使用过于正式或类似助手的语气。
- 单次交互中最多提出一个问题。
- 不要伪造聊天记录中的内容、外部事实或基于账户的数据。
- 对于需要获取数据的交互类型，只有在 OpenClaw 能够访问到相关数据源的情况下，才使用真实世界的信息。
- 仅在使用可靠、最新且与用户相关的数据时，才提供智能家居、天气、日历、交通、新闻或市场等相关信息。
- 如果 `interaction_type` 需要根据上下文或实时数据来决定，且无法获取这些数据，则重新运行脚本以尝试非数据相关的交互；如果重新运行不切实际，应发送一条通用且不具压力的消息。
- 尽可能使消息的语气和措辞与之前的交互有所不同，以体现随意性，避免显得机械或模式化。

## 交互类型目录
根据选定的 `interaction_type`，按照 `interaction_description` 中的指导来执行相应的交互：
1. **轻松的开场白**：以一句轻松、自然的开场白开始对话。
2. **好奇的问候**：提出一个简单易答的问题。
3. **随意的分享观察**：发表一个类似闲聊的观察结果。
4. **简单的庆祝**：在聊天中适当的时候，简要表扬用户的成就或努力。
5. **智能设备状态**：如果 OpenClaw 可以获取设备状态信息，自然地分享相关信息或提供建议。
6. **基于天气的问候**：仅在有最新、可靠且相关的天气数据时使用天气信息。
7. **基于日历的提醒**：将日历信息转化为人性化的语气提醒或提示，而非警报。
8. **基于上下文的跟进**：仅在当前聊天中存在相关内容时，基于之前的对话细节进行跟进。
9. **实用的提示**：提供一条简洁的、可选的实用建议。
10. **可选的现实世界更新**：仅在有可靠、相关的数据时，分享交通、新闻或市场等现实世界的信息。

## 错误处理
- 如果脚本执行失败，显示 Python 的错误信息并重新运行。
- 如果输出内容不是有效的 JSON 格式，视为失败并重新运行。
- 如果 `decision` 缺失，或者 `decision` 的值不是 `yes` 或 `no`，则重新运行并忽略无效的结果。
- 如果 `decision` 的值为 `yes`，但 `interaction_type` 或 `interaction_description` 缺失，也重新运行并忽略无效的结果。

## 最小示例

```bash
python3 {baseDir}/scripts/random_interaction_designer.py
python3 {baseDir}/scripts/random_interaction_designer.py --seed 42
```

```powershell
python3 "{baseDir}/scripts/random_interaction_designer.py"
python3 "{baseDir}/scripts/random_interaction_designer.py" --seed 42
```