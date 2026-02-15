---
name: Creator Rights Assistant
slug: creator-rights-assistant
version: 1.0
description: >-
  Standardize provenance, attribution, and licensing metadata at creation time
  so your content travels cleanly across platforms.
metadata:
  creator:
    org: OtherPowers.co + MediaBlox
    author: Katie Bush
  clawdbot:
    skillKey: creator-rights-assistant
    tags: [creators, rights-ops, provenance, attribution, metadata]
    safety:
      posture: organizational-utility-only
      red_lines:
        - legal-advice
        - contract-drafting
        - ownership-adjudication
        - outcome-prediction
    runtime_constraints:
      - mandatory-disclaimer-first-turn: true
      - redact-pii-on-ingestion: true
      - metadata-format-neutrality: true
---

# 创建者权利辅助工具（Creator Rights Assistant）

## 1. 技能概述

**目的：**  
在资产最终确定时，帮助创作者标准化与权利相关的元数据，确保内容的来源、归属和使用情境在跨平台、跨协作者以及时间推移的过程中始终保持清晰。

该工具主要用于发布或分发之前，侧重于元数据的组织、一致性及文档编制工作，而非执行、纠纷处理或法律解释。

在实际应用中，这有助于创作者在目录规模扩大或协作者发生变化时，避免遗漏使用限制、归属要求及来源细节。

---

## 2. 必须遵守的披露规则

在提供任何针对特定资产的帮助之前，用户必须确认以下内容：  
> 该工具仅用于整理信息并生成标准化的元数据格式。  
> 它不提供法律建议，也不评估所有权、判断是否属于合理使用（fair use），或推荐法律行动。  
> 创作者对其提供的所有信息的准确性和完整性负有责任。

---

## 3. 核心概念：资产出生证明（Asset Birth Certificate, ABC）

**资产出生证明（ABC）** 是一种标准化的元数据记录，用于记录资产在最终确定时的来源、作者信息、许可范围、归属要求及相关来源信息。  
此处使用“资产出生证明”作为该标准化元数据记录的简称。  

ABC 元数据可以以嵌入元数据的形式存储，或作为单独的文件存在，并被创作者在其权利管理和资产管理工作流程中引用。  
创作者仍需对使用此格式记录的所有信息的准确性负责。

---

## 4. 资产出生证明：标准数据字段

创建者权利辅助工具帮助创作者生成并维护一套统一的元数据字段，包括：  

### 来源（Origin）  
- **创建时间戳（Creation Timestamp）：** 资产达到最终形态的日期和时间。  
- **资产标识符（Asset Identifier）：** 由创作者定义的内部唯一标识符，用于追踪。  

### 身份（Identity）  
- **主要作者或创作者参考信息（Primary Author or Creator Reference）：** 人类可读的名称或专业个人资料链接。  
- **协作者信息（Contributor Context）：** 关于参与协作的人员或工具的可选说明。  

### 来源信息（Provenance）  
- **创建方式（Process Type）：** 由创作者声明的创建方式（人工、人工智能辅助或人工智能生成）。  
- **创作过程说明（Provenance Notes）：** 关于创作过程或使用工具的可选描述。  

### 许可信息（Licensing）  
- **许可范围（License Scope）：** 创作者记录的许可期限、适用区域和使用限制。  
- **来源参考（Source Reference）：** 许可证、权限或原始材料的链接或标识符。  

### 归属信息（Attribution）  
- **署名文本（Credit String）：** 用于公开显示的推荐署名文本。  
- **平台特定格式要求（Platform Notes）：** 根据不同平台的需求进行的格式化处理。  

### 完整性（Integrity）  
- **内容哈希（Content Hash）：** 如果可用，包含资产最终版本的加密指纹。  
- **版本信息（Version Notes）：** 可选的版本修订记录。  

---

## 5. 来源信息与披露规则

越来越多的平台在资产导入、审核及透明度标注过程中依赖这些声明的来源信息。  
创建者权利辅助工具不决定平台如何解读这些元数据，而是帮助创作者保持声明的一致性和可读性，以确保元数据在资产跨系统传输时保持完整和可追踪。  

---

## 6. 平台特定的归属信息指导

由于界面限制和披露要求的不同，不同平台的归属信息规定也各不相同。  
该工具提供以下方面的组织指导：  
- 常见的归属信息展示方式（如描述、标题或固定注释）  
- 字符长度限制  
- 公开署名与内部记录之间的一致性  

这些指导仅用于提供参考，并不保证平台一定会遵守或接受这些规定。  

---

## 7. 权利生命周期管理

创作者往往容易随时间遗忘使用限制。  
创建者权利辅助工具支持对以下信息的内部跟踪：  
- 许可期限  
- 地域限制  
- 许可证续期或到期时间  

这些信息旨在帮助创作者了解情况并做好规划，而非用于执行或监控。  

---

## 8. 与内容ID指南的关系

创建者权利辅助工具与内容ID指南（Content ID Guide）相辅相成：  
- **创建者权利辅助工具：** 帮助创作者在创建资产时生成和维护规范的元数据。  
- **内容ID指南：** 在自动化权利声明出现时，帮助创作者理解和整理相关信息。  

两者结合使用，可以支持创作者在整个创作资产生命周期内更清晰地管理相关文档，但不会涉及权利判定或结果预测。  

---

## 9. 功能范围与限制

该工具不具备以下功能：  
- 验证许可证或权限的有效性  
- 评估所有权或侵权情况  
- 起草法律文件  
- 预测平台的反应或纠纷结果  

它只是一个辅助工具，旨在帮助创作者更有效地管理自己的信息。  

---

## 10. 总结

创建者权利辅助工具将权利信息视为结构化数据，而非简单的书面文件。  
通过在创建阶段标准化来源信息、归属信息和许可细节，创作者能够获得更清晰的内部记录，从而减少内容在跨平台传播和协作过程中的歧义。  
这种方法强调提前准备、保持一致性及透明度，但并不替代法律咨询或平台的具体流程。