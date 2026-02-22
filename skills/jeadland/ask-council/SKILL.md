---
name: ask-council
version: 1.0.3
description: 您可以直接通过 Telegram/聊天窗口向 LLM Council 提出问题，无需打开网页界面即可获得主席的合成回答。这是一种快速、无界面的方式，用于访问多模型共识系统。
slash_command: /council
metadata: {"category":"productivity","tags":["llm","council","quick","telegram","cli"],"repo":"https://github.com/jeadland/llm-council"}
---
# 询问委员会 — 快速无头访问（Quick Headless Access）

无需离开聊天窗口，即可获取 LLM 委员会的合成答案。

## 使用方法

```
/council Should I invest in Tesla right now?
```

在所有模型完成讨论后，该功能会返回 **主席的合成答案**。

## 工作原理

1. 将您的问题发送到 LLM 委员会后端。
2. 等待第一阶段（所有模型作出响应）。
3. 等待第二阶段（模型之间相互评分）。
4. 返回第三阶段（主席的最终合成结果）。

**耗时 30-60 秒** — 模型需要时间进行讨论。

## 先决条件

LLM 委员会后端必须处于运行状态：
```
/install-llm-council
```

## 使用 LLM 委员会的两种方式

| 使用方式 | 适用场景 | 命令 |
|------|----------|---------|
| **快速回答**（此功能） | 快速决策、移动设备、非正式问题 | `/council "问题"` |
| **全面讨论**（Web 界面） | 深入研究、探讨分歧、查看所有模型的回答 | `/install-llm-council`，然后打开浏览器 |

## 示例

**输入：**
```
/council Is Python or Go better for a new microservice?
```

**输出：**
```
Council is deliberating... (this may take 30-60s)
................

═══════════════════════════════════════════════════════════════
                    CHAIRMAN'S ANSWER
═══════════════════════════════════════════════════════════════

Based on the council's deliberation, Python is recommended for rapid 
prototyping and team velocity, while Go excels for high-throughput 
services where performance is critical...

═══════════════════════════════════════════════════════════════

View full discussion: http://10.0.1.184:5173
```

## 代理脚本说明

当用户输入 `/council <问题>` 或 “询问委员会” 时，脚本会执行以下操作：

```bash
bash ~/.openclaw/skills/ask-council/ask-council.sh "<question>"
```

- 创建新的对话窗口。
- 启动委员会讨论流程。
- 持续轮询讨论进度，直到讨论完成。
- 提取主席的最终答案。
- 在等待过程中显示进度条。

## 相关文件

| 文件名 | 用途 |
|------|---------|
| `SKILL.md` | 文档说明 |
| `ask-council.sh` | 主脚本 — 调用 API 并返回答案 |
| `_meta.json` | 技能元数据 |

## 注意事项

- 超时时间：120 秒。
- 如果后端未运行，系统会提示用户启动后端。
- 系统会始终提供完整的 Web 界面链接以供用户详细查看讨论内容。
- 每次使用都会创建新的对话记录（无对话历史记录）。