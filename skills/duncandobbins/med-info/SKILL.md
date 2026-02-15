---
name: med-info
description: 药品信息，包含来自权威公共来源（openFDA、RxNorm/RxClass、DailyMed、MedlinePlus）的引用和可追溯的标识符（RxCUI/NDC/set_id）。信息中包含药品说明书内容，以及可选的药品召回、短缺、FDA不良事件报告（FAERS）相关数据，以及《橙皮书》（Orange Book）和《紫皮书》（Purple Book）中的相关信息。
metadata: {"clawdbot": {"emoji": "💊", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---

# med-info

**药品信息查询与引用——快速高效**

该工具可提供来自权威公共来源（FDA标签信息及NLM标识符）的、经过验证的药品信息摘要。适用于参考和研究用途——**不**提供医疗建议。

**隐私保护：**不包含任何患者隐私信息（PHI）。支持通过药品名称、**RxCUI**、**NDC**或标签**set_id**进行查询。

## 主要特点

- **引用与可追溯性：**包含标识符（RxCUI、NDC、SPL set_id），以及可用的标签日期和来源链接。
- **优先显示标签内容：**提取关键信息（如警告信息、适应症、用法用量、禁忌症、注意事项、药物相互作用和不良反应）。
- **数据标准化：**将品牌名/通用名转换为与RxCUI最匹配的标准化格式（RxNorm），同时支持NDC查询。
- **用户友好型展示：**在可用情况下提供MedlinePlus Connect的链接。
- **可选扩展功能：**包括药品召回信息、短缺情况、FAERS报告汇总、药品分类信息、DailyMed历史记录及图片、Orange Book和Purple Book数据。

## 安装理由

- 您需要将药品信息用于笔记、培训材料、质量保证（QA）或内部文档中，并希望这些信息具有可追溯性。
- 您希望快速将复杂的药品名称转换为标准化的标识符（RxCUI/NDC/set_id）。
- 您正在开发自动化系统，需要可审计和复现的JSON格式输出。
- 您关心隐私保护：该工具不存储或提供任何患者隐私信息。

## 数据来源

该工具查询以下数据源：
- **openFDA**：药品标签、NDC目录、药品召回/执法报告、短缺信息及FAERS报告。
- **RxNorm (RxNav)**：用于数据标准化（将品牌名转换为通用名）。
- **RxClass (RxNav)**：用于确定药品所属类别。
- **DailyMed**：提供药品的历史记录及图片信息（由标签发布方提供）。
- **Orange Book**：包含生物制品、生物类似药的相关信息。
- **Purple Book**：提供生物制品和生物类似药的月度数据。
- **MedlinePlus Connect**：提供用户友好的药品信息摘要。

## 安全注意事项

- 在做出临床决策时，请务必**核对官方完整标签**。本工具仅提取关键信息并返回相关参考资料。
- 该工具将所有用户输入视为不可信数据，并在构建openFDA查询时对敏感信息进行转义处理，以防止查询注入攻击。

## 示例命令

### 1) 按药品名称查询信息
```bash
cd {baseDir}
python3 scripts/med_info.py "metoprolol succinate" 
```

### 2) 按NDC查询信息
```bash
python3 scripts/med_info.py "70518-4370"     # product_ndc (example)
python3 scripts/med_info.py "70518-4370-0"   # package_ndc (example)
```

### 3) 生成JSON格式输出（适用于自动化流程）
```bash
python3 scripts/med_info.py "ibuprofen" --json
```

### 4) 在标签文本中查找关键词
```bash
python3 scripts/med_info.py "Eliquis" --find ritonavir
python3 scripts/med_info.py "metformin" --find crush --find chew
```

### 5) 解决标签歧义（选择最合适的匹配项）
```bash
# show label candidates
python3 scripts/med_info.py "metformin" --candidates

# pick the 2nd candidate
python3 scripts/med_info.py "metformin" --candidates --pick 2

# force a specific label by set_id
python3 scripts/med_info.py "05999192-ebc6-4198-bd1e-f46abbfb4f8a"  # set_id
# or
python3 scripts/med_info.py "metformin" --set-id "05999192-ebc6-4198-bd1e-f46abbfb4f8a"
```

### 6) 查看药品召回、短缺信息及FAERS报告（可选）
```bash
python3 scripts/med_info.py "metformin" --recalls
python3 scripts/med_info.py "amphetamine" --shortages
python3 scripts/med_info.py "Eliquis" --faers --faers-max 10
python3 scripts/med_info.py "Eliquis" --rxclass
```

### 7) 查看DailyMed记录及图片（可选）
```bash
python3 scripts/med_info.py "Eliquis" --dailymed
python3 scripts/med_info.py "Eliquis" --images

# Note: RxImage was retired in 2021, so --rximage is an alias for --images.
python3 scripts/med_info.py "Eliquis" --rximage
```

### 8) 获取Orange Book和Purple Book数据（可选）
```bash
python3 scripts/med_info.py "metformin" --orangebook
python3 scripts/med_info.py "adalimumab" --purplebook
```

### 9) 自定义输出格式（可选）
```bash
# only print a couple sections
python3 scripts/med_info.py "Eliquis" --sections contraindications,drug_interactions

# brief output
python3 scripts/med_info.py "Eliquis" --brief --sections all

# print redacted URLs queried
python3 scripts/med_info.py "Eliquis" --print-url --brief
```

## 返回内容

- 与RxCUI最匹配的标准化标识符（RxNorm）及药品名称。
- openFDA标签信息（包括生效时间、set_id，以及以下关键内容）：
  - 警告信息
  - 适应症和用法
  - 用法用量
  - 禁忌症
  - 注意事项和预防措施
  - 药物相互作用
  - 不良反应
- 可用的MedlinePlus Connect链接

## 环境配置（可选）

- **OPENFDA_API_KEY**：适用于高频率使用的情况，可提升openFDA的查询频率限制。

## 实施说明

- 为确保安全性，脚本设计较为保守：当存在多个匹配结果时，仅显示排名靠前的选项，并选择与RxNorm最匹配的结果。
- 建议在数据标准化后优先使用**RxCUI**进行查询，以提高查询精度。