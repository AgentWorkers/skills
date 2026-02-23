---
name: context-engineer
version: 1.0.0
description: 上下文窗口优化器（Context Window Optimizer）——用于分析、审计并优化您的代理程序（agent）对上下文数据的利用情况。在令牌（tokens）被发送之前，您可以准确了解它们的去向。
author: Anvil AI
license: MIT
homepage: https://github.com/cacheforge-ai/cacheforge-skills
user-invocable: true
tags:
  - cacheforge
  - context-engineering
  - token-optimization
  - llm
  - ai-agents
  - prompt-optimization
  - observability
  - discord
  - discord-v2
metadata: {"openclaw":{"emoji":"🔬","homepage":"https://github.com/cacheforge-ai/cacheforge-skills","requires":{"bins":["python3"]}}}
---
## 何时使用此技能

当用户希望执行以下操作时，请使用此技能：
- 了解其上下文窗口中的令牌（tokens）的去向；
- 分析工作区文件（如 SKILL.md、SOUL.md、MEMORY.md 等）是否存在冗余或臃肿的问题；
- 审查工具定义，检查其中是否存在冗余和额外的开销；
- 获取全面的上下文效率报告；
- 比较分析前后的数据，以衡量优化效果；
- 优化系统提示，以提高令牌的使用效率。

## 命令

```bash
# Analyze workspace context files — token counts, efficiency scores, recommendations
python3 skills/context-engineer/context.py analyze --workspace ~/.openclaw/workspace

# Analyze with a custom budget and save a snapshot for later comparison
python3 skills/context-engineer/context.py analyze --workspace ~/.openclaw/workspace --budget 128000 --snapshot before.json

# Audit tool definitions for overhead and overlap
python3 skills/context-engineer/context.py audit-tools --config ~/.openclaw/openclaw.json

# Generate a comprehensive context engineering report
python3 skills/context-engineer/context.py report --workspace ~/.openclaw/workspace --format terminal

# Compare two snapshots to see projected token savings
python3 skills/context-engineer/context.py compare --before before.json --after after.json
```

## 分析内容

- **系统提示效率**：分析系统提示的长度、是否存在冗余以及压缩的潜力；
- **工具定义的开销**：统计工具的数量、每个工具所消耗的令牌数量，并识别未使用或重复的工具；
- **内存文件冗余**：检查 MEMORY.md 文件的大小、过时的条目以及提供优化建议；
- **技能使用开销**：分析已安装的技能对上下文的影响，以及每个技能所消耗的令牌数量；
- **上下文预算**：计算模型上下文窗口中被静态内容占用的比例，以及可用于对话的部分。

## 选项

- `--workspace PATH`：工作区目录的路径（默认值：`~/.openclaw/workspace`）；
- `--config PATH`：OpenClaw 配置文件的路径（默认值：`~/.openclaw/openclaw.json`）；
- `--budget N`：上下文窗口令牌的预算（默认值：200000）；
- `--snapshot FILE`：将分析结果保存到指定文件中，以便后续比较；
- `--format terminal`：输出格式（当前格式：终端输出）。

## 注意事项

- 令牌数量的估计值仅供参考（大约每个令牌占用 4 个字符）。如需精确计数，请使用特定于模型的分词器（tokenizer）。
- 无需任何外部依赖项，仅使用 Python 3 的标准库即可运行；
- 该工具由 Anvil AI 开发，团队成员为上下文工程领域的专家。更多信息请访问：https://anvil-ai.io