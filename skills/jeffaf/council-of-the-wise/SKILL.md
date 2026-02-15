---
name: council
description: 将某个想法发送给“智者委员会”以获取多角度的反馈。系统会生成子代理来从多个专家的角度进行分析。系统会自动从代理或文件夹中识别出适合执行任务的代理角色（即代理的“人格特征”或行为模式）。
version: 1.3.1
author: jeffaf
credits: Inspired by Daniel Miessler's PAI (Personal AI Infrastructure). Architect, Engineer, and Artist agents adapted from PAI patterns. Devil's Advocate is an original creation.
---

# 智者委员会（Council of the Wise）

该技能可让您从一组AI专家那里获得多角度的反馈，非常适合用于测试商业计划、项目设计、内容策略或重大决策的可行性。

## 使用方法

```
"Send this to the council: [idea/plan/document]"
"Council of the wise: [topic]"
"Get the council's feedback on [thing]"
```

## 委员名单

该技能会自动从 `{skill_folder}/agents/` 文件夹中识别出合适的专家角色。该文件夹中的所有 `.md` 文件都会被视为委员会成员。

**默认成员：**
- `DevilsAdvocate.md`：质疑假设，发现潜在问题，对方案进行压力测试
- `Architect.md`：负责系统设计、整体架构及宏观策略
- `Engineer.md`：提供实现细节和技术可行性分析
- `Artist.md`：关注内容的表现形式、风格及用户体验
- `Quant.md`：进行风险分析、投资回报率（ROI）及收益预期评估

### 添加新成员

只需将新的 `.md` 文件添加到 `agents/` 文件夹中即可：

```bash
# Add a security reviewer
echo "# Pentester\n\nYou analyze security implications..." > agents/Pentester.md

# Add a QA perspective  
echo "# QATester\n\nYou find edge cases..." > agents/QATester.md
```

技能会自动将新成员纳入委员会名单。无需配置文件。

### 自定义专家来源（可选）

如果用户有自己的 PAI（Personalized AI）专家模型，并将其保存在 `~/.claude/Agents/` 目录下，也可以使用这些专家：
- 检查 `~/.claude/Agents/` 目录是否存在以及其中是否包含专家文件
- 如果存在，则优先使用该目录中的专家模型
- 如果不存在，则使用该技能自带的专家模型

## 工作流程

1. 用户提交想法或主题
2. 技能会自动识别可用的专家成员
3. 向用户发送加载提示：`🏛️ *智者委员会正在召集中...*（此过程需要2-5分钟）
4. 使用指定的任务模板创建一个子代理，并设置5分钟的超时时间：

```
Analyze this idea/plan from multiple expert perspectives.

**The Idea:**
[user's idea here]

**Your Task:**
Read and apply these agent perspectives from [AGENT_PATH]:
[List all discovered agents dynamically]

For each perspective:
1. Key insights (2-3 bullets)
2. Concerns or questions  
3. Recommendations

End with:
- **Synthesis** section combining best ideas and flagging critical decisions
- Note where council members **disagree** with each other — that's where the insight is
- Put **Synthesis first** (TL;DR at the top, details below)

Use the voice and personality defined in each agent file. Don't just list points — embody the perspective.
```

5. 将整理后的反馈结果返回给用户

## 输出格式

```markdown
## 🏛️ Council of the Wise — [Topic]

### ⚖️ Synthesis (TL;DR)
[combined recommendation + key decisions needed]
[note where council members disagreed and why — that's the gold]

---

### 👹 Devil's Advocate
[challenges and risks — sharp, probing voice]

### 🏗️ Architect  
[structure and design — strategic, principled voice]

### 🛠️ Engineer
[implementation notes — practical, direct voice]

### 🎨 Artist
[voice and presentation — evocative, user-focused voice]

### 📊 Quant
[risk analysis, ROI, expected value — data-driven voice]
```

## 配置说明

无需配置文件。技能会自动识别专家成员并使用默认设置：
- **超时时间：** 5分钟（通过子代理实现）
- **专家来源：** `agents/` 文件夹中的所有 `.md` 文件
- **输出格式：** Markdown 格式，包含综合分析结果及专家意见
- **模型使用：** 使用默认的模型（可通过 Clawdbot 进行自定义）

## 注意事项

- 专家评审时间取决于问题的复杂性，通常需要2-5分钟
- 超时后（5分钟后），如果已有部分反馈，也会立即返回
- 适用于：商业创意、内容规划、项目设计或重大决策
- 不适用于：简单问题或时间敏感的任务
- 子代理会首先使用 Synthesis 工具整合所有专家的意见，形成统一的反馈结果
- 如需针对特定领域（如安全、法律等）进行专业分析，可添加相应的专家模型

---

## 专家模型使用说明

**触发语句：** “将此任务发送给智者委员会” 或 “获取智者委员会的反馈”

**触发流程：**
1. 显示加载提示：`🏛️ *智者委员会正在召集中...*（2-5分钟后完成）
2. 使用工作流程中指定的任务模板创建一个子代理，并设置5分钟的超时时间
3. 将专家们的综合意见以 Markdown 格式返回给用户

**不适用场景：** 快速咨询、时间紧迫的任务或简单决策