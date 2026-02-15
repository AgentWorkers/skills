---
name: gifgrep
description: 通过 CLI/TUI 搜索 GIF 提供商，下载结果，并提取其中的静态图片（stills）或动画帧（sheets）。
homepage: https://gifgrep.com
metadata: {"clawdbot":{"emoji":"🧲","requires":{"bins":["gifgrep"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/gifgrep","bins":["gifgrep"],"label":"Install gifgrep (brew)"},{"id":"go","kind":"go","module":"github.com/steipete/gifgrep/cmd/gifgrep@latest","bins":["gifgrep"],"label":"Install gifgrep (go)"}]}}
---

# gifgrep

使用 `gifgrep` 可以搜索 GIF 图片提供者（如 Tenor/Giphy），在图形用户界面（TUI）中浏览结果，下载图片，并提取静态帧或图片切片。

**GIF-Grab（gifgrep 的工作流程）**  
- 搜索 → 预览 → 下载 → 提取静态帧或图片切片，便于快速查看和分享。

**快速入门**  
- `gifgrep cats --max 5`  
- `gifgrep cats --format url | head -n 5`  
- `gifgrep search --json cats | jq '.[0].url'`  
- `gifgrep tui "office handshake"`  
- `gifgrep cats --download --max 1 --format url`

**图形用户界面（TUI）与预览**  
- 在 TUI 中搜索：`gifgrep tui "query"`  
- 通过 CLI 查看静态帧预览：`--thumbs`（仅支持 Kitty/Ghostty 格式；显示静态帧）

**下载与显示**  
- `--download`：将下载的图片保存到 `~/Downloads`  
- `--reveal`：在 Finder 中显示最近下载的图片

**提取静态帧或图片切片**  
- `gifgrep still ./clip.gif --at 1.5s -o still.png`  
- `gifgrep sheet ./clip.gif --frames 9 --cols 3 -o sheet.png`  
- 图片切片：由多个静态帧组成的 PNG 文件（适合快速查看、制作文档或用于聊天）。  
- 可调整参数：`--frames`（帧数）、`--cols`（网格列数）、`--padding`（间距）。

**图片提供者**  
- `--source auto|tenor|giphy`  
- 使用 `--source giphy` 时需要 `GIPHY_API_KEY`  
- `TENOR_API_KEY` 是可选的（如果未设置，则使用 Tenor 的演示 API 密钥）

**输出格式**  
- `--json`：输出结果数组（包含 `id`、`title`、`url`、`preview_url`、`tags`、`width`、`height`）  
- `--format`：用于格式化输出内容（例如，仅输出 `url`）

**环境配置**  
- `GIFGREP_SOFTWARE_ANIM=1`：强制显示软件动画效果  
- `GIFGREP_CELL_ASPECT=0.5`：调整预览图像的显示比例