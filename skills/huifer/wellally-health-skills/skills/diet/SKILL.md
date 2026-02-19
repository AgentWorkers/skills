---
name: diet
description: Record and track daily nutrition intake through food photos. Analyze nutritional content including calories, protein, fat, carbohydrates, vitamins, and minerals. Use when user wants to log meals, track nutrition, or analyze dietary habits.
argument-hint: <operation_type image_path_or_meal_time, e.g.: add lunch.jpg 12:30>
allowed-tools: Read, Write
schema: diet/schema.json
---

# 饮食与营养追踪技能

通过照片或文件上传记录每日餐食，自动分析营养成分，并追踪营养摄入情况。

## 核心流程

```
User Input → Identify Operation Type → [add] Analyze Image → Nutrition Analysis → Save Record
                              ↓
                         [history/status/summary] → Read Data → Display Report
```

## 第一步：解析用户输入

### 操作类型识别

| 输入关键词 | 操作类型 |
|----------------|----------------|
| add       | 添加饮食记录 |
| history    | 查看历史记录 |
| status     | 营养统计 |
| summary    | 营养概览 |

### 餐食分类（根据用餐时间）

| 时间范围 | 餐食类型 |
|------------|-----------|
| 05:00 - 09:59 | 早餐 |
| 10:00 - 14:59 | 午餐 |
| 15:00 - 16:59 | 下午茶 |
| 17:00 - 21:59 | 晚餐 |
| 22:00 - 04:59 | 深夜零食 |

## 第二步：检查信息完整性

### 对于“add”操作，必需的参数：
- `image`    - 食物照片路径

### 对于“add”操作，可选的参数：
- `meal_time`  - 餐食时间（默认为当前时间）

### 对于“history/status/summary”操作：
- 无需参数，可选时间范围

## 第三步：交互式提示（如需要）

### 场景A：未提供图片
```
Please provide a food photo. You can drag and drop or specify the path.
```

### 场景B：图片路径无效
```
Cannot read the image. Please check if the path is correct.
Supported formats: JPG, PNG, WebP
```

### 场景C：时间格式无效
```
Invalid time format. Please use HH:mm or YYYY-MM-DD HH:mm format
Example: 12:30 or 2025-12-30 12:30
```

## 第四步：生成JSON数据

### 饮食记录数据结构

```json
{
  "id": "20251231123456789",
  "record_date": "2025-12-31",
  "meal_time": "12:30",
  "meal_type": "Lunch",
  "image_path": "food.jpg",
  "foods": [
    {
      "name": "Rice",
      "portion": "1 bowl (about 150g)",
      "weight_estimate": 150,
      "cooking_method": "Steamed",
      "confidence": 0.95
    }
  ],
  "nutrition": {
    "calories": {
      "value": 485,
      "unit": "kcal"
    },
    "macronutrients": {
      "protein": { "value": 15.2, "unit": "g" },
      "fat": { "value": 18.5, "unit": "g" },
      "carbohydrate": { "value": 60.3, "unit": "g" },
      "fiber": { "value": 6.2, "unit": "g" }
    },
    "vitamins": {
      "vitamin_a": { "value": 245, "unit": "μg" },
      "vitamin_c": { "value": 35, "unit": "mg" }
    },
    "minerals": {
      "calcium": { "value": 45, "unit": "mg" },
      "iron": { "value": 2.8, "unit": "mg" }
    }
  },
  "health_score": {
    "overall": 7.5,
    "balance": 8.0,
    "variety": 7.0,
    "nutrition_density": 7.5
  }
}
```

## 第五步：保存数据

1. 生成文件路径：`data/diet-records/YYYY-MM/YYYY-MM-DD_HHMM.json`
2. 如果不存在，则创建对应的月份目录
3. 保存JSON数据文件
4. 更新全局索引文件 `data/index.json`

## 执行说明

```
1. Parse user input, identify operation type
2. For add operation:
   a. Use Read tool to read image
   b. Analyze food types and portions
   c. Calculate nutritional content
   d. Save record to data/diet-records/
3. For history operation: Display diet history
4. For status operation: Display nutrition statistics
5. For summary operation: Display nutrition summary
```

## 营养参考

### 常见主食的份量
- 1碗米饭 ≈ 150克（180千卡）
- 1碗面条 ≈ 200克（220千卡）
- 1个馒头 ≈ 100克（220千卡）

### 肉类
- 猪肉 100克 ≈ 250千卡
- 鸡肉 100克 ≈ 130千卡
- 鱼类 100克 ≈ 100千卡

### 蔬菜
- 叶类蔬菜 1份 ≈ 200克（40千卡）
- 根茎类蔬菜 1份 ≈ 200克（80千卡）

## 成人每日营养推荐

### 宏量营养素
- 热量：1800-2400千卡
- 蛋白质：55-75克
- 脂肪：55-75克
- 碳水化合物：250-350克
- 膳食纤维：25-35克

### 主要维生素
- 维生素A：700-900微克
- 维生素C：100毫克
- 维生素D：10-20微克

### 主要矿物质
- 钙：800-1000毫克
- 铁：12-18毫克
- 锌：10-15毫克

更多示例，请参见 [examples.md](examples.md)。