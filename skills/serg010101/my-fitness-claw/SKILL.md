---
name: my-fitness-claw
version: 1.7.0
description: 您的个人营养助手。只需用简单的自然语言记录饮食内容，系统会自动统计碳水化合物（P）、蛋白质（C）和脂肪（F）的摄入量，并在精美的实时仪表板上展示您的健康进展。1.7版本新增了基于32岁男性每日推荐摄入量的微量营养素自动追踪功能。此外还提供人工智能驱动的健康建议、常见食物信息以及每日健康进度追踪功能——所有这些功能均可通过聊天界面进行操作。
requires:
  tools: [canvas, read, write, edit]
  paths: [nutrition/, canvas/, memory/]
---
# MyFitnessClaw

该技能用于管理用户的营养数据，并利用 OpenClaw 的原生工具提供可视化仪表板，以跟踪宏量营养素和微量营养素的摄入情况。

## 核心文件（技能资产）

- `assets/nutrition/daily_macros.json`：每日摄入量的结构化日志。
- `assets/nutrition/targets.json`：每日营养目标（热量、蛋白质、碳水化合物、脂肪以及 10 种必需的微量营养素）。
- `assets/nutrition/insights.json`：基于当前进度的 AI 生成的建议。
- `assets/nutrition/foods/common.md`：常见食物的参考列表及其所含的宏量/微量营养素信息。
- `assets/canvas/index.html`：OpenClaw 画布的可视化仪表板。

## 工作流程：记录饮食

当用户表示摄入了某种食物时：
1. **估算宏量营养素和微量营养素**：如果用户未提供相关数据，则进行估算：
   - 宏量营养素：热量、蛋白质、碳水化合物、脂肪。
   - 微量营养素：维生素 D3、镁、钾、锌、维生素 B6、维生素 B12、硒、维生素 C、维生素 A、维生素 E。
   首先查看 `assets/nutrition/foods/common.md`。
2. **更新每日日志**：更新 `assets/nutrition/daily_macros.json`，包括每顿饭的详细数据以及每日总量。
3. **更新离线数据**：将相同的数据更新到 `assets/canvas/offline_data.js` 文件中，确保其中包含微量营养素信息。
   使用以下代码覆盖文件内容：`window.__OFFLINE_DAILY_MACROS = [...]; window.__OFFLINE_TARGETS = {...}; window.__OFFLINE_INSIGHTS = {...};`
   这样在通过 `file://`（离线/浏览器优先）方式打开仪表板时，数据仍能正常显示。
4. **更新内存记录**：将此次饮食记录到代理程序的当前每日日志文件中（例如 `memory/YYYY-MM-DD.md`）。
5. **显示仪表板**：使用 `canvas(action=present, url='skills/my-fitness-claw/assets/canvas/index.html')` 在 OpenClaw 中显示更新后的仪表板。
6. **提供浏览器访问方式**：每次记录饮食后，显示以下提示：
   > 📊 **在浏览器中查看：**
   > - **快速方式**：在浏览器中打开 `skills/my-fitness-claw/assets/canvas/index.html`（使用离线数据）。
   > - **完整方式**：从工作区根目录运行 `python -m http.server 8000`，然后访问 `http://localhost:8000/skills/my-fitness-claw/assets/canvas/index.html`。
7. **生成分析结果**：根据 `assets/nutrition/targets.json` 中的目标分析用户的营养摄入情况，并更新 `assets/nutrition/insights.json`。

**数据持久化规则**：
- `assets/nutrition/*.json`：用于存储核心营养数据。
- `assets/canvas/offline_data.js`：仅用于通过 `file://` 查看离线数据。
- **常规记录过程中**：不得修改 `assets/canvas/index.html` 文件。

## 发布前的检查清单（公共安全）

在发布或分享此技能之前，请执行以下操作：
1. **清理数据**：将 `nutrition/dailymacros.json` 设置为空数组 `[]`。
2. **清理离线数据**：将 `canvas/offline_data.js` 清空，使其恢复到初始状态：`window.__OFFLINE_DAILY_MACROS = [];`。
3. **清除分析结果**：清空 `nutrition/insights.json` 或将其重置为默认的建议内容。
4. **删除个人信息**：从 `nutrition/targets.json` 和 `memory/` 文件中删除任何敏感信息。
5. **验证文件**：确保 `assets/` 文件夹中不存在任何私人图片或文档。