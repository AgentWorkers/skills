---
name: skillboss
description: "多AI网关：支持50多种模型，涵盖聊天、图像识别、视频处理、文本转语音（TTS）、音乐播放以及搜索功能。"
allowed-tools: Bash, Read
metadata: {"clawdbot":{"requires":{"bins":["node"],"env":["SKILLBOSS_API_KEY"]},"primaryEnv":"SKILLBOSS_API_KEY"}}
---
# SkillBoss

一个API密钥，可访问50多种来自不同提供商的模型服务：聊天、图像处理、视频处理、文本转语音（TTS）、语音转文本（STT）、音乐播放以及网络搜索功能。

## 模型列表

```bash
node {baseDir}/scripts/run.mjs models
node {baseDir}/scripts/run.mjs models image
node {baseDir}/scripts/run.mjs models chat
```

## 运行模型

```bash
node {baseDir}/scripts/run.mjs run bedrock/claude-4-5-sonnet "Explain quantum computing"
node {baseDir}/scripts/run.mjs run mm/img "A sunset over mountains"
node {baseDir}/scripts/run.mjs run minimax/speech-01-turbo "Hello world"
```

## 智能模式

```bash
node {baseDir}/scripts/run.mjs tasks
node {baseDir}/scripts/run.mjs task image "A sunset"
node {baseDir}/scripts/run.mjs task chat "Hello"
node {baseDir}/scripts/run.mjs task tts "Hello world"
```

## 保存媒体文件

图像/视频/音频处理后的结果会生成一个URL。可以使用`curl`命令进行保存：

```bash
URL=$(node {baseDir}/scripts/run.mjs run mm/img "A sunset")
curl -sL "$URL" -o sunset.png
```

注意事项：
- 请在 [https://www.skillboss.co](https://www.skillboss.co) 获取SKILLBOSS_API_KEY。
- 使用`models`命令来查看可用的模型列表。