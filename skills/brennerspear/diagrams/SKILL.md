---
name: diagrams
description: 生成可视化的流程图、架构图和系统图，格式为 SVG/PNG。当用户需要流程图、用户交互图、架构图、系统图或任何类型的可视化图表时，可以使用该工具。该工具支持 ELK JSON 布局引擎，并能自动将图表渲染为 SVG 格式。
---
# 图表生成

可以将结构化的 JSON 数据转换为 SVG 图表（可选也可生成 PNG 图片）。

## 快速入门

1. 在目标目录中安装 `elkjs`（如果尚未安装）：
   ```bash
   cd <project>/docs/diagrams && npm init -y && npm install elkjs
   # Set "type": "module" in package.json
   ```

2. 编写描述图表的 ELK JSON 文件（请参考以下格式）。

3. 生成图表：
   ```bash
   # Single file
   node <skill-dir>/scripts/render-elk.mjs diagram.json output.svg

   # Batch: all .json files in a folder → svg/ subfolder
   node <skill-dir>/scripts/render-elk.mjs --dir <folder>

   # Batch + PNG (macOS only, uses sips)
   node <skill-dir>/scripts/render-elk.mjs --dir <folder> --png
   ```

4. 将生成的图表嵌入到 Markdown 文档中：
   ```markdown
   ![Diagram Title](diagrams/svg/my-diagram.svg)
   ```

## ELK JSON 格式

```json
{
  "id": "root",
  "title": "Diagram Title (rendered as heading)",
  "layoutOptions": {
    "elk.algorithm": "layered",
    "elk.direction": "DOWN",
    "elk.spacing.nodeNode": "30",
    "elk.layered.spacing.nodeNodeBetweenLayers": "40",
    "elk.padding": "[top=40,left=20,bottom=20,right=20]"
  },
  "children": [
    {
      "id": "node1",
      "width": 220,
      "height": 45,
      "labels": [{"text": "Node label for ELK layout"}],
      "label": "📦 Display label (rendered in SVG)",
      "color": "core",
      "subtitle": "Optional second line"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "sources": ["node1"],
      "targets": ["node2"],
      "labels": [{"text": "Yes", "width": 25, "height": 14}],
      "edgeColor": "#10B981",
      "dashed": true
    }
  ]
}
```

### 节点属性

| 属性 | 类型 | 描述 |
|----------|------|-------------|
| `id` | 字符串 | 必填项。唯一标识符 |
| `width` | 数字 | 节点宽度（单位：px，默认值 120） |
| `height` | 数字 | 节点高度（单位：px，默认值 40） |
| `labels` | 数组 | `[{text}]` — 用于 ELK 进行布局计算 |
| `label` | 字符串 | 在 SVG 中显示的文本（支持使用表情符号）；如果未设置 `labels`，则使用 `id` 作为显示文本 |
| `color` | 字符串 | 颜色代码（来自颜色调色板） |
| `subtitle` | 字符串 | 标签下方的次要文本 |
| `fontSize` | 数字 | 标签字体大小（默认值 13） |
| `children` | 数组 | 子节点 — 使该节点成为一个容器节点 |
| `containerColor` | 字符串 | 容器背景的颜色代码 |

### 边缘属性

| 属性 | 类型 | 描述 |
|----------|------|-------------|
| `id` | 字符串 | 必填项。唯一标识符 |
| `sources` | 字符串数组 | 源节点的 ID |
| `targets` | 字符串数组 | 目标节点的 ID |
| `labels` | 数组 | `[{text, width, height}]` — 边缘的标签信息 |
| `edgeColor` | 字符串 | 十六进制颜色代码（默认值 `#64748B`） |
| `dashed` | 布尔值 | 是否显示虚线 |
| `strokeWidth` | 数字 | 线条粗细（默认值 1.5） |

### 颜色调色板

共有 8 种语义颜色，每个节点对应一种颜色。每个 SVG 图表的底部会自动生成颜色图例。

| 颜色代码 | 颜色 | 含义 | 适用场景 |
|---------|-------|---------|---------|
| `action` | 🔵 蓝色 | **系统操作** | 应用程序执行的操作（如 API 调用、数据库写入、定时任务触发） |
| `external` | 🟢 浅绿色 | **外部服务** | 第三方 API（如 Google、Twilio、Stripe 等） |
| `decision` | 🩷 粉色 | **决策节点** | 表示“是/否”分支、条件判断 |
| `user` | 🟠 橙色 | **用户操作** | 用户执行的操作（如点击、输入、审核） |
| `success` | 🟢 绿色 | **成功结果** | 任务已完成、已确认、已创建或可见 |
| `negative` | 🔴 红色 | **失败结果** | 任务被取消、出现错误或未完成 |
| `neutral` | ⚫ 灰色 | **中性/信息性** | 用于表示起始点、标签或非活动状态 |
| `data` | 🟡 琥珀色 | **数据/中间结果** | 记录、草稿、输出结果或中间数据 |

在根节点的 JSON 数据中设置 `"legend": false` 可以隐藏自动生成的图例。

### 布局选项

常见的 `layoutOptions` 参数：

- `elk.direction`：`DOWN`（默认值）、`RIGHT`、`LEFT`、`UP` — 图表的排列方向 |
- `elk.algorithm`：`layered`（默认值，适合流程图）、`force`、`stress` — 图表的布局方式 |
- `elk.spacing.nodeNode`：同级节点之间的间距（单位：px） |
- `elk.layered.spacing.nodeNodeBetweenLayers`：不同层之间的间距（单位：px） |
- `elk.padding`：`[top=N,left=N,bottom=N,right=N]` — 图表边框的尺寸 |

## 设计建议

- **尺寸建议**：大多数节点的宽度为 200-280px；单行标签的高度为 45px，双行标签的高度为 55px。
- **决策节点**：使用粉色（`context`）来表示“是/否”分支。
- **边缘标签**：保持标签简短（如“是/否/错误”）。通过设置 `width` 和 `height` 来确保标签正确显示。
- **容器节点**：在节点中添加 `children` 数组；使用 `containerColor: "step"` 可以创建浅蓝色的容器组。
- **手动路径与自动路径**：在表示可选路径的边缘上设置 `dashed: true`。
- **标题**：在根节点上设置 `title`，以便在图表上方显示标题。
- **标签中的表情符号**：支持并鼓励使用表情符号以提升可读性。

## 注意事项

- **容器布局**：当使用 `RIGHT` 方向的层次化布局时，嵌套容器可能会导致布局重叠。建议使用 `DOWN` 方向的布局；如果需要水平布局，可以将容器扁平化。
- **`labels` 与 `label` 的区别**：`labels` 是 ELK 用于计算布局间距的数据结构，而 `label` 是在 SVG 中实际显示的文本。请同时设置这两个属性；`labels[0].text` 应该与实际显示的标签长度相近，以确保正确的显示效果。
- 为了使 ESM（ESM）导入生效，`package.json` 文件中必须包含 `"type": "module"` 的配置。
- `elkjs` 必须安装在运行脚本的目录中，它不是全局可用的库。