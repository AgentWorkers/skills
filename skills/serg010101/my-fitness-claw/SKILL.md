---
name: my-fitness-claw
version: 1.4
description: 您的个人营养助手。只需用简单的自然语言记录饮食内容，系统会自动统计碳水化合物（P）、蛋白质（C）和脂肪（F）的摄入量，并在精美的实时仪表板上展示您的健康进展。该工具还提供基于人工智能的健康建议、常见的食物信息以及每日饮食追踪功能——所有这些都可以通过聊天界面进行操作和控制。
requires:
  tools: [canvas, read, write, edit]
  paths: [nutrition/, canvas/, memory/]
---
# MyFitnessClaw

该技能用于管理您的营养数据，并通过 OpenClaw 的原生工具提供可视化的营养摄入跟踪面板。

## 核心文件（工作区根目录）

- `nutrition/dailymacros.json`：记录每日营养摄入情况的结构化日志。
- `nutrition/targets.json`：每日营养目标（卡路里、蛋白质、碳水化合物、脂肪）。
- `nutrition/insights.json`：基于当前进度的 AI 生成的营养建议。
- `nutrition/foods/common.md`：常用食物及其营养成分的参考列表。
- `canvas/index.html`：OpenClaw Canvas 的可视化面板。

## 工作流程：记录食物摄入

当用户表示摄入了某种食物时：
1. **估算营养成分**：如果用户未提供具体数据，系统会估算卡路里、蛋白质、碳水化合物和脂肪的摄入量。请先查看 `nutrition/foods/common.md`。
2. **更新每日日志**：将相关数据添加到 `nutrition/dailymacros.json` 文件中。
3. **更新内存记录**：使用 `write` 或 `edit` 工具将食物摄入记录到代理程序的当前每日日志文件中（例如 `memory/YYYY-MM-DD.md`）。
4. **更新面板显示**：
   - 确保 `nutrition/dailymacros.json`、`nutrition/targets.json` 和 `nutrition/insights.json` 文件的内容是最新的。
   - 使用 `canvas(action=present, url='canvas/index.html')` 显示更新后的面板。
   **安全规则**：严禁使用 `edit` 工具修改 `canvas/index.html` 文件或其他可执行代码（如 JS/HTML）。数据持久化应始终通过 JSON 文件完成。
5. **生成营养建议**：根据 `nutrition/targets.json` 中的目标分析摄入情况，并更新 `nutrition/insights.json` 文件。

## 面板维护

可视化面板（`canvas/index.html`）从 JSON 文件中获取数据，但会使用 `fallbackData` 进行即时数据持久化。请确保 HTML 备用数据始终与 `dailymacros.json` 文件保持同步。