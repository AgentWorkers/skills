---
name: skill-creator
description: "**创建高效技能的指南：**  
本指南旨在帮助您利用专业知识、工作流程或工具集成来扩展代理的功能。当用户提出以下需求时，请参考本指南：  
(1) 创建新技能；  
(2) 构建技能；  
(3) 设置技能参数；  
(4) 初始化技能；  
(5) 搭建技能框架；  
(6) 更新或修改现有技能；  
(7) 验证技能的有效性；  
(8) 了解技能的结构；  
(9) 理解技能的运作原理；  
(10) 获取技能设计模式的指导。  
**触发条件：**  
当用户使用以下短语时，本指南将自动被触发：  
“创建一个技能”（Create a skill）、  
“新技能”（New skill）、  
“构建某个技能”（Build a skill for X）、  
“如何创建技能”（How do I create a skill）、  
“帮助我构建一个技能”（Help me build a skill）。"
---
# 技能创建器

本文档提供了关于如何创建高效技能的指导。

## 关于技能

技能是模块化、自包含的包，通过提供专门的知识、工作流程和工具来扩展代理的功能。可以将它们视为针对特定领域或任务的“入门指南”——它们将一个通用代理转变为具备程序性知识和领域专业知识的专用代理。

### Deepagents中的技能存储位置

在deepagents CLI中，技能存储在`~/.deepagents/<agent>/skills/`目录下，其中`<agent>`是你的代理配置名称（默认值为`agent`）。例如，在默认配置下，技能文件位于：

```
~/.deepagents/agent/skills/
├── skill-name-1/
│   └── SKILL.md
├── skill-name-2/
│   └── SKILL.md
└── ...
```

### 技能提供的内容

1. **专门的工作流程**：针对特定领域的多步骤程序
2. **工具集成**：使用特定文件格式或API的说明
3. **领域专业知识**：公司特定的知识、模式和业务逻辑
4. **捆绑资源**：用于复杂和重复性任务的脚本、参考资料和资产

## 核心原则

### 简洁是关键

上下文窗口是一种公共资源。技能会与代理所需的其他所有内容共享上下文窗口：系统提示、对话历史记录、其他技能的元数据以及实际的用户请求。

**默认假设：代理已经具备很强的能力。** 仅添加代理尚未拥有的上下文信息。对于每条信息都要问自己：“代理真的需要这个解释吗？”以及“这一段内容是否值得消耗相应的资源（即令牌）？”

优先使用简洁的示例，而非冗长的解释。

### 设置适当的自由度

根据任务的复杂性和可变性来匹配自由度的级别：

- **高自由度（基于文本的指令）**：当存在多种方法、决策取决于上下文或需要使用启发式方法时使用。
- **中等自由度（带参数的伪代码或脚本）**：当存在首选模式、允许某些变化或配置会影响行为时使用。
- **低自由度（特定脚本，参数较少）**：当操作容易出错、一致性至关重要或必须遵循特定顺序时使用。

可以将代理想象成在探索一条路径：狭窄的桥梁需要特定的护栏（低自由度），而开阔的田野则允许多种路径（高自由度）。

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

每个`SKILL.md`文件包含以下内容：

- **前置内容**（YAML格式）：包含`name`和`description`字段。这些字段是代理判断何时使用该技能的唯一依据，因此描述技能的内容及其使用场景时必须清晰全面。
- **正文**（Markdown格式）：使用技能的说明和指导。这些内容仅在技能被触发后才会加载（如果被触发的话）。

#### 拼绑资源（可选）

##### 脚本（`scripts/`）

用于需要确定性可靠性的任务的可执行代码（Python/Bash等）。

- **包含时机**：当相同的代码需要反复编写或需要确定性可靠性时。
- **示例**：`scripts/rotate_pdf.py`用于PDF旋转任务
- **优点**：节省资源（令牌），具有确定性，无需加载到上下文中即可执行
- **注意**：脚本可能仍需要被代理读取以进行修补或根据环境进行调整

##### 参考资料（`references/`）

旨在根据需要加载到上下文中以指导代理操作的文档和参考资料。

- **包含时机**：当代理在执行任务时需要参考这些资料时。
- **示例**：`references/finance.md`用于财务模式，`references/mnda.md`用于公司NDA模板，`references/policies.md`用于公司政策，`references/api_docs.md`用于API规范
- **用途**：数据库模式、API文档、领域知识、公司政策、详细的工作流程指南
- **优点**：保持`SKILL.md`文件简洁，仅在代理需要时才加载
- **最佳实践**：如果文件较大（超过10,000字），在`SKILL.md`中包含搜索路径
- **避免重复**：信息应仅存在于`SKILL.md`或参考资料文件中，不要同时存在于两者中。除非信息对技能至关重要，否则建议将详细信息放在参考资料文件中——这样既能保持`SKILL.md`的简洁性，又能方便用户查找。仅在`SKILL.md`中保留必要的程序性指令和工作流程指导；将详细的参考资料、模式和示例移到参考资料文件中。

##### 资产（`assets/`）

这些文件不打算加载到上下文中，而是用于代理生成的输出中。

- **包含时机**：当技能需要最终输出中使用的文件时。
- **示例**：`assets/logo.png`用于品牌资产，`assets/slides.pptx`用于PowerPoint模板，`assets/frontend-template/`用于HTML/React模板代码，`assets/font.ttf`用于字体
- **用途**：模板、图片、图标、模板代码、示例文档等，这些文件会被复制或修改
- **优点**：将输出资源与文档分离，使代理能够在不加载到上下文中的情况下使用这些文件

#### 技能中不应包含的内容

技能应仅包含直接支持其功能的必要文件。不要创建额外的文档或辅助文件，例如：

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- 等

技能应仅包含AI代理完成任务所需的信息。不应包含关于创建过程、设置和测试程序、面向用户的文档等辅助信息。创建额外的文档文件只会增加混乱。

### 渐进式披露设计原则

技能使用三级加载系统来高效管理上下文：

1. **元数据（名称 + 描述）**：始终包含在上下文中（约100个单词）
2. **SKILL.md正文**：在技能被触发时加载（不超过5,000个单词）
3. **捆绑资源**：根据代理的需求加载（数量不限，因为脚本可以在不加载到上下文窗口的情况下执行）

#### 渐进式披露模式

保持`SKILL.md`正文简洁，不超过500行，以减少上下文冗余。当内容达到这个限制时，将其拆分为单独的文件。在将内容拆分到其他文件时，必须从`SKILL.md`中明确引用这些文件，并说明何时阅读它们，以确保读者知道它们的存在及其使用方法。

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

代理仅在需要时加载`FORMS.md`、`REFERENCE.md`或`EXAMPLES.md`。

**模式2：按领域组织内容**

对于涉及多个领域的技能，按领域组织内容，以避免加载无关的上下文：

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

当用户询问销售指标时，代理仅读取`sales.md`。

类似地，对于支持多种框架或变体的技能，按变体组织内容：

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

当用户选择AWS时，代理仅读取`aws.md`。

**模式3：条件性显示内容**

仅当用户需要高级功能时，才显示相关内容：

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

代理仅在用户需要`REDLINING.md`或`OOXML.md`时才读取这些文件。

**重要指南：**

- **避免深度嵌套的引用**：保持引用文件与`SKILL.md`只有一层嵌套关系。所有引用文件都应直接从`SKILL.md`中链接。
- **结构化较长的参考文件**：对于超过100行的文件，在顶部添加目录表，以便代理在预览时能够看到全部内容。

## 技能创建过程

技能创建包括以下步骤：

1. 通过具体示例理解技能
2. 规划可重用的技能内容（脚本、参考资料、资产）
3. 初始化技能（运行`init_skill.py`）
4. 编辑技能（实现资源并编写`SKILL.md`）
5. 验证技能（运行`quick_validate.py`）
6. 根据实际使用情况迭代

按照这些步骤进行，除非有明确的原因表明某些步骤不适用，否则请按顺序执行。

### 第1步：通过具体示例理解技能

只有当技能的使用模式已经非常清楚时，才可跳过此步骤。即使在使用现有技能时，这一步骤仍然很有价值。

要创建一个有效的技能，需要清楚地了解该技能的具体使用场景。这种理解可以通过直接的用户示例或经过用户反馈验证的生成示例来获得。

例如，在构建图像编辑器技能时，相关的问题包括：

- “图像编辑器技能应该支持哪些功能？编辑、旋转等功能吗？”
- “你能举一些使用该技能的例子吗？”
- “我可以想象用户会请求‘去除这张图片的红眼’或‘旋转这张图片’这样的操作。还有其他使用方式吗？”
- “用户会如何触发这个技能？”

为了避免让用户感到困惑，不要在一条消息中问太多问题。先提出最重要的问题，然后根据需要进一步询问以获得更好的效果。

当对技能应支持的功能有清晰的认识后，即可完成此步骤。

### 第2步：规划可重用的技能内容

要将具体示例转化为有效的技能，需要分析每个示例，包括：

- 考虑如何从头开始执行这些示例
- 确定在执行这些工作流程时哪些脚本、参考资料和资产会有帮助

例如，在构建`pdf-editor`技能以处理“帮我旋转这张PDF”这样的请求时，分析结果表明：

- 旋转PDF需要每次都重新编写代码
- 因此，`scripts/rotate_pdf.py`脚本会很有用

例如，在构建`frontend-webapp-builder`技能以处理“为我构建一个待办事项应用程序”或“为我构建一个跟踪步骤的仪表板”这样的请求时，分析结果表明：

- 每次构建前端Web应用程序都需要编写相同的HTML/React代码
- 因此，`assets/hello-world/`模板（包含HTML/React项目文件）会很有用

例如，在构建`big-query`技能以处理“今天有多少用户登录了”这样的请求时，分析结果表明：

- 每次查询BigQuery都需要重新发现表格结构和关系
- 因此，`references/schema.md`文件（记录表格结构）会很有用

为了确定技能的内容，需要分析每个具体示例，列出可重用的资源：脚本、参考资料和资产。

### 第3步：初始化技能

此时，就可以实际创建技能了。

只有当正在开发的技能已经存在并且需要迭代或打包时，才可跳过此步骤。在这种情况下，请继续执行下一步。

从头开始创建新技能时，务必运行`init_skill.py`脚本。该脚本会自动生成一个新的技能模板目录，其中包含技能所需的所有内容，从而使技能创建过程更加高效和可靠。

**使用方法：**

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

对于deepagents CLI，使用代理的技能目录：

```bash
scripts/init_skill.py <skill-name> --path ~/.deepagents/agent/skills
```

该脚本会：

- 在指定路径创建技能目录
- 生成带有正确前置内容和TODO占位符的`SKILL.md`模板
- 创建`scripts/`、`references/`和`assets/`示例资源目录
- 在每个目录中添加可自定义或删除的示例文件

初始化后，根据需要自定义或删除生成的`SKILL.md`和示例文件。

### 第4步：编辑技能

在编辑（新生成的或现有的）技能时，请记住，这些技能是为代理使用的。应包含对代理有帮助的信息，尤其是那些对代理来说不明显的信息。考虑哪些程序性知识、领域特定细节或可重用的资产可以帮助代理更有效地执行这些任务。

#### 学习经过验证的设计模式

根据你的技能需求，参考以下有用的指南：

- **多步骤流程**：查看`references/workflows.md`以获取顺序工作流程和条件逻辑
- **特定的输出格式或质量标准**：查看`references/output-patterns.md`以获取模板和示例模式

这些文件包含了有效技能设计的最佳实践。

#### 从可重用的资源开始

开始实现时，先从上述的可重用资源开始：`scripts/`、`references/`和`assets/`文件。请注意，这一步可能需要用户输入。例如，在实现`brand-guidelines`技能时，用户可能需要提供品牌资产或存储在`assets/`中的模板，或提供存储在`references/`中的文档。

添加的脚本必须通过实际运行来测试，以确保没有错误并且输出符合预期。如果有很多类似的脚本，只需测试一个代表性的样本，以确保所有脚本都能正常工作，同时平衡完成时间。

任何不需要的示例文件和目录都应删除。初始化脚本会在`scripts/`、`references/`和`assets/`中创建示例文件以展示结构，但大多数技能并不需要所有这些文件。

#### 更新`SKILL.md`

**编写指南：** 始终使用祈使句/动名词形式。

##### 前置内容

使用YAML格式编写前置内容，包括`name`和`description`字段：

- `name`：技能名称
- `description`：这是触发技能的主要机制，有助于代理了解何时使用该技能。
  - 包括技能的功能以及具体的触发条件/使用场景。
  - 将所有“使用场景”信息放在这里——不要放在正文中。正文仅在技能被触发后才会加载，因此正文中的“何时使用此技能”部分对代理没有帮助。
  - 例如，`docx`技能的描述：“支持创建、编辑和分析文档的功能，包括跟踪更改、添加注释、格式保留和文本提取。适用于处理.docx格式的专业文档，用于：(1) 创建新文档，(2) 修改或编辑内容，(3) 处理跟踪更改，(4) 添加注释等”

不要在YAML前置内容中包含其他字段。

##### 正文

编写使用技能及其捆绑资源的说明。

### 第5步：验证技能

技能开发完成后，需要验证它是否满足所有要求：

```bash
scripts/quick_validate.py <path/to/skill-folder>
```

验证脚本会检查：

- YAML前置内容的格式和必需字段
- 技能命名规范（使用连字符-大写形式，最多64个字符）
- 描述的完整性（不含尖括号，最多1024个字符）
- 必需的字段：`name`和`description`
- 允许的前置内容属性：`name`、`description`、`license`、`allowed-tools`、`metadata`

如果验证失败，请修复报告的错误，然后再次运行验证命令。

### 第6步：迭代

测试技能后，用户可能会提出改进意见。通常这种情况会在使用技能后立即发生，因为用户会对技能的表现有新的了解。

**迭代流程：**

1. 在实际任务中使用技能
2. 发现困难或效率低下的地方
3. 确定`SKILL.md`或捆绑资源需要更新的内容
4. 实施更改并再次测试