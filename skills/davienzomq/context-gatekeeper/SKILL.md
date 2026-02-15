---
name: context-gatekeeper
description: 该技能通过总结最近的对话内容、列出待处理的操作，并在每次调用模型之前提供简洁的概述，来确保对话的流畅性和条理性。无论何时你需要精简冗长的讨论内容或使下一个提示更加简洁明了，都可以使用该技能。
author: Davi Marques
---

# Context Gatekeeper

## 目的
减少发送到模型的令牌数量，仅保留最重要的信息：决策摘要、下一步行动以及对话的最新内容。该工具会与您的常规流程并行运行，生成一个名为 `context/current-summary.md` 的文件作为上下文替代品（而不是重新发送整个对话内容）。

## 最小工作流程
1. **记录对话内容**：每当收到提示或回复时，将格式为 `ROLE: 文本` 的行记录到历史记录文件（`context/history.txt` 或任何可访问的路径）中。示例：
   ```
   USER: Quero definir metas para o Q2
   ASSISTANT: Fiz um plano com marcos e métricas
   ```
2. **运行 Context Gatekeeper**：
   ```bash
   python skills/context-gatekeeper/scripts/context_gatekeeper.py \
     --history context/history.txt \
     --summary context/current-summary.md
   ```
   该脚本会限制摘要的长度（默认为 6 句），提取未完成的任务（TODO、下一步行动、待办事项）以及最近的 4 条对话记录以供即时参考。
3. **使用摘要**：在调用 API 或回复用户之前，先插入 `context/current-summary.md` 的内容，并提及未完成的事项。只有在必要时，才添加最新的对话记录（最多 2-3 条消息）以增强信息的清晰度。
4. **重复执行**：用新的回复更新 `context/history.txt`，并在下一次轮次之前再次运行脚本。

## 脚本的参数
- `--history`：对话记录文件的路径（每行格式应为 `ROLE: 文本`）。如果省略此参数，则使用标准输入（STDIN）。
- `--summary`：摘要文件的保存路径（如果文件已存在，则会覆盖该文件）。
- `--max-summary-sents`：摘要的最大句子数（默认为 6 句）。
- `--max-recent-turns`：显示在“最近轮次”部分中的最后几条对话记录的数量（默认为 4 条）。

## 日常使用建议
- 设置一个定时任务/循环，在每次自动回复之前运行该脚本。
- 创建一个名为 `context/pending-tasks.md` 的文件，并将摘要中的“待办事项”部分复制到其中。
- 在回复的开头始终提及摘要文件的路径（例如：“摘要内容：...”），以便于审计。

## 这个工具为何有效？
OpenClaw 已经会将对话记录保存在 Markdown 文件中，并在需要时执行 `/compact` 命令进行压缩。这个工具遵循相同的策略：它不会依赖那些仍然存在于上下文中的 100 多条旧消息，而是在每次调用之前提供一页简短的摘要。这样可以节省令牌，并确保模型专注于真正重要的信息（决策、待办事项、最新变化）。