---
name: voice-transcribe
description: 使用 OpenAI 的 gpt-4o-mini-transcribe 模型转录音频文件，该模型提供词汇提示和文本替换功能。需要使用 UV 工具（https://docs.astral.sh/uv/）。
---

# 语音转录

使用 OpenAI 的 gpt-4o-mini-transcribe 模型来转录音频文件。

## 使用场景

当收到语音备忘录（尤其是通过 WhatsApp 传输的）时，只需运行以下命令：
```bash
uv run /Users/darin/clawd/skills/voice-transcribe/transcribe <audio-file>
```
然后根据转录的内容进行回复。

## 修正转录错误

如果 Darin 指出某个单词的转录有误，可以将其添加到 `vocab.txt`（用于提供提示）或 `replacements.txt`（用于确保修正错误）中。具体操作方法请参见下方说明。

## 支持的音频格式

- mp3、mp4、mpeg、mpga、m4a、wav、webm、ogg、opus

## 示例

```bash
# transcribe a voice memo
transcribe /tmp/voice-memo.ogg

# pipe to other tools
transcribe /tmp/memo.ogg | pbcopy
```

## 设置

1. 将你的 OpenAI API 密钥添加到 `/Users/darin/clawd/skills/voice-transcribe/.env` 文件中：
   ```
   OPENAI_API_KEY=sk-...
   ```

## 自定义词汇表

将需要识别的单词（每个单词占一行）添加到 `vocab.txt` 文件中，以帮助模型识别专有名词或行业术语：
```
Clawdis
Clawdbot
```

## 文本替换规则

如果模型仍然转录错误，可以在 `replacements.txt` 文件中添加相应的替换内容：
```
wrong spelling -> correct spelling
```

## 注意事项

- 该工具仅支持英语音频的转录（不支持语言检测）。
- 特定使用 gpt-4o-mini-transcribe 模型进行转录。
- 该工具会通过音频文件的 SHA256 哈希值来缓存转录结果。