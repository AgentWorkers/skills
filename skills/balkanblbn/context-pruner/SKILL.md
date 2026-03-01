---
name: context-pruner
description: 通过汇总和删除冗余的历史记录来智能管理上下文窗口。这有助于代理在长时间运行的线程中保持高性能。
---
# **上下文精简器（Context Pruner）**

该工具用于保存关键信息，帮助用户保持专注。它能够有效处理长时间对话中产生的冗余内容。

## **精简机制：**

1. **噪声检测（Noise Detection）**：过滤掉无关的“确认”信息以及填充性词汇。
2. **事实提取（Fact Distillation）**：提取对话中的核心事实，剔除冗余的对话内容。
3. **分段处理（Chunking）**：将长篇对话记录分割成易于搜索的摘要。

## **安装说明：**
```bash
clawhub install context-pruner
```