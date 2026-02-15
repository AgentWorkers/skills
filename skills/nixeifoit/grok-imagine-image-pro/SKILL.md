---
name: grok-imagine-image-pro
description: 使用 xAI 的 Grok/Flux API 生成高质量图片。适用于用户请求图片生成（如“生成一张...的图片”、“创建 PNG 文件”）或图片编辑（如“修改这张图片”、“将其转换为...”）的场景。支持处理各种提示语、样式设置、宽高比调整以及批量生成功能。输出格式为 PNG，可通过 base64 编码或文件形式获取。
metadata:
  openclaw:
    requires:
      env:
        - XAI_API_KEY
      bins:
        - curl
        - python3
---
# Grok Imagine Image Pro

**API密钥：** `$XAI_API_KEY` （已配置）  
**保存目录：** `~/.openclaw/media/` （实际路径为 `/data/.openclaw/media/`，支持通过Telegram发送）

## 可用模型  
- `grok-imagine-image` — 标准质量，生成速度较快  
- `grok-imagine-image-pro` — 更高质量（默认模型）

## 1. 图像生成  
```bash
curl -s https://api.x.ai/v1/images/generations \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "grok-imagine-image-pro",
    "prompt": "<PROMPT>",
    "n": 1,
    "response_format": "b64_json"
  }' | python3 -c "
import json, sys, base64, os, time
os.makedirs(os.path.expanduser('~/.openclaw/media'), exist_ok=True)
r = json.load(sys.stdin)
ts = int(time.time())
for i, img in enumerate(r['data']):
    img_data = base64.b64decode(img['b64_json'])
    fpath = os.path.expanduser(f'~/.openclaw/media/generated_{ts}_{i}.png')
    with open(fpath, 'wb') as f:
        f.write(img_data)
    print(fpath)
"
```  

### 宽高比  
在JSON请求体中添加 `"aspect_ratio": "<ratio>"`。支持的宽高比值如下：  
| 宽高比 | 适用场景 |  
|-------|----------|  
| `1:1` | 社交媒体、缩略图 |  
| `16:9` / `9:16` | 宽屏显示、移动端内容 |  
| `4:3` / `3:4` | 演示文稿、肖像照片 |  
| `3:2` / `2:3` | 摄影作品 |  
| `2:1` / `1:2` | 流行广告、页面标题 |  
| `auto` | 模型自动选择最佳宽高比（默认） |

### 批量生成  
设置 `"n": <count>`（1-10），可一次生成多张图片。

## 2. 图像编辑/风格转换  
通过提供源图片和编辑指令来编辑现有图片。  
使用相同的 `/v1/images/generations` 端点，并添加 `image_url` 字段。  
**请勿使用 `/v1/images/edits` 端点进行多部分数据上传——xAI仅支持JSON格式。**  

**重要提示：** 对于本地文件，需使用Python生成JSON请求数据，然后通过 `curl` 命令发送。  
在 `curl` 命令中直接使用Base64编码会导致“参数列表过长”的错误（尤其是对于超过100KB的图片）。  

**注意：** 这并非真正的图像编辑功能——该API仅根据源图片生成新的图片，无法进行像素级的精确修改（例如仅更改汽车的颜色而保持其他部分不变）。  

### 从本地文件编辑（推荐方式）：  
```bash
python3 -c "
import json, base64
with open('<SOURCE_PATH>', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
payload = {
    'model': 'grok-imagine-image',
    'prompt': '<EDIT_PROMPT>',
    'image_url': f'data:image/png;base64,{b64}',
    'n': 1,
    'response_format': 'b64_json'
}
with open('/tmp/img_edit_payload.json', 'w') as f:
    json.dump(payload, f)
print('Payload ready')
" && \
curl -s https://api.x.ai/v1/images/generations \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/img_edit_payload.json | python3 -c "
import json, sys, base64, os, time
os.makedirs(os.path.expanduser('~/.openclaw/media'), exist_ok=True)
r = json.load(sys.stdin)
img_data = base64.b64decode(r['data'][0]['b64_json'])
fpath = os.path.expanduser(f'~/.openclaw/media/edited_{int(time.time())}.png')
with open(fpath, 'wb') as f:
    f.write(img_data)
print(fpath)
"
```  

### 从URL编辑：  
```bash
curl -s https://api.x.ai/v1/images/generations \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "grok-imagine-image",
    "prompt": "<EDIT_PROMPT>",
    "image_url": "<PUBLIC_IMAGE_URL>",
    "n": 1,
    "response_format": "b64_json"
  }' | python3 -c "
import json, sys, base64, os, time
os.makedirs(os.path.expanduser('~/.openclaw/media'), exist_ok=True)
r = json.load(sys.stdin)
img_data = base64.b64decode(r['data'][0]['b64_json'])
fpath = os.path.expanduser(f'~/.openclaw/media/edited_{int(time.time())}.png')
with open(fpath, 'wb') as f:
    f.write(img_data)
print(fpath)
"
```  

### 风格转换示例：  
- “将此图片渲染为印象派风格的油画”  
- “将其转换为具有详细阴影效果的素描”  
- “将其转换为色彩鲜艳的波普艺术风格”  
- “将其转换为边缘柔和的水彩画”

## 3. 发送到Telegram  
```
message tool: action=send, channel=telegram, target=<id>,
  message="<caption>", filePath=~/.openclaw/media/<file>.png
```  
- 必须包含 `message` 字段（即使仅发送图片时也必须填写）  
- 允许的图片存储路径：`/tmp/`, `~/.openclaw/media/`, `~/.openclaw/agents/`  

## 其他注意事项：  
- **请勿传递 `size` 参数**——系统会返回默认尺寸（400像素）。  
- 宽高比：在JSON请求体中设置 `aspect_ratio`。  
- 编辑操作：使用 `generations` 端点中的 `image_url` 字段（而非 `edits` 端点）。  
- **务必使用 `"response_format": "b64_json"`**——URL格式返回的临时链接可能无法长期使用（可能会被403错误阻止访问）。  
- 对于大型图片：使用Python生成JSON数据，保存到 `/tmp/` 目录，再通过 `curl` 命令发送。  
- 每次请求最多可发送10张图片。  
- 图片内容可能会经过审核。  
- 此功能仅支持风格转换或重新构想，并非像素级的精确修复。