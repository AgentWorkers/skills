# 语音转录技能

使用 Faster Whisper（本地服务，注重用户隐私）来转录语音消息。

## 需求

```bash
pip3 install --break-system-packages faster-whisper
```

## 使用方法

```bash
# Transcribe a voice file
voice-transcribe /path/to/audio.ogg

# Or use with media path
voice-transcribe ~/.openclaw/media/inbound/file_xxx.ogg
```

## 模型

- `tiny`：速度最快，但准确率最低（默认设置）
- `base`：准确率与性能平衡
- `small`：准确率较高
- `medium`：准确率很高（但需要更多内存）

## 输出结果

将语音消息转录为文本形式并返回。