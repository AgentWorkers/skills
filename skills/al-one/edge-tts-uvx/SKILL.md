---
name: edge-tts-uvx
description: |
  Text-to-speech conversion using `uvx edge-tts` for generating audio from text.
  Use when:
    (1) User requests audio/voice output with the "tts" trigger or keyword.
    (2) Content needs to be spoken rather than read (multitasking, accessibility, driving, cooking).
    (3) User wants a specific voice, speed, pitch, or format for TTS output.
metadata:
  {
    "openclaw":
      {
        "emoji": "🗣️",
        "requires": {"bins": ["uvx"]}
      }
  }
---

# Edge-TTS 技能

通过 `node-edge-tts` npm 包，利用 Microsoft Edge 的神经 TTS 服务生成高质量的文本转语音（Text-to-Speech）音频。支持多种语言、多种语音效果，以及可调节的语速/音调，并支持字幕生成功能。

## 使用方法
```shell
uvx edge-tts --text "{msg}" --write-media {tempdir}/{filename}.mp3

# With subtitles
uvx edge-tts --text "{msg}" --write-media {tempdir}/{filename}.mp3 --write-subtitles -
```

## 调节语速/音量/音调
```shell
uvx edge-tts --text "{msg}" --write-media {tempdir}/{filename}.mp3 --rate=+50%
uvx edge-tts --text "{msg}" --write-media {tempdir}/{filename}.mp3 --volume=+50% --pitch=-50Hz
```

## 更换语音
```shell
uvx edge-tts --text "{msg}" --write-media {tempdir}/{filename}.mp3 --voice=zh-CN-XiaoxiaoNeural
```

## 可用的语音选项
```
Name                               Gender    ContentCategories      VoicePersonalities
en-GB-LibbyNeural                  Female    General                Friendly, Positive
en-GB-RyanNeural                   Male      General                Friendly, Positive
en-GB-SoniaNeural                  Female    General                Friendly, Positive
en-GB-ThomasNeural                 Male      General                Friendly, Positive
en-HK-SamNeural                    Male      General                Friendly, Positive
en-HK-YanNeural                    Female    General                Friendly, Positive
en-US-AnaNeural                    Female    Cartoon, Conversation  Cute
en-US-AndrewMultilingualNeural     Male      Conversation, Copilot  Warm, Confident, Authentic, Honest
en-US-AndrewNeural                 Male      Conversation, Copilot  Warm, Confident, Authentic, Honest
en-US-AriaNeural                   Female    News, Novel            Positive, Confident
en-US-AvaMultilingualNeural        Female    Conversation, Copilot  Expressive, Caring, Pleasant, Friendly
en-US-AvaNeural                    Female    Conversation, Copilot  Expressive, Caring, Pleasant, Friendly
en-US-BrianMultilingualNeural      Male      Conversation, Copilot  Approachable, Casual, Sincere
en-US-BrianNeural                  Male      Conversation, Copilot  Approachable, Casual, Sincere
en-US-ChristopherNeural            Male      News, Novel            Reliable, Authority
en-US-EmmaMultilingualNeural       Female    Conversation, Copilot  Cheerful, Clear, Conversational
en-US-EmmaNeural                   Female    Conversation, Copilot  Cheerful, Clear, Conversational
en-US-EricNeural                   Male      News, Novel            Rational
en-US-GuyNeural                    Male      News, Novel            Passion
en-US-JennyNeural                  Female    General                Friendly, Considerate, Comfort
en-US-MichelleNeural               Female    News, Novel            Friendly, Pleasant
en-US-RogerNeural                  Male      News, Novel            Lively
en-US-SteffanNeural                Male      News, Novel            Rational
fr-FR-DeniseNeural                 Female    General                Friendly, Positive
fr-FR-HenriNeural                  Male      General                Friendly, Positive
zh-CN-XiaoxiaoNeural               Female    News, Novel            Warm
zh-CN-YunjianNeural                Male      Sports,  Novel         Passion
zh-CN-liaoning-XiaobeiNeural       Female    Dialect                Humorous
zh-CN-shaanxi-XiaoniNeural         Female    Dialect                Bright
zh-HK-HiuGaaiNeural                Female    General                Friendly, Positive
zh-HK-WanLungNeural                Male      General                Friendly, Positive
zh-TW-HsiaoChenNeural              Female    General                Friendly, Positive
zh-TW-YunJheNeural                 Male      General                Friendly, Positive\
```

使用 shell 命令查询所有可用的语音：
```shell
uvx edge-tts --list-voices
```