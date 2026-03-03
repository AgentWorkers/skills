---
name: pixverse
description: 使用 Pixverse API 生成 AI 视频
homepage: https://pixverse.ai/
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      env: ["PIXVERSE_API_KEY"]
    primaryEnv: "PIXVERSE_API_KEY"
---
# Pixverse 视频生成

使用 Pixverse API 生成 AI 视频。

## 设置

1. 从 https://pixverse.ai/ 获取您的 API 密钥。
2. 设置环境变量：
   ```bash
   export PIXVERSE_API_KEY="your-api-key-here"
   ```
   或将其添加到 `~/.openclaw/openclaw.json` 文件中：
   ```json
   {
     "skills": {
       "pixverse": {
         "env": {
           "PIXVERSE_API_KEY": "your-api-key-here"
         }
       }
     }
   }
   ```

## 使用方法

### 根据文本提示生成视频

```bash
curl -X POST https://api.pixverse.ai/v1/generate \
  -H "Authorization: Bearer $PIXVERSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A group of hackers coding intensely in a futuristic lab",
    "aspect_ratio": "16:9",
    "duration": 4,
    "style": "realistic"
  }'
```

### 根据图片生成视频

```bash
curl -X POST https://api.pixverse.ai/v1/generate \
  -H "Authorization: Bearer $PIXVERSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.png",
    "prompt": "Make this image come alive with motion",
    "duration": 4
  }'
```

### 检查视频状态

```bash
curl -X GET https://api.pixverse.ai/v1/tasks/{task_id} \
  -H "Authorization: Bearer $PIXVERSE_API_KEY"
```

### 下载视频

任务完成后，从响应中下载视频 URL。

## 参数

- **prompt**：视频的文本描述（必填）
- **image_url**：起始图片的 URL（可选）
- **aspect_ratio**："16:9", "9:16", "1:1"（默认值："16:9")
- **duration**：2-8 秒（默认值：4 秒）
- **style**："realistic", "anime", "3d", "cinematic"（默认值："realistic")
- **motion_strength**：0-10（默认值：5）

## 注意事项

⚠️ **重要提示**：
- 这只是一个模板技能。您需要验证实际的 Pixverse API 端点。
- Pixverse 可能需要不同的认证方式或具有不同的 API 结构。
- 请访问 https://docs.pixverse.ai/ 查看最新的 API 文档。
- 视频生成可能需要 1-5 分钟，具体取决于视频的复杂度。

## 替代方案：Web UI 自动化

如果无法使用 API，可以考虑使用浏览器自动化工具来与 Pixverse 的 Web 界面进行交互。