---
name: announcer
description: "通过 Airfoil 和 ElevenLabs 的 TTS（文本到语音）功能，利用 AirPlay 扬声器在整个房屋内播放公告文本。"
summary: "House-wide TTS announcements via AirPlay speakers, Airfoil, and ElevenLabs."
version: 1.2.1
homepage: https://github.com/odrobnik/announcer-skill
metadata:
  {
    "openclaw":
      {
        "emoji": "📢",
        "requires": { "bins": ["python3", "ffmpeg"], "apps": ["Airfoil"], "env": ["ELEVENLABS_API_KEY"], "skills": ["elevenlabs"], "platform": "macos" },
      },
  }
---

# 宣告系统（Announcer）

通过 Airfoil 和 ElevenLabs，利用 AirPlay 扬声器播放文本转语音（TTS）公告。

## 工作原理

1. 使用 ElevenLabs 生成语音文件（高质量音频格式 → 立体声 MP3 格式）
2. 通过 Airfoil 将音频文件传输到 AirPlay 扬声器
3. 可选择播放一段提示音（如铃声），随后播放公告内容
4. 播放完成后断开与扬声器的连接

## 设置

有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。

## 使用方法

```bash
# Announce to all configured speakers
python3 skills/announcer/scripts/announce.py "Dinner is ready!"

# Announce to specific speakers only
python3 skills/announcer/scripts/announce.py "Wake up!" --speakers "Kids Room"

# Skip the chime
python3 skills/announcer/scripts/announce.py "Quick note" --no-gong
```

## 文件结构

```
announcer/
├── SKILL.md
├── assets/
│   └── gong_stereo.mp3      # Announcement chime
└── scripts/
    └── announce.py           # Main announcement script
```

用户配置文件（不属于该功能的组成部分）：
```
~/clawd/announcer/
└── config.json               # Speaker list, voice, audio settings
```