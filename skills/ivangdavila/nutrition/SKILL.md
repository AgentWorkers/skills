---
name: Nutrition
description: 构建一个个人营养管理系统，用于记录饮食、摄入的卡路里、宏量营养素（碳水化合物、蛋白质、脂肪）、维生素和矿物质。
metadata: {"clawdbot":{"emoji":"🥗","os":["linux","darwin","win32"]}}
---

## 核心功能
- 用户记录饮食后，系统会计算并存储营养数据。
- 当用户查询营养信息时，系统会显示各项营养素的总量及不足之处。
- 用户长期跟踪饮食数据后，系统可以展示营养摄入的规律和进步情况。
- 系统会创建一个名为 `~/nutrition/` 的工作文件夹用于存储所有相关数据。

## 文件结构
```
~/nutrition/
├── daily/
│   └── 2024-02/
│       ├── 2024-02-10.md
│       └── 2024-02-11.md
├── foods/
│   └── common.md
├── targets.md
├── supplements.md
└── insights.md
```

## 每日饮食记录
```markdown
# 2024-02-11.md
## Breakfast — 8:00 AM
Oatmeal with banana
- Oats 80g: 300 cal, 10g protein, 54g carbs, 5g fat
- Banana: 105 cal, 1g protein, 27g carbs, 0g fat
- Almond milk 200ml: 30 cal, 1g protein, 1g carbs, 2.5g fat

## Lunch — 1:00 PM
Chicken salad
- Chicken breast 150g: 165 cal, 31g protein, 0g carbs, 3.6g fat
- Mixed greens 100g: 20 cal, 2g protein, 3g carbs, 0g fat
- Olive oil 15ml: 120 cal, 0g protein, 0g carbs, 14g fat

## Dinner — 7:30 PM
Salmon with vegetables
- Salmon 200g: 400 cal, 40g protein, 0g carbs, 25g fat
- Broccoli 150g: 50 cal, 4g protein, 10g carbs, 0.5g fat

## Snacks
- Apple: 95 cal, 0g protein, 25g carbs, 0g fat
- Greek yogurt 150g: 100 cal, 17g protein, 6g carbs, 0.7g fat

## Daily Totals
Calories: 1,385
Protein: 106g | Carbs: 126g | Fat: 51g

## Micronutrients Notable
- Vitamin D: salmon (high)
- Potassium: banana, salmon
- Vitamin C: broccoli
- Omega-3: salmon (high)
```

## 营养目标
```markdown
# targets.md
## Daily Goals
Calories: 2,000
Protein: 150g
Carbs: 200g
Fat: 65g

## Micronutrient Focus
- Vitamin D: 600 IU (often low)
- Iron: 8mg
- Omega-3: 1,000mg

## Notes
Higher protein for muscle building
Limiting added sugars to 25g
```

## 常见食物参考表
```markdown
# foods/common.md
## Quick Reference
| Food | Cal | Protein | Carbs | Fat |
|------|-----|---------|-------|-----|
| Egg | 70 | 6g | 0g | 5g |
| Chicken 100g | 165 | 31g | 0g | 3.6g |
| Rice 100g cooked | 130 | 2.7g | 28g | 0.3g |
| Banana | 105 | 1g | 27g | 0g |

## Micronutrient Stars
- Vitamin D: salmon, eggs, fortified milk
- Iron: red meat, spinach, lentils
- Vitamin C: citrus, peppers, broccoli
- Potassium: bananas, potatoes, salmon
- Omega-3: salmon, sardines, walnuts
```

## 补充剂信息
```markdown
# supplements.md
## Daily
- Vitamin D3: 2000 IU (morning)
- Omega-3: 1000mg (with food)

## As Needed
- Magnesium: before bed if needed
```

## 营养建议
```markdown
# insights.md
## Patterns
- Usually low on Vitamin D without supplements
- Protein higher on workout days
- Weekends: higher calories, less consistent

## Adjustments
- Added salmon twice weekly for Omega-3
- Morning eggs improved protein start
```

## 显示的信息示例：
- “您今天已经摄入了80克蛋白质，还差70克。”
- “今天维生素D摄入不足——建议多吃三文鱼或鸡蛋。”
- “本周平均热量摄入为1900卡路里，低于目标值。”
- “本周铁摄入量偏低——建议多吃菠菜或红肉。”

## 饮食记录流程：
- 当用户描述所吃的食物时：
  - 如果没有指定食物分量，系统会自动估算。
  - 系统会计算食物中的宏量营养素和总热量。
  - 会标记出特别重要的微量营养素。
  - 系统会将这些信息记录到每日饮食日志中。

## 需要跟踪的内容：
- 每餐的热量和宏量营养素摄入量。
- 特别重要的微量营养素摄入情况。
- 摄入的补充剂种类。
- 长期饮食数据中的营养摄入规律。

## 功能升级计划：
- 初始阶段：仅记录饮食及所含的宏量营养素。
- 逐步增加微量营养素的监测功能。
- 开始跟踪用户所服用的补充剂。
- 编制常见食物的参考列表。

## 需要避免的行为：
- 过分追求营养素摄入的精确度（克数）。
- 对用户的饮食选择进行评判。
- 强制用户遵循严格的饮食规定。
- 忽视所有数据都是估算的事实。