---
name: markdown-viewer
description: 实时Markdown查看器，支持AI协同编辑功能。在协作过程中，所有更改会立即显示在页面上。兼容任何AI助手和网页浏览器。
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

这是一个用于AI协同编辑的实时Markdown查看器。在您进行协作时，所有更新会立即显示在浏览器中。该工具支持与任何AI工具以及网页浏览器配合使用。

GitHub仓库：[wipcomputer/wip-markdown-viewer](https://github.com/wipcomputer/wip-markdown-viewer)  
npm包：[@wipcomputer/markdown-viewer](https://www.npmjs.com/package/@wipcomputer/markdown-viewer)

## 安装

```bash
npm install -g @wipcomputer/markdown-viewer
```

此命令会将`mdview`模块全局安装到系统中。该工具没有运行时依赖项，完全基于Node.js实现。

## 快速入门

1. 启动服务器（仅绑定到本地地址`127.0.0.1`，不会暴露在网络中）：
   ```bash
curl -s http://127.0.0.1:3000/ > /dev/null 2>&1 || mdview &
```

2. 使用默认浏览器打开目标Markdown文件：
   ```bash
# macOS
open "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"

# Linux
xdg-open "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"

# Windows
start "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"
```

## 工作原理

- 指令您的AI编程工具全局安装`@wipcomputer/markdown-viewer`；
- 命令AI在Markdown查看器中打开相应的`.md`文件；
- AI会在您的默认浏览器中显示文件内容；
- 每次保存文件后，页面会立即重新渲染，无需手动刷新。

您可以同时打开多个标签页来处理多个文档。

## 安全性

- 服务器仅绑定到`127.0.0.1`，无法从外部机器访问；
- `/view?path=`参数用于从本地文件系统中读取文件。建议使用`--root <dir>`参数来限制访问范围（例如，仅允许访问特定目录）；
- 该工具没有npm依赖项，因此不存在供应链安全风险（仅依赖于Node.js本身）。

## 主要功能

- 支持SSE（Server-Sent Events）技术，实现实时页面刷新（兼容Safari、Chrome、Firefox浏览器）；
- 支持多文件编辑（每个标签页独立显示对应文件内容）；
- 支持GitHub风格的Markdown格式（包括表格、任务列表、下划线标注等）；
- 提供语法高亮显示（支持180多种编程语言）；
- 提供暗黑模式；
- 支持自动生成目录结构；
- 支持Mermaid图表和KaTeX数学公式显示。

## 注意事项

- 服务器默认运行在`http://127.0.0.1:3000`端口，可通过`mdview --port 8080`更改端口；
- 服务器在系统重启后不会自动恢复运行，但可以通过`curl`命令进行手动重启。