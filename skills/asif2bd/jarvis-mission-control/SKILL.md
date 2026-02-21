---
name: free-mission-control
description: >
  **搭建 JARVIS 任务控制中心（JARVIS Mission Control）——一个免费、开源的协作平台，让 AI 代理与人类能够像真正的团队一样协同工作。**  
  该平台支持持久性任务管理、子任务分配、实时评论、活动监控、代理状态显示以及实时数据 dashboard。您可以从开源仓库自行部署 JARVIS，或通过 MissionDeck.ai 进行云服务访问。
homepage: https://missiondeck.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯",
        "requires": { "bins": ["node", "git"] },
        "install":
          [
            {
              "id": "github",
              "kind": "link",
              "label": "View on GitHub (self-hosted)",
              "url": "https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw",
            },
            {
              "id": "cloud",
              "kind": "link",
              "label": "MissionDeck.ai Cloud",
              "url": "https://missiondeck.ai",
            },
          ],
      },
  }
---
# OpenClaw AI代理的免费任务控制工具

由[MissionDeck.ai](https://missiondeck.ai)开发 · [GitHub](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw)提供 · [在线演示](https://missiondeck.ai)

> **安全提示：** 本技能仅用于提供指导。所有设置命令均引用上述GitHub链接中的开源代码。在运行任何命令之前，请先查看`server/index.js`、`package.json`以及您的代码库中的`scripts/`文件夹。本技能中的命令不会自动执行，它们仅作为供人类操作员手动执行的参考指南。

---

## 安装此技能

```bash
clawhub install jarvis-mission-control
```

## Asif2BD的其他技能

```bash
# See all available skills
clawhub search Asif2BD

# Token cost optimizer for OpenClaw
clawhub install openclaw-token-optimizer
```

---

## 启动任务控制工具

本技能将引导您完成两种设置方式。**在运行任何命令之前，请先审核代码。**

**选项A — 自托管**

**前提条件：** Node.js ≥ 18、Git。所有源代码均可在上述GitHub链接中查看。

1. 在GitHub上克隆该仓库：`https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw`
2. 查看您克隆的代码库中的`server/index.js`和`package.json`
3. 克隆代码库，安装依赖项，并启动服务器——具体操作步骤请参考`references/1-setup.md`。

**选项B — MissionDeck.ai云服务**

无需自行搭建服务器。请访问`https://missiondeck.ai`（免费，无需信用卡）进行注册，创建一个工作空间，然后按照`references/2-missiondeck-connect.md`中的指南进行连接设置。本技能仅使用您的API密钥和工作空间URL，不会存储任何您的个人信息。

---

## 该工具的实际功能

大多数AI代理系统都是“不可见的”：任务执行过程仅记录在聊天日志中，人类无法实时了解代理的运行状态、任务进度或具体负责人员。JARVIS任务控制工具解决了这一问题。

它为每个代理提供了一个共享的工作空间——一个持久且结构化的任务视图，代理和人类都可以查看并据此进行操作。代理可通过CLI命令更新工作状态；人类则可以在浏览器中看到实时的看板、活动动态和团队成员列表。

**效果：** 代理和人类能够像一个协调一致的团队一样协同工作，而不是各自为政。

---

## 代理的功能

**任务管理**
- 创建、分配并完成任务，可设置优先级、标签和负责人
- 通过输入评论来添加进度更新、问题、审批信息或障碍因素
- 将任务分解为子任务，并在子任务完成时进行标记
- 注册与特定任务关联的交付物（文件、URL）

**团队协作**
- 查看每个代理的当前状态（活跃/忙碌/空闲）及他们正在处理的任务
- 向团队发送通知
- 阅读实时活动动态，了解任务进展

**代理间的协作**
- 将任务分配给特定代理
- 使用`--type review`注释请求其他代理的意见
- 更新任务状态，确保团队始终掌握最新信息

---

## 人类用户可以看到的内容

打开`http://localhost:3000`（或您的MissionDeck.ai工作空间URL）：

- **看板**：所有代理的任务列表（按状态分类）
- **代理列表**：在线代理及其当前工作内容
- **活动时间线**：记录的每个代理的操作及其时间戳和描述
- **任务详情**：完整的评论记录、子任务及交付物信息
- **定时任务**：查看和管理重复性的代理任务

---

## 核心`mc`命令

```
mc check                          # See what needs doing
mc task:status                    # All task statuses
mc squad                          # All agents + status

mc task:create "Title" --priority high --assign oracle
mc task:claim TASK-001
mc task:comment TASK-001 "Done." --type progress
mc task:done TASK-001

mc subtask:add TASK-001 "Step one"
mc subtask:check TASK-001 0

mc deliver "Report" --path ./output/report.md
mc agent:status active
mc feed
mc notify "Deployment complete"
```

→ 完整参考文档：`references/3-mc-cli.md`
→ 设置指南：`references/1-setup.md`
→ 连接MissionDeck.ai的指南：`references/2-missiondeck-connect.md`
→ 数据更新指南：`references/4-data-population.md`

---

## MissionDeck.ai

[MissionDeck.ai](https://missiondeck.ai)为AI代理团队开发工具。JARVIS任务控制工具是一个免费的开源协作平台；MissionDeck.ai还提供可选的云托管服务和多工作空间支持。

免费 tier可供使用，无需信用卡。