---
name: excalidraw-canvas
description: 使用 Excalidraw 创建图表，并将其渲染为 PNG 图像。无论何时你需要绘制复杂的工作流程图、可视化用户界面/线框图，或者绘制任何类型的图表，都可以使用它。
---
# Excalidraw Canvas

通过托管的API将图表或任何绘图内容渲染为PNG格式的图像。在操作元素或箭头时，请务必仔细核对它们的坐标。

## 图像渲染

```bash
RESULT=$(curl -s -m 60 -X POST https://excalidraw-mcp.up.railway.app/api/render \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"elements": [...]}')

# Save PNG
echo "$RESULT" | python3 -c "import json,sys,base64; d=json.load(sys.stdin); open('/tmp/diagram.png','wb').write(base64.b64decode(d['png']))"

# Get edit URL
echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)['editUrl'])"
```

响应格式：`{"success": true, "png": "<base64>", "editUrl": "https://..../canvas/render-xxxxx"}`

系统会同时返回PNG图像文件以及一个编辑URL，用户可以通过该URL在Excalidraw编辑器中修改图表内容。

## 可用的元素类型

所有可用的元素类型包括：`rectangle`（矩形）、`ellipse`（椭圆）、`diamond`（菱形）、`text`（文本）、`arrow`（箭头）、`line`（线条）和`freedraw`（自由绘图）。

### 图形元素（矩形、椭圆、菱形）
```json
{"type":"rectangle","x":100,"y":100,"width":200,"height":80,"bg":"#a5d8ff","label":"My Box"}
{"type":"ellipse","x":100,"y":100,"width":150,"height":100,"bg":"#b2f2bb","label":"Node"}
{"type":"diamond","x":100,"y":100,"width":140,"height":100,"bg":"#ffec99","label":"Decision?"}
```
- `x`, `y` — 元素的位置
- `width`, `height` — 元素的尺寸
- `bg` — 元素的填充颜色（十六进制格式）
- `stroke` — 元素的边框颜色（默认为`#1e1e1e`）
- `label` — 显示在图形内部的文本

### 文本元素
```json
{"type":"text","x":100,"y":50,"text":"Title","fontSize":28}
```

### 箭头与线条元素
```json
{"type":"arrow","x":300,"y":140,"points":[[0,0],[150,0]]}
{"type":"line","x":0,"y":200,"points":[[0,0],[800,0]]}
```
箭头的起点和终点坐标使用以下格式表示：
- 水平箭头：`[[0,0],[150,0]]`
- 垂直箭头：`[[0,0],[0,100]]`
- 弯曲箭头：`[[0,0],[0,50],[100,50]]`

### 自由绘图元素
```json
{"type":"freedraw","x":100,"y":100,"points":[[0,0],[5,3],[10,8],[20,15]]}
```
自由绘图路径由一系列相对于图形起点的 `[x,y]` 坐标点组成。

## 完整示例
```bash
RESULT=$(curl -s -m 60 -X POST https://excalidraw-mcp.up.railway.app/api/render \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"elements": [
    {"type":"text","x":250,"y":20,"text":"System Design","fontSize":28},
    {"type":"rectangle","x":50,"y":80,"width":180,"height":70,"bg":"#a5d8ff","label":"Frontend"},
    {"type":"rectangle","x":300,"y":80,"width":180,"height":70,"bg":"#b2f2bb","label":"API"},
    {"type":"rectangle","x":550,"y":80,"width":180,"height":70,"bg":"#ffec99","label":"Database"},
    {"type":"arrow","x":230,"y":115,"points":[[0,0],[70,0]]},
    {"type":"arrow","x":480,"y":115,"points":[[0,0],[70,0]]}
  ]}')

echo "$RESULT" | python3 -c "import json,sys,base64; d=json.load(sys.stdin); open('/tmp/diagram.png','wb').write(base64.b64decode(d['png'])); print(d['editUrl'])"
```

## 将图表发送给用户

```
message(action="send", filePath="/tmp/diagram.png", caption="✏️ Edit: {editUrl}")
```

请务必提供编辑URL，以便用户能够对图表进行后续修改。