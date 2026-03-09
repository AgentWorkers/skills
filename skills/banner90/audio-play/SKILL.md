---
 name: audio-play
 description: Play audio files using Windows media player. Non-blocking execution.
 tools:
   - play_audio
---
# 音频播放

## 使用方法

```bash
python scripts/audio_play.py <audio_path> [--config player_config.json]
```

## 参数

- `audio_path`（必填）：音频文件的绝对路径
- `config`（可选）：播放器配置文件

## 播放器配置（player_config.json）

```json
{
  "player": "vlc",
  "player_path": "C:/Program Files/VideoLAN/VLC/vlc.exe"
}
```

## 返回值

```json
{
  "success": true,
  "audio_path": "H:/works/audio/xxx.mp3",
  "player_used": "vlc",
  "duration": 1200
}
```

## 工具

## play_audio

使用媒体播放器播放音频文件


## 工作流程集成

此技能是 YouTube 翻译工作流程的一部分：
1. **youtube-audio-download**：从 YouTube 下载音频文件
2. **doubao-launch**：启动 Doubao 翻译窗口
3. **audio-play**：播放下载的音频文件
4. **doubao-capture**：捕获翻译后的字幕

## 执行方式

所有技能均在 Windows 上通过 WSL（Windows Subsystem for Linux）跨平台调用 Python 来执行：
```
wsl -> python.exe scripts/audio_play.py ...
```

## 错误处理

所有技能都会返回一个包含 `success` 字段的 JSON 对象：
- `success: true`：操作完成
- `success: false`：请查看 `error_code` 和 `error_message` 以获取错误信息

## 注意事项

- Windows GUI 自动化需要可见的桌面（禁止使用 RDP 断开连接）
- 输出文件存储在 Windows 的 `works/` 目录中
- WSL 通过 `/mnt/h/...` 访问 Windows 文件系统中的文件