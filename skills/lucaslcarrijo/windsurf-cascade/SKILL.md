---
name: windsurf-cascade
version: 1.0.0
description: 这是一项关于如何使用Windsurf IDE及其Cascade AI代理来完成各种软件工程任务的综合性技能指南（已更新至2026年的新功能，涵盖技能（Skills）、工作流程（Workflows）、记忆（Memories）、MCP以及多代理会话（Multi-agent Sessions）等内容）。
author: Lucas Carrijo
---
# Windsurf Cascade智能助手技能

本技能提供了使用Windsurf集成开发环境（IDE）及其Cascade AI智能助手的全面指南和工作流程，涵盖了自2026年1月发布的Wave 13版本的所有功能。

## 安装

### 下载

从 [windsurf.com](https://windsurf.com) 下载适用于您操作系统的Windsurf编辑器：
- **macOS**: `.dmg` 安装包（支持Intel和Apple Silicon架构）
- **Windows**: `.exe` 安装包
- **Linux**: `.deb` 包（Debian/Ubuntu系统）或 `.tar.gz` 压缩包

### 安装后的设置

**将Windsurf添加到PATH环境变量中（可选，但推荐）：**

在入职培训期间，您可以选择将Windsurf添加到PATH环境变量中，以便通过命令行直接使用：

```bash
# macOS - create symlink manually if needed
sudo ln -sF /Applications/Windsurf.app/Contents/Resources/app/bin/windsurf /usr/local/bin/windsurf

# Open a project from terminal
windsurf /path/to/project
```

**导入现有配置：**

Windsurf支持从VS Code或Cursor导入设置、扩展程序和快捷键绑定。您也可以通过命令面板稍后进行导入：

```
Cmd+Shift+P → "Import VS Code Settings"
Cmd+Shift+P → "Import Cursor Settings"
```

### Windows系统下的WSL（Windows Subsystem for Linux）设置

Windsurf支持WSL（测试版）。请按照以下步骤连接到您的WSL实例：
1. 单击左下角的远程连接按钮
2. 选择“Connect to WSL”或使用命令面板：`Remote-WSL: Connect to WSL`

若需从WSL终端访问Windsurf功能，请创建一个辅助脚本：

```bash
#!/bin/bash
CURRENT_PATH=$(readlink -f "$1")
windsurf --folder-uri "vscode-remote://wsl+Ubuntu$CURRENT_PATH"
```

### 认证

在入职培训期间或通过个人资料菜单注册或登录您的Windsurf（原名Codeium）账户。

## Cascade——AI智能助手

Cascade是Windsurf的智能助手，它可以理解您的整个代码库，跟踪您的实时操作（编辑、终端操作、剪贴板内容），并能够自动创建文件、编辑多个文件中的代码、运行终端命令以及管理项目相关数据。

### Cascade模式

Cascade主要有两种模式：

- **编写模式**（`Cmd+L` / `Ctrl+L`）：具有完整的编写权限，可以创建文件、编辑代码、运行终端命令并对代码库进行修改。
- **聊天模式**（`Cmd+Shift+L` / `Ctrl+Shift+L`切换）：仅支持读取模式，可以回答关于代码库和编码原则的问题，但不会进行任何修改。

### 模型选择

您可以从Cascade输入框下方的下拉菜单中选择不同的模型。可选模型包括：
- **SWE-1.5**（Windsurf自家的前沿模型，所有用户均可免费使用）
- **Claude Opus 4.6**、**Claude Sonnet 4.5**
- **GPT-5.2**、**GPT-5.2-Codex**、**GPT-5.1**、**GPT-5.1-Codex**
- **Gemini 3 Flash**、**Gemini 3 Pro**
- **Falcon Alpha**（优化速度的隐身模型）
- **BYOK**（用户自定义模型）

每个模型的使用会消耗相应的信用点数。

### 工具调用

Cascade内置了多种工具：
- **搜索**：在代码库中进行语义搜索
- **分析**：深入分析代码结构和关系
- **网络搜索**：在互联网上查找文档和参考资料
- **MCP**：通过模型上下文协议调用外部工具
- **终端**：直接执行shell命令

Cascade每次请求最多可调用25个工具。如果操作暂停，输入`continue`即可恢复。

### 使用@提及引用上下文

您可以在提示中引用特定的文件、函数或上下文：

```
@filename.ts
@src/components/
@function:calculateTotal
```

您还可以：
- 从文件资源管理器中将文件拖放到Cascade中
- 从问题面板将问题发送给Cascade
- 高亮显示错误并点击“解释并修复”
- 通过@提及来引用之前的对话内容以保持会话间的上下文关联

### 语音输入

您可以通过语音输入与Cascade进行交互，系统会将其转换为文本。

### 检查点与回滚

Cascade会创建带有名称的检查点。您可以通过将鼠标悬停在提示上并点击回滚箭头来撤销更改。**需要注意的是，目前回滚操作是不可逆的。**

## 键盘快捷键

| 功能 | macOS | Windows/Linux |
|---|---|---|
| 打开Cascade（编写模式） | `Cmd+L` | `Ctrl+L` |
| 切换编写/聊天模式 | `Cmd+Shift+L` | `Ctrl+Shift+L` |
| 命令面板 | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| 内联AI（终端） | `Cmd+I` | `Ctrl+I` |
| 接受选中的代码差异部分 | `Option+Enter` | `Alt+Enter` |
| 拒绝选中的代码差异部分 | `Option+Shift+Backspace` | `Alt+Shift+Backspace` |
| 快速上下文（显示第一条消息） | `Cmd+Enter` | `Ctrl+Enter` |

## 技能

技能允许您将指令、模板、检查表和支持文件打包到文件夹中，以便Cascade能够执行复杂的、多步骤的任务。

### 创建技能

1. 单击Cascade右上角自定义设置图标
2. 转到技能面板
3. 点击`+ Workspace`（针对特定工作空间）或`+ Global`（全局技能）
4. 为技能命名（仅使用小写字母、数字和连字符）

### Skill.md文件格式

`SKILL.md`文件用于存储技能的名称和描述等信息。描述字段有助于Cascade判断何时自动触发该技能。

### 调用技能

- **自动触发**：Cascade会根据任务需求自动调用相应的技能。
- **手动触发**：在提示中通过@提及来调用技能名称。

有关技能的完整规范，请访问 [agentskills.io](https://agentskills.io)。

## 工作流程

工作流程定义了一系列步骤，用于指导Cascade完成重复性任务。它们以markdown格式保存，并通过特定的命令来调用。

### 创建工作流程

1. 单击自定义设置图标 → 工作流程面板 → `+ Workflow`
2. 或者让Cascade为您自动生成工作流程

### 工作流程的存储位置

工作流程保存在`.windsurf/workflows/`目录下。Windsurf会从以下位置自动检测工作流程：
- 当前工作空间及其子目录
- 一直到git仓库根目录的父目录
- 支持多个工作空间的工作流程，并会进行去重处理

每个工作流程文件的长度限制为**12,000个字符**。

### 调用工作流程

```
/workflow-name
```

工作流程可以相互调用：

```markdown
## Steps
1. Call /lint-and-format
2. Call /run-tests
3. Deploy to staging
```

### 示例工作流程——PR审查

```markdown
---
name: pr-review
description: Review PR comments and address them
---

## Steps
1. Check out the PR branch: `gh pr checkout [id]`
2. Get comments on PR:
   ```bash
   gh api --paginate repos/[owner]/[repo]/pulls/[id]/comments | jq '.[] | {user: .user.login, body, path, line}'
   ```
3. For EACH comment, address the feedback and commit the fix
4. Push changes and reply to each comment
```

## 记忆与规则

记忆功能可以在Cascade的对话中保持上下文信息。规则用于指导Cascade的行为。

### 记忆

- **自动生成**：Cascade在遇到有用信息时会自动生成记忆记录，且不会消耗信用点数。
- **用户创建**：在Cascade中输入`create memory ...`来手动保存上下文信息。
- 自动生成的记忆记录仅适用于当前工作空间。

**管理记忆记录：**
- 通过Windsurf设置 → 设置选项卡 → “Cascade-Generated Memories”进行管理
- 或者：在Cascade中点击三个点 → 管理记忆记录
- 切换自动生成功能：设置 → “Auto-Generate Memories”

### 规则

规则是用户为Cascade定义的指令。

**规则类型：**
- `global_rules.md`：适用于所有工作空间
- `.windsurf/rules/`：包含特定工作空间规则的目录
- 系统级规则（企业版）：通过MDM策略进行配置

**规则激活模式：**
- **始终启用**：规则始终生效
- **全局规则**：应用于符合特定模式的文件（例如`.js`、`src/**/*.ts`）
- **手动/基于描述的规则**：通过自然语言匹配来激活

**规则编写最佳实践：**
- 保持规则简洁明了
- 使用项目符号和markdown格式
- 避免使用过于笼统的规则（如“编写优质代码”）
- 使用XML标签对规则进行分组

**示例规则：**

```markdown
# Coding Guidelines
- My project's programming language is Python
- Use early returns when possible
- Always add documentation when creating new functions and classes
- Use pytest for testing
- Follow PEP 8 style guide
```

## 终端集成

### 内联AI终端

在终端中按`Cmd+I` / `Ctrl+I`可以打开一个内联聊天框，该聊天框可以根据自然语言生成CLI命令。

### Cascade的终端执行功能

Cascade可以直接运行终端命令。您可以在Windsurf设置中配置自动执行规则：
- **手动模式**：每次执行命令时都需要用户确认
- **半自动模式**：自动执行安全命令
- **快速模式**：无需确认即可自动执行所有命令
- **自定义模式**：通过允许/拒绝列表来控制特定命令的执行

### 专用终端（Wave 13版本）

Windsurf为Cascade提供了专用的zsh shell，提升了命令执行的可靠性。该终端使用您的`.zshrc`环境变量，并支持完整的交互功能。

### ⚠️ 与AI助手/自动化工具的配合使用

当在自动化环境中（如AI助手、脚本或编排器）使用Windsurf时，IDE需要图形用户界面（GUI）环境。对于无界自动化场景，您可以考虑：
- **使用Windsurf的工作流程**：将多步骤任务定义为工作流程，由Cascade执行
- **MCP集成**：通过MCP服务器连接外部自动化工具
- **Cascade钩子**：在Cascade的工作流程中的关键点执行自定义shell命令

## MCP集成

Windsurf支持Model Context Protocol（MCP）协议，用于连接外部工具和服务。

### 配置MCP服务器

请在`mcp_config.json`文件中进行配置：

```json
{
  "mcpServers": {
    "github": {
      "command": "uvx",
      "args": ["github-mcp"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

访问方式：Windsurf设置 → Cascade → 管理MCPs → 查看原始配置文件

### MCP功能

- **MCP市场**：在Windsurf设置中浏览精选的MCP服务器，支持一键配置
- **@提及**：在Cascade中通过@提及来触发MCP工具
- **启用/禁用**：通过Cascade界面切换MCP服务器
- **传输方式**：支持标准输入输出（STDIO）、Streamable HTTP和SSE协议
- **企业版**：团队管理员可以白名单/黑名单MCP服务器

每次调用MCP工具会消耗一个信用点数。

## Cascade钩子

您可以在Cascade的工作流程中的关键点执行自定义shell命令：
- **模型响应时**：用于日志记录、审计或安全控制
- **预处理/后处理钩子**：用于验证或管理目的（企业版）

## 同时运行多个Cascade实例

您可以并行运行多个Cascade实例：
- 打开多个Cascade窗口
- 使用Git工作区在不同的分支上同时进行开发，避免冲突
- 在一个Cascade实例执行时启动另一个Cascade实例

## 快速上下文功能

按`Cmd+Enter` / `Ctrl+Enter`可以启用快速上下文功能。该功能利用SWE-grep模型，从大型代码库中快速检索信息，速度提升多达20倍。

## 文件忽略规则

将需要忽略的文件添加到工作空间的`.codeiumignore`文件中（格式与`.gitignore`相同）。若需在所有仓库中应用全局忽略规则，请将`.codeiumignore`文件放在`~/.codeium/`目录下。

## 常见工作流程示例

### 代码审查

```
Review the changes in the current branch against main.
Focus on security and performance.
```

### 代码重构

```
Refactor src/utils.ts to reduce complexity and improve type safety.
```

### 调试

```
Analyze the following error log and suggest a fix: [paste error]
```

### 错误处理

### Git集成

```
Generate a commit message for the staged changes adhering to conventional commits.
```

### 部署

在`.windsurf/workflows/deploy.md`文件中创建部署脚本：

```markdown
---
name: deploy
description: Deploy to production with safety checks
---

## Steps
1. Run all tests: `npm test`
2. Build the project: `npm run build`
3. Run linter: `npm run lint`
4. If all pass, deploy: `npm run deploy:production`
5. Verify deployment health checks
```

通过`/deploy`命令在Cascade中调用该脚本进行部署。

### 实时预览

Windsurf内置了实时预览功能，可用于Web应用程序。您可以请求Cascade启动开发服务器，预览结果会显示在编辑器中。点击任何元素即可让Cascade对其进行修改。

### 应用程序部署

通过Cascade的工具调用功能（支持Netlify部署，目前处于测试阶段），您可以一键完成应用程序的部署。

## 价格方案

| 价格方案 | 价格 | 每月信用点数 | 适用对象 |
|---|---|---|---|
| 免费 | $0 | 25个信用点 | 学生、爱好者 |
| Pro | $15/月 | 500个信用点 | 个人开发者 |
| Teams | $30/用户/月 | 可定制 | 开发团队 |
| Enterprise | $60/用户/月 | 可定制 | 大型企业 |

## Windsurf与Cursor的主要区别

| 功能 | Windsurf | Cursor |
|---|---|---|
| AI助手 | Cascade（具有智能交互能力） | Cursor助手（基于CLI） |
| 规则管理 | `.windsurf/rules/` + `global_rules.md` | `.cursor/rules` + `CLAUDE.md` |
| 工作流程 | `.windsurf/workflows/`（使用斜杠命令） | 无（需手动操作） |
| 记忆功能 | 自动生成 + 用户自定义 | 基于代码库的索引 + 项目规则 |
| 技能管理 | `.windsurf/skills/`（文件夹形式） | 无 |
| 终端支持 | 专用zsh shell + 快速执行模式 | 标准终端 |
| 实时预览 | 内置功能 | 需依赖扩展程序 |
| MCP集成 | 内置支持 | 内置支持 |