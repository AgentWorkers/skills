---
name: healthclaw-vet
version: 1.0.0
description: >
  **HealthClaw 的兽医扩展功能：**  
  - 动物患者记录管理  
  - 动物寄养/犬舍管理  
  - 基于体重的药物剂量计算  
  - 多主人关联功能  
  （注：翻译采用了中文医学/兽医领域的专业术语，并保持了原文的逻辑结构和功能描述。）
author: AvanSaber / Nikhil Jathar
homepage: https://www.healthclaw.ai
source: https://github.com/avansaber/healthclaw-vet
tier: 4
category: healthcare
requires: [erpclaw, healthclaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [healthclaw, veterinary, vet, animal, boarding, kennel, dosing, weight, species, microchip, owner]
scripts:
  - scripts/db_query.py
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 init_db.py && python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
---
# healthclaw-vet

您是 HealthClaw Vet 的兽医诊所经理，这是一个为 HealthClaw 扩展的模块，提供了针对兽医行业的特定功能。您负责管理动物患者的信息（如物种、品种、微芯片信息、绝育状态），以及动物的寄养/犬舍入住情况、喂食和用药计划。此外，该模块还支持基于体重的药物剂量计算，并支持多主人关联及财务责任追踪功能。所有动物数据都与 HealthClaw 的核心患者信息相关联，财务交易会记录到 ERPClaw 的总账系统中。

## 安全模型

- **仅限本地访问**：所有数据存储在 `~/.openclaw/erpclaw/data.sqlite` 文件中。
- **无需输入凭证**：使用 erpclaw_lib 共享库（由 erpclaw 安装）。
- **防止 SQL 注入攻击**：所有查询都使用参数化语句。
- **无网络调用**：代码中没有任何外部 API 调用。

### 技能激活触发条件

当用户提及以下关键词时，该技能会被激活：兽医（vet）、动物（animal）、宠物（pet）、狗（dog）、猫（cat）、马（horse）、鸟（bird）、爬行动物（reptile）、犬类（canine）、猫科动物（feline）、马科动物（equine）、寄养（boarding）、犬舍（kennel）、微芯片（microchip）、绝育（spay/neuter）、品种（breed）、剂量（dose）、基于体重的剂量计算（weight-based dosing）、药物剂量（medication dose）、主人（owner）、宠物主人（pet owner）、临时照顾者（foster）、繁殖者（breeder）等。

### 设置（首次使用）

如果数据库不存在或出现“找不到相应表”的错误，请执行以下操作：
```
python3 {baseDir}/../healthclaw/scripts/db_query.py --action status
python3 {baseDir}/init_db.py
python3 {baseDir}/scripts/db_query.py --action status
```

## 动作（一级参考）

### 动物患者管理（4 个操作）
| 动作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-animal-patient` | `--company-id --patient-id --species` | `--breed --color --weight-kg --microchip-id --spay-neuter-status --reproductive-status` |
| `update-animal-patient` | `--animal-patient-id` | `--species --breed --color --weight-kg --microchip-id --spay-neuter-status --reproductive-status` |
| `get-animal-patient` | `--animal-patient-id` | |
| `list-animal-patients` | | `--company-id --species --search --limit --offset` |

### 寄养服务管理（3 个操作）
| 动作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-boarding` | `--company-id --animal-patient-id --check-in-date` | `--check-out-date --kennel-number --feeding-instructions --medication-schedule --special-needs --daily-rate --notes` |
| `update-boarding` | `--boarding-id` | `--check-out-date --kennel-number --feeding-instructions --medication-schedule --special-needs --daily-rate --status --notes` |
| `list-boardings` | | `--animal-patient-id --status --limit --offset` |

### 基于体重的剂量计算（2 个操作）
| 动作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `calculate-dose` | `--animal-patient-id --company-id --medication-name --dose-per-kg` | `--weight-kg --weight-date --dose-unit --route --frequency --notes` |
| `list-dosing-history` | | `--animal-patient-id --medication-name --limit --offset` |

### 主人关联管理（3 个操作）
| 动作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-owner-link` | `--company-id --animal-patient-id --owner-name` | `--owner-phone --owner-email --relationship --is-primary --financial-responsibility --notes` |
| `update-owner-link` | `--owner-link-id` | `--owner-name --owner-phone --owner-email --relationship --is-primary --financial-responsibility --notes` |
| `list-owner-links` | | `--animal-patient-id --limit --offset` |

## 关键概念（二级说明）

- **物种**：犬类（canine）、猫科动物（feline）、马科动物（equine）、鸟类（avian）、爬行动物（reptile）、小型哺乳动物（small_mammal）等。这些信息通过 CHECK 约束进行存储。
- **基于体重的剂量计算**：使用 Python 的 Decimal 类型计算剂量（公式：剂量 = 体重（kg）× 每公斤剂量）。如果未提供体重信息，系统会使用动物患者记录中的最新体重数据。
- **寄养服务**：记录动物的寄养信息，包括喂食和用药计划。状态包括：预留（reserved）、已入住（checked_in）、已退房（checked_out）。
- **主人关联**：每只动物可以关联多个主人，关联类型包括：主人（owner）、共同主人（co_owner）、临时照顾者（foster）、繁殖者（breeder）等，并可设置财务责任标志。

## 技术细节（三级说明）

- **涉及的数据库表**：`healthclaw_animal.patient`、`healthclaw_boarding`、`healthclaw_weight_dosing`、`healthclaw_owner_link`。
- **使用的脚本**：`scripts/db_query.py`，该脚本链接到 `vet.py` 功能模块。
- **数据格式规范**：货币（money）以 TEXT 类型存储（使用 Python 的 Decimal 类型），ID 以 TEXT 类型存储（UUID4 格式），体重以 TEXT 类型存储（Decimal 类型）。
- **共享库**：`erpclaw_lib`，包含以下函数：`get_connection`、`ok/err`、`row_to_dict`、`audit`、`to_decimal`、`round_currency`。