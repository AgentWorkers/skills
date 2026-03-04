---
name: skill-build-helper
description: 创建或优化一个 OpenClaw 技能。适用于用户需要构建新技能、改进现有技能、审阅 SKILL.md 文件，或为在 ClawHub 上发布技能做准备的情况。
metadata: {"openclaw":{"requires":{"bins":["jq"]}}}
---
# 技能构建器（Skill Builder）

这是一个用于创建和优化 OpenClaw 技能的元技能（meta-skill），遵循官方的最佳实践。它指导您完成从确定技能需求到发布完成的全过程。

## 工作流程

### 1. 理解需求

确定技能的创建或优化模式：

| 模式 | 触发条件 |
|------|---------|
| **创建** | 用户希望创建一个新的技能 |
| **优化** | 用户希望改进或审查现有的技能 |

**如果需要创建新技能**：请用户提供 2-3 个具体的使用示例（他们会如何触发这个技能，以及技能应该执行哪些操作）。这些示例将用于指导技能的描述和流程设计。

**如果需要优化现有技能**：在继续之前，请阅读现有的 `SKILL.md` 文件并了解其当前的结构。

### 2. 创建技能目录

在 `~/workspace/skills/` 目录下创建相应的技能目录：

```
<skill-name>/
├── SKILL.md          (required — agent instructions)
├── README.md         (recommended for published skills)
├── scripts/          (if deterministic code is needed)
└── references/       (if large docs needed on-demand)
```

**命名规则**：
- 仅使用小写字母和连字符（禁止使用下划线或空格）
- 名称长度不超过 64 个字符
- 尽量以动词开头（例如：`workout-track`、`skill-builder`）
- 目录名称必须与 `frontmatter` 文件中的 `name` 字段完全匹配

### 3. 编写 `SKILL.md` 文件

`SKILL.md` 是核心文件，其中包含了代理执行该技能所需的指令。

#### `frontmatter`（YAML 格式）

包含三个字段：

```yaml
---
name: <skill-name>
description: <what it does>. Use when <trigger context>.
metadata: {"openclaw":{"requires":{"bins":["list","of","binaries"]}}}
---
```

- **`name`：名称必须与目录名称完全匹配 |
- **`description`：技能的主要使用场景或触发条件。请包含 “Use when...” 语句，以帮助代理判断何时激活该技能。描述应具有唯一性，避免与其他技能重复 |
- **`metadata`：声明运行时所需的依赖项。如有需要，可参考 `{baseDir}/references/frontmatter-spec.md` 文件以获取完整说明 |

#### 正文结构

按照以下规则编写正文内容：
1. **开头行**：用一句话说明该技能的功能。
2. **## 工作流程**：使用编号的 H3 标题列出各个步骤（例如：`### 1. 确定需求`）。
3. **表格**：用于展示结构化数据（如需要提取的字段、标志、映射关系等）。
4. **代码块**：使用 `exec` 工具的 JSON 格式编写具体的命令。
   ```json
   {
     "tool": "exec",
     "command": "<shell command here>"
   }
   ```
5. ****示例**：提供至少 3 行的输入/输出示例。
6. **错误处理**：明确说明在遇到问题时应如何处理错误——切勿默默重试。

#### 关键规则：
- `SKILL.md` 文件的长度应控制在 500 行以内；详细文档请放在 `references/` 目录下。
- 在文件中引用路径时，请使用 `{baseDir}`（例如：`{baseDir}/scripts/run.sh`）。
- **禁止使用硬编码的敏感信息**——应从环境变量、`.env` 文件或 `openclaw.json` 文件中读取相关信息（使用 `jq` 进行解析）。
- 保持命令的祈使句形式（例如：“提取 URL”，而不是 “The URL is extracted”）。
- 在执行任何可能改变系统状态的操作之前，务必先显示确认信息并获取用户确认。

### 4. 编写 `README.md` 文件

`README.md` 是面向用户的文档，包含以下内容：

```markdown
# <Skill Name>

<What it does — 1-2 lines>

## Requirements

- <binary or service 1>
- <binary or service 2>

## Setup

<Step-by-step setup instructions>

## Usage

<2-3 natural language examples showing what the user would say>

## Install

\`\`\`bash
clawhub install <author>/<skill-name>
\`\`\`
```

### 5. 质量检查

运行 `{baseDir}/references/checklist.md` 文件，检查以下各项内容：
- `frontmatter` 文件中是否包含 `name` 和 `description` 字段。
- `name` 是否与目录名称一致。
- 描述中是否包含 “Use when...” 等触发条件。
- 是否存在硬编码的敏感信息或 API 密钥。
- 所有内部路径是否都使用了 `{baseDir}`。
- `metadata` 中是否声明了运行时依赖项（如 `requires.bins`、`requires.env`）。
- 是否有错误处理部分。
- 示例部分是否包含至少 3 行的示例数据。
- `SKILL.md` 文件的长度是否在 500 行以内。
- 是否为已发布的技能准备了 `README.md` 文件。
- 在执行任何可能改变系统状态的操作之前，是否都有确认步骤。

将检查结果以清单的形式报告给用户，并指出存在的问题。

### 6. 优化现有技能

在审查现有技能时，请执行以下步骤：
1. 阅读当前的 `SKILL.md` 文件。
2. 运行第 5 步中的质量检查。
3. 列出所有发现的问题及其对应的修复方案。
4. 询问用户应应用哪些修复措施。
5. 应用经过审核的修复方案。

**注意**：不要重新编写整个 `SKILL.md` 文件，只需进行有针对性的、最小化的修改。

## 示例

| 用户输入 | 模式 | 应采取的操作 |
|-----------|------|--------|
| “我想创建一个用于记录阅读清单的技能” | 创建新技能 | 创建 `reading-track/` 目录，收集使用示例，编写 `SKILL.md` 和 `README.md` 文件 |
| “你能帮我检查一下 sm-saver 技能吗？” | 优化现有技能 | 阅读 `sm-saver/SKILL.md` 文件，运行质量检查，列出问题并报告 |
| “创建一个用于检查服务器状态的技能” | 创建新技能 | 创建 `server-check/` 目录，收集使用示例，编写 `SKILL.md` 和 `README.md` 文件 |
| “改进 ClawHub 的提醒功能” | 优化现有技能 | 阅读 `reminder/SKILL.md` 文件，运行质量检查，如有需要添加 `README.md` 文件 |