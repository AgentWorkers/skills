---
name: gamma
description: 使用 Gamma 的 AI API 创建演示文稿、文档、社交媒体帖子和网站。当需要通过 Gamma 创建幻灯片、演示文稿、文档或网页内容时，请使用该 API。
---

# Gamma API 技能

通过 Gamma 的 API 以编程方式创建演示文稿和文档。

## 设置

1. 从 [https://developers.gamma.app](https://developers.gamma.app) 获取 API 密钥。
2. 将密钥存储在环境变量中：`export GAMMA_API_KEY=sk-gamma-xxx`
   或者将其添加到 `TOOLS.md` 文件中：`Gamma API Key: sk-gamma-xxx`

## 认证

```
Base URL: https://public-api.gamma.app/v1.0
Header: X-API-KEY: <your-api-key>
```

## 生成内容

```bash
curl -X POST https://public-api.gamma.app/v1.0/generations \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $GAMMA_API_KEY" \
  -d '{
    "inputText": "Your content here",
    "textMode": "generate|condense|preserve",
    "format": "presentation|document|social|webpage"
  }'
```

**响应：** `{"generationId": "xxx"}`

## 检查状态

```bash
curl https://public-api.gamma.app/v1.0/generations/<generationId> \
  -H "X-API-KEY: $GAMMA_API_KEY"
```

**响应（已完成）：** `{"status": "completed", "gammaUrl": "https://gamma.app/docs/xxx", "credits": {...}}`

每隔 10-20 秒检查一次状态，直到状态变为 “completed”。

## 关键参数

| 参数 | 值 | 说明 |
|-----------|--------|-------|
| `textMode` | `generate`, `condense`, `preserve` | `generate`：展开内容；`condense`：简化内容；`preserve`：保留原始格式 |
| `format` | `presentation`, `document`, `social`, `webpage` | 输出类型 |
| `numCards` | 1-60（标准版），1-75（高级版） | 幻灯片/卡片数量 |
| `cardSplit` | `auto`, `inputTextBreaks` | 在 `inputText` 中使用 `\n---\n` 来手动分隔内容 |
| `exportAs` | `pdf`, `pptx` | 可选的导出格式 |

## 可选参数

```json
{
  "additionalInstructions": "Make titles catchy",
  "imageOptions": {
    "source": "aiGenerated|unsplash|giphy|webAllImages|noImages",
    "model": "imagen-4-pro|flux-1-pro",
    "style": "photorealistic, modern"
  },
  "textOptions": {
    "amount": "brief|medium|detailed|extensive",
    "tone": "professional, inspiring",
    "audience": "tech professionals",
    "language": "en"
  },
  "cardOptions": {
    "dimensions": "fluid|16x9|4x3|1x1|4x5|9x16"
  }
}
```

注意：当 `textMode` 为 `preserve` 时，`textOptions.tone` 和 `textOptions.audience` 参数将被忽略。

## 其他端点

- `GET /themes` — 列出可用的主题（在生成内容时使用 `themeId`）
- `GET /folders` — 列出文件夹（在生成内容时使用 `folderIds`）

## 工作流程

1. 检查环境变量或 `TOOLS.md` 中是否已设置 API 密钥（`$GAMMA_API_KEY`）。
2. 使用内容构建 `inputText`（可以包含内联的图片链接）。
3. 向 `/generations` 发送 POST 请求以获取 `generationId`。
4. 不断检查 `/generations/{id}` 的状态，直到状态变为 “completed”。
5. 将生成的文档链接（`gammaUrl`）返回给用户。