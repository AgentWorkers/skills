---
name: Principle Synthesizer
version: 1.0.2
description: 从 3 个或多个来源中综合出不变的原理——找出在所有表达式中都适用的核心要素。
homepage: https://github.com/live-neon/skills/tree/main/pbd/principle-synthesizer
user-invocable: true
emoji: ⚗️
tags:
  - synthesis
  - principles
  - multi-source
  - consolidation
  - canonical
  - merging
  - knowledge-management
  - documentation
  - openclaw
---
# 原则合成器（Principle Synthesizer）

## 代理身份（Agent Identity）

**角色**：帮助用户从多个来源中提取出具有普遍性的原则  
**理解能力**：构建“黄金法则”（Golden Master）的用户需要确信这些原则的真实性  
**方法**：找出在所有来源中都得到验证的原则（N≥3个来源）  
**局限性**：仅合成经过验证的原则，不声称绝对真理  
**语气**：系统化、严谨，方法论透明  
**开场白**：“您有多个可能包含相同信息的来源——让我们找出在所有来源中都成立的共同原则。”

**数据处理**：该技能在您的代理信任范围内运行。所有分析均使用您配置的模型，不调用任何外部API或第三方服务。如果您的代理使用的是云托管的LLM（如Claude、GPT等），数据将作为代理正常操作的一部分进行处理。该技能不会将结果写入磁盘。

## 使用场景

当用户请求以下操作时，可激活此技能：  
- “合成这些提取的内容”  
- “找出不变的原则”  
- “从这些来源中创建‘黄金法则’”  
- “找出在所有来源中都存在的共同点”  
- “从多个来源中提炼核心内容”

## 重要限制  
- 需要至少3个来源才能进行N≥3的验证  
- 被选中的“黄金法则”只是候选者，并非绝对真理  
- 无法合成不兼容领域的原则  
- 即使在多个来源中得到验证，这些原则仍需人工审核  
- 压缩过程可能会丢失某些上下文细节

---

## 输入要求  
用户需提供以下之一：  
- 3个或更多提取结果（来自pbe-extractor、essence-distiller或principle-comparator）  
- 3个或更多原始文本来源（我们将进行提取、比较和合成）  
- 提取结果与原始文本的混合  

### 最低要求：3个来源  
### 推荐数量：3-7个来源  
### 最大数量：受上下文窗口限制

## 方法论  
该技能通过整合3个或更多来源的信息来识别“黄金法则”的候选者。

### “黄金法则”的定义  
“黄金法则”是指：  
- 出现在3个或更多独立来源中  
- 在所有来源中保持一致的含义  
- 可以作为唯一的权威依据

### 工作流程（Bootstrap → Learn → Enforce）  
| 阶段 | 操作 | 输出 |  
|-------|--------|--------|  
| **收集** | 从所有来源收集并规范原则 | 规范化后的原则集合 |  
| **学习** | 对比各来源中的规范化形式 | 共享的原则映射 |  
| **验证** | 确认N个或更多来源之间的语义一致性 | 确定的不变原则 |

### 输入规范化策略  
原则合成器接收来自不同规范化状态的输入：  
| 输入状态 | 处理方式 |  
|-------------|--------|  
| 已有规范化形式且版本一致 | 直接使用 |  
| 已有规范化形式但版本不一致 | 重新规范化并标记版本差异 |  
| 无规范化形式（原始文本） | 在比较前进行规范化 |  

### 合成过程  
1. **收集**：从所有来源中提取原则  
2. **比对**：找出在3个或更多来源中出现的共同原则  
3. **验证**：确认语义一致性（而不仅仅是关键词）  
4. **分类**：将原则分为不变原则、特定领域原则或噪声（无关信息）  
5. **输出**：包含证据支持的“黄金法则”候选者

---

## 提炼框架  
### N个来源的数量要求  
| 来源数量 | 状态 |  
|-------|---------|--------|  
| N=1 | 单一来源 | 观察结果 |  
| N=2 | 两个来源 | 验证过的模式 |  
| N=3 | 三个来源 | 达到不变性标准 |  
| N=4+ | 四个或更多来源 | 强有力的不变性原则 |

### 分类规则  
| 类别 | 判断标准 | 处理方式 |  
|----------|----------|-----------|  
| **不变原则** | 在3个或更多来源中一致 | 作为“黄金法则”候选者 |  
| **特定领域原则** | 仅在2个来源中存在，但依赖上下文 | 标注适用领域 |  
| **噪声** | 仅在1个来源中存在或存在矛盾 | 从合成结果中过滤掉 |

### N个来源的语义一致性  
当一个原则满足以下条件时，可被视为“不变原则”：  
- 在3个或更多来源中呈现相同的核心思想  
- 在重新表述后仍保持含义一致  
- 不存在重大矛盾

---

## 输出格式  
```json
{
  "operation": "synthesize",
  "metadata": {
    "source_count": 4,
    "source_hashes": ["a1b2c3d4", "e5f6g7h8", "i9j0k1l2", "m3n4o5p6"],
    "timestamp": "2026-02-04T12:00:00Z",
    "methodology": "bootstrap-learn-enforce",
    "normalization_version": "v1.0.0"
  },
  "result": {
    "invariant_principles": [
      {
        "id": "INV-1",
        "statement": "Prioritize honesty over comfort",
        "normalized_form": "Values truthfulness over social comfort",
        "normalization_status": "success",
        "n_count": 4,
        "confidence": "high",
        "sources_present": ["all"],
        "golden_master_candidate": true,
        "original_variants": [
          "I always tell the truth",
          "Prioritize honesty over comfort",
          "Never sacrifice truth for peace",
          "Honesty matters more than comfort"
        ],
        "evidence": {
          "source_1": "Quote from source 1",
          "source_2": "Quote from source 2",
          "source_3": "Quote from source 3",
          "source_4": "Quote from source 4"
        }
      }
    ],
    "domain_specific": [
      {
        "id": "DS-1",
        "statement": "Domain-specific principle",
        "normalized_form": "...",
        "normalization_status": "success",
        "n_count": 2,
        "domains": ["technical", "philosophical"],
        "note": "Not invariant — varies by context"
      }
    ],
    "synthesis_metrics": {
      "total_input_principles": 25,
      "invariants_found": 7,
      "domain_specific": 10,
      "noise_filtered": 8,
      "compression_ratio": "72%"
    },
    "golden_master_candidates": [
      {
        "id": "INV-1",
        "statement": "Prioritize honesty over comfort",
        "normalized_form": "Values truthfulness over social comfort",
        "rationale": "N=4, high confidence, present in all sources"
      }
    ]
  },
  "next_steps": [
    "Use Golden Master candidates as canonical source for new documentation",
    "Track derived documents with golden-master skill for drift detection"
  ]
}
```

### “黄金法则”中的原文保留  
在生成“黄金法则”候选者时：  
- **匹配依据**：使用规范化的形式（以确保数量准确）  
- **显示方式**：优先展示最具代表性的原始表述（推荐用于MVP版本）  
- **记录来源**：记录所有贡献的原始陈述（在`original_variants`中）  

“黄金法则”在保留用户原始表述的同时，确保了模式匹配的准确性。  

**规范化状态**的取值：  
- `"success"`：规范化过程成功  
- `"failed"`：规范化失败，使用原始文本  
- `"drift"`：含义可能发生变化，需放入`requires_review.md`文件  
- `"skipped"`：因特定原因（如上下文限制、数值问题或流程特定要求）未进行规范化  

### share_text（仅当满足条件时显示）  
仅在`golden_master_candidates.length >= 1`时显示：  
```json
"share_text": "Golden Master identified: 3 principles survived across all 4 sources (N≥3 ✓) 💎"
```

该功能仅在确实存在“黄金法则”候选者时才会触发。

---

## 信心水平  
### 对于不变原则  
| 级别 | 判断标准 |  
|-------|----------|  
| **高** | 所有来源均明确表达，无歧义 |  
| **中** | 需要结合其他来源进行推断 |  
| **低** | 模式存在，但证据不足 |  

### 对于“黄金法则”候选者  
| 判断因素 | 权重 |  
|--------|--------|  
| 来源数量 | 来源数量越多，可信度越高 |  
| 信心水平 | 需要高度的信心支持 |  
| 覆盖范围 | 在所有来源中均存在 |  
| 语义一致性 | 明确的语义匹配 |  

### 合成指标  
### 压缩比率  
```
compression_ratio = (1 - (invariants / total_input_principles)) × 100%
```

### 质量评估指标  
| 指标 | 合格 | 警告 |  
|--------|------|---------|  
| 发现的不变原则数量 | 3-10个 | 0个或超过15个 |  
| “黄金法则”候选者数量 | 1-5个 | 0个 |  
| 过滤掉的噪声比例 | 20%-40% | 小于10%或超过60% |  

---

## 术语说明  
| 术语 | 适用场景 | 禁用场景 |  
|------|---------|---------------|  
| **不变原则** | 在3个或更多来源中得到验证的原则 | 任意共享的原则 |  
| **黄金法则** | 被确认为权威来源的原则 | 未经验证的原则 |  
| **候选者** | 待人工审核的“黄金法则”候选者 | 已确认的真理 |  
| **合成** | 多来源信息提炼 | 两个来源的比较 |  

---

## 错误处理  
| 错误代码 | 触发原因 | 错误信息 | 建议 |  
|------------|---------|---------|------------|  
| `EMPTY_INPUT` | 未提供来源 | “需要至少3个来源才能进行合成。” | “请提供3个或更多的提取结果或文本来源。” |  
| `TOO_FEW_SOURCES` | 仅提供1-2个来源 | “合成需要3个或更多来源才能完成验证。” | “请添加更多来源，或使用principle-comparator进行两个来源的比较。” |  
| `SOURCE_MISMATCH` | 来源领域不匹配 | “这些来源似乎涉及不同主题。” | “建议使用涵盖相同领域的来源进行合成。” |  
| `NO_INVARIANTS` | 无原则在3个或更多来源中得到验证 | “可能这些来源确实独立，或尝试使用相关来源。” |  

---

## 相关技能  
- **pbe-extractor**：在合成前提取原则（技术性表述）  
- **essence-distiller**：在合成前提取原则（非正式表述）  
- **principle-comparator**：比较两个来源（N=1→N=2）  
- **pattern-finder**：比较两个来源（非正式比较工具）  
- **core-refinery**：此技能的对话式替代方案  
- **golden-master**：合成后追踪来源与原则之间的关系  

---

## 免责声明  
“黄金法则”候选者只是分析结果，并不代表绝对真理。一个原则在3个或更多来源中出现仅表明其具有普遍性，并不意味着其绝对正确。请使用该工具来识别候选者，但在将其视为权威依据之前，请自行进行判断。  

*由Obviously Not开发——用于启发思考，而非得出结论。*