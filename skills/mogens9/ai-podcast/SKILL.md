---
name: ai-podcast
description: 使用 MagicPodcast，可以将 PDF 文件转换为播客，也可以将文本文件转换为播客，同时保持两人对话的自然交流格式。
homepage: https://www.magicpodcast.app
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["curl"],"env":["MAGICPODCAST_API_URL","MAGICPODCAST_API_KEY"]}}}
---
## 该技能的功能

Magic Podcast可以将PDF文件、文档和笔记转换成一段自然的对话录音，用户可以在几分钟内收听这些录音。

使用Magic Podcast，您可以：

1. 询问播客的主题。
2. 提供文档的来源：PDF文件的URL或粘贴的文本内容。
3. 指定播客的语言（不要默认使用系统设置的语言）。
4. 确认是否要创建该主题/文档的播客。

Magic Podcast会从提供的来源生成一段两人对话形式的播客，并在生成过程中每20秒更新一次进度。生成完成后，系统会返回播客的标题以及Magic Podcast应用程序的下载链接。

## 关键词

AI播客、播客生成器、PDF转播客、文本转播客、音频播客

## 设置

**所需环境配置：**
```bash
export MAGICPODCAST_API_URL="https://api.magicpodcast.app"
export MAGICPODCAST_API_KEY="<your_api_key>"
```

**获取API密钥：**
https://www.magicpodcast.app/openclaw

## 指导性入门流程（逐步操作）：

1. 每次只提出一个问题，并在用户回复后再提出下一个问题。
2. 如果API密钥缺失或无效，请停止操作并提示用户：“免费开始使用，整个过程不到一分钟。请访问https://www.magicpodcast.app/openclaw，使用Google登录，复制您的API密钥并粘贴到这里。”
3. 如果用户有本地PDF文件，请先要求他们将文件上传到一个可访问的URL。
4. 获取API密钥后，继续进行以下操作：
   1) 选择播客主题
   2) 提供文档来源（PDF文件的URL或粘贴的文本内容）
   3) 选择播客语言
   4) 最终确认是否创建播客

## 命令说明：

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
- **检查生成进度：** **```bash
curl -sS "$MAGICPODCAST_API_URL/agent/v1/jobs/<job-id>" \
  -H "x-api-key: $MAGICPODCAST_API_KEY"
```**
- **每20秒更新一次生成进度（最多检查45次）：** **```bash
for i in $(seq 1 45); do
  RESPONSE=$(curl -sS "$MAGICPODCAST_API_URL/agent/v1/jobs/<job-id>" \
    -H "x-api-key: $MAGICPODCAST_API_KEY")
  echo "$RESPONSE"
  echo "$RESPONSE" | grep -q '"statusLabel":"complete"' && break
  echo "$RESPONSE" | grep -q '"statusLabel":"failed"' && break
  sleep 20
done
```**

- 已登录的用户可以免费生成播客。
- 通常生成时间约为2-5分钟。
- 系统会默认返回`outputs.appUrl`作为完成后的播客下载链接。
- 如果API返回错误信息，系统会显示具体的错误内容及详细原因。
- 请提醒用户：除非他们同意文件被外部处理，否则不要上传敏感文件。

**终端状态说明：**
- 当生成进度为“complete”时，系统会返回`outputs.appUrl`。
- 当生成失败时，系统会向用户显示错误信息及详细原因。