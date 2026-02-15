---
name: blogwatcher
description: 使用 blogwatcher CLI 监控博客以及 RSS/Atom 订阅源以获取更新。
homepage: https://github.com/Hyaxia/blogwatcher
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["blogwatcher"]},"install":[{"id":"go","kind":"go","module":"github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest","bins":["blogwatcher"],"label":"Install blogwatcher (go)"}]}}
---

# blogwatcher

使用 `blogwatcher` 命令行工具（CLI）来跟踪博客以及 RSS/Atom 订阅源的更新。

**安装：**
- 使用 Go 语言安装：`go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest`

**快速入门：**
- `blogwatcher --help` （显示命令帮助信息）

**常用命令：**
- 添加博客：`blogwatcher add "我的博客" https://example.com`  
- 列出所有博客：`blogwatcher blogs`  
- 扫描更新：`blogwatcher scan`  
- 列出文章：`blogwatcher articles`  
- 将文章标记为已读：`blogwatcher read 1`  
- 将所有文章标记为已读：`blogwatcher read-all`  
- 删除博客：`blogwatcher remove "我的博客"`  

**示例输出：**
```
$ blogwatcher blogs
Tracked blogs (1):

  xkcd
    URL: https://xkcd.com
```  
```
$ blogwatcher scan
Scanning 1 blog(s)...

  xkcd
    Source: RSS | Found: 4 | New: 4

Found 4 new article(s) total!
```  

**备注：**  
- 使用 `blogwatcher <命令> --help` 可以查看该命令的详细参数和选项。