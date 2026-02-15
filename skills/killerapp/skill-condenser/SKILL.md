---
name: skill-condenser
description: "使用“Chain-of-Density”方法对冗长的 SKILL.md 文件进行压缩，并采用能够体现技能特性的格式化方式。当某项技能的描述超过 200 行或需要精简重构时，建议采用此方法。"
license: Apache-2.0
metadata:
  author: agentic-insights
  version: "1.0"
---

# 技能精简工具

使用 CoD 工具对 SKILL.md 文件进行压缩，同时保留技能文档的格式结构。由于技能文档具有明确的结构（而非纯文本），因此只需进行 2-3 次压缩处理即可达到最佳效果（而非 5 次）。

## 使用场景

- 当 SKILL.md 文件超过 200 行时
- 当技能文档中包含大量纯文本段落而非项目符号列表时
- 当需要将冗长的文档重构为简洁的风格时

## 处理流程

1. 阅读技能文档内容，进行初步精简
2. 运行 `cod-iteration` 工具 2-3 次，确保每次处理时都考虑到技能文档的格式结构
3. 在每次迭代中：提取关键信息，并将其转换为项目符号列表或表格形式
4. 输出精简后的技能文档，同时保持原有的结构

## 详细步骤

### 第一次迭代：提取文档结构

将文档传递给 `cod-iteration` 工具进行处理：
```
iteration: 1
target_words: [current_words * 0.6]
format_context: |
  OUTPUT FORMAT: Agent Skills SKILL.md
  - Use ## headers for sections
  - Bullet lists, not prose paragraphs
  - Tables for comparisons/options
  - Code blocks for commands
  - No filler phrases ("this skill helps you...")

text: [FULL SKILL.MD CONTENT]
```

### 第二次迭代：优化内容结构

继续使用 `cod-iteration` 工具进行处理：
```
iteration: 2
target_words: [iteration_1_words]
format_context: |
  SKILL.md TERSE RULES:
  - Each bullet = one fact
  - Combine related bullets with semicolons
  - Remove redundant examples (keep 1 best)
  - Tables compress better than lists for options

text: [ITERATION 1 OUTPUT]
source: [ORIGINAL SKILL.MD]
```

### 第三次迭代（可选）：最终润色

仅当文档长度仍超过 150 行时进行：
```
iteration: 3
target_words: [iteration_2_words]
format_context: |
  FINAL PASS:
  - Move detailed content to references/ links
  - Keep only: Quick Start, Core Pattern, Troubleshooting
  - Each section <20 lines

text: [ITERATION 2 OUTPUT]
source: [ORIGINAL SKILL.MD]
```

## 预期输出格式

每次迭代后，输出如下格式的文档：
```
Missing_Entities: "entity1"; "entity2"; "entity3"

Denser_Summary:
---
name: skill-name
description: ...
---
# Skill Name
[Condensed content in proper SKILL.md format]
```

## 需要重点关注的文档元素

在精简技能文档时，请优先处理以下类型的元素：

| 元素类型 | 保留 | 删除 |
|-------------|------|--------|
| 命令 | `deploy.py --env prod` | 详细的操作说明 |
| 选项 | 以表格形式呈现 | 单个选项对应的完整描述 |
| 错误信息 | `Error → Fix` | 长篇的故障排除说明 |
| 示例 | 最佳示例 | 多个相似示例 |
| 先决条件 | 以项目符号列表形式呈现 | 对这些条件为何必要的解释 |

## 压缩目标

| 原始文件长度 | 目标文件长度 | 所需迭代次数 |
|----------|--------|------------|
| 200-300 行 | 100-150 行 | 2 次 |
| 300-500 行 | 150-200 行 | 2-3 次 |
| 500 行以上 | 200 行以上（含参考链接） | 3 次以上（包括重构） |

## 示例：压缩冗长内容

**压缩前**（45 个单词）：
```markdown
## Configuration
The configuration system allows you to customize various aspects of the deployment.
You can set environment variables, adjust timeouts, and configure retry behavior.
Each setting has sensible defaults but can be overridden as needed.
```

**压缩后**（18 个单词）：
```markdown
## Configuration
| Setting | Default | Override |
|---------|---------|----------|
| `ENV` | prod | `--env dev` |
| `TIMEOUT` | 30s | `--timeout 60` |
| `RETRIES` | 3 | `--retries 5` |
```

## 与渐进式文档展示方式的集成

如果经过 3 次迭代后文档长度仍未达到目标：

1. 将文档的概述、快速入门指南和常见错误信息保留到 SKILL.md 中
2. 将 API 详细信息、高级配置设置和示例内容移至 `references/` 目录
3. 在 SKILL.md 中添加链接：`参见 [高级配置](references/config.md)`

## 注意事项

- 请严格保留文档的开头部分（元数据）不要进行压缩
- 保留所有的 ## 标签（这些标签用于区分不同的文档章节）
- 不要删除代码块（因为代码块属于文档的重要组成部分）
- 每个工作流程至少保留一个具体的示例