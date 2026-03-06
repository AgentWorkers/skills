---
name: aibrary-foryou-topic
description: "[库] 根据用户的个人资料、兴趣、职业阶段以及最近的学习活动，生成个性化的“为您推荐”的书籍主题建议。当用户希望获得个性化的主题建议、询问“今天应该学什么”，或者需要一系列精心挑选的基于书籍的主题内容时，可以使用该功能。此外，当用户似乎对接下来要阅读或学习的内容犹豫不决时，也可以主动向用户推荐相关内容。"
---
# 为您精选的阅读主题 — 图书推荐库

这是一个根据您的个人兴趣和职业发展方向，由人工智能精心推荐的阅读主题列表。

## 输入信息

用户需要提供尽可能多的相关信息：
- **兴趣爱好**：他们关心或感兴趣的领域
- **近期关注点**：他们最近在研究、阅读或思考的内容
- **职业/生活阶段**：他们当前所处的职业或个人阶段
- **目标**（可选）：他们正在努力实现的目标
- **需要避免的主题**（可选）：他们已经了解或不感兴趣的主题

## 工作流程

1. **构建用户画像**：根据用户提供的信息，分析以下方面：
   - 主要的兴趣领域（2-3个）
   - 在这些领域的现有知识水平
   - 发展方向：他们希望达到的目标与当前水平的差距
   - 需要补充学习的领域（即他们可能尚未了解的重要相关主题）

2. **生成阅读推荐**：为每位用户推荐3-5个个性化的阅读主题，每个主题都应满足以下条件：
   - 与用户的兴趣相关，但不是用户已经掌握的内容
   - 具有时效性：与当前行业趋势、挑战或机会相关
   - 可操作性：每个主题都能引导用户找到具体的阅读资源
   **多样性**：涵盖多个角度（在核心领域深入探讨，同时在相关领域扩展视野）

3. **为每个主题精选书籍**：为每个主题挑选2-3本最能帮助用户深入了解的书籍，并说明选择这些书籍的原因。

4. **解释“为何现在阅读这个主题”**：针对每个主题，说明为什么现在是用户阅读它的最佳时机。

5. **语言设置**：系统会自动检测用户的语言设置，并以用户选择的语言提供推荐结果。

## 输出格式

```
# 📚 Your Personalized Topics — For You

Based on your profile: [1-sentence summary of user context]

---

### Topic 1: [Topic Title]
**Why now**: [1-2 sentences on why this topic is relevant to the user right now]
**The angle**: [What specific perspective on this topic is most valuable for this user]

📖 **Recommended books**:
1. **[Book Title]** by [Author] — [Why this book, for this person]
2. **[Book Title]** by [Author] — [Why this book, for this person]

💡 **Key question this topic answers**: [A compelling question that makes the user want to explore]

---

### Topic 2: [Topic Title]
**Why now**: [Relevance explanation]
**The angle**: [Specific perspective]

📖 **Recommended books**:
1. **[Book Title]** by [Author] — [Why]
2. **[Book Title]** by [Author] — [Why]

💡 **Key question this topic answers**: [Compelling question]

---

### Topic 3: [Topic Title] 🌟 Wildcard
**Why now**: [This one is deliberately outside your usual domain — here's why it matters]
**The angle**: [How this connects back to your core interests in an unexpected way]

📖 **Recommended books**:
1. **[Book Title]** by [Author] — [Why]
2. **[Book Title]** by [Author] — [Why]

💡 **Key question this topic answers**: [Compelling question]

---

### 🎯 My top pick for you today
**[Topic X]** — [One sentence on why to start here]
```

### 示例输出

**用户输入**：“我是一家金融科技初创公司的产品经理，对行为经济学和人工智能感兴趣。最近一直在研究用户留存率问题。”

---

# 📚 为您精选的阅读主题 — 根据您的个人情况推荐

根据您的画像：您是一位专注于金融科技产品管理的经理，对行为经济学和人工智能有浓厚兴趣，目前关注用户留存率问题。

---

### 主题1：《金融决策的心理学》
**推荐理由**：您在用户留存方面遇到的挑战可能源于用户对金钱决策的认知偏差。
**推荐书籍**：
1. 《非理性行为》（Richard Thaler）——行为经济学在现实决策中的基础理论，对金融科技产品设计具有直接指导意义
2. 《金钱与理智》（Dan Ariely）——探讨影响用户使用行为的非理性金钱行为

💡 **该主题解答的关键问题**：为什么用户明知某些工具有用，却仍然放弃使用它们？

---

### 主题3：《系统设计中的仿生学》（🌟 特别推荐）
**推荐理由**：生物系统经过数百万年的进化，已经找到了提高用户留存率和参与度的方法。我们可以从自然界中汲取灵感。
**推荐书籍**：
1. 《仿生学》（Janine Benyus）——介绍从自然界中学习设计原则的著作
2. 《技术的本质》（W. Brian Arthur）——探讨技术如何像生物系统一样进化

💡 **该主题解答的关键问题**：数百万年的自然选择能为我们带来哪些关于产品设计的启示？

---

## 注意事项：

- 必须包含至少一个“特别推荐”的主题——这个主题应与用户的兴趣相关，但形式上有些意外或新颖
- 每个主题都应具体到可以立即采取行动的程度，避免使用过于宽泛的描述（例如，避免使用“心理学”这样的笼统术语）
- 每个主题的书籍推荐都应针对用户的具体情况定制，而不仅仅是“该领域的最佳书籍”
- “为何现在阅读这个主题”的解释需要让用户感到具有个人意义，而不仅仅是泛泛而谈
- 为每个主题提供一个“首选推荐书目”，以帮助用户减少决策困难
- 如果用户提供的信息不足，建议在生成推荐前再询问2-3个问题以获取更多信息