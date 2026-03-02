---
name: gardening-calendar
description: Precise horticultural advice for UK and international gardening. Use when a user asks for: (1) What to plant or harvest this month, (2) Sowing/harvesting windows for specific plants, (3) UK-specific (Celsius/Allotment) advice, or (4) International gardening context (Thailand, US, Australia).
---

# 园艺日历技能 🎷

该技能为英国及全球地区的种植季节提供精确的园艺建议。它通过一个包含160多种植物的数据库，来确定室内播种、室外播种以及收获的最佳时机。

## 核心功能

1. **“立即种植”报告**：生成当前月份可以播种（室内/室外）或收获的植物列表。
2. **植物种植指南**：为特定植物（如番茄、胡萝卜等）提供详细的种植建议，包括土壤要求、种植间距和维护技巧。
3. **地区适应性**：根据用户所在地区（英国、美国、泰国、澳大利亚）调整种植建议。
4. **园艺日志记录**：采用“SowTimes”风格的写作方式——简洁明了且专注于英国的园艺实践。

## 工作流程

### 第1阶段：收集信息
查看当前月份和用户所在地区。如未指定，默认为**英国/三月**。

### 第2阶段：应用逻辑
使用 `scripts/calendar-logic.ts` 脚本计算植物的生长状态：
- **立即播种**：当前处于播种期（优先考虑室内播种）。
- **立即收获**：当前处于收获期。
- **提前规划**：播种期将在1-2个月内到来。

### 第3阶段：生成报告
报告结构如下：
- ### 🚜 立即播种（室内）
- ### 🌱 立即播种（室外）
- ### 🧺 立即收获
- ### 🧠 专业技巧

## 文风指南
- **专业且通俗易懂**：以英国园艺爱好者的口吻撰写。
- **数据精确**：使用摄氏度（℃）和英国常用的度量单位。
- **简洁直接**：避免使用“可持续性”等流行词汇，重点关注植物的生长效率和健康状况。
- **语气**：提供实用建议，同时带有一点幽默感（Andre的写作风格）。

## 资源
- `scripts/calendar-logic.ts`：用于计算播种/收获时机的核心逻辑代码。
- `references/plant-database.md`：包含所有植物ID及其生长季节数据的完整列表。（即将发布）