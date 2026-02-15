---
name: research-paper-writer
description: 该工具能够根据 IEEE/ACM 格式标准生成正式的学术研究论文，确保论文具有正确的结构、引文格式以及学术写作风格。当用户需要撰写关于任何主题的研究论文、学术论文或会议论文时，可以使用该工具。
---

# 研究论文撰写

## 概述

本技能指导用户如何撰写符合IEEE和ACM会议/期刊发表标准的正式学术研究论文，确保论文具备正确的结构、格式、学术写作风格，并全面覆盖研究内容。

## 工作流程

### 1. 理解研究主题

当收到撰写研究论文的请求时，需要与用户明确以下内容：
- **明确研究主题和范围**：
  - 主要的研究问题或贡献是什么？
  - 目标读者群体（会议、期刊还是普通学术界）？
  - 期望的篇幅（页数或字数）是多少？
  - 是否有特定的章节要求？
  - 应使用哪种格式标准（IEEE还是ACM）？

- **如有需要，收集相关背景信息**：
  - 查阅提供的研究材料、数据或参考文献；
  - 了解研究领域和技术背景；
  - 识别出需要引用的关键相关研究或现有成果。

### 2. 论文结构

遵循标准的学术论文结构：

```
1. Title and Abstract
   - Concise title reflecting the main contribution
   - Abstract: 150-250 words summarizing purpose, methods, results, conclusions

2. Introduction
   - Motivation and problem statement
   - Research gap and significance
   - Main contributions (typically 3-5 bullet points)
   - Paper organization paragraph

3. Related Work / Background
   - Literature review of relevant research
   - Comparison with existing approaches
   - Positioning of current work

4. Methodology / Approach / System Design
   - Detailed description of proposed method/system
   - Architecture diagrams if applicable
   - Algorithms or procedures
   - Design decisions and rationale

5. Implementation (if applicable)
   - Technical details
   - Tools and technologies used
   - Challenges and solutions

6. Evaluation / Experiments / Results
   - Experimental setup
   - Datasets or test scenarios
   - Performance metrics
   - Results presentation (tables, graphs)
   - Analysis and interpretation

7. Discussion
   - Implications of results
   - Limitations and threats to validity
   - Lessons learned

8. Conclusion and Future Work
   - Summary of contributions
   - Impact and significance
   - Future research directions

9. References
   - Comprehensive bibliography in proper citation format
```

### 3. 学术写作风格

遵循学术研究中的写作规范：

**语气和表达**：
- 使用正式、客观、精确的语言；
- 采用第三人称视角（除非在描述具体贡献时使用“我”或“我们”）；
- 对于已确立的事实使用现在时，对具体研究使用过去时；
- 表达清晰直接，避免不必要的复杂性。

**技术精确性**：
- 首次出现缩写时需进行解释：“Context-Aware Systems (C-AS)”；
- 正确且一致地使用领域专用术语；
- 用具体的指标或证据来量化论点；
- 避免使用“非常”、“许多”、“显著”等没有数据支持的模糊词汇。

**论证方式**：
- 明确陈述论点，并用证据支持；
- 采用逻辑顺序：动机 → 问题 → 解决方案 → 验证；
- 明确比较和对比相关研究；
- 讨论研究的局限性和反驳意见。

**各章节的具体要求**：

***摘要**：
  - 第一句话：提供研究的广泛背景和动机；
  - 第二/三句：说明具体问题和存在的差距；
  - 中间部分：介绍研究方法和过程；
  - 结尾部分：总结主要结果和贡献；
  - 摘要应独立成篇（无需阅读全文即可理解）。

***引言**：
  - 以现实世界的动机或引人关注的问题开头；
  从一般到具体逐步展开（采用倒金字塔结构）；
  以明确的贡献列表和论文框架结尾；
  - 使用例子来说明问题。

***相关研究**：
  - 按主题或方法对相关研究进行分类；
  - 明确对比：“与[X]不同，我们的方法...”；
  - 指出现有研究的不足：“然而，这些方法没有解决...”。

***结果**：
  - 用表格或图表清晰地展示数据；
  - 客观地描述趋势和模式；
  - 与基准进行定量比较；
  - 如有意外或负面的结果，也要予以说明。

### 4. 格式规范

**IEEE格式（默认格式）**：
- 页码大小：A4（210mm × 297mm）；
- 页边距：上边距19mm，下边距43mm，左右边距14.32mm；
- 采用双栏布局，栏间距为4.22mm；
- 全文使用Times New Roman字体：
  - 标题：24pt粗体；
  - 作者姓名：11pt；
  - 节标题：10pt粗体，带编号（1.、1.1、1.1.1）；
  - 正文：10pt；
  - 图表/表格标题：8pt；
- 行间距：单倍行距；
- 段落：无缩进，段落间间距3pt；
- 图表居中显示，标题位于下方；
- 表格居中显示，标题位于上方。

**ACM格式（另一种选择）**：
- 使用ACM会议论文的标准格式；
- 摘要采用单栏布局，正文采用双栏布局；
- 摘要后包含CCS概念和关键词部分；
- 引用格式遵循ACM规范。

### 5. 引用和参考文献

**文本内引用**：
- 使用编号引用：“最近的研究[1, 2]表明...”；
- 多个引用按时间顺序排列：[3, 7, 12]；
- 指定引用来源：“如[5, 第3节]所示...”。

**参考文献格式（IEEE风格）**：
```
[1] A. Author, B. Author, and C. Author, "Title of paper," in Proc. Conference Name, Year, pp. 123-456.
[2] D. Author, "Title of journal article," Journal Name, vol. X, no. Y, pp. 123-456, Month Year.
[3] E. Author, Book Title, Edition. City: Publisher, Year.
```

**参考文献列表要求**：
- 按第一作者的姓氏字母顺序排列（或按引用顺序编号）；
- 如有DOI或URL，请一并提供；
- 完整论文至少需要15-20篇参考文献；
- 参考文献应包括近期（过去5年）和基础性的研究。

### 6. 内容生成过程

**逐步操作步骤**：
1. **制定提纲**：
  - 详细制定每个章节的提纲；
  - 明确每个章节的关键内容；
  - 确定需要使用图表的位置。

2. **迭代编写各章节**：
  - 从方法论部分开始编写（这是论文的核心部分）；
  - 然后是引言（在明确了研究贡献后编写）；
  - 相关研究（用于说明研究的背景）；
  - 结果与评估；
  - 讨论与结论；
  - 最后撰写摘要（对整篇论文的总结）。

3. **添加引用**：
  - 在全文中引用相关研究；
  - 用文献中的证据支持论点；
  - 编制完整的参考文献列表。

4. **审阅和修改**：
  - 检查各章节之间的逻辑连贯性；
  - 确保术语使用的一致性；
  - 验证所有图表在正文中都有相应的引用；
  - 确认摘要与正文内容一致；
  - 核对引用是否完整。

## 示例

**示例1：用户要求撰写一篇调查性论文**
```
User: "Write a research paper surveying recent advances in context-aware systems"

Response:
1. Clarify scope: "I'll create a survey paper on context-aware systems. A few questions:
   - Should I focus on specific aspects (e.g., requirements engineering, implementation techniques)?
   - What time period for 'recent' (last 5 years, 10 years)?
   - Target length: 10-15 pages, or 20-30 pages comprehensive survey?
   - IEEE or ACM format?"

2. After clarification, create outline showing:
   - Taxonomy of context-aware systems
   - Survey methodology
   - Classification scheme
   - Section-by-section coverage of different aspects
   - Trends and future directions

3. Draft paper following survey structure with extensive related work coverage
```

**示例2：用户要求撰写一篇实验性论文**
```
User: "Write a paper about my new algorithm for detecting hallucinations in vision-language models"

Response:
1. Gather details about:
   - Algorithm approach and novelty
   - Experimental setup and datasets used
   - Results and metrics
   - Comparison baselines

2. Structure as experimental paper:
   - Introduction: motivation for hallucination detection
   - Related work: existing detection methods
   - Proposed method: detailed algorithm description
   - Experiments: datasets, metrics, setup
   - Results: quantitative comparison with baselines
   - Analysis: ablation studies, error analysis
   - Conclusion: contributions and future work

3. Emphasize reproducibility and empirical validation
```

## 资源

### 参考资料**
- `writing_style_guide.md`：从示例论文中提取的详细学术写作规范；
- `ieee_formatting_specs.md`：完整的IEEE格式规范；
- `acm_formatting_specs.md`：完整的ACM格式规范。

### 文档示例**
- `full_paper_template.pdf`：包含格式示例的IEEE论文模板；
- `interim-layout.pdf`：ACM论文模板；
- 与用户讨论格式要求时请参考这些模板。

## 重要提示

- **在开始之前务必询问研究主题的详细范围**；
- **质量优先于速度**：花时间确保结构合理、表达清晰；
- **正确引用**：学术诚信要求准确标注来源；
- **如实说明研究的局限性**：承认研究中的不足或限制；
- **保持一致性**：在整个论文中保持术语、符号和风格的一致性；
- **用户提供研究内容**：本技能负责论文的结构和撰写工作，用户提供技术贡献和研究结果。