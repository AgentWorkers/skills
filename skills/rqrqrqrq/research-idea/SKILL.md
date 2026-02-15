---
name: idea-clawdbot
description: "启动后台的 Clawdbot 会话以探索和分析商业创意。输入 “Idea: [描述]” 即可触发该会话。该技能已重新编写，现在使用 `sessions_spawn` 而不是 `claude CLI` + `tmux` + `telegram CLI` 来执行操作。所有结果都会发送到当前聊天窗口，而不会保存到 “Saved Messages” 中。该功能完全不依赖任何外部组件（即零外部依赖）。"
metadata: {"clawdbot":{"emoji":"💡"}}
---

# 想法探索技能（Clawdbot原生功能）

启动自动化的后台会话，深入探索商业创意。利用Clawdbot内置的功能，获取市场研究、技术分析、市场进入策略（GTM）以及可操作的推荐方案。

## 快速入门

**触发语句：** 说出“想法：[描述]”，助手将：
1. 使用`sessions_spawn`创建一个后台子代理会话
2. 全面研究并分析该创意
3. 将结果保存到`~/clawd/ideas/<slug>/research.md`文件中
4. 将文件及总结内容发送回当前的Telegram聊天窗口

## 工作原理

```
User: "Idea: AI calendar assistant"
       ↓
┌─────────────────────────────────┐
│  1. Detect "Idea:" trigger      │
│  2. sessions_spawn background   │
│  3. Sub-agent researches        │
│  4. Writes research.md          │
│  5. Returns to main chat        │
│  6. Sends file + summary        │
└─────────────────────────────────┘
```

## 先决条件

- 已启用`sessions_spawn`功能的Clawdbot
- 无需使用任何外部命令行工具（完全原生支持）

## 在`AGENTS.md`中的集成

将以下内容添加到您的`AGENTS.md`文件中：

```markdown
## Idea Exploration

**When user says "Idea: [description]":**

1. Extract the idea description
2. Create a slug from the idea (lowercase, hyphens)
3. Use `sessions_spawn` to launch a background research session:
   - **task**: Use the template from `skills/idea-clawdbot/templates/idea-exploration-prompt.md`
   - **label**: `idea-research-<slug>`
   - **cleanup**: keep (so we can review the session later)
4. Confirm: "🔬 Research started for: [idea]. I'll ping you when done (usually 3-5 minutes)."
5. When the sub-agent completes, send the research file to the chat

**Result handling:**
- Research saved to: `~/clawd/ideas/<slug>/research.md`
- Send file as document via Telegram
- Include brief summary of verdict (🟢/🟡/🟠/🔴)
```

## 分析框架

分析内容包括：

1. **核心概念分析** - 问题、假设、独特性
2. **市场研究** - 用户群体、目标市场（TAM/SAM/SOM）、竞争对手
3. **技术实现** - 技术栈、最小可行产品（MVP）的范围、挑战
4. **商业模式** - 收入来源、定价策略、单位经济性
5. **市场进入策略** - 发布方式、市场拓展、合作伙伴关系
6. **风险与挑战** - 技术风险、市场竞争、法规问题
7. **结论与建议** - 明确的“是/否”判断及行动计划

## 结论类型

- 🟢 **强烈推荐** - 明显存在机会，应积极推进
- 🟡 **有条件推荐** - 有潜力但需要进一步验证
- 🟠 **建议调整方向** - 核心洞察良好，但执行方案需改进
- 🔴 **不推荐** - 存在太多问题

## 示例输出

```
~/clawd/ideas/ai-calendar-assistant/
├── metadata.txt
├── research.md    # 400-500 line comprehensive analysis
```

## 使用技巧

- 每个创意的分析通常需要3-5分钟
- 检查会话进度：`clawdbot sessions list --kinds spawn`
- 监控子代理的运行情况：`clawdbot sessions history <session-key>`
- 分析结果会自动发送回同一聊天窗口

## 模板变量

在创建子代理时，请在提示模板中替换以下内容：
- `{IDEA_DESCRIPTION}`：实际的想法描述
- `{IDEA_SLUG}`：适合URL使用的名称（例如：“ai-powered-calendar”）