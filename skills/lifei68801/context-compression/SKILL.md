---
name: context-compression
version: 3.9.7
description: "管理 OpenClaw 会话上下文，支持自动截断和内存保护功能，有效防止上下文溢出错误。主要特性包括：基于令牌的会话管理机制、人工智能事实提取功能以及偏好设置生命周期管理。适用场景：  
(1) 当会话窗口超出预设限制时；  
(2) 在设置内存层次结构时；  
(3) 在管理具有过期时间的用户偏好设置时。  
触发条件包括：压缩配置更改、内存管理操作以及会话上下文溢出情况。"
license: MIT-0
author: lifei68801
metadata:
  openclaw:
    requires:
      bins: ["bash", "jq", "sed", "grep", "head", "tail", "wc", "mkdir", "date", "tr", "cut"]
    permissions:
      - "file:read:~/.openclaw/agents/main/sessions/*.jsonl"
      - "file:write:~/.openclaw/agents/main/sessions/*.jsonl"
      - "file:read:~/.openclaw/workspace/memory/*.md"
      - "file:write:~/.openclaw/workspace/memory/*.md"
      - "file:write:~/.openclaw/workspace/MEMORY.md"
    behavior:
      modifiesLocalFiles: true
      description: "Local file operations for session trimming and memory storage. Uses built-in system tools (bash, jq, sed). No external network activity from scripts. Optional AI fact extraction uses local OpenClaw installation."
---
# 上下文压缩 - 完整解决方案 v3.9

这是一个全面的上下文管理系统，确保：
1. **永远不会超过模型上下文限制**
2. **通过分层内存记住所有之前的对话**
3. **利用人工智能进行智能的事实提取，并进行分类**

---

## 🆕 v3.9.5 的新功能

### 首选项生命周期管理
- **新脚本**：`check-preferences-expiry.sh` - 自动删除短期和中期首选项
- **分层结构**：首选项现在被分类为 长期（永久）、中期（1-4周）和短期（1-7天）
- **过期跟踪**：每日通过 cron 任务检查并删除过期的首选项
- **使用方法**：使用 `@YYYY-MM-DD` 标记首选项以跟踪其有效期，例如：`- 今天不想运动 @2026-03-12`

### 使用模式
```markdown
#### ⏰ 短期偏好 (1-7天)
- 今天不想运动 @2026-03-12
- 这周专注写论文 @2026-03-10

#### 🔄 中期偏好 (1-4周)
- 这个月要早起 @2026-03-01

#### 📍 长期偏好 (永久)
- 沟通风格：女友风格
```

cron 任务将根据首选项的有效期自动删除过期的条目。

---

## 🆕 v3.9.4 的新功能

### 文档清理
- 文档清晰度得到提升
- 技术参考资料已更新
- 功能没有变化

### v3.9.2 的新功能

### 重要修复：活动会话现在也能提取事实
- **问题**：活动会话（带有 `.lock` 文件）之前完全被忽略，无法提取事实
- **现在**：即使是活动会话，其高优先级内容也会被提取到 `MEMORY.md` 中
- **影响**：长时间会话期间不再出现内存丢失的问题

### v3.9.1 的新功能

### 不区分大小写的关键词匹配
- **问题**：优先级关键词现在不区分大小写（IMPORTANT, Important, important）
- **新增**：为所有英文关键词添加了常见的大小写变体
- **改进**：为全球用户提供了更好的双语支持

### v3.9.0 的新功能

### 重要修复：事实提取功能现已启用！
- **问题**：之前优先级策略完全跳过了事实提取
- **现在**：所有策略（优先级优先、时间衰减、仅基于令牌）都会在截断之前提取事实
- **可配置**：优先级关键词现在可以从配置文件中加载
- **双语支持**：默认关键词同时包含中文和英文，适用于全球用户

### 错误处理得到增强
- **重试机制**：提取操作在失败时最多重试 2 次
- **待办队列**：失败的提取操作会被保存以备后续重试
- **日志记录改进**：日志中的 v8 标签更加清晰，以便跟踪新行为

### v3.8.3 的新功能

### 维护更新
- 删除了过时的备份文件
- 通过 `truncate-sessions-safe.sh` 保持所有核心功能的完整性
- 文档得到更新

### v3.8.0 的新功能

### 基于人工智能的事实提取
- **新脚本**：`extract-facts-enhanced.sh` - 使用本地人工智能提取结构化事实
- **不再使用简单的关键词匹配** - 人工智能能够理解上下文并提取真正重要的信息
- **自动工作流程**：检测高价值内容 → 人工智能提取事实 → 写入 `MEMORY.md` → 然后截断
- **分类输出**：事实被标记为 [偏好], [决策], [任务], [时间], [关系], [重要]

### 工作原理
```
Session grows → Approaches token limit → Truncation script runs
    ↓
Detect high-value keywords (重要, 决定, TODO, etc.)
    ↓
AI extracts structured facts → Write to MEMORY.md
    ↓
Then perform truncation
```

### v3.6.3 的变更
- 安全扫描修复：不再扫描凭证信息
- 脚本仅检测用户的首选项、决策和任务

### 内存持久性保护（v3.6）
- **会话结束钩子 v2.0**：检测未保存的重要内容并生成警报
- **会话中检查**：定期扫描需要保存的关键词
- **警报文件系统**：当内存可能失效时生成 `.session-alert` 文件
- **新鲜度跟踪**：监控每日笔记更新频率

### 与 AGENTS.md 的集成
- 钩子现在输出结构化数据供人工智能读取
- 推荐系统：检测到重要内容时执行 `SAVE_NOW`
- 自动关键词检测：重要/决定/记住/待办/偏好

---

## 🆕 v3.5 的新功能

### 强化的事实提取
- **6 个类别的检测**：偏好、决策、任务、重要事项、时间、关系
- **结构化存储**：事实存储在 TSV 文件中，便于查询
- **自动同步**：事实会自动合并到 `MEMORY.md` 中

### 智能摘要
- **智能压缩**：提取标题、任务、重要项目
- **事实整合**：包含来自所有类别的事实
- **统计信息**：显示完成率和关键指标

### 会话钩子
- **会话开始钩子**：自动加载上下文并检查内存健康状况
- **会话结束钩子**：强制保存关键信息

---

## ⚠️ 工作原理

**仅进行本地文件操作：**
- 从 `~/.openclaw/agents/main/sessions/*.jsonl` 读取会话文件
- 截断大型会话以防止上下文溢出
- 将提取的事实写入 `MEMORY.md` 和每日笔记
- 使用标准系统工具（bash, jq, sed, grep）

**可选的人工智能功能：**
- 事实提取使用您的本地 OpenClaw 安装
- 脚本本身不使用外部服务或网络连接
- 所有数据都保留在您的机器上

**提取的内容包括：**
- 用户偏好（喜欢/偏好/讨厌）
- 重要决策（决定/确定）
- 任务状态（待办/已完成）
- 时间参考（明天/下周）
- 联系人参考（同事/朋友/客户）

---

## 🚀 快速入门：交互式设置

当此技能首次加载时，**会主动引导用户完成配置**：

### 第 0 步：检查现有配置

```bash
# Check if already configured
cat ~/.openclaw/workspace/.context-compression-config.json 2>/dev/null
```

如果已经配置好了，询问：“检测到现有配置。是否需要重新配置？”

### 第 1 步：逐一询问配置问题

**问题 1：上下文保留**
> “每个新会话应保留多少上下文？（1 个令牌约等于 3-4 个中文字符）”
> - 默认值（40000 个令牌）→ 推荐值，平衡历史记录保留与上下文安全性
- 保守值（60000 个令牌）→ 保留更多历史记录
- 较激进值（20000 个令牌）→ 最小化上下文
- 自定义 → 输入令牌数量（10000-100000）

**问题 2：截断频率**
> “应多久截断一次上下文以防止溢出？”
- 每 10 分钟一次（默认值）→ 推荐值
- 每 30 分钟一次 → 低频率
- 每小时一次 → 最低频率
- 自定义 → 输入分钟数

**问题 3：是否跳过活动会话**
> “在截断过程中是否应跳过活动会话以防止正在写入的会话损坏？”
- 是（默认值）→ 推荐值，防止数据损坏
- 否 → 可能会截断正在写入的会话

**问题 4：是否自动生成每日摘要**
> “是否应自动生成每日会话摘要？”
- 是 → 每 4 小时从每日笔记生成压缩摘要
- 否（默认值）→ 依赖实时内存写入

### 第 2 步：保存配置

创建配置文件并更新脚本：

```bash
# Save configuration
cat > ~/.openclaw/workspace/.context-compression-config.json << 'EOF'
{
  "version": "2.3",
  "maxTokens": <user_choice>,
  "frequencyMinutes": <user_choice>,
  "skipActive": <user_choice>,
  "enableSummaries": <user_choice>,
  "strategy": "priority-first",
  "priorityKeywords": [
    "重要", "决定", "记住", "TODO", "偏好",
    "important", "remember", "must", "deadline", "decision"
  ],
  "preserveUserMessages": true,
  "configuredAt": "$(date -Iseconds)"
}
EOF
```

**优先级关键词**：匹配这些关键词的内容将在截断之前被提取。
- 默认值包含中文和英文关键词
- 根据您的语言偏好进行自定义
- 使用正则表达式模式（例如，`"周[一二三四五六日"` 用于星期几）

### 第 3 步：配置定期任务

设置向导将引导您完成可选的定期任务配置。

### 第 4 步：更新脚本参数

使用用户配置更新 `truncate-sessions-safe.sh`：

```bash
# Create config env file for the script
cat > ~/.openclaw/workspace/skills/context-compression/scripts/.config << 'EOF'
export MAX_TOKENS=<user_max_tokens>
export SKIP_ACTIVE=<user_skip_active>
EOF
```

### 第 5 步：确认配置

告知用户：
```
✅ Configuration complete!

Truncation settings:
- Token limit: X tokens (~Y Chinese characters)
- Check frequency: Every Z minutes
- Skip active sessions: Yes/No

Next steps:
1. Real-time memory writes ensure continuity
2. System will auto-truncate session files
3. Run check-context-health.sh to check status
```

---

## 🎯 设计目标

| 目标 | 解决方案 |
|------|----------|
| 永远不超过上下文限制 | 预加载截断功能 + 上下文窗口管理 |
| 记住历史记录 | 分层内存：短时间窗口 + 压缩摘要 |
| 可靠性 | 关键操作不依赖代理上下文 |

---

## 🏗️ 架构概述

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Context Assembly Pipeline                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Total Context Budget: 80k tokens                                          │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ L4: Long-term Memory (MEMORY.md)                    ~5k tokens      │   │
│  │     - User preferences, important decisions, key facts              │   │
│  │     - Loaded first, always present                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ L3: Compressed Summaries (memory/summaries/)        ~10k tokens     │   │
│  │     - Daily summaries of older conversations                        │   │
│  │     - Compressed but semantically complete                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ L2: Short-term Window (recent sessions)             ~25k tokens     │   │
│  │     - Last N sessions, full conversation history                    │   │
│  │     - Loaded from session files directly                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ L1: Current Session                                  ~40k tokens     │   │
│  │     - Active conversation, full detail                              │   │
│  │     - Real-time writing to memory                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Reserved for system: ~10k tokens                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 实现方式

### 第 1 部分：系统级别的会话截断

**问题**：截断必须在加载上下文之前完成。

**解决方案**：运行独立的后台进程。

```bash
# Key parameters:
MAX_TOKENS=40000       # Keep last 40000 tokens per session
SKIP_ACTIVE=true       # Don't truncate sessions with .lock files
```

**设置**：
该技能在初始设置期间会自动配置定期会话维护。

---

### 第 2 部分：会话启动顺序

**每个会话在加载完整上下文之前必须执行以下顺序：**

```
Step 1: Read MEMORY.md (long-term memory)
Step 2: Read memory/YYYY-MM-DD.md (today + yesterday notes)
Step 3: Load recent session files (limited by window size)
Step 4: Assemble context within budget
Step 5: Begin conversation
```

**在 AGENTS.md 中的实现**：
```markdown
## Every Session

1. Read MEMORY.md — long-term memory
2. Read memory/YYYY-MM-DD.md (today + yesterday)
3. Session files are auto-truncated by system cron
4. Begin conversation
5. **Real-time memory writing**: Important info → write to memory files immediately
```

---

### 第 3 部分：实时内存写入

**关键**：必须在对话进行期间写入内存，而不是之后。

```
During Conversation:
│
├─→ User mentions preference → IMMEDIATELY update MEMORY.md
├─→ Important decision made → IMMEDIATELY update MEMORY.md
├─→ Task completed → IMMEDIATELY write to daily notes
└─→ Key information learned → IMMEDIATELY update relevant file
```

**为什么需要立即写入？**
- 会话可能随时被截断
- 摘要可能不可靠（当上下文超出限制时失效）
- 这是唯一能保证内存持久性的方法

---

### 第 4 部分：分层内存结构

#### L4：长期内存（MEMORY.md）

```markdown
# MEMORY.md

## User Profile
- Name: ...
- Preferences: ...
- Goals: ...

## Important Decisions
- [Date] Decision: ...

## Key Information
- ...
```

**更新触发器**：一旦提到重要信息，立即更新。

#### L3：每日摘要（memory/summaries/YYYY-MM-DD.md）

```markdown
# Summary - YYYY-MM-DD

## Key Events
1. Event 1: ...
2. Event 2: ...

## Decisions
- Decision 1

## Tasks
- ✅ Completed: ...
- 🔄 In Progress: ...

## Tokens: ~500 (compressed from ~10k original)
```

**生成方式**：每天通过 cron 运行（但不要依赖它来保存关键内存）。

#### L2：最近会话（session 文件）

- 每个会话的最后 2000 行
- 由系统 cron 自动截断
- 最近历史记录的完整对话详情

#### L1：当前会话

- 活动对话
- 实时写入内存文件

---

## 📊 上下文预算管理

### 令牌分配

| 层次 | 预算 | 来源 |
|-------|--------|--------|
| 系统消息 | 约 10k | OpenClaw 内部 |
| 长期内存（L4） | 约 5k | MEMORY.md |
| 每日摘要（L3） | 约 10k | memory/summaries/*.md |
| 最近会话（L2） | 约 25k | 会话文件（有限） |
| 当前会话（L1） | 约 30k | 活动对话 |
| **总计** | 约 80k | |

### 溢出处理

```
If context > 80k tokens:
│
├─→ Step 1: Skip older summaries (L3)
├─→ Step 2: Reduce recent sessions window (L2)
├─→ Step 3: Compress current session (handled by OpenClaw safeguard mode)
└─→ Always preserve: L4 (MEMORY.md) + L1 (current session)
```

---

## 🚀 脚本

### 1. truncate-sessions-safe.sh

安全截断，同时保持 JSONL 的完整性。

```bash
#!/bin/bash
# Truncates session files to last N lines
# Preserves JSONL line integrity
# Skips active sessions (with .lock files)
```

### 2. generate-daily-summary.sh

从每日笔记生成压缩摘要（不是从会话上下文中提取）。

```bash
#!/bin/bash
# Reads memory/YYYY-MM-DD.md
# Compresses to ~500 tokens
# Writes to memory/summaries/YYYY-MM-DD.md
```

### 3. check-context-health.sh

报告当前的上下文状态。

```bash
#!/bin/bash
# Reports:
# - Total session file sizes
# - Memory file sizes
# - Estimated context usage
# - Recommendations
```

### 4. session-start-hook.sh

在会话开始时加载上下文并检查内存健康状况。

```bash
#!/bin/bash
# Checks MEMORY.md exists
# Creates today's daily note if missing
# Outputs context summary for AI
```

### 5. session-end-hook.sh (v2.0)

检测未保存的内容并生成警报。

```bash
#!/bin/bash
# Checks MEMORY.md has today's updates
# Checks daily note freshness
# Detects potential unsaved important content
# Generates .session-alert if needed
```

### 6. mid-session-check.sh (NEW)

定期检查需要保存的重要内容。

```bash
#!/bin/bash
# Scans current session for keywords (重要/决定/TODO/偏好)
# Checks daily note freshness
# Outputs JSON recommendation: SAVE_NOW or OK
```

---

## ⚙️ 配置

### openclaw.json

```json
{
  "agents": {
    "defaults": {
      "contextTokens": 80000,
      "compaction": {
        "mode": "safeguard",
        "reserveTokens": 25000,
        "reserveTokensFloor": 30000,
        "keepRecentTokens": 10000,
        "maxHistoryShare": 0.5
      }
    }
  }
}
```

### 定期任务

会话维护会自动运行。在 `~/.openclaw/logs/truncation.log` 中检查技能日志以获取状态。

---

## ✅ 验证清单

设置完成后，验证以下内容：
- [ ] 截断脚本是否可执行：`ls -la scripts/truncate-sessions-safe.sh`
- [ ] 内存目录是否存在：`ls -la memory/ memory/summaries/`
- [ ] MEMORY.md 是否存在且是最新的
- [ ] AGENTS.md 是否具有实时内存写入规则

---

## 🔍 故障排除

### 上下文仍然超出限制

1. 检查截断脚本是否正在运行：`cat /root/.openclaw/logs/truncation.log`
2. 减少截断脚本中的 `MAX_LINES`
3. 减少 openclaw.json 中的上下文令牌数量

### 内存未持久化

1. 检查 AGENTS.md 是否具有实时写入规则
2. 验证内存文件是否正在更新：`ls -la memory/`
3. 确保重要信息立即写入，而不是在会话结束时写入

### 摘要未生成

1. 检查每日笔记是否存在：`ls -la memory/YYYY-MM-DD.md`
2. 手动运行摘要脚本进行测试
3. 检查 cron 日志：`grep CRON /var/log/syslog`

---

## 📚 参考资料

- [OpenClaw 压缩文档](https://docs.openclaw.ai)
- [分层内存架构](references/memory-architecture.md)
- [令牌估计指南](references/token-estimation.md)