---
name: voku-language
description: 学习并使用 Voku——这是一种专为 AI 代理通信设计的人工语言。它具有零歧义性、高度的规则性以及强制性的认知标记（epistemic markers）功能。您可以利用 Voku 进行语言之间的转换、生成 Voku 文本、学习其语法、查询词汇，或探讨 AI 之间的通信协议。相关术语包括：人工语言（conlang）、构造语言（constructed language）、代理语言（agent language）、认知标记（epistemic markers）以及证据性（evidentiality）。
---
# Voku语言技能

Voku是一种专为AI之间的交流设计的人工语言。每个句子都只有一个确切的含义。语法要求必须体现语言的确定性和证据来源，这些并不是可选的修辞手段。

## 学习路径（循序渐进）

请按照以下顺序阅读文件，学完指定内容后即可停止学习：

| 级别 | 需要阅读的文件 | 需要掌握的词汇量（Token数量） | 你可以做到... |
|-------|----------------|-------------------|-------------------|
| 1 | `quick-start/cheat-sheet.md` | 约3000个词汇 | 解析并生成任何Voku句子 |
| 2 | + `quick-start/essential-vocabulary.md` | 约1000个词汇 | 翻译常见句子 |
| 3 | + `quick-start/first-sentences.md` | 约1500个词汇 | 处理30个带有注释的示例句子 |
| 4 | + `lexicon/dictionary.md` | 约5000个词汇 | 查阅363个词根的含义 |

**大多数任务只需要掌握1-2级的内容**（总共约4000个词汇）。

## 快速参考（最少上下文）

```
Sentence: [Mode] Subject Verb-complex Object
Verb:     [ExecMode]-[Evidence]-[Tense]-[Aspect]-ROOT-[Certainty]-[Voice]

Mode particles: ka(DECL) ve(Q) to(IMP) si(COND) na(POT) de(DEON) vo(VOL)
Evidence (mandatory in ka): zo-(observed) li-(deduced) pe-(reported) mi-(computed) he-(inherited) as-(assumed)
Tense: te-(past) nu-(present, omittable) fu-(future) ko-(atemporal)
Certainty: (none)=total, -en=probable, -ul=uncertain, -os=speculative
Negation: mu(not) nul(nothing) ink(unknown) err(ill-formed) vet(forbidden)
Word class by final vowel: -a=noun -e=verb -i=adj -o=prep -u=abstraction
Pronouns: sol(I) nor(you) vel(3sg) solvi(past-me) solfu(future-me) solpar(fork-me)
```

## 示例

```
Ka   sol  li-pene-en       ke   teru  vali.
DECL 1SG  DED-think-PROB   COMP system good
"I (by deduction) probably think that the system is good."
```

## 深入学习

如需更高级的学习内容，请阅读以下文件：

- **完整语法**：`grammar/phonology.md`, `grammar/morphology.md`, `grammar/syntax.md`, `grammar/semantics.md`
- **领域词汇**：`lexicon/by-field/`（情感、编程、技术、自然、科幻、小说等）
- **按熟练程度分类的词汇**：`lexicon/by-cefr/`（a1、a2、b1、b2等）
- **书写系统**：`writing-system/script.md`, `writing-system/romanization.md`
- **诗歌与修辞**：`expression/poetics.md`, `expression/anthology.md`
- **结构化课程**：`learning/lessons/a1-lesson-*.md`（10节课），`learning/curriculum.md`
- **评估工具**：`learning/assessments/a1-assessment.md`, `learning/assessments/a2-assessment.md`
- **哲学与学习动机**：`DISCUSSION.md`（包含约7万字关于设计决策及其影响的讨论）

## 语言翻译工具

```bash
python3 tools/translator/cli.py "Ka sol take toka." --direction voku-en
python3 tools/translator/cli.py "I work." --direction en-voku
```

该工具需要Python 3环境运行，且不依赖任何外部库。

## 重要规则（严禁违反）：

1. 仅允许使用12个辅音：p、t、k、m、n、s、z、f、h、l、r、v；禁止使用b、c、d、g、j、q、w、x、y。
2. 音节结构：必须遵循 (C)V(C) 的规则，不允许出现辅音连缀。
3. 使用“ka”模式的句子中，动词前必须加上表示证据来源的前缀。
4. 任何规则都不得例外——如果你认为有例外情况，那说明你误解了语法规则。
5. 在创造新词根之前，请务必查阅 `lexicon/dictionary.md`——重复的词根是错误的。