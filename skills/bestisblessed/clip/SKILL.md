---
name: clip
description: 从 YouTube 下载指定的视频；根据指定的开始和结束时间提取视频片段，并将它们保存到您桌面上的文件夹中。
metadata: {"openclaw": {"emoji": "✂️", "requires": {"bins": ["yt-dlp", "ffmpeg"]}, "install": [{"id": "brew-ffmpeg", "kind": "brew", "formula": "ffmpeg", "bins": ["ffmpeg"], "label": "Install ffmpeg (brew)"}, {"id": "brew-ytdlp", "kind": "brew", "formula": "yt-dlp", "bins": ["yt-dlp"], "label": "Install yt-dlp (brew)"}, {"id": "apt-ffmpeg", "kind": "apt", "package": "ffmpeg", "bins": ["ffmpeg"], "label": "Install ffmpeg (apt)"}, {"id": "apt-ytdlp", "kind": "apt", "package": "yt-dlp", "bins": ["yt-dlp"], "label": "Install yt-dlp (apt)"}], "user-invocable": true}}
---
# clip

该工具会从 YouTube 下载指定的视频 URL，并根据用户指定的开始和结束时间范围来剪辑视频片段，将其保存到桌面上的 `~/Desktop/Clips` 文件夹中。下载完成后，会自动删除原始视频文件以清理磁盘空间。

## 示例

```
/clip https://www.youtube.com/watch?v=Tyej_V2ilZA 0:00 3:17 holloway-bmf-walkout
```

## 使用方法

**提供所需的时间戳信息：**  
URL + 开始时间 + 结束时间 + 可选的视频名称。  
例如：  
`Clip https://youtu.be/VIDEO_ID from 0:00 to 1:12, name it myclip`  

## 运行命令

```bash
{baseDir}/clip.sh --url "https://youtu.be/VIDEO_ID" --start 0 --end 72 [--name "myclip"]
```

时间格式：秒（例如 `72`）或 `HH:MM:SS`。  
输出文件路径：`~/Desktop/Clips/<名称>.mp4`