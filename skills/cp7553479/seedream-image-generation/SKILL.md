---
name: seedream-image-generation
description: 通过 Volcengine 的 Seedream API 生成图像。当您需要执行文本到图像（Text-to-Image, T2I）、图像到图像（Image-to-Image, I2I）转换，或者基于文本或视觉输入进行豆包生图（DouBao Image Generation）等通用视觉创意任务时，可以使用该 API。
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["ARK_API_KEY"] },
        "primaryEnv": "ARK_API_KEY"
      }
  }
---
# Seedream 图像生成技能

该技能提供了调用 Volcengine Ark 大模型服务平台的图像生成模型（Seedream）的方法。

## 选择环境

该脚本提供了 Python 和 JavaScript 两种实现方式：
- 如果您的运行环境主要是 Node.js/TypeScript 或 Web 模块，请使用 **seedream.js**。
- 如果您的运行环境涉及复杂的数据分析、批量调度，或者纯 Python 环境，请使用 **seedream.py**。

## 支持的模型参数（模型 ID/端点 ID）

在调用时，`model` 参数需要是来自 Ark 控制台的部署端点 ID（例如 `ep-202X...`），该 ID 必须对应以下基础图像生成模型之一：
- `doubao-seedream-5-0-260128`
- `doubao-seedream-4-5-251128`
- `doubao-seedream-4-0-250828`

## 脚本参数

您必须传递特定参数来控制图像生成过程。可用的参数包括：

- **model** *(字符串，可选)*：对应于模型的端点 ID。默认值为 `doubao-seedream-5-0-260128`。
- **prompt** *(字符串，必填)*：用于生成图像的文本描述。
- **image** *(字符串 | 字符串列表，可选)*：用于图像到图像生成的本地图像路径或图像路径列表。脚本会读取本地文件，将其转换为 base64 格式，并作为 `image` 字段发送。
- **watermark** *(布尔值，可选)*：是否添加 Volcengine AI 水印。未提供该参数时，默认值为 `false`。
- **optimize_prompt_options** *(对象，可选)*：配置自动提示优化选项。格式：JSON 对象。例如：`{"mode": "standard"}`。
- **tools** *(对象列表，可选)*：模型的功能选项，格式为 JSON。示例：`[{"type": "web_search"}]`。
- **output_format** *(字符串，可选)*：输出图像格式。可选值包括 `png`、`jpeg`。
- **sequential_image_generation** *(字符串，可选)*：图像生成策略（例如 `"auto"`）。
- **download_dir** *(字符串，可选)*：用于保存生成图像的本地目录。如果未提供该参数，图像将不会被下载到本地，仅返回 API 响应。

## 推荐的宽度和高度值

| 分辨率 | 长宽比 | 尺寸 |
| :--------- | :----------- | :--------- |
| **2K**     | 1:1          | 2048x2048  |
|            | 4:3          | 2304x1728  |
|            | 3:4          | 1728x2304  |
|            | 16:9         | 2848x1600  |
|            | 9:16         | 1600x2848  |
|            | 3:2          | 2496x1664  |
|            | 2:3          | 1664x2496  |
|            | 21:9         | 3136x1344  |
| **3K**     | 1:1          | 3072x3072  |
|            | 4:3          | 3456x2592  |
|            | 3:4          | 2592x3456  |
|            | 16:9         | 4096x2304  |
|            | 9:16         | 2304x4096  |
|            | 2:3          | 2496x3744  |
|            | 3:2          | 3744x2496  |
|            | 21:9         | 4704x2016  |

## 使用示例

**Python 示例：**
```bash
cd <current_skill_dir>
python3 seedream.py \
  --prompt "A cute orange cat laying under the sun" \
  --model "ep-xxxxx..." \
  --size "1024x1024" \
  --watermark "false" \
  --output_format "png"
```

**Node.js 示例：**
```bash
cd <current_skill_dir>
node seedream.js \
  --prompt "A cute orange cat laying under the sun" \
  --model "ep-xxxxx..." \
  --size "1024x1024" \
  --watermark "false" \
  --output_format "png"
```

**图像到图像生成示例（Python）：**
```bash
cd <current_skill_dir>
python3 seedream.py \
  --prompt "Turn this product photo into a clean white-background ecommerce image" \
  --image "/path/to/source.png" \
  --model "ep-xxxxx..."
```

**使用工具和优化的高级示例（Python）：**
```bash
cd <current_skill_dir>
python3 seedream.py \
  --prompt "A futuristic cityscape" \
  --model "ep-xxxxx..." \
  --optimize_prompt_options '{"mode": "standard"}' \
  --tools '[{"type": "web_search"}]'
```

有关更详细的 API 文档，请访问：[https://www.volcengine.com/docs/82379/1541523?lang=zh](https://www.volcengine.com/docs/82379/1541523?lang=zh)
如需查看更多模型 ID 或获取最新模型 ID，请访问：[https://www.volcengine.com/docs/82379/1330310?lang=zh#36969059](https://www.volcengine.com/docs/82379/1330310?lang=zh#36969059)，然后更新此 `seedream-image-generation/SKILL.md` 文件中的 “Supported Model Parameters” 部分。