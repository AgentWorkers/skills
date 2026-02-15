---
name: excalidraw
description: 使用 Excalidraw 的 JSON 数据生成手绘风格的图表、流程图和架构图，并将这些图表导出为 PNG 格式的图像。
---

# Excalidraw 图表生成器

生成美观的手绘风格图表，并将其渲染为 PNG 图像。

## 工作流程

1. **生成 JSON 数据** — 根据用户的需求编写 Excalidraw 元素数组。
2. **保存到文件** — 将 JSON 数据保存到 `/tmp/<name>.excalidraw` 文件中。
3. **渲染** — 使用 `node <skill_dir>/scripts/render.js` 命令将 JSON 数据渲染为 PNG 图像（文件路径为 `/tmp/<name>.png`）。
4. **发送** — 通过消息工具将生成的 PNG 图像发送出去（需要提供文件路径）。

## 快速参考

```bash
node <skill_dir>/scripts/render.js input.excalidraw output.png
```

## 元素类型

| 类型 | 形状 | 关键属性 |
|------|-------|-----------|
| `rectangle` | 矩形 | x, y, 宽度, 高度 |
| `ellipse` | 椭圆 | x, y, 宽度, 高度 |
| `diamond` | 菱形 | x, y, 宽度, 高度 |
| `arrow` | 箭头 | 用于连接形状（详见“箭头绑定”部分） |
| `line` | 直线 | x, y, 点坐标：[[0,0],[dx,dy]] |
| `text` | 文本标签 | x, y, 文本内容, 字体大小, 字体样式（1=手写风格, 2=标准字体, 3=代码风格） |

### 图形样式（所有形状通用）

```json
{
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "hachure",
  "strokeWidth": 2,
  "roughness": 1,
  "strokeStyle": "solid"
}
```

- `fillStyle`：`hachure`（斜线）、`cross-hatch`（交叉线）、`solid`（实线）
- `roughness`：0=清晰显示；1=手绘效果；2=非常粗糙的草图效果

## 箭头绑定（非常重要）

**箭头必须使用 `from`/`to` 属性进行绑定**。渲染器会自动计算箭头的起始点和终点坐标，无需手动计算。

### 简单箭头（直线，连接两个形状）

```json
{"type":"arrow","id":"a1","from":"box1","to":"box2","strokeColor":"#1e1e1e","strokeWidth":2,"roughness":1}
```
只需提供起点和终点的形状信息即可。渲染器会自动计算箭头的路径。

### 多段箭头（需要绕过障碍物的路径）

对于需要绕过障碍物的箭头，请使用 `absolutePoints` 和中间路径点：
```json
{
  "type":"arrow","id":"a2","from":"box3","to":"box1",
  "absolutePoints": true,
  "points": [[375,500],[30,500],[30,127],[60,127]],
  "strokeColor":"#1e1e1e","strokeWidth":2,"roughness":1
}
```
- 第一个点：靠近起点形状的边缘（会自动对齐到实际边缘）
- 最后一个点：靠近终点形状的边缘（会自动对齐到实际边缘）
- 中间点：用于确定箭头路径的坐标

### 箭头标签

在箭头的中点附近放置一个单独的文本标签：
```json
{"type":"text","id":"label","x":215,"y":98,"width":85,"height":16,"text":"sends data","fontSize":10,"fontFamily":1,"strokeColor":"#868e96"}
```

### 箭头样式

- `"strokeStyle":"dashed"`：虚线箭头
- `"startArrowhead": true`：双向箭头

## 模板：带绑定的流程图

```json
{
  "type": "excalidraw",
  "version": 2,
  "elements": [
    {"type":"rectangle","id":"start","x":150,"y":50,"width":180,"height":60,"strokeColor":"#1e1e1e","backgroundColor":"#b2f2bb","fillStyle":"hachure","strokeWidth":2,"roughness":1},
    {"type":"text","id":"t1","x":200,"y":65,"width":80,"height":30,"text":"Start","fontSize":20,"fontFamily":1,"strokeColor":"#1e1e1e"},

    {"type":"arrow","id":"a1","from":"start","to":"decision","strokeColor":"#1e1e1e","strokeWidth":2,"roughness":1},

    {"type":"diamond","id":"decision","x":140,"y":170,"width":200,"height":120,"strokeColor":"#1e1e1e","backgroundColor":"#ffec99","fillStyle":"hachure","strokeWidth":2,"roughness":1},
    {"type":"text","id":"t2","x":185,"y":215,"width":110,"height":30,"text":"Condition?","fontSize":18,"fontFamily":1,"strokeColor":"#1e1e1e","textAlign":"center"},

    {"type":"arrow","id":"a2","from":"decision","to":"process","strokeColor":"#1e1e1e","strokeWidth":2,"roughness":1},

    {"type":"rectangle","id":"process","x":150,"y":350,"width":180,"height":60,"strokeColor":"#1e1e1e","backgroundColor":"#a5d8ff","fillStyle":"hachure","strokeWidth":2,"roughness":1},
    {"type":"text","id":"t3","x":190,"y":365,"width":100,"height":30,"text":"Process","fontSize":20,"fontFamily":1,"strokeColor":"#1e1e1e"}
  ]
}
```

## 布局指南

- **节点大小**：140-200 × 50-70 像素
- **菱形**：180-200 × 100-120 像素（文本区域会更高）
- **节点间距**：垂直间距 60-100 像素；水平间距 80-120 像素
- **文本**：手动将文本放置在形状内部（距离形状左上角约 15-30 像素的位置）
- **箭头标签**：将箭头标签作为单独的文本元素放置在箭头路径的中点附近

## 颜色方案

- **填充颜色**：`#a5d8ff`（蓝色）、`#b2f2bb`（绿色）、`#ffec99`（黄色）、`#ffc9c9`（红色）、`#d0bfff`（紫色）、`#f3d9fa`（粉色）、`#fff4e6`（奶油色）
- **线条颜色**：`#1e1e1e`（深色）、`#1971c2`（蓝色）、`#2f9e44`（绿色）、`#e8590c`（橙色）、`#862e9c`（紫色）
- **文本标签颜色**：`#868e96`（灰色，用于注释）

## 提示

- 每个元素都需要一个唯一的 `id`（用于绑定操作！）
- 箭头必须使用 `from`/`to` 属性进行绑定，无需手动计算坐标。
- `roughness:0` 用于生成清晰的图表；`roughness:1` 用于生成粗糙的草图效果。
- 文本字体样式 `fontFamily:1` 适用于手写风格；`fontFamily:3` 适用于代码风格。
- 将相关元素进行空间分组，并按类型使用不同的颜色进行区分。
- 对于嵌套布局，可以使用一个较大的背景矩形作为容器。