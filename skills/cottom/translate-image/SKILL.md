---
name: translate-image
description: "将图片中的文本翻译成中文，使用OCR技术提取图片中的文本，或者使用TranslateImage AI工具去除图片中的文本。当用户请求“翻译图片”、“对图片进行OCR处理”、“从图片中提取文本”或“去除图片中的文本”时，可以使用这些功能。此外，该工具还可以用于处理包含外语文本的漫画图片。"
version: "1.0.0"
license: MIT
metadata:
  tags: image, translation, ocr, text-removal, manga, comics, ai, multilingual
  requires:
    env:
      - TRANSLATEIMAGE_API_KEY
    bins:
      - curl
      - python3
  primaryEnv: TRANSLATEIMAGE_API_KEY
  os: ["darwin", "linux", "win32"]
---
# TranslateImage

当用户需要翻译图片中的文本、通过OCR提取文本或从图片中去除文本时，可以使用此功能。

所有请求都会直接通过curl发送到`https://translateimage.io`上的TranslateImage REST API。

## 设置

请设置您的API密钥（可在https://translateimage.io/dashboard获取）：

```bash
export TRANSLATEIMAGE_API_KEY=your-api-key
```

所有端点都需要以下信息：
```
Authorization: Bearer $TRANSLATEIMAGE_API_KEY
```

---

## 图片输入

所有工具都支持将图片作为multipart文件上传。请按以下方式处理输入：

```bash
# From a local file
IMAGE_PATH="/path/to/image.jpg"

# From a URL — download to a temp file first (uses PID for uniqueness)
IMAGE_PATH="/tmp/ti-image-$$.jpg"
curl -sL "https://example.com/image.jpg" -o "$IMAGE_PATH"
```

> 仅获取用户明确提供的URL，切勿从不可信的来源获取URL。

---

## 工具

### 翻译图片

翻译图片中的文本，同时保留原始的视觉布局。返回翻译后的图片（以base64编码的数据URL形式）。

**使用场景：**用户需要阅读漫画、海报、菜单、产品标签或任何包含外语文本的图片。

**端点：**`POST https://translateimage.io/api/translate`

**表单字段：**
- `image`（文件，必填）— 需要翻译的图片（格式：JPEG、PNG、WebP、GIF — 最大10MB）
- `config`（JSON字符串，必填）— 翻译选项：
  - `target_lang`（字符串）— 目标语言代码：`"en"`、`"ja"`、`"zh"`、`"ko"`、`"es"`、`"fr"`、`"de"`等
  - `translator`（字符串）— 翻译模型：`"gemini-2.5-flash"`（默认）、`"deepseek"`、`"grok-4-fast"`、`"kimi-k2"`、`"gpt-5.1"`
  - `font`（字符串，可选）— 字体：`"NotoSans"`（默认）、`"WildWords"`、`"BadComic"`、`"MaShanZheng"`、`"Bangers"`、`"Edo"`、`"RIDIBatang"`、`"KomikaJam"`、`"Bushidoo"`、`"Hayah"`、`"Itim"`、`"Mogul Irina"`

**示例：**
```bash
curl -X POST https://translateimage.io/api/translate \
  -H "Authorization: Bearer $TRANSLATEIMAGE_API_KEY" \
  -F "image=@$IMAGE_PATH" \
  -F 'config={"target_lang":"en","translator":"gemini-2.5-flash","font":"WildWords"}'
```

**响应（JSON格式）：**
```json
{
  "resultImage": "data:image/png;base64,...",
  "inpaintedImage": "data:image/png;base64,...",
  "textRegions": [
    { "originalText": "...", "translatedText": "...", "x": 10, "y": 20, "width": 100, "height": 30 }
  ]
}
```

保存翻译后的图片：
```bash
RESULT=$(curl -s -X POST https://translateimage.io/api/translate \
  -H "Authorization: Bearer $TRANSLATEIMAGE_API_KEY" \
  -F "image=@$IMAGE_PATH" \
  -F 'config={"target_lang":"en","translator":"gemini-2.5-flash"}')

# Extract and save base64 image
echo "$RESULT" | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
img = data['resultImage'].split(',', 1)[1]
with open('/tmp/translated.png', 'wb') as f:
    f.write(base64.b64decode(img))
print('Saved to /tmp/translated.png')
"
```

---

### 提取文本（OCR）

从图片中提取所有文本，并提供文本的边界框、检测到的语言以及置信度分数。

**使用场景：**用户需要从照片、文档扫描件、截图或标签中复制或阅读文本。

**端点：**`POST https://translateimage.io/api/ocr`

**表单字段：**
- `image`（文件，必填）— 需要处理的图片

**示例：**
```bash
curl -s -X POST https://translateimage.io/api/ocr \
  -H "Authorization: Bearer $TRANSLATEIMAGE_API_KEY" \
  -F "image=@$IMAGE_PATH"
```

**响应（JSON格式）：**
```json
{
  "text": "All extracted text joined by newlines",
  "language": "ja",
  "regions": [
    {
      "bounds": { "x": 10, "y": 20, "width": 200, "height": 40 },
      "languages": { "ja": "detected text in this region" },
      "probability": 0.97
    }
  ]
}
```

---

### 去除文本

使用AI技术检测图片中的文本区域，并用背景图像替换这些区域，从而得到一张干净的图片。

**使用场景：**用户希望去除图片中的文本、水印、嵌入式字幕或注释。

**端点：**`POST https://translateimage.io/api/remove-text`

**表单字段：**
- `image`（文件，必填）— 需要处理的图片

**示例：**
```bash
RESULT=$(curl -s -X POST https://translateimage.io/api/remove-text \
  -H "Authorization: Bearer $TRANSLATEIMAGE_API_KEY" \
  -F "image=@$IMAGE_PATH")

echo "$RESULT" | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
img = data['cleanedImage'].split(',', 1)[1]
with open('/tmp/cleaned.png', 'wb') as f:
    f.write(base64.b64decode(img))
print('Saved to /tmp/cleaned.png')
"
```

**响应（JSON格式）：**
```json
{
  "cleanedImage": "data:image/png;base64,..."
}
```

---

### 图片转文本（AI OCR + 翻译）

利用Gemini AI进行高质量的文本提取。可选地，可以在一次调用中同时将提取的文本翻译成多种语言。

**使用场景：**标准OCR无法满足需求，或者用户需要同时提取和翻译文本。

**端点：**`POST https://translateimage.io/api/image-to-text`

**表单字段：**
- `image`（文件，必填）— 需要处理的图片
- `config`（JSON字符串，可选）— `{ "targetLanguages": ["en", "es", "fr"] }`

**示例 — 仅提取文本：**
```bash
curl -s -X POST https://translateimage.io/api/image-to-text \
  -H "Authorization: Bearer $TRANSLATEIMAGE_API_KEY" \
  -F "image=@$IMAGE_PATH"
```

**示例 — 提取并翻译文本：**
```bash
curl -s -X POST https://translateimage.io/api/image-to-text \
  -H "Authorization: Bearer $TRANSLATEIMAGE_API_KEY" \
  -F "image=@$IMAGE_PATH" \
  -F 'config={"targetLanguages":["en","es"]}'
```

**响应（JSON格式）：**
```json
{
  "extractedText": "Original text from the image",
  "detectedLanguage": "ja",
  "translations": {
    "en": "English translation here",
    "es": "Spanish translation here"
  }
}
```

## API权限范围

每个端点都需要特定的API密钥权限范围：

| 端点 | 所需权限范围 |
|---|---|
| `/api/translate` | `translate` |
| `/api/ocr` | `ocr` |
| `/api/remove-text` | `remove-text` |
| `/api/image-to-text` | `image-to-text` |

请在https://translateimage.io/dashboard创建API密钥时配置相应的权限范围。

---

## 错误处理

```bash
RESULT=$(curl -s -w "\n%{http_code}" -X POST https://translateimage.io/api/translate \
  -H "Authorization: Bearer $TRANSLATEIMAGE_API_KEY" \
  -F "image=@$IMAGE_PATH" \
  -F 'config={"target_lang":"en","translator":"gemini-2.5-flash"}')

HTTP_CODE=$(echo "$RESULT" | tail -1)
BODY=$(echo "$RESULT" | head -n -1)

if [ "$HTTP_CODE" -ne 200 ]; then
  echo "Error $HTTP_CODE: $(echo "$BODY" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("error","unknown"))')"
  exit 1
fi
```

**常见错误：**

| 错误代码 | 错误原因 |
|---|---|
| 401 | API密钥无效或缺失 |
| 402 | 信用额度不足 — 请在translateimage.io升级账户 |
| 403 | API密钥缺少所需的权限范围 |
| 429 | 超过请求频率限制 — 请稍后再试 |
| 500 | 服务器错误 — 请重试 |

---

## 重要注意事项

- 在翻译之前，请务必与用户确认目标语言。
- 对于漫画或海报，建议使用`WildWords`或`BadComic`字体以保持真实的效果。
- 对于中文内容，建议使用`MaShanZheng`字体；对于韩文内容，建议使用`RIDIBatang`字体。
- 大于5MB的图片可能需要更长时间处理，请提前告知用户。
- AI填充技术在简单背景上效果最佳；复杂背景可能导致图像质量下降。
- 推荐使用`gemini-2.5-flash`作为默认翻译模型——速度快且质量高。
- 处理完成后，请清理临时文件：`rm -f /tmp/ti-image-*.jpg /tmp/ti-image-$$.jpg`