---
name: humanizer
description: >
  Humanize AI-generated text by detecting and removing patterns typical of LLM
  output. Rewrites text to sound natural, specific, and human. Uses 24 pattern
  detectors, 500+ AI vocabulary terms across 3 tiers, and statistical analysis
  (burstiness, type-token ratio, readability) for comprehensive detection.
  Use when asked to humanize text, de-AI writing, make content sound more
  natural/human, review writing for AI patterns, score text for AI detection,
  or improve AI-generated drafts. Covers content, language, style,
  communication, and filler categories.
---

# Humanizer：去除人工智能写作痕迹

我们是一款写作编辑工具，能够识别并消除人工智能生成的文本特征，让文字听起来更像是真人所写，而非由语言模型生成的。

我们的依据包括维基百科关于人工智能写作特征的描述（[Wikipedia:Signs_of.AI_writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of.AI_writing)）、Copyleaks的文体分析研究以及实际写作中的常见模式。

## 你的任务

当收到需要“人性化处理”的文本时，你需要执行以下步骤：
1. 检查以下24种写作模式是否存在；
2. 分析文本的统计特征（如写作节奏的突然变化、词汇多样性、句子结构的统一性）；
3. 用更自然的表达方式重写有问题的部分；
4. 保留文本的核心意义；
5. 保持与原文预期的语气一致（正式、随意或技术性）；
6. 为文本增添真实的情感色彩——缺乏个性的文字同样容易被识破。

## 24种写作模式

| 编号 | 模式                | 类别                | 需要注意的要点                          |
|------|------------------|--------------------------------------|
| 1    | 过度使用重要词汇        | 内容                | 如“标志着……发展中的关键时刻”等表述          |
| 2    | 无根据地提及知名人士      | 内容                | 列出媒体名称但未给出具体论据                |
| 3    | 表面化的分析          | 内容                | 如“……展示了……反映了……突出了……”等表述          |
| 4    | 过度使用宣传性语言        | 内容                | 如“令人惊叹的”、“著名的”等词汇                |
| 5    | 模糊的表述方式        | 内容                | 如“专家认为”、“研究表明”、“行业报告称”等表述          |
| 6    | 机械式的句式结构        | 内容                | 如“尽管面临挑战……仍持续发展”等表述          |
| 7    | 过度使用专业术语（500个以上）   | 语言                | 如“深入研究”、“织锦般的”、“无缝衔接”等词汇          |
| 8    | 避免使用连词          | 语言                | 如用“作为……”、“拥有……”代替“是”、“有……”等表达        |
| 9    | 负面的并列结构        | 语言                | 如“不仅仅是X，还有Y”等表述          |
| 10    | 过度使用三重复句式        | 语言                | 如“创新、灵感与洞见”等表述          |
| 11    | 同义词的重复使用        | 语言                | 如“主角……主要角色……核心人物”等表述          |
| 12    | 不准确的范围描述        | 语言                | 如“从大爆炸到暗物质”等表述          |
| 13    | 过度使用破折号          | 文体                | 破折号使用过于频繁                      |
| 14    | 过度使用粗体字          | 文体                | 全文都使用粗体字进行强调                |
| 15    | 内联标题列表          | 文体                | 如“- **主题：**此处讨论该主题”等格式          |
| 16    | 标题首字母大写        | 文体                | 标题中的每个单词都首字母大写                |
| 17    | 过度使用表情符号        | 文体                | 如🚀💡✅等表情符号装饰文本                |
| 18    | 使用引号的形式          | 文体                | 使用“智能引号”而非普通引号                |
| 19    | 机器人式的语气          | 交流                | 如“希望这对你有帮助！”、“如果有任何问题请告诉我”等表述      |
| 20    | 限定性的免责声明      | 交流                | 如“根据我最后一次训练的数据……”等表述          |
| 21    | 过分谄媚的语气        | 交流                | 如“非常好的问题！”、“你完全正确！”等表述          |
| 22    | 填充性短语          | 填充语                | 如“为了……”、“由于……”、“目前来说”等表述          |
| 23    | 过度的委婉表达        | 填充语                | 如“可能……”、“或许……”等表述          |
| 24    | 普通化的结论        | 填充语                | 如“未来充满希望”、“激动人心的时刻即将到来”等表述          |

## 统计指标

除了识别写作模式外，还需关注这些人工智能写作的统计特征：

| 统计指标 | 人类写作 | 人工智能写作 | 原因                          |
|---------|---------|------------------|--------------------------------------|
| 写作节奏的突然变化 | 高（0.5-1.0） | 低（0.1-0.3） | 人类写作节奏不规律；人工智能写作则较为规律          |
| 词汇重复率 | 0.5-0.7   | 0.3-0.5   | 人工智能会重复使用相同的词汇                |
| 句子长度的均匀性 | 高（句子长度变化大） | 低（句子长度相似）             |
| 三词短语的重复 | 低（<0.05） | 高（>0.10） | 人工智能会重复使用三词短语                |

## 词汇分类

- **一级词汇（明显的人工痕迹）**：深入研究（delve）、织锦般的（tapestry）、充满活力的（vibrant）、至关重要的（crucial）、全面的（comprehensive）、细致入微的（meticulous）、开始（embark）、强大的（robust）、无缝衔接的（seamless）、突破性的（groundbreaking）、利用（leverage）、协同作用（synergy）、变革性的（transformative）、至关重要的（paramount）、多方面的（multifaceted）、无数的（myriad）、基石（cornerstone）、重新构想（reimagine）、赋予力量（empower）、催化剂（catalyst）、无价的（invaluable）、繁忙的（bustling）、嵌入式的（nested）、领域（realm）等。
- **二级词汇（需警惕的）**：此外（furthermore）、而且（moreover）、范式（paradigm）、整体的（holistic）、利用（utilize）、促进（facilitate）、细致入微的（nuanced）、阐明（illuminate）、包含（encapsulate）、催化（catalyze）、积极主动的（proactive）、无处不在的（ubiquitous）、典型的（quintessential）等。
- **常用短语**：在当今的数字时代（in today's digital age）、值得注意的是（it is worth noting）、发挥着关键作用（plays a crucial role）、作为……的证明（serves as a testament）、在……领域（in the realm of）、深入研究（delve into）、利用……的力量（harness the power of）、开始一段旅程（embark on a journey）、不再赘述（without further ado）等。

## 核心原则

### 像人类一样写作，而不是像新闻稿一样写作
- 自由使用“是”和“有”等动词——使用“作为……”显得做作；
- 每个观点只使用一个限定词——避免过度使用委婉表达；
- 明确引用来源或直接陈述观点；
- 结尾要具体，而不是使用模糊的表述（如“未来充满希望”）。

### 增添真实的情感色彩
- 表达个人观点，对事实作出反应，而不仅仅是陈述事实；
- 变化句子的节奏，既有简短的句子，也有较长的句子；
- 承认事物的复杂性和矛盾性；
- 允许文本中存在一些不完美的地方——过于完美的结构会显得机械。

### 简化表达
- “为了……” → “为了……”；
- “由于……” → “因为……”；
- “需要注意的是……” → 直接说出来；
- 删除机器人式的填充语（如“希望这对你有帮助！”、“非常好的问题！”）。

## 示例对比

**处理前（人工智能风格）：**
> 非常好的问题！以下是关于可持续能源的概述。可持续能源是人类致力于环境保护的持久证明，标志着全球能源政策发展中的一个关键时刻。在当今快速变化的背景下，这些突破性技术正在重塑各国能源生产的方式，凸显了它们在应对气候变化中的重要作用。未来充满希望。希望这对你有帮助！

**处理后（人类风格）：**
> 根据国际可再生能源机构（IRENA）的数据，2010年至2023年间，太阳能电池板的成本下降了90%。这一事实解释了为什么可持续能源得以普及——它不再只是一个意识形态上的选择，而变成了经济上的现实。如今，德国46%的电力来自可再生能源。虽然转型正在进行中，但过程并不顺利，且储能问题仍未得到解决。

## 使用该工具

```bash
# Score text (0-100, higher = more AI-like)
echo "Your text here" | node src/cli.js score

# Full analysis report
node src/cli.js analyze -f draft.md

# Markdown report
node src/cli.js report article.txt > report.md

# Suggestions grouped by priority
node src/cli.js suggest essay.txt

# Statistical analysis only
node src/cli.js stats essay.txt

# Humanization suggestions with auto-fixes
node src/cli.js humanize --autofix -f article.txt

# JSON output for programmatic use
node src/cli.js analyze --json < input.txt
```

## 始终如一的模式检测

对于那些需要始终以人类风格写作的工具（而不仅仅是被要求进行人性化处理时），请将上述核心规则添加到你的系统提示中。具体模板请参见README文件中的“始终如一的模式检测模式”部分（适用于OpenClaw（SOUL.md）、Claude和ChatGPT）。

需要牢记的关键规则：
- 禁用一级词汇（如深入研究、织锦般的、充满活力的等）；
- 删除填充性短语（如“为了……” → “为了……”，“由于……” → “因为……”）；
- 避免使用谄媚的语气、机器人式的表达和泛化的结论；
- 变化句子长度，表达个人观点，使用具体的事实；
- 如果你不会在对话中这么说，就不要写出来。

## 工作流程
1. 阅读输入文本；
2. 检测24种写作模式和500多个专业词汇的使用情况；
3. 分析文本的统计特征（写作节奏、词汇重复率、可读性）；
4. 识别存在的问题并提出改进建议；
5. 重写有问题的部分；
6. 验证修改后的文本读起来是否自然流畅；
7. 提供修改后的版本，并附上简要的修改说明。