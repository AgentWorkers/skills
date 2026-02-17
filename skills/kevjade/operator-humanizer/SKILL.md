---
name: humanizer-pro
description: 将人工智能生成的文本转化为真实的人类写作风格。该工具能够检测并去除24种典型的AI写作模式，替换500多个与AI相关的词汇，分析文本的统计特征（如文本的突发性、词汇的多样性），并通过故意的拼写错误、插入性的评论、偏离主题的叙述以及随机的想法来为文本增添“人性”。适用于以下场景：使文本更具人性化、检测文本中的AI痕迹、消除机械化的写作风格、让文本听起来不那么刻意雕琢，或者当需要模仿特定人物的写作风格时。适用于各种类型的文本，包括社交媒体帖子、文章、电子邮件、营销文案以及技术文档——任何需要表现出真实人类写作特征的文本。
---
# Humanizer Pro

该工具能够将人工智能生成的文本转化为自然、富有个性的文字，通过消除机械化的表达方式，让文本更具人文气息。

## 该工具的功能

**核心能力：**
- 检测24种人工智能写作模式（如过度强调重要性、使用宣传性语言、填充性短语等）
- 识别500多个属于不同严重程度的AI词汇
- 分析文本的统计特征（如写作节奏的突然变化、词汇重复率、句子结构的统一性）
- 去除聊天机器人特有的表达方式和谄媚的语气
- **新增功能：**通过插入自然的语境插话、故意的拼写错误、偏离主题的表述以及即兴的思考来增加文本的真实性

**基于以下研究：**维基百科关于“人工智能写作特征的描述”、Copyleaks的研究结果以及实际文本分析。

## 快速上手

### 基本的人性化处理

当需要将文本转化为更自然的语言时，请按照以下步骤操作：
1. **检测模式** → 查看`references/patterns.md`文件中的24种写作模式
2. **检查词汇** → 标记`references/vocabulary.md`文件中的1/2/3级AI词汇
3. **分析统计数据** → 计算文本的写作节奏、词汇重复率以及句子长度的多样性
4. **重写文本** → 删除人工智能特有的表达，增添真实的情感色彩
5. **验证效果** → 朗读文本，判断其是否听起来自然

### 增加文本的个性

可以使用`references/personality-injection.md`文件中的新功能来增加文本的个性：
- **插入自然的语境插话**：例如“(说实话，这部分内容每次都让我觉得有点荒谬)”  
- **故意的拼写错误**：在非正式文本中，一些小的拼写错误不会影响可信度  
- **偏离主题的表述**：如“说到这里，我突然想到……”  
- **即兴的思考**：让表达更加自然，不拘泥于预设的脚本

## 各功能的使用场景

### 必须检查的常见模式（核心模式）

- **1级词汇**：这些词汇是人工智能写作的明显标志，应完全避免使用（例如：delve、tapestry、vibrant、seamless等）
- **填充性短语**：将“in order to”替换为“to”，将“due to the fact that”替换为“because”  
- **聊天机器人特有的表达**：如“Great question!”、“I hope this helps!”、“Let me know if...”  
- **泛化的结论**：如“The future looks bright”、“Exciting times lie ahead”  

### 根据需要检查的词汇和表达

- **宣传性语言**：在描述地点、产品或服务时需特别注意  
- **过度强调重要性**：在讨论历史事件或里程碑时需警惕  
- **模糊的表述**：在没有来源支持的情况下使用这些表述时需谨慎  
- **过度使用破折号**：如果文本中破折号使用频繁，需要调整  

### 高级分析

对于需要全面优化文本或进行评分的情况，请参考以下内容：
1. 阅读`references/patterns.md`文件，了解24种写作模式的详细示例  
2. 查看`references/vocabulary.md`文件，了解完整的AI词汇库  
3. 阅读`references/statistical-signals.md`文件，学习如何计算文本的统计特征  
4. 阅读`references/personality-injection.md`文件，学习如何为文本增添人性化的元素  

## 核心原则

- **像人类一样写作，而不是像写新闻稿一样**：  
  - 自由使用“is”和“has”等动词；避免使用“serves as”这样的表达  
  - 每个观点都应配有具体的依据，避免使用过多的否定词  
  - 明确引用来源，或直接陈述观点  
  - 以具体的内容结尾，而不是使用模糊的乐观表述  

### 增加真实的个性

- **表达真实的情感**：对事实做出反应，而不仅仅是简单地陈述  
- **变化句子节奏**：使用短句和稍长的句子，使表达更加自然  
- **承认复杂性**：如“我真不知道该如何看待这个问题”  
- **允许文本有些不完美**：完美的结构反而会显得机械  
- **使用缩写**：如“don't”、“won't”、“it's”等  
- **适当使用句子片段**：在合适的情况下使用  

### 自动删除冗余表达

- 将“in order to”替换为“to”  
- 将“due to the fact that”替换为“because”  
- 将“at this point in time”替换为“now”  
- 将“It is important to note that”替换为“只需说明即可”  
- 将“in the event that”替换为“if”  

## 24种写作模式（快速参考）

详细信息及示例请参见`references/patterns.md`文件。

| 编号 | 模式 | 需要注意的点 |
| --- | --- | --- |
| 1 | 过度强调重要性 | 如“marking a pivotal moment in the evolution of...”（过度强调重要性） |
| 2 | 不恰当地引用媒体名称 | 仅列出媒体名称而未给出具体内容 |
| 3 | 表面化的分析 | 如“...showcasing... reflecting... highlighting...”（分析内容过于肤浅） |
| 4 | 宣传性语言 | 如“nestled”, “breathtaking”, “stunning”, “renowned”（使用夸张的形容词） |
| 5 | 模糊的表述 | 如“Experts believe”, “Studies show”, “Industry reports”（缺乏具体依据） |
| 6 | 机械化的挑战描述 | 如“Despite challenges... continues to thrive”（缺乏变化） |
| 7 | 过长的AI词汇（500多个词） | 如“delve”, “tapestry”, “landscape”, “showcase”（重复使用词汇） |
| 8 | 避免使用连词“is” | 如“serves as”, “boasts”代替“is”, “has” |
| 9 | 使用负面的并列结构 | 如“It's not just X, it's Y”（结构重复） |
| 10 | 机械化的表达方式 | 如“innovation, inspiration, and insights”（缺乏变化） |
| 11 | 过度使用同义词 | 如“protagonist... main character... central figure...”（重复使用相同的词汇） |
| 12 | 不准确的范围描述 | 如“from the Big Bang to dark matter”（范围描述不准确） |
| 13 | 过度使用破折号 | 文本中破折号使用过多 |
| 14 | 过度使用粗体字 | 机械化的强调方式 |
| 15 | 内联标题列表 | 如“- Topic: Topic is discussed here”（格式过于正式） |
| 16 | 所有主词都大写 | 标题格式过于生硬 |
| 17 | 过度使用表情符号 | 如🚀💡✅在专业文本中使用表情符号 |
| 18 | 使用曲线引号 | 如“smart quotes”代替“straight quotes” |
| 19 | 聊天机器人特有的表达 | 如“I hope this helps!”, “Let me know if...” |
| 20 | 使用免责声明 | 如“As of my last training...”, “While details are limited...” |
| 21 | 谄媚的语气 | 如“Great question!”, “You're absolutely right!” |
| 22 | 填充性短语 | 如“in order to”, “Due to the fact that” |
| 23 | 过度的否定表达 | 如“could potentially possibly”, “might arguably” |
| 24 | 泛化的结论 | 如“The future looks bright”, “Exciting times lie ahead” |

## 词汇分类

### 1级词汇（绝对避免使用）
delve, tapestry, vibrant, crucial, comprehensive, meticulous, embark, robust, seamless, groundbreaking, leverage, synergy, transformative, paramount, multifaceted, myriad, cornerstone, reimagine, empower, catalyst, invaluable, bustling, nestled, realm

### 2级词汇（需谨慎使用）
furthermore, moreover, paradigm, holistic, utilize, facilitate, nuanced, illuminate, encompasses, catalyze, proactive, ubiquitous, quintessential

### 3级词汇（使用需结合上下文）
landscape (abstract), journey (metaphorical), ecosystem, framework, roadmap, touchpoint, pain point, streamline, optimize, scalable

**完整的500多个词汇库请参见`references/vocabulary.md`文件。**

## 统计分析指标

在进行全面分析时，请参考以下指标：
| 指标 | 人类写作 | 人工智能写作 | 原因 |
|--------|-------|----|----|
| 写作节奏的突然变化 | 0.5-1.0 | 0.1-0.3 | 人类写作通常有节奏上的变化；人工智能写作则较为规律 |
| 词汇重复率 | 0.5-0.7 | 0.3-0.5 | 人工智能写作会重复使用词汇 |
| 句子长度的多样性 | 高 | 低 | 人工智能写作中的句子长度较为固定 |

**具体的计算公式和实现方法请参见`references/statistical-signals.md`文件。**

## 增加文本个性的方法（新增功能）

当需要为文本增添人性化的元素时，请参考以下方法：
### 1. 插入自然的语境插话
在文本中插入真实的反应：
- “(说实话，这部分内容每次都让我觉得有点荒谬)”  
- “(这其实有点不合理)”  
- “(我仍然不太明白为什么……)”  

**规则：**仅用于表达真实的情感或观点，每500个词最多使用1-3次。  

### 2. 故意的拼写错误
在非正式文本中，允许出现一些不影响可信度的拼写错误：
- 可接受的错误：如“teh” → “the”，“recieve” → “receive”，“definately” → “definitely”  
**注意：**在正式或专业语境中应避免使用这些错误。  

### 3. 偏离主题的表述
让表达更加自然：
- “说到这里，我突然想到……”  
- “好吧，稍微偏离一下主题……”  
- “等等，这个和之前提到的内容有关联……”  

**规则：**在较长的文本中（1000个词以上），每段最多使用1-2次。  

### 4. 即兴的思考
加入真实的情感或即兴的思考：
- “说实话，我原本以为这不会奏效，但……”  
- “我一直都在思考这个问题……”  
- “这个情况让我感到不安……”  
**规则：**仅在表达真实的情感或强烈反应时使用。  

**详细的使用方法请参见`references/personality-injection.md`文件。**

## 使用流程

1. **仔细阅读输入文本**  
2. **识别所有不符合人类写作模式的表达**  
3. **标记需要处理的词汇**（1级词汇直接删除，2级词汇减少使用频率，3级词汇需根据上下文调整）  
4. **分析文本的统计特征**（如需进行全面分析）  
5. **重写有问题的部分**  
6. **增添个性化元素**（根据需求或文本的缺乏人情味的情况）  
7. **验证文本的自然度**（朗读文本，检查表达是否自然）  
8. **呈现优化后的版本**，并附上简要的修改说明  

## 示例文本转换

### 优化前（人工智能风格）：
Great question! Here is an overview of sustainable energy. Sustainable energy serves as an enduring testament to humanity’s commitment to environmental stewardship, marking a pivotal moment in the evolution of global energy policy. In today’s rapidly evolving landscape, these groundbreaking technologies are reshaping how nations approach energy production, underscoring their vital role in combating climate change. The future looks bright. I hope this helps!

### 优化后（更自然的语言）：
根据IRENA的数据，2010年至2023年间，太阳能电池板的成本下降了90%。这一事实解释了为什么可持续能源的采用率会迅速上升——它不再只是意识形态上的选择，而成为了一种经济上的必要措施。  
如今，德国46%的电力来自可再生能源。虽然转型正在进行中，但过程并不顺利，且储能问题仍未得到解决。  

### 做出的修改：
- 删除了“Great question!”和“I hope this helps!”（聊天机器人特有的表达）  
- 删除了“serves as an enduring testament”（过度强调重要性）  
- 删除了“marking a pivotal moment”（重复使用的AI词汇）  
- 删除了“rapidly evolving landscape”（机械化的表达）  
- 删除了“groundbreaking”, “underscoring”, “vital”（过度使用的AI词汇）  
- 删除了“The future looks bright”（泛化的结论）  
- 添加了具体的数据和来源  
- 加入了个人的观察（通过语境插话）  
- 表达了对复杂性的承认  
- 句子长度更加自然  

## 使用CLI工具

`scripts/humanize.js`工具提供了命令行接口：

```bash
# Score text (0-100, higher = more AI-like)
node scripts/humanize.js score "Your text here"

# Full analysis report
node scripts/humanize.js analyze -f draft.md

# Humanization suggestions
node scripts/humanize.js suggest article.txt

# Auto-fix common patterns
node scripts/humanize.js fix --autofix -f article.txt
```

## 长期应用设置

若希望将此工具的规则设置为默认的写作风格（而不仅仅是根据需求进行优化），可以执行以下操作：
1. 完全禁止在所有文本中使用1级词汇  
2. 自动删除填充性短语  
3. 避免使用谄媚的语气、聊天机器人特有的表达和泛化的结论  
4. 使句子长度多样化，表达真实的情感，使用具体的信息  
5. 如果你不会在日常对话中说出这些话，就不要写在文本中  

这些规则可以添加到`SOUL.md`文件或代理的个性化配置文件中，以实现长期的应用。  

## 优化文本的建议：

- **从1级词汇开始优化**：这些词汇最容易识别，也是人工智能写作最明显的特征  
- **注意破折号的使用**：快速检查文本中破折号的使用频率  
- **阅读最后一段**：泛化的结论较为常见  
- **注意语调的自然度**：朗读文本，判断其是否听起来像机器人说话  
- **避免过度修饰**：适度的不完美反而更显真实  
- **根据上下文调整风格**：正式文档和社交帖子需要不同的处理方式  
- **保持信息传递的准确性**：在去除不良表达的同时，确保核心信息的传递  

## 常见问题及解决方法

- **修改后文本仍然听起来像人工智能写的？**  
  → 你可能只去掉了人工智能的痕迹，但还没有加入真实的情感。请参考`references/personality-injection.md`文件。  
- **个性化处理后文本显得过于随意？**  
  → 个性化处理应结合上下文使用；在正式文本中，减少语境插话和拼写错误的数量。  
- **文本变得过于完美？**  
  → 通过调整句子长度、加入偏离主题的表述或表达不确定性来增加自然感。  
- **不确定某个词是否属于AI词汇？**  
  → 查看`references/vocabulary.md`文件；如果有疑问，可以问自己“如果我在日常生活中会这么说吗？”