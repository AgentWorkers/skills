---
name: design-fhir-loinc-questionnaires
description: 该工具能够帮助用户根据普通的业务需求文档创建符合 FHIR 标准的问卷定义。它包含了一些脚本，用于通过官方的编码 API 查找与医疗状况、检查结果、观察结果、药物及医疗程序相关的 LOINC（Logical Observation Identifiers）和 SNOMED CT（Systematized Nomenclature of Medicine – Clinical Terms）代码。目前无需使用 API 密钥即可使用该工具。
metadata:
  dependencies: python>=3.8, jsonschema>=4.0.0
---

# FHIR 问卷技能

## ⚠️ 重要规则 - 请先阅读

**切勿凭记忆或训练数据来推荐 LOINC 或 SNOMED CT 代码。务必使用本技能中的搜索和查询脚本。**

当需要任何临床代码时：
1. **对于临床问题/观察结果：务必先运行 `python scripts/search_loinc.py "搜索词"`**
2. **对于临床概念/疾病：务必先运行 `python scripts/search_snomed.py "搜索词"`**
3. **仅使用脚本返回的代码**
4. **如果搜索失败或未返回结果，请勿自行编造代码**

来自 AI 的临床代码可靠性极低，可能会导致错误的临床编码。

## 网络访问要求

需要白名单网络访问权限：
- `clinicaltables.nlm.nih.gov`（用于 LOINC 搜索）
- `tx.fhir.org`（用于 LOINC 答案列表和 SNOMED CT 搜索的 FHIR 术语服务器）

如果网络访问失败，请立即停止操作，切勿推荐任何代码。

## 必需使用的脚本（每次使用）

### 1. 搜索 LOINC 代码
**在推荐任何 LOINC 代码（临床问题/观察结果）之前，务必先运行此脚本：**
```bash
python scripts/search_loinc.py "depression screening"
python scripts/search_loinc.py "blood pressure" --format fhir
```

### 2. 搜索 SNOMED CT 代码
**在推荐任何 SNOMED CT 代码（临床概念/疾病）之前，务必先运行此脚本：**
```bash
python scripts/search_snomed.py "diabetes"
python scripts/search_snomed.py "hypertension" --format fhir
python scripts/search_snomed.py "diabetes mellitus" --semantic-tag "disorder"
```
注意：当语义标签出现在显示名称中时（例如：“Diabetes mellitus (disorder)”），`--semantic-tag` 过滤器效果最佳。

### 3. 查找答案选项
**对于有标准化答案的问题：**
```bash
python scripts/query_valueset.py --loinc-code "72166-2"
python scripts/query_valueset.py --loinc-code "72166-2" --format fhir
```

### 4. 验证问卷
**在最终确定答案之前：**
```bash
python scripts/validate_questionnaire.py questionnaire.json
```

## 模板

从 `assets/templates/` 目录开始：
- `minimal.json` - 基本结构
- `basic.json` - 简单问卷
- `advanced.json` - 包含条件逻辑的复杂问卷

## 工作流程

### 标准化临床工具（PHQ-9、GAD-7 等）
```bash
# Step 1: Find panel code (NEVER skip this)
python scripts/search_loinc.py "PHQ-9 panel"

# Step 2: Find answer options
python scripts/query_valueset.py --loinc-code "FOUND-CODE" --format fhir

# Step 3: See examples/templates
# Check references/examples.md for complete implementations
```

### 定制组织问卷
```bash
# Step 1: Start with template
cp assets/templates/advanced.json my-questionnaire.json

# Step 2: For any clinical questions, search LOINC
python scripts/search_loinc.py "body weight"

# Step 3: Add answer options if available
python scripts/query_valueset.py --loinc-code "FOUND-CODE"

# Step 4: For custom questions without LOINC results, use inline answerOptions
# (no coding system needed - just code + display)

# Step 5: Validate
python scripts/validate_questionnaire.py my-questionnaire.json
```

### 定制答案列表（当 LOINC 无法匹配时）

当 LOINC 搜索未返回合适的答案列表时，默认使用 **带有无系统代码的 inline answerOption**。这是符合规范的、最简单的自定义答案列表方法：

```json
{
  "linkId": "sleep-quality",
  "type": "choice",
  "text": "How would you rate your sleep quality?",
  "answerOption": [
    {"valueCoding": {"code": "good", "display": "Good"}},
    {"valueCoding": {"code": "fair", "display": "Fair"}},
    {"valueCoding": {"code": "poor", "display": "Poor"}}
  ]
}
```

**切勿创建自定义的编码系统 URI**。省略 `system` 是符合 FHIR 标准的做法，表示这些代码是本地生成的、仅用于特定问卷的。

#### 可选：可重用的 Welshare 编码系统

如果用户明确要求使用可在多个问卷中重复使用的代码，请通过辅助脚本使用 Welshare 命名空间（`http://codes.welshare.app`）：

```bash
python scripts/create_custom_codesystem.py --interactive
```

这将创建一个 CodeSystem + ValueSet 对。要将内联答案列表转换为可重用格式，请在每个 `valueCoding` 中添加 `"system": "http://codes.welshare.app/CodeSystem/<category>/<id>.json"`，并通过 `answerValueSet` 参考相应的 ValueSet。详情请参阅 `references/loinc_guide.md`。

## 常见模式

- **条件显示**：使用 `enableWhen` 来显示/隐藏问题
- **重复组**：对于药物、过敏等情况，设置 `"repeats": true`
- **标准化答案**：对于基于 LOINC 的答案列表，使用 `query_valueset.py --loinc-code "CODE"`
- **自定义答案**：对于非标准化的选项，使用带有 `valueCoding` 的内联 `answerOption`（不包含 `system`）

完整的工作示例请参阅 `references/examples.md`。

## 脚本参考

### search_loinc.py - 查找 LOINC 代码
```bash
python scripts/search_loinc.py "blood pressure"
python scripts/search_loinc.py "depression" --limit 10 --format fhir
```

### search_snomed.py - 查找 SNOMED CT 代码
```bash
python scripts/search_snomed.py "diabetes"
python scripts/search_snomed.py "hypertension" --limit 10 --format fhir
python scripts/search_snomed.py "asthma" --format table
python scripts/search_snomed.py "diabetes mellitus" --semantic-tag "disorder"
```
**输出格式：** `json`（默认）、`table`、`fhir`
**结果中的语义标签：** `disorder`、`finding`、`procedure`、`body structure`、`substance`、`organism`
注意：只有当术语服务器的显示名称中包含语义标签时，语义标签过滤才有效。

### query_valueset.py - 查找答案选项
```bash
python scripts/query_valueset.py --loinc-code "72166-2"
python scripts/query_valueset.py --loinc-code "72166-2" --format fhir
python scripts/query_valueset.py --search "smoking"
```
**备用服务器**（如果 `tx.fhir.org` 失效时）：
- `--server https://hapi.fhir.org/baseR4`
- `--server https://r4.ontoserver.csiro.au/fhir`

### validate_questionnaire.py - 验证问卷结构
```bash
python scripts/validate_questionnaire.py questionnaire.json
python scripts/validate_questionnaire.py questionnaire.json --verbose
```

### extract_loinc_codes.py - 分析代码
```bash
python scripts/extract_loinc_codes.py questionnaire.json
python scripts/extract_loinc_codes.py questionnaire.json --validate
```

### create_custom_codesystem.py - 可重用的自定义代码（可选）
```bash
python scripts/create_custom_codesystem.py --interactive
```
仅当用户明确要求在多个问卷中使用可重用代码时使用。使用 Welshare 命名空间：`http://codes.welshare.app`。默认情况下，自定义答案使用不带编码系统的 inline `answerOption`。

## 故障排除

- **没有 LOINC 结果**：使用更宽泛的搜索词（例如，使用 “depression” 而不是 “PHQ-9 question 1”）
- **网络错误**：尝试使用 `--server` 标志切换到备用服务器
- **验证错误**：请查阅 `references/fhir_questionnaire_spec.md` 以了解要求
- **未找到答案列表**：使用带有无系统代码的 `valueCoding` 的内联 `answerOption`（仅显示代码）。除非用户明确要求，否则不要使用自定义编码系统

## 深度知识参考

我们整理了相关主题的深度知识供您参考。请查看 [REFERENCE.md] 中的索引文件，并深入了解问卷建模的详细说明。

## 参考链接

- [FHIR 问卷规范](https://hl7.org/fhir/questionnaire.html)
- [LOINC 数据库](https://loinc.org)
- [完整文档](REFERENCE.md)