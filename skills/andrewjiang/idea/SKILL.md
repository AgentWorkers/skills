---
name: idea
description: "启动后台的 Claude 会话以探索和分析商业创意。只需说出“创意：[描述]”即可触发该会话。"
homepage: https://github.com/anthropics/claude-code
metadata: {"clawdbot":{"emoji":"💡","requires":{"bins":["claude","tmux","telegram"]}}}
---

# 想法探索技能

启动自主运行的Claude Code会话，深入探索商业创意。获取市场研究、技术分析、市场推广（GTM）策略以及可操作的推荐方案。

## 快速入门

**触发语句：** 说出“想法：[描述]”，助手将：
1. 在tmux中启动一个Claude Code会话
2. 全面研究并分析该想法
3. 将结果保存到`~/clawd/ideas/<slug>/research.md`文件中
4. 将文件发送到您的Telegram保存消息中
5. 完成后通过cron通知您

## 工作原理

```
User: "Idea: AI calendar assistant"
       ↓
┌─────────────────────────────────┐
│  1. explore-idea.sh starts      │
│  2. Creates tmux session        │
│  3. Runs Claude Code            │
│  4. Claude analyzes & writes    │
│  5. notify-research-complete.sh │
│     → Sends file to "me"        │
│     → Queues notification       │
│  6. Cron checks queue (1 min)   │
│  7. Notifies user in chat       │
└─────────────────────────────────┘
```

## 设置

### 先决条件
- `claude` CLI（Claude Code）
- `tmux`
- `telegram` CLI（supertelegram）
- 已启用cron的Clawdbot

### 1. 创建脚本

请查看`~/clawd/scripts/explore-idea.sh`以获取完整的实现细节。

**关键组件：**
- 创建包含提示和运行脚本的想法目录
- 清除OAuth环境变量，以使用Claude Max
- 以`--dangerously-skip-permissions`选项运行Claude
- 完成后调用通知脚本

### 2. 设置Cron作业

```bash
# Cron job to check notification queue every minute
{
  name: "Check notification queue",
  sessionTarget: "isolated",
  wakeMode: "now",
  payload: {
    kind: "agentTurn",
    message: "Check ~/.clawdbot/notify-queue/ for .json files...",
    deliver: true,
    channel: "telegram",
    to: "YOUR_CHAT_ID"
  },
  schedule: { kind: "every", everyMs: 60000 }
}
```

### 3. 添加AGENTS.md说明

```markdown
**When user says "Idea: [description]":**
1. Extract the idea description
2. Execute: `CLAWD_SESSION_KEY="main" ~/clawd/scripts/explore-idea.sh "[idea]"`
3. Confirm: "Idea exploration started. You'll be notified when complete."
```

## 分析框架

分析内容包括：

1. **核心概念分析** - 问题、假设、独特性
2. **市场研究** - 用户群体、目标市场（TAM/SAM/SOM）、竞争对手
3. **技术实现** - 技术栈、最小可行产品（MVP）范围、挑战
4. **商业模式** - 收入来源、定价策略、单位经济模型
5. **市场推广策略** - 上市方式、收购计划、合作伙伴关系
6. **风险与挑战** - 技术风险、竞争风险、监管风险
7. **结论与建议** - 明确的“是/否”判断及行动计划

## 结论类型

- 🟢 **强烈推荐** - 明显的机会，应积极追求
- 🟡 **有条件推荐** - 有潜力但需要验证
- 🟠 **建议调整方向** - 核心洞察良好，但执行方案需要改进
- 🔴 **不推荐** - 存在太多问题

## 示例输出

```
~/clawd/ideas/ai-calendar-assistant/
├── metadata.txt
├── prompt.txt
├── run-claude.sh
└── research.md    # 400-500 line comprehensive analysis
```

## 提示

- 分析一个想法通常需要3-5分钟
- 监控进度：`tmux attach -t idea-<slug>-<timestamp>`
- 即使通知失败，文件也会被发送到保存的消息中
- 检查`~/.clawdbot/notify-queue/`文件夹，查看是否有未发送的通知