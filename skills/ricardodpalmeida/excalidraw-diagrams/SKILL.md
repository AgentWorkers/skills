---
name: excalidraw-diagrams
description: >
  **生成 Excalidraw 图表用于 Obsidian**  
  支持两种输出格式：  
  - **Obsidian 格式（.md）**：可直接用于 Obsidian 插件中；  
  - **标准格式（.excalidraw）**：适用于上传至 Excalidraw.com 平台。  
  适用于以下场景：  
  - 创建架构图、流程图、概念图、序列图、系统设计图或任何类型的可视化图表。
---
# Excalidraw 图表生成器

该工具能够根据文本内容生成 Excalidraw 图表，并支持多种输出格式，这些格式可与 Obsidian 的 Excalidraw 插件兼容。

## 输出模式

用户必须明确请求生成图表。除非用户提出要求，否则不要自动生成或保存文件。

| 模式 | 使用场景 | 文件扩展名 | 用途 |
|------|-------------|----------------|----------|
| **Obsidian** | 用户需要 Obsidian/Excalidraw 图表 | `.md` | 可直接在 Obsidian 中通过 Excalidraw 插件打开 |
| **标准格式** | 用户需要 excalidraw.com 格式的文件 | `.excalidraw` | 可在 excalidraw.com 上打开 |

如果模式不明确，请询问用户他们希望使用哪种格式。

## 处理流程

1. 如果模式不明确，先与用户确认输出格式。
2. **分析内容**：识别概念、关系和层次结构。
3. 根据内容结构选择合适的图表类型。
4. 生成符合设计规则的 Excalidraw JSON 数据。
5. 按照选定的格式输出结果。
6. 在写入文件之前，询问用户保存路径和文件名。
7. 检查目标路径下是否已存在同名文件；如果存在，请先询问用户是否要覆盖该文件。
8. 仅在用户确认后保存文件。

## 输出格式

### 模式 1：Obsidian 格式（默认）

此格式将 JSON 数据封装在 Markdown 格式中，以便 Obsidian 的 Excalidraw 插件可以直接打开：

```markdown
```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---

==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==
You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%

## Drawing
```
json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [
    ...
  ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff",
    "files": {}
}
___CODE_BLOCK_1_
```

**关键格式规则：**
- 文档的开头必须包含 `tags: [excalidraw]`。
- 警告信息必须完整显示。
- JSON 数据必须放在 ````json` 代码块中。
- `Text Elements` 部分应保持为空（仅保留 `%%`）。
- 对于 Obsidian 模式，`source` 必须是 `"https://github.com/zsviczian/obsidian-excalidraw-plugin"`。

### 模式 2：标准 Excalidraw 格式

纯 JSON 格式，适用于 excalidraw.com：

```markdown
___CODE_BLOCK_2_
```

## 设计规则

### 字体样式
- **所有文本元素应使用 `"fontFamily": 5"`（Excalifont 字体，手绘风格）。
- **字体大小**：
  - 标题：24-28px（最小 20px）
  - 子标题：18-20px
  - 正文/标签：16-18px（最小 16px）
  - 注释：14px（慎用）
- **禁止使用小于 14px 的字体大小**——在正常缩放下难以阅读。
- **行高**：所有文本的行高应为 `1.25`。
- **文本对齐**：标签的文本对齐方式为 `"textAlign": "center"`，垂直对齐方式为 `"verticalAlign": "middle"`。

### 布局
- **画布范围**：确保所有元素都在 0-1200 x 0-800 像素范围内。
- **最小形状尺寸**：带文字的矩形/椭圆至少应为 120x60px。
- **元素间距**：元素之间至少保留 20-30px 的间距，以防重叠。
- **边框**：所有元素周围至少保留 50-80px 的边框。
- **网格**：使用 20px 的网格来对齐元素。

### 颜色方案

**形状填充颜色（backgroundColor, fillStyle: "solid"）：**

| 颜色 | 十六进制代码 | 用途 |
|-------|-----|-------|
| 浅蓝色 | `#a5d8ff` | 输入框、数据源、主要节点 |
| 浅绿色 | `#b2f2bb` | 成功状态、输出结果 |
| 浅橙色 | `#ffd8a8` | 警告、待处理事项、外部依赖项 |
| 浅紫色 | `#d0bfff` | 处理中、中间件、特殊项目 |
| 浅红色 | `#ffc9c9` | 错误、严重警告 |
| 浅黄色 | `#fff3bf` | 备注、决策、计划内容 |
| 浅青色 | `#c3fae8` | 存储、数据、缓存 |
| 浅粉色 | `#eebefa` | 分析结果、指标、统计数据 |

**文本颜色（strokeColor）：**

| 用途 | 十六进制代码 | 说明 |
|-------|-----|-------|
| 标题 | `#1e40af` | 深蓝色 |
| 子标题/连接线 | `#3b82f6` | 浅蓝色 |
| 正文 | `#374151` | 深灰色（在白色背景上至少使用 `#757575`） |
| 强调文本 | `#f59e0b` | 金色/琥珀色 |

**对比度规则**：
- 白色背景下的文本颜色：最低亮度应为 `#757575`。
- 浅色填充部分应使用较深的颜色（例如，浅绿色填充对应的文本颜色应为 `#15803d`）。
- 避免在白色背景上使用浅灰色（如 `#b0b0b0`、`#999`）的文本。

### 样式设置
- **粗糙度**：设置为 `1` 以获得手绘效果；设置为 `0` 以获得清晰的图表效果。
- **线条宽度**：大多数元素的线条宽度为 `2`。
- **圆角**：矩形的圆角设置为 `{ "type": 3 }`。
- **透明度**：大多数元素的透明度为 `100`，背景层的透明度为 `30-50`。

## 图表类型

根据内容选择合适的图表类型：

| 类型 | 适用场景 | 布局方式 |
|------|----------|--------|
| **流程图** | 逐步流程、工作流程 | 从上到下或从左到右，带有箭头 |
| **思维导图** | 概念扩展、头脑风暴 | 从中心向外辐射的放射状结构 |
| **层次结构图** | 组织结构图、系统分解 | 从上到下的树状结构 |
| **关系图** | 依赖关系、交互关系 | 用连接线表示的关系网络 |
| **对比图** | A 与 B 的对比分析 | 并排的列状展示 |
| **时间线** | 事件进展、里程碑 | 水平时间轴 |
| **矩阵图** | 二维分类、优先级排序 | X/Y 坐标平面 |
| **架构图** | 系统组件、数据流 | 分层显示（前端/中间件/后端）

## JSON 结构

### 根节点结构

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [...],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

### 元素模板

**所有元素都必须包含以下字段：**

```json
{
  "id": "unique-id-string",
  "type": "rectangle|ellipse|text|arrow|diamond|line",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 50,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "roundness": { "type": 3 },
  "seed": 123456789,
  "version": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

**注意：**
- 使用 `"boundElements": null`（而不是 `[]`）。
- 使用 `"updated": 1`（而不是时间戳）。
- **不要包含 `frameId`、`index`、`versionNonce` 或 `rawText`。

### 文本元素（附加字段）

```json
{
  "type": "text",
  "text": "Label Text",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "Label Text",
  "autoResize": true,
  "lineHeight": 1.25
}
```

### 箭头元素（附加字段）

```json
{
  "type": "arrow",
  "points": [[0, 0], [200, 0]],
  "startBinding": null,
  "endBinding": null,
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": false
}
```

对于连接形状的箭头，使用 `startBinding` 和 `endBinding`：

```json
{
  "startBinding": { "elementId": "shape-id-1", "focus": 0, "gap": 1, "fixedPoint": null },
  "endBinding": { "elementId": "shape-id-2", "focus": 0, "gap": 1, "fixedPoint": null }
}
```

将箭头添加到每个形状的 `boundElements` 列表中：

```json
{
  "boundElements": [
    { "id": "arrow-id", "type": "arrow" }
  ]
}
```

### 文本居中计算

文本元素使用左边缘的 x 坐标进行居中。例如，要将文本 “Hello”（5 个字符，20px 大小）居中在 x=300 的位置：

```markdown
# 计算文本宽度：5 * 20 * 0.5 = 50
# 计算居中位置：x = 300 - 25 = 275
```

## 常见图表类型及示例

### 架构图
- 使用矩形表示服务/组件。
- 通过颜色区分不同层次（前端=蓝色，中间件=紫色，后端=绿色）。
- 用箭头表示数据流动。
- 将相关组件可视化地组合在一起。

### 流程图
- 使用矩形表示流程步骤。
- 使用菱形表示决策点。
- 使用箭头指示流程方向。
- 布局方式可以是从上到下或从左到右。

### 思维导图
- 中心主题位于图表的中心。
- 分支从中心向外辐射。
- 每个分支使用统一的颜色。
- 子分支连接到主分支。

## 文件命名规则

根据内容建议使用描述性的文件名，但在保存前务必先与用户确认：

| 模式 | 文件格式 | 示例文件名 |
|------|--------|---------|
| Obsidian | `[主题].md` | `system-architecture.diagram.md` |
| 标准格式 | `[主题].excalidraw` | `system-architecture.diagram.excalidraw` |

**在写入文件之前：**
- 与用户确认完整的保存路径和文件名。
- 如果目标路径下已存在同名文件，需先警告用户并询问是否要覆盖。
- 绝不要自动将文件保存到默认路径。

## 用户示例命令
- “生成我们的微服务架构的 Excalidraw 图表。”
- “绘制一个展示 CI/CD 流程的流程图。”
- “制作一个关于机器学习概念的思维导图。”
- “为这个工作流程生成一个标准的 excalidraw 文件。”（此时会生成 `.excalidraw` 格式的文件。）

## 实现检查清单

在生成图表时，请执行以下步骤：
1. [ ] 与用户确认输出格式（Obsidian 或标准格式）。
2. [ ] 分析内容并选择合适的图表类型。
3. [ ] 规划图表布局（元素位置、连接方式、分组方式）。
4. [ ] 生成图表元素，包括：
   - 为每个元素分配唯一的 ID。
   - 使用 `fontFamily: 5` 作为所有文本的字体样式。
   - 使用正确的颜色。
   - 确保箭头和标签的连接正确。
5. [ ] 验证 JSON 数据的语法是否正确。
6. [ ] 将数据封装在适当的格式中。
7. [ ] 与用户确认保存路径和文件名。
8. [ ] 检查目标路径下是否已存在文件（如果存在则警告用户）。
9. [ ] 仅在用户确认后保存文件。
10. [ ] 向用户提供文件的保存路径和使用说明。