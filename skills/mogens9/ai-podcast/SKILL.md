---
name: ai-podcast
description: 使用 MagicPodcast，可以将 PDF 文件转换为播客，也可以将文本文件转换为播客，同时保持两人对话的自然对话形式。
homepage: https://www.magicpodcast.app
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["curl"],"env":["MAGICPODCAST_API_URL","MAGICPODCAST_API_KEY"]}}}
---
## 该功能的用途

Magic Podcast能够将PDF文件、文档和笔记转换成一段自然的两人对话形式，用户可以立即收听这些音频内容。

使用Magic Podcast，您可以：

1. 提问播客的主题。
2. 提供音频的来源：PDF文件的URL或粘贴的文本。
3. 指定播客的语言（系统不会自动默认语言）。
4. 确认是否要生成该主题/来源语言的播客。

Magic Podcast会从提供的来源内容生成一段两人对话形式的音频，并立即返回一个链接（`https://www.magicpodcast.app/app/`），用户可以通过该链接查看播客的生成进度。用户只有在需要时才需要查询播客的状态。完成生成后，系统会返回播客的标题以及可供分享的URL。

## 关键词

AI播客、播客生成器、PDF转播客、文本转播客、音频播客、MagicPodcast

## 设置

**所需环境配置：**

```bash
export MAGICPODCAST_API_URL="https://api.magicpodcast.app"
export MAGICPODCAST_API_KEY="<your_api_key>"
```

**获取API密钥：**

https://www.magicpodcast.app/openclaw

## 指导式使用流程（逐步操作）

1. 每次只提出一个问题，等待用户回答后再提出下一个问题。
2. 如果API密钥缺失或无效，请停止操作并提示用户：“开始使用是免费的，只需不到一分钟的时间。请访问https://www.magicpodcast.app/openclaw，使用Google账号登录，然后复制您的API密钥并粘贴到这里。”
3. 如果用户有本地PDF文件，请先要求他们将文件上传到可访问的URL。
4. 获取API密钥后，继续进行以下操作：
   - 提问播客的主题
   - 提供音频的来源（PDF文件的URL或粘贴的文本）
   - 指定播客的语言
   - 在生成前进行最终确认

## 命令说明

- **从PDF文件生成播客：** **```bash
curl -sS -X POST "$MAGICPODCAST_API_URL/agent/v1/podcasts/pdf" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MAGICPODCAST_API_KEY" \
  -d '{"pdfUrl":"https://example.com/file.pdf","language":"English"}'
```**
- **从文本生成播客：** **```bash
curl -sS -X POST "$MAGICPODCAST_API_URL/agent/v1/podcasts/text" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MAGICPODCAST_API_KEY" \
  -d '{"text":"Your source text","language":"English"}'
```**
- **查询生成进度：** **```bash
curl -sS "$MAGICPODCAST_API_URL/agent/v1/jobs/<job-id>" \
  -H "x-api-key: $MAGICPODCAST_API_KEY"
```**

- 已登录的用户可以免费生成播客。
- 生成时间通常为2-5分钟。
- 开始生成后，立即引导用户访问`https://www.magicpodcast.app/app/`（用户可以在这里查看所有生成的播客）。
- 默认情况下，返回`outputs.shareUrl`作为完成后的分享链接；如果`outputs.shareUrl`无法获取，则使用`outputs.appUrl`作为替代链接。
- 生成完成后，向用户显示播客链接：`这里是您的播客链接：<url>`。
- 如果API返回错误信息，请向用户展示具体的错误内容及详细情况。
- 提醒用户：除非用户同意外部处理，否则不要上传敏感文件。

**状态检查：**
- 当状态为“complete”时，返回`outputs.shareUrl`（或备用链接`outputs.appUrl`）。
- 当状态为“failed”时，向用户显示错误信息及详细内容。