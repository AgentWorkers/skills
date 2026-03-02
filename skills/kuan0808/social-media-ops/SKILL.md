---
name: social-media-ops
description: 在 OpenClaw 上搭建一个完整的多品牌社交媒体管理团队。通过星形拓扑结构配置 7 个专业 AI 代理（团队领导、研究员、内容策略师、视觉设计师、操作员、工程师和审核员），实现持续的点对点交流（A2A）、三层记忆系统、共享知识库、审批工作流程以及品牌隔离功能。该方案适用于新社交媒体运营团队的组建、现有 OpenClaw 实例中多代理框架的添加，或当用户需要处理社交媒体管理、多品牌运营或内容团队设置相关任务时。
metadata:
  {
    "openclaw": {
      "emoji": "📱",
      "requires": {
        "bins": ["node"]
      }
    }
  }
---
# 社交媒体运营

## 概述

此技能配置了一个基于 OpenClaw 的完整人工智能驱动的社交媒体运营团队。它包括：

- **7 个专业代理**，采用星形拓扑结构（1 个领导者和 6 个专家）
- **持久的 A2A（代理对代理）会话**，以保持多代理工作流的上下文一致性
- **三层记忆系统**（包括 `MEMORY.md`、每日笔记和共享知识库）
- **共享知识库**，其中包含品牌资料、运营指南和领域知识
- **审批工作流**，确保所有内容在获得所有者批准前不会发布
- **品牌隔离**，每个品牌都有独立的频道、内容指南和资产目录
- **Cron 自动化**，用于每日记忆整合和每周知识库审查

## 可选依赖项

- **设计师代理的图像生成工具**：设计师代理需要在 `workspace-designer/skills/` 目录中安装图像生成工具才能生成图片。推荐使用 `nano-banana-pro`（基于 Gemini，免费 tier）。如果没有该工具，设计师只能生成文本形式的视觉简报，无法生成图片。

## 先决条件

在安装之前，请确保：
1. 已安装 OpenClaw v2026.2.26 或更高版本，并完成 `openclaw onboard` 过程
2. 至少存在一个认证配置文件（例如 Anthropic API 密钥）
3. `~/.openclaw/` 目录存在

## 快速入门

```
1. Install the skill (if not already in workspace/skills/)
2. Trigger setup: "Set up my social media operations team"
3. Follow the interactive onboarding (6 steps, ~10 minutes)
4. Start creating content!
```

## 上线流程

首次触发此技能时，会运行一个交互式设置流程。

### 第 1 步：检查先决条件

验证环境是否准备就绪：
- [ ] OpenClaw 已安装且 `openclaw onboard` 完成
- [ ] `~/.openclaw/` 目录存在
- [ ] 至少配置了一个认证配置文件

如果缺少任何先决条件，请指导用户解决后再继续。

### 第 2 步：团队设置

**所有 7 个代理将自动安装。** 不需要用户选择团队规模。

完整的团队成员包括：
| 代理 | 角色 |
|-------|------|
| 领导者 | 组织协调、路由管理、质量把控 |
| 研究员 | 市场研究、竞争对手分析 |
| 内容创作者 | 内容策略、文案撰写 |
| 设计师 | 视觉简报制作、图像生成 |
| 操作员 | 平台运营、任务调度 |
| 工程师 | 技术集成、自动化 |
| 审核员 | 独立的质量审核 |

**模型** — 所有代理都继承在 `openclaw onboard` 期间配置的模型（位于 `agents.defaults.model`）。无需为每个代理单独配置模型。

> **高级提示：** 如果后来希望运行更精简的团队，可以重新运行 `scaffold.sh --agents leader,content,designer,engineer` 来创建所需的代理组合。

### 第 3 步：运行搭建脚本

首先执行搭建脚本以创建所有目录和文件：

```bash
# 1. Create directories, copy templates, set up symlinks
bash scripts/scaffold.sh \
  --skill-dir "$(pwd)"

# 2. Merge agent configuration into openclaw.json
node scripts/patch-config.js \
  --config ~/.openclaw/openclaw.json
```

搭建脚本会创建：
- 各代理的工作空间目录（包含 `SOUL.md` 和 `AGENTS.md`）
- 共享知识库（包含所有模板文件）
- 从每个工作空间到共享目录的符号链接
- 领导者技能目录下的子技能（如 `instance-setup`、`brand-manager`）
- Cron 作业定义

配置补丁会合并到 `openclaw.json` 中：
- 代理定义（包括模型分配和工具限制）
- A2A 会话配置
- QMD 记忆路径（**仅在安装了 QMD 时启用**，否则跳过此步骤）
- 内部钩子

### 第 4 步：Telegram 设置

此步骤采用**引导式流程**——不要要求用户提供原始聊天 ID 或线程 ID。

#### 第 A 阶段：确认机器人令牌

1. 检查 `openclaw.json` 中的 `channelsTelegram.botToken` 是否存在
2. 如果存在 → 转到第 B 阶段
3. 如果不存在 → 指导用户：
   - 打开 Telegram，搜索 **@BotFather**
   - 发送 `/newbot` 并按照提示创建机器人
   - 复制机器人令牌并粘贴到 `openclaw.json` 的 `channelsTelegram.botToken` 位置

#### 第 B 阶段：选择频道模式

按以下顺序展示选项（建议选择 **Group+Topics**）：
1. **Group+Topics** — 最适合大多数设置
   - 品牌信息存储在 Telegram 超群组的主题帖中
   - 适用于单人操作员和多人团队
   - 需要一个启用了主题功能的超群组

2. **DM+Topics** — 私人替代方案，不需要群组
   - 每个品牌在机器人的私信中拥有自己的主题帖
   - 需要在机器人上启用线程模式（下面有详细指导）

3. **DM-simple** — 最简单的模式，没有品牌隔离
   - 与机器人的单次私信对话
   - 基于上下文的品牌路由（无主题）

4. **Group-simple** — 无品牌隔离的群组对话
   - 群组内的单次对话
   - 基于上下文的品牌路由（无主题）

#### 第 C 阶段：特定模式的配置

**如果选择 DM+Topics：**

1. 指导用户在机器人上启用线程模式：
   - 打开 Telegram，找到 **@BotFather**
   - 点击左下角的 **Open** 按钮打开 BotFather MiniApp
   - 在 MiniApp 中选择你的机器人
   - 进入 **Bot Settings**
   - 启用 **Thread Mode**
   - 完成后告诉我

2. 确认后，使用机器人令牌获取用户的聊天 ID：
   - 向机器人发送任意消息
   - 代理会从 `{{From}}` 中提取用户的聊天 ID 并将其写入频道配置

3. 自动创建 **Operations** 主题：
   ```bash
   node scripts/telegram-topics.js \
     --config ~/.openclaw/openclaw.json \
     --chat <USER_CHAT_ID> \
     --name "Operations"
   ```

4. 将生成的线程 ID 写入 `shared/operations/channel-map.md`

5. 更新 `cron/jobs.json` — 将 `{{OPERATIONS_CHANNEL}}` 替换为实际的运营频道地址（格式：`chatId:threadId`，例如 `123456789:7`）

**如果选择 Group+Topics：**

1. 检查用户是否已经拥有超群组：
   - 如果没有：指导他们创建一个超群组（创建群组 → 打开 “Topics” 功能）

2. 指导用户将机器人添加到超群组：
   - 将机器人设置为 **管理员** 并赋予 **Manage Topics** 权限
   - 在群组中发送一条消息

3. 代理从消息中提取群组聊天 ID：
   - 将群组聊天 ID 写入频道配置

4. 自动创建 **Operations** 主题：
   ```bash
   node scripts/telegram-topics.js \
     --config ~/.openclaw/openclaw.json \
     --chat <GROUP_CHAT_ID> \
     --name "Operations"
   ```

5. 将生成的线程 ID 写入 `shared/operations/channel-map.md`

6. 更新 `cron/jobs.json` — 将 `{{OPERATIONS_CHANNEL}}` 替换为实际的运营频道地址（格式：`chatId:threadId`，例如 `-100XXXXXXXXXX:7`）

**如果选择 DM-simple：**

1. 向机器人发送任意消息
2. 代理从消息中提取聊天 ID 并将其写入频道配置

**如果选择 Group-simple：**

1. 指导用户将机器人添加到群组并发送消息
2. 代理从消息中提取群组聊天 ID 并将其写入频道配置

### 第 5 步：实例设置 + 第一个品牌

完成搭建和 Telegram 配置后，运行子技能：

1. **实例设置**（`instance-setup` 技能）
   - 所有者姓名和时区
   - 通信语言（面向所有者的）
   - 默认内容语言
   - 机器人身份（名称、表情符号、个性设置）
   - 更新内容：`shared/INSTANCE.md`、`workspace/IDENTITY.md`

2. **第一个品牌**（`brand-manager add`）
   - 品牌 ID、显示名称、域名
   - 目标市场和内容语言
   - **主题创建**（对于使用 Topic 模式的场景）：
     - 代理调用 `scripts/telegram-topics.js` 为品牌创建一个主题
     - 脚本返回线程 ID
     - 代理将线程 ID 写入 `shared/operations/channel-map.md` 和品牌配置文件
   - 对于简单模式：无需创建主题，跳过此步骤
   - 创建：品牌资料、内容指南、领域知识文件、资产目录

### 第 6 步：验证 + 重启网关

1. **重启网关：**
   ```
   openclaw gateway restart
   ```

2. **运行诊断工具：**
   ```
   openclaw doctor
   ```
   此步骤验证：代理配置、DM 允许列表的继承性、会话状态、模型可用性以及工作空间的完整性。

3. **其他检查：**
   - [ ] 领导者能够回复消息
   - [ ] 至少有一个代理能够成功接收 `sessions_send` 消息

**可选：启用 QMD 语义记忆**

如果在第 3 步中 `patch-config.js` 报告 “未找到 qmd binary”，代理将使用基于文件的记忆系统（这也完全可以正常使用）。要启用增强型语义搜索：
- 说 “Set up QMD” 以运行 `qmd-setup` 子技能，该技能会指导你完成安装和配置。

**建议的安装后首次任务：**
1. 填写品牌资料：`shared/brands/{brand_id}/profile.md`
2. 测试内容创建：`为 {brand} 写一篇 Facebook 帖子`
3. 添加更多品牌：`添加一个新的品牌`
4. 设置发布计划：填写 `shared/operations/posting-schedule.md`

## 安装后

### 异步调度模型（v2.0.0+）

领导者使用**完全异步的调度方式**（`sessions_send` 的 `timeoutSeconds: 0`）来进行所有代理之间的通信。这意味着：
- 领导者**永远不会被阻塞**，随时可以响应所有者的请求。
- 代理的结果以会话间消息的形式发送给领导者；领导者根据 `AGENTS.md` 中的 “Handling Agent Reports” 流程处理这些消息。
- **过期任务检测** 由 Cron 作业（`stale-task-check`，每 10 分钟执行一次）处理，该作业会检查 `SCRATCH.md` 中处于 `[⏳]` 状态的待处理任务。
- **HEARTBEAT.md** 默认为空文件——定期检查由 Cron 作业完成，而不是通过心跳轮询。

### 秘密管理（可选）

为了集中管理 API 密钥，可以使用以下方法：
```
openclaw secrets audit      # Check for plaintext secrets in config
openclaw secrets configure  # Set up secret entries
openclaw secrets apply      # Activate secrets
openclaw secrets reload     # Hot-reload without gateway restart
```

### 添加更多品牌

使用 `brand-manager` 子技能：
- “添加新品牌” — 自动创建品牌（对于使用 Topic 模式的场景）
- “列出品牌” — 显示所有活跃品牌
- “归档 {brand}” — 停用某个品牌

### 自定义代理行为

每个代理的行为由两个文件定义：
- **SOUL.md** — 代理的个性、工作原则和行为规范
- **AGENTS.md** — 操作流程、数据处理方式、品牌范围和使用的工具

根据具体需求修改这些文件以调整代理的行为。

### 记忆系统

三层记忆系统自动运行：
- **MEMORY.md** — 长期存储的精选信息（由 Cron 自动更新）
- **memory/YYYY-MM-DD.md** — 每日活动日志
- **shared/** — 永久性知识库（内容会随着时间积累）

**可选增强功能：** 安装 QMD 以实现知识库中的语义搜索。可以使用 `qmd-setup` 子技能进行安装，或手动安装（命令：`bun install -g @tobilu/qmd`）。

详细文档请参阅 `references/memory-system.md`。

### 通信信号

代理使用标准化的信号来传递状态信息。完整信号字典请参阅 `references/signals-protocol.md`。

## 参考文档

| 文档 | 用途 | 阅读时机 |
|----------|---------|-------------|
| `references/architecture.md` | 星形拓扑结构、会话模型、并行处理 | 了解系统设计 |
| `references/agent-roles.md` | 代理的详细功能和限制 | 定制团队组成 |
| `references/signals-protocol.md` | 完整的信号字典 | 调试代理通信 |
| `references/memory-system.md` | 三层记忆系统 + 知识存储机制 | 了解记忆系统的运作方式 |
| `references/approval-workflow.md` | 审批流程 + 所有者的操作快捷方式 | 内容发布流程 |
| `references/troubleshooting.md | 常见问题（如 IPv6 等）及解决方法 | 在遇到问题时参考 |

## 目录结构

安装完成后，会创建以下目录结构：

```
~/.openclaw/
├── openclaw.json                    # Updated with agent configs
├── workspace/                       # Leader
│   ├── SOUL.md, AGENTS.md, HEARTBEAT.md, IDENTITY.md
│   ├── memory/, skills/, assets/
│   └── shared/                      # Real directory (shared KB lives here)
│       ├── INSTANCE.md              # Instance configuration
│       ├── brand-registry.md        # Brand registry
│       ├── system-guide.md, brand-guide.md, compliance-guide.md
│       ├── team-roster.md
│       ├── brands/{id}/profile.md   # Per-brand profiles
│       ├── domain/{id}-industry.md  # Industry knowledge
│       ├── operations/              # Ops guides
│       └── errors/solutions.md      # Error KB
├── workspace-researcher/            # Researcher
│   ├── SOUL.md, AGENTS.md, MEMORY.md
│   ├── memory/, skills/
│   └── shared -> ../workspace/shared/
├── workspace-content/               # Content Strategist
│   └── (same structure)
├── workspace-designer/              # Visual Designer
│   └── (same structure)
├── workspace-operator/              # Operator
│   └── (same structure)
├── workspace-engineer/              # Engineer
│   └── (same structure)
├── workspace-reviewer/              # Reviewer (minimal, read-only)
│   ├── SOUL.md, AGENTS.md
│   └── shared -> ../workspace/shared/
└── cron/jobs.json                   # Scheduled tasks
```

## 脚本

| 脚本 | 用途 | 运行时机 |
|--------|---------|-------------|
| `scripts/scaffold.sh` | 创建目录、复制模板、设置符号链接 | 初始设置时 |
| `scripts/patch-config.js` | 将代理配置合并到 openclaw.json | 初始设置时 |
| `scripts/telegram-topics.js` | 在 Telegram 私信或超群组中创建主题帖 | 设置过程中或添加品牌时 |

## 子技能

| 技能 | 用途 |
|-------|---------|
| `instance-setup` | 配置所有者信息、语言设置、机器人身份 |
| `brand-manager` | 添加、编辑、归档品牌 |
| `qmd-setup` | 安装并配置 QMD 语义搜索系统（可选） |