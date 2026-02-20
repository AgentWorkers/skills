---
name: solo-audit
description: 健康检查知识库（Health Check Knowledge Base）用于检测链接失效、缺少前言内容（frontmatter）、标签使用不一致（tag inconsistencies）以及知识库覆盖范围存在漏洞（coverage gaps）等问题。当用户请求执行“审计知识库”（audit KB）、“检查前言内容”（check frontmatter）、“查找失效链接”（find broken links）或“清理标签”（tag cleanup）等操作时，可使用该工具。请勿将其用于SEO审计（请使用 /seo-audit）或代码审查（code reviews）。
license: MIT
metadata:
  author: fortunto2
  version: "1.4.0"
  openclaw:
    emoji: "🩺"
allowed-tools: Read, Grep, Bash, Glob, mcp__solograph__kb_search
argument-hint: "[optional: focus area like 'tags' or 'frontmatter']"
---
# /audit

对知识库进行质量检查，查找以下问题：缺少前言（frontmatter）、链接失效、标签不一致、孤立文件（orphaned files）以及内容覆盖范围不足（coverage gaps）。该工具适用于任何包含大量Markdown文件的项目。

## 步骤

1. **确定检查重点**：从 `$ARGUMENTS` 中获取检查重点（可选）。如果提供了重点，仅检查该重点（例如：“tags”、“frontmatter”、“links”）；如果未提供，则执行全面检查。

2. **查找所有Markdown文件**：使用Glob命令查找所有`.md`文件，同时排除以下非内容目录：`.venv/`、`node_modules/`、`.git/`、`.embeddings/`、`archive/`、`archive_old/`。

3. **前言检查**：对于每个Markdown文件，检查其前言内容：
   - 是否包含YAML格式的前言（以`---`开头并以`---`结尾）
   - 是否包含必填字段：`type`、`status`、`title`、`tags`
   - `type`字段的值是否有效（只能是`principle`、`methodology`、`agent`、`opportunity`、`capture`、`research`之一）
   `status`字段的值是否有效（只能是`active`、`draft`、`validated`、`archived`之一）
   `tags`字段是否为非空列表
   记录缺少前言的文件以及前言内容不完整或无效的文件。

4. **链接检查**：
   - 如果存在`scripts/check_links.py`脚本，运行该脚本：`uv run python scripts/check_links.py`
   - 否则，使用Grep命令查找Markdown文件中的链接（格式为`\[.*\]\(.*\.md\)`，并验证每个链接的目标文件是否存在。

5. **标签一致性检查**：使用Grep命令查找所有`.md`文件中的`tags:`部分，检查以下问题：
   - 标签重复（例如：“ai”与“AI”或“artificial-intelligence”）
   - 仅被使用一次的标签（可能是拼写错误）
   - 过于宽泛的常用标签
   列出所有唯一标签及其使用频率。

6. **孤立文件检查**：查看哪些文件在其他文件的`related:`字段中未被引用。这些文件可能是孤立文件（即没有被其他内容引用的文件）。

7. **机会类文档（opportunity documents）的质量检查**：查找所有`type`为`opportunity`的文档，并检查以下内容：
   - 是否缺少`opportunity_score`字段
   `evidence_sources`字段是否为0或未设置
   文档的状态是否在30天后仍为`draft`

8. **内容覆盖范围检查**：检查每个目录的内容：
   - 标记为空或内容极少的目录
   - 查看只有1-2个文件的目录（可能需要补充更多内容）

9. **生成报告**：
   ```
   ## KB Audit Report

   **Date:** [today]

   ### Summary
   - Total .md files: X
   - With frontmatter: X (X%)
   - Without frontmatter: X

   ### Frontmatter Issues
   | File | Issue |
   |------|-------|
   | path | Missing field: type |

   ### Broken Links
   [list of broken references]

   ### Tag Analysis
   - Total unique tags: X
   - Single-use tags: [list]
   - Potential duplicates: [list]

   ### Orphaned Files
   [files not referenced anywhere]

   ### Opportunity Quality
   - Without opportunity_score: [list]
   - Without evidence_sources: [list]

   ### Coverage
   [directory analysis]

   ### Recommendations
   1. [specific action]
   2. [specific action]
   3. [specific action]
   ```

## 常见问题

### 未找到Markdown文件
**原因**：可能在错误的目录中运行脚本，或者所有文件都被排除在外。
**解决方法**：确保位于知识库的根目录下，并检查步骤2中设置的排除规则。

### 标签使用过于频繁（单一用途标签过多）
**原因**：文档间的标签使用不统一。
**解决方法**：从使用频率最高的标签列表中选择标准标签，清理后重新运行检查。

### 前言验证错误
**原因**：YAML语法错误（缺少引号或缩进不正确）。
**解决方法**：确保前言以`---`开头和结尾，并使用允许的`type:`和`status:`值。