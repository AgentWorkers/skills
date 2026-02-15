# 语音技能（Voice Skill）

该语音技能利用 edge-tts 提供了增强的文本转语音（text-to-speech）功能，支持多种播放选项，可将文本转换为语音形式。

## 主要特性

- 使用 Microsoft Edge 的 TTS 引擎进行文本转语音转换
- 支持多种语音选项和音频设置
- 可直接播放生成的语音文件
- 自动清理临时音频文件
- 与 MEDIA 系统集成以实现音频播放

## 安装

在使用此技能之前，您需要安装以下依赖项：

```bash
pip3 install edge-tts
```

或者通过以下命令安装该技能：

```javascript
await skill.execute({ action: 'install' });
```

## 使用方法

### 直接语音输入（推荐）

无需将文本保存到文件中，即可直接进行语音转换：

```javascript
const result = await skill.execute({
  action: 'speak',  // New improved action
  text: 'Hello, how are you today?'
});
// Audio is played directly and temporary file is cleaned up automatically
```

### 使用默认设置将文本转换为语音

使用默认设置将文本转换为语音：

```javascript
const result = await skill.execute({
  action: 'tts',
  text: 'Hello, how are you today?'
});
// Returns a MEDIA link to the audio file
```

### 直接播放转换后的语音

转换完成后即可立即播放语音：

```javascript
const result = await skill.execute({
  action: 'tts',
  text: 'Hello, how are you today?',
  playImmediately: true  // Plays the audio immediately after generation
});
```

### 使用自定义设置

您还可以根据需要自定义语音转换的参数：

```javascript
const result = await skill.execute({
  action: 'tts',
  text: 'This is a sample of voice customization.',
  options: {
    voice: 'zh-CN-XiaoxiaoNeural',
    rate: '+10%',
    volume: '-5%',
    pitch: '+10Hz'
  }
});
```

### 播放现有的音频文件

您可以播放已存在的音频文件：

```javascript
const result = await skill.execute({
  action: 'play',
  filePath: '/path/to/audio/file.mp3'
});
```

### 查看可用的语音选项

您可以查看系统中支持的语音列表：

```javascript
const result = await skill.execute({
  action: 'voices'
});
```

### 清理临时文件

系统会自动清理保存时间超过 1 小时的临时音频文件（默认设置）：

```javascript
const result = await skill.execute({
  action: 'cleanup'
});
```

您也可以指定自定义的文件删除时间阈值：

```javascript
const result = await skill.execute({
  action: 'cleanup',
  options: {
    hoursOld: 2  // Clean files older than 2 hours
  }
});
```

## 可用的文本转语音选项

- `voice`：选择使用的语音（默认值：`zh-CN-XiaoxiaoNeural`）
- `rate`：调整语音语速（默认值：`+0%`）
- `volume`：调整音量（默认值：`+0%`
- `pitch`：调整音高（默认值：`+0Hz`）

## 支持的语音

Edge-TTS 支持多种语言的语音：
- 中文：`zh-CN-XiaoxiaoNeural`, `zh-CN-YunxiNeural`, `zh-CN-YunyangNeural`
- 英文（美式）：`en-US-Standard-C`, `en-US-Standard-D`, `en-US-Wavenet-F`
- 英文（英式）：`en-GB-Standard-A`, `en-GB-Wavenet-A`
- 日文：`ja-JP-NanamiNeural`
- 韩文：`ko-KR-SunHiNeural`
- 以及更多其他语言的语音...

## 文件管理

- 音频文件会临时保存在 `temp` 目录中
- 文件会在 1 小时后自动被删除（默认设置）
- 如果选择“直接语音输入”功能，文件会在 5 秒后自动被删除

## 系统要求

- Python 3.x
- `pip` 包管理器
- `edge-tts` 库（通过 `pip3 install edge-tts` 安装）