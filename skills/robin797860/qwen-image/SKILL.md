---
name: qwen-image
description: 使用 Qwen Image API（阿里云 DashScope）生成图像。适用于用户需要根据中文提示生成图像，或从文本描述中获取高质量 AI 生成图像的场景。
homepage: https://dashscope.aliyuncs.com/
metadata: {"openclaw":{"emoji":"🎨","requires":{"bins":["uv"]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# Qwen Image

使用阿里云的 Qwen Image API（通义万相）生成高质量图像。

## 使用方法

**仅生成图像（返回图像 URL）：**
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "一副典雅庄重的对联悬挂于厅堂之中" --size "1664*928" --api-key sk-xxx
```

**生成并本地保存图像：**
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "一副典雅庄重的对联悬挂于厅堂之中" --size "1664*928" --api-key sk-xxx
```

**使用自定义模型：**
支持以下模型：`qwen-image-max-2025-12-30`、`qwen-image-plus-2026-01-09`、`qwen-image-plus`
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "a beautiful sunset over mountains" --model qwen-image-plus-2026-01-09 --api-key sk-xxx
```

## API 密钥
您可以按照以下顺序获取 API 密钥并运行图像生成命令：

- 从 `~/.openclaw/openclaw.json` 文件中的 `modelsproviders.bailian.apiKey` 获取 API 密钥
- 或从 `~/.openclaw/openclaw.json` 文件中的 `skills."qwen-image".apiKey` 获取 API 密钥
- 或从 `DASHSCOPE_API_KEY` 环境变量中获取 API 密钥
- 或从以下链接获取 API 密钥：https://dashscope.console.aliyun.com/

## 选项
**尺寸：**
- `1664*928`（默认） - 16:9 横屏格式
- `1024*1024` - 正方形格式
- `720*1280` - 9:16 纵屏格式
- `1280*720` - 更小的 16:9 横屏格式

**其他参数：**
- `--negative-prompt "unwanted elements"` - 指定需要避免的元素
- `--no-prompt-extend` - 禁用自动提示优化功能
- `--watermark` - 在生成的图像中添加水印
- `--no-verify-ssl` - 禁用 SSL 证书验证（在企业代理后使用时使用）

## 工作流程：
1. 使用用户的提示信息执行 `generate_image.py` 脚本
2. 解析脚本输出，找到以 `MEDIA_URL:` 开头的行
3. 从该行中提取图像 URL（格式：`MEDIA_URL: https://...`)
4. 使用 markdown 语法显示图像：`![生成的图像](URL)`
5. 除非用户特别要求，否则不要下载或保存图像

## 注意事项：
- 支持中文和英文提示
- 默认情况下，仅返回图像 URL，不进行下载
- 脚本会在输出中打印 `MEDIA_URL:`，请提取该 URL 并使用 markdown 语法显示图像：`![生成的图像](URL)`
- 始终在脚本输出中查找以 `MEDIA_URL:` 开头的行，并为用户显示相应的图像
- 默认的负向提示功能有助于避免常见的 AI 生成图像中的瑕疵
- 图像存储在阿里云 OSS 上，访问 URL 为临时链接