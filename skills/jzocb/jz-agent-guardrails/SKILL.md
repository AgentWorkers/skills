---
name: agent-guardrails
version: "1.1.0"
author: "Anonymous"
license: "MIT"
category: "development-tools"
description: "防止 AI 代理秘密绕过您的规则。通过 Git 钩子（git hooks）、秘密检测（secret detection）、部署验证（deployment verification）以及导入注册表（import registries）等机制实现强制性的规则执行。这一解决方案源于实际生产环境中的问题，例如服务器崩溃（server crashes）、令牌泄露（token leaks）以及代码被篡改（code rewrites）。该方案兼容 Claude Code、Clawdbot 和 Cursor 等工具。只需安装一次，即可永久生效。"
tags:
  - "ai-safety"
  - "code-quality"
  - "enforcement"
  - "git-hooks"
  - "deployment"
  - "security"
  - "automation"
  - "guardrails"
  - "claude-code"
  - "clawdbot"
  - "cursor"
  - "mechanical-enforcement"
  - "agent-reliability"
keywords:
  - "AI agent bypassing"
  - "code enforcement"
  - "git hooks automation"
  - "secret detection"
  - "deployment verification"
  - "import enforcement"
  - "mechanical guardrails"
  - "agent safety"
  - "production incidents"
  - "Claude Code skills"
  - "Clawdbot skills"
  - "AI coding safety"
repository: "https://github.com/anon/agent-guardrails"
homepage: "https://github.com/anon/agent-guardrails#readme"
bugs: "https://github.com/anon/agent-guardrails/issues"
compatibility:
  - "claude-code"
  - "clawdbot"
  - "cursor"
  - "any-ai-agent"
requirements:
  bash: ">=4.0"
  git: ">=2.0"
pricing: "FREE"
---
# 代理行为规范（Agent Behavior Guidelines）

这些规范用于确保AI代理项目遵循既定的技术标准。Markdown格式的规则仅作为建议提供，而代码钩子（code hooks）则是强制执行的机制。

## 快速入门

```bash
cd your-project/
bash /path/to/agent-guardrails/scripts/install.sh
```

此步骤会安装git预提交钩子（pre-commit hook），创建一个注册表模板（registry template），并将检查脚本（check scripts）复制到你的项目中。

## 执行层次结构（Enforcement Hierarchy）

1. **代码钩子**（git预提交钩子、创建前/创建后检查）——100%可靠
2. **架构约束**（注册表、导入检查）——95%可靠
3. **自我验证机制**（代理自行检查代码）——80%可靠
4. **提示规则**（AGENTS.md文件中的提示）——60-70%可靠
5. **Markdown规则**——40-50%可靠，其可靠性会随规则内容的复杂性增加而降低

## 提供的工具（Provided Tools）

### 脚本（Scripts）

| 脚本 | 运行时机 | 功能 |
|--------|------------|--------------|
| `install.sh` | 为每个项目执行一次 | 安装代码钩子和基础框架 |
| `pre-create-check.sh` | 在创建新的`.py`文件之前 | 列出现有的模块/函数，防止重复实现 |
| `post-create-validate.sh` | 在创建/编辑`.py`文件之后 | 检测重复代码、缺失的导入语句以及潜在的绕过规则 |
| `check-secrets.sh` | 在提交之前/按需执行 | 检查代码中是否存在硬编码的令牌、密钥或密码 |
| `create-deployment-check.sh` | 在设置部署验证机制时 | 生成`.deployment-check.sh`脚本、检查列表以及git钩子模板 |
| `install-skill-feedback-loop.sh` | 在设置技能更新自动化机制时 | 实现技能更新的自动检测和提交功能 |

### 资源（Assets）

| 资源 | 用途 |
|-------|---------|
| `pre-commit-hook` | 可立即安装的git钩子，用于阻止绕过规则和泄露敏感信息的行为 |
| `registry-template.py` | 项目模块注册表的`__init__.py`模板文件 |

### 参考资料（References）

| 文件 | 内容 |
|------|----------|
| `enforcement-research.md` | 关于为何代码检查比提示更有效的研究 |
| `agents-md-template.md` | 包含强制执行规则的AGENTS.md模板文件 |
| `deployment-verification-guide.md` | 防止部署漏洞的完整指南 |
| `skill-update-feedback.md` | 实现技能更新自动反馈的机制 |
| `SKILL_CN.md` | 本文档的中文翻译版本 |

## 使用流程（Usage Workflow）

### 设置新项目（Setting up a new project）

```bash
bash scripts/install.sh /path/to/project
```

### 在创建新的`.py`文件之前（Before creating any new `.py` file）

```bash
bash scripts/pre-create-check.sh /path/to/project
```

查看输出结果。如果现有的函数能够满足你的需求，请直接使用它们。

### 创建/编辑`.py`文件后（After creating/editing a `.py` file）

```bash
bash scripts/post-create-validate.sh /path/to/new_file.py
```

在继续下一步之前，先修复所有出现的警告。

### 设置部署验证机制（Setting up deployment verification）

```bash
bash scripts/create-deployment-check.sh /path/to/project
```

此步骤会生成以下文件：
- `.deployment-check.sh`：自动验证脚本
- `DEPLOYMENT-CHECKLIST.md`：完整的部署工作流程文档
- `.git-hooks/pre-commit-deployment`：git钩子模板

**后续步骤：**
1. 为`.deployment-check.sh`脚本添加针对你的集成点的测试用例
2. 在`DEPLOYMENT-CHECKLIST.md`中详细记录你的部署流程
3. 安装git钩子

详细指南请参阅`references/deployment-verification-guide.md`。

### 修改AGENTS.md文件（Adding to AGENTS.md）

从`references/agents-md-template.md`中复制模板，并根据你的项目需求进行定制。

## 中文文档（Chinese Documentation）

本技能的完整中文翻译版本请参阅`references/SKILL_CN.md`。

## 常见的代理行为问题（Common Agent Failure Modes）

### 1. 代码重复实现（Reimplementation, Bypass Pattern）
**症状：**代理生成了“快速版本”的代码，而不是导入经过验证的代码。
**解决方法：**使用`pre-create-check.sh`、`post-create-validate.sh`以及git钩子进行检测。

### 2. 硬编码的敏感信息（Hardcoded Secrets）
**症状：**代码中直接使用了密钥或令牌，而非从环境变量中获取。
**解决方法：**使用`check-secrets.sh`脚本进行检测，并通过git钩子进行监控。

### 3. 部署遗漏（Deployment Gap）
**症状：**虽然开发了新功能，但忘记将其集成到生产环境中，导致用户无法使用。
**示例：**更新了`notify.py`文件，但定时任务仍然使用旧版本。
**解决方法：**使用`.deployment-check.sh`脚本和git钩子进行检测。

**注意：**这是最难发现的错误类型，因为：
- 手动测试时代码可以正常运行
- 代理在编写代码后会标记任务为“已完成”
- 问题通常只有在用户反馈时才会被发现。

**解决方案：**在允许任务标记为“已完成”之前，实施端到端的自动验证。

### 4. 技能更新遗漏（Skill Update Gap, META - NEW）
**症状：**虽然开发了新的功能改进，但忘记更新相关技能的配置文件。
**示例：**为项目A实现了部署验证机制，但由于其他项目未更新技能配置，这些改进无法生效。
**解决方法：**使用`install-skill-feedback-loop.sh`实现自动检测和半自动提交功能。

**说明：**这是一种“元级失败模式”（meta-failure mode），因为：
- 它涉及到了改进机制本身的管理问题
- 如果不进行修复，这些改进将无法被其他项目共享
- 通过自动检测和半自动提交，可以确保改进能够被及时应用。

## 关键原则（Key Principles）

> 不要增加更多的Markdown规则，而是优先采用强制性的执行机制。
> 如果代理持续违反规范，不要编写更严格的规则，而是直接设置相应的钩子来阻止违规行为。
>
> **推论：**如果代理经常忘记执行某些操作，不要只是提醒它，而是通过代码钩子在提交前自动进行检查。