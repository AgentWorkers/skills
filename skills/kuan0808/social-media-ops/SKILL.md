---
name: social-media-ops
description: 在 OpenClaw 上搭建一个完整的多品牌社交媒体管理团队。该团队包括 5 种类型的专门代理（负责人、内容创作者、执行者、研究员和工程师），以及按需使用的审核员。团队采用星形拓扑结构，支持持久的点对点（A2A）通信、三层记忆系统、共享知识库、审批工作流程，并具备品牌隔离功能。此方案适用于新社交媒体运营团队的组建、将多代理框架添加到现有 OpenClaw 实例中，或当用户需要处理社交媒体管理、多品牌运营或内容团队设置相关任务时。
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

- **5 个专业代理**，采用星型拓扑结构（1 个负责人 + 4 个专家）+ 需要时启动的审核员
- **持久的 A2A（代理对代理）会话**，以保持多代理工作流程的上下文一致性
- **三层记忆系统**（MEMORY.md + 每日笔记 + 共享知识库）
- **共享知识库**，其中包含品牌资料、运营指南和领域知识
- **审批工作流程**，确保所有内容在获得负责人批准前不会发布
- **品牌隔离**，每个品牌都有独立的频道、内容指南和资产目录
- **Cron 自动化**，用于每日记忆整合和每周知识库审查

## 可选依赖项

- **用于 Creator 代理的图像生成工具**：Creator 代理需要在其 `workspace-creator/skills/` 目录中安装图像生成工具才能生成图片。推荐使用 `nano-banana-pro`（基于 Gemini，免费 tier）。如果没有此工具，Creator 仅能生成文本形式的视觉简报，无法生成图片。

## 先决条件

在安装之前，请确保：

1. 已安装 OpenClaw v2026.2.26+ 并完成 `openclaw onboard` 流程
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

- [ ] OpenClaw 已安装且 `openclaw onboard` 已完成
- [ ] `~/.openclaw/` 目录存在
- [ ] 至少配置了一个认证配置文件

如果缺少任何先决条件，请指导用户解决后再继续。

### 第 2 步：团队设置

**所有 5 个代理将自动安装。** 不需要用户选择团队规模。

完整团队成员如下：

| 代理 | 角色 |
|-------|------|
| 负责人 | 组织协调、路由管理、质量把控 |
| Creator | 内容制作 + 视觉设计（文案撰写、图片生成、平台格式化） |
| Worker | 执行负责人分配的任务（文件处理、命令行操作、配置管理、维护工作） |
| Researcher | 市场调研、竞争对手分析 |
| Engineer | 技术集成、自动化实现 |

**按需添加：**

| 代理 | 角色 |
|-------|------|
| Reviewer | 独立的质量审核员（根据需要启动） |

**模型** — 所有代理都继承在 `openclaw onboard` 期间配置的模型（位于 `agentsdefaults.model`）。无需为每个代理单独配置模型。

> **高级提示：** 如果后来希望使用更精简的团队，可以重新运行 `scaffold.sh --agents leader,creator,engineer` 来创建一个精简的团队配置。

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
- 各代理的工作空间目录（包含 SOUL.md、AGENTS.md、MEMORY.md）
- 共享知识库及所有模板文件
- 从每个工作空间到共享目录的符号链接
- 负责人技能目录下的子技能（如 instance-setup、brand-manager）
- Cron 作业定义

配置文件 `patch-config.js` 会合并到 `openclaw.json` 中：
- 代理定义（包括模型分配和工具限制）
- A2A 会话配置
- QMD 记忆路径（**仅在安装了 QMD 时使用** — 否则跳过此步骤）
- 内部钩子

### 第 4 步：Telegram 设置

此步骤采用**引导式流程** — 不需要用户提供原始聊天 ID 或线程 ID。

#### 第 A 阶段：确认机器人令牌

1. 检查 `openclaw.json` 中的 `channelsTelegram.botToken` 是否存在
2. 如果存在 → 转到第 B 阶段
3. 如果不存在 → 指导用户：
   - 打开 Telegram，搜索 **@BotFather**
   - 发送 `/newbot` 并按照提示创建机器人
   - 复制机器人令牌并粘贴到这里
   - 将令牌写入 `openclaw.json` 的 `channelsTelegram.botToken` 字段

#### 第 B 阶段：选择频道模式

按以下顺序展示选项（建议先选择 Group+Topics）：

1. **Group+Topics** — 适用于大多数设置
   - 品牌信息存储在 Telegram 超群组的主题帖中
   - 适用于单人操作或多人团队
   - 需要一个启用了主题功能的超群组

2. **DM+Topics** — 私人替代方案，无需群组
   - 每个品牌在机器人的私信中拥有自己的主题帖
   - 需要在机器人上启用线程模式（以下有详细指导）

3. **DM-simple** — 最简单的模式，没有品牌隔离
   - 与机器人进行单次私信对话
   - 基于对话内容的品牌路由（不支持主题帖）

4. **Group-simple** — 无品牌隔离的群组对话
   - 在群组中进行对话
   - 基于对话内容的品牌路由（不支持主题帖）

#### 第 C 阶段：特定模式的配置

**如果选择 DM+Topics：**

1. 指导用户在机器人上启用线程模式：
   - 打开 Telegram，找到 **@BotFather**
   - 点击左下角的 **Open** 按钮打开 BotFather MiniApp
   - 在 MiniApp 中选择你的机器人
   - 进入 **Bot Settings**
   - 找到 **Thread Mode** 并启用它
   - 完成后告诉我

2. 确认后，使用机器人令牌获取用户的聊天 ID：
   - 向机器人发送任意消息
   - 代理会从消息中的 `{{From}}` 字段提取用户的聊天 ID
   - 代理将聊天 ID 写入频道配置文件

3. 自动创建 **Operations** 主题帖：
   ```bash
   node scripts/telegram-topics.js \
     --config ~/.openclaw/openclaw.json \
     --chat <USER_CHAT_ID> \
     --name "Operations"
   ```

4. 将生成的线程 ID 写入 `shared/operations/channel-map.md`
5. 更新 `cron/jobs.json` — 将 `{{OPERATIONS_CHANNEL}}` 替换为实际的 Operations 频道地址（格式：`chatId:threadId`，例如 `123456789:7`）

**如果选择 Group+Topics：**

1. 检查用户是否已经拥有超群组：
   - 如果没有：指导用户创建一个超群组（创建群组 → 打开 “Topics” 功能）
2. 指导用户将机器人添加到群组：
   - 将机器人设置为 **管理员** 并赋予 “Manage Topics” 权限
   - 在群组中发送一条消息

3. 代理从消息中提取群组聊天 ID：
   - 从 `{{To}}` 字段提取群组聊天 ID
   - 代理将聊天 ID 写入频道配置文件
4. 自动创建 **Operations** 主题帖：
   ```bash
   node scripts/telegram-topics.js \
     --config ~/.openclaw/openclaw.json \
     --chat <GROUP_CHAT_ID> \
     --name "Operations"
   ```

5. 将生成的线程 ID 写入 `shared/operations/channel-map.md`
6. 更新 `cron/jobs.json` — 将 `{{OPERATIONS_CHANNEL}}` 替换为实际的 Operations 频道地址（格式：`chatId:threadId`，例如 `-100XXXXXXXXXX:7`）

**如果选择 DM-simple：**

1. 向机器人发送任意消息
2. 代理从消息中提取聊天 ID
3. 将聊天 ID 写入频道配置文件

**如果选择 Group-simple：**

1. 指导用户将机器人添加到群组并发送一条消息
2. 代理从消息中提取群组聊天 ID
3. 将聊天 ID 写入频道配置文件

### 第 5 步：实例设置 + 首个品牌配置

完成搭建和 Telegram 配置后，运行子技能：

1. **实例设置**（`instance-setup` 技能）
   - 负责人姓名和时区
   - 与负责人沟通的语言
   - 默认内容语言
   - 机器人身份（名称、表情符号、个性设定
   - 更新内容：`shared/INSTANCE.md`、`workspace/IDENTITY.md`

2. **首个品牌**（`brand-manager add`）
   - 品牌 ID、显示名称、域名
   - 目标市场和内容语言
   - **主题创建**（对于 Group+Topics 模式）：
     - 代理调用 `scripts/telegram-topics.js` 根据品牌名称创建主题帖
     - 脚本返回线程 ID
     - 代理将线程 ID 写入 `shared/operations/channel-map.md` 和品牌配置文件
   - 对于简单模式：无需创建主题帖，可跳过此步骤
   - 创建品牌资料、内容指南、领域知识文件、资产目录

### 第 6 步：验证 + 重启网关

1. **重启网关：**
   ```
   openclaw gateway restart
   ```

2. **运行诊断测试：**
   ```
   openclaw doctor
   ```
   此步骤会验证代理配置、私信允许列表的继承性、会话状态、模型可用性以及工作空间的完整性。

3. **其他检查：**
   - [ ] 负责人能够回复消息
   - [ ] 至少有一个代理能够成功接收 `sessions_send` 请求

**可选：启用 QMD 语义记忆**

如果在第 3 步中 `patch-config.js` 报告 “qmd binary not found”，代理将使用基于文件的记忆系统（这也是可行的）。要启用增强型语义搜索功能：
- 输入 “Set up QMD” 来运行 `qmd-setup` 子技能，该技能会指导你完成安装和配置。

**建议的安装后首次任务：**
1. 填写品牌资料：`shared/brands/{brand_id}/profile.md`
2. 测试内容创建：`为 {brand} 编写一条 Facebook 帖子`
3. 添加更多品牌：`添加一个新的品牌`
4. 设置发布计划：填写 `shared/operations/posting-schedule.md`

## 安装后

### 异步调度模型（v2.0.0+）

负责人使用**完全异步的调度机制**（`sessions_send` 的 `timeoutSeconds: 0`）来处理所有代理之间的通信。这意味着：

- 负责人**永远不会因为等待代理而阻塞** — 始终可以对负责人保持响应。
- 代理在完成任务后通过 `sessions_send` 回调给负责人（基于事件驱动，而非轮询）。负责人根据 `agents.md` 中的 “Agent Callback Protocol” 流程处理回调。
- 每个任务都会记录在单独的文件 `tasks/T-{YYYYMMDD}-{HHMM}.md` 中。已完成的任务会被归档到 `tasks/archive/`。
- **过期任务检测** 由 Cron 作业（`stale-task-check`，每 10 分钟执行一次）处理，它会检查 `tasks/` 目录中处于 `[⏳]` 状态的未完成任务。
- 默认情况下 `HEARTBEAT.md` 文件为空 — 定期检查由 Cron 作业完成，而不是通过心跳轮询。

### 密钥管理（可选）

为了集中管理 API 密钥，可以使用以下方法：
```
openclaw secrets audit      # Check for plaintext secrets in config
openclaw secrets configure  # Set up secret entries
openclaw secrets apply      # Activate secrets
openclaw secrets reload     # Hot-reload without gateway restart
```

### 添加更多品牌

使用 `brand-manager` 子技能：
- “添加新品牌” — 交互式创建品牌（对于 Group+Topics 模式会自动创建主题帖）
- “列出所有品牌” — 显示所有活跃品牌
- “归档 {brand}” — 停用某个品牌

### 自定义代理行为

每个代理的行为通过两个文件定义：
- **SOUL.md** — 代理的个性、工作原则、行为界限、安全规则
- **AGENTS.md** — 操作流程、数据处理方式、品牌范围、使用工具

根据具体需求修改这些文件以调整代理行为。

### 记忆系统

三层记忆系统会自动运行：
- **MEMORY.md** — 长期保存的数据（由 Cron 自动更新）
- **memory/YYYY-MM-DD.md** — 每日活动日志
- **shared/**** — 持久性知识库（内容会随时间积累）

**可选升级：** 安装 QMD 以实现知识库中的语义搜索功能。可以使用 `qmd-setup` 子技能进行安装，或手动安装（`bun install -g @tobilu/qmd`）。

详细文档请参阅 `references/memory-system.md`。

### 通信信号

代理使用标准化的信号来传递状态信息。完整信号字典请参阅 `references/signals-protocol.md`。

## 参考文档

| 文档 | 用途 | 阅读时机 |
|----------|---------|-------------|
| `references/architecture.md` | 星型拓扑结构、会话模型、并行处理 | 了解系统设计 |
| `references/agent-roles.md` | 代理的详细功能和限制 | 定制团队组成 |
| `references/signals-protocol.md` | 完整的信号字典 | 调试代理通信 |
| `references/memory-system.md` | 三层记忆系统 + 知识存储机制 | 了解记忆系统的运作方式 |
| `references/approval-workflow.md` | 审批流程 + 负责人操作快捷方式 | 内容发布流程 |
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
├── workspace-creator/               # Creator
│   ├── SOUL.md, AGENTS.md, MEMORY.md
│   ├── memory/, skills/
│   └── shared -> ../workspace/shared/
├── workspace-worker/                # Worker
│   └── (same structure)
├── workspace-researcher/            # Researcher
│   └── (same structure)
├── workspace-engineer/              # Engineer
│   └── (same structure)
├── workspace-reviewer/              # Reviewer (minimal, read-only)
│   ├── SOUL.md, AGENTS.md
│   └── shared -> ../workspace/shared/
└── cron/jobs.json                   # Scheduled tasks
```

## 脚本

| 脚本 | 用途 | 执行时机 |
|--------|---------|-------------|
| `scripts/scaffold.sh` | 创建目录、复制模板、设置符号链接 | 在初始设置阶段 |
| `scripts/patch-config.js` | 将代理配置合并到 openclaw.json | 在初始设置阶段 |
| `scripts/telegram-topics.js` | 在设置阶段或添加品牌时，在 Telegram 私信或超群组中创建主题帖 |

## 子技能

| 技能 | 用途 |
|-------|---------|
| `instance-setup` | 配置负责人信息、语言设置、机器人身份 |
| `brand-manager` | 添加、编辑、归档品牌 |
| `qmd-setup` | 安装和配置 QMD 语义搜索功能（可选） |