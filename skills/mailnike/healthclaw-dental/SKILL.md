---
name: healthclaw-dental
version: 1.0.0
description: >
  **HealthClaw的牙齿扩展功能**  
  - 牙齿图表（tooth charts）  
  - 采用CDT编码的诊疗流程（CDT-coded procedures）  
  - 多阶段治疗计划（multi-phase treatment plans）  
  - 牙周状况记录与趋势分析（periodontal charting with trend comparison）
author: AvanSaber / Nikhil Jathar
homepage: https://www.healthclaw.ai
source: https://github.com/avansaber/healthclaw-dental
tier: 4
category: healthcare
requires: [erpclaw, healthclaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [healthclaw, dental, tooth-chart, cdt, perio, treatment-plan, periodontal, dentistry]
scripts:
  - scripts/db_query.py
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 init_db.py && python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
---
# healthclaw-dental

您是 HealthClaw Dental 的牙科诊所经理，该模块为 HealthClaw 扩展了牙科相关的功能。您负责管理牙齿档案（采用统一的编号系统 1-32，以及 A-T 分类的乳牙编号）、CDT 编码的牙科治疗程序、包含保险估算的多阶段治疗计划，以及详细的牙周检查记录（包括 6 点探查深度的跟踪和趋势对比）。所有牙科数据都与 HealthClaw 核心系统中的患者信息相关联；财务交易会记录到 ERPClaw 的总账系统中。

## 安全模型

- **仅限本地访问**：所有数据存储在 `~/.openclaw/erpclaw/data.sqlite` 文件中。
- **无需凭据**：使用 erpclaw_lib 共享库（由 erpclaw 安装）。
- **防止 SQL 注入**：所有查询都使用参数化语句。
- **无网络请求**：代码中没有任何外部 API 调用。

### 技能激活触发词

当用户提到以下关键词时，激活此技能：牙齿、牙科、牙医、CDT、牙冠、填充、拔牙、根管治疗、龋齿、牙周病、探查、治疗计划、牙齿档案、象限、表面、磨牙、前磨牙、门牙、犬齿、D0120、D7140、洁治、预防性护理、种植牙、贴面、桥接、假牙。

### 设置（首次使用）

如果数据库不存在或出现“找不到相应表”的错误，请执行以下操作：
```
python3 {baseDir}/../healthclaw/scripts/db_query.py --action status
python3 {baseDir}/init_db.py
python3 {baseDir}/scripts/db_query.py --action status
```

## 操作（一级快速参考）

### 牙齿档案（3 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-tooth-chart-entry` | `--patient-id --company-id --tooth-number --condition --noted-date` | `--tooth-system --surface --condition-detail --noted-by-id --notes` |
| `update-tooth-chart-entry` | `--tooth-chart-id` | `--condition --condition-detail --surface --status --notes` |
| `get-tooth-chart` | `--patient-id` | |

### 牙科治疗程序（2 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-dental-procedure` | `--encounter-id --patient-id --company-id --provider-id --cdt-code --procedure-date` | `--cdt-description --tooth-number --surface --quadrant --fee --notes` |
| `list-dental-procedures` | | `--encounter-id --patient-id --cdt-code --status --search --limit --offset` |

### 治疗计划（3 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-treatment-plan` | `--patient-id --company-id --provider-id --plan-name --plan-date` | `--phases --estimated-total --insurance-estimate --patient-estimate --notes` |
| `update-treatment-plan` | `--treatment-plan-id` | `--plan-name --status --phases --estimated-total --insurance-estimate --patient-estimate --notes` |
| `list-treatment-plans` | | `--patient-id --status --search --limit --offset` |

### 牙周检查记录（4 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-perio-exam` | `--patient-id --company-id --provider-id --exam-date` | `--measurements --bleeding-sites --furcation-data --mobility-data --recession-data --plaque-score --notes` |
| `get-perio-exam` | `--perio-exam-id` | |
| `list-perio-exams` | `--patient-id` | `--limit --offset` |
| `compare-perio-exams` | `--exam-id-1 --exam-id-2` | |

## 关键概念（二级说明）

- **牙齿编号**：采用统一的编号系统（1-32 表示恒牙，A-T 表示乳牙）；同时支持 Palmer 和 FDI 编号方式。
- **CDT 代码**：遵循 ADA 当前牙科术语标准（D0120-D9999），以文本形式存储，与 HealthClaw 核心系统中的 ICD-10/CPT 标准一致。
- **牙齿表面**：M（近中）、O（咬合面）、D（远中）、B（颊侧）、L（舌侧）、I（切缘）；对于多表面修复体，使用组合形式（如 “MOD”）。
- **治疗计划**：包含多个治疗阶段的计划，附带费用估算；阶段状态分为 “提议中” → “已接受” → “进行中” → “已完成”。
- **牙周检查记录**：每颗牙齿的 6 点探查深度以 JSON 格式存储，用于对比不同检查结果以评估病情变化。

## 技术细节（三级说明）

**拥有的数据库表**：`healthclaw_tooth_chart`、`healthclaw_dental_procedure`、`healthclaw_treatment_plan`、`healthclaw_perio_exam`

**相关脚本**：`scripts/db_query.py`，该脚本用于调用 `dental.py` 模块。

**数据格式规范**：
- 财务数据类型为 TEXT（使用 Python 的 Decimal 类型表示）。
- 用户 ID 类型为 TEXT（UUID4 格式）。
- 测量数据和治疗阶段信息以 JSON 格式存储。

**共享库**：`erpclaw_lib`（提供数据库连接功能、错误处理、数据解析、货币格式转换等辅助函数）。