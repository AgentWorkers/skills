---
name: youtube-transcript
description: **功能说明：**  
用于获取并汇总YouTube视频的字幕内容。当需要从YouTube视频中提取内容（如进行总结、转录或提取关键信息时）时，可使用该工具。该工具通过使用本地IP代理来绕过YouTube对云IP的访问限制，从而顺利获取视频字幕。  

**技术细节：**  
- **字幕获取方式：**  
  该工具利用本地IP代理来访问YouTube，从而规避YouTube对特定IP地址的访问限制（尤其是云IP地址）。  

**适用场景：**  
- **内容提取与总结：**  
  适用于需要从YouTube视频中提取文本信息（如视频标题、描述、评论等）的场景。  

**注意事项：**  
- **代理配置：**  
  确保已正确配置本地IP代理，以便工具能够正常使用。  

**示例用法：**  
- **命令行示例：**  
  ```
  python fetch_and_summary_video.py youtube_url
  ```  
  （将 `youtube_url` 替换为需要获取字幕的YouTube视频链接。）  

**技术支持：**  
如需更多关于该工具的使用说明或技术支持，请联系我们的技术支持团队。
---

# YouTube 字幕提取

从 YouTube 视频中提取字幕，并可选择对其进行总结。

## 快速入门

```bash
python3 scripts/fetch_transcript.py <video_id_or_url> [languages]
```

**示例：**
```bash
python3 scripts/fetch_transcript.py dQw4w9WgXcQ
python3 scripts/fetch_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
python3 scripts/fetch_transcript.py dQw4w9WgXcQ "fr,en,de"
```

**输出：** 包含 `video_id`、`title`、`author`、`full_text` 以及带有时间戳的 `transcript` 数组的 JSON 数据。

## 工作流程

1. 使用视频 ID 或 URL 运行 `fetch_transcript.py` 脚本。
2. 脚本会检查是否需要使用 VPN；如有需要，会自动启动 VPN。
3. 返回包含完整字幕文本的 JSON 数据。
4. 根据需要对 `full_text` 字段进行总结。

## 语言代码

默认优先顺序：`en, fr, de, es, it, pt, nl`

可以通过第二个参数进行覆盖：`python3 scripts/fetch_transcript.py VIDEO_ID "ja,ko,zh"`

## 设置与配置

请参阅 [references/SETUP.md](references/SETUP.md) 以了解以下内容：
- Python 依赖项的安装
- WireGuard VPN 的配置（适用于云虚拟专用服务器）
- 常见错误的排查方法
- 可选的代理服务器选项