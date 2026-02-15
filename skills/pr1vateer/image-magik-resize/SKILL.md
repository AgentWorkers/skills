---
name: resize-magic
version: 0.1.0
author: Stenkil <you@example.com>
description: 使用 ImageMagick（命令行接口，CLI）调整图像大小。该脚本是一个 Bash 脚本。
entrypoint: scripts/resize.sh
metadata: { "openclaw": { "emoji": "🖼️", "requires": { "bins": ["bash"], "anyBins": ["magick","convert"] }, "install": [ { "id": "brew", "kind": "brew", "formula": "imagemagick", "bins": ["magick","convert"], "label": "Install ImageMagick (brew)" } ] } }
user-invocable: true
command-dispatch: tool
command-tool: resize
commands:
  - name: resize
    usage: resize <input-path> <geometry> [output-path]
    description: |
      Resize an image using ImageMagick.
      Geometry examples:
        - 800x        -> width 800, preserve aspect ratio
        - 800x600     -> exact geometry (may change aspect)
        - 50%         -> scale to 50% of original
        - 800x800\>   -> resize only if larger than 800x800
---
## 概述

此技能提供了一个名为 `scripts/resize.sh` 的可执行脚本，代理程序（或 `openclaw` 命令行界面）可以调用该脚本来使用 ImageMagick 对图像进行缩放操作。

## 安装（手动）

将此文件夹复制到您的 OpenClaw 技能目录中，例如：

```bash
cp -r resize-magic ~/.openclaw/skills/resize-magic

# or install via CLI if available
openclaw skill install ./resize-magic
```