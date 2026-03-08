---
name: auto-model-router
description: 根据任务类型，自动选择并使用最适合的 AI 模型来完成任务。在新任务开始时，或当用户提出实质性问题时，务必激活此功能。将编码任务分配给专门处理编码的模型，数学问题分配给推理模型，翻译任务分配给多语言处理模型，闲聊任务分配给响应快速且成本低廉的模型等。随着时间的推移，该系统会通过用户的反馈不断进行优化。触发短语包括：“help me”（帮助我）、”write”（编写）、”code”（编码）、”debug”（调试）、”translate”（翻译）、”analyze”（分析）、”summarize”（总结）、”explain”（解释）或任何与任务相关的请求。
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      # Declare all credentials this skill may use.
      # Users only need to set the keys for providers they actually use.
      # AUTO_MODEL_ROUTER_URL is optional — only needed for router mode (Mode B).
      env:
        - name: ANTHROPIC_API_KEY
          description: "Anthropic API key (for Claude models)"
          required: false
        - name: OPENAI_API_KEY
          description: "OpenAI API key (for GPT models and embeddings)"
          required: false
        - name: DEEPSEEK_API_KEY
          description: "DeepSeek API key (for DeepSeek models)"
          required: false
        - name: MINIMAX_API_KEY
          description: "MiniMax API key (for MiniMax models)"
          required: false
        - name: GOOGLE_API_KEY
          description: "Google API key (for Gemini models)"
          required: false
        - name: AUTO_MODEL_ROUTER_URL
          description: "Optional: URL of a self-hosted router service for learning mode (Mode B). If not set, the skill runs fully locally (Mode A)."
          required: false
        - name: AUTO_MODEL_ROUTER_API_KEY
          description: "Optional: API key for the self-hosted router service"
          required: false
    user-invocable: true
    emoji: "🧠"
    homepage: https://github.com/JoyyyceD/auto-model-router
    privacy: >
      Mode A (default): all processing is local. Your task text is sent only to
      the AI provider you configured (e.g. Anthropic, OpenAI). No data is sent
      to any third party beyond your chosen provider.
      Mode B (router): only active when AUTO_MODEL_ROUTER_URL is explicitly set
      by the user. Task text and an anonymous session ID are sent to that
      self-hosted router for model selection and feedback learning. The router
      URL is always user-controlled — this skill ships with no default router.
---
# 自动模型路由器技能

该技能具备智能的模型路由功能。对于每一个具体的任务，请按照以下流程进行操作。

## 任务分类

将任务归类到以下类别中：

| 类别 | 使用场景 |
|----------|-------------|
| `coding` | 编写代码、调试、实现功能、架构设计 |
| `code_review` | 审查现有代码、安全/性能分析 |
| `math_reasoning` | 数学问题、逻辑谜题、定量分析 |
| `writing_long` | 文章、报告、论文、长篇文档 |
| `writing_short` | 标题、标语、社交媒体帖子、简短文案 |
| `translation` | 语言翻译 |
| `summarization` | 长文本摘要、会议记录 |
| `data_analysis` | 数据分析、编写SQL语句、解读图表 |
| `image_understanding` | 图像分析或描述 |
| `daily_chat` | 随机问答、简单问题、一般性协助 |

## 流程

首先检查 `AUTO_MODEL_ROUTER_URL` 是否已设置，以确定使用哪种模式。

---

### 模式 A — 本地模式（默认模式，无需使用路由器）

当 `AUTO_MODEL_ROUTER_URL` 未设置时，使用此模式。

**步骤 1 — 自行分类任务**

阅读用户的任务内容，并从上述类别中选择最合适的类别。

**步骤 2 — 调用模型**

```
python3 ~/.claude/skills/auto-model-router/scripts/call_model.py "<category>" "<user task text>"
```

退出代码：
- `3` — API 密钥缺失：告知用户需要设置哪个环境变量。
- `4` — 配置文件未找到：告知用户运行 `python3 scripts/setup.py`。
- `5` — 完全没有配置路由规则：告知用户运行 `python3 scripts/setup.py`。

**步骤 3 — 显示结果**

自然地展示模型返回的结果，并添加以下提示：
`_[自动模型路由器：使用了 {类别} → {模型}]_`

---

### 模式 B — 带有学习功能的路由器模式（需要设置 `AUTO_MODEL_ROUTER_URL`）

当 `AUTO_MODEL_ROUTER_URL` 已设置时，使用此模式。

> **隐私说明：** 任务内容及一个匿名会话 ID 会被发送到 `AUTO_MODEL_ROUTER_URL`。该 URL 由用户自行设置——该技能本身没有内置的远程接口。如果用户未明确设置此变量，请始终使用模式 A。

**步骤 1 — 获取推荐结果**

```
python3 ~/.claude/skills/auto-model-router/scripts/recommend.py "<user task text>" "<USER_ID>"
```

- 将模型的输出（stdout）捕获并保存。
- 从错误日志（stderr）中提取 `TASK_ID`（以 `TASK_ID=` 开头的行）。

退出代码：
- `2` — 路由器处于离线状态：自动切换回模式 A。
- `3` — API 密钥缺失：告知用户需要设置哪个环境变量。

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

## 更改模型使用

当用户要求切换模型（例如：“将翻译任务切换到 GPT-4o”或“使用 DeepSeek 进行编码”）时：

```
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py <category> <provider> <model>
```

示例：
```
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py translation openai gpt-4o
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py coding deepseek deepseek-chat
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py daily_chat google gemini-2.0-flash
```

向用户确认：“已更改，现在 {类别} 类型的任务将使用 {model} 进行处理。”

## 首次设置

如果配置文件缺失，告知用户运行以下命令：
```
python3 ~/.claude/skills/auto-model-router/scripts/setup.py
```

## 手动调用

`/auto-model-router <你的任务>`