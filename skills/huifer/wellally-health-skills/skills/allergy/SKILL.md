---
name: allergy
description: 管理过敏记录，包括药物过敏、食物过敏和环境过敏，并支持过敏严重程度的跟踪以及与医疗警报系统的集成。
argument-hint: <operation_type(add/list/update/delete) allergy_information_natural_language_description>
allowed-tools: Read, Write
schema: allergy/schema.json
---
# 过敏史管理功能

该功能用于记录和管理过敏史，包括药物过敏、食物过敏、环境过敏等，并提供快速查询和更新的支持。

## 核心流程

```
User Input -> Parse Operation Type -> [add] Parse Allergy Info -> Medical Standardization -> Generate JSON -> Save
                             -> [list] Filter and Display
                             -> [update] Find and Update -> Save
                             -> [delete] Confirm Deletion
```

## 第一步：解析用户输入

### 操作类型识别

| 输入关键词 | 操作类型 |
|----------------|-----------|
| add     | 添加       |
| list    | 列出       |
| update   | 更新       |
| delete   | 删除       |

## 第二步：添加过敏记录（add）

### 过敏信息解析

从用户输入的自然语言中提取以下信息：

**基本信息（自动提取）：**
- **过敏原名称**：引起过敏的具体物质名称
- **过敏类型**：药物过敏、食物过敏、环境过敏或其他
- **严重程度**：轻微、中度、重度、过敏性休克
- **反应症状**：具体的过敏反应表现

**详细信息（可选输入）：**
- **发现时间**：首次发现过敏的时间
- **发现情境**：发现过敏时的环境和情况
- **确认方式**：医生诊断、自我观察或检测确认
- **当前状态**：是否仍然过敏或已痊愈

### 医学术语标准化转换

| 非专业术语 | 医学术语 | 类型       |
|------------|-----------|-----------|
| 青霉素     | Penicillin    | 药物过敏     |
| 花生       | Peanut      | 食物过敏     |
| 花粉       | Pollen      | 环境过敏     |
| 碘造影剂    | Iodine contrast | 药物过敏     |
| 蜜蜂毒液     | Hymenoptera venom | 其他过敏     |

### 过敏类型分类

- **药物过敏**：抗生素（青霉素、头孢菌素等）、止痛药（阿司匹林等）、造影剂、疫苗、中药等
- **食物过敏**：海鲜（虾、蟹、贝类）、坚果（花生、核桃）、鸡蛋、乳制品、麸质、水果等
- **环境过敏**：花粉、尘螨、动物皮屑、霉菌、乳胶等
- **其他过敏**：昆虫叮咬、化学物质、金属等

### 自动判断过敏严重程度

- **关键词映射**：
  - “休克”、“过敏性休克”、“昏迷”、“意识丧失” → 严重程度4级（过敏性休克）
  - “严重”、“全身性反应”、“无法忍受”、“血压下降” → 严重程度3级（重度）
  - “明显”、“中度”、“需要治疗”、“肿胀” → 严重程度2级（中度）
  - “轻微”、“偶尔发生”、“局部反应” → 严重程度1级（轻微）

### 识别过敏反应症状

- **皮肤症状**：皮疹、荨麻疹、瘙痒、发红
- **呼吸系统症状**：呼吸困难、喘息、喉头水肿、胸闷
- **消化系统症状**：恶心、呕吐、腹泻、腹痛
- **全身性症状**：休克、血压下降、晕厥、全身性荨麻疹

## 第三步：生成JSON格式的数据

```json
{
  "allergies": [
    {
      "id": "allergy_20251231123456789",
      "allergen": {
        "name": "Penicillin",
        "type": "drug",
        "type_category": "Drug allergy",
        "synonyms": ["Penicillin", "盘尼西林"]
      },
      "severity": {
        "level": "severe",
        "level_code": 3,
        "description": "Severe allergic reaction"
      },
      "reactions": [
        {
          "reaction": "Rash",
          "onset_time": "Within 30 minutes of exposure",
          "severity": "moderate"
        }
      ],
      "discovery": {
        "date": "2010-05-15",
        "age_at_discovery": "8 years old",
        "circumstances": "Appeared after penicillin injection during pneumonia treatment"
      },
      "confirmation": {
        "method": "doctor_confirmed",
        "method_name": "Doctor diagnosis",
        "confirmed_by": "XX Hospital Pediatrics"
      },
      "current_status": {
        "status": "active",
        "status_name": "Active"
      },
      "management": {
        "avoidance_strategy": "Strictly avoid penicillin-class medications",
        "emergency_plan": "Seek immediate medical attention if accidentally used, carry allergy information",
        "medical_alert": true
      },
      "notes": "Must proactively inform medical staff during all medical visits"
    }
  ]
}
```

## 第四步：保存数据

数据文件路径：`data/allergies.json`

## 第五步：查看过敏记录（list）

**过滤参数：**
- 无参数：显示所有过敏记录
- `active`：仅显示活跃的过敏记录
- `drug`：仅显示药物过敏记录
- `food`：仅显示食物过敏记录
- `severe`：仅显示严重程度为3级及以上的过敏记录

## 第六步：更新/删除过敏记录

**可修改的字段：**
- `severity`：过敏严重程度（轻微/中度/重度/过敏性休克）
- `status`：过敏记录的当前状态（活跃/已痊愈）
- `notes`：过敏记录的备注信息

## 执行说明

```
1. Parse operation type (add/list/update/delete)
2. [add] Parse allergy info, medical standardization, generate JSON, save
3. [list] Read allergies.json, filter and display
4. [update] Find allergen, update fields, save
5. [delete] Confirm deletion, remove record
```

## 示例交互流程

### 添加过敏记录
```
User: Penicillin severe allergy from childhood injection caused difficulty breathing
-> Save drug allergy record, severity level 3
```

### 查看所有过敏记录
```
User: View all allergies
-> Display all allergy records grouped by type
```

### 查看严重过敏记录
```
User: View severe allergies
-> Display only level 3 and above allergy records
```

### 更新过敏记录的状态
```
User: Peanut status changed to resolved
-> Update current status to resolved
```

### 删除过敏记录
```
User: Delete penicillin allergy
-> Confirm then delete record
```