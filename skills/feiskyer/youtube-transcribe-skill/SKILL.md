---
name: youtube-transcribe-skill
description: '从YouTube视频中提取字幕/文本。触发词：`youtube transcript`、`extract subtitles`、`video captions`、`video subtitles`、`subtitle extraction`、`YouTube to text`、`extract subtitles`.'
allowed-tools: Read, Write, Glob, Grep, Task, Bash(cat:*), Bash(ls:*), Bash(tree:*), Bash(yt-dlp:*), Bash(which:*), mcp__plugin_claude-code-settings_chrome__*
---
# 从YouTube视频中提取字幕/文字记录

从YouTube视频URL中提取字幕/文字记录，并将其保存为本地文件。

输入的YouTube视频URL：$ARGUMENTS

## 第1步：验证URL并获取视频信息

1. **验证URL格式**：确认输入的URL是有效的YouTube URL（支持`youtube.com/watch?v=`或`youtu.be/`格式）。

2. **获取视频信息**：使用WebFetch或firecrawl工具获取页面内容，并提取视频标题，用于后续的文件命名。

## 第2步：使用命令行工具快速提取字幕（优先尝试）

使用命令行工具快速提取字幕。

1. **检查工具是否可用**：
   执行`which yt-dlp`。

   - 如果找到`yt-dlp`，则继续进行字幕下载。
   - 如果没有找到`yt-dlp`，则立即跳转到**第3步**。

2. **执行字幕下载**（仅当找到`yt-dlp`时）：

   - **提示**：务必添加`--cookies-from-browser`选项以避免登录限制。默认使用Chrome浏览器。
   - **重试逻辑**：如果`yt-dlp`因浏览器问题（例如“无法打开Chrome”）而失败，请求用户指定可用的浏览器（如Firefox、Safari、Edge），然后重新尝试。

   ```bash
   # Get the title first (try chrome first)
   yt-dlp --cookies-from-browser=chrome --get-title "[VIDEO_URL]"

   # Download subtitles
   yt-dlp --cookies-from-browser=chrome --write-auto-sub --write-sub --sub-lang zh-Hans,zh-Hant,en --skip-download --output "<Video Title>.%(ext)s" "[VIDEO_URL]"
   ```

3. **验证结果**：
   - 检查命令的退出代码。
   - **退出代码0（成功）**：字幕已成功保存到本地，任务完成。
   - **退出代码非0（失败）**：
     - 如果错误与浏览器/cookies有关，请用户提供正确的浏览器信息并重新尝试第2步。
     - 如果是其他错误（例如视频无法访问），则跳转到**第3步**。

## 第3步：使用浏览器自动化提取字幕（备用方案）

当命令行方法失败或`yt-dlp`不可用时，使用浏览器自动化工具来提取字幕。

1. **检查工具是否可用**：
   - 检查`chrome-devtools-mcp`工具（特别是`mcp__plugin_claude-code-settings_chrome__new_page`）是否可用。
   - **关键检查**：如果`chrome-devtools-mcp`不可用，并且在第2步中也没有找到`yt-dlp`：
     - **停止执行**。
     - **通知用户**：“无法继续。请安装`yt-dlp`（以使用命令行快速提取字幕），或配置`chrome-devtools-mcp`（以使用浏览器自动化工具）。”

2. **初始化浏览器会话**（如果工具可用）：
   调用`mcp__plugin_claude-code-settings_chrome__new_page`来打开视频URL。

### 3.2 分析页面状态

调用`mcp__plugin_claude-code-settings_chrome__take_snapshot`来获取页面的访问权限树（accessibility tree）。

### 3.3 展开视频描述

**原因**：“显示字幕”按钮通常隐藏在视频标题下方的描述区域中。

1. 在页面快照中搜索标有“...more”、“...更多”或“Show more”等字样的按钮。
2. 调用`mcp__plugin_claude-code-settings_chrome__click`来点击该按钮。

### 3.4 打开字幕面板

1. 调用`mcp__plugin_claude-code-settings_chrome__take_snapshot`来获取更新后的用户界面快照。
2. 在快照中搜索标有“Show transcript”、“显示转录稿”或“内容转文字”等字样的按钮。
3. 调用`mcp__plugin_claude-code-settings_chrome__click`来点击该按钮。

### 3.5 通过DOM提取内容

**原因**：直接从访问权限树中读取长列表内容效率较低且会消耗大量系统资源；使用DOM操作更为高效。

调用`mcp__plugin_claude-code-settings_chrome__evaluate_script`来执行以下JavaScript代码：

```javascript
() => {
  // Select all transcript segment containers
  const segments = document.querySelectorAll("ytd-transcript-segment-renderer");
  if (!segments.length) return "BUFFERING"; // Retry if empty

  // Iterate and format as "timestamp text"
  return Array.from(segments)
    .map((seg) => {
      const time = seg.querySelector(".segment-timestamp")?.innerText.trim();
      const text = seg.querySelector(".segment-text")?.innerText.trim();
      return `${time} ${text}`;
    })
    .join("\n");
};
```

如果返回“BUFFERING”（表示正在加载中），请等待几秒钟后再尝试。

### 3.6 保存和清理

1. 使用Write工具将提取到的文本保存为本地文件（例如 `<Video Title>.txt`）。
2. 调用`mcp__plugin_claude-code-settings_chrome__close_page`来释放系统资源。

## 输出要求

- 将字幕文件保存到当前工作目录。
- 文件名格式：`<Video Title>.txt`
- 文件内容格式：每行应包含“时间戳 字幕文本”。
- 完成后输出结果：文件路径、字幕语言以及字幕的总行数。