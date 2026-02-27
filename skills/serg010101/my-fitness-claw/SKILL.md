---
name: my-fitness-claw
version: 1.6.0
description: 您的个人营养助手。只需用简单的自然语言记录您的饮食，系统会自动统计碳水化合物（P）、蛋白质（C）和脂肪（F）的摄入量，并在精美的实时仪表板上展示您的健康进展。该工具还提供基于人工智能的健康建议、常见食物的信息以及每日饮食情况的跟踪功能——所有这些都可以通过聊天界面进行控制。
requires:
  tools: [canvas, read, write, edit]
  paths: [nutrition/, canvas/, memory/]
---
# MyFitnessClaw

该技能用于管理您的营养数据，并通过 OpenClaw 的原生工具提供可视化的营养指标追踪界面。

## 核心文件（技能资源）

- `assets/nutrition/dailymacros.json`：每日摄入量的结构化记录。
- `assets/nutrition/targets.json`：每日营养目标（卡路里、蛋白质、碳水化合物、脂肪）。
- `assets/nutrition/insights.json`：基于当前进度的 AI 生成的建议。
- `assets/nutrition/foods/common.md`：常见食物的参考列表及其营养成分。
- `assets/canvas/index.html`：OpenClaw Canvas 的可视化界面。

## 工作流程：记录饮食

当用户报告摄入了某种食物时：
1. **估算营养成分**：如果用户未提供具体数据，系统会估算卡路里、蛋白质、碳水化合物和脂肪的摄入量。首先查看 `assets/nutrition/foods/common.md`。
2. **更新每日记录**：修改 `assets/nutrition/dailymacros.json`。这是数据的最权威来源。
3. **更新离线数据**：将相同的数据更新到 `assets/canvas/offline_data.js` 文件中：
   - 使用以下代码覆盖原有内容：`window.__OFFLINE_DAILY_MACROS = [...]; window.__OFFLINE_TARGETS = {...}; window.__OFFLINE_INSIGHTS = {...};`
   - 这确保了通过 `file://`（离线/浏览器优先）方式打开界面时，界面能够正常显示数据。
4. **更新内存记录**：将餐食信息记录到代理程序的每日内存文件中（例如 `memory/YYYY-MM-DD.md`）。
5. **显示界面**：使用 `canvas(action=present, url='skills/my-fitness-claw/assets/canvas/index.html')` 在 OpenClaw 中显示更新后的界面。
6. **提供浏览器访问方式**：每次记录后，显示以下提示：
   > 📊 **在浏览器中查看：**
   > - **快速方式**：在浏览器中打开 `skills/my-fitness-claw/assets/canvas/index.html`（使用离线数据）。
   > - **完整方式**：从工作区根目录运行 `python -m http.server 8000`，然后访问 `http://localhost:8000/skills/my-fitness-claw/assets/canvas/index.html`。
7. **生成分析报告**：根据 `assets/nutrition/targets.json` 中的目标分析进度，并更新 `assets/nutrition/insights.json`。

**数据持久化规则**：
- `assets/nutrition/*.json`：用于存储核心数据。
- `assets/canvas/offline_data.js`：仅用于通过 `file://` 查看数据的离线副本。
- **日常记录过程中** **禁止** 修改 `assets/canvas/index.html` 文件。

## 发布前的检查清单（公共安全）

在发布或共享此技能之前，请执行以下操作：
1. **清理数据**：将 `nutrition/dailymacros.json` 中的所有数据清空（设置为 `[]`）。
2. **清理离线数据**：将 `canvas/offline_data.js` 中的数据清空，使其恢复到初始状态：`window.__OFFLINE_DAILY_MACROS = [];`。
3. **清除分析报告**：清空 `nutrition/insights.json` 或将其重置为默认的建议内容。
4. **删除敏感信息**：从 `nutrition/targets.json` 和 `memory/` 文件中删除任何敏感信息。
5. **验证资源**：确保 `assets/` 文件夹中不存在任何私人图片或文档。