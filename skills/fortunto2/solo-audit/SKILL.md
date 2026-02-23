---
name: solo-audit
description: 健康检查知识库（Health Check Knowledge Base）用于检测链接失效、缺少前置内容（frontmatter）、标签不一致（tag inconsistencies）以及知识覆盖范围存在漏洞（coverage gaps）等问题。当用户请求“审核知识库”（audit KB）、“检查前置内容”（check frontmatter）、“查找失效链接”（find broken links）或“清理标签”（tag cleanup）时，可以使用该工具。请勿将其用于SEO审计（请使用 /seo-audit）或代码审查（code reviews）。
license: MIT
metadata:
  author: fortunto2
  version: "1.4.1"
  openclaw:
    emoji: "🩺"
allowed-tools: Read, Grep, Bash, Glob, mcp__solograph__kb_search
argument-hint: "[optional: focus area like 'tags' or 'frontmatter']"
---
# /audit

用于审计知识库中的质量问题，包括缺少前言部分、链接失效、标签不一致、孤立文件以及内容覆盖范围不足等问题。适用于任何使用大量 Markdown 格式文件的项目。

## 步骤

1. **从 `$ARGUMENTS` 中解析审计重点区域**（可选）。如果提供了该参数，将审计集中在指定区域（例如 “tags”（标签）、”frontmatter”（前言部分）或 “links”（链接））。如果未提供参数，则执行全面审计。

2. **查找所有 Markdown 文件**：使用 Glob 命令查找所有 `.md` 文件，同时排除以下非内容目录：`.venv/`、`node_modules/`、`.git/`、`archive/` 和 `archive_old/`。

3. **前言部分审计**：首先扫描部分现有文件（前 10-20 个文件），以确定所使用的前言结构（哪些字段存在，`type` 和 `status` 字段的常见值是什么）。然后对每个 Markdown 文件进行检查：
   - 是否包含 YAML 格式的前言部分（以 `---` 开头并以 `---` 结尾）
   - 是否包含核心字段：`title`（标题）、`tags`（标签）（以及在整个知识库中一致使用的其他字段）
   `type` 和 `status` 字段的值是否与检测到的结构一致
   `tags` 是否为非空列表
   记录缺少前言部分的文件以及前言部分不完整或无效的文件。

4. **链接检查**：查找失效的内部链接：
   使用正则表达式 `\[.*\]\(.*\.md\)` 查找 Markdown 链接，并验证每个目标文件是否存在
   如果项目中存在用于检查链接的脚本（例如 `scripts/check_links.py`），请同时运行该脚本。

5. **标签一致性审计**：使用正则表达式查找所有 `.md` 文件中的 `tags:` 部分，检查以下问题：
   - 几乎重复的标签（例如 “ai”、“AI” 和 “artificial-intelligence”）
   - 仅被使用一次的标签（可能是拼写错误）
   - 过于宽泛的常用标签
   列出所有唯一的标签及其使用频率。

6. **孤立文件**：检查哪些文件没有被其他文件的 `related:` 字段引用。这些文件可能存在问题（即它们是孤立的）。

7. **内容质量审计**：根据检测到的 `type` 字段或文件所在目录，找出可能属于概念性文档或待开发文档的文件，并检查以下内容：
   - 已处于 “draft”（草稿）状态的文档是否超过 30 天
   - 是否缺少其他类似文档所具有的关键元数据字段
   - 内容非常少的文档（字数少于 100 字，不包括前言部分）

8. **内容覆盖范围审计**：检查每个目录的内容：
   - 标记为空或几乎为空的目录
   - 检查只有 1-2 个文件的目录（可能需要补充更多内容）

9. **生成审计报告**：
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

   ### Content Quality
   - Stale drafts (> 30 days): [list]
   - Missing metadata: [list]
   - Low-content files: [list]

   ### Coverage
   [directory analysis]

   ### Recommendations
   1. [specific action]
   2. [specific action]
   3. [specific action]
   ```

## 常见问题

### 未找到 Markdown 文件
**原因**：可能在错误的目录中运行审计，或者所有文件都被排除在外。
**解决方法**：确保当前位于知识库的根目录。检查步骤 2 中指定的排除规则。

### 标签使用过于分散（单一用途标签过多）
**原因**：文档之间的标签使用不统一。
**解决方法**：从使用频率最高的标签列表中选择标准标签。清理后重新执行审计。

### 前言部分验证错误
**原因**：YAML 语法错误（缺少引号、缩进不正确）。
**解决方法**：确保使用正确的 `---` 作为分隔符，并确保 `type:` 和 `status:` 字段的值与知识库的规范一致。