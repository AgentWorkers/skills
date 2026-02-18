# 音频转录技能

使用 faster-whisper 自动转录语音消息（支持本地转录，无需 API 密钥）。

## 要求

```bash
pip install faster-whisper
```

模型会在首次使用时自动下载。

## 使用方法

### 转录文件

```bash
python3 /root/clawd/skills/audio-transcribe/scripts/transcribe.py /path/to/audio.ogg
```

### 更改模型（编辑脚本）

请编辑 `transcribe.py` 文件，并修改相关配置：

```python
model = WhisperModel('small', device='cpu', compute_type='int8')  # Options: tiny, base, small, medium, large-v3
```

## 模型

| 模型 | 大小 | 显存/内存 | 转录速度 | 适用场景 |
|-------|------|----------|-------|----------|
| tiny | 39 MB | 约 1 GB | 转录速度较快 | 适用于快速草稿 |
| base | 74 MB | 约 1 GB | 转录准确率一般 |
| small | 244 MB | 约 2 GB | 推荐使用的模型 |
| medium | 769 MB | 约 5 GB | 转录准确率较高 |
| large-v3 | 1.5 GB | 约 10 GB | 转录准确率最高 |

## 集成

启用此技能后，Clawdbot 会自动转录接收到的语音消息。

## 相关文件

- `scripts/transcribe.py` — 主要转录脚本
- `SKILL.md` — 本说明文件