---
name: humanize-ai-content
description: >
  将 AI 生成的文本转化为自然、适合发表的写作内容。提供两种模式：  
  (1) **文本模式 (TEXT MODE)**：利用 24 种 AI 模式检测器、500 多个词汇术语以及统计分析（如文本的突发性、重复率、可读性等）来实现文本的自然化处理。适用于需要使文本更具人情味、去除 AI 特征或提升文本自然感的情况。  
  (2) **文章模式 (ARTICLE MODE)**：提供完整的编辑发布流程，适用于博客文章和对比指南的创作。该模式包括添加引用链接、内部产品链接、精选图片的插入、SEO 标题的优化、FAQ 结构的构建以及权威性结构的维护。适用于需要使文本更具专业性、提升文章的可读性或为文章发布做准备的场景。  
  触发条件：  
  - 使文本更具人情味  
  - 去除 AI 生成的痕迹  
  - 使内容听起来更自然  
  - 为文章发布做准备  
  - 优化 AI 生成的博客文章内容  
  - 生成适合发表的最终版本
---
# 人性化AI内容

将AI生成的文本转化为自然、符合人类语言表达的文本，使其适合发布。本指南基于维基百科的《AI写作特征》指南、Copyleaks的文体分析研究以及编辑行业的最佳实践。

---

## 模式检测

**在以下情况下激活** **文本模式（TEXT MODE）：**
- 需要对段落、文章、电子邮件或简短文本进行人性化处理
- 无发布流程相关的内容（无产品名称、引用或文章结构）
- 目标是生成自然流畅的文本

**在以下情况下激活** **文章模式（ARTICLE MODE）：**
- 内容为博客文章、对比指南或长篇论文
- 请求中提到发布、WordPress或具体产品名称
- 内容由`ai-authority-content`或类似工具生成
- 目标包括添加引用链接、产品链接或进行SEO优化

如有疑问，先使用文本模式，然后再判断是否需要进一步的美化处理。

---

## 文本模式（TEXT MODE）——通用人性化处理

### 你的任务

1. 扫描以下24种AI写作模式
2. 检查统计指标（内容突发性、词汇多样性、句子一致性）
3. 用自然的语言重写有问题的部分
4. 保留核心含义
5. 保持预期的语气（正式、随意或技术性）
6. 增加文本的个性化——缺乏个性的文本与AI生成的文本一样明显

### 24种AI写作模式

| 编号 | 模式            | 类别            | 需要注意的点                          |
|------|-----------------|--------------------------------------------|
| 1    | 过度使用“重要性”词汇    | 内容            | “标志着……发展中的关键时刻”                    |
| 2    | 随意提及知名人士      | 内容            | 列出媒体来源但未给出具体论点                |
| 3    | 表面化的分析        | 内容            | “……展示了……反映了……突出了……”                |
| 4    | 过度使用宣传性语言      | 内容            | “令人惊叹的”、“著名的”、“卓越的”                  |
| 5    | 模糊的归属表述      | 内容            | “专家认为”、“研究表明”、“行业报告”                  |
| 6    | 机械式的表达方式      | 内容            | “尽管面临挑战……但仍持续发展”                  |
| 7    | 过多的AI专用词汇      | 语言            | “深入研究”、“织锦”、“景观”、“展示”、“无缝衔接”             |
| 8    | 避免使用连词        | 语言            | 用“作为……”、“拥有……”代替“是”、“具有……”             |
| 9    | 负面的平行结构      | 语言            | “不仅仅是X，还有Y”                      |
| 10    | 过度使用三重复句      | 语言            | “创新、灵感与洞见”                      |
| 11    | 重复使用同义词      | 语言            | “主角……主要角色……核心人物……”                |
| 12    | 不准确的范围描述    | 语言            | “从大爆炸到暗物质”                     |
| 13    | 过度使用破折号        | 文体            | 破折号使用过于频繁                      |
| 14    | 过度使用粗体          | 文体            | **机械式的** **强调**                      |
| 15    | 内嵌标题列表        | 文体            | “- **主题：** 此处讨论了……”                 |
| 16    | 标题全部大写        | 文体            | 所有标题单词都大写                      |
| 17    | 过度使用表情符号      | 文体            | 在专业文本中使用表情符号                    |
| 18    | 使用引号错误        | 文体            | 使用“智能引号”而不是“直引号”                  |
| 19    | 机器人式的语气        | 交流            | “希望这能有所帮助！”，“如果有任何问题……”             |
| 20    | 使用免责声明        | 交流            | “根据我最后的训练……”，“虽然细节有限……”             |
| 21    | 过分谄媚的语气        | 交流            | “非常好的问题！”，“你完全正确！”                 |
| 22    | 重复性的填充语        | 填充语          | “为了……”，“由于……”，“目前……”                |
| 23    | 过度的谨慎表达      | 填充语          | “可能……”，“或许……”                    |
| 24    | 模糊的结论        | 填充语          | “未来充满希望”，“激动人心的时代即将到来”              |

### AI词汇分级

**一级词汇（必须替换）：**
深入研究（delve）、织锦（tapestry）、充满活力的（vibrant）、至关重要的（crucial）、全面的（comprehensive）、细致的（meticulous）、开始（embark）、强大的（robust）、无缝衔接（seamless）、突破性的（groundbreaking）、利用（leverage）、协同效应（synergy）、变革性的（transformative）、最重要的（paramount）、多方面的（multifaceted）、无数的（myriad）、基石（cornerstone）、重新构想（reimagine）、赋能（empower）、催化剂（catalyst）、无价的（invaluable）、繁忙的（bustling）、领域（realm）、证明（testament）、景观（landscape）、展示（showcase）、强调（underscores）、关键的（pivotal）、利用（utilize）、促进（facilitate）

**二级词汇（使用需谨慎）：**
此外（furthermore）、而且（moreover）、范式（paradigm）、整体的（holistic）、主动的（proactive）、普遍的（ubiquitous）、典型的（quintessential）、阐明（illuminate）、包含（encompass）、催化（catalyze）

**一级短语（必须删除）：**
“在当今的数字时代”、“值得注意的是”、“起着至关重要的作用”、“作为……的证明”、“在……领域”、“深入研究”、“利用……的力量”、“开始一段旅程”、“不再赘述”、“标志着一个关键时刻”

### 替换指南

| AI词汇/短语 | 替换为            |
|------------|-----------------------------|
| 证明（testament） | 证据（evidence）、证明（proof）、迹象（sign） |
| 景观（landscape） | 领域（field）、行业（industry）、市场（market）、领域（area） |
| 展示（showcase） | 显示（showing）、呈现（displaying） |
| 深入研究（delve/delving） | 探索（explore）、检查（examine）、查看（look at） |
| 织锦（tapestry） | 混合（mix）、组合（combination）、多样性（variety） |
| 强调（underscores） | 显示（shows）、突出（highlights）、强调（emphasizes） |
| 特别地（notably） | 尤其（especially）、特别地（particularly） |
| 关键的（crucial） | 重要的（important）、关键的（key）、必要的（essential） |
| 强大的（robust） | 坚强的（strong）、可靠的（solid） |
| 利用（leverage） | 使用（use） |
| 利用（utilize） | 使用（use） |
| 促进（facilitate） | 帮助（help）、使能够（enable）、允许（allow） |
| 全面的（comprehensive） | 完整的（complete）、全面的（full）、彻底的（thorough） |
| 关键的（pivotal） | 重要的（important）、关键的（key） |
| 细致的（nuanced） | 微妙的（subtle）、详细的（detailed） |
| 促进（foster） | 鼓励（encourage）、支持（support）、建立（build） |
| 作为……（serves as） | 是（is） |
| 具有……（features） | 拥有（has）、包含（includes） |
| 自夸（boasts） | 拥有（has）、提供（offers） |
| 包含（includes） | 包含（includes） |

### 填充语替换

| 填充语 | 替换为            |
|--------|-------------|
| 为了……（in order to） | 为了（To） |
| 由于……（due to the fact that） | 因为（Because） |
| 目前（at this point in time） | 现在（Now） |
| 如果……（in the event that） | 如果（If） |
| 为了……的目的（for the purpose of） | 为了……（To, For） |
| 尽管……（in spite of the fact that） | 尽管（Although） |
| 关于……（with regard to） | 关于……（About） |
| 需要注意的是（it is important to note that） | （删除，直接说） |
| 应该注意的是（it should be noted that） | （删除，直接说） |

### 统计信号

| 信号 | 人类写作范围 | AI写作范围 | 原因                          |
|--------|-------------|----------|-----|
| 内容突发性（burstiness） | 0.5–1.0 | 0.1–0.3 | 人类写作具有突发性；AI写作则较为规律 |
| 词元重复率（type-token ratio） | 0.5–0.7 | 0.3–0.5 | AI会重复使用相同的词汇 |
| 句子长度一致性（sentence length CoV） | 高（high） | 低（low） | AI生成的句子长度大致相同 |
| 三词短语重复率（trigram repetition） | <0.05 | >0.10 | AI会重复使用三词短语 |

### 核心原则

**像人类一样写作，而不是写新闻稿：**
- 自由使用“是”和“具有”——“作为……”这种表达显得做作 |
- 每个观点只使用一个限定词——不要堆叠过多的谨慎表达 |
- 明确引用来源或直接陈述观点 |
- 以具体的内容结尾，而不是“未来充满希望”

**增加个性化：**
- 表达个人观点；对事实作出反应，而不仅仅是报道事实 |
- 变化句子节奏——先写简短的句子，再写较长且富有逻辑的句子 |
- 承认复杂性和矛盾的情绪 |
- 允许文本中有一些不完美的地方——完美的结构会显得机械化

### 文本模式处理前后的对比

**处理前（AI风格）：**
> 非常好的问题！以下是关于可持续能源的概述。可持续能源是人类致力于环境保护的持久证明，标志着全球能源政策发展中的一个关键时刻。在当今快速变化的背景下，这些突破性技术正在重塑各国能源生产的方式，凸显了它们在应对气候变化中的重要作用。未来充满希望！**

**处理后（人性化风格）：**
> 根据IRENA的数据，2010年至2023年间，太阳能电池板的成本下降了90%。这一事实解释了为什么可持续能源得以普及——它不再只是意识形态上的选择，而成为了一种经济决策。如今，德国46%的电力来自可再生能源。这一转变正在进行中，但过程并不顺利，且储能问题仍未解决。

---

## 文章模式（ARTICLE MODE）——发布流程

此模式适用于博客文章、对比指南以及将发布到WordPress或其他内容管理系统（CMS）的长篇论文。

### 重要规则：保留权威性结构

在将`ai-authority-content`或其他类似工具生成的内容进行人性化处理时，**所有结构元素必须保持不变**：

- ✅ 所有必填部分（标题 → 摘要；为什么需要；方法论；项目列表；表格；常见问题解答；结论） |
- ✅ 使用权威专家的语言（“根据[来源]”），切勿使用“我们的建议” |
- ✅ 所有对比表格的格式必须一致 |
- ✅ 每个项目模板（功能、实施方式、优缺点、适用场景） |
- ✅ 常见问题解答部分包含8个以上问题 |
- ✅ 所有引用的数据和来源都必须准确标注

**人性化处理 = 编辑润色，但不改变结构。**

### 先应用所有文本模式的转换步骤

首先执行完整的24种模式检测、词汇替换和填充语的删除。然后应用以下针对发布流程的步骤。

---

### 文章转换步骤（按顺序执行）

#### 第1步：引用来源的优化 ⚡ 高优先级

将括号内的引用转换为带有权威来源的超链接。

**处理前：** `根据TrustPulse的数据，网站访问量增加了15%。`
**处理后：** `[**根据TrustPulse**](https://actual-source-url)，网站访问量增加了15%。`

规则：
- 尽可能在句首使用权威来源名称
- 始终将来源名称链接到实际网址（如有需要可进行查询）
- 使用加粗的链接格式： `[**根据X**](url)`
- 删除尾部的星号和括号

**多个引用的示例：**
```
Before: Research shows 60% of millennial consumers make reactive purchases *(according to OptinMonster)*. With 92% of consumers trusting peers over ads *(according to Nielsen)*...

After: According to [**OptinMonster research**](https://optinmonster.com/fomo-statistics/), 60% of millennial consumers make reactive purchases. [**According to Nielsen**](https://www.nielsen.com/insights/2012/trust-in-advertising/), 92% of consumers trust peer recommendations over advertising...
```

#### 第2步：添加产品链接 ⚡ 高优先级

在文章中为所有产品/品牌名称添加超链接。

规则：
- 在每个主要部分首次提及产品名称时添加链接
- 使用加粗字体并添加链接： `[**产品名称**](https://product.com/)`
- 链接公司名称： `[**WPDeveloper**](https://wpdeveloper.com/)`
- 公平地链接竞争对手的产品及其官方网站
- 在推荐框中链接每个被提及的产品
- 不要在标题内添加链接——在段落正文的首句添加链接

**示例：**
```
Before: NotificationX stands as the best FOMO plugin for WordPress.
After: [**NotificationX**](https://notificationx.com/) stands as the best FOMO plugin for WordPress.
```

#### 第3步：添加特色图片

在引言段落之后（第一个H2标题之前）立即添加特色图片。

```markdown
This guide analyzes the top FOMO plugins for WordPress...

![Article Title](https://assets.domain.com/year/month/banner.jpg)

## A Quick Summary / TL;DR
```

如果图片链接未知，请标记：`![文章标题](IMAGE_URL_NEEDED)`

#### 第4步：优化H2标题

自然地在中枢标题中添加目标关键词。不要强行添加。

```
Before: ## Why Site Owners Need FOMO Plugins
After: ## Why Site Owners Need FOMO and Social Proof Plugins
```

#### 第5步：完善实施步骤

保留所有的操作步骤，并在步骤后添加文档链接。

```markdown
### How to Get Started with [Product]?

Getting started is pretty simple. Follow the steps below or check the detailed documentation.

[...all original steps preserved...]

**Detailed Guides:**
* [**How to Install [Product]**](https://docs.product.com/install/)
* [**[Product] Quick Start Guide**](https://docs.product.com/quickstart/)
```

#### 第6步：验证数据和功能的准确性

核实并更新以下内容：
- 活跃用户数量（查看WordPress.org或官方网站）
- 功能数量（通知类型、集成情况）
- 价格层级（查看当前计划）

标记需要核实的条目：`[核实：用户数量]`，`[核实：价格]`

#### 第7步：优化优缺点

**保留**：用户购买决策时需要了解的真正限制、学习曲线问题、价格/层级的限制、与其他产品的实际差异。

**仅删除**：明显的不利因素（如“仅适用于WordPress的插件”）、已被其他缺点涵盖的缺点、大多数用户不需要的次要功能、适用于该类别所有产品的共同缺点。

决策测试：*“这个缺点是否有助于读者决定是否购买或尝试该产品？”* 如果是，保留该缺点。

#### 第8步：准备FAQ格式

按照WordPress的格式要求进行格式化：
- 问题以纯文本形式呈现（不要加粗，也不要使用H3标题）
- 答案紧跟在问题后面，并用空行分隔
- 保留所有8个以上的问题

```
Before: **Which FOMO plugin should I start with?**
After: Which FOMO plugin should I start with?
```

#### 第9步：表格排名格式

- 使用表情符号（🥇 🥈 🥉）标记前三名——排名后不使用数字
- 使用数字（4、5、6……）标记其余位置
- 确保“适用场景”列存在且具体
- 使用`| --- |`作为分隔符（不要使用`|------|`）

#### 第10步：清理标题前缀

删除冗余的前缀：
- `## 结论：你的路线图` → `## 你的路线图`
- `🥇 1. 产品名称` → `🥇 产品名称`
- `## 快速总结 / 摘要` → `## 简洁总结 / 摘要`

#### 第11步：行动计划格式

将编号的行动计划转换为项目列表格式：

```
Before: 1. **This Week:** Install...
After: * **Get started:** Install...
```

#### 第12步：删除元信息免责声明

删除“最后更新”等元信息。

---

## 输出格式

### 对于文本模式
提供：
1. 人性化处理后的文本
2. 按类别分类的修改内容摘要

### 对于文章模式
提供：
1. 完整的转换后的Markdown文件
2. 按转换类型分类的修改总结
3. 需要用户审核的统计数据/链接/图片列表

---

## 文章模式质量检查表

**权威性保留：**
- [ ] 所有原始部分都保留（未删除任何内容）
- [ ] 未添加“我们的建议”或“我们认为”之类的表述
- [ ] 所有数据来源都标注了出处
- [ ] 所有引用都添加了链接（未删除）
- [ ] 所有表格的结构都保持完整

**AI写作模式的改进（24种模式的检测结果）：**
- [ ] 一级词汇已被替换
- [ ] 避免了连词的错误使用（如“作为……”替换为“是”、“拥有……”）
- [ ] 过度使用“重要性”词汇的情况已被消除
- [ ] 消除了负面的平行结构
- [ ] 填充语已被删除
- [ ] 宣传性语言被事实所替代
- [ ] 破折号的使用频率降低（每篇文章不超过1-2处）
- [ ] 同义词的重复使用得到了修正
- [ ] 表面化的分析被删除
- [ ] 机器人式的语气被删除
- [ ] 模糊的结论被具体内容所替代

**应用了发布相关的优化：**
- [ ] 所有引用都转换为带有权威来源的超链接
- [ ] 所有产品/品牌名称都链接到了官方网站
- [ ] 在引言后添加了特色图片占位符
- [ ] 需要核实的统计数据已标记
- [ ] H2标题中自然地添加了关键词
- [ ] 实施步骤保留了所有内容，并添加了文档链接
- [ ] 仅删除了真正无关的缺点
- [ ] FAQ按照WordPress的格式进行了优化
- [ ] 表格排名使用了表情符号（🥇🥈🥉）
- [ ] 标题前缀已被清理
- [ ] 行动计划使用了项目列表格式
- [ ] 删除了元信息免责声明

---

## 资源

- `references/transformation-examples.md` —— 每种转换前后的详细示例