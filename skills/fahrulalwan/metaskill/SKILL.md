---
name: metaskill
description: "该工具通过实施深度纠错（deep correction）、迁移学习（transfer learning）和主动模式识别（proactive pattern recognition）机制，教导人工智能代理如何更有效地学习。适用于以下场景：  
- 当出现错误且需要深入分析时（而非仅仅进行表面性的修复）；  
- 在开始执行复杂任务之前，用于查找过去的类似案例或经验；  
- 在任务成功后，用于总结并记录成功的操作模式或策略。  
**不适用于常规的文件读取操作或简单的、一次性执行的命令。**"
---# Metaskill

## 三个核心组件

1. **深度自我纠正功能 (`deep-correct.sh`)** — 对错误进行三级分析：
   - **表面层**：具体发生了什么错误；
   - **原理层**：违反了哪些基本规则或约束；
   - **行为层**：为防止错误再次发生，需要采取哪些具体措施。

2. **迁移学习功能 (`transfer-check.sh`)** — 在执行任务之前，会搜索之前的学习记录中是否存在类似的模式。该功能能够跨不同领域（例如，“认证”领域与“安全”领域）进行知识迁移，避免知识孤岛现象。

3. **主动模式识别功能 (`success-capture.sh`)** — 记录哪些方法有效以及为什么有效，并建立一个成功案例的数据库。

## 使用方法

```bash
# When an error occurs
bash skills/metaskill/scripts/deep-correct.sh "description of the error"

# Before starting a complex task
bash skills/metaskill/scripts/transfer-check.sh "description of the new task"

# After successful execution
bash skills/metaskill/scripts/success-capture.sh "what worked" "why it worked"

# Monthly health eval
bash skills/metaskill/scripts/eval.sh --save
```

## 配置（大语言模型提供者）

Metaskill 支持两种提供者类型：**fast**（主要用于数据提取）和 **deep**（主要用于知识迁移和评估）。请编辑 `config.yaml` 文件以匹配您的配置：

```yaml
# config.yaml
providers:
  fast: anthropic   # change to: openai | ollama | gemini
  deep: anthropic
```

| 提供者 | 环境变量 | 备注 |
|---|---|---|
| `anthropic` | `ANTHROPIC_API_KEY` | 默认值 |
| `openai` | `OPENAI_API_KEY` | |
| `ollama` | *无需设置* | 本地免费服务 |
| `gemini` | `GOOGLE_API_KEY` | |

**Ollama 示例**（完全本地运行，无需 API 密钥）：
```yaml
providers:
  fast: ollama
  deep: ollama
models:
  ollama:
    fast: llama3.2
    deep: llama3.1:70b
```

如果无法使用任何提供者，Metaskill 会切换到手动/启发式模式（虽然功能仍然可用，但提取数据的准确性会降低）。

## 与自我提升代理的集成

如果系统中存在 `skills/self-improving-agent` 目录，Metaskill 会将该目录下的数据写入其中；否则，它会使用自身的 `.learnings/` 目录。无需额外配置。

## 必须执行的操作（在任务执行前）

请在任务执行前添加以下操作：
1. 运行 `transfer-check.sh`；
2. 在遇到任何错误后立即运行 `deep-correct.sh`（而不仅仅是将错误信息追加到 `LEARNINGS.md` 文件中）；
3. 在复杂任务成功完成后运行 `success-capture.sh`。