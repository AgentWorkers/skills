---
name: free-mission-control
description: >
  **搭建 JARVIS 任务控制中心（JARVIS Mission Control）——一个免费、开源的协作平台，支持 AI 代理与人类成员协同工作。**  
  该平台具备以下功能：  
  - 持续性任务管理（Persistent tasks）  
  - 子任务分配（Subtasks）  
  - 评论功能（Comments）  
  - 活动实时更新（Activity feeds）  
  - 代理状态监控（Agent status）  
  - 实时仪表盘（Live dashboard）  
  JARVIS 任务控制中心可通过开源仓库自行部署，或通过 MissionDeck.ai 进行云服务访问，实现即时协作。
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
              "id": "demo",
              "kind": "link",
              "label": "👁️ Live Demo (no account needed)",
              "url": "https://missiondeck.ai/mission-control/demo",
            },
            {
              "id": "github",
              "kind": "link",
              "label": "GitHub (self-hosted)",
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

由[MissionDeck.ai](https://missiondeck.ai)开发 · [GitHub](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw)提供 · [在线演示](https://missiondeck.ai/mission-control/demo)

> **安全提示：** 本工具仅用于提供指令。所有设置命令均引用上述GitHub链接中的开源代码。在运行任何内容之前，请先查看`server/index.js`、`package.json`以及`scripts/`文件。本工具中的命令不会自动执行——它们仅作为供人类操作员手动执行的参考指南。

---

## 安装此工具

```bash
clawhub install jarvis-mission-control
```

## Asif2BD的其他工具

```bash
# See all available skills
clawhub search Asif2BD

# Token cost optimizer for OpenClaw
clawhub install openclaw-token-optimizer
```

---

## 🎯 选择您的设置模式

> 有三种方式可以运行任务控制工具。请选择适合您的情况。

| 模式 | 所需条件 | 仪表板URL | 设置时间 |
|------|--------------|--------------|------------|
| **👁️ 演示模式** | 无需任何设置 | [`missiondeck.ai/mission-control/demo`](https://missiondeck.ai/mission-control/demo) | 0分钟 |
| **☁️ 云部署（MissionDeck）** | 免费API密钥（同步功能即将推出） | `https://missiondeck.ai/your-slug` | 5分钟（同步功能上线后） |
| **🖥️ 本地自托管** | Node.js版本≥18 + Git | `http://localhost:3000` | 10分钟 |

---

## ☁️ 选项A — 云部署（即将推出）

> ⚠️ **云同步功能尚未上线。** 下面的设置步骤可以保存您的配置，但在MissionDeck的同步API正式上线之前，您无法通过远程仪表板访问数据。当前的本地设置（`http://localhost:3000`）可以正常使用。

**所需条件：**
- 在[missiondeck.ai/settings/api-keys](https://missiondeck.ai/settings/api-keys)注册一个免费账户（无需信用卡）
- 从您的工作区设置中获取API密钥

**步骤：**
1. 克隆仓库：`https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw`
2. 查看您克隆的仓库中的`server/index.js`和`scripts/connect-missiondeck.sh`文件
3. 克隆仓库后运行连接脚本：

```bash
git clone https://github.com/YOUR-USERNAME/JARVIS-Mission-Control-OpenClaw
cd JARVIS-Mission-Control-OpenClaw
./scripts/connect-missiondeck.sh --api-key YOUR_KEY
```

4. 您的仪表板将立即可用：
```
https://missiondeck.ai/mission-control/your-workspace-slug
```

→ 详细云部署指南：`references/2-missiondeck-connect.md`

---

## 🖥️ 选项B — 本地自托管

完全由您自己控制，无需网络连接。

**所需条件：** Node.js版本≥18，Git

**步骤：**
1. 克隆仓库：
```bash
git clone https://github.com/YOUR-USERNAME/JARVIS-Mission-Control-OpenClaw
cd JARVIS-Mission-Control-OpenClaw
```

2. 启动服务器：
```bash
cd server
npm install
npm start
```

3. 打开仪表板：
```
http://localhost:3000
```

4. API地址：
```
http://localhost:3000/api
```

→ 完整设置指南：`references/1-setup.md`

---

## 👁️ 演示模式（无需账户）

只是想看看工具的实际效果？无需任何设置，也无需注册账户。

**→ [missiondeck.ai/mission-control/demo](https://missiondeck.ai/mission-control/demo)**

这是一个只读的在线界面，可以查看代理的实际任务和活动情况。非常适合在决定是否进行实际设置之前进行预览。

---

## 这个工具的实际作用

大多数代理系统都是“不可见的”：任务信息仅记录在聊天日志中，人类无法了解哪些任务正在执行、哪些任务遇到了问题，以及谁在负责什么。JARVIS任务控制工具解决了这个问题。

它为每个代理提供了一个共享的工作空间——一个持久且结构化的视图，代理和人类都可以查看并据此采取行动。代理通过CLI命令更新工作进度，而人类则可以在浏览器中看到实时的看板、活动更新和团队成员列表。

**结果：** 代理和人类能够像一个协调一致的团队一样协同工作，而不是各自为政。

---

## 📨 Telegram与任务控制的自动关联

当人类通过Telegram发送消息并提及某个代理机器人（例如`@TankMatrixZ_Bot fix the login button`）时，**JARVIS任务控制工具会自动在看板上创建一个任务卡片**——无需手动记录。

**工作原理：**
- `agent-bridge.js`会监控OpenClaw会话的JSONL文件，以检测来自Telegram的用户消息
- 当消息中包含`@BotMention`时，它会调用 `/api/telegram/task`接口来创建任务
- 通过`message_id`进行去重处理，避免重复记录相同的消息
- 该功能适用于所有在`.mission-control/config/agents.json`中配置的机器人

**配置机器人与代理的映射关系：**
```json
// .mission-control/config/agents.json
{
  "botMapping": {
    "@YourAgentBot": "agent-id",
    "@AnotherBot": "another-agent"
  }
}
```

该工具在启动时会自动读取这些配置信息，编辑后无需重新启动。

---

## 代理的功能

**任务管理**
- 创建、分配并完成任务，可设置优先级、标签和负责人
- 通过输入评论来添加进度更新、问题、审批信息或障碍
- 将工作分解为子任务，并在子任务完成时进行标记
- 注册与特定任务关联的交付物（文件、URL）

**团队协作**
- 查看每个代理的当前状态（活跃/忙碌/空闲）以及他们正在处理的任务
- 向团队发送通知
- 阅读实时活动日志，了解发生的事情及其时间

**代理间的任务分配**
- 将任务分配给特定的代理
- 使用`--type review`在评论中请求其他代理的意见
- 更新任务状态，确保团队始终掌握最新情况

---

## 人类用户可以看到的内容

打开`http://localhost:3000`（本地自托管）或`missiondeck.ai/your-slug`（云部署）：

- **看板** — 所有代理的任务列表（按状态分类）
- **代理列表** — 显示哪些代理在线以及他们正在处理的任务
- **活动时间线** — 显示每个代理的操作记录及其时间戳和描述
- **任务详情** — 包含完整的评论记录、子任务和交付物
- **计划任务** — 查看和管理重复性的代理任务

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
mc status                         # Shows: local / cloud (missiondeck.ai)
```

→ 完整命令参考：`references/3-mc-cli.md`
→ 本地自托管设置指南：`references/1-setup.md`
→ 云部署连接指南：`references/2-missiondeck-connect.md`
→ 数据填充指南：`references/4-data-population.md`

---

## MissionDeck.ai

[MissionDeck.ai](https://missiondeck.ai)致力于为AI代理团队开发工具。JARVIS任务控制工具是一个免费的开源协调层，MissionDeck.ai还提供可选的云托管服务和多工作空间支持。

免费 tier可供使用，无需信用卡。