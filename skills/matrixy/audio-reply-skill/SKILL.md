---
name: audio-reply
description: '使用 TTS（文本到语音）功能生成音频回复。输入 “read it to me [URL]” 可以获取指定 URL 的内容并朗读出来；输入 “talk to me [topic]” 可以生成与该主题相关的口语化回复。同时，系统也支持 “speak”、“say it” 和 “voice reply” 等指令。'
homepage: https://github.com/anthropics/claude-code
metadata: {"clawdbot":{"emoji":"🔊","requires":{"bins":["uv"]}}}
---

# 音频回复功能

使用 MLX Audio TTS（chatterbox-turbo 模型）生成语音回复。

## 触发语句

- **“read it to me [URL]”** - 从 URL 获取内容并朗读出来
- **“talk to me [主题/问题]”** - 生成对话式的语音回复
- **“speak”**, **“say it”**, **“voice reply”** - 将你的回复转换为语音

## 使用方法

### 模式 1：读取 URL 内容
```
User: read it to me https://example.com/article
```
1. 使用 WebFetch 获取 URL 内容
2. 提取可读文本（去除 HTML，仅保留主要内容）
3. 使用 TTS 生成音频
4. 播放音频后删除文件

### 模式 2：对话式语音回复
```
User: talk to me about the weather today
```
1. 生成自然、对话式的回复
2. 保持回复简洁（TTS 对较短的文本效果更好）
3. 将文本转换为音频并播放，之后删除文件

## 实现细节

### TTS 命令
```bash
uv run mlx_audio.tts.generate \
  --model mlx-community/chatterbox-turbo-fp16 \
  --text "Your text here" \
  --play \
  --file_prefix /tmp/audio_reply
```

### 关键参数
- `--model mlx-community/chatterbox-turbo-fp16` - 快速、自然的语音效果
- `--play` - 自动播放生成的语音
- `--file_prefix` - 将文件保存到临时目录以便后续清理
- `--exaggeration 0.3` - 可选参数：调整语音表达的夸张程度（0.0-1.0）
- `--speed 1.0` - 根据需要调整语速

### 文本准备指南

**对于“read it to me”模式：**
1. 使用 WebFetch 工具获取 URL 内容
2. 提取主要内容，去除导航栏、广告和重复内容
3. 如果内容过长（超过 500 字），请总结关键点
4. 使用句号和逗号添加自然的停顿

**对于“talk to me”模式：**
1. 以对话的方式编写回复
2. 使用缩写形式（如 I’m, you’re, it’s）
3. 适量使用填充词（如 [chuckle], um, anyway）以增强自然感
4. 保持回复长度在 200 字以内以获得最佳音质
5. 除非需要解释，否则避免使用专业术语

### 音频生成与清理（非常重要）

播放完成后务必删除音频文件——该文件会保存在聊天记录中。

```bash
# Generate with unique filename and play
OUTPUT_FILE="/tmp/audio_reply_$(date +%s)"
uv run mlx_audio.tts.generate \
  --model mlx-community/chatterbox-turbo-fp16 \
  --text "Your response text" \
  --play \
  --file_prefix "$OUTPUT_FILE"

# ALWAYS clean up after playing
rm -f "${OUTPUT_FILE}"*.wav 2>/dev/null
```

### 错误处理

如果 TTS 生成失败：
1. 检查模型是否已下载（首次运行时可能需要下载约 500MB 的数据）
2. 确保 `uv` 已安装并位于系统路径中
3. 在无法生成音频时，切换为文本回复并给出歉意

## 示例流程

### 示例 1：读取 URL 内容
```
User: read it to me https://blog.example.com/new-feature

Assistant actions:
1. WebFetch the URL
2. Extract article content
3. Generate TTS:
   uv run mlx_audio.tts.generate \
     --model mlx-community/chatterbox-turbo-fp16 \
     --text "Here's what I found... [article summary]" \
     --play --file_prefix /tmp/audio_reply_1706123456
4. Delete: rm -f /tmp/audio_reply_1706123456*.wav
5. Confirm: "Done reading the article to you."
```

### 示例 2：进行对话
```
User: talk to me about what you can help with

Assistant actions:
1. Generate conversational response text
2. Generate TTS:
   uv run mlx_audio.tts.generate \
     --model mlx-community/chatterbox-turbo-fp16 \
     --text "Hey! So I can help you with all kinds of things..." \
     --play --file_prefix /tmp/audio_reply_1706123789
3. Delete: rm -f /tmp/audio_reply_1706123789*.wav
4. (No text output needed - audio IS the response)
```

## 注意事项

- 首次运行可能需要较长时间（因为模型文件较大，约 500MB）
- 英语内容的音质最佳；其他语言的音质可能有所不同
- 对于较长的内容，建议将其分割成多个音频文件
- `--play` 选项会使用系统内置的音频播放器——请确保音量调高