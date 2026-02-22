---
name: solo-init
description: 一次性创始人入职指导：生成个性化配置文件、STREAM校准数据、开发原则以及技术栈选择指南。适用于用户执行以下操作时：设置独立开发环境（"set up solo factory"）、初始化个人配置文件（"initialize profile"）、配置默认设置（"configure defaults"）或首次进行系统设置（"first time setup"）。该流程可重复执行，无需担心数据冲突。请勿将其用于项目搭建（请使用命令 "/scaffold"）。
license: MIT
metadata:
  author: fortunto2
  version: "2.1.1"
  openclaw:
    emoji: "🎬"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion
argument-hint: "[project-path]"
---
# /init

这是一个用于新创始人入职的初始化流程。该流程会询问一些关键问题，并根据回答生成个性化的配置文件。所有配置信息都以可读的 Markdown 或 YAML 格式存储，可以随时进行修改。

配置信息分为两个层级：
- **`~/.solo-factory/defaults.yaml`**：组织级配置（包含包 ID、GitHub 组织信息、Apple 团队 ID），在所有项目中共享。
- **`.solo/`**：项目级配置（包含创始人的理念、开发原则、代码流程校准设置以及所选的技术栈），每个项目可能有不同的配置，但通常基本相同。

`solo-factory/templates/` 目录中的模板为默认配置。该脚本会根据用户的回答对这些模板进行个性化调整。

在安装 `solo-factory` 后，只需运行一次该脚本即可。之后可以安全地重新运行该脚本，系统会显示当前的配置信息并允许用户进行更新。

## 输出结构

```
~/.solo-factory/
└── defaults.yaml              # Org defaults (bundle IDs, GitHub, Team ID)

.solo/
├── manifest.md                # Your founder manifesto (generated from answers)
├── stream-framework.md         # STREAM calibrated to your risk/decision style
├── dev-principles.md          # Dev principles tuned to your preferences
└── stacks/                    # Only your selected stack templates
    ├── nextjs-supabase.yaml
    └── python-api.yaml
```

其他相关脚本会从以下文件中读取配置信息：
- `/scaffold` 会读取 `defaults.yaml` 文件中的 `<org_domain>` 和 `<apple_dev_team>` 配置信息，以及 `/.solo/stacks/` 目录中的技术栈模板。
- `/validate` 会读取 `manifest.md` 文件以检查配置是否符合项目规范。
- `/setup` 会读取 `dev-principles.md` 文件以获取开发工作流程的配置。
- `/stream` 会读取 `stream-framework.md` 文件以获取决策框架的配置。

## 流程步骤

### 1. 检查现有配置
- 读取 `~/.solo-factory/defaults.yaml` 文件（如果存在），显示当前的配置值。
- 检查项目路径下是否包含 `.solo/` 文件。
- 如果两者都存在，询问用户：“是否要从头重新配置？”或“保持现有配置并跳过此步骤？”
- 如果两者都不存在，继续执行步骤 2。

### 2. 确定项目路径
- 如果 `$ARGUMENTS` 中包含项目路径，使用该路径；否则使用当前的工作目录。

### 3. 询问组织级配置信息（通过 AskUserQuestion 提问 5 个问题）
详细问题内容请参阅 `references/questions.md` 中的 “Round 0: Org Defaults” 部分。

### 4. 创建组织级配置
```bash
mkdir -p ~/.solo-factory
```

编写 `~/.solo-factory/defaults.yaml` 文件：
```yaml
# Solo Factory — org defaults
# Used by /scaffold and other skills for placeholder replacement.
# Re-run /init to update these values.

org_domain: "<answer from 3.1>"
apple_dev_team: "<answer from 3.2>"
github_org: "<answer from 3.3>"
projects_dir: "<answer from 3.4>"
knowledge_base_repo: "<answer from 3.5>"
```

### 5. 第一轮询问：理念与价值观（通过 AskUserQuestion 提问 4 个问题）
详细问题内容请参阅 `references/questions.md` 中的 “Round 1: Philosophy & Values” 部分。

### 6. 第二轮询问：开发偏好（通过 AskUserQuestion 提问 4 个问题）
详细问题内容请参阅 `references/questions.md` 中的 “Round 2: Development Preferences” 部分。

### 7. 第三轮询问：决策风格与技术栈（通过 AskUserQuestion 提问 3 个问题）
详细问题内容请参阅 `references/questions.md` 中的 “Round 3: Decision Style & Stacks” 部分。

### 8. 加载默认模板并生成个性化配置文件
详细信息请参阅 `references/generation-rules.md`：
- 模板的来源位置。
- 输出文件的结构（`defaults.yaml`、`manifest.md`、`stream-framework.md`、`dev-principles.md`、`stacks/`）。
- 每个文件的个性化规则（用户回答如何映射到生成的配置文件中）。
- 技术栈模板与用户选择的映射关系（用户答案如何对应到相应的 YAML 文件中）。

### 10. 验证 Solograph MCP（可选步骤）
- 尝试运行 `uvx solograph --help` 命令，或检查是否安装了 Solograph 工具。
- 如果 Solograph 可用，则提示 “Solograph 已检测到——代码图谱已生成”。
- 如果未安装 Solograph，则提示 “提示：安装 Solograph 以在项目中搜索代码（使用 `pip install solograph` 或 `uvx solograph`）”。

### 11. 总结
```
Solo Factory initialized!

Org config:
  Config:         ~/.solo-factory/defaults.yaml
  org_domain:     <value>
  apple_dev_team: <value>
  github_org:     <value>
  projects_dir:   <value>

Founder profile:
  Manifest:       .solo/manifest.md
  Dev Principles: .solo/dev-principles.md
  STREAM:          .solo/stream-framework.md
  Stacks:         .solo/stacks/ (N stacks)

These files are yours — edit anytime.
Other skills read from .solo/ automatically.

Next steps:
  /validate "your idea"          — validate with your manifest
  /scaffold app nextjs-supabase  — scaffold with your stack
```

### 特殊情况
详细信息请参阅 `references/generation-rules.md` 中的 “Edge Cases” 部分。

## 常见问题

### 模板目录未找到
**原因**：`solo-factory` 未被作为子模块安装，或者模板文件被移动了。
**解决方法**：如果模板文件缺失，该脚本会使用内置的默认配置。为永久解决此问题，请确保 `solo-factory/templates/` 目录存在。

### 技术栈未复制到 `.solo/` 目录
**原因**：用户选择的技术栈对应的模板文件不存在。
**解决方法**：检查 `templates/stacks/` 目录中是否有可用的技术栈模板，然后重新运行 `/init` 并重新选择技术栈。

### `defaults.yaml` 文件已存在
**原因**：系统之前已经进行过初始化配置。
**解决方法**：该脚本会检测到现有的配置，并询问用户是否需要重新配置。选择 “从头重新配置” 以覆盖现有配置。