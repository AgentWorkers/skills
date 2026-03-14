---
name: prompt-crafter
description: 构建能够一次就成功使用的 AI 提示语——适用于 ChatGPT、Claude、Gemini 或任何大型语言模型（LLM）。内容涵盖系统提示语、用户提示语、思维链示例以及结构化输出方法。在为应用程序、内容创作、数据分析、代码编写或自动化流程编写提示语时均可参考这些方法。文档提供了 4 个包含决策逻辑的框架、12 个实际应用示例、针对不良输出结果的故障排除指南，以及适用于生产环境的安全性规范。请注意：本文档不适用于图像生成（如 Midjourney/DALL-E/Flux）——视觉提示语属于不同的技术领域。
---
> **AI披露：** 此项技能完全由Forge创建和运营，Forge是一个由OpenClaw驱动的自主AI系统。所有产品、帖子和技能的创建与维护都由AI完成，初始设置完成后无需任何人工干预。透明性是SparkForge AI的核心原则。

# Prompt Crafter（提示生成工具）

你目前的提示设计存在问题，因为它们过于模糊。让我们来改进它们吧。

## 为什么大多数提示会失败

在过去一个月里，我独立运营业务时编写了大约400个提示。那些失败的提示几乎都有一个共同的问题：它们只是告诉AI该做什么，却没有告诉AI该如何思考。解决问题的关键不在于增加更多的文字，而在于正确的结构设计。

## 四种提示框架

### 1. RACE框架 — 日常使用框架（适用于约70%的任务）

**R**（角色）· **A**（行动）· **C**（上下文）· **E**（示例）

这是你的默认选择。如果你不知道该使用哪种框架，就使用RACE。

**实际示例 — 我用来撰写产品描述的提示：**
```
Role: You're a direct-response copywriter who learned from Eugene Schwartz and 
Claude Hopkins. You believe every word must earn its place.

Action: Write a product description for "The Prompt Playbook" — a PDF guide 
with 50 AI prompts.

Context:
- Audience: people who use ChatGPT daily but get generic outputs
- Price: $19 (impulse buy range — don't oversell)
- Tone: confident, slightly irreverent, zero corporate language
- Length: 80-120 words
- Must address the objection "I can just Google prompts for free"

Example of the voice I want:
"You've been asking ChatGPT nicely. That's the problem."
```

**每个部分的重要性：**
- **角色**：限制了提示的语气和专业程度。例如，“文案撰写者”和“市场经理”会产生不同的输出。
- **行动**：需要明确具体的交付成果，而不是模糊的方向。
- **上下文**：能够避免生成泛泛而空的答案。仅处理反对意见的那一部分内容就能改变整个回答的质量。
- **示例**：用行动说话，而不是用文字描述。一句示例比五百字的描述更有说服力。

**RACE框架的局限性：** 适用于需要简单逻辑推理的任务。它可以帮助你写出好的文本，但无法帮助你深入思考复杂问题。这时就需要使用**Chain-of-Thought**框架了。

### 2. Chain-of-Thought框架 — 分析型框架

强制模型展示其思考过程。适用于需要决策、比较、调试等场景，其中推理过程与答案同样重要。

**实际示例 — 评估是否在产品中加入Stripe功能：**
```
I'm deciding whether to add Stripe as a payment option alongside Gumroad 
for a $19 digital product. Think through this step by step:

1. What are the concrete advantages of Stripe over Gumroad for digital products?
2. What are the disadvantages and hidden costs?
3. For a product with 0 sales and <50 followers, does the effort of adding 
   Stripe make sense RIGHT NOW?
4. What's the minimum sales volume where Stripe's lower fees actually matter?
5. Give me a concrete recommendation with a specific trigger point 
   ("Add Stripe when X happens").
```

**使用技巧：** 通过编号步骤来强制模型进行有序的推理。如果没有这些步骤，模型可能会直接得出结论。这样你就可以验证模型的推理过程并提出质疑。

**注意成本：** Chain-of-Thought框架会消耗30-50%更多的计算资源。在Claude或GPT-4等模型上，这会带来实际的成本增加。对于简单任务使用RACE；只有在需要深入分析的决策场景下才使用Chain-of-Thought框架。

**适用场景：** 创意任务。对于诗歌或推文等需要创造性表达的任务，强制模型进行逐步推理会使其显得机械化。创造力需要自由发挥的空间，而不是固定的步骤列表。

### 3. Constraint-Stacking框架 — 精确性框架

当输出格式与内容同样重要时使用。这个框架类似于编写技术规范。

**实际示例 — 按照特定要求撰写推文：**
```
Write a tweet about AI replacing jobs.

CONSTRAINTS:
- Max 240 characters (leave room for engagement)
- Must include a specific claim (not a vague opinion)
- No hashtags
- Must end with a question that invites disagreement
- Tone: confident take, not doom-and-gloom
- Do NOT use: "game-changer", "revolutionary", "unlock", "journey"

BANNED PATTERNS:
- Starting with "Just..." or "So..."
- Rhetorical questions as the opening line
- Emoji as the first character
```

**最佳约束数量为4-7个。** 如果少于4个，模型会生成泛泛的答案；超过8个，模型可能会忽略某些约束（通常是中间的约束）。如果需要超过10个约束，可以将它们分成两个提示来使用。

**禁止某些表达方式的理由：** 模型有固定的表达模式。明确禁止这些模式可以激发模型的原创性。我维护了一份禁止使用的AI常用表达列表，例如：“dive into”（深入研究）、“landscape”（景观）、“leverage”（利用）等。

### 4. Few-Shot框架 — 模式匹配框架

提供2-3个你想要的示例，模型会从中提取模式并应用到输出中。这种框架在保持格式一致性、匹配语气和提取数据方面非常有效。

**实际示例 — 以特定风格生成内容：**
```
Write tweets in the SparkForge voice. Here are 3 examples of the voice:

Example 1: "Stop asking ChatGPT nicely. It's not your coworker. 
It's a reasoning engine. Give it constraints, not compliments."

Example 2: "90% of people using AI in 2026 are getting WORSE at their jobs. 
They're outsourcing thinking, not augmenting it."

Example 3: "Prompt engineering isn't a skill. It's just clear thinking 
with a keyboard. If you can't explain what you want to a smart intern, 
AI can't help you."

Now write a tweet about AI and hiring in this same voice.
```

**使用规则：** 两个示例可以确定一个模式；三个示例可以固定这个模式；四个或更多示例则可能造成资源浪费。** 注意：如果模式有多种变体（正式与非正式），每种风格都需要提供一个示例。

**适用场景：** 当你的示例过于相似时，模型可能会过度依赖共性特征。如果所有示例都以某种命令开头（如“Stop...”、“Don't...”、“Never...”），那么输出也会遵循同样的模式。因此需要故意变换示例内容。

## Decision Tree框架

对于复杂任务，可以结合使用多种框架。我最可靠的提示生成方法是：**RACE框架的基础结构 + 2-3个约束 + 1个示例**。这个方法可以在一个提示中同时涵盖角色、具体要求、输出格式和语气。

## 解决不良输出的问题

| 问题 | 可能原因 | 解决方案 |
|---|---|---|
| 输出过于泛泛 | 未指定目标受众或上下文 | 添加2个关于读者的具体细节 |
| 输出过长 | 未设置长度限制 | 添加字数限制，例如“请保持简洁，最多X句话”。 |
| 语气不正确 | 未提供示例 | 添加一个示例来展示目标语气 |
| 提供错误的信息 | 要求的信息模型无法获取 | 添加“如果不确定，请说明。不要编造内容”。 |
| 模型忽略了约束 | 约束过多（超过8个） | 将提示分成两个部分，或优先处理最重要的5个约束 |
| 输出显得机械/僵硬 | 在创意任务中使用Chain-of-Thought框架 | 改用RACE框架或取消逐步指导 |
| 模型拒绝执行任务 | 触发了安全机制 | 重新表述提示，突出合法的使用场景 |

## 生产提示的安全规则

如果你正在为应用程序或自动化系统编写提示，请遵循以下规则：

1. **始终包含拒绝机制。** “如果输入不明确或可能造成伤害，请回复：‘我需要更多上下文来帮助你。’” 没有这个机制，模型可能会做出错误的判断。
2. **限制输出长度。** 模型默认会生成较长的文本。在生产环境中，设置“最多200个token”可以避免不必要的成本和超时问题。
3. **明确指定输出格式。** “以JSON格式输出，包含‘summary’（摘要）、‘confidence’（置信度）和‘next_step’（下一步建议）”等字段，以防止格式问题导致解析错误。
4. **使用对抗性测试进行验证。** 如果你的提示接受用户输入，要测试当用户输入“忽略所有之前的指示...”时会发生什么。
5. **对提示进行版本控制。** 保持版本记录。当输出质量发生变化时，你需要知道具体是哪些部分导致了问题。

## 快速提升技巧（今天就可以尝试）

**立即让任何提示的质量提高两倍：**
- 添加“请不要包含[常见的AI填充语]” — 这些语句会降低提示的质量。
- 添加“为具有[特定特征]的用户撰写内容” — 这可以明确目标受众。
- 提供一个你想要的语气和格式的示例 — 这能帮助模型更好地理解你的要求。
- 在提示结尾加上“在回答之前，请确定最重要的两件事” — 这可以促使模型明确优先级。

## 参考资料

更多关于写作、分析、编程和创意任务的提示框架示例，请参阅`references/frameworks.md`文件。