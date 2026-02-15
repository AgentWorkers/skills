---
name: youtube-shorts-automation
description: **YouTube Shorts 自动生成与上传流程：**  
利用 Deevid AI Agent 将图片转换为包含背景音乐和语音的视频，随后将其上传至 YouTube。该流程可通过 Cron Job 每日自动执行。  
**适用场景：**  
- 生成短视频（竖版视频）  
- 创作 AI 生成的视频内容  
- 上传视频至 YouTube Shorts  
- 自动化日常视频内容的生成与上传流程
---

# YouTube Shorts 自动化

使用 Deevid AI 生成图片/视频，然后自动上传到 YouTube Shorts 的自动化流程。

## 整体工作流程

```
1. 이미지 생성 (Deevid AI)
2. Agent 영상 생성 (Deevid Agent — 오디오 포함)
3. 영상 다운로드
4. YouTube 업로드
5. (선택) Telegram으로 결과 전송
```

## 核心规则

- **⚠️ 禁止使用“将图片转换为视频”的工具**：否则生成的视频将没有声音。
- **✅ 使用 Deevid Agent**（`https://deevid.ai/ko/agent`）：生成的视频包含背景音乐和对话。
- 视频比例：**9:16**（竖屏格式，符合 YouTube Shorts 的要求）。
- 视频时长：**60 秒以内**（建议 8–10 秒）。

## 设置文件结构

各频道的相关设置以 JSON 格式进行管理。示例：[references/config_example.json](references/config_example.json)

必填字段：
- `channel`：频道名称
- `deevid.prompt`：用于生成图片的提示语（需指定为 9:16 纵屏格式）
- `youtube.title_template`：上传视频的标题（包含 `#shorts` 标签）
- `youtube.description_template`：上传视频的描述
- `youtube.tags`：用逗号分隔的标签

## 分步执行流程

### 1. 生成图片
在 Deevid AI 的网站上生成图片。提示语中必须包含 “9:16 vertical format”。
- 费用：每张图片需要 6 个信用点。
- 详情：[references/deevid-agent-workflow.md](references/deevid-agent-workflow.md)

### 2. 使用 Deevid Agent 生成视频
将生成的图片上传到 Deevid Agent，并提供相应的提示语，然后生成视频（生成时间约为 2–5 分钟）。
- 费用：每 8 秒视频需要 20 个信用点。
- 使用的模型：Start Image Master V2.0
- 详情：[references/deevid-agent-workflow.md](references/deevid-agent-workflow.md)

### 3. 上传视频到 YouTube
```bash
python3 scripts/youtube_upload.py \
  --file video.mp4 \
  --title "제목 #shorts" \
  --description "설명" \
  --tags "tag1,tag2"
```
- 需要预先设置 `client_secret.json` 和 `token.json` 文件。
- 详情：[references/youtube-upload.md](references/youtube-upload.md)

### 4. 注册 Cronjob（使用 OpenClaw）
设置定时任务，在指定时间通过 isolated session 运行整个工作流程。
Cronjob 的 payload 中需要包含整个工作流程的描述以及相关环境路径。

## 故障排除

| 问题 | 原因 | 解决方法 |
|------|------|------|
| 视频没有声音 | 使用了“将图片转换为视频”的工具 | 更改为使用 Deevid Agent 生成视频 |
| 上传失败 | `token.json` 过期 | 重新认证或刷新 token |
| Deevid 登录失效 | 会话过期 | 重新在浏览器中登录 |
| 无法提取视频 URL | SPA 渲染延迟 | 增加等待时间 |