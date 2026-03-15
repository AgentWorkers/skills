---
name: im-framework
description: 参考、解释并应用 Forrest Landry 提出的“内在形而上学（Immanent Metaphysics, IM）”框架。该框架基于一个包含 767 个实体的结构化本体（包括概念、公理、定理、术语和格言），这些实体均直接链接到 mflb.com 网站上的原始文本。在需要解释 IM 概念、将该框架应用于具体情境、追踪推导过程、查找原始参考资料，或在白皮书（whitebook）中关联不同思想时，均可使用该框架。相关关键词包括：“内在形而上学”（immanent metaphysics）、“IM 框架”（IM framework）、模态问题（modality questions）、公理引用（axiom references）、信息与通信技术（ICT）、对称性/连续性伦理（symmetry/continuity ethics）、有效选择（effective choice）、正确行动的路径（path of right action），以及任何要求在该框架基础上论证观点的请求。
---
# 内在形而上学框架（Immanent Metaphysics Framework）

该框架用于评估人们如何运用内在形而上学的工具（IM tools），并提供基于事实的、有来源依据的回答。所有内容均直接引用Forrest Landry在mflb.com上的白皮书。

## 所有参考文件（Bundled Reference Files）

所有参考文件均位于`references/`目录下：

| 文件名 | 文件内容 |
|------|----------|
| `graph.jsonl` | 包含767个实体：134个概念（Concepts）、3个公理（Axioms）、11个定理（Theorems）和147条格言（Aphorisms），每个实体都包含`name`（名称）、`definition`（定义）、`source_section`（来源章节）和`location`（URL）。实体之间的关系包括：implies（蕴含）、paired_with（与...配对）、contrasts_with（与...对比）、depends_on（依赖于...）、has_modality（具有某种模态）、illuminates（阐明...）和defined_in（在...中定义）。 |
| `whitebook-map.jsonl` | 包含73个条目，用于映射白皮书的章节结构（chapters, sections, URLs）。入口页面：https://mflb.com/8192 |
| `schema.yaml` | 该本体（ontology）的类型定义和关系类型（relation types）。 |

完整源代码文件（未打包，可在mflb.com获取）：
- 《内在形而上学》（The Immanent Metaphysics）：https://mflb.com/8192 |
- 《有效选择的格言》（Aphorisms of Effective Choice）：https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch5.htm |

## 使用方法

### 1. 在本体中搜索（Search the Ontology）

```bash
# Find a concept by name
grep -i '"name": "symmetry"' references/graph.jsonl

# Find all entities mentioning a term
grep -i 'continuity' references/graph.jsonl | head -10

# Find entities with source URLs
python3 -c "
import json
for line in open('references/graph.jsonl'):
    d = json.loads(line)
    if 'entity' in d:
        props = d['entity'].get('properties',{})
        loc = props.get('location','')
        name = props.get('name', props.get('word', props.get('text','')))
        if 'SEARCH_TERM' in name.lower() or 'SEARCH_TERM' in props.get('definition','').lower():
            print(f'{d[\"entity\"][\"type\"]}: {name}')
            if loc: print(f'  URL: {loc}')
            print(f'  Def: {props.get(\"definition\",\"\")[:200]}')
            print()
"

# Find relations for a specific entity
grep '"ENTITY_ID"' references/graph.jsonl | grep relation
```

### 2. 链接到来源（Link to Source）

所有具有`location`属性的实体都对应着mflb.com上的相应白皮书章节。引用时务必包含这些链接。

**关键章节链接：**
| 主题 | 链接 |
|-------|-----|
| 模态（Modalities） | [第1章](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch1.htm#1_modalities) |
| 公理（Axioms） | [第1章](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch1.htm#1_axioms) |
| ICT（Incommensuration Theorem） | [第3章](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch3.htm#1_ict) |
| 对称性/连续性（Symmetry / Continuity） | [第3章](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch3.htm#1_symmetry) |
| 伦理学（Ethics） | [第6章](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch6.htm) |
| 正确行动的路径（Path of Right Action） | [第6章](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch6.htm#2_path) |
| 基本动机（Basal Motivations） | [第6章](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch6.htm#2_basal) |
| 美学（Aesthetics） | [第7章](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch7.htm) |
| 心灵（Mind） | [第8章](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch8.htm) |
| 进化（Evolution） | [第9章](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch9.htm) |

### 3. 评估与应用（Assess and Apply）

1. **确定所涉及的模态、公理或定理。** 在本体中进行搜索。
2. **检查是否存在模态混淆。** 例如：将“全知”（omniscient）的概念错误地视为“内在的”（immanent）？或将“超越的”（transcendent）的概念视为“全知的”？公理III（Theorem III）可以用于诊断这类问题。
3. **追踪推导过程。** 利用`implies`、`depends_on`、`has_modality`等关系来理解概念之间的逻辑联系。
4. **提供来源链接。** 必须注明mflb.com上的具体页面地址。
5. **结合格言理解。** 147条格言有助于理解这些概念的实际应用。

## 快速参考（Quick Reference）

### 三种模态（The Three Modalities）

- **内在的（Immanent）**：具有关系性、互动性、参与性，属于第一人称的体验。是任何连续性的核心。
- **全知的（Omniscient）**：具有结构性、外在性、固定性，属于第三人称的观察视角，能够同时看到整体。
- **超越的（Transcendent）**：代表可能性、先验条件，没有固定的位置，适用于所有情况。

### 三个公理（The Three Axioms）

- **公理I**：内在的比全知的和/或超越的更为根本；全知的和超越的是相互关联的。
- **公理II**：某一类别的超越的概念先于某一类别的内在概念；某一类别的内在概念先于某一类别的超越概念；某一类别的全知概念先于某一类别的超越概念。
- **公理III**：内在的、全知的和超越的概念是相互独立、不可分割且不可互换的。

### ICT（不兼容性定理，Incommensuration Theorem）

基于六个比较属性（相同性、差异性、内容、背景、主体、对象）：
- **连续性（Continuity）**：当背景相同时，内容也相同。
- **对称性（Symmetry）**：当背景不同时，内容也相同。
- **不对称性（Asymmetry）**：当背景不同时，内容也不同。
- **不连续性（Discontinuity）**：当背景相同时，内容却不同。
**结论：** 对称性和连续性不能同时成立。有效的逻辑组合为：（连续性 + 不对称性）或（对称性 + 不连续性）。

**跨领域应用（Cross-domain Applications）**：
- 贝尔定理（Bell’s Theorem，物理学）：描述了信息传递的局限性。
- 戈德尔不完备性定理（Godel’s Incompleteness，逻辑学）：指某些数学系统无法被完全证明。
- 无决定论的因果关系（Causality without Determinism，形而上学）：说明某些因果关系无法被严格确定。

### 伦理学（Ethics）

- **对称性伦理学（Symmetry Ethics）**：当内在本质不变时，表达方式应保持不变，不受外部环境的影响。
- **连续性伦理学（Continuity Ethics）**：当内在本质不变时，无论与什么或谁互动，互动的方式也应保持不变。

这些伦理原则都是从ICT的逻辑关系中推导出来的。它们不可能同时完美地实现。

### 正确行动的路径（Path of Right Action）

在任何存在层次上，总是可以选择对所有相关方都有利的结果。双赢的选择是相互支持的，并构成一条连续的路径。双赢选择难以实现的程度，反映了偏离正确路径的程度。

## 本体中的实体类型（Entity Types in the Ontology）

| 实体类型 | 数量 | 包含内容 |
|------|-------|----------|
| 概念（Concept） | 134 | 带有定义、模态属性和来源链接的命名概念。 |
| 公理（Axiom） | 3 | 基础性的公理，包含陈述和推论。 |
| 定理（Theorem） | 11 | 包括ICT、对称性伦理学、连续性伦理学等相关概念。 |
| 格言（Aphorism） | 147 | 来自《有效选择》（Effective Choice），包含主题和相关解释链接。 |
| 推论（Implication） | 4 | 具有跨领域应用（物理学、逻辑学、伦理学等）。 |

## 引用说明（Attribution）

所有内容均归功于Forrest Landry的《内在形而上学》。引用时请区分以下几种情况：
- **直接引用**：直接引用原文并附上来源链接。
- **近似表述**：对原文进行总结并附上来源链接。
- **个人解读**：如果是自己的解读或应用，请明确标注。

请勿凭空创造新的观点，也不要对未在原始材料中明确支持的论点表示赞同。