---
name: nutrition-tracker
description: 在 Obsidian 中记录每日摄入的卡路里和营养成分（宏量营养素），支持用户设置个人资料（性别、身高、体重、目标），并具备基于目标的自动检查功能。该工具支持多语言（中文/英文）。用户可以记录饮食摄入情况，查询是否达到营养目标，或调整/保存自己的营养计划。
---
# 营养追踪器（Obsidian）

该工具可将餐食信息（热量、蛋白质、碳水化合物、脂肪含量）记录到 Obsidian 文档系统中，并统计每日摄入总量。同时，它还会存储用户的营养信息（性别、身高、体重、活动水平及健康目标），并能够判断当天的摄入量是否达到目标。

> i18n: 脚本支持 `--lang zh-CN|en-US`（默认值：`zh-CN`）。

## 存储设置

- 文档存储路径（默认）：`~/Documents/obsidian/yzhai-daily`
- 用户资料文件：`health/eat/profile.json`
- 每月饮食记录文件：`health/eat/YYYY-MM/YYYYMM_calories_macros.md`

## 快速入门

### 1) 初始化/更新用户资料

```bash
bash ~/.openclaw/workspace/skills-public/nutrition-tracker/scripts/nutrition_init.sh \
  --sex male \
  --height 175 \
  --weight 75 \
  --activity office \
  --goal cut \
  --kcal 2200 \
  --lang zh-CN
```

### 2) 记录餐食信息

```bash
bash ~/.openclaw/workspace/skills-public/nutrition-tracker/scripts/nutrition_log.sh \
  --date "2026-03-04" --time "19:54" --meal dinner \
  --desc "rice 150g; potato 120g; meat+egg 200g; soup 200g" \
  --kcal 830 --p 45 --c 69 --f 40 \
  --lang zh-CN
```

### 3) 检查当天是否达到目标

```bash
bash ~/.openclaw/workspace/skills-public/nutrition-tracker/scripts/nutrition_check_today.sh \
  --date "2026-03-04" \
  --lang zh-CN
```

## 目标设定规则（默认值）

如果用户资料中没有明确设定营养目标，系统会根据用户的健康目标自动计算默认值：

- **减脂**：
  - 蛋白质：2.0 克/千克体重
  - 脂肪：0.8 克/千克体重
  - 碳水化合物：剩余热量（根据总热量目标计算）

用户可以在用户资料文件中手动修改这些目标（使用命令 `nutrition_init.sh --pTarget/--cTarget/--fTarget`）。

## 注意事项

- 餐食中的营养成分数据仅供参考，建议通过后续更新记录来修正这些数值。
- 该工具主要通过脚本进行自动化操作，不支持自由形式的编辑。