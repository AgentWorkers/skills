# Podman 浏览器技能

使用 Podman 和 Playwright 实现无头浏览器自动化，用于抓取由 JavaScript 渲染的页面。

## 前提条件

- 安装并运行 Podman 5.x 或更高版本
- 安装 Node.js 18 或更高版本（用于运行命令行工具）
- 拥有互联网连接（首次运行时会下载约 1.5GB 的容器镜像）

## 安装

创建一个符号链接以便于使用：

```bash
chmod +x browse.js
ln -sf "$(pwd)/browse.js" ~/.local/bin/podman-browse
```

首次运行时会下载 Playwright 容器镜像（约 1.5GB）。

## 命令

### `podman-browse`（或 `./browse.js`）

获取由 JavaScript 渲染的页面并返回其文本内容。

```bash
podman-browse "https://example.com"
```

**选项：**
- `--html` - 返回原始 HTML 内容而非纯文本
- `--wait <ms>` - 在页面加载完成后等待指定时间（默认值：2000 毫秒）
- `--selector <css>` - 等待特定元素出现后再进行操作
- `-h, --help` - 显示帮助信息

**示例：**
```bash
# Get rendered text content from Hacker News
podman-browse "https://news.ycombinator.com"

# Get raw HTML
podman-browse --html "https://news.ycombinator.com"

# Wait for specific element
podman-browse --selector ".itemlist" "https://news.ycombinator.com"

# Extra wait time for slow pages
podman-browse --wait 5000 "https://news.ycombinator.com/newest"
```

## 工作原理

1. 通过 Podman 运行微软官方提供的 Playwright 容器
2. 使用 Chromium 在无头模式下执行页面渲染
3. 等待 JavaScript 完成页面渲染（使用 `networkidle` 指令以及自定义等待时间）
4. 返回页面的文本内容或 HTML 内容

## 容器镜像

使用 `mcr.microsoft.com/playwright:v1.50.0-noble`，并依赖 `playwright@1.50.0` 的 npm 包（版本必须一致）。

## 相关文件

- `browse.js`：一个独立的 Node.js 命令行工具，用于处理参数并启动 Podman 容器
- `SKILL.md`：本文档文件

## 注意事项

- 首次运行时会下载容器镜像（约 1.5GB）
- 为确保 Chromium 的稳定性，使用 `--ipc=host` 选项
- 使用 `--init` 选项来处理可能产生的僵尸进程（zombie processes）
- 以 root 用户权限运行时禁用沙箱模式（适用于可信网站）
- 每次运行都会创建一个新的容器（环境会被清空，但启动过程需要约 10-15 秒）