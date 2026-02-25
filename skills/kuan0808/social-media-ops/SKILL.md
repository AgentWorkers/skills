---
name: social-media-ops
description: 在 OpenClaw 上搭建一个完整的多品牌社交媒体管理团队。通过星形拓扑结构配置 7 个专业 AI 代理（组长、研究员、内容策略师、视觉设计师、操作员、工程师、审核员），实现持久的双向沟通（A2A）、三层记忆系统、共享知识库、审批工作流程以及品牌隔离功能。该方案适用于新社交媒体运营团队的组建、将多代理框架添加到现有 OpenClaw 实例中，或当用户需要处理社交媒体管理、多品牌运营或内容团队设置相关任务时。
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

本技能用于在 OpenClaw 上搭建一个完整的、由人工智能驱动的社交媒体运营团队。它包括以下内容：

- **7 个专业代理**，采用星型拓扑结构（1 个负责人 + 6 个专家）
- **持久的点对点（A2A）会话**，以保持多代理工作流程的上下文一致性
- **三层记忆系统**（包括 `MEMORY.md`、每日笔记和共享知识库）
- **共享知识库**，其中包含品牌资料、运营指南和领域知识
- **审批流程**，确保所有内容在发布前都需获得负责人批准
- **品牌隔离**，每个品牌都有独立的频道、内容指南和资产目录
- **定时任务自动化**，用于每日知识整合和每周知识库审查

## 先决条件

在安装之前，请确保：
1. OpenClaw 已经安装，并且完成了 `openclaw onboard` 过程
2. 至少存在一个认证配置文件（例如 Anthropic API 密钥）
3. `~/.openclaw/` 目录已经存在

## 快速入门

```
1. Install the skill (if not already in workspace/skills/)
2. Trigger setup: "Set up my social media operations team"
3. Follow the interactive onboarding (6 steps, ~10 minutes)
4. Start creating content!
```

## 入职流程

首次触发此技能时，会运行一个交互式设置流程。

### 第 1 步：检查先决条件

验证环境是否准备就绪：
- [ ] OpenClaw 已安装，并且完成了 `openclaw onboard`
- [ ] `~/.openclaw/` 目录存在
- [ ] 至少配置了一个认证配置文件

如果缺少任何先决条件，请指导用户解决这些问题后再继续。

### 第 2 步：团队设置

**所有 7 个代理会自动安装。** 不需要用户选择团队规模。

完整的团队成员包括：
| 代理 | 角色 |
|-------|------|
| 负责人 | 整合协调、路由管理、质量把控 |
| 研究员 | 市场调研、竞争对手分析 |
| 内容创作者 | 内容策略、文案撰写 |
| 设计师 | 视觉设计、图片生成 |
| 操作员 | 平台运营、任务调度 |
| 工程师 | 技术集成、自动化处理 |
| 审核员 | 独立的质量审核 |

**模型分配** — 使用用户认证配置文件中已配置的模型（`agents.defaults.model.primary`）。所有代理默认使用相同的模型，以简化设置过程。

自动配置完成后，可以询问用户：
> “所有 7 个代理都将使用您配置的模型。是否希望为审核员代理选择不同的模型以获得独立的视角？（您随时可以更改。）”

如果用户同意，收集所需的模型信息；否则直接进入下一步。

> **高级提示：** 如果日后希望组建更精简的团队，可以重新运行 `scaffold.sh --agents leader,content,designer,engineer` 命令来创建一个精简版的团队。

### 第 3 步：Telegram 设置

此步骤采用**引导式流程**，无需用户提供聊天 ID 或主题 ID。

#### 第 A 阶段：确认机器人令牌

1. 检查 `openclaw.json` 文件中的 `channelsTelegram.botToken` 是否存在
2. 如果存在 → 转到第 B 阶段
3. 如果不存在 → 指导用户：
   - 打开 Telegram，搜索 **@BotFather**
   - 发送 `/newbot` 并按照提示创建机器人
   - 复制机器人令牌并粘贴到这里
   - 将令牌写入 `openclaw.json` 文件的 `channelsTelegram.botToken` 字段

#### 第 B 阶段：选择频道模式

按以下顺序展示选项（先选择 DM+Topics）：
1. **DM+Topics（推荐）** — 最简单的设置方式，无需创建群组
   - 每个品牌在机器人的私信中都有自己的主题线程
   - 适合单独管理多个品牌的操作员
   - 需要为机器人启用 Thread Mode（后续会有详细指导）

2. **Group+Topics** — 适用于多人团队
   - 品牌信息存储在 Telegram 超群组的主题线程中
   - 多个团队成员可以参与讨论
   - 需要一个已启用 Topic 功能的超群组

3. **DM-simple** — 最简单的模式，没有品牌隔离
   - 与机器人进行单次私信交流
   - 基于上下文的品牌路由（不支持主题）

4. **Group-simple** — 无品牌隔离的群组交流
   - 全群组对话
   - 基于上下文的品牌路由（不支持主题）

#### 第 C 阶段：特定模式的设置

**如果选择 DM+Topics：**

1. 指导用户为他们的机器人启用 Thread Mode：
   - 打开 Telegram，找到 **@BotFather**
   - 点击左下角的 **Open** 按钮打开 BotFather MiniApp
   - 在 MiniApp 中选择您的机器人
   - 进入 **Bot Settings**
   - 启用 **Thread Mode**
   - 完成后告知我

2. 确认启用后，使用机器人令牌获取用户的聊天 ID：
   - 向机器人发送任意消息
   - 代理会从消息中的 `{{From}}` 字段提取用户的聊天 ID
   - 代理将聊天 ID 保存到频道配置中

3. 自动创建 **Operations** 主题：
   ```bash
   node scripts/telegram-topics.js \
     --config ~/.openclaw/openclaw.json \
     --chat <USER_CHAT_ID> \
     --name "Operations"
   ```

4. 将生成的线程 ID 保存到 `shared/operations/channel-map.md` 文件中

**如果选择 Group+Topics：**

1. 检查用户是否已经拥有超群组：
   - 如果没有：指导用户创建一个超群组（选择 “Create Group” 并启用 “Topics” 功能）
2. 指导用户将机器人添加到超群组：
   - 将机器人设置为 **管理员** 并赋予 “Manage Topics” 权限
   - 在群组中发送一条消息

3. 代理会从消息中的 `{{To}}` 字段提取群组聊天 ID
   - 将聊天 ID 保存到频道配置中

4. 自动创建 **Operations** 主题：
   ```bash
   node scripts/telegram-topics.js \
     --config ~/.openclaw/openclaw.json \
     --chat <GROUP_CHAT_ID> \
     --name "Operations"
   ```

5. 将生成的线程 ID 保存到 `shared/operations/channel-map.md` 文件中

**如果选择 DM-simple：**

1. 向机器人发送任意消息
2. 代理从消息中提取聊天 ID
   - 将聊天 ID 保存到频道配置中

**如果选择 Group-simple：**

1. 指导用户将机器人添加到群组并发送一条消息
2. 代理从消息中提取群组聊天 ID
   - 将聊天 ID 保存到频道配置中

### 第 4 步：执行设置脚本

运行 `scripts/scaffold.sh` 脚本：
```bash
# 1. Create directories, copy templates, set up symlinks
bash scripts/scaffold.sh \
  --skill-dir "$(pwd)"

# 2. Merge agent configuration into openclaw.json
node scripts/patch-config.js \
  --config ~/.openclaw/openclaw.json
```

脚本会完成以下操作：
- 为每个代理创建工作空间目录（包含 `SOUL.md` 和 `SECURITY.md` 文件）
- 创建包含所有模板文件的共享知识库
- 在负责人技能目录下创建指向共享目录的符号链接
- 设置子技能（`instance-setup` 和 `brand-manager`）
- 配置定时任务

配置文件会更新 `openclaw.json`：
- 包含代理定义、模型分配和工具限制
- A2A 会话配置
- QMD（知识管理）路径
- 内部钩子

### 第 5 步：实例设置 + 首个品牌

设置完成后，运行子技能：
1. **实例设置**（`instance-setup` 技能）
   - 设置负责人信息、时区
   - 通信语言（面向负责人的语言）
   - 默认内容语言
   - 机器人身份（名称、表情符号、个性设置）
   - 更新相关文件：`shared/INSTANCE.md` 和 `workspace/IDENTITY.md`

2. **首个品牌**（`brand-manager add`）
   - 设置品牌 ID、显示名称、域名
   - 目标市场和内容语言
   - **创建主题**（对于支持 Topic 模式的模式）：
     - 代理调用 `scripts/telegram-topics.js` 命令，根据品牌名称创建主题
     - 脚本返回主题 ID
     - 代理将主题 ID 保存到 `shared/operations/channel-map.md` 和品牌配置文件中
   - 对于简单模式：无需创建主题，跳过此步骤
   - 创建品牌资料、内容指南、领域知识文件和资产目录

### 第 6 步：验证 + 重启网关

1. **重启网关**：
   ```
   openclaw gateway restart
   ```

2. **验证安装结果：**
   - 所有代理的工作空间都包含了 `SOUL.md` 和 `SECURITY.md` 文件
   - `shared/` 目录中包含所有模板文件
   - 所有工作空间的符号链接都有效
   `openclaw.json` 文件中包含了所有代理的配置信息
   A2A 会话配置已启用（`tools.agentToAgent.enabled: true`）
   定时任务已配置
   网关成功重启
   负责人能够接收并回复消息
   至少有一个代理能够接收到 `sessions_send` 消息

**设置完成后建议执行的任务：**
1. 填写品牌资料：`shared/brands/{brand_id}/profile.md`
2. 测试内容创建功能：例如 “为 {brand} 创建一条 Facebook 帖子”
3. 添加更多品牌：使用 “Add a new brand” 命令
4. 设置发布计划：编辑 `shared/operations/posting-schedule.md` 文件

## 安装后的操作

### 添加更多品牌

使用 `brand-manager` 子技能：
- “Add a new brand” — 自动创建新品牌（支持 Topic 模式）
- “List brands” — 查看所有活跃品牌
- “Archive {brand}” — 关闭某个品牌

### 自定义代理行为

每个代理的行为都由其对应的 `SOUL.md` 文件定义：
- `workspace/SOUL.md`：负责人的行为规则和路由策略
- `workspace-{agent}/SOUL.md`：专家的具体行为和限制

根据实际需求修改这些文件以调整代理的行为。

### 记忆系统

三层记忆系统会自动运行：
- **MEMORY.md**：长期保存的数据（通过定时任务自动更新）
- `memory/YYYY-MM-DD.md`：每日活动日志
- `shared/**`：永久性的知识库（内容会随着时间不断积累）

详细信息请参阅 `references/memory-system.md` 文件。

### 通信信号

代理使用标准化的信号来传递状态信息。详细信号字典请参阅 `references/signals-protocol.md` 文件。

## 参考文档

| 文档 | 用途 | 阅读时机 |
|----------|---------|-------------|
| `references/architecture.md` | 星型拓扑结构、会话模型、并行处理 | 了解系统设计 |
| `references/agent-roles.md` | 代理的详细功能和限制 | 自定义团队组成 |
| `references/signals-protocol.md` | 完整的信号字典 | 调试代理间的通信 |
| `references/memory-system.md` | 三层记忆系统 + 知识存储机制 | 了解记忆系统的运作方式 |
| `references/approval-workflow.md` | 审批流程 + 负责人操作指南 | 内容发布流程 |
| `references/troubleshooting.md` | 常见问题（如 IPv6 相关问题）及解决方法 | 解决故障时参考 |

## 目录结构

安装完成后，系统会创建以下目录结构：
```
~/.openclaw/
├── openclaw.json                    # Updated with agent configs
├── workspace/                       # Leader
│   ├── SOUL.md, AGENTS.md, HEARTBEAT.md, IDENTITY.md, SECURITY.md
│   ├── memory/, skills/, assets/
│   └── shared -> ../shared/
├── workspace-researcher/            # Researcher
│   ├── SOUL.md, SECURITY.md, MEMORY.md
│   ├── memory/, skills/
│   └── shared -> ../shared/
├── workspace-content/               # Content Strategist
│   └── (same structure)
├── workspace-designer/              # Visual Designer
│   └── (same structure)
├── workspace-operator/              # Operator
│   └── (same structure)
├── workspace-engineer/              # Engineer
│   └── (same structure)
├── workspace-reviewer/              # Reviewer (minimal, read-only)
│   ├── SOUL.md, SECURITY.md
│   └── shared -> ../shared/
├── shared/                          # Shared knowledge base
│   ├── INSTANCE.md                  # Instance configuration
│   ├── brand-registry.md            # Brand registry
│   ├── system-guide.md, brand-guide.md, compliance-guide.md
│   ├── team-roster.md
│   ├── brands/{id}/profile.md       # Per-brand profiles
│   ├── domain/{id}-industry.md      # Industry knowledge
│   ├── operations/                  # Ops guides
│   └── errors/solutions.md          # Error KB
└── cron/jobs.json                   # Scheduled tasks
```

## 脚本

| 脚本 | 用途 | 执行时机 |
|--------|---------|-------------|
| `scripts/scaffold.sh` | 创建目录、复制模板、设置符号链接 | 初始设置阶段 |
| `scripts/patch-config.js` | 将代理配置合并到 openclaw.json | 初始设置阶段 |
| `scripts/telegram-topics.js` | 在 Telegram 私信或超群组中创建主题 | 设置阶段及添加新品牌时 |

## 子技能

| 技能 | 用途 |
|-------|---------|
| `instance-setup` | 配置负责人信息、语言设置、机器人身份 | |
| `brand-manager` | 添加、编辑或关闭品牌 |