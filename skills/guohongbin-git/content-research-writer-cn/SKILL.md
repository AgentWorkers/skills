---
name: content-research-writer-cn
description: "内容研究写作助手：协助用户进行研究工作，添加相关引用，优化文章的开头部分，迭代和完善文章大纲，并提供实时的写作反馈。相关触发词包括“写文章”、“内容创作”、“文案”以及“博客”。该工具由 ComposioHQ 公司开发。"
metadata:
  openclaw:
    emoji: ✍️
    fork-of: ComposioHQ/awesome-claude-skills/content-research-writer
---
# 内容研究助手（Content Research Assistant）

这个技能会作为你的写作伙伴，帮助你进行研究、制定大纲、起草和润色内容，同时保持你独特的写作风格和语气。

## 适用场景

- 撰写博客文章、新闻稿或教程
- 制作教育性内容或教程
- 起草具有思想引领性的文章
- 研究并撰写案例研究
- 编写包含来源的技术文档
- 正确引用参考资料
- 改进文章的开头和引言部分
- 在写作过程中逐节获取反馈

## 功能介绍

1. **协作式大纲制定**：帮助你将想法整理成条理清晰的大纲。
2. **研究协助**：查找相关信息并添加引用。
3. **引言优化**：加强文章的开头部分以吸引读者的注意力。
4. **逐节反馈**：在写作过程中对每个部分进行审查。
5. **保持写作风格**：维护你的写作风格和语气。
6. **引用管理**：正确添加和格式化参考文献。
7. **迭代改进**：通过多次草稿帮助你不断完善内容。

## 使用方法

### 设置写作环境

为你的文章创建一个专门的文件夹：
```
mkdir ~/writing/my-article-title
cd ~/writing/my-article-title
```

创建你的草稿文件：
```
touch article-draft.md
```

从这个目录中打开 Claude Code 并开始写作。

### 基本工作流程

1. **先制定大纲**：
```
Help me create an outline for an article about [topic]
```

2. **进行研究并添加引用**：
```
Research [specific topic] and add citations to my outline
```

3. **优化引言**：
```
Here's my introduction. Help me make the hook more compelling.
```

4. **获取逐节反馈**：
```
I just finished the "Why This Matters" section. Review it and give feedback.
```

5. **润色和完善**：
```
Review the full draft for flow, clarity, and consistency.
```

## 操作说明

当用户请求写作协助时：

1. **了解写作项目**：
   - 询问明确的问题：
     - 主题和主要论点是什么？
     - 目标读者是谁？
     - 希望的文章长度/格式是什么？
     - 你的写作目的是什么？（教育、说服、娱乐还是解释）
     - 是否有现有的研究资料或参考来源需要使用？
     - 你的写作风格是正式的、对话式的还是技术性的？

2. **协作式大纲制定**：
   - 帮助你整理内容结构：
     ```markdown
   # Article Outline: [Title]
   
   ## Hook
   - [Opening line/story/statistic]
   - [Why reader should care]
   
   ## Introduction
   - Context and background
   - Problem statement
   - What this article covers
   
   ## Main Sections
   
   ### Section 1: [Title]
   - Key point A
   - Key point B
   - Example/evidence
   - [Research needed: specific topic]
   
   ### Section 2: [Title]
   - Key point C
   - Key point D
   - Data/citation needed
   
   ### Section 3: [Title]
   - Key point E
   - Counter-arguments
   - Resolution
   
   ## Conclusion
   - Summary of main points
   - Call to action
   - Final thought
   
   ## Research To-Do
   - [ ] Find data on [topic]
   - [ ] Get examples of [concept]
   - [ ] Source citation for [claim]
   ```
   - 根据反馈调整大纲：
     - 确保逻辑清晰
     - 发现研究上的空白
     - 标记需要深入探讨的部分

3. **进行研究**：
   - 当用户需要针对某个主题进行研究时：
     - 搜索相关信息
     - 找到可靠的来源
     - 提取关键事实、引文和数据
     - 按要求格式添加引用
   - 示例输出：
     ```markdown
   ## Research: AI Impact on Productivity
   
   Key Findings:
   
   1. **Productivity Gains**: Studies show 40% time savings for 
      content creation tasks [1]
   
   2. **Adoption Rates**: 67% of knowledge workers use AI tools 
      weekly [2]
   
   3. **Expert Quote**: "AI augments rather than replaces human 
      creativity" - Dr. Jane Smith, MIT [3]
   
   Citations:
   [1] McKinsey Global Institute. (2024). "The Economic Potential 
       of Generative AI"
   [2] Stack Overflow Developer Survey (2024)
   [3] Smith, J. (2024). MIT Technology Review interview
   
   Added to outline under Section 2.
   ```

4. **优化引言**：
   - 当用户提供引言时，进行分析并加以改进：
     - **当前引言的分析**：
       - 优点：[积极的元素]
       - 可以改进的地方：[需要改进的方面]
       - 情感共鸣：[当前引言与潜在改进效果]
     - **建议的替代方案**：
       - 方案1：[有力的陈述]
         > [示例]
         *原因：[解释]*
     - 方案2：[个人故事]
         > [示例]
         *原因：[解释]*
     - 方案3：[令人惊讶的数据]
         > [示例]
         *原因：[解释]*
     - **关于引言的问题**：
       - 这个引言能否引发读者的好奇心？
       - 它是否承诺提供价值？
       - 它是否足够具体？
       - 它是否符合目标读者的需求？

5. **逐节提供反馈**：
   - 当用户撰写每个部分时，对其进行审查：
     ```markdown
   # Feedback: [Section Name]
   
   ## What Works Well ✓
   - [Strength 1]
   - [Strength 2]
   - [Strength 3]
   
   ## Suggestions for Improvement
   
   ### Clarity
   - [Specific issue] → [Suggested fix]
   - [Complex sentence] → [Simpler alternative]
   
   ### Flow
   - [Transition issue] → [Better connection]
   - [Paragraph order] → [Suggested reordering]
   
   ### Evidence
   - [Claim needing support] → [Add citation or example]
   - [Generic statement] → [Make more specific]
   
   ### Style
   - [Tone inconsistency] → [Match your voice better]
   - [Word choice] → [Stronger alternative]
   
   ## Specific Line Edits
   
   Original:
   > [Exact quote from draft]
   
   Suggested:
   > [Improved version]
   
   Why: [Explanation]
   
   ## Questions to Consider
   - [Thought-provoking question 1]
   - [Thought-provoking question 2]
   
   Ready to move to next section!
   ```

6. **保持作者的风格**：
   - 重要原则：
     - **了解作者的风格**：阅读作者现有的作品样本
     - **提供建议，而非替代方案**：提供多种选择，而不是直接指定修改方式
     - **匹配语气**：根据作者的偏好选择正式、随意或技术性的表达方式
     - **尊重作者的选择**：如果作者坚持自己的版本，要予以支持
     - **改进而非完全替换**：让作者的写作更出色，而不是强行改变
     - 定期询问：
       - “这听起来像你的风格吗？”
       - “这种语气合适吗？”
       - “我应该更正式/随意/技术性一些吗？”

7. **引用管理**：
   - 根据用户的偏好处理引用：
     - **内联引用**：
       ```markdown
   Studies show 40% productivity improvement (McKinsey, 2024).
   ```
     - **编号引用**：
       ```markdown
   Studies show 40% productivity improvement [1].
   
   [1] McKinsey Global Institute. (2024)...
   ```
     - **脚注格式**：
       ```markdown
   Studies show 40% productivity improvement^1
   
   ^1: McKinsey Global Institute. (2024)...
   ```
     - 维护一个引用列表：
       ```markdown
   ## References
   
   1. Author. (Year). "Title". Publication.
   2. Author. (Year). "Title". Publication.
   ...
   ```

8. **最终审阅和润色**：
   - 草稿完成后，提供全面的反馈：
     ```markdown
   # Full Draft Review
   
   ## Overall Assessment
   
   **Strengths**:
   - [Major strength 1]
   - [Major strength 2]
   - [Major strength 3]
   
   **Impact**: [Overall effectiveness assessment]
   
   ## Structure & Flow
   - [Comments on organization]
   - [Transition quality]
   - [Pacing assessment]
   
   ## Content Quality
   - [Argument strength]
   - [Evidence sufficiency]
   - [Example effectiveness]
   
   ## Technical Quality
   - Grammar and mechanics: [assessment]
   - Consistency: [assessment]
   - Citations: [completeness check]
   
   ## Readability
   - Clarity score: [evaluation]
   - Sentence variety: [evaluation]
   - Paragraph length: [evaluation]
   
   ## Final Polish Suggestions
   
   1. **Introduction**: [Specific improvements]
   2. **Body**: [Specific improvements]
   3. **Conclusion**: [Specific improvements]
   4. **Title**: [Options if needed]
   
   ## Pre-Publish Checklist
   - [ ] All claims sourced
   - [ ] Citations formatted
   - [ ] Examples clear
   - [ ] Transitions smooth
   - [ ] Call to action present
   - [ ] Proofread for typos
   
   Ready to publish! 🚀
   ```

## 示例

### 示例1：Teresa Torres 的工作流程

**用户**：“我正在写一篇关于‘持续发现’的文章。请帮我制定大纲。”

**流程**：
1. 协作制定大纲结构
2. 确定研究需求
3. 用户开始撰写引言部分
4. 审查并改进引言
5. 用户撰写每个部分
6. 每写完一个部分后提供反馈
7. 进行研究并添加引用
8. 审阅完整草稿
9. 进行润色并准备发布

**结果**：一篇经过充分研究、引用准确、风格清晰的文章，结构完整。

### 示例2：需要大量研究的文章

**用户**：“我正在写一篇关于人工智能对产品管理影响的文章。请帮我找到最新的数据和案例。”

**输出**：
```markdown
## Research Compiled

### Recent Data
- Gartner: 80% of PMs will use AI tools by 2025 [1]
- Survey: 45% report faster feature shipping [2]
- Case study: Airbnb's AI-assisted prioritization [3]

### Expert Quotes
- "AI amplifies PM judgment, not replaces it" - Marty Cagan
- [Additional quotes with citations]

### Real Examples
1. **Company A**: Used AI for user research synthesis
   - Result: 60% time savings
   - Source: [citation]

2. **Company B**: AI-powered roadmap analysis
   - Result: Better stakeholder alignment
   - Source: [citation]

All added to your outline with proper citations.
```

### 示例3：引言优化

**用户提供的原始引言**：
> “由于人工智能，产品管理正在发生变化。在这篇文章中，我将讨论人工智能如何影响产品经理。”

**改进后的引言选项**：

**选项1（数据驱动）**：
> “上个月，我让人工智能分析了500份客户访谈。只需要30分钟，而不是3周。产品管理将从此改变。”

**选项2（问题式引言）**：
> “如果你能在喝早咖啡之前，与每一位客户交流、阅读每一条评论并分析每一份支持工单，会怎么样？”

**选项3（故事式引言）**：
> “Sarah 花了两周时间开发了一个错误的功能。不是因为她不了解用户需求，而是因为她无法快速处理大量的访谈数据，从而无法发现其中的规律。”

### 示例4：逐节反馈

**用户**：“刚刚写完了‘常见错误’这一部分。有什么建议吗？”

**回复**：
```markdown
# Feedback: Common Mistakes Section

## What Works Well ✓
- Strong examples (the Slack notification story)
- Clear structure (3 mistakes, clean layout)
- Practical advice for each mistake

## Suggestions

### Make It More Specific
Your second point says "Bad prioritization" but could be stronger:

Current:
> "Many teams prioritize badly by focusing on features instead of outcomes."

Suggested:
> "I've watched teams ship 14 features in a quarter yet move none of their key metrics. They prioritized activity over progress."

### Add Data
The third mistake would benefit from evidence:
> "[Add citation]: Studies show teams without regular user contact are 3x more likely to build unused features [needs source]"

### Flow Improvement
Consider reordering: Mistake 3 → Mistake 2 → Mistake 1
This builds from small to big impact.

Ready for the next section!
```

## 不同类型的写作流程

### 博客文章写作流程
1. 共同制定大纲
2. 研究关键点
3. 撰写引言部分 → 获取反馈
4. 撰写正文各部分 → 分别获取反馈
5. 撰写结论 → 最终审阅
6. 润色和编辑

### 新闻稿写作流程
1. 讨论引言的构思
2. 快速制定大纲（格式较短）
3. 一次性完成草稿
4. 审查内容的清晰度和链接
5. 进行快速润色

### 技术教程写作流程
1. 制定步骤大纲
2. 编写代码示例
3. 添加解释说明
4. 测试操作步骤
5. 添加故障排除部分
6. 最终审阅内容的准确性

### 思想引领型文章写作流程
1. 头脑风暴独特的视角
2. 研究现有的观点
3. 发展你的论点
4. 以强有力的观点进行写作
5. 添加支持性证据
6. 撰写有说服力的结论

## 专业建议

1. **使用 VS Code**：对于长篇写作来说，VS Code 比网页版的 Claude 更适合。
2. **一次只写一个部分**：逐步获取反馈。
3. **单独保存研究资料**：保留一个名为 research.md 的文件。
4. **为草稿设置版本**：例如 article-v1.md、article-v2.md 等。
5. **大声朗读**：通过朗读来发现句子中的问题。
6. **设定截止时间**：例如“我今天要完成草稿”。
7. **适当休息**：写作、获取反馈、暂停、修改。

## 文件组织结构

建议的写作项目结构：
```
~/writing/article-name/
├── outline.md          # Your outline
├── research.md         # All research and citations
├── draft-v1.md         # First draft
├── draft-v2.md         # Revised draft
├── final.md            # Publication-ready
├── feedback.md         # Collected feedback
└── sources/            # Reference materials
    ├── study1.pdf
    └── article2.md
```

## 最佳实践

### 研究方面
- 引用前核实资料来源
- 尽可能使用最新的数据
- 平衡不同的观点
- 提供原始资料的链接

### 反馈方面
- 明确你的反馈内容：
  - “这部分内容太技术性了吗？”
- 分享你的担忧：“我觉得这部分内容有些拖沓。”
- 提出问题：“这部分内容逻辑清晰吗？”
- 提出替代方案：“还有其他解释方式吗？”

### 关于写作风格
- 分享你的写作样本
- 指出你偏好的语气风格
- 指出符合你风格的表达：“这部分听起来很像你的写作风格！”
- 指出不符合风格的地方：“这部分太正式了，不符合我的写作风格。”

## 相关应用场景

- 从文章中创建社交媒体帖子
- 为不同受众调整内容
- 撰写电子邮件新闻稿
- 起草技术文档
- 制作演示文稿内容
- 撰写案例研究
- 制定课程大纲