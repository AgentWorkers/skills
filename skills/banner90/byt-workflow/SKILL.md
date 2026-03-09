---
 name: byt-workflow
 description: YouTube video translation workflow, download audio, launch Doubao, play audio, capture translation
 tools:
   - youtube_translate
---
# Byt Workflow

## 使用方法

```bash
python workflow.py <youtube_url> [mode]
```

## 参数

- `url`（必填）：YouTube视频的URL
- `mode`（可选）：翻译模式（双语、单语、中文、双语混合），默认值为“dual”

## 工作流程步骤

1. **下载YouTube音频**：使用 `youtube-audio-download` 技能
2. **启动Doubao**：使用 `doubao-launch` 技能
3. **播放音频**：使用 `audio-play` 技能
4. **捕获翻译结果**：使用 `doubao-capture` 技能

## 返回值

```json
{
  "success": true,
  "audio_path": "H:/works/audio/video_title-xxxxx.mp3",
  "translation_path": "H:/works/translations/doubao_20240307_143022.txt",
  "duration": 1200
}
```

## 工具

## youtube_translate

完整的YouTube视频翻译工作流程


## 工作流程集成

此技能是YouTube翻译工作流程的一部分：
1. **youtube-audio-download**：从YouTube下载音频文件
2. **doubao-launch**：启动Doubao翻译软件
3. **audio-play**：播放下载的音频文件
4. **doubao-capture**：捕获翻译后的字幕内容

## 执行方式

所有技能均在Windows系统上通过WSL（Windows Subsystem for Linux）跨平台调用Python脚本执行：
```
wsl -> python.exe scripts/workflow.py ...
```

## 错误处理

所有技能都会返回一个包含 `success` 字段的JSON对象：
- `success: true`：操作成功
- `success: false`：请查看 `error_code` 和 `error_message` 以获取错误信息

## 注意事项

- Windows图形界面自动化需要桌面显示（禁止使用RDP远程连接）
- 输出文件存储在Windows系统的 `works/` 目录中
- WSL通过 `/mnt/h/...` 路径访问Windows文件系统中的文件