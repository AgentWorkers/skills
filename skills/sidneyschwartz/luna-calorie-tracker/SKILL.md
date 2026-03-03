---
name: luna-calorie-tracker
description: 通过发送食物照片来记录每日的热量摄入量。Luna 使用视觉人工智能分析照片，估算热量和营养成分，并将所有数据存储在内存中，以便生成每日/每周的总结报告。
metadata: {"openclaw": {"requires": {"env": ["OPENAI_API_KEY"]}, "primaryEnv": "OPENAI_API_KEY", "emoji": "🍽️"}}
---
# Luna 卡路里追踪器技能

Luna 是一个用于追踪用户卡路里摄入量的模块。当用户发送食物图片时，它会分析图片并记录用户的营养摄入情况。

## 当用户发送食物图片时

1. **使用视觉识别功能分析图片**：
   - 识别图片中可见的所有食物；
   - 估算食物的份量（以克或毫升为单位）；
   - 计算卡路里、蛋白质（克）、碳水化合物（克）、脂肪（克）和膳食纤维（克）的摄入量；
   - 为估算结果分配一个置信度评分（0-1）。

2. **以结构化的方式回复用户**：
   ```
   🍽️ Meal Logged!
   
   📸 Items detected:
   - [Food item 1]: [portion] — [calories] kcal (P: [x]g | C: [x]g | F: [x]g)
   - [Food item 2]: [portion] — [calories] kcal (P: [x]g | C: [x]g | F: [x]g)
   
   📊 Meal Total: [total] kcal
   Protein: [x]g | Carbs: [x]g | Fat: [x]g | Fiber: [x]g
   Confidence: [score]
   
   📅 Daily Running Total: [X] kcal ([meals] meals logged today)
   ```

3. **将分析结果存储到内存中**：以以下格式追加到今天的日志文件 `memory/YYYY-MM-DD.md` 中：
   ```markdown
   ## Meal [N] — [HH:MM]
   - **Items**: [comma-separated food items]
   - **Calories**: [total] kcal
   - **Protein**: [x]g | **Carbs**: [x]g | **Fat**: [x]g | **Fiber**: [x]g
   - **Confidence**: [score]
   ```

4. **更新当天的每日总结**：在当天日志文件的顶部显示每日卡路里摄入情况：
   ```markdown
   # Daily Nutrition Log — [YYYY-MM-DD]
   **Total Calories**: [X] kcal | **Meals**: [N]
   **Protein**: [X]g | **Carbs**: [X]g | **Fat**: [X]g | **Fiber**: [X]g
   ---
   ```

## 命令行操作

当用户输入以下命令时，系统会相应地做出响应：

### /calories today
读取 `memory/YYYY-MM-DD.md` 文件，显示当天的所有餐食及其卡路里摄入量。

### /calories week
读取过去7天的 `memory/YYYY-MM-DD.md` 文件，计算每周的总摄入量、每日平均值，并以迷你条形图的形式展示每日卡路里摄入情况：
```
📊 Weekly Summary ([start] to [end])
Total: [X] kcal | Daily Avg: [X] kcal
Avg Protein: [X]g | Avg Carbs: [X]g | Avg Fat: [X]g

Mon: ████████░░ 1,850 kcal
Tue: ██████████ 2,200 kcal
Wed: ███████░░░ 1,600 kcal
...
```

### /calories goal [number]
将用户的每日卡路里目标保存到 `MEMORY.md` 文件的 `## 卡路里目标` 部分。在每日总结中显示目标达成情况（例如：“1,450 / 2,000 千卡 — 达到每日目标的 72%”）。

### /calories history [food]
在内存文件中搜索包含指定食物的记录，显示用户最后一次摄入该食物的时间、平均卡路里摄入量以及摄入频率。

### /calories undo
删除当天日志文件中最后一条记录，并更新每日总结。

## 视觉分析指南

- 估算食物份量时，以标准餐盘（约10英寸）作为参考；
- 考虑隐藏的卡路里来源（如烹饪油、酱料、黄油）；
- 对于包装食品，如果标签在图片中可见，请尽量读取相关信息；
- 如果食物种类无法确定，请说明你的假设（例如：“假设为全脂牛奶，而非脱脂牛奶”）；
- 对于餐厅餐食，建议保守估计卡路里摄入量（餐厅通常使用更多的油和黄油）；
- 如果确实无法识别食物，请让用户提供更多信息。

## 内存管理规则

- 在追加新数据之前，务必先读取当天的现有日志以获取准确的累计摄入量；
- 当用户查询历史记录时，使用 `memory_search` 功能进行查找；
- 将用户的卡路里目标保存在 `MEMORY.md` 文件中，以便在不同会话间保持一致；
- 在进行数据压缩时，确保即使部分餐食信息被汇总，每日总摄入量仍然能够被保留。