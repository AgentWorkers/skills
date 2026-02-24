---
name: social-media-ops
description: 在 OpenClaw 上搭建一个完整的多品牌社交媒体管理团队。通过星型拓扑结构部署 7 个专门的人工智能代理（组长、研究员、内容策略师、视觉设计师、操作员、工程师、审核员），实现持续的点对点交流（A2A）、三层记忆系统、共享知识库、审批工作流程以及品牌隔离功能。该方案适用于新社交媒体运营团队的组建、将多代理框架添加到现有的 OpenClaw 实例中，或当用户需要处理社交媒体管理、多品牌运营或内容团队设置相关任务时。
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
# 社交媒体运营（Social Media Operations）

## 概述

此技能配置了一个基于 OpenClaw 的完整 AI 驱动的社交媒体运营团队。它包括：

- **7 个专业代理**，采用星型拓扑结构（1 个负责人 + 6 个专家）
- **持久的 A2A（代理间）会话**，以保持多代理工作流的上下文一致性
- **三层记忆系统**（包括 `MEMORY.md`、每日笔记和共享知识库）
- **共享知识库**，其中包含品牌资料、运营指南和领域知识
- **审批流程**，确保所有内容在获得负责人批准前不会发布
- **品牌隔离**，每个品牌都有独立的频道、内容指南和资产目录
- **Cron 自动化**，用于每日知识更新和每周知识库审查

## 先决条件

在安装之前，请确保：

1. OpenClaw 已安装，并且已完成 `openclaw onboard` 过程
2. 至少存在一个认证配置文件（例如 Anthropic API 密钥）
3. 已配置 Telegram 机器人（或在设置过程中进行配置）
4. `~/.openclaw/` 目录存在

## 快速入门

```
1. Install the skill (if not already in workspace/skills/)
2. Trigger setup: "Set up my social media operations team"
3. Follow the interactive onboarding (5 steps, ~10 minutes)
4. Add your first brand: "Add a new brand"
5. Start creating content!
```

## 新员工入职流程

首次触发此技能时，会运行一个交互式设置流程。

### 第 1 步：检查先决条件

验证环境是否准备就绪：

- [ ] OpenClaw 已安装，并且 `openclaw onboard` 已完成
- [ ] `~/.openclaw/` 目录存在
- [ ] 至少配置了一个认证配置文件
- [ ] Telegram 机器人令牌可用（或在设置过程中配置）

如果缺少任何先决条件，请指导用户解决这些问题后再继续。

### 第 2 步：团队配置

**选择团队配置** — 询问用户希望使用哪种团队配置：

| 配置 | 代理数量 | 适用场景 |
|---------------|--------|----------|
| **完整团队**（推荐） | 7 个代理 | 多品牌运营，内容量较大 |
| **精简团队** | 1 个负责人 + 1 个内容生成员 + 1 个设计师 + 1 个工程师 | 单一品牌，内容量较少 |
| **自定义** | 用户自行选择 | 根据具体需求定制 |

**模型分配** — 为每个代理推荐合适的模型：

| 代理类型 | 推荐模型 | 选择理由 |
|-------|-------------------|-----------|
| 负责人 | Opus（或最佳可用模型） | 需要高级推理能力的复杂协调任务 |
| 研究员 | Opus（或最佳可用模型） | 需要强大模型的深度分析任务 |
| 内容生成员 | Sonnet（或中等性能模型） | 快速且功能强大的文本生成能力 |
| 设计师 | Sonnet（或中等性能模型） | 快速生成视觉简报和图片的能力 |
| 操作员 | Sonnet（或中等性能模型） | 需要快速执行浏览器自动化任务的代理 |
| 工程师 | Sonnet（或中等性能模型） | 中等性能模型适合代码生成任务 |
| 审核员 | 其他模型（如 GLM-5、Gemini） | 提供独立的视角 |

用户可以选择默认配置或根据需要自定义。

### 第 3 步：平台设置

收集平台配置信息：

1. **Telegram 机器人令牌** — 如果 `openclaw.json` 中尚未配置
2. **频道模式** — 对于多品牌运营，建议使用 **Group+Topics** 模式：
   - **Group+Topics**（推荐）：包含每个品牌的论坛主题的超级群组
   - **DM+Topics**：具有论坛模式的私信
   - **Group-simple**：没有特定主题的群组（基于上下文的消息路由）
   - **DM-simple**：纯私信（基于上下文的消息路由）
3. **群组/聊天 ID** — 对于 Group 模式，需要提供 Telegram 超级群的 ID
4. **运营主题** — 用于系统通知的线程 ID

### 第 4 步：运行设置脚本

执行设置脚本：

```bash
# 1. Create directories, copy templates, set up symlinks
bash scripts/scaffold.sh \
  --skill-dir "$(pwd)" \
  --agents "leader,researcher,content,designer,operator,engineer,reviewer"

# 2. Merge agent configuration into openclaw.json
node scripts/patch-config.js \
  --config ~/.openclaw/openclaw.json \
  --agents "leader,researcher,content,designer,operator,engineer,reviewer"
```

脚本会创建：
- 各代理的工作空间目录（包含 `SOUL.md` 和 `SECURITY.md` 文件）
- 共享知识库（包含所有模板文件）
- 从各工作空间到共享目录的符号链接
- 负责人技能目录下的子技能（如 `instance-setup`、`brand-manager`）
- Cron 作业定义

配置文件（`openclaw.json`）会更新以下内容：
- 代理定义（包括模型分配和工具限制）
- A2A 会话配置
- QMD（知识库）的存储路径
- 内部钩子（用于系统内部通信）

### 第 5 步：实例设置 + 第一个品牌

设置完成后，运行相关子技能：

1. **实例设置**（`instance-setup` 技能）：
   - 设置负责人信息和工作时区
   - 设置与负责人沟通的语言
   - 设置默认内容语言
   - 设置机器人的身份（名称、表情符号和个性特征
   - 更新 `shared/INSTANCE.md` 和 `workspace/IDENTITY.md` 文件

2. **添加第一个品牌**（`brand-manager add` 技能）：
   - 设置品牌 ID、显示名称和域名
   - 设置目标市场和内容语言
   - 设置频道/主题的线程 ID
   - 创建品牌资料、内容指南和领域知识文件

3. **重启 Gateway**

```
   openclaw gateway restart
   ```

### 第 6 步：验证安装结果

设置完成后，验证以下内容：
- 所有代理的工作空间是否都包含了 `SOUL.md` 和 `SECURITY.md` 文件
- `shared/` 目录是否已填充模板文件
- 各工作空间到共享目录的符号链接是否有效
- `openclaw.json` 中是否包含所有代理的配置信息
- A2A 会话配置是否已设置（`tools.agentToAgent.enabled` 为 `true`）
- Cron 作业是否已配置
- Gateway 是否成功重启
- 负责人是否能够接收并回复消息
- 是否能够成功向至少一个代理发送消息

**建议的安装后首次任务：**
1. 填写品牌资料：`shared/brands/{brand_id}/profile.md`
2. 测试内容生成：例如：“为 {brand} 写一篇 Facebook 帖子”
3. 添加更多品牌：例如：“添加一个新的品牌”
4. 设置发布计划：例如：填写 `shared/operations/posting-schedule.md`

## 安装后的操作

### 添加更多品牌

使用 `brand-manager` 子技能：
- “添加新品牌” — 交互式创建新品牌
- “列出所有品牌” — 查看所有活跃品牌
- “归档品牌” — 取消某个品牌的活跃状态

### 自定义代理行为

每个代理的行为在其 `SOUL.md` 文件中定义：
- `workspace/SOUL.md`：负责人的行为规则和路由策略
- `workspace/{agent}/SOUL.md`：专家的具体行为和限制

根据实际需求修改这些文件以调整代理的行为。

### 记忆系统

三层记忆系统自动运行：
- **MEMORY.md**：长期存储的数据（通过 Cron 定时更新）
- **memory/YYYY-MM-DD.md**：每日活动日志
- **shared/**：永久性的知识库（内容会随时间累积）

详细文档请参阅 `references/memory-system.md`。

### 通信信号

代理使用标准化的信号进行状态沟通。完整信号字典请参阅 `references/signals-protocol.md`。

## 参考文档

| 文档 | 用途 | 阅读时机 |
|----------|---------|-------------|
| `references/architecture.md` | 星型拓扑结构、会话模型、并行处理机制 | 了解系统设计 |
| `references/agent-roles.md` | 代理的详细功能和限制 | 定制团队组成 |
| `references/signals-protocol.md` | 完整的信号字典 | 调试代理间的通信 |
| `references/memory-system.md` | 三层记忆系统及知识存储机制 | 了解记忆系统的运作方式 |
| `references/approval-workflow.md` | 审批流程和负责人操作流程 | 理解内容发布流程 |
| `references/troubleshooting.md | 常见问题及解决方法 | 解决系统故障时参考 |

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

| 脚本 | 用途 | 运行时机 |
|--------|---------|-------------|
| `scripts/scaffold.sh` | 创建目录、复制模板、设置符号链接 | 在初始设置阶段 |
| `scripts/patch-config.js` | 将代理配置合并到 `openclaw.json` | 在初始设置阶段 |

## 子技能

| 技能名称 | 用途 |
|-------|---------|
| `instance-setup` | 配置负责人信息、语言和机器人身份 |
| `brand-manager` | 添加、编辑或归档品牌信息 |