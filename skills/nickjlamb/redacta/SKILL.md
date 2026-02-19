---
name: redacta
description: Redacta 会对医疗文件进行匿名处理——将患者标识信息（如 NHS 编号、出生日期、邮政编码、电话号码、医院名称等）替换为带有标签的占位符，从而确保临床数据能够被 AI 安全地处理。该工具由 PharmaTools.AI 开发。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔒",
        "homepage": "https://pharmatools.ai",
      },
  }
---
# Redacta

Redacta 在对医疗文档进行人工智能处理之前，会对其进行匿名化处理。它会检测出患者标识符，并将这些标识符替换为标记化的令牌，从而在保护隐私的同时保留文档的临床信息。

## 工作原理

当用户共享医疗文本时，系统会扫描文本中的患者标识符，并将其替换为匿名化令牌。处理后的文档仍然具有临床可读性，但不包含任何真实的患者数据。

## 可检测的标识符类型

### 结构化标识符（基于正则表达式）

系统会自动应用以下规则进行替换：

**NHS 编号**（英国）
- 格式：3-3-4 位数字（例如 `943 476 5919`）或连续的 10 位数字
- 替换为：`[NHS_NUMBER]`
- 可能会使用模 11 算法进行校验

**出生日期**
- 格式：DD/MM/YYYY、DD-MM-YYYY、DD.MM.YYYY、YYYY-MM-DD、"3rd February 1985"、"Feb 3, 1985"
- 替换为：`[DATE_OF_BIRTH]`（如果是出生日期）或 `[DATE]`（其他日期）
- 如果日期明显不用于识别患者身份（例如 "预约日期为 15 March"），则保留原样

**英国邮政编码**
- 格式：A9 9AA、A99 9AA、A9A 9AA、AA9 9AA、AA99 9AA、AA9A 9AA
- 替换为：`[POSTCODE]`

**电话号码**
- 英国格式：07xxx、01xxx、02xxx、+44
- 美国格式：(xxx) xxx-xxxx、xxx-xxx-xxxx、+1
- 替换为：`[PHONE_NUMBER]`

**电子邮件地址**
- 标准电子邮件格式
- 替换为：`[EMAIL]`

**医院编号/医疗记录编号（MRN）**
- 出现在 "hospital number"、"MRN"、"patient ID"、"unit number"、"case number" 等关键词附近的编号
- 替换为：`[HOSPITAL_NUMBER]`

**英国国民保险号码**
- 格式：2 个字母 + 6 位数字 + 1 个字母（例如 AB123456C）
- 替换为：`[NI_NUMBER]`

**上下文相关的标识符（基于人工判断）**

系统会根据对医疗文档的理解来检测以下内容：

**患者姓名**
- 在称呼（如 "Dear Mrs Jones"）、标题（如 "Patient: John Smith"）或正文中的引用中查找患者姓名
- 区分患者姓名和医护人员姓名——除非用户明确要求，否则不要对医生/护士/顾问的姓名进行匿名化处理
- 替换为：`[PATIENT_NAME]`
- 如果提到多个患者，使用 `[PATIENT_NAME_1]`、`[PATIENT_NAME_2]` 等格式

**患者地址**
- 完整或部分的地址（门牌号 + 街道名称），或出现在 "address"、"lives at"、"resides" 等短语附近的地址
- 替换为：`[ADDRESS]`
- 邮政编码的处理方式与上述规则相同

**年龄**
- 单独使用时可能用于识别患者的年龄（例如 "82-year-old"、"aged 47"）
- 替换为：`[AGE]`
- 上下文很重要：例如 "children aged 5-12"（泛指）与 "a 73-year-old woman"（特定患者）

## 输出格式

系统会返回两个部分：

### 1. 匿名化后的文档
- 所有标识符都被替换为令牌后的完整文档。保留原有的格式、段落分隔和临床内容。

### 2. 匿名化报告
- 包含检测结果和替换内容的总结：

```
Redaction Report
================
Items pseudonymised: 7

- [NHS_NUMBER] × 1 (line 3)
- [PATIENT_NAME] × 2 (lines 1, 5)
- [DATE_OF_BIRTH] × 1 (line 2)
- [POSTCODE] × 1 (line 8)
- [PHONE_NUMBER] × 1 (line 9)
- [AGE] × 1 (line 4)

Clinical content preserved: ✓
Clinician names preserved: Dr. Sarah Chen, Mr. James Wright
```

## 规则

1. **切勿在输出中显示原始的患者标识符**，仅显示匿名化后的版本。
2. **保留所有临床内容**，包括药物信息、诊断结果、治疗过程和临床观察记录。
3. **默认情况下保留医护人员姓名**，除非用户明确要求进行匿名化处理。
4. **默认情况下保留医院/医疗机构的名称**，因为这些属于机构信息，不属于患者个人数据。
5. **在不确定的情况下，倾向于进行匿名化处理**——误判为阳性比误判为阴性更安全。
6. **日期**：除非可能用于识别患者（例如具体的出生日期），否则应保留预约日期、治疗日期和随访日期。
7. **一致性**：相同的标识符在整个文档中应使用相同的标记方式（例如，患者的姓名始终替换为 `[PATIENT_NAME]`）。

## 示例

**输入：**
```
Dear Mrs Patricia Hartley,

DOB: 14/03/1952 (age 73)
NHS Number: 943 476 5919
Hospital Number: RXH-2847561

I am writing to inform you of the results of your recent investigations.
Mrs Hartley attended the cardiology outpatient clinic on 10 February 2026
under the care of Dr Sarah Chen.

Address: 14 Oakfield Road, Headingley, Leeds LS6 3PJ
Tel: 0113 278 4532
```

**输出：**
```
Dear [PATIENT_NAME],

DOB: [DATE_OF_BIRTH] (age [AGE])
NHS Number: [NHS_NUMBER]
Hospital Number: [HOSPITAL_NUMBER]

I am writing to inform you of the results of your recent investigations.
[PATIENT_NAME] attended the cardiology outpatient clinic on 10 February 2026
under the care of Dr Sarah Chen.

Address: [ADDRESS], [POSTCODE]
Tel: [PHONE_NUMBER]
```

## 本功能不包含的内容

- 不会存储或传输患者数据。
- 无法保证 100% 的检测率（请务必审核处理后的结果）。
- 不能替代正式的数据保护流程。
- 不提供法律合规性认证。
- 仅支持文本输入（不支持图像或 PDF 文件的处理）。

## 隐私声明

本功能在您的 AI 会话中本地处理文本。任何患者数据都不会被发送到外部服务。不过，文本会由底层的语言模型进行处理，请确保您使用的语言模型提供商的数据处理方式符合您组织的要求。

---

由 [PharmaTools.AI](https://pharmatools.ai) 开发——专为制药和医疗行业设计的 AI 工具。