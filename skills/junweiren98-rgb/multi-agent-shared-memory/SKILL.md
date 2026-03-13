---
name: shared-memory
description: 在多个 OpenClaw 代理之间设置共享内存，以确保它们保持同步，从而避免用户重复说明相同的内容。当用户拥有 2 个或更多的代理（工作区）时，可以使用此功能来实现知识共享、会话摘要的同步以及长期记忆的维护。该功能适用于以下场景：用户希望多个代理之间能够共享信息、避免重复对话内容，以及实现跨代理的协同工作。相关关键词包括“共享内存”、“代理同步”、“多代理内存”、“代理间数据共享”等。
---
# 多代理OpenClaw的共享内存机制

通过共享目录结构和同步协议，实现多个OpenClaw代理之间的知识、对话上下文以及长期记忆的共享。

## 问题

当运行多个OpenClaw代理（例如一个主要助手和一个专家）时，每个代理在每次会话开始时都会处于“空白状态”，对其他代理与你讨论的内容一无所知。这导致你需要反复向每个代理传达相同的对话内容。

## 解决方案概述

在其中一个代理的工作空间中创建一个名为`shared-knowledge/`的目录，所有参与的代理都可以访问该目录。每个代理执行以下操作：
1. **会话开始时**：读取共享内存中的内容。
2. **会话结束时**：更新自己的同步文件。
3. **在做出重要决策时**：将相关信息添加到共享的长期记忆中。

## 设置步骤

### 第一步：创建共享目录

选择一个工作空间作为主机（通常是主要代理），并创建相应的目录结构：

```
shared-knowledge/
├── SHARED-MEMORY.md          # Shared long-term memory
├── README.md                 # Usage rules (optional)
├── sync/                     # Per-agent conversation summaries
│   ├── agent-a-latest.md     # Agent A's latest summary
│   └── agent-b-latest.md     # Agent B's latest summary
└── projects/                 # Shared project documents (optional)
```

使用`assets/`目录中的模板来生成这些文件：

```bash
# From the skill directory:
cp assets/SHARED-MEMORY.template.md  <workspace>/shared-knowledge/SHARED-MEMORY.md
cp assets/README.template.md         <workspace>/shared-knowledge/README.md
cp assets/sync-latest.template.md    <workspace>/shared-knowledge/sync/<agent-name>-latest.md
```

请将占位符（`{{AGENT_A_NAME}}`、`{{AGENT_B_NAME}}`等）替换为实际的代理名称或相应的标识符。

### 第二步：配置每个代理的`AGENTS.md`文件

在每个参与代理的`AGENTS.md`文件中添加共享内存的配置信息。具体需要添加的内容请参考`references/agents-protocol-snippet.md`文件。

每个代理需要添加的关键内容：
- **会话开始时**：读取`SHARED-MEMORY.md`文件以及其他代理的同步文件。
- **会话结束时**：将对话中的重要内容更新到自己的同步文件中。
- **在做出重要决策时**：更新`SHARED-MEMORY.md`文件。

### 第三步：确保文件访问权限

两个代理都需要具备对`shared-knowledge/`目录的读写权限：
- **在同一台机器上但位于不同的工作空间中**：在`AGENTS.md`文件中使用符号链接或绝对路径来引用该目录。
- **在同一台机器上但位于嵌套的工作空间中**：如果工作空间B位于同一个`.openclaw/`目录内，可以使用相对路径。

**Windows下的符号链接示例：**
```powershell
New-Item -ItemType SymbolicLink -Path "<workspace-b>\shared-knowledge" -Target "<workspace-a>\shared-knowledge"
```

**Linux/Mac下的符号链接示例：**
```bash
ln -s <workspace-a>/shared-knowledge <workspace-b>/shared-knowledge
```

## 协议规则

### 共享内存中可以包含的内容：
- ✅ 用户信息、偏好设置、决策结果
- ✅ 项目背景和进度
- ✅ 对话摘要（每个代理的同步文件）
- ✅ 共享的参考文档

### 不能共享的内容：
- ❌ 代理的个人信息文件（如`SOUL.md`、`IDENTITY.md`）
- ❌ 私人记忆和角色设置
- ❌ 凭据、令牌、密码

### 同步规则：
| 触发条件 | 操作 |
|---------|--------|
| 会话开始 | 读取`SHARED-MEMORY.md`文件以及其他代理的同步文件 |
| 会话结束时 | 将对话中的重要内容更新到自己的同步文件中 |
| 作出重要决策时 | 更新`SHARED-MEMORY.md`文件 |

## 自定义设置：
- **超过2个代理的情况**：在`sync/`目录下为每个代理创建一个同步文件。每个代理需要读取其他所有代理的同步文件。
- **项目特定的文档**：使用`projects/`子目录来存储项目相关的共享文档。
- **选择性共享**：如果某个代理仅具有读取权限，可以配置为仅读取共享内存内容，而不能进行写入操作。