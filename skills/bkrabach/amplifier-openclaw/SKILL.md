---
name: amplifier-openclaw
description: "将复杂的任务委托给 Amplifier 的多代理框架。适用场景包括：(1) 需要从多个角度进行研究或比较的情况；(2) 涉及多个文件的代码项目；(3) 架构/设计评审；(4) 用户需要深入、细致的工作成果。不适用场景包括：简单的问答、快速编辑、非正式的聊天，以及任何需要少于 5 秒响应的任务。命令行工具：amplifier-openclaw。"
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
              "package": "amplifier-app-openclaw @ git+https://github.com/microsoft/amplifier-app-openclaw@main",
              "bins": ["amplifier-openclaw"],
              "label": "Install Amplifier OpenClaw integration (uv)",
            },
          ],
      },
  }
---
# 放大器（Amplifier）——多智能体任务委托系统

Amplifier 是一个基于多智能体的人工智能框架，适用于需要利用专业智能体、结构化工作流程或并行处理来完成任务的情况。

## 何时进行任务委托

**信心较高时 → 立即委托：**
- “研究 X 并比较不同的方法”
- “开发一个用于执行 X 功能的 Python 工具”
- “审查这段代码的安全性和设计”
- 用户请求“进行深入分析”或“全面检查”
- 任务包含可以由多个智能体并行处理的子任务

**信心中等时 → 提供选择：**
- “我可以快速分析，或者将任务委托给 Amplifier 进行多智能体协同处理。”

**信心较低时 → 自己处理：**
- 简单的问答、快速的代码修改、非正式的对话，以及任何需要立即响应的任务

## 使用方法

### 基本任务委托

```bash
exec command:"amplifier-openclaw run 'Research the top 3 Python web frameworks' --bundle foundation" background:true timeout:600
```

### 配合模型选择使用

通过传递 `--model` 参数来指定使用的特定大型语言模型（LLM）。Amplifier 会自动选择最适合的智能体提供者：

```bash
# Anthropic — full thinking, caching, tool repair
exec command:"amplifier-openclaw run --model anthropic/claude-sonnet-4-20250514 'Deep code review' --bundle foundation" background:true timeout:600

# Gemini — fast, large context
exec command:"amplifier-openclaw run --model gemini/gemini-2.5-flash 'Quick analysis' --bundle foundation" background:true timeout:300

# Any model OpenClaw has configured works automatically
exec command:"amplifier-openclaw run --model xai/grok-3 'Research task'" background:true timeout:600
```

**重要提示：** 必须传递与当前 OpenClaw 模型匹配的 `--model` 参数（例如，从系统提示中获取的模型名称，如 `model=anthropic/claude-opus-4-6`）。这样能确保 Amplifier 使用正确的提供者，并避免需要额外的 API 密钥。

### 智能体提供者路由

`--model` 参数会自动将任务路由到最合适的智能体提供者：

| 模型            | 提供者                | 功能                          |
|------------------|------------------|-----------------------------|
| `anthropic/claude-*`     | provider-anthropic       | 支持思考、缓存功能，支持处理大量上下文数据，具备工具修复能力 |
| `openai/gpt-4o*`, `openai/o3*` | provider-openai        | 提供 API 响应和推理服务                |
| 其他所有模型        | provider-litellm         | 通过环境变量接入 100 多个智能体提供者           |

无需额外配置 API 密钥——Amplifier 会继承 OpenClaw 配置的所有功能。

### 功能包

```bash
amplifier-openclaw bundles list
```

| 功能包            | 适用场景                        |
|------------------|-----------------------------|
| `foundation`       | 通用任务：研究、分析、规划（默认配置）         |
| `superpowers`       | 多智能体协同 brainstorm、深入调查           |
| `coder`          | 代码生成、重构、调试                     |

### 会话持久化

```bash
# Start a named session
exec command:"amplifier-openclaw run --session-name my-project 'Start building the auth module' --bundle foundation" background:true

# Resume later
exec command:"amplifier-openclaw run --resume --session-name my-project 'Now add unit tests'" background:true
```

### 模式设置

Amplifier 支持在命令中使用斜杠（/）来指定运行模式。**注意：运行模式不会在多次调用之间保持一致**——每次使用命令时都需要重新指定模式：

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

**仅在工作请求或成本超过一定阈值（>1）时才会显示成本信息。**

## 结果解读

- **`response`**：向用户展示最终处理结果
- **`error`**：以易于理解的方式报告错误信息（避免直接输出原始 JSON 数据）
- **`usage.estimated_cost`**：可能为 0.0——无需对零成本情况感到担忧
- **`status`**：表示任务状态（已完成、已取消或出现错误）

## 在任务执行过程中

- 如果需要停止或取消任务：**使用 “stop”/“cancel” 命令终止后台进程**
- 对于与当前任务无关的问题，请自行回答，不要干扰智能体的工作
- 对于后续处理：**告知用户任务完成后会将其转交给相应的智能体处理**

## 安装方法

如果尚未安装 Amplifier：

```bash
curl -fsSL https://raw.githubusercontent.com/microsoft/amplifier-app-openclaw/main/install.sh | bash
```

或者手动安装：

```bash
uv tool install "amplifier-app-openclaw @ git+https://github.com/microsoft/amplifier-app-openclaw@main"
```