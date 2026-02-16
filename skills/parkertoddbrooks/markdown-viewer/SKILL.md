---
name: markdown-viewer
description: 实时Markdown查看器，支持AI协同编辑功能。在协作过程中，所有更改会立即显示在页面上。该工具兼容任何AI辅助工具和网页浏览器。
homepage: https://github.com/wipcomputer/wip-markdown-viewer
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires": { "bins": ["node", "curl"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@wipcomputer/markdown-viewer",
              "global": true,
              "bins": ["mdview"],
              "label": "Install markdown-viewer (npm)",
            },
          ],
      },
  }
---
# 实时Markdown查看器

这是一个用于AI协同编辑的实时Markdown查看器。在您进行协作时，所有更改会立即呈现出来。该工具兼容任何AI助手和网页浏览器。

## 安装

```bash
npm install -g @wipcomputer/markdown-viewer
```

此命令会将`mdview`全局安装到系统中。无需任何运行时依赖项，完全基于Node.js实现。

来源：[github.com/wipcomputer/wip-markdown-viewer](https://github.com/wipcomputer/wip-markdown-viewer)

## 快速入门

1. 启动服务器（仅绑定到`127.0.0.1`端口，不会暴露到外部网络）：

```bash
curl -s http://127.0.0.1:3000/ > /dev/null 2>&1 || mdview &
```

2. 在您的默认浏览器中打开一个Markdown文件：

```bash
# macOS
open "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"

# Linux
xdg-open "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"

# Windows
start "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"
```

## 工作原理

1. 告诉您的AI编程工具全局安装`@wipcomputer/markdown-viewer`；
2. 指令AI在Markdown查看器中打开相应的Markdown文件；
3. AI会在您的默认浏览器中显示该文件；
4. 每次保存文件时，页面会立即重新渲染，无需手动刷新。

您可以同时打开多个标签页来处理多个文档。

## 安全性

- 服务器仅绑定到`127.0.0.1`端口，无法从其他机器访问；
- `/view?path=`参数用于从本地文件系统中读取文件，这是本地查看器的正常行为。请勿将此端口暴露给不受信任的网络；
- 该工具完全不依赖npm包，因此不存在供应链安全风险（仅依赖于Node.js本身）。

## 主要功能

- 支持SSE技术的实时页面刷新（兼容Safari、Chrome、Firefox浏览器）；
- 多文件支持（每个标签页独立显示对应的文件）；
- 支持GitHub风格的Markdown格式（包括表格、任务列表、下划线标记等）；
- 语法高亮显示（支持180多种编程语言）；
- 深色模式；
- 提供目录导航功能；
- 支持Mermaid图表和KaTeX数学公式。

## 注意事项

- 服务器默认运行在`http://127.0.0.1:3000`端口，您可以通过`mdview --port 8080`来更改端口；
- 服务器在系统重启后不会自动恢复运行，但“快速入门”指南中的curl命令会自动重启服务器（如有需要）。