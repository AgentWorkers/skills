---
name: seekdb-docs
description: **seekdb数据库文档查询**  
当用户询问关于seekdb的功能、SQL语法、向量搜索、混合搜索、集成方式、部署方法或任何与seekdb相关的问题时，可以使用此功能。系统会通过基于目录的语义搜索自动定位相关文档。
version: "V1.1.0"
---

# seekdb 文档

本文档通过一个集中式的目录系统，提供了对 seekdb 数据库的全面访问。

## 快速入门

1. **定位技能目录**（请参阅下面的路径解析方法）
2. **加载完整目录**（包含 1015 个文档条目）
3. **根据查询内容在目录中找到匹配项**
4. **从匹配到的条目中阅读文档**

## 路径解析（关键的第一步）

**问题**：像 `./seekdb-docs/` 这样的相对路径是从 **当前工作目录** 开始解析的，而不是从 SKILL.md 的位置开始解析的。当代理的工作目录与技能目录不同时，这会导致问题。

**解决方案**：在访问文档之前，动态地定位技能目录。

### 分步解析过程

1. **读取 SKILL.md 本身** 以获取其绝对路径：
   ```
   read(SKILL.md)  // or any known file in this skill directory
   ```

2. **从返回的路径中提取技能目录**：
   ```
   If read returns: /root/test-claudecode-url/.cursor/skills/seekdb/SKILL.md
   Skill directory: /root/test-claudecode-url/.cursor/skills/seekdb/
   ```

3. **使用该目录构建文件路径**：
   ```
   Catalog path: <skill directory>references/seekdb-docs-catalog.jsonl
   Docs base: <skill directory>seekdb-docs/
   ```

## 文档来源

### 完整目录
- **本地**：`<技能目录>references/seekdb-docs-catalog.jsonl`（1015 个条目，JSONL 格式）
- **远程**：`https://raw.githubusercontent.com/oceanbase/seekdb-ecology-plugins/main/agent-skills/skills/seekdb/references/seekdb-docs-catalog.jsonl`（备用方案）
- **条目数量**：1015 个文档文件
- **覆盖范围**：完整的 seekdb 文档
- **格式**：JSONL 格式——每行一个 JSON 对象，包含文件路径和描述

### 完整文档（优先使用本地文档，远程作为备用）

**本地文档**（如果可用）：
- **基础路径**：`<技能目录>seekdb-docs/`
- **大小**：7.4MB，包含 952 个 markdown 文件
- **文档路径**：基础路径 + 文件路径

**远程文档**（备用方案）：
- **基础 URL**：`https://raw.githubusercontent.com/oceanbase/seekdb/V1.1.0/en-US/`
- **文档路径**：基础 URL + 文件路径

**策略**：
1. **定位**：使用上述路径解析方法确定 `<技能目录>`
2. **加载**：加载完整目录（1015 个条目）——优先尝试本地，必要时使用远程
3. **搜索**：在所有目录条目中进行语义搜索
4. **阅读**：优先尝试本地文档，如果找不到则使用远程 URL

## 工作流程

### 第 0 步：解析路径（请先执行此步骤！）

```bash
# Read this file to discover its absolute path
read("SKILL.md")

# Extract directory from the path
# Example: /root/.claude/skills/seekdb/SKILL.md → /root/.claude/skills/seekdb/
```

### 第 1 步：搜索目录

首先使用 grep 进行关键词搜索。只有在必要时才加载完整目录。

#### 方法 1：Grep 搜索（适用于 90% 的查询）

使用 grep 在目录中搜索关键词：
```bash
grep -i "keyword" <skill directory>references/seekdb-docs-catalog.jsonl
```

**示例**：
```bash
# Find macOS deployment docs
grep -i "mac" references/seekdb-docs-catalog.jsonl

# Find Docker deployment docs
grep -i "docker\|container" references/seekdb-docs-catalog.jsonl

# Find vector search docs
grep -i "vector" references/seekdb-docs-catalog.jsonl
```

#### 方法 2：仅在必要时加载完整目录

仅在以下情况下加载完整目录：
- grep 搜索没有结果
- 需要进行复杂的语义匹配
- 没有特定的关键词需要搜索

```
Local: <skill directory>references/seekdb-docs-catalog.jsonl
Remote: https://raw.githubusercontent.com/oceanbase/seekdb-ecology-plugins/main/agent-skills/skills/seekdb/references/seekdb-docs-catalog.jsonl (fallback)
Format: JSONL (one JSON object per line)
Entries: 1015 documentation files
```

**策略**：
1. 首先尝试本地目录：`<技能目录>references/seekdb-docs-catalog.jsonl`
2. 如果本地目录中没有找到所需内容，则从上述远程 URL 下载

**目录内容**：
- 每一行包含一个 JSON 对象，格式为 `{"path": "...", "description": "..."}`
- 所有 seekdb 文档都被索引在目录中
- 优化了语义搜索和 grep 查询的性能

### 第 2 步：匹配查询结果

分析搜索结果，找出最相关的文档：

**对于 grep 搜索结果**：
- 查看 grep 输出中的匹配行
- 从每个匹配结果中提取文件路径和描述
- 选择描述与查询最匹配的文档
- 为了获得全面的答案，可以考虑多个匹配结果

**对于完整目录**：
- 将每行解析为 JSON 格式，提取文件路径和描述
- 对描述内容进行语义匹配
- 根据文档的实际含义进行匹配，而不仅仅是关键词
- 返回所有相关的条目以提供全面的答案

**注意**：目录中包含 `path` 和 `description` 两个字段。`description` 字段包含了主题和功能相关的关键词，因此既适合关键词搜索也适合语义搜索。

### 第 3 步：阅读文档

**优先使用本地文档的策略**：
1. **首先尝试本地文档**：`<技能目录>seekdb-docs/[文件路径]`
   - 如果文件存在 → 在本地快速读取
   - 如果文件不存在 → 进入第 2 步

2. **使用远程文档**：`https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.1.0/en-US/[文件路径]`
   - 从 GitHub 下载文件

**示例**：
```
Query: "How to integrate with Claude Code?"

1. Resolve path: read(SKILL.md) → /root/.claude/skills/seekdb/SKILL.md
   Skill directory : /root/.claude/skills/seekdb/

2. Search catalog with grep:
   grep -i "claude code" /root/.claude/skills/seekdb/references/seekdb-docs-catalog.jsonl

3. Match query from grep results:
   → Found: {"path": "300.integrations/300.developer-tools/700.claude-code.md",
             "description": "This guide explains how to use the seekdb plugin with Claude Code..."}
   → This matches the query, select this document

4. Read doc:
   Try: /root/.claude/skills/seekdb/seekdb-docs/300.integrations/300.developer-tools/700.claude-code.md
   If missing: https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.1.0/en-US/300.integrations/300.developer-tools/700.claude-code.md
```

## 使用指南

- **始终先解析路径**：使用 `read-your-SKILL.md` 的方法获取绝对路径
- **对于关键词查询，优先使用 grep**：只有在 grep 搜索没有结果或需要语义匹配时才加载完整目录
- **语义匹配**：根据文档的实际含义进行匹配，而不仅仅是关键词
- **多个匹配结果**：为了获得全面的答案，会读取所有相关的条目
- **优先使用本地文档，远程作为备用**：首先尝试本地文档，如果找不到则使用远程 URL
- **可选的本地文档下载**：运行 `scripts/update_docs.sh` 命令将所有文档下载到本地（速度更快）
- **离线可用**：只要有本地文档，就可以完全离线使用

## 目录搜索格式

目录文件采用 **JSONL 格式**（每行一个 JSON 对象）：

```json
{"path": "path/to/document.md", "description": "Document description text"}
```

**搜索目录的方法**：
- **关键词搜索**：使用 grep（参见第 1 步的示例）。每个匹配的条目都包含文件路径和描述。
- **当 grep 搜索不够准确时**：读取完整目录，将每行解析为 JSON 格式，然后对描述内容进行语义匹配。

## 常见的安装路径

该技能可以安装在以下位置：
- **Cursor**：`.cursor/skills/seekdb/`
- **Claude Code**：`.claude/skills/seekdb/`
- **自定义目录**：任何目录（路径解析会自动处理）

**请不要将这些路径硬编码**。请使用动态路径解析方法。

## 详细示例

请参阅 [examples.md](references/examples.md)，其中包含完整的流程示例，包括：
- 完整的目录搜索场景
- 优先使用本地文档的查找场景
- 使用远程文档作为备用的场景
- 集成查询
- 多轮对话的示例

## 类别概述

- **入门**：快速入门、基本操作、概述
- **开发**：向量搜索、混合搜索、AI 功能、MCP、多模型
- **集成**：框架、模型平台、开发工具、工作流程
- **指南**：部署、管理、安全、OBShell、性能
- **参考**：SQL 语法、PL 语言、错误代码、SDK API
- **教程**：分步操作指南