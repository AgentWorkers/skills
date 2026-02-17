---
name: azure-image-gen
description: 使用 Azure OpenAI DALL-E 生成图像。支持批量生成、自定义提示，并输出图像画廊。
metadata:
  author: kai
  version: "1.0.0"
  tags:
    - image generation
    - azure
    - dall-e
    - ai art
---
# Azure 图像生成

使用 Azure OpenAI 的 DALL-E 功能生成图像。

## 设置

### 必需的环境变量

```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_DALLE_DEPLOYMENT="your-dalle-deployment-name"
```

或者可以在 `skill` 目录下创建一个 `.env` 文件来存储这些环境变量。

### API 版本

默认值：`2024-02-01`（支持 DALL-E 3）

## 使用方法

### 基本生成

```bash
python3 /Users/abhi/clawd/skills/azure-image-gen/scripts/generate.py --prompt "A futuristic city at sunset"
```

### 生成多张图像

```bash
python3 /Users/abhi/clawd/skills/azure-image-gen/scripts/generate.py \
  --prompt "Professional blog header for a tech startup" \
  --count 4
```

### 自定义图像大小和质量

```bash
python3 /Users/abhi/clawd/skills/azure-image-gen/scripts/generate.py \
  --prompt "Minimalist illustration of cloud computing" \
  --size 1792x1024 \
  --quality hd
```

### 指定输出目录

```bash
python3 /Users/abhi/clawd/skills/azure-image-gen/scripts/generate.py \
  --prompt "Abstract data visualization" \
  --out-dir ./blog-images
```

## 选项

| 选项 | 默认值 | 说明 |
|------|---------|-------------|
| `--prompt` | 必需 | 图像描述 |
| `--count` | 1 | 生成图像的数量 |
| `--size` | 1024x1024 | 图像尺寸：`1024x1024`、`1792x1024`、`1024x1792` |
| `--quality` | standard | 图像质量：`standard` 或 `hd` |
| `--style` | vivid | 图像风格：`vivid` 或 `natural` |
| `--out-dir` | ./azure-images | 输出目录 |
| `--api-version` | 2024-02-01 | Azure OpenAI API 版本 |

## 输出结果

- PNG 格式的图像保存在指定的输出目录中
- 一个 `manifest.json` 文件，用于记录每个图像对应的描述信息
- 一个 `index.html` 文件，用于方便预览生成的图像

## 博文图片提示语示例

对于博客标题图片，可以尝试使用以下提示语：

```
# Tech/SaaS
"Minimalist isometric illustration of cloud migration, blue and white color scheme, clean lines, professional"

# Comparison posts
"Split screen illustration showing old vs new technology, warm vs cool colors, modern flat design"

# How-to guides
"Clean illustration of a step-by-step process, numbered steps floating in space, soft gradients"

# Cost/pricing
"Abstract visualization of savings and growth, upward arrows, green accents, professional business style"
```

## 故障排除

**401 Unauthorized**：请检查您的 `AZURE_OPENAI_API_KEY` 是否正确。

**404 Not Found**：请确认您的 `AZURE_OPENAI_DALLE_DEPLOYMENT` 名称是否与实际配置一致。

**内容策略**：Azure 有严格的内容审核规则。如果提示语被屏蔽，请重新表述您的请求。