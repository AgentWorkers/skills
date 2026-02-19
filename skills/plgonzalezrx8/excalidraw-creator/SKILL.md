---
name: excalidraw-creator
description: 创建手绘风格的 Excalidraw 图表、流程图和架构可视化图表，并将它们保存为 PNG 图像。
---
# Excalidraw Creator

这是一个用于生成美观的手绘风格图表的工具，生成的图表会以PNG图像的形式输出。

## 工作流程

1. **生成JSON数据**：根据用户的需求，编写Excalidraw图表的元素数组。
2. **保存到文件**：将生成的JSON数据保存到`/tmp/<name>.excalidraw`文件中。
3. **渲染图表**：执行`node <skill_dir>/scripts/render.js /tmp/<name>.excalidraw /tmp/<name>.png`命令来渲染图表。
4. **发送结果**：通过消息工具将生成的PNG图像文件发送出去（需要提供文件的路径`filePath`）。

## 快速参考

```bash
node <skill_dir>/scripts/render.js input.excalidraw output.png
```

## 图表元素类型

| 类型 | 形状 | 主要属性 |
|------|-------|-----------|
| `rectangle` | 矩形 | x, y, 宽度, 高度 |
| `ellipse` | 椭圆 | x, y, 宽度, 高度 |
| `diamond` | 菱形 | x, y, 宽度, 高度 |
| `arrow` | 箭头 | 用于连接其他形状（详见“箭头绑定”部分） |
| `line` | 直线 | x, y, 点坐标：[[0,0],[dx,dy]] |
| `text` | 文本标签 | x, y, 文本内容, 字体大小, 字体样式（1=手写风格, 2=标准字体, 3=代码风格） |

### 图表元素的样式设置

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
- `roughness`：0=清晰显示；1=手绘风格；2=非常粗糙的绘图效果

## 箭头绑定（非常重要）

**箭头的绘制必须使用`from`和`to`属性**。渲染器会自动计算箭头的起始点和终点坐标，无需手动计算。

### 简单箭头（直线，连接两个形状）

```json
{"type":"arrow","id":"a1","from":"box1","to":"box2","strokeColor":"#1e1e1e","strokeWidth":2,"roughness":1}
```
只需提供箭头的方向，无需指定具体的x、y坐标或起点、终点坐标。渲染器会自动计算这些信息。

### 多段箭头（需要绕过障碍物的路径）

对于需要绕过障碍物的箭头，可以使用`absolutePoints`属性来指定中间路径点：
```json
{
  "type":"arrow","id":"a2","from":"box3","to":"box1",
  "absolutePoints": true,
  "points": [[375,500],[30,500],[30,127],[60,127]],
  "strokeColor":"#1e1e1e","strokeWidth":2,"roughness":1
}
```
- 第一个点：靠近起始形状的边缘（会自动对齐到实际边缘）
- 最后一个点：靠近目标形状的边缘（会自动对齐到实际边缘）
- 中间点：用于确定箭头的路径

### 箭头标签的放置

可以在箭头的中点附近添加一个单独的文本元素来显示标签内容：
```json
{"type":"text","id":"label","x":215,"y":98,"width":85,"height":16,"text":"sends data","fontSize":10,"fontFamily":1,"strokeColor":"#868e96"}
```

### 箭头样式设置

- `"strokeStyle":"dashed"`：虚线箭头
- `"startArrowhead": true`：双向箭头

## 示例模板：带箭头绑定的流程图

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
- **节点间的垂直间距**：60-100 像素
- **节点间的水平间距**：80-120 像素
- **文本标签**：手动将文本放置在形状内部（通常距离形状左上角约15-30像素的位置）
- **箭头标签**：将标签作为单独的文本元素放置在箭头路径的中点附近

## 颜色方案

- **填充颜色**：`#a5d8ff`（蓝色）、`#b2f2bb`（绿色）、`#ffec99`（黄色）、`#ffc9c9`（红色）、`#d0bfff`（紫色）、`#f3d9fa`（粉色）、`#fff4e6`（米色）
- **线条颜色**：`#1e1e1e`（深色）、`#1971c2`（蓝色）、`#2f9e44`（绿色）、`#e8590c`（橙色）、`#862e9c`（紫色）
- **文本标签颜色**：`#868e96`（灰色，用于注释）

## 使用提示

- 每个图表元素都需要一个唯一的`id`（用于箭头绑定）。
- 箭头的绘制必须使用`from`和`to`属性，避免手动计算坐标。
- 设置`roughness=0`可以获得清晰的图表显示效果；`roughness=1`可以获得更粗糙的手绘风格。
- 文本标签的字体样式`fontFamily=1`表示手写风格，`fontFamily=3`表示代码风格。
- 将相关的元素进行分组，并根据类型使用不同的颜色进行区分。
- 对于嵌套的图表布局，可以使用一个较大的背景矩形作为容器。