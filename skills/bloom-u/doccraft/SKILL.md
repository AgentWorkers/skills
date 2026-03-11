---
name: doccraft
description: 根据现有的材料、大纲或模板，创建内容完整、基于源代码的专业文档。随后生成、编辑、审阅或标记最终的.docx文件。当Codex需要将PDF、DOCX、TXT、Markdown或混合格式的项目源文件转换为提案、技术方案、实施计划、施工方案、报告、申报材料等正式的、结构化的长期交付物时，可以使用此流程。这些交付物需要具备Word格式，并且支持审阅流程。
---
# DocCraft

## 概述

此技能分为两个层次使用：

1. 从源材料和目标框架中构建结构清晰的文本。
2. 如有需要，创建或修改最终的 `.docx` 交付成果。

在文本内容和结构稳定之前，始终使用 Markdown 或纯文本作为工作的基础。只有在内容足够成熟后，再进行 `.docx` 文件的创建、格式化、版本控制或注释处理。

该技能提供了本地生成 `.docx` 文件的功能。请勿假设已安装了单独的 `$docx` 技能。

某些上传目标不支持包含 `.xsd` 等 OOXML 架构文件的包。在准备可发布的包时，请使用此技能提供的“上传安全”版本。该版本保留了文档生成和编辑的工作流程，但省略了严格的架构验证。

当最终交付成果为 Word 文档时，在最终确定格式之前，请务必明确以下内容：

- 用户提供的模板或现有的目标文档。
- 用户明确的格式要求。
- 相同领域内被认可的样本文档。
- 该技能中的默认格式配置文件。

## 工作流程决策树

### A. 从现有材料构建新文档

使用基于源文本的工作流程：

1. 规范化任务输入。
2. 创建源文档清单。
3. 根据目标大纲创建章节概要。
4. 起草章节文件。
5. 进行文档级一致性审查。
6. 拼装最终的 Markdown 或文本输出。

### B. 读取、创建或编辑 Word 文档

使用此技能中的 `.docx` 工作流程：

- 当只需要提取文本时，使用 `pandoc` 读取现有的 `.docx` 内容。
- 只有在完全阅读 [docx-js.md](docx-js.md) 后，才从头开始创建新的 `.docx` 文件。
- 只有在完全阅读 [ooxml.md](ooxml.md) 后，才编辑或标记现有的 `.docx` 文件。
- 对于政府、法律、学术或第三方文档，默认使用版本控制或注释功能。

### C. 同时进行两者

将工作分为几个阶段：

1. 先起草并稳定文本内容。
2. 固定基于源文本的表述。
3. 再进行 `.docx` 文件的生成或编辑。

除非任务非常简单，否则不要在同一阶段同时进行大量的内容生成和低级别的 OOXML 编辑。

## 基于源文本的工作流程

### 1. 规范化输入

在起草之前，请确认以下四个输入：

- **源文档库**：包含事实的目录和文件。
- **目标结构**：所需的大纲、模板或章节列表。
- **写作规则**：语气、排除内容、术语、格式、审查要求。
- **输出格式**：章节文件、合并后的 Markdown 文件、`.docx` 文件、审查备忘录或版本控制文件。

如果缺少任何输入，请推断出最低限度的安全默认值，并在工作笔记中说明这一假设，但不要在最终交付成果中体现。

如果输出格式包括 `.docx`，请提前确定格式规范。在需要捕获或确认格式规范时，请阅读 [references/word-format-profile.md](references/word-format-profile.md)，并使用 [scripts/init_format_profile.py](scripts/init_format_profile.py)。

如果任务是生成正式的、完整的 Word 文档，请在起草之前制定交付概要。阅读 [references/word-delivery-brief.md](references/word-delivery-brief.md)，并使用 [scripts/init_delivery_brief.py](scripts/init_delivery_brief.py) 来记录用户需要指定的内容以及仍需确认的信息。

### 2. 创建源文档清单

在开始写作之前，创建可用材料的清单。当文档库包含多个文件时，请阅读 [references/source-manifest.md](references/source-manifest.md)。

使用 [scripts/build_manifest.py](scripts/build_manifest.py) 生成初步清单，然后根据需要手动补充或调整。

清单应区分以下内容：

- 权威的源文件。
- 派生文件（如提取的文本、草稿或之前的输出）。
- 模板或大纲文件。
- 仅用于查找的文件（不用于引用）。

### 3. 创建章节概要

不要直接从大量文档中起草最终章节的内容。首先为每个目标章节创建一个章节概要。

在制定计划时，请阅读 [references/section-briefs.md](references/section-briefs.md)，并使用 [scripts/plan_sections.py](scripts/plan_sections.py) 将大纲转换为概要草稿。

每个章节概要应至少包含以下内容：

- 章节ID和标题。
- 章节的目的。
- 必须涵盖的内容。
- 可用的通用材料。
- 主要和次要的参考来源。
- 预期的图表和检查清单。
- 与相邻章节的冲突点。
- 未解决的问题或来源中的空白部分。

对于大型项目，章节概要是多个参与者之间的共同约定。

### 4. 起草章节内容

在起草之前，请阅读 [references/drafting-rules.md](references/drafting-rules.md)。

根据章节概要进行起草，而不是直接参考整个文档库。这样可以保持写作的条理性并减少重复。

规则：
- 保持与源文档相关的事实的可验证性。
- 仅允许使用管理、质量、安全、流程或行业标准措施相关的通用模板语言，且这些内容不应与源文档库冲突。
- 优先使用具体的实现语言，而不是口号式的抽象表述。
- 将图表和表格整合到正文中。不要创建仅标注为“图表”或“表格”的标题。
- 如果最终交付成果不允许显示来源注释，请将所有证据注释保留在工作文件中。

### 5. 进行一致性审查

在合并完整文档之前，请阅读 [references/consistency-review.md](references/consistency-review.md)。

进行全面审查，包括：
- 术语的一致性。
- 数字、数量、范围和接口的一致性。
- 重复或矛盾的段落。
- 章节边界的冲突。
- 标题编号和命名的一致性。
- 不应出现在最终版本中的隐藏源标签。

### 6. 拼装输出

根据需要，使用 [scripts/assemble_markdown.py](scripts/assemble_markdown.py) 将有序的章节文件合并成单一的 Markdown 草稿。

请明确区分以下内容：
- 包含证据或待办事项的工作草稿。
- 为 `.docx` 转换准备的干净交付成果。

## 默认执行模式

### 单个参与者模式

在以下情况下，默认使用单个参与者：

- 大纲较短。
- 源文档库较小。
- 跨章节之间的依赖性较高。
- 用户主要希望获得连贯的草稿，而不是并行处理。

### 多个参与者模式

仅在以下情况下使用多个参与者：

- 源文档库较大。
- 各章节相对独立。
- 可以先生成共享的术语表、写作规则和章节概要。

在多参与者模式下，在分配工作之前，请创建以下共享资源：
1. 源文档清单。
2. 章节概要包。
3. 如果命名较为敏感，还需创建术语表。
4. 共享的写作规则。

不要让参与者自行制定不同的命名系统、证据规则或章节边界。

## `.docx` 工作流程

### 读取或分析 `.docx`

如果只需要文本，可以使用以下代码块进行转换：
```bash
pandoc --track-changes=all path-to-file.docx -o output.md
```

如果需要结构、注释、媒体或版本控制信息，请解压 OOXML 包并检查 XML 内容。

### 创建新的 `.docx`

在编写任何代码之前，请完整阅读 [docx-js.md](docx-js.md)。

在以下情况下，使用捆绑的 `docx` JavaScript 工作流程：
- 从稳定的文本中创建新的 Word 文档。
- 从 Markdown 或结构化内容重新构建格式化的交付成果。
- 程序化生成表格、标题、页面设置、页眉或页脚。

在最终生成 `.docx` 之前，请确定格式规范。如果不存在权威模板，请使用 [references/word-format-profile.md](references/word-format-profile.md) 中的默认格式规范。

在最终生成 `.docx` 之前，还需解决影响文档完整性、审查模式和输出打包的交付细节问题。

在最终生成 `.docx` 之前，请运行 [scripts/resolve_word_job.py](scripts/resolve_word_job.py) 或参考 [references/word-assembly-plan.md](references/word-assembly-plan.md)，以确定 Word 文档是否准备好交付，哪些组件将被生成，以及还存在哪些障碍。

当任务准备好后，使用 [scripts/generate_docx_from_markdown.cjs](scripts/generate_docx_from_markdown.cjs) 生成文件。输入合并后的 Markdown 内容、交付概要 JSON 和格式规范 JSON。

### 编辑现有的 `.docx`

在编辑之前，请完整阅读 [ooxml.md](ooxml.md)。

在以下情况下，使用捆绑的 OOXML 工作流程：
- 编辑现有的 Word 文件。
- 保持现有的格式。
- 添加注释。
- 插入版本控制信息。
- 在专业文档中进行安全的结构编辑。

### 标记和审查模式

在编辑以下类型的文档时，默认使用版本控制或注释功能：
- 政府文档。
- 法律、商业或学术文档。
- 其他作者的文件。
- 审查性与正确性同样重要的文档。

使用此技能中的捆绑资源：
- [scripts/document.py](scripts/document.py)
- [scripts/utilities.py](scripts/utilities.py)
- [ooxml/scripts/unpack.py](ooxml/scripts/unpack.py)
- [ooxml/scripts/pack.py](ooxml/scripts/pack.py)
- [ooxml/scripts/validate.py](ooxml/scripts/validate.py)

如果上传安全的包中排除了 `.xsd` 架构文件，请将严格的架构验证视为不可用，继续执行解压、编辑和重新打包的工作流程。

### 格式确认规则

如果任务仍处于文本起草阶段，请不要过早要求用户确认格式。除非格式决策会显著改变文档结构，否则先起草内容。

在以下情况下，请在最终交付 Word 文档之前要求用户确认格式：
- 文档是外部或正式的交付成果。
- 不存在权威的模板或认可的样本文档。
- 用户提供了相互矛盾的格式要求。
- 输出必须严格符合机构标准。

在以下情况下，无需请求用户确认格式：
- 用户已经提供了模板或目标 `.docx` 文件。
- 任务仍然是 Markdown 或纯文本形式的草稿。
- 用户明确接受了技能的默认设置。

当需要确认格式时，请提供已确定的格式规范，而不是开放式问题。如果用户没有进行修改，请使用 [references/word-format-profile.md](references/word-format-profile.md) 中的默认设置。

### 交付概要规则

对于完整的 Word 文档交付成果，将用户的输入分为两类：

用户在起草之前必须指定以下内容：
- 文档标题
- 源文档库或权威的来源集
- 目标大纲、模板或要匹配的现有文档
- 文档的目的和目标受众
- 输出格式：新文档、重写或编辑现有的 `.docx`

用户在最终交付 Word 文档之前必须确认以下内容：
- 交付阶段是最终阶段，而不仅仅是草稿阶段
- 完整性要求（如封面、目录、附录、术语表、列表和附件）
- 审查模式：干净版本、版本控制或注释
- 格式规范或模板选择
- 如果交付包是正式的，还需确定文件命名或版本控制方式
- 是否需要从最终版本中删除工作笔记、来源标记或可追溯性信息

如果这些内容不明确，请在确保安全默认值不会影响内容的情况下继续起草文本。在未解决所有交付概要相关问题之前，不要最终确定 Word 文档的格式。

### Word 文档组装规则

将最终的 Word 生成视为一个有步骤的组装过程，而不仅仅是文件导出。

在组装之前，请解决以下问题：
- 是否准备好进入草稿阶段或最终阶段
- 所需的包组件（如封面、目录、附录、术语表、列表和附件清单）
- 审查模式（如干净版本、版本控制或注释）
- 工作笔记和来源痕迹的清理方式

如果任务尚未准备好，请停留在 Markdown 或内部 `.docx` 草稿阶段，并明确指出存在的障碍。

## 资源映射

- [references/source-manifest.md](references/source-manifest.md)：如何清点并分类源文档库。
- [references/section-briefs.md](references/section-briefs.md)：如何将大纲转换为可执行的章节概要。
- [references/drafting-rules.md](references/drafting-rules.md)：编写结构清晰文档的起草标准。
- [references/consistency-review.md](references/consistency-review.md)：文档级别的审查清单。
- [references/word-format-profile.md](references/word-format-profile.md)：格式规范规则和默认的 Word 格式设置。
- [references/word-delivery-brief.md](references/word-delivery-brief.md)：用户为完整的 Word 文档交付成果必须指定和确认的内容。
- [references/word-assembly-plan.md](references/word-assembly-plan.md)：在最终生成 `.docx` 之前如何确定准备情况和打包内容。
- [references/publishing-installation.md](references/publishing-installation.md)：如何打包、发布和安装此技能。
- [scripts/generate_docx_from_markdown.cjs](scripts/generate_docx_from_markdown.cjs)：根据 Markdown、交付概要和格式规范生成 `.docx` 文件。
- [docx-js.md](docx-js.md)：创建新的 `.docx` 文件的完整参考指南。
- [ooxml.md](ooxml.md)：编辑现有基于 OOXML 的 Word 文件的完整参考指南。

## 不可协商的规则

- 不要编造应来自源文档库的事实。
- 如果存在权威的来源，请不要将草稿文本作为主要来源。
- 除非任务纯粹是编辑性质的，否则在内容稳定之前不要进行 OOXML 级别的编辑。
- 请勿假设已安装了单独的 `.docx` 技能。请使用此技能中的捆绑资源。
- 在未确定格式规范之前，不要最终确定 Word 文档的格式。
- 在未解决交付细节问题之前，不要最终确定正式的 Word 文档格式。