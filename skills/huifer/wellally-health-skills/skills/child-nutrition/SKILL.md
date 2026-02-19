---
name: child-nutrition
description: Track child diet, nutrition assessment, picky eating management, and dietary advice. Use when user mentions child eating, meals, nutrition, vitamins, or feeding issues.
argument-hint: <operation_type: record/pickyeater/growth/deficiency/advice/history, e.g.: record breakfast milk eggs, pickyeater, deficiency, advice>
allowed-tools: Read, Write
schema: child-nutrition/schema.json
---

# 儿童营养评估技能

本技能包括儿童饮食记录、营养评估以及挑食行为的管理，同时提供针对不同年龄段的营养需求和饮食建议。

## 核心流程

```
User Input → Identify Operation Type → Read Child Information → Determine Nutritional Needs by Age → Generate Assessment Report → Save Data
```

## 第一步：解析用户输入

### 操作类型映射

| 输入 | 操作 | 说明 |
|------|--------|-------------|
| record | 记录饮食 | 录入儿童的饮食信息 |
| pickyeater | 挑食评估 | 对儿童的挑食行为进行评估 |
| growth | 生长评估 | 进行儿童生长相关的营养评估 |
| deficiency | 营养缺乏筛查 | 筛查是否存在营养缺乏 |
| advice | 饮食建议 | 提供相应的饮食建议 |
| history | 历史记录 | 查看儿童的营养记录 |

### 食物类别识别

| 关键词 | 对应类别 |
|----------|----------|
| rice, noodles, bread, porridge | 谷物 |
| beef, pork, chicken, fish, eggs | 蛋白质来源 |
| milk, yogurt, cheese | 乳制品 |
| vegetables | 蔬菜 |
| apple, banana, orange, pear | 水果 |
| nuts | 坚果 |

## 第二步：检查信息完整性

### record 操作：
- 饮食信息（可从用户输入中获取）

### 其他操作：
- 仅需要儿童的基本信息

## 第三步：根据年龄确定营养需求

| 年龄 | 每日能量（千卡） | 每日蛋白质（克） | 每日钙（毫克） | 每日铁（毫克） |
|-----|------------------|----------------|-----------------|--------------|
| 1-3岁 | 1000-1400 | 25-30 | 600 | 9 |
| 4-6岁 | 1400-1600 | 30-35 | 800 | 10 |
| 7-10岁 | 1600-2000 | 35-40 | 1000 | 13 |
| 11-14岁 | 2000-2500 | 50-60 | 1200 | 15-18（男性）/12-15（女性） |

## 第四步：生成评估报告

### 营养状况评估

| 评估项目 | 标准 |
|----------------|----------|
| 能量摄入 | 80-120%的推荐摄入量为正常 |
| 蛋白质 | 来源应包括牛奶、鸡蛋、肉类 |
| 钙 | 每日应摄入乳制品 |
| 铁 | 每日应摄入红肉或动物肝脏 |
| 维生素C | 每日应摄入水果和蔬菜 |

### 饮食记录报告示例：
```
Diet record saved

Diet Information:
Child: Xiaoming
Age: 2 years 5 months
Record date: January 14, 2025

Today's Diet:

Breakfast (08:00):
  Milk 200ml
  Egg 1
  Bread 1 slice
  Apple half

Lunch (12:00):
  Rice 1 small bowl
  Vegetables moderate
  Chicken 50g
  Tomato scrambled eggs

Dinner (18:00):
  Noodles 1 small bowl
  Tomato beef
  Cucumber

Nutrition Assessment:
  Energy intake: Adequate
  Protein: Adequate (milk, eggs, meat)
  Calcium: Adequate (dairy)
  Iron: Adequate (meat, eggs)
  Vitamin C: Adequate (fruits, vegetables)
  Dietary fiber: Adequate (vegetables, fruits)

Water Intake:
  Today's water: ~800ml
  Recommended: 1000-1300ml/day
  Assessment: Basically adequate

Overall Evaluation:
  Balanced diet, adequate nutrition

Recommendations:
  Continue current eating habits
  Increase water intake appropriately

Data saved
```

## 第五步：保存数据

将数据保存到 `data/child-nutrition-tracker.json` 文件中，内容包括：
- `child_profile`：儿童的基本信息
- `dietary_records`：饮食记录
- `picky_eating`：挑食情况
- `nutritional_assessment`：营养评估结果
- `statistics`：统计信息

## 挑食行为评估标准

| 挑食程度 | 表现 |
|---------------------|-----------|
| 无 | 可接受所有类型的食物 |
| 轻微 | 拒绝1-2种食物 |
| 中度 | 拒绝3-5种食物，影响营养摄入 |
| 严重 | 拒绝超过5种食物，严重影响营养状况 |

## 营养缺乏症状

### 铁缺乏
- 面色苍白 |
- 食欲不振 |
- 容易疲劳 |
- 注意力不集中 |
- 异食癖（吃非食物物品）

### 钙缺乏
- 夜间磨牙 |
- 出汗过多 |
- 夜惊 |
- 生长迟缓 |
- 多发性龋齿

### 维生素D缺乏
- 后脑勺头发稀疏 |
- 夜惊/出汗过多 |
- 出牙延迟 |
- 头骨呈方形或鸡胸 |
- O型腿/X型腿

### 锌缺乏
- 食欲不振 |
- 味觉减退 |
- 伤口愈合缓慢 |
- 指甲上有白色斑点 |
- 免疫力低下

## 不同年龄段的营养重点

### 1-3岁（幼儿期）
- 每日牛奶摄入量：400-500毫升 |
- 三餐定时 |
- 两餐加零食 |
- 逐渐过渡到固体食物

### 3-6岁（学龄前）
- 每日牛奶摄入量：300-400毫升 |
- 三餐定时 |
- 一餐加零食 |
- 注意饮食多样化，避免挑食

### 6-12岁（学龄期）
- 每日牛奶摄入量：300毫升 |
- 三餐定时 |
- 一餐加零食 |
- 早餐非常重要，确保营养均衡

## 常见营养来源

| 营养素 | 来源 |
|----------|---------|
| 蛋白质 | 肉类、鱼类、鸡蛋、牛奶、豆类 |
| 钙 | 乳制品、豆制品、绿叶蔬菜 |
| 铁 | 红肉、动物肝脏 |
| 锌 | 海鲜、瘦肉、坚果 |
| 维生素A | 动物肝脏、胡萝卜、深色蔬菜 |
| 维生素C | 柑橘类水果、猕猴桃、甜椒 |
| 维生素D | 阳光、鱼肝油、强化食品 |
| 膳食纤维 | 全谷物、蔬菜、水果 |

## 执行说明

1. 读取 `data/profile.json` 文件中的儿童信息。
2. 根据年龄确定儿童的营养需求。
3. 分析饮食信息并生成相应的饮食建议。
4. 将结果保存到 `data/child-nutrition-tracker.json` 文件中。

## 医学安全原则

### 安全注意事项
- 本系统仅用于记录和参考营养信息，不能替代专业的营养评估和诊断。
- 本系统不提供任何营养补充剂的推荐或处方。
- 本系统不处理严重的营养缺乏问题。

### 系统功能
- 记录和跟踪儿童的饮食情况
- 评估营养摄入情况
- 提供挑食行为的管理建议
- 筛查营养缺乏问题
- 提供营养建议的教育内容

## 重要提示

本系统仅用于记录饮食和提供营养参考，**不能替代专业的营养评估和诊断**。

如果出现以下情况，请咨询儿科医生或营养师：
- 生长迟缓 |
- 显著的体重过轻或过重 |
- 挑食行为严重影响生长 |
- 出现疑似营养缺乏的症状