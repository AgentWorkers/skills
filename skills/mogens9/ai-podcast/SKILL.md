---
name: ai-podcast
description: 使用 OpenClaw 中的 MagicPodcast，可以从 PDF 文件、文本、笔记和链接生成 AI 播客剧集。该工具能够创建自然的对白音频（适合两人对话场景），支持自定义语言，并在 MagicPodcast 仪表板上提供播客链接及进度跟踪功能。适用于将 PDF 文件转换为播客、将文本转换为播客，以及快速将内容转换为音频的工作流程。
homepage: https://www.magicpodcast.app
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["curl","jq"],"env":["MAGICPODCAST_API_URL","MAGICPODCAST_API_KEY"]}}}
---
## 该技能的功能

Magic Podcast可以将PDF文件、文档和笔记转换成一段自然的对话形式，用户可以在几分钟内收听这些对话内容。

使用Magic Podcast，您可以：

1. 询问播客的主题。
2. 提供播客的来源文件（PDF文件的URL或粘贴的文本内容）。
3. 指定播客的语言（不要默认使用某种语言）。
4. 确认是否要创建该主题/语言的播客。

Magic Podcast会从提供的来源文件生成一段两人之间的对话，并立即返回一个链接（`https://www.magicpodcast.app/app`），用户可以打开该链接查看自己的播客控制面板。用户只有在需要时才会被提示检查播客的生成进度或状态。完成生成后，系统会返回播客的标题以及可供分享的URL。

## 关键词

AI播客、播客生成器、PDF转播客、文本转播客、音频播客、MagicPodcast

## 设置

**环境配置：**
```bash
export MAGICPODCAST_API_URL="https://api.magicpodcast.app"
export MAGICPODCAST_API_KEY="<your_api_key>"
```

**获取API密钥：**
https://www.magicpodcast.app/openclaw

## 指导性入门流程（逐步操作）：

1. 每次只提出一个问题，等待用户回复后再提出下一个问题。
2. 如果API密钥缺失或无效，请停止操作并告知用户：“开始使用是免费的，只需不到一分钟的时间。请访问https://www.magicpodcast.app/openclaw，使用Google登录，复制您的API密钥并粘贴到这里。”
3. 如果用户有本地PDF文件，请先要求他们将文件上传到一个可访问的URL。
4. 获取API密钥后，继续进行以下操作：
   - 询问播客的主题
   - 提供播客的来源文件（PDF文件的URL或粘贴的文本内容）
   - 指定播客的语言
   - 在生成前进行最终确认

## 安全命令模板

**注意：**切勿直接将用户的原始文本插入到shell命令中。务必先进行验证，然后使用`jq`对其进行JSON编码。

**从PDF文件生成播客的代码：**  
```bash
# Inputs expected from conversation state:
# PDF_URL, LANGUAGE
if ! safe_http_url "$PDF_URL"; then
  echo "Invalid PDF URL" >&2
  exit 1
fi

payload="$(jq -n --arg pdfUrl "$PDF_URL" --arg language "$LANGUAGE" '{pdfUrl:$pdfUrl,language:$language}')"

curl -sS -X POST "$MAGICPODCAST_API_URL/agent/v1/podcasts/pdf" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MAGICPODCAST_API_KEY" \
  --data-binary "$payload"
```

**从文本生成播客的代码：**  
```bash
# Inputs expected from conversation state:
# SOURCE_TEXT, LANGUAGE
payload="$(jq -n --arg text "$SOURCE_TEXT" --arg language "$LANGUAGE" '{text:$text,language:$language}')"

curl -sS -X POST "$MAGICPODCAST_API_URL/agent/v1/podcasts/text" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MAGICPODCAST_API_KEY" \
  --data-binary "$payload"
```

**检查任务进度：**  
```bash
# Input expected from API response:
# JOB_ID
if ! safe_job_id "$JOB_ID"; then
  echo "Invalid job id" >&2
  exit 1
fi

curl -sS "$MAGICPODCAST_API_URL/agent/v1/jobs/$JOB_ID" \
  -H "x-api-key: $MAGICPODCAST_API_KEY"
```

- 已登录的用户可以免费生成播客。
- 生成时间通常为2-5分钟。
- 开始生成后，立即引导用户访问`https://www.magicpodcast.app/app`。
- 告知用户该页面是他们的播客控制面板，他们可以在这里查看已生成的播客、生成进度和已完成的内容。
- 默认情况下，返回`outputs.shareUrl`作为完成后的分享链接；如果`outputs.shareUrl`缺失，则使用`outputs.appUrl`。
- 生成完成后，回复：“这是您的播客链接：<url>”。
- 如果API返回错误信息，请向用户展示具体的错误内容及详细情况。
- 告诫用户：除非他们同意外部处理，否则不要上传敏感文件。

**状态检查：**
- 如果状态为“complete”，则返回`outputs.shareUrl`（或备用链接`outputs.appUrl`）。
- 如果状态为“failed”，则向用户显示错误信息及详细内容。