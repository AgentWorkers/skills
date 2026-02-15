---
name: clipboard
description: "在任何 OpenClaw 会话中，都可以使用 `xclip` 命令与系统的剪贴板进行交互（仅支持文本数据）。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📋",
        "requires": { "bins": ["xclip"] },
        "install":
          [
            {
              "id": "dnf",
              "kind": "dnf",
              "package": "xclip",
              "bins": ["xclip"],
              "label": "Install xclip (dnf)",
            },
          ],
      },
  }
---

# 复制粘贴功能

允许从任何 OpenClaw 会话中与系统剪贴板（仅支持文本）进行交互。在 Linux 系统上使用 `xclip` 工具来实现相关操作。

## 复制到剪贴板

将文本复制到剪贴板：

```bash
echo "Hello, world!" | xclip -selection clipboard
```

## 从剪贴板粘贴

输出剪贴板中的当前内容：

```bash
xclip -selection clipboard -o
```

## 复制文件内容

将文件的内容复制到剪贴板：

```bash
xclip -selection clipboard < /path/to/file.txt
```

## 安装

```bash
sudo dnf install xclip
```