---
name: med-info
description: 从权威的开放资源（如 openFDA 药物标签/NDC、RxNorm、MedlinePlus Connect）中检索药物信息。将药物名称解析为 RxCUI/NDC 格式，并获取包含引用信息的处方标签内容。
metadata: {"clawdbot": {"emoji": "💊", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---

# med-info

该技能用于获取药物信息，并提供相关引用来源：
- **openFDA**：提供药品标签、NDC目录、药品召回信息、药品短缺情况以及FAERS不良事件报告。
- **RxNorm (RxNav API)**：用于数据标准化（包括RxCUI和品牌-通用名称的映射）。
- **RxClass (RxNav)**：用于确定药品所属的类别。
- **DailyMed**：提供SPL元数据及药品相关媒体资料（包括药品制造商提交的图片）。
- **Orange Book**：包含生物制品、生物类似药的相关数据。
- **Purple Book**：提供生物制品和生物类似药的月度数据及互换性信息。
- **MedlinePlus Connect**：提供易于患者理解的药品信息摘要。

该技能注重**准确性和可追溯性**：在条件允许的情况下，会始终报告药品的标识符和数据来源的时间戳。

## 安全规则

- 在做出临床决策时，请**根据完整的官方药品标签进行核实**。该工具仅提取关键信息并返回相关参考资料。
- 请勿输入能够识别患者的信息。在构建openFDA搜索查询时，系统会将所有用户输入视为不可信的数据，并对输入内容进行转义处理，以防止查询注入攻击等安全风险。

## 快速入门

### 1) 按药品名称查询药品信息
```bash
cd {baseDir}
python3 scripts/med_info.py "metoprolol succinate" 
```

### 2) 按NDC代码查询药品信息
```bash
python3 scripts/med_info.py "70518-4370"     # product_ndc (example)
python3 scripts/med_info.py "70518-4370-0"   # package_ndc (example)
```

### 3) 以JSON格式输出结果（适用于数据管道）
```bash
python3 scripts/med_info.py "ibuprofen" --json
```

### 4) 在药品标签文本中查找指定关键词
```bash
python3 scripts/med_info.py "Eliquis" --find ritonavir
python3 scripts/med_info.py "metformin" --find crush --find chew
```

### 5) 解决标签歧义（选择合适的药品条目）
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

### 6) 查询药品召回信息、短缺情况、FAERS不良事件及药品类别（可选）
```bash
python3 scripts/med_info.py "metformin" --recalls
python3 scripts/med_info.py "amphetamine" --shortages
python3 scripts/med_info.py "Eliquis" --faers --faers-max 10
python3 scripts/med_info.py "Eliquis" --rxclass
```

### 7) 获取DailyMed数据及药品图片（可选）
```bash
python3 scripts/med_info.py "Eliquis" --dailymed
python3 scripts/med_info.py "Eliquis" --images

# Note: RxImage was retired in 2021, so --rximage is an alias for --images.
python3 scripts/med_info.py "Eliquis" --rximage
```

### 8) 查阅Orange Book和Purple Book数据（可选）
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

## 返回结果

- **RxNorm**的匹配结果（最佳匹配的RxCUI + 药品名称）
- **openFDA**的标签信息（包括生效时间、set_id，以及以下关键内容）：
  - 警告信息
  - 适应症和用法
  - 剂量与用法
  - 禁忌症
  - 注意事项
  - 药物相互作用
  - 不良反应
- **MedlinePlus Connect**的链接（如可用）

## 环境配置（可选）

- **OPENFDA_API_KEY**：用于提升高频使用时的openFDA接口访问速率限制。

## 实施说明

- 该脚本的设计较为保守：当存在多个匹配结果时，系统会显示前几个结果，并选择评分最高的RxNorm匹配项。
- 在完成数据匹配后，建议优先使用**RxCUI**进行查询，因为这种方式更为准确。