---
name: brew-install
description: "通过 dnf（Fedora/Bazzite 的包管理器）安装缺失的二进制文件。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📦",
        "requires": { "bins": ["dnf"] },
        "install": [],
      },
  }
---

# Brew 安装

通过 dnf（Fedora/Bazzite 的包管理器）来安装缺失的二进制文件。尽管名称中包含“Brew”，但实际上这个技巧是在 Bazzite 环境中使用 dnf 而不是 Homebrew 来完成安装的。

## 命令

```bash
# Install a package
brew-install <package>

# Search for a package
brew-install search <query>
```

## 安装过程

无需额外安装。dnf 是 Fedora/Bazzite 的默认包管理器，因此它始终存在于系统中。