---
name: amplifier-openclaw
description: "将复杂任务委托给 Amplifier 的多代理框架。适用场景包括：(1) 需要从多个角度进行研究的任务；(2) 涉及多个文件的代码项目；(3) 架构或设计评审；(4) 用户需要深入、细致的工作成果。不适用于：简单的问答、快速编辑、日常聊天，以及任何需要不到 5 秒响应的任务。命令行工具：amplifier-openclaw。"
metadata:
  {
    "openclaw":
      {
        "emoji": "⚡",
        "requires": { "bins": ["amplifier-openclaw"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "uv",
              "package": "amplifier-app-openclaw @ git+https://github.com/microsoft/amplifier-app-openclaw@v1.0.4",
              "bins": ["amplifier-openclaw"],
              "label": "Install Amplifier OpenClaw integration (uv)",
            },
          ],
      },
  }
---
# Amplifier — 多智能体任务委托系统

Amplifier 是一个基于多智能体的人工智能框架，适用于需要利用专业智能体、结构化工作流程或并行处理来完成任务的情况。

## 何时进行任务委托

- **信心较高时 → 立即委托**：
  - “研究 X 并比较不同的方法”
  - “开发一个用于执行 X 功能的 Python 工具”
  - “检查这段代码的安全性和设计问题”
  - 用户要求进行“深入分析”或“全面审查”
  - 任务包含可以通过多个智能体并行处理的子任务

- **信心中等时 → 提供选择**：
  - “我可以快速分析，或者将任务委托给 Amplifier 进行全面的多智能体审查。”

- **信心较低时 → 自己处理**：
  - 简单的问答、快速的代码修改、非正式的对话，以及任何需要立即响应的任务

## 使用方法

### 基本任务委托

```bash
exec command:"amplifier-openclaw run 'Research the top 3 Python web frameworks' --bundle foundation" background:true timeout:600
```

### 使用特定模型

通过传递 `--model` 参数来指定使用的 LLM（大型语言模型）。Amplifier 会自动选择最适合的智能体提供者：

```bash
# Anthropic — full thinking, caching, tool repair
exec command:"amplifier-openclaw run --model anthropic/claude-sonnet-4-20250514 'Deep code review' --bundle foundation" background:true timeout:600

# Gemini — fast, large context
exec command:"amplifier-openclaw run --model gemini/gemini-2.5-flash 'Quick analysis' --bundle foundation" background:true timeout:300

# Any model works
exec command:"amplifier-openclaw run --model xai/grok-3 'Research task'" background:true timeout:600
```

**提示：** 如果 OpenClaw 使用了特定的模型，请通过 `--model` 参数传递该模型名称，以确保 Amplifier 使用相同的模型。

### 模型支持

`--model` 参数支持任何模型标识符（例如 `anthropic/claude-sonnet-4-20250514`、`openai/gpt-4o`、`gemini/gemini-2.5-flash`）。Amplifier 会自动将任务路由到相应的智能体提供者。

### 模块组合

```bash
amplifier-openclaw bundles list
```

| 模块组合 | 适用场景 |
|--------|----------|
| `foundation` | 通用任务：研究、分析、规划（默认配置） |
| `superpowers` | 多智能体头脑风暴、深入调查 |
| `coder` | 代码生成、重构、调试 |

### 会话持久化

```bash
# Start a named session
exec command:"amplifier-openclaw run --session-name my-project 'Start building the auth module' --bundle foundation" background:true

# Resume later
exec command:"amplifier-openclaw run --resume --session-name my-project 'Now add unit tests'" background:true
```

### 模式设置

Amplifier 支持在提示中设置特定的工作模式。**模式在多次运行之间不会保留**——每次使用都需要重新指定模式：

```bash
# Brainstorm mode (uses all agents)
exec command:"amplifier-openclaw run --bundle superpowers '/brainstorm How should we architect the new API?'" background:true

# Research mode
exec command:"amplifier-openclaw run --bundle foundation '/research Latest advances in RAG'" background:true
```

## JSON 输出格式

```json
{
  "response": "The analysis found...",
  "usage": {
    "input_tokens": 28566,
    "output_tokens": 1800,
    "estimated_cost": 0.12,
    "tool_invocations": 3
  },
  "status": "completed"
}
```

## 成本跟踪

仅在被请求或成本超过一定阈值（>1）时才会显示成本信息。

## 结果解读

- **`response`**：向用户展示最终结果
- **`error`**：以通俗易懂的方式报告错误信息，避免直接显示原始 JSON 数据
- **`usage.estimated_cost`**：可能为 0.0——无需对此感到担忧
- **`status`**：表示任务状态（已完成、已取消或出现错误）

## 在任务执行过程中

- **“停止”/“取消”**：终止后台任务进程
- **无关问题**：自行回答，不要打扰正在工作的智能体
- **后续处理**：告知用户任务完成后会将其结果转交给他们

## 安装方法

如果尚未安装 Amplifier，请按照以下步骤进行安装：

```bash
uv tool install "amplifier-app-openclaw @ git+https://github.com/microsoft/amplifier-app-openclaw@v1.0.4"
```