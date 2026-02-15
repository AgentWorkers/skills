---
name: file-search
description: "使用 `fd` 和 `rg`（ripgrep）快速搜索文件名和文件内容。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["fd", "rg"] },
        "install":
          [
            {
              "id": "dnf-fd",
              "kind": "dnf",
              "package": "fd-find",
              "bins": ["fd"],
              "label": "Install fd-find (dnf)",
            },
            {
              "id": "dnf-rg",
              "kind": "dnf",
              "package": "ripgrep",
              "bins": ["rg"],
              "label": "Install ripgrep (dnf)",
            },
          ],
      },
  }
---

# 文件搜索技巧

使用 `fd` 和 `rg`（ripgrep）快速搜索文件名和文件内容。

## 按名称查找文件

搜索与指定模式匹配的文件：

```bash
fd "\.rs$" /home/xrx/projects
```

按文件名精确查找文件：

```bash
fd -g "Cargo.toml" /home/xrx/projects
```

## 搜索文件内容

在文件中搜索正则表达式模式：

```bash
rg "TODO|FIXME" /home/xrx/projects
```

带上下文行进行搜索：

```bash
rg -C 3 "fn main" /home/xrx/projects --type rust
```

## 安装

```bash
sudo dnf install fd-find ripgrep
```