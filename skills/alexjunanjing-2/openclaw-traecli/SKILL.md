---
name: traecli
description: TRAE CLI 安装、配置和使用指南。TRAE CLI 是一个基于人工智能的命令行编程助手，支持通过自然语言进行开发。
read_when:
  - Installing TRAE CLI
  - Configuring TRAE
  - Using TRAE commands
  - Troubleshooting TRAE issues
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["sh","curl"]}}}
allowed-tools: Bash(*), Read(*), Write(*), Edit(*)
---
# TRAE CLI 技能

## 什么是 TRAE CLI？

TRAE CLI 是您的专用代码助手。您可以通过发送自然语言指令给 TRAE CLI 来完成一系列复杂的开发任务，从编写代码、测试到 Git 操作，从而让您能够专注于更高价值的创造性工作。

### 核心功能

- **代码编写与修改**：根据需求添加新功能、修复错误或重构现有代码
- **代码理解与问答**：快速回答关于项目架构、业务逻辑、函数实现等方面的代码问题
- **功能测试与调试**：运行代码检查工具（lint 工具）和单元测试，修复失败的测试用例，并帮助排查和解决问题
- **Git 操作自动化**：简化 Git 工作流程，例如自动创建提交信息、解决合并冲突、查询提交历史等
- **第三方能力集成**：通过 Model Context Protocol (MCP) 灵活集成第三方工具和服务
- **大型语言模型**：内置多个大型语言模型，支持配置和使用 OpenAI 与 Claude 提供的模型

### 产品优势

- **即用型**：配置简单，安装后立即可在项目中使用，无需复杂的环境设置
- **高度可扩展**：通过配置文件轻松集成自定义工具和大型语言模型，以满足团队特定需求
- **任务自动化**：自动化繁琐且重复的开发任务，让您能够专注于更具创造性的工作

### 重要说明

- **使用限制**：仅 TRAE 企业版才能使用 TRAE CLI
- **使用警告**：TRAE CLI 默认使用 Max 模式，请监控您的使用量

## 安装

### macOS 与 Linux

在本地终端中执行以下脚本以安装 TRAE CLI：

```bash
sh -c "$(curl -L https://lf-cdn.trae.com.cn/obj/trae-com-cn/trae-cli/install.sh)" && export PATH=~/.local/bin:$PATH
```

### Windows (PowerShell)

在 PowerShell 中执行以下脚本以安装 TRAE CLI：

```powershell
irm https://lf-cdn.trae.com.cn/obj/trae-com-cn/trae-cli/install.ps1 | iex
```

**注意**：如果 TRAE CLI 中的内置 Ripgrep 无法使用，您还需要安装 Visual C++ Redistributable（VC 运行时库）。

## 快速入门

### 启动 TRAE CLI

1. 执行 `cd` 命令进入目标项目
2. 执行以下命令启动 TRAE CLI：

```bash
traecli
```

3. 启动后，您将进入 TRAE CLI 界面
4. 在对话框中输入指令或问题并发送给 TRAE CLI。例如：“解释这个项目的架构”
5. TRAE CLI 会提示您登录企业账户
6. 登录企业账户并完成授权，然后返回 TRAE CLI
7. TRAE CLI 将开始分析问题并生成响应

### 升级 TRAE CLI

TRAE CLI 支持自动和手动升级：

- **自动升级**：当您启动 TRAE CLI 时，如果当前版本不是最新版本，TRAE CLI 将开始自动升级，并在右下角显示进度
- **手动升级**：使用 `traecli update` 命令手动升级

## 使用场景

### 理解不熟悉的代码库

在处理新项目时，使用 TRAE CLI 快速了解代码库的整体结构。

**示例**：

- **理解项目架构**：“这个项目的整体架构是什么？请用目录树和文字说明。”
- **跟踪核心业务流程**：“我们系统中的支付流程是什么？涉及哪些关键服务和函数调用？”
- **定位特定功能**：“用户权限验证逻辑在哪里实现？”
- **分析复杂模块设计**：“告诉我缓存模块的设计，包括缓存策略和失效机制。”

### 编写和修改代码

TRAE CLI 可以帮助您开发新功能、修复错误、编写文档等。

**示例**：

- **更新文档**：“更新 README.md 文件，在功能介绍部分添加‘支持多模型切换’的描述。”
- **添加业务逻辑**：“在订单创建界面添加输入参数验证，确保用户 ID 不能为空。”
- **修复复杂问题**：“后台工作队列实现中存在竞态条件。请帮我定位并修复它。”

### 测试和调试

TRAE CLI 可以帮助您运行单元测试、定位问题并提供修复建议。

**示例**：

- **运行单元测试并修复问题**：“运行所有单元测试并尝试修复那些失败的测试用例。”
- **调查安全漏洞**：“扫描代码中可能的 SQL 注入漏洞并提供修复建议。”
- **分析失败原因**：“CI 构建失败了。帮我分析日志并找出失败的原因。”

### 自动化 Git 操作

让 TRAE CLI 为您处理 Git 命令。

**示例**：

- **快速提交**：“帮我提交暂存文件，并设置提交信息为‘feat: add user profile page’。”
- **查询提交历史**：“找出哪个提交修改了登录页面的 UI 样式。”
- **处理复杂的分支操作**：“将我的当前分支重新基接到主分支，并在过程中自动解决冲突。”

### 在自动化脚本中使用 TRAE CLI

TRAE CLI 支持在非交互模式下运行。您可以方便地将 TRAE CLI 集成到 CI/CD 流程或其他自动化脚本中，以实现开发流程的自动化。

**示例**：

- **根据最近的 Git 提交自动更新 README**：
  ```bash
  traecli --allowed-tool Bash,Edit,MultiEdit,Write -p "update README with latest changes"
  ```

- **在 CI 脚本中自动运行预写的提示模板**：
  ```bash
  traecli -p /command arg1 arg2
  ```

## 命令行参数

您可以使用以下命令行参数传递额外信息：

| 参数 | 描述 |
|----------|-------------|
| `--allowed-tool` | 指定允许使用的工具，例如 “Bash”、“Edit”、“Replace” 等。多个工具用逗号分隔。可以多次指定。 |
| `--bash-tool-timeout` | 设置通过 Bash 工具执行的命令的最大运行时间。超时后，执行将自动终止，例如 30 秒、5 分钟、1 小时。 |
| `-c / --config` | 覆盖 “k=v” 格式的设置。 |
| `--disallowed-tools` | 指定禁止使用的工具。多个工具用逗号分隔。可以多次指定。 |
| `-h / --help` | 获取 TRAE CLI 的使用帮助。 |
| `--json` | 以 JSON 格式输出完整信息，包括系统提示、工具调用、执行过程和最终结果。仅与 `--print` 一起使用。 |
| `-p / --print` | 打印响应内容并立即退出，适用于管道场景。 |
| `--query-timeout` | 设置单个查询的最大执行时长。超时将终止查询，例如 30 秒、5 分钟、1 小时。 |
| `-v / --version` | 查看 TRAE CLI 的当前版本。 |

## 斜杠命令

在会话中，使用斜杠命令来执行快速操作、管理会话状态和自定义常见工作流程。

### 内置斜杠命令

| 命令 | 用途 |
|---------|---------|
| `/agent-new` | 创建一个新的自定义代理。 |
| `/clear` 或 `/reset` | 清除对话历史并释放上下文。 |
| `/feedback` | 提交反馈或报告问题。 |
| `/init` | 为当前目录初始化一个新的 AGENTS.md 文件。 |
| `/login` | 登录 TRAE CLI。 |
| `/logout` | 登出 TRAE CLI。 |
| `/mcp` | 管理 MCP 服务器和工具。 |
| `/model` | 切换使用的 AI 模型。 |
| `/plugin` 或 `/plugins` | 管理插件。 |
| `/status` | 显示 TRAE CLI 的状态信息。 |
| `/terminal-setup` | 安装 Shift+Enter 的换行快捷键。 |

### 自定义斜杠命令

您可以将常用的提示定义为 Markdown 文件，TRAE CLI 会将它们作为自定义斜杠命令执行。

#### 语法

```
/<command-name> [arguments]
```

**参数描述**：

- `<命令名称>`：来自 Markdown 文件名称的名称（不包含 `.md` 扩展名）
- `[参数]`：传递给命令的可选参数

#### 创建自定义斜杠命令

1. 使用 `mkdir -p .traecli/commands` 在项目根目录下创建 `.traecli/commands` 目录
2. 使用 `cd .traecli/commands` 进入 `.traecli/commands` 目录
3. 在 `.traecli/commands` 目录中创建一个 Markdown 格式的自定义斜杠命令配置文件
4. 配置自定义斜杠命令并保存

**Frontmatter 字段描述**：

| Frontmatter | 描述 | 示例 |
|-------------|-------------|---------|
| `description` | 此自定义斜杠命令的简要描述。 | `Review code changes with context` |
| `argument-hint` | 斜杠命令所需的参数。此提示将在执行斜杠命令自动补全时显示给用户。 | `argument-hint: add [tagId] \| remove [tagId] \| list` |
| `tools` | 指定可用的工具。多个工具用逗号分隔。 | `Read,Write,mcp__{$mcp_server_name}__{$tool_name}` |
| `model` | 指定要使用的模型。 | `kimi-k2` |

**示例**：

```markdown
---
description: Review code changes with context
argument-hint: <file-pattern>
model: kimi-k2
tools: Read
---

## Code Review Request

Files to review: $1

Current git diff: !`git diff HEAD -- $1`

File structure: !`find . -name "$1" -type f | head -10`

## Your task

Please perform a thorough code review of specified files focusing on:

1. **Code Quality**: Check for best practices, readability, and maintainability
2. **Security**: Look for potential security vulnerabilities
3. **Performance**: Identify potential performance issues
4. **Testing**: Suggest areas that need test coverage
5. **Documentation**: Check if code is properly documented

Provide specific suggestions for improvement with line numbers where applicable.
```

#### 其他功能

TRAE CLI 提供了一系列特殊语法，用于动态引用参数、设置默认值以及在命令定义中插入系统命令的执行结果，极大地增强了自定义命令的灵活性和可重用性。

**`$ARGUMENTS`**

`$ARGUMENTS` 占位符捕获传递给命令的所有参数，多个参数之间用空格分隔。

示例：

```bash
# Command definition
echo 'Deploying service: $ARGUMENTS to staging environment' > .traecli/commands/deploy-service.md

# Usage
> /deploy-service auth-api v2.3.1
# $ARGUMENTS becomes: "auth-api v2.3.1"
```

**`$N`**

您可以通过位置参数 `$N` 单个访问特定参数，就像在 shell 脚本中一样。

示例：

```bash
# Command definition
echo 'Deploy service $1 to environment $2 with version $3' > .traecli/commands/deploy-service.md

# Usage
> /deploy-service auth staging v1.4.2
# $1 becomes "auth", $2 becomes "staging", $3 becomes "v1.4.2"
```

**!`命令`

`!`命令用于执行指定的命令，并将其标准输出结果直接插入当前位置作为文本内容。

例如，在以下命令定义中，`!`cat VERSION` 会在 TRAE CLI 处理文件时被执行。TRAE CLI 会运行 `cat VERSION`，然后获取其标准输出（例如 1.4.0），最后将 `!`cat VERSION` 替换为输出内容。

```bash
# Command definition
echo "Project version: !`cat VERSION`" > traecli/commands/show-version.md

# After replacement
Project version: 1.4.0
```

**`${N:-DefaultValue}`**

`${N:-DefaultValue}` 用于为变量提供默认值。

- 如果变量 N 未定义或为空，使用 DefaultValue 作为替代
- 如果变量 N 已定义且有非空值，使用变量的实际值

示例：

```bash
# Command definition
echo 'Deploying to environment: ${1:-staging}' > .traecli/commands/deploy.md

# Usage
# Case 1: User provided parameter and defined $1="production"
> /deploy production
# ${1:-staging} becomes "production"

# Case 2: User did not provide parameter, $1 is undefined
> /deploy
# ${1:-staging} becomes "staging"
```

## 故障排除

### 安装问题

**问题**：安装脚本无法执行

**解决方案**：
- 确保您有访问 `lf-cdn.trae.com.cn` 的网络权限
- 检查系统中是否安装了 `curl`
- 对于 Windows，确保 PowerShell 的执行策略允许运行脚本

**问题**：安装后找不到 TRAE CLI 命令

**解决方案**：
- 确保您已将 `~/.local/bin` 添加到 PATH 环境变量中
- 在 macOS 和 Linux 上：`export PATH=~/.local/bin:$PATH`
- 在 Windows 上：安装完成后重新启动 PowerShell

### 运行时问题

**问题**：Ripgrep 无法使用

**解决方案**：
- 在 Windows 上安装 Visual C++ Redistributable（VC 运行时库）
- 从 Microsoft 官网下载

**问题**：登录问题

**解决方案**：
- 确保您拥有 TRAE 企业版账户
- 检查网络连接
- 使用 `/login` 命令重新认证

**问题**：命令超时

**解决方案**：
- 使用 `--bash-tool-timeout` 增加长时间运行的命令的超时时间
- 使用 `--query-timeout` 增加查询的超时时间
- 示例：`traecli --bash-tool-timeout 10m --query-timeout 5m`

### 性能问题

**问题**：使用量过高

**解决方案**：
- TRAE CLI 默认使用 Max 模式，可能会消耗更多资源
- 考虑使用 `/model` 命令切换到更轻量的模型
- 定期监控您的使用量

## 最佳实践

1. **从简单开始**：在处理复杂任务之前，先通过简单问题了解代码库
2. **使用自定义命令**：为重复性任务创建自定义斜杠命令以提高效率
3. **Git 集成**：让 TRAE CLI 处理 Git 操作，以确保提交信息的一致性
4. **CI/CD 集成**：在自动化脚本中使用非交互模式
5. **监控使用情况**：定期跟踪您的使用量，尤其是在使用 Max 模式时
6. **审查更改**：在应用 TRAE CLI 建议的代码更改之前，务必先进行审查

## 其他资源

- 官方文档：https://docs.trae.cn/cli
- TRAE CLI 开源许可证：https://docs.trae.cn/cli/open-source-software-notice-for-trae-cli
- MCP 文档：https://docs.trae.cn/cli/model-context-protocol