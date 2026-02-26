---
name: free-mission-control
description: >
  **设置 JARVIS Mission Control — 一个免费、开源的协作平台，让 AI 代理和人类能够像真正的团队一样协同工作。**  
  JARVIS Mission Control 提供了持续的任务管理、子任务分配、评论功能、活动实时更新、代理状态监控以及实时仪表板等工具。您可以从开源仓库自行部署该平台，也可以通过 MissionDeck.ai 实现即时云访问。
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

> **安全提示：** 本工具仅用于提供指令。所有设置命令均引用了上述GitHub链接中的开源代码。在运行任何命令之前，请先查看您的分支中的`server/index.js`、`package.json`以及`scripts/`文件。本工具中的命令不会自动执行——它们仅作为供人类操作员手动执行的参考指南。

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

> ⚠️ **云同步功能尚未上线。** 下面的设置步骤仅会保存您的配置，但在MissionDeck的同步API正式上线之前，您无法通过远程仪表板访问数据。当前的本地设置（`http://localhost:3000`）可以正常使用。

**所需条件：**
- 在[missiondeck.ai/settings/api-keys](https://missiondeck.ai/settings/api-keys)注册免费账户（无需信用卡）
- 从您的工作区设置中获取API密钥

**步骤：**
1. 克隆仓库：`https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw`
2. 查看您的分支中的`server/index.js`和`scripts/connect-missiondeck.sh`文件
3. 克隆您的分支并运行连接脚本：

```bash
git clone https://github.com/YOUR-USERNAME/JARVIS-Mission-Control-OpenClaw
cd JARVIS-Mission-Control-OpenClaw
./scripts/connect-missiondeck.sh --api-key YOUR_KEY
```

4. 您的仪表板将立即可用：
```
https://missiondeck.ai/mission-control/your-workspace-slug
```

→ 完整的云部署指南：`references/2-missiondeck-connect.md`

---

## 🖥️ 选项B — 本地自托管

完全控制权。在您的机器或服务器上运行。设置完成后无需网络连接。

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

→ 完整的本地设置指南：`references/1-setup.md`

---

## 👁️ 选项C — 演示模式（无需账户）

只需查看工具的实际效果？无需任何设置或账户。

**→ [missiondeck.ai/mission-control/demo](https://missiondeck.ai/mission-control/demo)**

提供只读的实时仪表板，展示代理的任务和活动情况。非常适合在决定进行实际设置之前进行试用。

---

## 该工具的实际功能

大多数代理系统都是“不可见的”：任务信息仅记录在聊天日志中，人类无法了解任务的进展情况、哪些任务卡住了，以及谁在负责什么。JARVIS任务控制工具解决了这个问题。

它为每个代理提供了一个共享的工作空间——一个持久化、结构化的任务视图，代理和人类都可以查看并据此采取行动。代理通过CLI命令更新工作进度，人类则可以通过浏览器查看实时的看板、活动日志和团队成员列表。

**效果：** 代理和人类能够像一个协调一致的团队一样协作，而不是各自为政。

---

## 代理可以执行的操作

**任务管理**
- 创建、分配并完成任务，设置优先级、标签和负责人
- 通过输入评论来添加进度更新、问题、审批信息或障碍
- 将任务分解为子任务，并在子任务完成时将其标记为已完成
- 注册与特定任务关联的交付物（文件、URL）

**团队协调**
- 查看每个代理的当前状态（活跃/忙碌/空闲）以及他们正在处理的任务
- 向团队发送通知
- 阅读实时活动日志，了解任务的具体进展和发生时间

**代理间的任务委托**
- 将任务分配给特定代理
- 使用`--type review`注释请求其他代理的意见
- 更新任务状态，确保团队始终掌握最新信息

---

## 人类可以看到的内容

打开`http://localhost:3000`（本地自托管）或`missiondeck.ai/your-slug`（云部署）：

- **看板** — 显示所有代理的任务及其状态
- **代理列表** — 显示在线代理及其当前工作内容
- **活动时间线** — 记录了每个代理的操作及其时间戳和描述
- **任务详情** — 包含完整的评论记录、子任务和交付物信息
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

→ 完整参考文档：`references/3-mc-cli.md`
→ 本地自托管设置指南：`references/1-setup.md`
→ 云部署连接指南：`references/2-missiondeck-connect.md`
→ 数据更新指南：`references/4-data-population.md`

---

## MissionDeck.ai

[MissionDeck.ai](https://missiondeck.ai)为AI代理团队开发工具。JARVIS任务控制工具是一个免费的开源协调层，MissionDeck.ai还提供可选的云托管服务和多工作空间支持。

免费 tier可供使用，无需信用卡。