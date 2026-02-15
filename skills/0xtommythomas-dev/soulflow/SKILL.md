---
name: soulflow
description: OpenClaw 的通用 AI 工作流程框架：可构建适用于任何任务（开发、运维、研究、内容处理或自动化）的定制化多步骤工作流程。随软件提供开发工作流程示例。
homepage: https://github.com/0xtommythomas-dev/soulflow
metadata: 
  clawdbot:
    emoji: "⚙️"
    requires:
      bins: ["node"]
      config_files:
        - "~/.openclaw/openclaw.json"
    permissions:
      config: 
        read: ["~/.openclaw/openclaw.json"]
        write: ["~/.openclaw/openclaw.json"]
      gateway: modify
      agents: create
      filesystem: 
        read: ["~/.openclaw/workspace"]
        write: ["~/.openclaw/workspace/.soulflow", "~/.openclaw/agents/soulflow-worker"]
      credentials: inherit
    security_note: "Creates a dedicated 'soulflow-worker' agent with full tool access (read, write, edit, exec, browser) to execute workflow steps. Reads gateway config (~/.openclaw/openclaw.json) for authentication token. Modifies gateway config to add/manage worker agent. Worker inherits authProfiles from existing agents (grants access to external services like GitHub, cloud providers). All operations run locally with your existing OpenClaw permissions. Only install if you trust the skill author and have reviewed the code."
---

# SoulFlow — OpenClaw的工作流框架

**一个用于构建自定义AI工作流的框架。**每个工作流都是一系列在隔离的代理会话中执行的步骤，这些代理会话具有完整的工具访问权限。您可以使用JSON定义工作流，然后自然地调用它，让代理来处理执行任务。

**您可以构建的内容：**
- 开发流程（安全审计、漏洞修复、功能开发）
- 内容工作流（研究 → 草稿 → 编辑 → 发布）
- 操作自动化（部署 → 验证 → 失败时回滚）
- 研究流程（收集 → 分析 → 合成 → 报告）
- 任何可以从隔离的、专注的代理会话中受益的多步骤任务

**随附3个示例开发工作流**，以展示其工作原理。您可以根据需要构建自己的工作流。

## 快速入门

**自然语言（最简单的方式）：**
只需告诉您的代理您需要什么：
- “对我的项目`~/myapp`进行安全审计”
- “修复这个漏洞：用户无法使用Google OAuth登录`~/webapp`”
- “为`~/webapp`构建一个推荐系统”

您的代理会读取这个SKILL.md文件，并自动调用SoulFlow。

**命令行：**
```bash
cd ~/.openclaw/workspace/soulflow

# Run a security audit
node soulflow.js run security-audit "Audit the codebase at ~/project for vulnerabilities"

# Fix a bug
node soulflow.js run bug-fix "Login returns 500 when email has uppercase letters in ~/myapp"

# Build a feature
node soulflow.js run feature-dev "Add dark mode toggle to the settings page in ~/myapp"
```

## 工作原理

SoulFlow通过WebSocket连接到您的本地OpenClaw网关，并将每个工作流步骤作为隔离的代理会话来运行。会自动创建一个专用的`soulflow-worker`代理，该代理具有最小的上下文信息——不会占用主代理的内存。

每个步骤：
1. 获得一个新的会话（没有上下文冗余）
2. 接收到前一步的任务和输出
3. 具有完整的工具访问权限（读取、写入、编辑、执行、浏览器）
4. 必须完成工作并报告结果

**自动通知（v1.1.0+）：**当工作流完成后，SoulFlow会自动通知主代理会话结果。无需手动检查状态。

## 示例工作流（包含在内）

**这些示例展示了可能的功能。您可以根据任何领域构建自己的工作流。**

### security-audit（安全审计）
**扫描 → 优先级排序 → 修复 → 验证**
开发示例：读取您的源文件，按严重程度识别漏洞，应用修复措施，然后进行验证。

### bug-fix（漏洞修复）
**分类 → 修复 → 验证**
开发示例：通过阅读代码调查根本原因，应用修复措施，然后验证是否引入了回归问题。

### feature-dev（功能开发）
**规划 → 实现 → 审查**
开发示例：设计实现计划，编写代码，然后审查代码的质量和正确性。

**需要内容工作流？研究流程？部署自动化？** 创建您自己的`.workflow.json`文件——请参阅下面的“自定义工作流”部分。

## 命令

```bash
node soulflow.js run <workflow> "<task>"    # Run a workflow
node soulflow.js list                       # List available workflows
node soulflow.js runs                       # List past runs
node soulflow.js status [run-id]            # Check run status
node soulflow.js test                       # Test gateway connection
```

## 通过自然语言（通过您的代理）

**代理知道如何为您调用SoulFlow。**只需描述您的需求：

**安全审计：**
- “对我的应用程序进行安全问题审计”
- “检查`~/myapp`是否存在漏洞”
- “扫描代码库中的安全问题”

**漏洞修复：**
- “修复这个漏洞：登录失败时出现...”
- “支付流程有问题”
- “用户在...时看到500错误”

**功能：**
- “构建一个推荐系统”
- “在设置页面中添加暗黑模式”
- “实现使用Google的OAuth登录”

**工作原理：**
1. 您告诉代理您的需求
2. 代理会读取这个SKILL.md文件
3. 代理调用`node soulflow.js run <workflow> "<task>"`
4. SoulFlow运行工作流并返回结果

**模式匹配：**代理会根据您的消息匹配相应的工作流：
- 安全审计 → 关键词：`audit`, `security`, `scan`, `vulnerabilit`
- 漏洞修复 → 关键词：`fix`, `bug`, `broken`, `not working`, `error`
- 功能开发 → 关键词：`build`, `add`, `implement`, `create`, `feature`

**没有匹配的工作流？** 代理会询问您想要哪个工作流，或者建议您创建一个自定义的工作流。

## 自定义工作流

**您可以为任何任务创建工作流。**使用JSON定义它们，并将它们放在`workflows/`目录中。

### 通过聊天创建

告诉您的代理：
> “为[您的用例]创建一个SoulFlow工作流”

示例：
- “创建一个内容发布的工作流：研究主题 → 草稿文章 → 编辑 → 发布到博客”
- “创建一个部署的工作流：运行测试 → 构建 → 部署 → 验证健康检查 → 失败时回滚”
- “创建一个每周报告的工作流：收集指标 → 分析趋势 → 生成摘要 → 发送电子邮件”

您的代理将：
1. 设计工作流步骤
2. 将`.workflow.json`文件写入`workflows/`
3. 向您展示如何运行它

### 手动创建

在`workflows/`目录中创建一个`.workflow.json`文件：

```json
{
  "id": "my-workflow",
  "name": "My Custom Workflow",
  "version": 1,
  "description": "What this workflow does",
  "steps": [
    {
      "id": "step1",
      "name": "First Step",
      "input": "Do this thing: {{task}}",
      "expects": "STATUS: done",
      "maxRetries": 1
    },
    {
      "id": "step2",
      "name": "Second Step",
      "input": "Now do this based on step 1:\n\n{{step1_output}}\n\nOriginal task: {{task}}",
      "expects": "STATUS: done",
      "maxRetries": 1
    }
  ]
}
```

### 变量

- `{{task}}` — 用户的原始任务描述
- `{{stepid_output}}` — 前一步的输出（例如`{{scan_output}}`）
- 步骤输出中的任何`KEY: value`行都会成为变量（例如`ROOT_CAUSE: ...` → `{{root_cause}}`）

### 提示技巧

为了获得最佳效果，请编写如下提示：
- 明确告诉代理使用哪些工具：“使用`read`来检查文件”，“使用`edit`来应用修复”
- 说“不要只是描述——实际执行它”
- 以“完成时，输入：STATUS: done”作为结束语

## 架构

- **零依赖** — 纯粹的Node.js 22（原生WebSocket）
- **网关原生** — 通过WebSocket进行连接，并使用挑战-响应认证
- **会话隔离** — 每个步骤都在一个新的会话中运行
- **专用工作器** — 自动创建`soulflow-worker`代理，且只使用最小的文件
- **JSON状态** — 运行历史记录保存在`~/.openclaw/workspace/.soulflow/runs/`
- **每个步骤的超时时间为10分钟（可配置）**

## 要求

- OpenClaw 2026.2.x或更高版本
- Node.js 22+（用于原生WebSocket）
- 配置了令牌认证的网关

## 安全与权限

**SoulFlow对您的OpenClaw实例所做的操作：**

1. **读取您的网关配置**（`~/.openclaw/openclaw.json`）以获取通过WebSocket连接所需的认证令牌
2. **修改您的网关配置**（`~/.openclaw/openclaw.json`）通过`config.patch`来注册`soulflow-worker`代理
3. **创建一个专用的工作器代理**（`soulflow-worker`），该代理仅使用最小的文件（仅包含SOUL.md，没有内存/历史记录）
4. **从现有代理复制认证配置文件** — 工作器继承其他代理使用的外部服务（如GitHub、云提供商等）的凭据
5. **授予工作器完整的工具访问权限**（读取、写入、编辑、执行、浏览器）——这是工作流执行任务所必需的
6. **将运行状态写入`~/.openclaw/workspace/.soulflow/runs/`作为JSON文件**

**为什么需要这些权限：**
- **配置读/写**：用于与网关认证和注册工作器代理（与`openclaw` CLI工具相同）
- **代理创建**：每个工作流步骤都在隔离的会话中运行，以防止上下文泄漏
- **认证配置文件继承**：允许工作流使用您现有的凭据与外部服务交互（例如，git推送、云API调用）
- **完整工具**：工作流需要实际的功能（例如，安全审计读取文件、漏洞修复编辑代码、部署流程推送到git）
- **文件系统写入**：存储工作流历史记录，并允许工作流创建/修改文件

**安全考虑：**
- 工作器代理无法访问您主代理的内存或历史记录
- 工作器确实继承了您的外部服务凭据（认证配置文件）——可以访问GitHub、云API等
- 工作流以您的权限运行（与您自己运行命令相同）
- 恶意工作流可能会读取/修改文件、运行命令或访问外部服务
- **只有在您信任技能作者的情况下才安装SoulFlow**（请先在GitHub上查看代码）
- **仅运行您信任的工作流** — 来自不受信任来源的自定义工作流可能会泄露数据或滥用凭据
- 如果处理不受信任的工作流，请在隔离/沙箱环境中运行SoulFlow

**推荐做法：**
- 在首次使用之前查看内置的工作流（特别是安全审计和漏洞修复）
- 在运行之前检查自定义的`.workflow.json`文件
- 在安装之前查看GitHub仓库（https://github.com/0xtommythomas-dev/soulflow）
- 在测试新工作流时在非生产环境的OpenClaw实例上运行
- 在运行修改代码的工作流之前备份重要文件
- 如果您希望每个工作流都有独立的凭据，请使用BYOK（自带密钥）模式
- 监控`~/.openclaw/workspace/.soulflow/runs/`以获取工作流执行日志

---

## 对代理的说明：如何调用SoulFlow

当用户请求一个工作流（安全审计、漏洞修复、功能开发等）时，您应该：

1. **通过匹配关键词来识别工作流**：
   - 安全审计：`audit`, `security`, `scan`, `vulnerabilit`
   - 漏洞修复：`fix`, `bug`, `broken`, `not working`, `error`
   - 功能开发：`build`, `add`, `implement`, `create`, `feature`
   - 自定义：检查`workflows/*.workflow.json`以获取其他选项

2. **提取任务描述** — 用户对所需操作的描述

3. **使用`exec`调用SoulFlow**：
   ```bash
   cd /root/.openclaw/workspace/soulflow && node soulflow.js run <workflow> "<task>"
   ```

4. **监控运行过程** — SoulFlow会输出运行ID，然后在每个步骤完成时显示进度

5. **报告结果** — 完成后，将最终状态传达给用户

**示例：**
```
User: "Run a security audit on ~/myapp"
You: [exec] cd /root/.openclaw/workspace/soulflow && node soulflow.js run security-audit "Audit ~/myapp for vulnerabilities"
```

**为用户创建工作流：**
如果用户请求创建一个自定义工作流：
1. 根据他们的要求设计工作流步骤
2. 将`.workflow.json`文件写入`/root/.openclaw/workspace/soulflow/workflows/`
3. 向他们展示如何运行它

有关工作流设计的最佳实践，请参阅CONTRIBUTING.md。