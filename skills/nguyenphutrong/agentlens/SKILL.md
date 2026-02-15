---
name: agentlens
description: 使用 agentlens 的分层式文档结构来导航和理解代码库。适用于探索新项目、查找模块、在大型文件中定位符号、查找待办事项/警告信息，或理解代码结构。
metadata:
  short-description: Codebase navigation with agentlens
  author: agentlens
  version: "1.0"
---

# AgentLens - 代码库导航

## 在开始处理任何代码库之前
请务必先阅读 `.agentlens/INDEX.md`，以了解项目整体结构。

## 导航层次结构

| 层级 | 文件 | 用途 |
|-------|------|---------|
| L0 | `INDEX.md` | 项目概览，列出所有模块 |
| L1 | `modules/{slug}/MODULE.md` | 模块详细信息，文件列表 |
| L1 | `modules/{slug}/outline.md` | 大文件中的函数/方法索引 |
| L1 | `modules/{slug}/memory.md` | 待办事项、警告信息、业务规则 |
| L1 | `modules/{slug}/imports.md` | 文件依赖关系 |
| L2 | `files/{slug}.md` | 复杂文件的详细文档 |

## 导航流程

```
INDEX.md → Find module → MODULE.md → outline.md/memory.md → Source file
```

## 在什么情况下阅读相应的文档

| 需要什么 | 阅读什么 |
|----------|-----------|
| 了解项目概览 | `.agentlens/INDEX.md` |
| 查找特定模块 | `INDEX.md`，搜索模块名称 |
| 了解模块详情 | `modules/{slug}/MODULE.md` |
| 在大文件中查找函数/方法 | `modules/{slug}/outline.md` |
| 查看待办事项、警告信息、业务规则 | `modules/{slug}/memory.md` |
| 了解文件依赖关系 | `modules/{slug}/imports.md` |

## 最佳实践

1. **对于大型代码库，不要直接阅读源代码**——先使用 `outline.md` 进行快速浏览 |
2. **修改代码前，请先查看 `memory.md` 以了解警告和待办事项** |
3. **使用 `outline.md` 定位所需的功能/方法，然后仅阅读相关的源代码部分** |
4. 如果文档看起来过时，请使用 `agentlens` 命令重新生成文档。

有关详细的导航规则，请参阅 [references/navigation.md]；
有关代码库结构的说明，请参阅 [references/structure.md]。