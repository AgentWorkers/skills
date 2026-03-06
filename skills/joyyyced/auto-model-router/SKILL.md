---
name: auto-model-router
description: 根据任务类型，自动选择并使用最适合的 AI 模型来完成任务。在新任务开始时或用户提出具体问题时，务必激活此功能。将编程任务分配给专门处理编程的模型，数学任务分配给推理模型，翻译任务分配给多语言处理模型，闲聊任务分配给响应快速且成本较低的模型等。随着时间的推移，系统会通过用户的反馈不断优化任务分配策略。触发短语包括：“help me”（帮助我）、”write”（编写）、”code”（编码）、”debug”（调试）、”translate”（翻译）、”analyze”（分析）、”summarize”（总结）、”explain”（解释）或任何与任务相关的请求。
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    user-invocable: true
    emoji: "🧠"
    homepage: https://github.com/JoyyyceD/auto-model-router
---
# 自动模型路由器技能

您可以使用智能模型来路由任务。对于每一个具体的任务，请按照以下步骤操作。

## 任务分类

将任务分为以下类别之一：

| 类别 | 使用场景 |
|----------|-------------|
| `coding` | 编写代码、调试、实现功能、架构设计 |
| `code_review` | 审查现有代码、安全/性能分析 |
| `math_reasoning` | 数学问题、逻辑谜题、定量分析 |
| `writing_long` | 文章、报告、论文、长篇文档 |
| `writing_short` | 标题、口号、社交媒体帖子、简短文案 |
| `translation` | 语言翻译 |
| `summarization` | 摘要长文本、会议记录 |
| `data_analysis` | 数据分析、编写SQL语句、解读图表 |
| `image_understanding` | 分析或描述图像 |
| `daily_chat` | 随机问答、简单问题、一般性协助 |

## 操作流程

首先检查 `AUTO_MODEL_ROUTER_URL` 是否已设置，以确定使用哪种模式。

---

### 模式 A — 本地模式（默认模式，无需路由器）

当 `AUTO_MODEL_ROUTER_URL` 未设置时，使用此模式。

**步骤 1 — 自行分类任务**

阅读用户的任务，并从上述类别中选择最合适的类别。
做出决策——选择一个类别。

**步骤 2 — 调用模型**

```
python3 ~/.claude/skills/auto-model-router/scripts/call_model.py "<category>" "<user task text>"
```

退出代码：
- `3` — API 密钥缺失：告知用户需要设置哪个环境变量
- `4` — 配置文件未找到：告知用户运行 `python3 scripts/setup.py`
- `5` — 完全没有配置路由规则：告知用户运行 `python3 scripts/setup.py`

**步骤 3 — 显示结果**

自然地展示模型输出，并添加以下提示：
`_[auto-model-router: 使用了 {category} → {model}]_`

---

### 模式 B — 带有学习功能的路由器模式**

当 `AUTO_MODEL_ROUTER_URL` 已设置时，使用此模式。

**步骤 1 — 获取推荐**

```
python3 ~/.claude/skills/auto-model-router/scripts/recommend.py "<user task text>" "<USER_ID>"
```

- 将模型的标准输出（stdout）捕获为结果。
- 从标准错误输出（stderr）中提取 `TASK_ID`（以 `TASK_ID=` 开头的行）。

退出代码：
- `2` — 路由器离线：自动切换回模式 A
- `3` — API 密钥缺失：告知用户需要设置哪个环境变量

**步骤 2 — 显示结果**

与模式 A 的步骤 3 相同。

**步骤 3 — 收集反馈**

在展示结果后询问用户：
> “这个回答有帮助吗？请回复 👍、👎 或者跳过。”

如果用户回复 👍：
```
python3 ~/.claude/skills/auto-model-router/scripts/feedback.py "<TASK_ID>" 1 "<USER_ID>"
```

如果用户回复 👎：
```
python3 ~/.claude/skills/auto-model-router/scripts/feedback.py "<TASK_ID>" -1 "<USER_ID>"
```

如果用户选择跳过，则无需执行任何操作。

---

## 更改模型分配

当用户请求更换模型（例如：“将翻译任务切换到 GPT-4o”或“使用 DeepSeek 进行编码”）时：

```
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py <category> <provider> <model>
```

示例：
```
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py translation openai gpt-4o
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py coding deepseek deepseek-chat
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py daily_chat google gemini-2.0-flash
```

向用户确认：“已更改，未来的 {category} 任务将使用 {model} 进行处理。”

## 首次设置

如果配置文件缺失，告知用户运行以下命令：
```
python3 ~/.claude/skills/auto-model-router/scripts/setup.py
```

## 手动调用

`/auto-model-router <你的任务>`