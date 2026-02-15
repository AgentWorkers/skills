---
name: tube-summary
description: 在 YouTube 上搜索任何主题的视频，并从视频字幕中获取智能摘要。这些功能适用于以下场景：  
(1) 查找并预览关于某个主题的 YouTube 视频；  
(2) 根据视频的实际内容获取其详细描述；  
(3) 在不观看视频的情况下快速了解视频的主题。  
工作流程如下：  
1. 在 YouTube 上进行搜索；  
2. 选择所需的视频；  
3. 提取并总结视频的字幕内容。
---

# tube-summary

在 YouTube 上搜索任何主题的视频，然后使用字幕提取并总结这些视频的内容。

## 快速入门

### 第一步：搜索视频

当被问及某个主题时，在 YouTube 上进行搜索，并列出前 10 个搜索结果：

```bash
python3 scripts/youtube-search.py "your search query"
```

这将返回一个包含视频标题、频道和观看次数的编号列表。

### 第二步：用户选择视频

用户通过编号选择其中一个视频（例如，选择“3”表示第三个视频）。

### 第三步：下载字幕

使用 `yt-dlp` 命令从选定的视频中提取英文字幕：

```bash
yt-dlp --write-subs --sub-langs en --skip-download "VIDEO_URL"
```

这会生成一个 `.en.vtt` 格式的字幕文件，而不会下载视频本身。

### 第四步：处理并总结

使用字幕处理工具对字幕进行分析和总结：

```bash
python3 scripts/process-subtitles.py "path/to/subtitle-file.vtt"
```

该工具会生成以下内容：
- **关键主题**：视频中涵盖的主要内容
- **总结**：对视频内容的简短描述（2-3 段）
- **时间戳**：带有上下文的重要时刻
- **关键引语**：演讲者说出的重要语句

## 工作流程

1. **搜索** → `youtube-search.py "<主题>"` → 显示前 10 个视频
2. **用户选择** → 例如，选择“视频 5”
3. **提取视频链接** → 从搜索结果中获取链接
4. **下载字幕** → `yt-dlp --write-subs --sub-langs en --skip-download "视频链接"`
5. **处理字幕** → `process-subtitles.py "subtitle.vtt"`
6. **展示结果** → 以格式化的方式呈现总结内容

## 先决条件

- `yt-dlp`（安装方法：`pip install yt-dlp`）
- `requests`（用于 YouTube 搜索的备用方案）
- Python 3.7 或更高版本

## 注意事项

- 如果 YouTube 搜索 API 不可用，系统会使用 `requests` 进行网页抓取
- 字幕可能是自动生成的（而非手动添加的）
- 有些视频可能没有英文字幕
- 字幕文件会保存在运行 `yt-dlp` 的同一目录中

## 示例用法

```
User: "Tell me about Rust programming language"

→ Search returns 10 videos about Rust

User: "Summarize video 3"

→ Downloads subtitles from video 3
→ Processes and returns detailed summary
```