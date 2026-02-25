---
name: amplifier-openclaw
description: "将复杂的任务委托给 Amplifier 的多代理框架。适用场景包括：(1) 需要从多个角度进行研究或比较的情况；(2) 涉及多个文件的代码项目；(3) 架构或设计评审；(4) 用户需要深入、细致的工作成果。不适用场景包括：简单的问答、快速编辑、闲聊，以及任何需要少于 5 秒响应的任务。命令行工具：amplifier-openclaw。"
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
              "package": "amplifier-app-openclaw @ git+https://github.com/microsoft/amplifier-app-openclaw@v1.0.5",
              "bins": ["amplifier-openclaw"],
              "label": "Install Amplifier OpenClaw integration (uv)",
            },
          ],
      },
  }
---
# Amplifier — 多智能体任务委托系统

Amplifier 是一个基于多智能体的 AI 框架，适用于需要利用专业智能体、结构化工作流程或并行处理来完成任务的情况。

## 何时进行任务委托

- **信心较高时 → 立即委托**：
  - “研究 X 并比较不同的方法”
  - “开发一个用于执行 X 功能的 Python 工具”
  - “审查这段代码的安全性和设计”
  - 用户要求进行“深入分析”或“全面检查”
  - 任务包含可以由多个智能体并行处理的子任务

- **信心中等时 → 提供选择**：
  - “我可以快速分析，或者将任务委托给 Amplifier 进行多智能体协同审查。”

- **信心较低时 → 自己处理**：
  - 简单的问答、快速的代码修改、非正式的对话，以及需要立即响应的任务

## 使用方法

### 基本任务委托

```bash
exec command:"amplifier-openclaw run 'Research the top 3 Python web frameworks' --bundle foundation" background:true timeout:600
```

### 选择模型

通过传递 `--model` 参数来指定使用的模型（默认模型为系统默认值）：

```bash
exec command:"amplifier-openclaw run --model your-preferred-model 'Deep code review' --bundle foundation" background:true timeout:600
```

**提示：** 请确保指定的模型与 OpenClaw 运行时环境中使用的模型一致，以确保 Amplifier 能正确使用该模型。

### 模块组合

```bash
amplifier-openclaw bundles list
```

| 模块名称 | 适用场景 |
|---------|---------|
| `foundation` | 常规任务：研究、分析、规划（默认配置） |
| `superpowers` | 多智能体协同讨论、深入调查 |
| `coder` | 代码生成、重构、调试 |

### 会话持久化

```bash
# Start a named session
exec command:"amplifier-openclaw run --session-name my-project 'Start building the auth module' --bundle foundation" background:true

# Resume later
exec command:"amplifier-openclaw run --resume --session-name my-project 'Now add unit tests'" background:true
```

### 模式设置

Amplifier 支持在命令提示中设置运行模式。**不同运行之间的模式设置不会保留**——每次运行时都需要重新指定模式：

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

仅在工作被请求或成本超过一定阈值（>1）时才会显示成本信息。

## 结果解读

- **`response`**：向用户展示最终处理结果
- **`error`**：以通俗易懂的方式报告错误信息，避免直接输出原始 JSON 数据
- **`usage.estimated_cost`**：可能为 0.0——无需对零成本产生疑虑
- **`status`**：表示任务状态（已完成、已取消或出现错误）

## 在任务执行过程中

- 如果需要停止或取消任务，请使用 “stop”/“cancel” 命令终止后台进程
- 对于与当前任务无关的问题，请自行回答，不要打扰 Amplifier 的运行
- 可以告知用户：当前任务完成后会将其结果转交给相关智能体处理

## 安装方法

如果尚未安装 Amplifier，请按照以下步骤进行安装：

```bash
uv tool install "amplifier-app-openclaw @ git+https://github.com/microsoft/amplifier-app-openclaw@v1.0.5"
```