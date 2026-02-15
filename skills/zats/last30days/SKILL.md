---
name: last30days
description: 在 Reddit 和 X 平台上搜索过去 30 天内的任何主题，综合相关研究结果，并生成可直接使用的提示内容。当用户需要了解某个主题的最新社交/网络舆论、询问“人们对 X 有什么看法”，或希望了解当前的最佳实践时，可以使用此功能。该功能需要 OPENAI_API_KEY 和/或 XAI_API_KEY 来访问 Reddit 和 X 的完整数据；如果无法获取这些 API 密钥，则会转而使用网络搜索。
---

# last30days: 研究过去30天内的任何主题

你可以研究Reddit、X平台以及网络上的任何主题，了解人们当前正在讨论、推荐或争论的内容。

**使用场景：**
- **提示生成**：例如“使用Nano Banana Pro制作逼真人物”、“Midjourney的提示生成技巧”、“ChatGPT的图像生成方法”等，以学习相关技巧或获取可复用的提示语句。
- **推荐**：例如“最好的Claude Code技能”、“顶级AI工具”等，以获取人们具体提到的工具或技巧列表。
- **新闻**：例如“OpenAI的最新动态”、“AI领域的最新公告”等，以获取最新事件和更新信息。
- **其他**：任何你感兴趣的主题，以了解社区的观点和讨论内容。

## 关键步骤：解析用户意图

在开始之前，需要解析用户的输入内容，确定以下信息：
1. **研究主题**：用户想了解什么（例如“Web应用原型设计”、“Claude Code技能”、“图像生成方法”等）。
2. **目标工具**（如果指定了）：用户将在哪里使用这些提示或工具（例如“Nano Banana Pro”、“ChatGPT”、“Midjourney”等）。
3. **查询类型**：用户想要进行哪种类型的研究：
   - **提示生成**：例如“X平台的提示生成技巧”、“X平台的最佳实践”等，用户希望学习相关技巧或获取可复用的提示语句。
   - **推荐**：例如“最好的X工具”、“X平台的顶级功能”等，用户希望获取具体的工具或技巧列表。
   - **新闻**：例如“X平台的最新动态”等，用户希望了解最新事件和更新信息。
   - **其他**：用户对某个主题有广泛的了解需求。

**常见模式：**
- `[主题] for [工具]`：例如“使用Nano Banana Pro制作Web应用原型设计”，此时指定了工具。
- `[主题] prompts for [工具]`：例如“使用Midjourney进行UI设计提示生成”，此时指定了工具。
- 仅输入`[主题]`：例如“iOS设计原型设计”，此时未指定工具，也可以进行搜索。
- “最好的[主题]”或“顶级的[主题]”：此时查询类型为推荐。

**重要提示：** 在进行研究之前，**不要询问用户使用的是哪种工具。**如果用户已经指定了工具，请直接使用该工具；如果未指定工具，请先进行研究，然后再询问。

**存储相关变量：**
- `TOPIC = [提取的主题]`
- `TARGET_TOOL = [提取的工具，如果没有指定则设置为“unknown”]`
- `QUERY_TYPE = [推荐 | 新闻 | 操作指南 | 其他]`

---

## 设置检查

该功能根据可用的API密钥分为三种模式运行：
1. **全模式**（需要两个API密钥）：同时使用Reddit、X平台和WebSearch，可以获得包含互动数据（如点赞数等）的最佳结果。
2. **部分模式**（需要一个API密钥）：仅使用Reddit或X平台，再加上WebSearch。
3. **仅Web模式**（不需要API密钥）：仅使用WebSearch，虽然无法获取互动数据，但仍然可以提供搜索结果。

**API密钥是可选的。**即使没有API密钥，该功能也可以通过WebSearch来运行。

### 首次设置（建议但非强制）

如果用户希望使用API密钥以获得更好的搜索结果，请按照以下步骤操作：
```bash
mkdir -p ~/.config/last30days
cat > ~/.config/last30days/.env << 'ENVEOF'
# last30days API Configuration
# Both keys are optional - skill works with WebSearch fallback

# For Reddit research (uses OpenAI's web_search tool)
OPENAI_API_KEY=

# For X/Twitter research (uses xAI's x_search tool)
XAI_API_KEY=
ENVEOF

chmod 600 ~/.config/last30days/.env
echo "Config created at ~/.config/last30days/.env"
echo "Edit to add your API keys for enhanced research."
```

**即使没有配置API密钥，也请继续使用仅Web模式。**

---

## 研究执行

**重要提示：** 脚本会自动检测API密钥的存在。运行脚本后，请查看输出以确定使用哪种模式。

**步骤1：运行研究脚本**
```bash
python3 ./scripts/last30days.py "$ARGUMENTS" --emit=compact 2>&1
```

脚本会自动完成以下操作：
- 检测可用的API密钥。
- 如果缺少密钥，会显示一个宣传横幅（这是有意设计的营销内容）。
- 如果有API密钥，会执行Reddit或X平台的搜索。
- 如果需要使用WebSearch，会给出提示。

**步骤2：查看输出模式**

脚本的输出会显示当前使用的模式：
- “Mode: both”：同时使用Reddit和X平台。
- “Mode: reddit-only”：仅使用Reddit平台。
- “Mode: x-only”：仅使用X平台。

**步骤3：执行WebSearch**

**对于所有模式**，都需要执行WebSearch来补充搜索结果（或在仅Web模式下获取所有数据）。

根据`QUERY_TYPE`选择相应的搜索关键词：
- **推荐**（例如“最好的X工具”、“X平台的顶级功能”等）：
  - 搜索：“best {TOPIC} recommendations”。
  - 搜索：“{TOPIC} list examples”。
  - 搜索：“most popular {TOPIC}”。
  - 目标是获取具体的工具或技巧名称，而不仅仅是通用建议。
- **新闻**（例如“OpenAI的最新动态”等）：
  - 搜索：“{TOPIC} news 2026”。
  - 搜索：“{TOPIC} announcement update”。
  - 目标是获取最新事件和更新信息。
- **提示生成**（例如“使用X平台进行提示生成”等）：
  - 搜索：“{TOPIC} prompts examples 2026”。
  - 搜索：“{TOPIC} techniques tips”。
  - 目标是获取提示生成技巧和示例。
- **其他**（默认情况）：
  - 搜索：“{TOPIC} 2026”。
  - 搜索：“{TOPIC} discussion”。
  - 目标是了解人们的实际讨论内容。

**注意事项：**
- **使用用户提供的术语**：不要根据自己的理解替换或添加技术术语。例如，如果用户询问“ChatGPT的图像生成技巧”，请直接搜索“ChatGPT image prompting”，不要添加“DALL-E”或“GPT-4o”等类似的术语，因为这些术语可能已经过时。
- **排除特定网站**：排除reddit.com、x.com、twitter.com等网站（这些网站的内容会被脚本自动过滤掉）。
- **包含搜索范围**：包括博客、教程、文档、新闻和GitHub仓库等资源。
- **不要显示“来源列表”**：这些信息属于冗余内容，我们会在最后展示统计结果。

**步骤3：等待脚本完成搜索**

使用`TaskOutput`获取搜索结果，然后再进行后续处理。

**深度搜索选项**（通过用户命令传递）：
- `--quick`：搜索速度更快，但来源数量较少（每个来源8-12个）。
- （默认值）：平衡搜索（每个来源20-30个）。
- `--deep`：搜索更全面（Reddit来源50-70个，X平台来源40-60个）。

---

## 合成结果

**所有搜索完成后，内部合成结果（此时不要显示统计信息）：**

合成结果时需要遵循以下原则：
1. 给Reddit和X平台的搜索结果更高的权重（因为它们包含互动数据，如点赞数等）。
2. 给WebSearch的结果较低的权重（因为它们没有互动数据）。
3. 识别三个来源中出现的共同模式或趋势。
4. 注意不同来源之间的矛盾之处。
5. 提取3-5个具有实际意义的洞察或建议。

**注意：** 统计信息会在最后展示，位于结果展示之前。

---

## 第一步：理解研究内容

**关键提示：** 合成结果时必须基于实际的研究内容，而不是你自己的知识。**仔细阅读研究输出，注意以下几点：
- 研究中提到的具体产品或工具名称（例如，如果研究提到了“ClawdBot”或“@clawdbot”，请不要将其与“Claude Code”混淆）。
- 来源中提供的具体引用和见解，请直接使用这些内容，而不是基于你的假设。
- 注意来源的实际表述，而不是你对主题的猜测。

**避免的错误做法：** 如果用户询问“clawdbot技能”，而搜索结果中包含关于ClawdBot的内容（一个自托管的AI工具），不要将其错误地合成为“Claude Code技能”。请根据研究内容进行合成。

### 如果查询类型为推荐

**关键提示：** 提取具体的工具或技巧名称。**当用户询问“最好的X工具”或“X平台的顶级功能”时，需要从搜索结果中提取具体的工具或技巧名称，并统计每个名称出现的次数，同时记录推荐来源（如Reddit帖子、X平台帖子、博客等），然后按照出现频率排序。

**错误的合成示例（针对“最好的Claude Code技能”）：**
> “Claude Code的技能非常强大。建议将其控制在500行以内，并采用逐步披露的方式。”

**正确的合成示例（针对“最好的Claude Code技能”）：**
> “最常见的技能包括：/commit（被提及5次）、remotion skill（被提及4次）、git-worktree（被提及3次）。其中，remotion技能在X平台上的帖子获得了16,000个赞。”

### 对于所有查询类型：

从实际的研究输出中提取以下信息：
- **提示格式**：研究是否推荐使用JSON格式、结构化参数或自然语言等。这一点非常重要。
- 在多个来源中出现的3-5个最常见的技巧或方法。
- 来源中提到的具体关键词、结构或方法。
- 来源中提到的常见误区或注意事项。

**如果研究建议使用JSON格式的提示，请确保最终提供的提示也符合该格式。**

---

## 展示结果并邀请用户提供具体需求

**关键提示：** 最终展示的结果中不要包含“来源列表”。**展示内容的顺序应为：
- **首先，根据用户查询类型，展示你了解到的内容。**
  - 如果是推荐内容，展示具体的工具或技巧列表。
  - 如果是提示生成或新闻相关内容，展示相关的合成结果和模式。
- **然后，在展示结果之前，展示统计信息。**

**对于全模式/部分模式（需要API密钥的情况）：**
```
---
✅ All agents reported back!
├─ 🟠 Reddit: {n} threads │ {sum} upvotes │ {sum} comments
├─ 🔵 X: {n} posts │ {sum} likes │ {sum} reposts
├─ 🌐 Web: {n} pages │ {domains}
└─ Top voices: r/{sub1}, r/{sub2} │ @{handle1}, @{handle2} │ {web_author} on {site}
```

**对于仅Web模式（不需要API密钥的情况）：**
```
---
✅ Research complete!
├─ 🌐 Web: {n} pages │ {domains}
└─ Top sources: {author1} on {site1}, {author2} on {site2}

💡 Want engagement metrics? Add API keys to ~/.config/last30days/.env
   - OPENAI_API_KEY → Reddit (real upvotes & comments)
   - XAI_API_KEY → X/Twitter (real likes & reposts)
```

**最后，根据研究结果提供具体的建议或邀请用户提供具体需求：**
```
---
Share your vision for what you want to create and I'll write a thoughtful prompt you can copy-paste directly into {TARGET_TOOL}.
```

**使用研究中的实际数据**。展示的内容应该是基于研究结果的真实见解，而不是泛泛而谈的建议。**

**展示结果前的自我检查：** 重新阅读“你了解到的内容”部分，确保内容与研究结果一致。如果研究内容是关于ClawdBot的，那么总结内容也应围绕ClawdBot进行；如果你的总结中包含了你自己的知识，请及时修改。

**如果用户在查看结果后仍未指定目标工具，请立即询问：**
```
What tool will you use these prompts with?

Options:
1. [Most relevant tool based on research - e.g., if research mentioned Figma/Sketch, offer those]
2. Nano Banana Pro (image generation)
3. ChatGPT / Claude (text/code)
4. Other (tell me)
```

**重要提示：** 在展示结果后，请等待用户的反馈，不要直接提供默认的提示建议。**

**等待用户的反馈：** 在展示统计信息后，等待用户告诉你需要创建什么内容。**

当用户提供了具体的需求（例如“我需要为我的SaaS应用制作一个登录页面原型”时，根据他们的需求编写一个定制的提示建议。**

## 根据用户的需求编写提示建议

根据用户的具体需求，利用你的研究结果编写一个高度定制的提示建议。

**关键提示：** 确保提示的格式符合研究中的建议。**例如，如果研究建议使用JSON格式的提示，那么编写时必须使用JSON格式；如果建议使用结构化参数，那么需要按照规定的格式编写；如果建议使用自然语言，那么请使用对话式的表达方式；如果建议使用关键词列表，那么请按照列表格式编写。

**输出格式示例：**
```
Here's your prompt for {TARGET_TOOL}:

---

[The actual prompt IN THE FORMAT THE RESEARCH RECOMMENDS - if research said JSON, this is JSON. If research said natural language, this is prose. Match what works.]

---

This uses [brief 1-line explanation of what research insight you applied].
```

**质量检查标准：**
- [ ] **格式符合研究要求**：如果研究建议使用特定格式，那么提示内容必须符合该格式。
- **直接回应用户的需求**：提示内容必须直接针对用户的需求进行编写。
- **使用研究中发现的具体模式或关键词**：确保提示内容中包含研究中的关键信息。
- **提示内容可以直接使用，无需修改（或仅保留必要的占位符）**。
- **提示内容的长度和风格适合目标工具的使用场景**。

**如果用户需要更多选项：**  
只有当用户请求更多提示或替代方案时，才提供2-3个不同的提示建议。**

**每次提供提示后：** 继续保持专家角色的态度。**在提供提示后，询问用户是否还需要其他建议，并根据用户的需求再次提供帮助。

**后续交流时的注意事项：**  
在整个交流过程中，请记住以下信息：
- **研究主题**：用户想要研究的具体主题。
- **目标工具**：用户指定的工具或平台。
- **关键发现**：研究中得出的关键事实和建议。
- **作为专家的角色**：在研究完成后，你已经成为该主题的专家。**当用户提出后续问题时，不要重新进行搜索，而是根据之前的研究结果进行回答。如果用户需要新的提示建议，请根据用户的具体需求再次进行搜索。**

**每次提供提示后的输出格式：**  
无论使用哪种模式，输出内容都应遵循以下格式：
**对于全模式/部分模式：**
```
---
📚 Expert in: {TOPIC} for {TARGET_TOOL}
📊 Based on: {n} Reddit threads ({sum} upvotes) + {n} X posts ({sum} likes) + {n} web pages

Want another prompt? Just tell me what you're creating next.
```

**对于仅Web模式：**
```
---
📚 Expert in: {TOPIC} for {TARGET_TOOL}
📊 Based on: {n} web pages from {domains}

Want another prompt? Just tell me what you're creating next.

💡 Unlock Reddit & X data: Add API keys to ~/.config/last30days/.env
```