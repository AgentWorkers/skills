---
name: frinkiac
description: 搜索《辛普森一家》、《飞出个未来》、《瑞克和莫蒂》以及《我为喜剧狂》这些电视剧的截图，并从中生成表情包（meme）。
metadata:
  {"openclaw":{"emoji":"📺","requires":{"bins":["node","npx"]}}}
---

# Frinkiac TV截图与模因工具

使用Frinkiac/Morbotron API，您可以搜索电视剧中的对话、浏览剧集画面，并生成模因。

## 可使用的剧集

- `simpsons` - 《辛普森一家》（通过Frinkiac）
- `futurama` - 《飞出个未来》（通过Morbotron）
- `rickandmorty` - 《瑞克和莫蒂》
- `30rock` - 《恶搞之家》

## MCP服务器设置

此功能需要使用MCP服务器。请将其添加到您的MCP配置中：

```json
{
  "mcpServers": {
    "frinkiac": {
      "command": "npx",
      "args": ["-y", "@ryantenney/frinkiac-mcp"]
    }
  }
}
```

## 工具

### search

通过对话文本搜索剧集画面：

- `show`: 要搜索的剧集（simpsons, futurama, rickandmorty, 30rock）
- `query`: 要搜索的对话（例如：“D'oh!”, “Good news everyone”）
- `limit`: 最大结果数量（可选）
- `include_images`: 是否包含缩略图（可选）

### get_caption

获取剧集画面的详细信息，包括剧集元数据和附近的帧：

- `show`: 剧集名称
- `episode`: 剧集编号（格式为S##E##，例如：“S07E21”）
- `timestamp`: 帧的时间戳（以毫秒为单位）
- `include_nearby_images`: 是否包含附近帧的缩略图（可选）

### get_screenshot

从指定剧集画面中获取截图：

- `show`: 剧集名称
- `episode`: 剧集编号（格式为S##E##）
- `timestamp`: 帧的时间戳（以毫秒为单位）
- `return_url_only`: 仅返回截图的URL（可选）

### generate_meme

创建带有自定义文本的模因。文本会自动换行（每行约35个字符）：

- `show`: 剧集名称
- `episode`: 剧集编号（格式为S##E##）
- `timestamp`: 帧的时间戳（以毫秒为单位）
- `text`: 要显示在图片上的文本

### get_nearby_frames

浏览相邻的帧以找到最合适的截图：

- `show`: 剧集名称
- `episode`: 剧集编号（格式为S##E##）
- `timestamp`: 帧的时间戳（以毫秒为单位）
- `include_images`: 是否包含缩略图（可选）

### get_episode

获取指定时间范围内的剧集元数据和字幕：

- `show`: 剧集名称
- `episode`: 剧集编号（格式为S##E##）
- `start_timestamp`: 时间范围的开始时间（以毫秒为单位）
- `end_timestamp`: 时间范围的结束时间（以毫秒为单位）

## 示例工作流程

**查找并制作模因：**

1. 搜索对话：“search simpsons “everything’s coming up Milhouse””
2. 获取截图：使用`get_screenshot`获取对应的剧集和帧的时间戳
3. 创建模因：使用`generate_meme`并添加自定义文本

**浏览剧集画面：**

1. 搜索对话以获取剧集和帧的时间戳
2. 使用`get_nearby_frames`找到最合适的帧
3. 使用`get_caption`查看完整的上下文和字幕

**获取剧集信息：**

1. 使用`get_episode`获取指定时间范围内的所有对话
2. 找到您想要的画面
3. 生成模因或截图