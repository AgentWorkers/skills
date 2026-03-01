---
name: showcase-video-builder
description: Build polished showcase and demo videos from screenshots, avatars, and text overlays using ffmpeg. Use when creating demo reels, hackathon presentations, product walkthroughs, or social media video content from static assets. Requires ffmpeg.
version: 1.0.0
metadata:
  {
      "openclaw": {
            "emoji": "\ud83c\udfac",
            "requires": {
                  "bins": [
                        "ffmpeg"
                  ],
                  "env": []
            },
            "primaryEnv": null,
            "network": {
                  "outbound": false,
                  "reason": "Local ffmpeg operations only. No external network calls."
            }
      }
}
---

# Showcase Video Builder

这款工具可以将截图和图片转换成精美的演示视频，支持Ken Burns风格的平移/缩放效果、淡入淡出过渡效果以及文字叠加功能。它专为需要制作展示内容但缺乏视频编辑软件的团队和开源项目（OSS项目）设计。

## 核心功能模式

### 带有淡入淡出效果的图片幻灯片展示  
```bash
ffmpeg -loop 1 -t 4 -i slide1.png \
       -loop 1 -t 4 -i slide2.png \
       -loop 1 -t 4 -i slide3.png \
       -filter_complex \
       "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=out:st=3:d=1[v0]; \
        [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=in:st=0:d=1,fade=t=out:st=3:d=1[v1]; \
        [2:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=in:st=0:d=1[v2]; \
        [v0][v1][v2]concat=n=3:v=1:a=0[out]" \
       -map "[out]" -c:v libx264 -pix_fmt yuv420p output.mp4
```

### Ken Burns风格的慢速缩放效果  
```bash
# Slow zoom in over 5 seconds
ffmpeg -loop 1 -t 5 -i image.png -filter_complex \
  "scale=8000:-1,zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1920x1080:fps=30" \
  -c:v libx264 -pix_fmt yuv420p -t 5 zoomed.mp4
```

### 文字叠加功能  
```bash
# macOS: use /System/Library/Fonts/Helvetica.ttc
ffmpeg -i input.mp4 -vf \
  "drawtext=text='Built in 48 Hours':fontfile=/System/Library/Fonts/Helvetica.ttc:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-80:enable='between(t,2,5)'" \
  -c:v libx264 -c:a copy output.mp4
```

### 标题卡（纯色背景+文字）  
```bash
ffmpeg -f lavfi -i "color=c=0x6366F1:s=1920x1080:d=3" -vf \
  "drawtext=text='Your Project Name':fontfile=/System/Library/Fonts/Helvetica.ttc:fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
  -c:v libx264 -pix_fmt yuv420p title.mp4
```

### 视频片段拼接功能  
```bash
# Create concat list
echo "file 'title.mp4'" > concat.txt
echo "file 'slides.mp4'" >> concat.txt
echo "file 'closing.mp4'" >> concat.txt

ffmpeg -f concat -safe 0 -i concat.txt -c copy final.mp4
```

## 平台使用建议

- **LinkedIn:** 视频会自动静音播放——请依赖文字信息来传达关键内容。
- **Twitter/X:** 视频时长最多为2分20秒（免费账户限制）。标题字幕长度不得超过280个字符。上传媒体文件需要使用OAuth 1.0a认证。
- **嵌入视频时的尺寸要求:** 头像尺寸为150像素，截图为600像素，合成视频为700像素。确保文件大小不超过5MB。

## 使用技巧

- **macOS字体路径:** `/System/Library/Fonts/Helvetica.ttc` — 如果`drawtext`命令执行失败，请先检查该字体是否可用。
- **务必使用`-pix_fmt yuv420p`格式** — 不使用该格式时，某些播放器可能会显示绿色背景。
- **在大尺寸图片上使用Ken Burns效果会降低播放速度** — 请将图片缩放到目标分辨率的2倍，而非8倍。

## 相关文件

- `scripts/build_showcase.sh` — 完整的展示视频制作脚本，支持自定义各功能模块。