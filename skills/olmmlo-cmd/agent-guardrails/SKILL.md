---
name: agent-guardrails
version: "1.1.0"
author: "jzOcb"
license: "MIT"
category: "development-tools"
description: "防止 AI 代理秘密绕过您的规则。通过 Git 钩子（git hooks）、秘密检测机制、部署验证以及导入注册表（import registries）来实现强制性的规则执行。这一方案源于实际生产环境中的问题，例如服务器崩溃、令牌泄露（token leaks）以及代码被篡改（code rewrites）。该方案可与 Claude Code、Clawdbot 和 Cursor 等工具配合使用。只需安装一次，即可永久生效。"
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
repository: "https://github.com/jzOcb/agent-guardrails"
homepage: "https://github.com/jzOcb/agent-guardrails#readme"
bugs: "https://github.com/jzOcb/agent-guardrails/issues"
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

该步骤会安装Git的预提交钩子（pre-commit hook），创建一个注册表模板（registry template），并将检查脚本（check scripts）复制到你的项目中。

## 执行机制的层级结构

1. **代码钩子**（git预提交钩子、代码创建前/后的检查）——100%可靠
2. **架构约束**（注册表机制、导入检查）——95%可靠
3. **自我验证机制**（代理程序自动检查自身代码）——80%可靠
4. **提示性规则**（如AGENTS.md中的规则、系统提示）——60-70%可靠
5. **Markdown规则**——40-50%可靠，其有效性会随着规则内容的复杂度增加而降低

## 提供的工具

### 脚本

| 脚本 | 运行时机 | 功能 |
|--------|------------|--------------|
| `install.sh` | 为每个项目运行一次 | 安装所需的钩子和基础框架 |
| `pre-create-check.sh` | 在创建新的`.py`文件之前 | 列出已存在的模块/函数，防止重复实现 |
| `post-create-validate.sh` | 在创建或编辑`.py`文件之后 | 检测重复代码、缺失的导入语句以及潜在的绕过规则 |
| `check-secrets.sh` | 在提交之前/按需执行 | 检查代码中是否存在硬编码的令牌、密钥或密码 |
| `create-deployment-check.sh` | 在设置部署验证机制时 | 生成`.deployment-check.sh`脚本、验证清单以及Git钩子模板 |
| `install-skill-feedback-loop.sh` | 在设置技能更新自动化机制时 | 实现技能更新的自动检测和提交流程 |

### 提供的资源

| 资源 | 用途 |
|-------|---------|
| `pre-commit-hook` | 可直接安装的Git钩子，用于阻止绕过规则和泄露敏感信息的行为 |
| `registry-template.py` | 项目模块注册表的`__init__.py`模板 |

### 参考资料

| 文件 | 内容 |
|------|----------|
| `enforcement-research.md` | 关于为何应优先使用代码检查而非提示性规则的研究 |
| `agents-md-template.md` | 包含强制执行规则的AGENTS.md模板 |
| `deployment-verification-guide.md` | 完整的部署验证指南 |
| `skill-update-feedback.md` | 技能更新反馈机制的实现细节 |
| `SKILL_CN.md` | 本文档的中文翻译版本 |

## 使用流程

### 设置新项目

```bash
bash scripts/install.sh /path/to/project
```

### 在创建新的`.py`文件之前

```bash
bash scripts/pre-create-check.sh /path/to/project
```

请查看输出结果。如果现有的函数能够满足你的需求，请直接使用它们。

### 在创建或编辑`.py`文件之后

```bash
bash scripts/post-create-validate.sh /path/to/new_file.py
```

在继续下一步之前，请先修复所有出现的警告。

### 设置部署验证机制

```bash
bash scripts/create-deployment-check.sh /path/to/project
```

该步骤会生成以下文件：
- `.deployment-check.sh`：自动化的部署验证脚本
- `DEPLOYMENT-CHECKLIST.md`：完整的部署流程文档
- `.git-hooks/pre-commit-deployment`：Git钩子模板

**后续步骤：**
1. 为`.deployment-check.sh`脚本添加针对你的集成点的测试用例
2. 在`DEPLOYMENT-CHECKLIST.md`中记录你的部署流程
3. 安装Git钩子

详细指南请参阅`references/deployment-verification-guide.md`。

### 修改AGENTS.md文件

请从`references/agents-md-template.md`中复制模板，并根据你的项目需求进行定制。

## 中文文档

本文档的中文翻译版本请参阅`references/SKILL_CN.md`。

## 常见的代理行为问题

### 1. 代码重复实现（绕过规则）
**症状：**代理程序生成了“快速版本”的代码，而不是导入经过验证的代码。
**解决方法：** 使用`pre-create-check.sh`、`post-create-validate.sh`以及Git钩子进行检测。

### 2. 硬编码的敏感信息
**症状：**代码中直接使用了密钥或令牌，而非从环境变量中获取。
**解决方法：** 使用`check-secrets.sh`脚本进行检测，并结合Git钩子进行监控。

### 3. 部署遗漏
**症状：**虽然开发了新功能，但忘记将其集成到生产环境中，导致用户无法使用。
**示例：**更新了`notify.py`文件，但系统仍使用旧版本。
**解决方法：** 使用`.deployment-check.sh`脚本和Git钩子进行检测。

**注意：**这种问题最难发现，因为：
- 手动测试时代码可以正常运行
- 代理程序在编写代码后会标记任务为“已完成”
- 问题通常只有在用户反馈时才会被发现。

**解决方案：**在允许任务标记为“已完成”之前，实施端到端的自动化验证。

### 4. 技能更新遗漏
**症状：**虽然开发了新的功能改进，但忘记更新相关的技能配置。
**解决方法：** 使用`install-skill-feedback-loop.sh`脚本实现自动检测和半自动提交机制。

**说明：**这是一种“元级故障模式”（meta-failure mode），因为它涉及到了自动化执行机制的改进：
- 如果不进行修复，这些改进将孤立存在；
- 通过修复后，这些改进会自动得到应用。

**关键原则：**
- 不要增加过多的Markdown规则，而是优先采用自动化执行机制。
- 如果代理程序持续违反规则，不要试图编写更严格的规则，而是直接设置钩子来阻止违规行为。
- 如果代理程序经常忘记执行某些操作，不要只是提醒它，而是通过自动化机制强制其完成这些操作。

> **推论：**如果代理程序经常忘记执行某些步骤，不要只是提醒它，而是通过自动化机制确保其始终按照规定执行。