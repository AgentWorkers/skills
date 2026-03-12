---
name: seekdb-docs
description: >
  **seekdb 数据库文档查询**  
  当用户咨询关于 seekdb 的功能、SQL 语法、向量搜索、混合搜索、集成方式、部署方法或任何与 seekdb 相关的主题时，可以使用此功能。系统会通过基于目录的语义搜索自动定位相关文档。
---
# seekdb 文档说明

该技能通过基于目录的搜索系统提供对约 1000 个 seekdb 文档条目的访问。**仅支持远程模式**：该技能仅提供目录信息；文档内容始终从公共文档 URL 加载（不使用本地的 `seekdb-docs/` 目录）。

## 功能范围与行为

该技能仅用于文档查询，不执行任何代码或脚本。代理程序会读取本地的目录文件（一个 JSONL 文件），并从公共的只读 URL 获取文档内容。无需输入凭证，也不涉及任何安装或子进程调用。

## 版本信息

<!-- 信息会自动更新，请勿手动修改 -->
- **支持的文档版本**：V1.0.0、V1.1.0（以最新版本为准）
- **最新版本**：V1.1.0
- 目录条目中的 `branch` 字段表示文件所在的 Git 分支（仅用于生成远程备用 URL）。该字段并不表示文档内容适用于哪个具体的 seekdb 版本——许多文档适用于所有版本。
- 如果用户询问特定版本的 seekdb 文档，请注意这些文档内容反映的是最新版本的信息，可能无法区分不同版本之间的差异。

## 路径解析（请先执行此步骤）

1. 阅读本 SKILL.md 文件以获取其绝对路径，并提取父目录作为 `<skill_dir>`。
2. 目录文件：`<skill_dir>references/seekdb-docs-catalog.jsonl`
   如果本地不存在，请从以下地址下载：`https://raw.githubusercontent.com/oceanbase/seekdb-ecology-plugins/main/agent-skills/skills/seekdb/references/seekdb-docs-catalog.jsonl`

## 工作流程

### 第一步：搜索目录

**关键词搜索（适用于大多数查询）**
在目录文件 `<skill_dir>references/seekdb-docs-catalog.jsonl` 中搜索包含查询关键词的行。每行是一个 JSON 对象，包含 `path`、`description` 和 `branch` 字段。搜索时可以匹配关键词或文档内容的语义。

**完整目录**（如需查看所有文档）：使用上述文件，或从以下地址下载：`https://raw.githubusercontent.com/oceanbase/seekdb-ecology-plugins/main/agent-skills/skills/seekdb/references/seekdb-docs-catalog.jsonl`。格式为 JSONL 格式——每行包含一个 `{"path": "...", "description": "...", "branch": "..."}`（约 1000 条记录）。

### 第二步：匹配查询结果

- 从搜索结果中提取 `path`、`description` 和 `branch` 字段。
- 选择描述与查询内容最匹配的文档条目（匹配的是文档的语义，而不仅仅是关键词）。
- 为获得更全面的答案，可以考虑多个匹配结果。

### 第三步：远程读取文档

从公共文档 URL 下载文档（该技能包中不包含本地文档文件）：
- URL 格式：`https://raw.githubusercontent.com/oceanbase/seekdb-doc/[branch]/en-US/[path]`
- `[branch]` 和 `[path]` 来自目录条目（例如 `V1.0.0`、`V1.1.0`）。某些文件仅存在于特定的 Git 分支上。

## 示例

```
Query: "How to integrate with Claude Code?"

1. Search catalog: look for lines containing "claude code" in <skill_dir>references/seekdb-docs-catalog.jsonl
2. Match: {"path": "300.integrations/300.developer-tools/700.claude-code.md",
           "description": "This guide explains how to use the seekdb plugin with Claude Code...",
           "branch": "V1.0.0"}
3. Fetch doc: https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/300.integrations/300.developer-tools/700.claude-code.md
```

更多完整的工作流程示例请参见 [examples.md](references/examples.md)。

## 注意事项

- **多版本支持**：每个目录条目的 `branch` 字段会用于生成文档的 URL；某些文件仅存在于特定的 Git 分支上。

## 文档分类

- **入门指南**：快速入门、基本操作、概述
- **开发相关**：向量搜索、混合搜索、AI 功能、MCP、多模型
- **集成**：框架、模型平台、开发工具、工作流程
- **指南**：部署、管理、安全性、OBShell、性能优化
- **参考资料**：SQL 语法、PL（编程语言）、错误代码、SDK API
- **教程**：分步操作指南