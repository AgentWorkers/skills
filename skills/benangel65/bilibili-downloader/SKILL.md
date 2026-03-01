---
name: bilibili-downloader
description: 使用 `bilibili-api` 从哔哩哔哩（Bilibili）下载视频、音频、字幕以及封面图片。适用于需要处理哔哩哔哩内容的场景，包括下载不同质量的视频、提取音频和字幕、下载封面图片以及管理下载偏好设置等操作。
---
# Bilibili 下载器

## 快速入门

通过 URL 下载视频：
```bash
pip install bilibili-api-python
python -c "
from bilibili_api import video, sync
v = video.Video(bvid='BV1xx411c7m2')
sync(v.download(output='./video.mp4'))
"
```

## 下载选项

### 视频质量
- 使用 `qn` 参数指定视频质量（127=8K, 126=杜比音效, 125=1080P+ 等）
- 默认情况下会选择最佳可用质量

### 音频下载
- 下载原声带：`v.download_audious(output='./audio.mp3')`
- 支持多种音频格式

### 字幕
- 获取可用的字幕：`v.get_subtitle()`
- 下载字幕文件：`sync(v.download_subtitle(output='./'))`

### 封面和缩略图
- 获取封面 URL：`v.get_cover()`
- 下载封面图片：`sync(v.download_cover(output='./cover.jpg'))`

## 常用任务

### 下载单个视频
```python
from bilibili_api import video, sync
v = video.Video(bvid='BV1xx411c7m2')
sync(v.download(output='./video.mp4'))
```

### 下载指定质量的视频
```python
from bilibili_api import video, sync
v = video.Video(bvid='BV1xx411c7m2')
info = v.get_download_url(qn=127)  # 8K quality
```

### 下载整个播放列表
```python
from bilibili_api import video, sync
from bilibili_api import playlist

pl = playlist.Playlist(playlist_id='123456')
for v in sync(pl.get_videos()):
    sync(v.download(output=f'./playlist/{v["title"]}.mp4'))
```

### 仅下载音频
```python
from bilibili_api import video, sync
v = video.Video(bvid='BV1xx411c7m2')
sync(v.download_audio(output='./audio.mp3'))
```

## 认证

对于高级内容，需要使用浏览器 cookie：
1. 在浏览器中登录 Bilibili
2. 导出 SESSDATA cookie 的值
3. 设置环境变量：`export BILIBILI_SESSDATA='your_cookie_value'`

## 所需软件
- `bilibili-api-python`：`pip install bilibili-api-python`
- `ffmpeg`：用于视频/音频处理
- Python 3.8 或更高版本

## 资源

### scripts/
- 用于常见下载操作的实用脚本

### references/
- Bilibili API 文档
- 视频质量代码参考（qn 值）
- Cookie 设置指南

### assets/
- 下载模板和配置示例