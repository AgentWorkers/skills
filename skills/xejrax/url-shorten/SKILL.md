---
name: url-shorten
description: "通过 tinyurl 或 bitly API 缩短 URL"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔗",
        "requires": { "bins": ["curl"] },
        "install": [],
      },
  }
---

# URL缩短

可以通过 tinyurl 或 bitly API 来缩短 URL。使用 bitly 时需要设置 `BITLY_TOKEN` 环境变量；如果未设置，则会自动回退到使用 tinyurl。

## 命令

```bash
# Shorten a URL (uses tinyurl by default, bitly if BITLY_TOKEN is set)
url-shorten "https://example.com/very/long/path/to/resource"
```

## 安装

无需安装任何软件。系统上通常已经安装了 `curl`。可以选择设置 `BITLY_TOKEN` 环境变量，以使用 bitly API 而不是 tinyurl。