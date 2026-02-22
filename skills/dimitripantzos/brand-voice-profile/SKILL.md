---
name: brand-voice
description: 定义并存储您的品牌语言风格档案，以便生成一致的内容。该档案记录了您的写作风格、词汇使用习惯、语气偏好以及内容创作规则。在生成符合您品牌风格的内容时、引入新的内容创作流程时，或确保跨平台内容的一致性时，均可使用该档案。
---
# 品牌语言风格（Brand Language Style）

通过设定明确的语言风格，可以让人工智能生成的内容听起来更像你的风格，而不是机器人的声音。

## 快速入门

### 创建你的语言风格档案

自然地与我们的助手交流：

> “我想设置我的品牌语言风格。我写作时风格随意，喜欢使用简短的句子，并且希望让技术性内容更容易被理解。我从不使用公司内部的行话。我的目标读者是独立开发者和自由职业者。”

助手随后应该：
1. 提出一些后续问题来了解你的写作风格
2. 在 `brand-voice/profile.json` 文件中创建你的语言风格档案
3. 在为你生成内容时使用这个档案

## 档案结构

```json
{
  "name": "Your Brand",
  "created": "2026-02-22",
  "updated": "2026-02-22",
  
  "voice": {
    "tone": "casual, direct, slightly irreverent",
    "personality": ["helpful", "opinionated", "no-BS"],
    "formality": "informal",
    "humor": "dry wit, occasional sarcasm"
  },
  
  "writing": {
    "sentenceLength": "short to medium, punchy",
    "paragraphLength": "2-3 sentences max",
    "structure": "lead with the point, then explain",
    "formatting": ["use headers", "bullet points over paragraphs", "bold key phrases"]
  },
  
  "vocabulary": {
    "use": ["ship", "build", "hack", "vibe", "solid"],
    "avoid": ["utilize", "leverage", "synergy", "best practices", "learnings"],
    "jargon": "minimal, explain when used",
    "contractions": true
  },
  
  "audience": {
    "who": "indie developers, solopreneurs, tech-curious founders",
    "assumes": "basic technical literacy",
    "explains": "complex concepts simply"
  },
  
  "content": {
    "topics": ["AI", "automation", "building in public", "productivity"],
    "avoid": ["politics", "controversial takes without data"],
    "cta_style": "soft, value-first",
    "hashtags": "minimal, 1-3 max"
  },
  
  "platforms": {
    "twitter": {
      "maxLength": 280,
      "style": "punchy, hook-first",
      "threads": "use for longer ideas, 3-7 tweets"
    },
    "linkedin": {
      "style": "slightly more professional but still human",
      "formatting": "line breaks for readability"
    },
    "blog": {
      "style": "conversational, like talking to a friend",
      "length": "800-1500 words typical"
    }
  },
  
  "examples": {
    "good": [
      "Shipped a thing. It's rough but it works. Feedback welcome.",
      "Hot take: most 'AI strategies' are just ChatGPT with extra steps.",
      "Here's what I learned building X for 6 months..."
    ],
    "bad": [
      "We are pleased to announce the launch of our innovative solution.",
      "Leveraging cutting-edge AI to drive synergies across the value chain.",
      "🚀🔥💯 HUGE NEWS!!! 🔥🚀💯"
    ]
  }
}
```

## 使用方法

### 在生成内容时

在写作之前，请参考你的语言风格档案：

```
Before generating:
1. Read brand-voice/profile.json
2. Match tone, vocabulary, and style
3. Check examples for calibration
4. Adapt for specific platform if specified
```

### 自我检查提示

生成内容后，请进行自我检查：
- 这种表达方式是否与“优秀”示例中的风格相似？
- 是否避免了“糟糕”示例中的错误表达？
- 是否符合语言风格和用词规则？
- 这种风格是否适合目标平台？

### 多品牌支持

对于需要为多个项目或机构生成内容的场景：

```
brand-voice/
  profiles/
    personal.json
    company.json
    client-a.json
```

引用方式：“使用客户A的语言风格档案来生成这篇文章。”

## 建立你的语言风格档案

### 面试流程

以对话的形式向用户提出以下问题（不要像列清单一样）：

1. **语言风格**：你如何用三个词来描述你的写作风格？
2. **目标读者**：你为谁写作？他们已经掌握了哪些知识？
3. **正式程度**：是像LinkedIn那样的正式风格，还是像Twitter那样的随意风格？介于两者之间？
4. **幽默感**：内容是严肃的？有趣的？带有讽刺意味的？还是完全不含幽默？
5. **喜欢的词汇**：有哪些短语或词汇让你觉得非常符合你的写作风格？
6. **不喜欢的词汇**：公司内部的行话？过度使用表情符号？需要避免什么？
7. **示例**：分享2-3篇你认为写得很真实的文章。
8. **反例**：分享一些你觉得风格不符合要求或过于正式的文章。

### 分析现有内容

如果用户已经有现有的内容，可以对其进行分析：

```
Read their last 10 posts/articles. Look for:
- Sentence length patterns
- Opening hook style
- Common phrases
- Vocabulary choices
- Formatting preferences
- CTA patterns
```

### 持续优化

语言风格档案不是固定不变的。在以下情况下请及时更新：
- 用户表示“这听起来不像我的风格”
- 出现新的写作主题或目标平台
- 你的写作风格发生变化

## 与其他工具的集成

### 与RSS阅读器的集成
```
1. Check RSS for trending topics
2. Pick an angle
3. Generate post using brand voice
4. Review and schedule
```

### 与内容调度工具（如Metricool）的集成
```
1. Load voice profile
2. Generate week of content
3. Apply platform-specific formatting
4. Queue for posting
```

### 与图片生成工具的集成
```
Voice profile can include visual style:
{
  "visual": {
    "aesthetic": "clean, minimal, lots of whitespace",
    "colors": ["#1a1a1a", "#f5f5f5", "#0066cc"],
    "avoid": ["stock photo vibes", "corporate clip art"]
  }
}
```

## 提示

1. **从简单开始**——你可以随时添加更多细节
2. **使用真实的例子**——实际例子比描述更具有参考价值
3. **考虑平台特性**——在Twitter上有效的表达方式可能在LinkedIn上不适用
4. **定期更新**——语言风格会随着时间而演变
5. **与用户一起测试**——生成内容后展示给用户，根据反馈进行优化