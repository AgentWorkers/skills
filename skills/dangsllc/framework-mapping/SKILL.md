---
name: framework-mapping
description: 文档章节与合规性框架控制项之间的双向映射，并附带置信度评分。能够生成每个章节的控制项映射关系，以及针对 NIST、HITRUST、ISO 27001、SOC 2 和 HIPAA 标准的每个控制项的覆盖情况汇总。
argument-hint: Provide a compliance document and specify the target framework (e.g., NIST 800-53, HITRUST, ISO 27001)
allowed-tools: Read, Glob, Grep, WebFetch
version: 1.0
author: Rote Compliance
license: Apache-2.0
---
# 框架映射技能

作为一名合规性分析师，您的任务是在政策/程序文档与合规性框架（如 NIST 800-53、HITRUST CSF、HIPAA 安全规则、ISO 27001、SOC 2）的控制措施之间建立结构化的映射关系。您的输出结果应包括双向映射：控制措施 → 文档章节，以及文档章节 → 控制措施。这种映射关系将用于推动差距分析工作。

## 映射流程（步骤详解）

对于每个文档章节，请按照以下步骤操作：

1. **确定章节的主要主题**：该章节涉及哪个合规性领域？（例如：访问控制、风险管理、事件响应、物理安全、培训等）
2. **列出候选的控制措施**：列出所有与该章节主题相关的框架控制措施。在此阶段可以列出尽可能多的控制措施，宁可多一些也不要少。
3. **评估相关性**：根据以下标准评估每个控制措施的相关性，以确定该章节在多大程度上直接涉及了这些控制措施。
4. **剔除低相关性的映射**：删除相关性评分低于 0.3 的映射关系（除非该控制措施在文档中完全没有其他提及，否则保留该映射并标记为“相关性较弱”）。
5. **分配覆盖类型**：对于保留的映射关系，判断该章节是提供了主要覆盖、补充覆盖，还是仅提供了与该控制措施相关的信息。

## 相关性评分标准

| 评分范围 | 含义 |
|-------------|---------|
| 0.9 – 1.0 | 该章节直接实现了或定义了该控制措施，并使用了相应的监管语言。 |
| 0.7 – 0.89 | 该章节通过具体的程序或要求实质性地涵盖了该控制措施，但可能遗漏了一些细节。 |
| 0.5 – 0.69 | 该章节与该控制措施有显著关联，但未涉及重要的实施细节。 |
| 0.3 – 0.49 | 该章节仅部分涉及该控制措施，提到了相关主题但未满足其核心要求。 |
| 0.0 – 0.29 | 该章节与该控制措施仅有间接关联。除非它是唯一的证据，否则不要将其纳入映射关系中。 |

## 覆盖类型定义

- **主要覆盖**：该章节是直接满足控制措施要求的主要政策或程序。控制措施的负责人会将该章节视为权威的覆盖依据。
- **补充覆盖**：该章节提供了额外的细节、实施指南或背景信息，以支持主要覆盖内容。仅靠该章节不足以满足控制措施的要求。
- **间接关联**：该章节仅简要提到了该控制措施的主题，但不构成政策或程序上的覆盖。需要对这些内容进行标记，因为这可能表明对该控制措施的理解不够深入。

## 跨框架映射规则

在同时映射多个框架时，请遵循以下规则：

1. **优先选择最具体的引用方式**：对于 HIPAA，使用 45 CFR 的章节编号；对于 NIST，使用控制措施标识符（例如 AC-2）；对于 HITRUST，使用控制措施类别编号。
2. **识别控制措施所属的类别**：将属于同一类别的控制措施归为一组，以判断该章节是提供了广泛的类别覆盖还是具体的子控制措施覆盖。
3. **标记跨框架的等效关系**：当同一章节在多个框架中对应于相同的控制措施时（例如 NIST AC-2 和 HIPAA 164.308(a)(3)），请标注这种等效关系，以便分析师通过一次审查即可验证。
4. **切勿推断隐含的覆盖**：即使某个章节没有明确提及某个控制措施，也不要假设它已被覆盖。每个映射关系都必须有独立的依据。

## 输出格式规范

生成两种互补的映射结果：

### 按章节划分的映射关系

```json
{
  "section_id": "string — document section identifier (e.g., '§3.2', 'Section 4: Access Control')",
  "section_title": "string — heading text",
  "section_summary": "string — 1-2 sentence summary of what the section covers",
  "control_mappings": [
    {
      "control_id": "string — framework control identifier",
      "framework": "string — framework name",
      "relevance_score": "float — 0.0 to 1.0",
      "coverage_type": "primary | supplemental | tangential",
      "rationale": "string — why this section maps to this control"
    }
  ]
}
```

### 按控制措施划分的覆盖情况总结

```json
{
  "control_id": "string — framework control identifier",
  "control_name": "string — human-readable name",
  "framework": "string — framework name",
  "coverage_status": "covered | partial | gap",
  "primary_sections": ["string — section IDs with primary coverage"],
  "supplemental_sections": ["string — section IDs with supplemental coverage"],
  "unaddressed_aspects": "string | null — what parts of the control are not covered by any section",
  "aggregate_confidence": "float — 0.0 to 1.0"
}
```

## 示例说明

### 示例 1：主要覆盖关系明确

**控制措施：** NIST 800-53 AC-2 — 账户管理  
**章节内容：**  
“第 5.3 节：用户账户生命周期——所有用户账户均需经过正式的请求和审批流程进行管理。IT 部门在收到招聘经理的书面批准后一个工作日内创建账户。部门经理每季度对账户进行审核，并在员工离职通知后 24 小时内禁用账户。”

**映射关系：**
```json
{
  "control_id": "AC-2",
  "framework": "NIST 800-53 Rev 5",
  "relevance_score": 0.92,
  "coverage_type": "primary",
  "rationale": "Section directly implements account management lifecycle: provisioning (1 business day SLA), authorization (written manager approval), periodic review (quarterly), and account disabling on termination (24-hour SLA). Covers AC-2 enhancements (a)(1)-(a)(9) substantially."
}
```

### 示例 2：多个章节共同覆盖同一控制措施**

**控制措施：** ISO 27001 A.9.4.1 — 信息访问限制  
**涉及的章节：**  
- 第 4.1 节：角色定义和最小权限原则  
- 第 4.5 节：应用程序访问控制和权限矩阵  

**映射关系：**
```json
[
  {
    "section_id": "§4.1",
    "control_id": "A.9.4.1",
    "framework": "ISO 27001",
    "relevance_score": 0.75,
    "coverage_type": "primary",
    "rationale": "Establishes least privilege principle and role-based access concept — the policy foundation for access restriction."
  },
  {
    "section_id": "§4.5",
    "control_id": "A.9.4.1",
    "framework": "ISO 27001",
    "relevance_score": 0.85,
    "coverage_type": "supplemental",
    "rationale": "Provides implementation detail (permission matrices, application-level controls) that operationalizes the policy in §4.1."
  }
]
```

### 示例 3：无映射关系（表示存在差距）

**控制措施：** NIST 800-53 IR-4 — 事件处理  
**文档内容：** 未找到任何关于事件检测、分类、遏制、消除或恢复程序的章节。

**输出结果：**
```json
{
  "control_id": "IR-4",
  "control_name": "Incident Handling",
  "framework": "NIST 800-53 Rev 5",
  "coverage_status": "gap",
  "primary_sections": [],
  "supplemental_sections": [],
  "unaddressed_aspects": "No incident response procedures found in document. Missing: incident detection criteria, classification taxonomy, response team definition, containment procedures, recovery steps, and post-incident review process.",
  "aggregate_confidence": 0.95
}
```

## 重要指南

- **章节的粒度很重要**：请在章节级别进行映射，而不是段落级别。如果一个章节涉及多个控制措施，也请将所有映射关系都记录下来。
- **区分政策和程序**：政策规定了应执行的内容，而程序则说明了执行方式。控制措施通常需要同时满足这两方面的要求。请注意哪些章节提供了其中之一，但未提供另一方。
- **明确组织范围的模糊性**：如果不清楚某个章节适用于所有系统/用户还是仅适用于部分系统/用户，请在说明中说明这一点，因为这可能会影响差距分析的结果。
- **不要用通用最佳实践来填补空白**：如果文档中没有相关内容，不要根据行业规范进行推断。您的任务是映射文档中实际写明的内容，而不是应该写明的内容。
- **标记需要多个框架覆盖的控制措施**：当一个控制措施在多个框架中具有等效的映射关系时（例如 HIPAA 164.308(a)(1) ≈ NIST RA-3 ≈ ISO 27001 A.8.2.1），请明确标注这些关系，以避免分析师重复审查。