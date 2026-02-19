---
name: my-fitness-claw
description: 您的个人营养助手。只需用简单的自然语言记录您的饮食，系统会自动统计碳水化合物（P）、蛋白质（C）和脂肪（F）的摄入量，并在精美的实时仪表板上展示您的健康进展。该工具还提供基于人工智能的健康建议、常见食物的信息以及每日饮食情况的跟踪功能——所有这些都可以通过聊天界面进行控制。
requires:
  tools: [canvas, read, write, edit]
  paths: [nutrition/, canvas/, memory/]
---
# MyFitnessClaw

该技能用于管理您的营养数据，并通过 OpenClaw 的原生工具提供可视化仪表板来跟踪您的每日营养摄入情况。

## 核心文件

- `nutrition/dailymacros.json`：记录每日营养摄入情况的结构化日志。
- `nutrition/targets.json`：每日营养目标（卡路里、蛋白质、碳水化合物、脂肪）。
- `nutrition/insights.json`：基于当前进度的 AI 生成的营养建议。
- `nutrition/foods/common.md`：常见食物的参考列表及其营养成分。
- `canvas/index.html`：OpenClaw Canvas 的可视化仪表板。

## 工作流程：记录食物摄入

当用户表示吃了某种食物时：
1. **估算营养成分**：如果用户未提供具体数据，系统会估算卡路里、蛋白质、碳水化合物和脂肪的摄入量。请先查看 `nutrition/foods/common.md` 文件。
2. **更新每日日志**：将相关数据添加到 `nutrition/dailymacros.json` 文件中。
3. **更新记忆记录**：使用 `write` 或 `edit` 工具将餐食信息记录到代理程序的当前每日记忆文件中（例如 `memory/YYYY-MM-DD.md`）。
4. **更新仪表板**：
   - 从 `nutrition/dailymacros.json`、`nutrition/targets.json` 和 `nutrition/insights.json` 中读取最新数据。
   - 使用 `edit` 工具更新 `canvas/index.html` 中的以下变量：
     - `const fallbackData`：用 `dailymacros.json` 中的完整数据数组进行更新。
     - `const fallbackGoals`：用 `targets.json` 中的完整 JSON 对象进行更新。
     - `const fallbackInsights`：用 `insights.json` 中的完整 JSON 对象进行更新。
   - 使用 `canvas(action=present, url='canvas/index.html')` 显示更新后的仪表板。
5. **生成营养建议**：分析用户当前的摄入情况与 `nutrition/targets.json` 中设定的营养目标之间的差异，并更新 `nutrition/insights.json` 文件。

## 仪表板维护

仪表板（`canvas/index.html`）从 JSON 文件中获取数据，但在显示时使用 `fallbackData` 作为备用数据以确保数据的一致性。请始终确保 HTML 文件中的备用数据与 `dailymacros.json` 文件保持同步。