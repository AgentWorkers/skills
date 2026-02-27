---
name: skill-creator
description: 创建或更新 AgentSkills。在通过脚本、参考资料和资产来设计、构建或打包技能时使用该功能。
---
# 技能创建者

本文档提供了关于如何创建高效技能的指导。

## 关于技能

技能是模块化、自包含的包，它们通过提供专业知识、工作流程和工具来扩展Codex的功能。可以将它们视为针对特定领域或任务的“入门指南”——它们将Codex从一个通用代理转变为一个具备程序化知识的专用代理，这种知识是任何模型都无法完全拥有的。

### 技能提供的内容

1. **专业的工作流程**：针对特定领域的多步骤程序。
2. **工具集成**：使用特定文件格式或API的说明。
3. **领域专业知识**：公司特定的知识、模式和业务逻辑。
4. **捆绑资源**：用于复杂和重复性任务的脚本、参考资料和资产。

## 核心原则

### 简洁是关键

上下文窗口是一种公共资源。技能会与Codex需要的所有内容共享上下文窗口：系统提示、对话历史记录、其他技能的元数据以及实际的用户请求。

**默认假设：Codex已经非常智能了。** 只添加Codex尚未拥有的上下文信息。对每条信息都要进行质疑：“Codex真的需要这个解释吗？”以及“这一段内容是否值得花费相应的资源？”
优先选择简洁的示例，而不是冗长的解释。

### 设置适当的自由度

根据任务的复杂性和变异性来匹配自由度的级别：

**高自由度（基于文本的指令）**：当存在多种方法时使用，决策取决于上下文，或者启发式方法可以指导操作时使用。
**中等自由度（带有参数的伪代码或脚本）**：当存在首选模式时使用，允许某些变化时使用，或者配置会影响行为时使用。
**低自由度（特定脚本，参数较少）**：当操作容易出错且一致性至关重要，或者必须遵循特定顺序时使用。

将Codex想象成在探索一条路径：狭窄的桥梁需要特定的护栏（低自由度），而开阔的田野则允许多种路径（高自由度）。

### 技能的构成

每个技能都包含一个必需的`SKILL.md`文件和可选的捆绑资源：

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md（必需）

每个`SKILL.md`文件包含：

- **前端内容**（YAML）：包含`name`和`description`字段。这些是Codex用来判断何时使用该技能的唯一字段，因此清晰且全面地描述技能的功能及其使用场景非常重要。
- **正文**（Markdown）：使用该技能的说明和指导。只有在技能被触发后（如果有的话）才会加载。

#### 拼绑资源（可选）

##### 脚本（`scripts/`）

用于需要确定性可靠性的任务的可执行代码（Python/Bash等）。

- **何时包含**：当相同的代码需要被反复编写或需要确定性可靠性时。
- **示例**：`scripts/rotate_pdf.py`用于PDF旋转任务。
- **优点**：节省资源，结果可预测，无需加载到上下文中即可执行。
- **注意**：脚本可能仍需要被Codex读取以进行修补或根据环境进行调整。

##### 参考资料（`references/`）

旨在根据需要加载到上下文中以指导Codex处理的文档和参考材料。

- **何时包含**：当Codex在工作时需要参考这些资料时。
- **示例**：`references/finance.md`用于财务模式，`references/mnda.md`用于公司NDA模板，`references/policies.md`用于公司政策，`references/api_docs.md`用于API规范。
- **使用场景**：数据库模式、API文档、领域知识、公司政策、详细的工作流程指南。
- **优点**：保持`SKILL.md`文件简洁，仅在Codex需要时才加载。
- **最佳实践**：如果文件较大（超过10,000字），在`SKILL.md`中包含grep搜索模式。
- **避免重复**：信息应仅存在于`SKILL.md`或参考资料文件中，不要同时存在于两者中。除非信息对技能至关重要，否则将详细信息放在参考资料文件中——这样可以保持`SKILL.md`的简洁性，同时便于查找信息，而不会占用过多的上下文窗口空间。仅在`SKILL.md`中保留必要的程序性指令和工作流程指导；将详细的参考资料、模式和示例移到参考资料文件中。

##### 资产（`assets/`）

这些文件不打算加载到上下文中，而是用于生成Codex的输出中。

- **何时包含**：当技能需要最终输出中使用的文件时。
- **示例**：`assets/logo.png`用于品牌资产，`assets/slides.pptx`用于PowerPoint模板，`assets/frontend-template/`用于HTML/React样板代码，`assets/font.ttf`用于字体。
- **使用场景**：模板、图片、图标、样板代码、需要复制或修改的示例文档。
- **优点**：将输出资源与文档分离，使Codex能够在不加载到上下文中的情况下使用这些文件。

#### 技能中不应包含的内容

技能应仅包含直接支持其功能的必要文件。不要创建额外的文档或辅助文件，包括：

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- 等。

技能应仅包含AI代理完成任务所需的信息。它不应包含关于创建过程、设置和测试程序、面向用户的文档等辅助信息。创建额外的文档文件只会增加混乱。

### 渐进式披露设计原则

技能使用三级加载系统来高效管理上下文：

1. **元数据（名称 + 描述）** - 始终在上下文中提供（约100个单词）。
2. **SKILL.md正文** - 当技能被触发时（少于5,000个单词）。
3. **捆绑资源** - 根据Codex的需要加载（无限，因为脚本可以在不加载到上下文窗口的情况下执行）。

#### 渐进式披露模式

保持`SKILL.md`正文简洁，不超过500行，以减少上下文冗余。当内容接近这个限制时，将其分割到单独的文件中。在将内容分割到其他文件时，非常重要的是要在`SKILL.md`中引用这些文件，并清楚地说明何时阅读它们，以确保技能的读者知道它们的存在及其使用方法。

**关键原则：** 当技能支持多种变体、框架或选项时，仅在`SKILL.md`中保留核心工作流程和选择指导。将特定于变体的细节（模式、示例、配置）移到单独的参考资料文件中。

**模式1：带有参考资料的高级指南**

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

Codex仅在需要时加载`FORMS.md`、`REFERENCE.md`或`EXAMPLES.md`。

**模式2：按领域组织**

对于具有多个领域的技能，按领域组织内容，以避免加载无关的上下文：

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

当用户询问销售指标时，Codex仅读取`sales.md`。

类似地，对于支持多种框架或变体的技能，按变体组织内容：

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

当用户选择AWS时，Codex仅读取`aws.md`。

**模式3：条件性细节**

显示基本内容，并链接到高级内容：

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

只有当用户需要这些功能时，Codex才会读取`REDLINING.md`或`OOXML.md`。

**重要指南：**

- **避免深度嵌套的引用** - 保持引用文件与`SKILL.md`只有一层嵌套。所有参考文件都应直接从`SKILL.md`链接。
- **结构化较长的参考文件**：对于超过100行的文件，在顶部包含目录表，以便Codex在预览时可以看到全部内容。

## 技能创建过程

技能创建包括以下步骤：

1. 通过具体示例理解技能。
2. 规划可重用的技能内容（脚本、参考资料、资产）。
3. 初始化技能（运行`init_skill.py`）。
4. 编辑技能（实现资源并编写`SKILL.md`）。
5. 打包技能（运行`package_skill.py`）。
6. 根据实际使用情况迭代。

按照这些步骤进行，除非有明确的理由不适用于某些步骤。

### 技能命名

- 仅使用小写字母、数字和连字符；将用户提供的标题规范化为连字符-大小写形式（例如，“Plan Mode” -> `plan-mode`）。
- 在生成名称时，确保名称长度不超过64个字符（字母、数字、连字符）。
- 优先选择描述动作的简短动词短语。
- 如果工具名称能提高清晰度或触发效果，请使用该工具作为命名前缀（例如，`gh-address-comments`、`linear-address-issue`）。
- 将技能文件夹的名称与技能名称完全一致。

### 第1步：通过具体示例理解技能

只有当技能的使用模式已经明确时，才能跳过此步骤。即使是在处理现有技能时，这一步也是有价值的。

要创建一个有效的技能，需要清楚地了解该技能的具体使用场景。这种理解可以通过直接的用户示例或经过用户反馈验证的生成示例来获得。

例如，在构建图像编辑器技能时，相关的问题包括：

- “图像编辑器技能应该支持哪些功能？编辑、旋转，还是其他功能？”
- “你能举一些使用这个技能的例子吗？”
- “我可以想象用户会请求‘去除这张图片的红眼’或‘旋转这张图片’这样的操作。还有其他使用方式吗？”
- “用户会如何触发这个技能？”

为了避免让用户感到困惑，不要在一条消息中问太多问题。先提出最重要的问题，然后根据需要进一步询问。

当对技能应支持的功能有清晰的认识后，就可以完成这一步。

### 第2步：规划可重用的技能内容

要将具体示例转化为有效的技能，需要分析每个示例，包括：

1. 考虑如何从头开始执行该示例。
2. 确定在执行这些工作流程时哪些脚本、参考资料和资产会有帮助。

示例：在构建`pdf-editor`技能以处理“帮我旋转这张PDF”这样的请求时，分析显示：

- 旋转PDF每次都需要重写相同的代码。
- `scripts/rotate_pdf.py`脚本对于存储在技能中会很有帮助。

示例：在构建`frontend-webapp-builder`技能以处理“为我构建一个待办事项应用”或“为我构建一个跟踪步骤的仪表板”这样的请求时，分析显示：

- 每次构建前端Web应用都需要编写相同的样板HTML/React代码。
- `assets/hello-world/`模板中包含的样板HTML/React项目文件对于存储在技能中会很有帮助。

示例：在构建`big-query`技能以处理“今天有多少用户登录了”这样的请求时，分析显示：

- 每次查询BigQuery都需要重新发现表格模式和关系。
- `references/schema.md`文件中记录的表格模式对于存储在技能中会很有帮助。

为了确定技能的内容，需要分析每个具体示例，列出需要包含的可重用资源：脚本、参考资料和资产。

### 第3步：初始化技能

此时，是实际创建技能的时候了。

只有当正在开发的技能已经存在，并且需要迭代或打包时，才能跳过此步骤。在这种情况下，继续进行下一步。

从零开始创建新技能时，始终运行`init_skill.py`脚本。该脚本会自动生成一个新的技能模板目录，其中包含技能所需的所有内容，使技能创建过程更加高效和可靠。

**使用方法：**

```bash
scripts/init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets] [--examples]
```

**示例：**

```bash
scripts/init_skill.py my-skill --path skills/public
scripts/init_skill.py my-skill --path skills/public --resources scripts,references
scripts/init_skill.py my-skill --path skills/public --resources scripts --examples
```

脚本：

- 在指定路径创建技能目录。
- 生成带有正确前端内容和TODO占位符的`SKILL.md`模板。
- 根据`--resources`参数可选地创建资源目录。
- 如果设置了`--examples`参数，还可以创建示例文件。

初始化后，根据需要自定义`SKILL.md`并添加资源。如果使用了`--examples`参数，请替换或删除占位符文件。

### 第4步：编辑技能

在编辑（新生成的或现有的）技能时，请记住，该技能是为另一个Codex实例创建的。包含对另一个Codex实例有帮助且不显而易见的信息。考虑哪些程序性知识、领域特定细节或可重用的资产可以帮助另一个Codex实例更有效地执行这些任务。

#### 学习经过验证的设计模式

根据你的技能需求，参考以下有用的指南：

- **多步骤流程**：参见`references/workflows.md`以获取顺序工作流程和条件逻辑。
- **特定的输出格式或质量标准**：参见`references/output-patterns.md`以获取模板和示例模式。

这些文件包含了有效技能设计的最佳实践。

#### 从可重用的技能内容开始

开始实现时，先从上述的可重用资源开始：`scripts/`、`references/`和`assets/`文件。请注意，这一步可能需要用户输入。例如，在实现`brand-guidelines`技能时，用户可能需要提供品牌资产或存储在`assets/`中的模板，或者提供存储在`references/`中的文档。

添加的脚本必须通过实际运行来测试，以确保没有错误，并且输出符合预期。如果有许多类似的脚本，只需测试一个代表性的样本，以确保它们都能正常工作，同时平衡完成时间。

如果你使用了`--examples`参数，请删除不需要的占位符文件。只创建实际需要的资源目录。

#### 更新`SKILL.md`

**编写指南：** 始终使用祈使式/不定式形式。

##### 前端内容

使用YAML编写前端内容，包括`name`和`description`：

- `name`：技能名称。
- `description`：这是触发技能的主要机制，有助于Codex了解何时使用该技能。
  - 包括技能的功能以及具体的触发条件/使用场景。
  - 在这里包含所有“何时使用”的信息——不要放在正文中。正文仅在技能被触发后加载，因此正文中的“何时使用此技能”部分对Codex没有帮助。
  - 例如`docx`技能的描述：“全面的文档创建、编辑和分析功能，支持跟踪更改、添加注释、格式保留和文本提取。当Codex需要处理专业文档（.docx文件）时使用，例如：(1) 创建新文档，(2) 修改或编辑内容，(3) 处理跟踪更改，(4) 添加注释，或任何其他文档任务。”

不要在YAML前端内容中包含其他字段。

##### 正文

编写使用技能及其捆绑资源的说明。

### 第5步：打包技能

一旦技能开发完成，就必须将其打包成一个可分发的 `.skill` 文件并与用户共享。打包过程会自动验证技能，确保其满足所有要求：

```bash
scripts/package_skill.py <path/to/skill-folder>
```

**可选的输出目录规范：**

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

打包脚本将：

1. **自动验证** 技能，检查：
   - YAML前端内容的格式和所需字段。
   - 技能命名规范和目录结构。
   - 描述的完整性和质量。
   - 文件组织和资源引用。

2. **如果验证通过，** 将技能打包成一个以技能名称命名的`.skill`文件（例如，`my-skill.skill`），其中包含所有文件并保持正确的目录结构以供分发。.skill文件是一个带有 `.skill` 扩展名的压缩文件。

   安全限制：如果存在符号链接，打包将失败。如果验证失败，脚本将报告错误并退出，不会创建包。

### 第6步：迭代

在测试技能后，用户可能会提出改进意见。这通常发生在使用技能之后，因为他们有了关于技能表现的最新信息。

**迭代工作流程：**

1. 在实际任务中使用技能。
2. 注意遇到的困难或效率低下的地方。
3. 确定`SKILL.md`或捆绑资源应该如何更新。
4. 实施更改并再次测试。