---
name: songsee
description: 使用 songsee CLI 从音频文件中生成频谱图和特征面板可视化图像。
homepage: https://github.com/steipete/songsee
metadata: {"clawdbot":{"emoji":"🌊","requires":{"bins":["songsee"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/songsee","bins":["songsee"],"label":"Install songsee (brew)"}]}}
---

# songsee

该工具可以从音频文件生成频谱图以及各种特征分析面板。

**快速使用示例：**
- 生成单频谱图：`songsee track.mp3`
- 生成多面板分析图：`songsee track.mp3 --viz spectrogram,mel,chroma,hpss,selfsim,loudness,tempogram,mfcc,flux`
- 截取特定时间段的频谱图：`songsee track.mp3 --start 12.5 --duration 8 -o slice.jpg`
- 将音频文件转换为图片格式：`cat track.mp3 | songsee - --format png -o out.png`

**常用参数：**
- `--viz`：可选参数，用于指定要显示的分析面板（多个参数用逗号分隔）
- `--style`：可选参数，用于设置频谱图的显示风格（经典、熔岩、地狱、绿叶、灰色）
- `--width`/`--height`：输出图像的宽度/高度
- `--window`/`--hop`：用于设置FFT分析的窗口大小和步长
- `--min-freq`/`--max-freq`：指定频率范围
- `--start`/`--duration`：指定时间切片范围
- `--format`：输出图像的格式（jpg或png）

**注意事项：**
- 该工具支持直接解码WAV/MP3格式的音频文件；其他格式需要借助ffmpeg进行转换。
- 如果同时使用多个`--viz`参数，系统会生成多个并排显示的分析图。

（注：部分参数名称为英文缩写，保留原样。）