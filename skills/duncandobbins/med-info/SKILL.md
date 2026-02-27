---
name: med-info
description: 带有引用和可追溯ID的标签支持的药物信息：RxCUI/NDC/set_id、关键标签字段、可选的召回信息/短缺情况/药物不良反应报告（FAERS）/药物相互作用信息。
metadata: {"clawdbot": {"emoji": "💊", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# med-info

**可引用的药物信息**

`med-info` 能将药物名称（或 RxCUI、NDC、SPL set_id）转换为包含 **可追溯标识符** 和 **来源链接** 的格式化摘要。

当您需要在笔记、培训、质量保证（QA）、内部文档或代理工作流程中展示药物信息时，可以使用该工具。

本工具不提供医疗建议。

## 提供的内容

- **权威来源**：通过 openFDA 和 DailyMed 获取的 FDA 药物标签信息，标识符来自 RxNorm/RxClass。
- **引用与可追溯性**：包括 RxCUI、NDC（产品/包装信息）、SPL set_id、有效期以及相关 URL。
- **您真正需要的信息**：药品的注意事项、适应症、用法用量、禁忌症、警告信息、药物相互作用以及不良反应。
- **可选的安全性补充信息**（需手动启用）：药品召回信息、短缺情况、FAERS 报告汇总、药物类别、危险药物标识、REMS 链接、Orange Book 和 Purple Book 相关内容。
- **易于自动化处理**：支持 `--json` 格式输出，方便集成到自动化流程中。

## 隐私保护

该工具不会包含任何患者的个人健康信息（PHI）。查询时仅使用药物名称或标识符。

## 快速入门

```bash
cd {baseDir}
python3 scripts/med_info.py "Eliquis" --brief
```

**常见使用场景**：

```bash
# Only the sections you care about
python3 scripts/med_info.py "Eliquis" --sections contraindications,drug_interactions --brief

# Find keyword hits in label text (fast way to answer "does the label mention X?")
python3 scripts/med_info.py "Eliquis" --find ritonavir --find CYP3A4 --find P-gp --find-max 8

# Deterministic lookups by identifier (best for reproducibility)
python3 scripts/med_info.py "70518-4370-0"   # NDC (package)
python3 scripts/med_info.py "70518-4370"     # NDC (product)
python3 scripts/med_info.py "05999192-ebc6-4198-bd1e-f46abbfb4f8a"  # SPL set_id
```

## 解决名称歧义的问题（当存在多个药物标签时）：

```bash
python3 scripts/med_info.py "metformin" --candidates
python3 scripts/med_info.py "metformin" --candidates --pick 2 --brief
python3 scripts/med_info.py "metformin" --set-id "05999192-ebc6-4198-bd1e-f46abbfb4f8a"
```

## 可选扩展功能**：

```bash
# Pharmacist-friendly output bundle
python3 scripts/med_info.py "Eliquis" --pharmacist --brief

# Safety signals and operational context (opt-in)
python3 scripts/med_info.py "metformin" --recalls --brief
python3 scripts/med_info.py "amphetamine" --shortages --brief
python3 scripts/med_info.py "Eliquis" --faers --faers-max 10
python3 scripts/med_info.py "Eliquis" --interactions --interactions-max 20
python3 scripts/med_info.py "Eliquis" --rxclass
python3 scripts/med_info.py "cyclophosphamide" --hazardous
python3 scripts/med_info.py "isotretinoin" --rems

# Reference datasets
python3 scripts/med_info.py "adalimumab" --purplebook
python3 scripts/med_info.py "metformin" --orangebook

# Chemistry (best-effort)
python3 scripts/med_info.py "ibuprofen" --chem
```

## 输出格式定制**

```bash
python3 scripts/med_info.py "ibuprofen" --json
python3 scripts/med_info.py "Eliquis" --brief --sections all
python3 scripts/med_info.py "Eliquis" --print-url --brief   # prints queried URLs (api_key redacted)
```

## 数据来源（概述）

- **openFDA**：提供药物标签信息、NDC 目录、药品召回/监管信息以及 FAERS 报告。
- **RxNorm / RxClass**：负责数据标准化和药物类别分类。
- **DailyMed**：提供药品的标签历史记录和相关媒体资料。
- **MedlinePlus Connect**：提供用户友好的药品摘要链接。
- **Orange Book 和 Purple Book**：提供相关的药品信息补充资料。

## 安全提示

- 在做出临床决策时，请务必参考官方的完整药品标签说明。
- 输入的数据被视为不可信的；openFDA 的搜索字符串会经过转义处理，以防止查询注入攻击。

## 使用说明与速率限制

无需任何密钥即可使用该工具。可选配置：
- `OPENFDA_API_KEY`：用于提升高频率使用时的 openFDA 数据访问速率限制。