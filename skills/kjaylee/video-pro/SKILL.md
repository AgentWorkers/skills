---
name: video-pro
description: 利用 MiniPC 节点（Emotion + FFmpeg）实现实战型视频编辑技能。支持从编程方式制作视频到剪辑、字幕合成、格式转换等全方位的视频处理功能。
---

# 🎬 Video Pro（Miss Kim 版）

利用 MiniPC 强大的计算资源，实现高性能的视频编辑。结合了基于代码的视频生成工具 Remotion 和视频处理工具 FFmpeg，提供精确的视频处理能力。

## 🏗️ 环境配置（MiniPC）

- **IP:** `<MINIPC_IP>`（Tailscale）
- **Remotion 项目路径:** `$HOME/remotion-videos`
- **FFmpeg:** 已全局安装

---

## 🚀 主要功能

### 1. Remotion 组件渲染
将 React 代码渲染为 MP4 格式的视频，非常适合基于数据的个性化视频制作。

**使用方法:**
```bash
# MiniPC에서 실행
cd $HOME/remotion-videos
npx remotion render <CompositionId> out/video.mp4 --props '{"title": "안녕, 미스 김!"}'
```

### 2. FFmpeg 精确视频处理
以下是常用的一些实用命令：

| 操作 | 命令 |
|------|-------|
| **剪辑** | `ffmpeg -y -i input.mp4 -ss 00:00:10 -to 00:00:20 -c copy output.mp4` |
| **字幕合成（嵌入到视频中）** | `ffmpeg -y -i input.mp4 -vf "subtitles='input.srt'" output.mp4` |
| **格式转换（MOV→MP4）** | `ffmpeg -y -i input.mov -c:v libx264 -c:a aac output.mp4` |
| **提取音频（MP3）** | `ffmpeg -y -i input.mp4 -vn -acodec libmp3lame output.mp3` |
| **静音视频** | `ffmpeg -y -i input.mp4 -an -c:v copy output.mp4` |
| **转换为 GIF** | `ffmpeg -y -i input.mp4 -vf "fps=15,scale=480:-1" -loop 0 output.gif` |
| **调整分辨率（720p）** | `ffmpeg -y -i input.mp4 -vf "scale=1280:720" -c:a copy output.mp4` |

### 3. AI 字幕（Whisper）集成
通过将音频转换为文本，生成字幕文件并嵌入到视频中：

1. **提取音频:** 使用 FFmpeg 提取视频中的音频。
2. **转录:** 使用 Whisper 模型（Mac Studio 或 MiniPC）生成 `.srt` 字幕文件。
3. **合成字幕:** 使用 FFmpeg 的 `subtitles` 过滤器将字幕永久嵌入到视频中。

---

## 🛠️ 实际使用模式（nodes.run）

子代理在向 MiniPC 发送命令时，请使用以下模式：

```javascript
// MiniPC에서 렌더링 후 결과물 확인
await nodes.run({
  node: "MiniPC",
  command: "cd $HOME/remotion-videos && npx remotion render MyComp out/result.mp4"
});
```

## ⚠️ 注意事项

1. **MiniPC 路径:** 确保路径始终以 `$HOME/` 为基准的绝对路径。
2. **性能:** Remotion 的渲染过程对 CPU 资源要求较高，建议通过子代理在后台运行。
3. **字幕路径:** 如果 FFmpeg 的 `subtitles` 参数中的路径包含特殊字符，可能需要对其进行转义处理。
4. **大文件处理:** 尽量避免在节点间传输大文件，建议在 MiniPC 内完成所有处理后再传输最终结果。

---
*Miss Kim 的视频制作技巧注重实际操作中的效率和输出质量。* 💋