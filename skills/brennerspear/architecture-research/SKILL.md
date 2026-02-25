---
name: architecture-research
description: 研究代码库或系统的架构。阅读源代码，查找外部相关信息，解释设计决策，并生成 ELK 图表。当需要理解、解释或绘制代码库/系统的架构图时，可以使用此方法。
compatibility: "Requires: diagrams skill (clawhub install diagrams)"
---
# 架构研究

## 触发条件

当用户希望以下操作时，可激活此技能：
- 了解某个仓库或系统的架构设计
- 获取代码库的结构图或数据流图
- 理解项目中的设计决策及权衡因素

## 工作流程

### 1. 阅读源代码

克隆或浏览仓库，并阅读实际代码，包括模块结构、入口点以及关键抽象概念。不要仅依赖 `README.md` 文件。

重点关注以下内容：
- 目录结构和模块边界
- 入口点及公共 API
- 数据模型和存储方式
- 构建/部署配置

### 2. 查找外部资料

搜索官方文档、博客文章、会议演讲、设计文档、架构决策记录（ADR）以及社区讨论，以了解架构设计的背后原因。务必引用所查找到的信息；如果只是基于推测得出结论（没有直接来源），请明确说明。

### 3. 从多个角度进行解释

至少从以下角度进行说明：
| 角度       | 需要展示的内容         |
|------------|-------------------|
| **系统概述**    | 主要组件及其相互关系       |
| **数据/控制流**    | 关键操作（如请求、构建、部署）的执行过程 |
| **设计决策**    | 当前选择的设计方案、其他可能的方案及其原因 |

### 4. 生成 ELK 图表（使用 SVG 格式）

对于每个关键方面，生成一个 ELK JSON 图表（格式为 `elkjs`），然后将其渲染为 SVG 格式，以便在 Markdown 文档中直接显示。

#### ELK JSON 图表的结构
```json
{
  "id": "root",
  "layoutOptions": {
    "elk.algorithm": "layered",
    "elk.direction": "DOWN",
    "elk.spacing.nodeNode": "40"
  },
  "children": [
    { "id": "node1", "width": 150, "height": 60, "labels": [{ "text": "Component A" }] }
  ],
  "edges": [
    { "id": "e1", "sources": ["node1"], "targets": ["node2"], "labels": [{ "text": "calls" }] }
  ]
}
```

#### SVG 渲染方法

该技能使用 `diagrams` 技能进行图表渲染。如果尚未安装该技能，请先进行安装：
```bash
clawhub install diagrams
```

接下来，使用 `diagrams` 技能的渲染工具将 ELK JSON 数据转换为 SVG 格式：
```bash
# Single file
node <diagrams-skill-dir>/scripts/render-elk.mjs diagram.json output.svg

# Batch: all .json files in a folder → svg/ subfolder
node <diagrams-skill-dir>/scripts/render-elk.mjs --dir <folder>

# Batch + PNG (macOS only)
node <diagrams-skill-dir>/scripts/render-elk.mjs --dir <folder> --png
```

请将 `<diagrams-skill-dir>` 替换为已安装的 `diagrams` 技能的目录路径。

> **注意：** `elkjs` 必须安装在运行脚本的本地环境中。具体安装步骤请参考 `diagrams` 技能的 SKILL.md 文件。

**每个图表的工作流程：**
1. 将 ELK JSON 数据写入 `research` 文件夹中的 `.json` 文件。
2. 使用以下命令进行渲染：`node <diagrams-skill-dir>/scripts/render-elk.mjs diagram.json diagram.svg`
3. 在 Markdown 文档中嵌入生成的 SVG 图表：`![系统概述](system-overview.svg)`
4. 保留 `.json` 文件（原始数据）和生成的 `.svg` 文件在 `research` 文件夹中。

#### 提示：
- 对于展示流程或依赖关系的图表，使用 `elk.algorithm: "layered"`。
- 对于展示节点间关系的图表，使用 `elk.algorithm: "force"`。
- 使用复合节点（父节点包含子节点）来组织相关节点。
- 用标签标注边的类型（如调用、导入、输出、读取等）。
- 每张图表的节点数量控制在 20 个以内；如有需要，可拆分成多张图表。

### 5. 输出结果

创建一个 `research` 文件夹，并生成相应的 Markdown 文档：
```
<output-dir>/<repo-slug>-architecture/
├── prompt.md          # Original question
├── architecture.md    # The deliverable
├── *.json             # ELK JSON source files (editable)
└── *.svg              # Rendered SVG diagrams (embedded in architecture.md)
```

将输出结果保存在合适的工作目录中（例如 `research/` 目录下）。

**architecture.md` 文档的格式：
```markdown
# [Repo Name] — Architecture

**Repo:** <url>
**Researched:** <date>

## Overview
<1-2 paragraph summary of what this thing is and how it's built>

## System Diagram
![System Overview](system-overview.svg)
<Prose explanation>

## Data/Control Flow
<Pick a key operation, walk through it>
![Request Flow](request-flow.svg)

## Design Decisions

| Decision | Alternative | Rationale | Source |
|----------|------------|-----------|--------|
| ... | ... | ... | link or "inferred" |

## Key Abstractions
<The core types/interfaces/patterns that make the system tick>

## Sources
<Links to docs, posts, talks cited above>
```

### 6. 交付成果

在聊天中发送一份简短的总结（200-150 字），概述主要发现，并附上完整的文档或提供文档的链接。如用户需要，可提供 PDF 格式的文档。

## 注意事项：
- **不要编造内容。** 如果无法解释某个设计的理由，请注明“根据推测”或“未找到相关资料”。
- **Excalidraw 替代方案：** 如果用户要求使用 Excalidraw 生成图表，可以尝试使用该工具，但默认使用的是 ELK JSON 格式。
- **Mermaid 替代方案：** 如果用户的工具无法渲染 ELK 图表，可以提供 Mermaid 作为备用方案。
- **范围控制：** 对于大型仓库，先重点介绍整体架构框架；如用户需要，可进一步深入讲解特定子系统。