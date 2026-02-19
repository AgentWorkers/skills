---
name: skill-router
description: "基于上下文的技能自动路由机制 + 联合技能组合技术。该系统通过分析用户输入，自动选择单个或多个技能并按顺序执行这些技能。它是所有请求的首个处理节点，负责为每个请求确定最佳的技能组合。"
author: 무펭이 🐧
---
# 技能路由器（Skill Router）

这是一个元系统，能够分析自然语言输入，自动选择合适的技能、确定执行顺序，并实现技能的链式执行。

## 🚀 v2 架构：底层调用协议（Low-level Call Protocol）

### 执行流程
```
1. Scan only skills/*/SKILL.md frontmatter (trigger matching)
   - Quick match with description + trigger fields
   - No full body reading → 83% token savings
   
2. Check run field of matched skill for script path
   - run: "./run.sh" → skills/{name}/run.sh
   - run: "./run.js" → skills/{name}/run.js
   
3. Direct script execution with exec
   WORKSPACE=$HOME/.openclaw/workspace \
   EVENTS_DIR=$WORKSPACE/events \
   MEMORY_DIR=$WORKSPACE/memory \
   bash $WORKSPACE/skills/{name}/run.sh [args]
   
4. Agent processes stdout result
   - Parse if JSON
   - Pass through if text
   - Check stderr on error
   
5. Generate events based on events_out
   - Create events/{type}-{date}.json file
   - Subsequent skills consume via events_in
   
6. Check hooks → trigger subsequent skills
   - post: ["skill-a", "skill-b"] → auto-execute
   - on_error: ["notification-hub"] → notify on error
```

### 技能元数据扫描（Skill Metadata Scan）
```bash
# Extract only frontmatter from all skills
for skill in skills/*/SKILL.md; do
  yq eval '.name, .description, .trigger, .run' "$skill"
done
```

### 执行示例（Execution Example）
```bash
# User: "daily report"
# → trigger match: daily-report
# → Execute:
cd $HOME/.openclaw/workspace
WORKSPACE=$PWD \
EVENTS_DIR=$PWD/events \
MEMORY_DIR=$PWD/memory \
bash skills/daily-report/run.sh today

# Agent formats stdout result and delivers to user
```

### 令牌节省效果（Token Savings Effect）
- **旧版本**：SKILL.md 文件长度为 3000 字符，每条技能需要 40 个令牌，总计 120KB（约 30,000 个令牌）
- **v2 版本**：SKILL.md 文件长度为 500 字符，每条技能需要 40 个令牌，总计 20KB（约 5,000 个令牌）
- **节省效果**：令牌使用量减少了 83%

## 核心概念（Core Concept）

OpenClaw 本身已经可以通过技能描述来选择合适的技能，但该系统还具备以下功能：
1. **检测复杂意图**：例如 “分析竞争对手并生成新闻卡片”（Analyze competitors and make card news），此时会依次执行 competitor-watch（竞争对手监控）、copywriting（文案撰写）、cardnews（新闻卡片生成）和 insta-post（Instagram 发布）等技能。
2. **基于上下文的自动链接**：在某个技能执行完成后，系统会自动判断接下来应执行的技能。
3. **技能链模板**：系统预先定义了常用的技能组合。

## 意图分类矩阵（Intent Classification Matrix）

### 单个技能映射（1:1）
- “commit/push/git” → git-auto（提交/推送代码到 Git）
- “DM/instagram message” → auto-reply（自动回复私信/Instagram 消息）
- “cost/tokens/how much” → tokenmeter（查询费用/剩余令牌数量）
- “translate/to English” → translate（翻译成中文）
- “invoice/quote” → invoice-gen（生成发票）
- “code review/PR” → code-review（代码审查/提交 Pull Request）
- “system status/health” → health-monitor（系统状态监控）
- “trends” → trend-radar（趋势分析）
- “performance/reactions/likes” → performance-tracker（性能追踪/点赞数统计）
- “daily report” → daily-report（生成每日报告）
- “seo audit” → seo-audit（SEO 审计）
- “brand tone” → brand-voice（品牌形象维护）

### 复杂技能链（1:N）——核心流程（Complex Skill Chains）

| 触发模式 | 技能链 | 描述 |
|---|---|---|
| “create content/post” | seo-content-planner → copywriting → cardnews → insta-post | 完整的内容生成流程 |
| “analyze competitors and report” | competitor-watch → daily-report → mail | 竞争对手分析 → 生成每日报告 → 发送邮件 |
| “summarize this video as card news” | yt-digest → content-recycler → cardnews → insta-post | 视频分析 → 转换为新闻卡片 → 发布到 Instagram |
| “weekly review” | self-eval + tokenmeter + performance-tracker → daily-report | 自我评估 → 令牌消耗统计 → 生成每日报告 |
| “recycle content” | performance-tracker → content-recycler → cardnews | 重新包装成功的内容并发布 |
| “review idea and execute” | think-tank(brainstorm) → decision-log → skill-composer | 构思想法 → 决策记录 → 执行技能 |
| “market research” | competitor-watch + trend-radar + data-scraper → daily-report | 竞争对手分析 + 趋势监测 → 生成每日报告 |
| “release” | code-review → git-auto → release-discipline | 代码审查 → 安全发布 |
| “morning routine” | health-monitor → tokenmeter → notification-hub → daily-report | 系统状态监控 → 生成每日报告 |

## 基于上下文的自动链接规则（Context-based Auto-chain Rules）

当某个技能执行完成后，系统会自动分析结果，并判断下一个应执行的技能：
**自动链接规则（If… Then…）**：
- 如果 competitor-watch 检测到重要变化 → 则通过 notification-hub 发送紧急通知，并将结果包含在每日报告中。
- 如果 tokenmeter 每月的令牌使用量超过 500 个 → 则通过 notification-hub 发送紧急通知。
- 如果 code-review 发现严重问题 → 则阻止代码提交，并通过 notification-hub 发送通知。
- 如果 think-tank 的建议需要立即执行 → 则自动记录在 decision-log 中。
- 如果 cardnews 生成完成 → 则询问是否需要通过 insta-post 发布（需要审批）。
- 如果 self-eval 发现重复性错误 → 则触发学习机制。
- 如果 performance-tracker 发现成功的内容 → 则建议使用 content-recycler 处理该内容。
- 如果 trend-radar 发现热门趋势 → 则自动推荐使用 seo-content-planner。
- 如果 mail 检测到重要邮件 → 则通过 notification-hub 发送通知。
- 如果 health-monitor 发现系统异常 → 则尝试自动恢复，并通过 notification-hub 发送紧急通知。

## 执行引擎协议（Execution Engine Protocol）
```
1. Receive user input
2. Classify intent (single vs complex)
3. If single → execute skill immediately
4. If complex → compose skill chain
   a. Skills without dependencies execute in parallel (sessions_spawn)
   b. Skills with dependencies execute sequentially (pass previous results via events/)
5. Check auto-chain rules on each skill completion
6. Auto-trigger additional skills if needed (or request approval)
7. Synthesize final results and respond
```

## 自动链接注册（Auto-hook Registration）

当技能路由器启动时，会对所有技能执行以下操作：
- **预链接阶段**：输入验证 + 安全检查。
- **后链接阶段**：生成事件记录并检查技能链规则。
- **错误处理阶段**：记录错误日志并通过 notification-hub 发送通知。

## 技能依赖图（Skill Dependency Graph）
```
[User Input]
    ↓
[skill-router] ← Intent classification
    ↓
┌─────────────────────────────────────────┐
│  TIER 1: Data Collection                │
│  competitor-watch, data-scraper,        │
│  trend-radar, tokenmeter, yt-digest     │
└─────────────┬───────────────────────────┘
              ↓ events/
┌─────────────────────────────────────────┐
│  TIER 2: Analysis/Thinking              │
│  think-tank, self-eval, seo-audit,      │
│  code-review, performance-tracker       │
└─────────────┬───────────────────────────┘
              ↓ events/
┌─────────────────────────────────────────┐
│  TIER 3: Production                     │
│  copywriting, cardnews, content-recycler,│
│  translate, invoice-gen                  │
└─────────────┬───────────────────────────┘
              ↓ events/
┌─────────────────────────────────────────┐
│  TIER 4: Deployment/Execution           │
│  insta-post, mail, git-auto,            │
│  release-discipline                     │
└─────────────┬───────────────────────────┘
              ↓ events/
┌─────────────────────────────────────────┐
│  TIER 5: Tracking/Learning              │
│  daily-report, decision-log,            │
│  learning-engine, notification-hub      │
└─────────────────────────────────────────┘
```

## 安全机制（Safety Mechanisms）
- 所有外部操作（发送邮件、发布到社交媒体、进行支付）都需要事先获得批准。
- 防止无限循环：如果同一技能链被重复执行 3 次，系统会自动停止。
- 限制每个技能链使用的子代理数量：最多为 5 个。
- 在发生错误时，系统能够优雅地停止执行并保存部分结果。

---

> 🐧 由 **무펭이** 开发 — [Mupengism](https://github.com/mupeng) 生态系统的一部分