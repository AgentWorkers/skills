# Deepgram CLI 使用指南

## 工具
**@deepgram/cli** — Deepgram 的命令行接口，用于将语音转换为文本。

---

## 安装
```bash
npm install -g @deepgram/cli
```

---

## 认证
```bash
deepgram login
```

使用您的 Deepgram API 密钥（存储在本地）。

---

## 核心功能：语音转文本

### 转录本地音频文件
```bash
deepgram listen prerecorded audio.wav
```

### 带参数转录
```bash
deepgram listen prerecorded audio.wav \
  --model nova-2 \
  --language en \
  --punctuate \
  --diarize
```

---

## 核心功能：读取/获取内容

### 从 URL（远程音频）获取
```bash
deepgram listen prerecorded https://example.com/audio.mp3
```

### 从标准输入（管道）获取
```bash
cat audio.wav | deepgram listen prerecorded -
```

### 从麦克风（实时）获取
```bash
deepgram listen microphone
```

按 `Ctrl+C` 停止操作。恭喜，您刚刚“口述”完成了内容的生成！

---

## 输出处理

### 保存转录结果
```bash
deepgram listen prerecorded audio.wav > transcript.json
```

### 输出纯文本
```bash
deepgram listen prerecorded audio.wav --format text
```

---

## 有用的参数（请记住这些参数）

* `--model` – `nova-2`, `general` 等
* `--language` – `en`, `tr`, `de` 等
* `--punctuate` – 添加标点符号
* `--diarize` – 区分说话者
* `--format` – `json`, `text`, `srt`, `vtt`

---

## 典型工作流程

1. 获取所需内容（文件、URL 或麦克风输入）
2. 运行 `deepgram listen`
3. 捕获输出结果（JSON 或文本格式）
4. 后处理（搜索、总结、添加字幕）

---

## 功能总结

* 基于命令行的语音转文本工具
* 支持本地、远程和实时音频输入
* 支持脚本编程和管道传输
* 转换速度快、准确率高，无需复杂的用户界面

Deepgram CLI：因为键盘其实被高估了……