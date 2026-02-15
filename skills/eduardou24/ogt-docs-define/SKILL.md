---
name: ogt-docs-define
description: 创建定义文档的通用指南。当您需要明确说明某事物的本质（如概念、实体、系统或领域）时，请参考本指南。针对不同类型的定义（业务、功能、代码、市场营销、品牌建设、工具等），可参考相应的子指南。
---

# OGT 文档 - 定义（Definition Documentation）

本指南用于创建定义文档，明确系统中各项内容的含义。

## 哲学理念

**定义是共同理解的基础。**

在任何人能够实施、推广或讨论某个概念之前，必须首先对其有一个清晰、共识一致的定义。

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE DEFINITION PRINCIPLE                     │
├─────────────────────────────────────────────────────────────────┤
│  A definition answers:                                          │
│    • WHAT is this thing?                                        │
│    • WHY does it exist?                                         │
│    • WHAT are its boundaries? (what it is NOT)                  │
│    • HOW does it relate to other things?                        │
│                                                                 │
│  A definition does NOT specify:                                 │
│    • HOW to implement it (that's rules/)                        │
│    • WHAT to do with it (that's todo/)                          │
└─────────────────────────────────────────────────────────────────┘
```

## 何时使用该技能

当您需要以下操作时，请使用 `ogt-docs-define`：

- 了解定义文档的文件夹结构；
- 选择合适的定义子技能；
- 创建无法归类到特定类别的定义内容。

**针对不同类型的定义，可使用以下子技能：**

| 定义类型            | 子技能                          | 使用场景                          |
| ---------------------------- | ----------------------------- | -------------------------------------- |
| 商业概念            | `ogt-docs-define-business`       | 定价策略、用户群体、收入模型             |
| 产品特性            | `ogt-docs-define-feature`       | 新功能、用户交互界面                 |
| 技术架构            | `ogt-docs-define-code`       | 服务架构、数据模型、API                 |
| 营销概念            | `ogt-docs-define-marketing`       | 营销策略、目标受众                   |
| 品牌标识            | `ogt-docs-define-branding`       | 视觉标识、品牌调性、使用指南                 |
| 开发工具            | `ogt-docs-define-tools`       | 命令行工具、脚本、开发工作流程             |

## 文件夹结构

每个定义内容都对应一个文件夹，文件夹的命名规则如下：

```
docs/definitions/
├── business/                   # Business model and operations
│   ├── pricing_model/
│   │   ├── definition.md
│   │   ├── tiers.md
│   │   ├── limits.md
│   │   └── .approved_by_founder
│   ├── user_types/
│   ├── revenue_model/
│   └── market_position/
│
├── features/                   # Product features
│   ├── global_search/
│   │   ├── feature.md
│   │   ├── mvp.md
│   │   ├── phase_0.md
│   │   ├── phase_1.md
│   │   ├── nice_to_have.md
│   │   └── .version
│   ├── user_auth/
│   └── campaign_manager/
│
├── technical/                  # Architecture and systems
│   ├── service_layer/
│   │   ├── definition.md
│   │   ├── contracts.md
│   │   ├── patterns.md
│   │   └── .version
│   ├── data_model/
│   └── api_design/
│
├── domain/                     # Domain-specific concepts
│   ├── creatures/
│   ├── abilities/
│   └── campaigns/
│
├── marketing/                  # Marketing and communications
│   ├── value_proposition/
│   ├── target_audience/
│   └── messaging/
│
├── branding/                   # Brand identity
│   ├── visual_identity/
│   ├── tone_of_voice/
│   └── brand_guidelines/
│
└── tools/                      # Developer tooling
    ├── cli/
    ├── scripts/
    └── workflows/
```

## 文件夹作为实体（Folder-as-Entity）的模式

每个定义文档都包含以下文件：

```
{definition_slug}/
├── {type}.md                   # Primary definition file
├── {aspect}.md                 # Additional aspects/details
├── {related}.md                # Related concepts
└── .{signals}                  # Status and metadata
```

### 主文件命名规则

| 定义类型            | 主文件名                          |
| ---------------------------- | -------------------------------------- |
| 商业概念            | `definition.md`                     |
| 产品特性            | `feature.md`                        |
| 技术架构            | `technical_definition.md`                |
| 领域相关            | `domain_definition.md`                   |
| 营销策略            | `marketing_definition.md`                   |
| 品牌标识            | `branding_definition.md`                   |
| 开发工具            | `tools_definition.md`                   |

## 定义文档的生命周期

### 草稿阶段

定义文档正在编写中，尚未准备好接受审核。

```
{definition_slug}/
├── definition.md
├── .version
└── .draft                      # Empty signal: still in draft
```

### 审核阶段

定义文档已完成，等待审核通过。

```
{definition_slug}/
├── definition.md
├── .version
├── .ready_for_review           # Empty signal
└── .review_requested_at        # Timestamp
```

### 审核通过阶段

定义文档已通过审核，可以用于参考或实际应用。

```
{definition_slug}/
├── definition.md
├── .version
├── .approved                   # Empty signal
├── .approved_by_{name}         # Who approved
└── .approved_at                # When approved
```

### 被拒绝阶段

定义文档被拒绝，需要重新编写。

```
{definition_slug}/
├── definition.md
├── .version
├── .rejected                   # Empty signal
├── .rejected_reason            # Why rejected
└── .rejected_at                # When rejected
```

### 已过时阶段

定义文档已过时，被新的内容替代。

```
{definition_slug}/
├── definition.md
├── .version
├── .deprecated                 # Empty signal
├── .deprecated_reason          # Why deprecated
├── .deprecated_at              # When deprecated
└── .superseded_by              # What replaces it
```

---

## 创建定义文档的流程

### 第一步：提出澄清性问题

在编写定义之前，收集相关信息：

**核心问题（务必询问）：**
1. 这个概念的名称/标识是什么？
2. 用一句话概括它的含义是什么？
3. 为什么需要这个概念？它能解决什么问题？
4. 它不包括哪些内容？（明确边界）
5. 它与其他哪些概念相关？

**根据具体情况，还可以询问：**
6. 相关的利益相关者是谁？
7. 是否已有类似的概念？
8. 是哪些决策导致了这个概念的产生？
9. 成功的标准是什么？

### 第二步：起草定义文档

根据定义类型选择相应的模板（参见相应的子技能）。

**通用定义文档模板：**

```markdown
# Definition: {Name}

## Overview

One paragraph explaining what this is and why it exists.

## Core Concept

Detailed explanation of the concept.

### Key Characteristics

- Characteristic 1
- Characteristic 2
- Characteristic 3

### Boundaries

What this is NOT:

- Not X
- Not Y
- Not Z

## Relationships

How this relates to other concepts.

| Related Concept | Relationship               |
| --------------- | -------------------------- |
| Concept A       | Uses/Contains/Depends on   |
| Concept B       | Parallel to/Alternative to |

## Examples

Concrete examples that illustrate the concept.

### Example 1: {Name}

Description of example.

### Example 2: {Name}

Description of example.

## Open Questions

Unresolved questions that need future discussion.

- Question 1?
- Question 2?
```

### 第三步：添加辅助文件

```bash
# Create version file
echo '{"schema": "1.0", "created": "'$(date -Iseconds)'"}' > .version

# Mark as draft
touch .draft
```

### 第四步：请求审核

```bash
# Remove draft signal
rm .draft

# Add review signals
touch .ready_for_review
echo "$(date -Iseconds)" > .review_requested_at
```

### 第五步：处理审核结果

**如果审核通过：**

```bash
rm .ready_for_review .review_requested_at
touch .approved
touch .approved_by_{reviewer_name}
echo "$(date -Iseconds)" > .approved_at
```

**如果被拒绝：**

```bash
rm .ready_for_review .review_requested_at
touch .rejected
echo "Reason for rejection" > .rejected_reason
echo "$(date -Iseconds)" > .rejected_at
# Then address feedback and restart from Step 2
```

---

## 辅助文件说明

### 状态标识文件（empty files）

| 文件标识            | 含义                                      |
| ----------------------------- | -------------------------------------- |
| `.draft`            | 文档仍在编写中                         |
| `.ready_for_review`     | 已准备好接受审核                         |
| `.approved`         | 审核通过，可以投入使用                         |
| `.rejected`         | 被拒绝，需要重新编写                         |
| `.deprecated`       | 已过时，不再适用                         |

### 作者/审核者标识文件（empty files）

| 文件标识            | 含义                                      |
| ----------------------------- | -------------------------------------- |
| `.approved_by_{name}`     | 审核者姓名                             |
| `.created_by_{name}`     | 创建者姓名                             |
| `.reviewed_by_{name}`     | 审核者姓名                             |

### 内容标识文件（包含文本内容）

| 文件标识            | 文件内容                                      |
| ----------------------------- | -------------------------------------- |
| `.version`         | JSON 格式，包含版本信息（例如：`{"schema": "1.0", "created": "..."}`） |
| `.rejected_reason`     | 被拒绝的原因                         |
| `.deprecated_reason`     | 被标记为过时的原因                         |
| `.superseded_by`      | 替代文档的路径                         |
| `.review_requested_at`    | 提交审核的时间戳                         |
| `.approved_at`     | 被批准的时间戳                         |
| `.rejected_at`     | 被拒绝的时间戳                         |
| `.deprecated_at`     | 被标记为过时的时间戳                         |

---

## 引用定义文档

当其他文档需要引用某个定义时：

```markdown
See [Definition: User Types](docs/definitions/business/user_types/)
Per the [Service Layer Definition](docs/definitions/technical/service_layer/)
```

当代码实现某个定义时，应在代码中添加相应的注释：

```typescript
/**
 * Implements: docs/definitions/technical/service_layer/
 * @see definition.md for contracts
 */
export class UserService implements IService {
  // ...
}
```

---

## 常见错误

| 错误类型                | 错误原因                                      | 正确的做法                                      |
| ---------------------- | -------------------------------------- | -------------------------------------------------------- |
| 将定义与规则混为一谈        | 将“是什么”与“如何实现”混淆                   | 保持定义的纯粹性，将实现方式放在规则中                 |
| 未明确界定定义范围        | 范围不明确可能导致理解偏差                   | 必须明确界定定义的内容                         |
| 跳过审核流程            | 未经审核的定义可能导致不一致性                   | 必须完成审核流程                             |
| 修改已通过的定义          | 可能破坏引用关系                         | 应创建新版本或标记文档为过时                         |
| 未标注定义之间的关系        | 各自独立的定义难以协同使用                     | 明确标注定义之间的关联                         |
| 定义过于抽象            | 过于抽象的内容难以实现                         | 应提供具体的示例                         |
| 定义过于具体            | 过于具体的定义难以适应变化                     | 保持定义的抽象性                         |

---

## 质量检查清单

在提交审核之前，请确认以下内容：
- [ ] 概述部分能用一段话清晰解释定义的内容及其目的；
- [ ] 核心概念描述得足够详细，便于理解；
- [ ] 明确界定了定义的范围（即它不包括哪些内容）；
- [ ] 明确了该定义与其他定义之间的关系；
- [ ] 提供了至少两个具体的示例；
- [ ] 列出了所有未解决的问题（如果有）；
- [ ] 已创建了 `.version` 文件；
- [ ] 存在 `.draft` 文件（提交审核时会自动删除）。