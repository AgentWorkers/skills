---
 name: youtube-audio-download
 description: Download YouTube video audio and convert to MP3. Supports age-restricted videos with cookies.
 tools:
   - download_audio
---
# YouTube音频下载

## 使用方法

```bash
python scripts/download_audio.py <URL> [--cookies cookies.txt] [--output-dir dir]
```

## 参数

- `url`（必填）：YouTube视频的URL
- `cookies_path`（可选）：用于访问年龄限制视频的cookies.txt文件的路径
- `output_dir`（可选）：输出目录，默认为“works/audio”

## 返回值

```json
{
  "success": true,
  "audio_path": "H:/works/audio/video_title-xxxxx.mp3",
  "title": "Video Title",
  "duration": 1200,
  "file_size_mb": 15.5
}
```

## 工具

## download_audio

将YouTube音频下载为MP3格式

## 工作流程集成

此功能是YouTube翻译工作流程的一部分：
1. **youtube-audio-download**：从YouTube下载音频
2. **doubao-launch**：启动Doubao翻译窗口
3. **audio-play**：播放下载的音频
4. **doubao-capture**：捕获翻译后的字幕

## 执行方式

所有功能均通过WSL（Windows Subsystem for Linux）在Windows环境下使用Python执行：

```
wsl -> python.exe scripts/download_audio.py ...
```

## 错误处理

所有功能返回包含`success`字段的JSON对象：
- `success: true`：操作完成
- `success: false`：请查看`error_code`和`error_message`以获取错误信息

## 注意事项

- Windows图形界面自动化需要桌面可见（不允许通过RDP断开连接）
- 输出文件存储在Windows的`works/`目录下
- WSL通过`/mnt/h/...`路径访问Windows文件系统