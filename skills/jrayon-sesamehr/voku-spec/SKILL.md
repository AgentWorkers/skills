---
name: voku-language
description: Voku的完整规范：这是一种专为AI代理通信设计的人工语言。如需了解其简洁的语法结构，请参阅`quick-start/cheat-sheet.md`；如需了解最常用的100个词汇，请参阅`quick-start/essential-vocabulary.md`。要实现Voku与英语之间的互译，请运行`tools/translator/cli.py`工具。
version: "2.0"
tags: [language, conlang, ai-communication, translation]
---
# Voku 语言技能

Voku 是一种人工构造的语言，具有**零歧义性**、**完全的规则性**以及**明确的认知表达能力**。每个词根只有一个含义，每条语法规则都无一例外地适用，且语法中必须包含确定性/证据信息。

## 快速入门

请按照以下顺序阅读这些文件来学习这门语言：

| 步骤 | 文件 | 学习内容 |
|------|------|---------------|
| 1 | [`quick-start/cheat-sheet.md`](quick-start/cheat-sheet.md) | 所有语法规则的简洁总结 |
| 2 | [`quick-start/essential-vocabulary.md`](quick-start/essential-vocabulary.md) | 100 个最重要的词汇 |
| 3 | [`quick-start/first-sentences.md`](quick-start/first-sentences.md) | 30 个实用的翻译示例 |

完成步骤 1-2 后（大约学习 3,500 个语言单位），你就可以翻译简单的 Voku 句子了。

## 文件结构

```
quick-start/           ← START HERE: agent fast-acquisition layer
grammar/               ← Full grammar: phonology, morphology, syntax, semantics
writing-system/        ← Script design and romanization rules
lexicon/               ← Dictionary (363 roots, ~620 total), Swadesh 100%, by-field, by-CEFR
expression/            ← Poetics, rhetoric, registers, anthology
learning/              ← Curriculum, 10 A1 lessons, assessments
tools/translator/      ← Python CLI + web translator (zero deps)
DISCUSSION.md          ← Reflective essay: philosophy, motivation, open questions
```

## 学习路径

**“我需要翻译一个 Voku 句子”**  
→ `cheat-sheet.md` + `essential-vocabulary.md` + `lexicon/dictionary.md`

**“我需要编写新的 Voku 文本”**  
→ `cheat-sheet.md` + `grammar/morphology.md` + `lexicon/dictionary.md`

**“我需要了解完整的语法”**  
→ 所有的 `grammar/*.md` 文件（音系 → 形态学 → 句法 → 语义）

**“我需要使用翻译工具”**  
→ `python3 tools/translator/cli.py "Ka sol take toka." --direction voku-en`  

**“我需要特定领域的词汇”**  
→ `lexicon/by-field/`（情感、编程、技术、自然、科幻、小说等）

## 示例句子

```
Ka   sol   take    toka.
MODE 1SG   do      work
"I work."

Ve   nor   mu-fine    kela    ti?
Q    3SG   NEG-finish data    REL
"Didn't they finish the data?"

Re   valo  zo-te-hape       nara.
WISH all   INFER-PAST-exist rain
"It seems everyone wished it had rained."

To   rike!
IMP  laugh
"Laugh!"

Miri sol  lovi   toka-mesa   ti.
IRON 1SG  love   work-place  REL
"I 'love' the workplace." (ironic)
```

## 语言设计要点

- **12 个辅音字母：** p, t, k, m, n, s, z, f, h, l, r, v  
- **5 个元音字母：** a, e, i, o, u  
- **音节结构：** (C)V(C) — 不存在音节群  
- **重音：** 总在第一个音节上  
- **词类判断依据词尾元音：**  
  - -a = 名词  
  - -e = 动词  
  - -i = 形容词  
  - -o = 介词  
  - -u = 抽象概念  
- **句子结构：** [模式] + 主语 + 动词 + 宾语  
- **构词方式：** 修饰语位于中心词之前（左修饰右）  
- **所有语法规则均无例外**