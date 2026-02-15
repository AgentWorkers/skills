---
name: llmwhisperer
description: 使用 LLMWhisperer API 从图像和 PDF 文件中提取文本和布局信息。该技术适用于处理手写内容以及结构复杂的表格。
metadata: {"clawdbot":{"emoji":"📄","scripts":["scripts/llmwhisperer"]}}
---

# LLMWhisperer

使用 [LLMWhisperer API](https://unstract.com/llmwhisperer/) 从图片和 PDF 文件中提取文本——非常适合处理手写内容及复杂的表格。

## 配置

需要在 `~/.clawdbot/.env` 文件中设置 `LLMWHISPERER_API_KEY`：
```bash
echo "LLMWHISPERER_API_KEY=your_key_here" >> ~/.clawdbot/.env
```

### 获取 API 密钥
您可以在 [unstract.com/llmwhisperer](https://unstract.com/llmwhisperer/) 免费获取 API 密钥。
- **免费 tier：** 每天 100 页

## 使用方法

```bash
llmwhisperer <file>
```

## 脚本来源

可执行脚本位于 `scripts/llmwhisperer` 目录下。

```bash
#!/bin/bash
# Extract text using LLMWhisperer API

if [ -z "$LLMWHISPERER_API_KEY" ]; then
  if [ -f ~/.clawdbot/.env ]; then
    # shellcheck disable=SC2046
    export $(grep -v '^#' ~/.clawdbot/.env | grep 'LLMWHISPERER_API_KEY' | xargs)
  fi
fi

if [ -z "$LLMWHISPERER_API_KEY" ]; then
  echo "Error: LLMWHISPERER_API_KEY not found in env or ~/.clawdbot/.env"
  exit 1
fi

FILE="$1"
if [ -z "$FILE" ]; then
  echo "Usage: $0 <file>"
  exit 1
fi

curl -s -X POST "https://llmwhisperer-api.us-central.unstract.com/api/v2/whisper?mode=high_quality&output_mode=layout_preserving" \
  -H "Content-Type: application/octet-stream" \
  -H "unstract-key: $LLMWHISPERER_API_KEY" \
  --data-binary "@$FILE"
```

## 示例

**将文本输出到终端：**
```bash
llmwhisperer flyer.jpg
```

**将输出结果保存到文本文件：**
```bash
llmwhisperer invoice.pdf > invoice.txt
```

**处理手写笔记：**
```bash
llmwhisperer notes.jpg
```