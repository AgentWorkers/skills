---
name: markdown-viewer
description: 实时Markdown查看器，支持AI协同编辑功能。在协作过程中，所有更改会立即显示在页面上。兼容任何AI工具和网页浏览器。
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

这是一个专为AI协同编辑设计的实时Markdown查看器。在协作过程中，任何更新都会立即显示在浏览器中。该工具兼容任何AI编辑工具和网页浏览器。

GitHub仓库：[wipcomputer/wip-markdown-viewer](https://github.com/wipcomputer/wip-markdown-viewer)  
npm包：[@wipcomputer/markdown-viewer](https://www.npmjs.com/package/@wipcomputer/markdown-viewer)

## 安装

```bash
npm install -g @wipcomputer/markdown-viewer
```

此命令会将`mdview`模块全局安装到系统中。该工具无需任何运行时依赖，完全基于Node.js开发。

## 快速入门

1. 启动服务器（仅绑定到本地地址127.0.0.1，不会暴露在网络中）：
```bash
curl -s http://127.0.0.1:3000/ > /dev/null 2>&1 || mdview &
```

2. 在默认浏览器中打开目标Markdown文件：
```bash
# macOS
open "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"

# Linux
xdg-open "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"

# Windows
start "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"
```

## 工作原理

- 请指示您的AI编辑工具全局安装`@wipcomputer/markdown-viewer`；
- 请让AI使用`mdview`插件打开Markdown文件；
- AI会在您的默认浏览器中显示文件内容；
- 每次保存文件时，页面会立即重新渲染，无需手动刷新。

您可以同时打开多个标签页来处理多个文档。

## 安全性

- 服务器仅绑定到本地地址127.0.0.1，无法被外部机器访问；
- `/view?path=`参数用于从用户的本地文件系统中读取文件。建议使用`--root <dir>`选项来限制访问范围（适用于共享环境）；
- 该工具完全依赖Node.js本身，不存在供应链安全风险。

## 主要功能

- 支持SSE（Server-Side Rendering）技术，实现实时页面刷新（兼容Safari、Chrome、Firefox浏览器）；
- 支持多文件编辑（每个标签页独立处理对应的Markdown文件）；
- 支持GitHub风格的Markdown格式（包括表格、任务列表、删除线等）；
- 提供语法高亮显示（支持180多种编程语言）；
- 提供暗黑模式；
- 支持自动生成目录结构；
- 支持Mermaid图表和KaTeX数学公式。

## 常见问题解决方法

- **页面显示的是目录列表而非文件内容？**：可能是由于在启动服务器时使用了`--root`选项。请取消该选项后重新启动服务器。
- **Safari浏览器卡顿或显示空白页面？**：尝试强制刷新（Cmd+Shift+R）或重启服务器。Safari浏览器会对SSE请求进行频繁缓存。
- **在macOS系统中，使用`open`命令时查询字符串丢失？**：建议使用AppleScript来打开文件：
```bash
osascript -e 'tell application "Safari" to open location "http://127.0.0.1:3000/view?path=/your/file.md"'
```

## 其他注意事项

- 服务器默认运行在`http://127.0.0.1:3000`端口。如需更改端口，可使用`mdview --port 8080`；
- 服务器在系统重启后不会自动恢复运行。可以通过`curl`命令检查服务器状态，并在需要时手动重启；
- **切勿使用带有文件路径的参数来启动服务器**：务必直接运行`mdview`命令。使用路径参数会导致服务器仅处理指定目录内的文件；
- 可以将任何Markdown文件直接拖放到浏览器首页进行查看；
- 该工具不发送任何外部请求，所有依赖项均已集成在本地环境中。