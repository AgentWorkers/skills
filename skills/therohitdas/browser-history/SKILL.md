# 技能：浏览器历史记录 —— 搜索 Chrome 的浏览记录

可以搜索 Das 的 Chrome 浏览历史记录，以找到他之前访问过的网址、视频和网站。

## Chrome 历史记录的存储位置

```
~/Library/Application Support/Google/Chrome/Default/History
```

历史记录数据存储在 SQLite 数据库中。如果 Chrome 没有锁定该数据库，可以直接对其进行查询。

---

## 搜索命令

### 基本搜索（网址或标题中包含指定关键词）
```bash
sqlite3 ~/Library/Application\ Support/Google/Chrome/Default/History \
  "SELECT url, title FROM urls WHERE url LIKE '%TERM%' OR title LIKE '%TERM%' ORDER BY last_visit_time DESC LIMIT 10;"
```

### 仅搜索 YouTube 视频
```bash
sqlite3 ~/Library/Application\ Support/Google/Chrome/Default/History \
  "SELECT url, title FROM urls WHERE url LIKE '%youtube.com/watch%' AND (url LIKE '%TERM%' OR title LIKE '%TERM%') ORDER BY last_visit_time DESC LIMIT 10;"
```

### 最常访问的网站（所有时间）
```bash
sqlite3 ~/Library/Application\ Support/Google/Chrome/Default/History \
  "SELECT url, title, visit_count FROM urls ORDER BY visit_count DESC LIMIT 20;"
```

### 最近访问的网站
```bash
sqlite3 ~/Library/Application\ Support/Google/Chrome/Default/History \
  "SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 20;"
```

---

## 如果数据库被锁定

Chrome 在运行时会锁定历史记录文件。此时有以下两种解决方案：

1. **先复制数据：**
   ```bash
   cp ~/Library/Application\ Support/Google/Chrome/Default/History /tmp/chrome_history
   sqlite3 /tmp/chrome_history "SELECT ..."
   ```

2. **使用 WAL 模式**（通常即使在 Chrome 打开的情况下也能正常使用）：
   由于 SQLite 支持 WAL（Write-Ahead Logging）模式，`sqlite3` 命令通常仍然可以执行查询操作。

---

## 在 Chrome 中打开网址

```bash
open -a "Google Chrome" "URL_HERE"
```

## 隐藏/最小化 Chrome 窗口

```bash
osascript -e 'tell application "System Events" to set visible of process "Google Chrome" to false'
```

---

## Das 常使用的搜索词

| 搜索内容 | 搜索关键词 |
|------|-------------|
| Brain.fm 的专注音乐 | `brain.fm` |
| YouTube 视频 | `youtube.com/watch` |
| GitHub 仓库 | `github.com` |
| 文本转录 API | `transcriptapi` 或 `youtubetotranscript` |