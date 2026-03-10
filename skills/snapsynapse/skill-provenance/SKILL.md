---
name: skill-provenance
description: >
  **版本跟踪**  
  用于管理 Agent Skills 捆包及其相关文件在各个会话（session）、界面（surface）和平台（platform）之间的版本信息。该功能适用于以下场景：  
  - 创建、编辑或管理技能包（skill bundle）的版本信息；  
  - 验证技能包的完整性；  
  - 打包技能包；  
  - 将技能包交付给他人使用；  
  - 检查或更新 `MANIFEST.yaml`、`CHANGELOG.md` 文件；  
  - 确保技能包的版本信息与文件名保持一致（而非依赖文件名来识别版本）。  
  该功能兼容 agentskills.io 开放标准（open standard）。
metadata:
  author: Snap Synapse (snapsynapse.com)
  source: https://github.com/snapsynapse/skill-provenance
---
# 技能来源管理（Skill Provenance）

## 该方案解决的问题

在技能使用过程中，文件会在不同的会话、界面（如聊天、集成开发环境（IDE）、命令行界面（CLI）、协作工具（如Claude、Gemini CLI、Codex、Copilot）以及本地存储（如Obsidian、工作目录、git仓库）之间传输。当版本信息仅依赖于文件名时，版本信息容易丢失。例如，将文件从`SKILL_v4.md`重命名为`SKILL_v5.md`，但如果没有内部记录更改内容，就会导致版本混淆。

本方案通过以下三个规范来避免这一问题：

1. 在文件格式允许的情况下，将版本信息存储在文件内部，并始终在`MANIFEST.yaml` manifest文件中记录。
2. 最新的变更日志会随技能包一起传输，而更详细的版本历史记录可以存储在源代码仓库中。
3. `MANIFEST.yaml`会列出技能包中的所有文件，以便任何会话都能验证文件的完整性。

## 需要版本控制的对象

技能包包括`SKILL.md`文件及其所有关联文件。典型的文件内容包括：
- `SKILL.md`（技能定义文件）
- `evals.json`（评估脚本文件）
- 生成脚本（如`generate.js`、`generate.py`）
- 由评估脚本或实际使用生成的输出文件（如`.docx`、`.pdf`）
- 交接说明（handoff notes）
- 用户提供的源代码材料（被跟踪但不进行版本控制）

`SKILL.md`文件和`evals.json`文件是主要的版本控制对象。生成脚本和输出文件由`MANIFEST.yaml`跟踪版本，但它们的版本与技能包版本一致，而不是单独版本控制。交接说明文件是可选的辅助文件。

## 内部版本头部信息

可以安全地添加YAML前言的文件应以YAML前言块开头（或扩展现有的YAML前言块），其中包含以下字段：

### 规范

- **version**：用于跟踪每个文件的修订次数。它表示该文件在技能包内的修订次数。技能包级别的版本（`bundle_version`）使用semver格式。
- **change_summary**：从v1版本开始必须包含。内容为1到3句话，用于描述具体发生了哪些更改，而不仅仅是说明有更改。
- **previous_version**：用于记录版本演变过程，任何会话都可以通过这个字段追溯版本历史。
- **file_role**：表示文件的类型，例如：
  - `skill`：`SKILL.md`文件本身
  - `evals`：`evals.json`文件
  - `script`：生成脚本或辅助脚本
  - `output`：渲染后的输出文件（如`.docx`、`.pdf`）
  - `handoff`：交接说明文件
  - `source`：用户提供的源代码材料（被跟踪但不进行版本控制）
  - `reference`：参考文档或按需加载的文档
  - `asset`：资产中的模板、图片、字体等，用于输出
  - `agents`：平台UI元数据（例如Claude的`agents/openai.yaml`）

对于无法安全添加YAML前言的文件（如二进制文件或格式严格的文件，如`.json`、`.sh`），`MANIFEST.yaml`会记录它们的版本信息，`version`字段具有权威性。

**`SKILL.md`文件的前言规范**：根据agentskills.io标准，必须包含`name`和`description`字段。不同平台可能对其他字段有不同的要求：

| 平台 | 允许的`SKILL.md`前言字段 |
|---|---|
| **agentskills.io** | `name`, `description`, `license`, `metadata`, `compatibility`, `allowed-tools` |
| **Claude Chat / Settings UI** | 与agentskills.io规范相同。Claude的设置导入器会拒绝识别不到的字段。 |
| **Claude Code** | 规范字段加上额外字段：`disable-model-invocation`, `user-invocable`, `context`, `agent`, `model`, `hooks`, `argument-hint`。这些是Claude Code特有的字段，不属于标准规范。 |
| **Claude API** | 通过 `/v1/skills`上传的技能文件。验证`name`和`description`字段，并支持`metadata`字段。 |
| **Gemini CLI (Google)** | 仅要求`name`和`description`字段。不支持额外字段。 |
| **Codex (OpenAI)** | 仅要求`name`和`description`字段。不接受额外字段。 |
| **GitHub Copilot / VS Code** | 遵循agentskills.io规范。 |
| **Cursor, Roo Code, Junie, 其他** | 遵循agentskills.io规范。具体支持的平台列表请参见agentskills.io（超过30个）。 |

为了最大程度地保持兼容性，建议`SKILL.md`的前言仅包含`name`和`description`字段。如果需要为技能包添加元数据，可以使用`metadata`字段，并为特定平台生成简化的版本信息。

### 注意事项（针对Codex或其他严格要求的平台）

如果目标平台是Codex或其他对元数据有严格要求的环境，应完全省略`SKILL.md`中的`metadata`字段。无论如何，`MANIFEST.yaml`都会记录`SKILL.md`的版本信息，因此不会丢失版本信息。

**关于规范支持的说明**：agentskills.io规范正式支持将`metadata`作为键值对存储，其中`version`字段是一个示例用法。这意味着`metadata.version`是一种被官方认可的格式，但并非Claude平台独有的扩展。不过，这里的`version`字段仅用于显示版本信息，并不用于跟踪版本变更或验证文件完整性。建议优先使用`MANIFEST.yaml`进行版本控制。

## `MANIFEST.yaml`文件

`MANIFEST.yaml`是一个YAML文件，位于技能包目录的根目录中，与`SKILL.md`处于同一层级。当技能包被打包成`.skill` ZIP文件时，`MANIFEST.yaml`会包含在ZIP文件内部。它是描述技能包内容的唯一权威来源。

### 规范

- **bundle_version**使用semver格式（MAJOR.MINOR.PATCH）：`MAJOR`表示对技能模型或接口的重大更改，`MINOR`表示新增功能或能力，`PATCH`表示修复和文档更新。
- **hash**是文件内容的sha256哈希值。新会话通过这个哈希值来验证收到的文件是否与`MANIFEST.yaml`中记录的内容一致。保存文件时计算哈希值，加载文件时进行验证。
- **deployments`（可选）：用于记录已部署或安装的技能包副本，以便在不同界面之间进行追踪。请确保`bundle_version`作为版本信息的权威来源。平台自带的版本信息（如API时间戳）存储在`deployments`中，而不是`bundle_version`中。
- 对于源代码文件，`version`字段设置为`null`。这些文件虽然会被跟踪，但不进行版本控制。
- 文件路径是相对于技能包根目录的相对路径，不允许使用绝对路径。
- `MANIFEST.yaml`不会被包含在`files`列表中。`MANIFEST.yaml`的哈希计算是递归进行的。可以将`MANIFEST.yaml`视为技能包的控制文件，并通过git、传输校验和或外部包来验证其完整性。

## `.skill`包格式

Claude的设置界面将技能导出和导入为`.skill`文件格式。这些文件是标准的ZIP压缩包，其中包含一个以技能名称命名的目录。版本控制相关的文件（`MANIFEST.yaml`、`CHANGELOG.md`、`README.md`）位于与该目录同一层级。

Claude的设置导入器只检查`SKILL.md`文件及其预期的目录结构，忽略无法识别的文件。这意味着版本控制文件可以安全地包含在`.skill` ZIP文件中，而不会影响导入/导出操作。

在初始化或更新技能包时，务必将版本控制文件包含在`.skill` ZIP文件中，以确保它们在通过Claude设置界面时不会丢失。

某些上传工具只接受`.zip`或`.md`格式的文件。在这种情况下，只需将文件名从`.skill`更改为`.zip`，无需更改文件内容。

规范建议将`SKILL.md`文件保持在500行以内，并将详细的参考资料放在单独的文件中。版本控制文件（`MANIFEST.yaml`、`CHANGELOG.md`）属于按需加载的资源，不需要每次都加载。

Claude Code提供了一个名为`CLAUDE_SKILL_DIR`的变量，用于表示相对于技能包的路径。其他平台可能没有这个变量。在当前工作目录为技能包根目录的情况下，可以直接使用相对路径（如`./validate.sh`）。

`.skill` ZIP文件仅包含技能定义及其相关参考资料。技能包还可以跟踪生成脚本、输出文件和交接说明文件。`MANIFEST.yaml`文件仍包含完整的文件清单。

## 变更日志（ChangeLog）

`CHANGELOG.md`文件位于技能包目录的根目录中，与`SKILL.md`和`MANIFEST.yaml`位于同一层级。它记录了技能包的最新变更历史，最新条目位于文件顶部。如果技能的官方源代码存储在git仓库中，较旧的变更记录可以存放在仓库级别的变更日志文件中。

### 规范

- 每条变更记录都会列出所有发生更改的文件及其更改内容。
- 如果`SKILL.md`文件发生了更改，但`evals.json`文件没有更新，变更日志会明确指出这一点，以避免版本混淆。
- 变更日志中的内容由人工编写，而不是自动生成的差异对比结果。其目的是清晰地传达变更意图，而不是列出每一行的具体更改内容。当技能包存储在git仓库中时，也可以查看Git中的差异对比结果。
- 变更日志可以适当压缩。如果源代码仓库维护了完整的追加式变更日志，可以在技能包中保留最近5-15条记录。

## 会话协议

### 打开会话

当一个技能包被加载到新会话中时：
1. 首先读取`MANIFEST.yaml`文件。
2. 确认所有列出的文件都存在。如果缺少文件，请报告。
3. 对于包含哈希值的文件，验证哈希值是否匹配。在本地环境中，用户可以在上传前运行`validate.sh`命令进行哈希值验证（无需依赖大型语言模型LLM）。
4. 读取`CHANGELOG.md`文件以了解最近的变更情况。
5. 检查文件的版本是否过时：如果某个文件的版本低于技能包的版本，或者`deployments`中显示的版本与本地版本不同，请标记该文件并询问用户是否需要更新。
6. 如果`MANIFEST.yaml`文件缺失，视为未进行版本控制的技能包。可以通过列出文件并询问用户版本信息来创建`MANIFEST.yaml`文件。

### 保存/关闭会话

当工作完成并准备交付文件时：
1. 为所有使用这些文件的文件更新内部版本信息。
2. 使用新的版本号和哈希值更新`MANIFEST.yaml`文件。
3. 在`CHANGELOG.md`文件中添加新的条目。
4. 如果有版本控制的文件发生了更改，但相关文件没有更新（例如`SKILL.md`更改了但`evals.json`未更新），请在变更日志中明确标注文件的过时情况。
5. 将完整的技能包交付给用户，或者至少交付更改后的文件以及更新后的`MANIFEST.yaml`和`CHANGELOG.md`文件。
6. 如果用户表示技能包需要上传到git仓库，请提供基于变更日志生成的提交信息。

### 会话间的交接

交接说明文件用于记录当前会话的工作状态，应包含以下内容：
- 当前技能包的版本信息
- 本次会话完成的工作内容
- 需要处理的过时文件
- 下一次会话应首先执行的任务
- 任何尚未反映在文件中的决策
- 每个文件的变更摘要：对于本次会话中修改的每个文件，简要说明更改的内容（如添加了哪些部分、删除了哪些字段、修改了哪些逻辑等）。这比变更日志更详细，有助于下一次会话直接验证工作内容。

仅在跨越非持久性环境或用户明确要求时创建交接说明文件。在具有当前`MANIFEST.yaml`、变更日志和git历史记录的文件系统中，通常不需要创建交接说明文件。创建交接说明文件后，旧的交接记录会保存在变更日志中。

### 冲突解决

当会话中发现版本冲突时（例如，某个文件声称版本为v5，但`MANIFEST.yaml`显示为v4，或者两个文件声称的版本不同）：
1. 向用户展示具体的冲突情况。
2. 通过`change_summary`字段显示每个版本的变更内容。
3. 默认建议：信任最新的`version_date`。
4. 在继续操作之前，始终请求用户的明确确认。

切勿自动解决版本冲突。这个系统的核心目的是让版本冲突显而易见。

## 跨界面和跨平台的注意事项

一个技能包会经历三种状态：
- **官方源代码包**：存储在git仓库或本地存储中的版本。这里的`MANIFEST.yaml`和`CHANGELOG.md`是最权威的版本信息来源。如果维护了完整的仓库备份，请将其存储在仓库根目录或仓库级别的其他路径中。
- **适用于特定平台的安装版本**：为Codex、Gemini CLI等工具生成的版本。这些工具可能只接受`name`和`description`字段，因此需要从`SKILL.md`文件中删除`metadata`字段，将`frontmatter_mode`设置为`minimal`，重新计算这些文件的哈希值，并保持原始技能包不变（除非有意推广该版本）。
- **注册表或分发包**：如`.skill` ZIP文件或通过ClawHub上传的文件。这些文件可能不包含开发用的文件，但其`MANIFEST.yaml`必须准确描述文件内容。只有在实际发布、重新安装或重新部署后，才更新`deployments`字段。

### 不同平台的注意事项：
- **Claude Chat**：无状态的上传/下载机制。打开文件时进行验证，并生成交接说明文件。
- **Claude Cowork / Claude Code / Claude Agent SDK**：文件会保存在持久化的文件系统中，`MANIFEST.yaml`和变更日志会随技能包一起保存。
- **Claude API**：部署版本存储在`deployments`字段中，而不是`bundle_version`字段中。
- **其他agentskills客户端**：未知文件会被安全忽略。`.agents/skills/`目录可以作为中立的安装路径。

总体原则是：`MANIFEST.yaml`和变更日志始终具有权威性，而经过转换的安装或分发版本只是从官方源代码包派生出来的文件，不能直接修改原始文件。

## 信任与审计

使用`MANIFEST.yaml`、变更日志、哈希值以及可选的部署元数据来验证技能包的内容是否正确、文件是否与其记录的状态一致、哪些文件已更新或已部署的文件是否过时。如果技能包来自不可信的来源，请先进行验证。

## 文件命名规则

版本控制的文件应使用不含版本号的稳定名称：
- `SKILL.md`（而不是`SKILL_v5.md`）
- `evals.json`（而不是`evals_v3.json`）
- `generate.js`（而不是`generate-v4.js`）

版本信息存储在文件内部（通过文件头信息）和`MANIFEST.yaml`文件中，而不是文件名中。使用版本号作为文件名会导致版本管理问题。

**例外情况**：如果用户的本地存储环境要求文件名中包含版本号，请以`MANIFEST.yaml`中的信息作为判断标准来确定哪个版本是官方版本。无论如何，文件内部的版本信息必须保持一致。

## 初始化未版本控制的技能包

要为现有的未版本控制的技能包添加版本控制：
1. 列出所有存在的文件——可以通过读取目录结构或上传的文件列表来确定文件列表。不要让用户手动列出文件。
2. 询问用户希望使用的版本号。如果有交接说明或其他参考信息，可以根据历史记录建议一个版本号。
3. 为可以添加版本信息的文件添加内部版本头部信息，并为格式严格的文件记录仅包含在`MANIFEST.yaml`中的版本信息。
4. 生成包含哈希值的`MANIFEST.yaml`文件。
5. 创建`CHANGELOG.md`文件，总结已知的版本历史。
6. 将版本控制的技能包交付给用户。

此操作针对每个技能包只进行一次。

## 开发者信息

该方案由Snap Synapse开发。官方源代码仓库地址：https://github.com/snapsynapse/skill-provenance