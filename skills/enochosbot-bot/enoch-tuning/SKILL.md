---
name: enoch-tuning
description: 这是一个经过实战考验的 OpenClaw 配置方案，其中包含了预先设置的身份验证机制、内存架构、安全协议以及自动化功能。无需花费数周时间进行反复调试与试验——只需安装该配置文件，即可立即使用一个具备生产环境使用条件的代理程序（agent）。
homepage: https://github.com/enochosbot-bot/enoch-tuning
metadata:
  {
    "openclaw":
      {
        "emoji": "🔮",
        "os": ["darwin", "linux"],
      },
  }
---
# enoch-tuning

大多数人在设置AI代理时，都会得到一个“空白的状态”——没有记忆，没有个性，也没有任何规则。他们需要花费数周时间来弄清楚为什么这个代理总是忘记事情，为什么它的回答听起来像聊天机器人，以及为什么在它们犯错时它们不会提出反对意见。

而这个技能则省去了所有这些麻烦。

你安装的是一套经过生产环境测试的身份识别和记忆系统：包括决策启发式规则、硬性规定、安全协议、内存架构以及自动化流程，这些内容都是经过数月开发和完善才最终形成的。

## 你将获得的内容

- **Pre-wired SOUL.md**：包含决策启发式规则、硬性规定以及防止错误行为的机制。这是决定代理性能的关键因素，它让代理区别于普通的聊天机器人。
- **AGENTS.md**：包含完整的操作规则：验证协议、状态报告机制、与Claude Code的协调方式、代理的离线行为管理、子代理管理机制以及防止错误行为的措施。
- **Memory architecture**：一个分为6个类别的内存管理系统（用于存储决策、人员信息、经验教训、承诺事项、个人偏好和项目信息），以及用于存储日常日志的VAULT_INDEX文件。
- **MISSION.md模板**：基于任务驱动的代理行为模式。代理会主动询问“哪些行为能让我们更接近目标”，而不是被动等待指令。
- **验证协议**：防止过时数据、虚假的子代理完成结果以及未经验证的信息传递给你。
- **设置脚本**：用于配置代理的内存目录结构和身份文件的锁定机制。

## 安装步骤

### 第1步：复制模板
```bash
cp skills/enoch-tuning/templates/SOUL.md ~/.openclaw/workspace/SOUL.md
cp skills/enoch-tuning/templates/AGENTS.md ~/.openclaw/workspace/AGENTS.md
cp skills/enoch-tuning/templates/USER.md ~/.openclaw/workspace/USER.md
cp skills/enoch-tuning/templates/MEMORY.md ~/.openclaw/workspace/MEMORY.md
cp skills/enoch-tuning/templates/MISSION.md ~/.openclaw/workspace/MISSION.md
cp skills/enoch-tuning/templates/ops/verification-protocol.md ~/.openclaw/workspace/ops/verification-protocol.md
```

### 第2步：创建内存结构
```bash
bash skills/enoch-tuning/setup/memory-structure.sh ~/.openclaw/workspace
```

### 第3步：个性化设置（必选）
请编辑以下文件，其中[BRACKETS]内的内容均为占位符：
- `SOUL.md`：代理的名称、世界观和整体风格。
- `USER.md`：你的个人信息、目标以及工作节奏。
- `MEMORY.md`：你的平台设置和相关关键信息。
- `MISSION.md`：你的任务声明（一句话）。

### 第4步：锁定身份文件
```bash
bash skills/enoch-tuning/setup/lock-identity.sh ~/.openclaw/workspace
```

### 第5步：首次对话
向你的代理介绍你的名字、你的工作内容，以及你希望它自动完成的3项最重要任务，同时明确指出哪些事情它绝对不能未经询问就自行执行。从这一步开始，代理的行为模式将逐渐形成。

## 在不了解相关内容之前，请勿更改以下内容：

- **SOUL.md中的硬性规定**：这些是不可更改的行为准则。
- **AGENTS.md中的错误预防机制**：它们保护你的系统免受基于聊天界面的配置更改带来的影响。
- **验证协议**：如果删除或修改该协议，可能会导致过时数据和虚假完成结果再次出现。
- **自动化层级设置**：这些规则决定了代理在什么情况下可以自主执行任务，什么情况下必须等待你的指令。

## 文件结构
```
skills/enoch-tuning/
├── SKILL.md                          ← this file
├── templates/
│   ├── SOUL.md                       ← identity template
│   ├── AGENTS.md                     ← operating rules template
│   ├── USER.md                       ← user intake template
│   ├── MEMORY.md                     ← long-term memory template
│   ├── MISSION.md                    ← mission statement template
│   └── ops/
│       └── verification-protocol.md  ← fact-checking protocol
└── setup/
    ├── memory-structure.sh           ← creates memory directories
    └── lock-identity.sh              ← locks SOUL.md + AGENTS.md
```