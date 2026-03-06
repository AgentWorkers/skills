---
name: pinterest-scraper
description: Full-featured Pinterest image scraper with infinite scroll, quality options, Telegram integration, duplicate detection, resume support, and verbose logging. Use when: (1) Scraping Pinterest boards/users/search, (2) Need quality options (originals/736x/474x/236x), (3) Sending images to Telegram, (4) Resuming interrupted scrapes, (5) Avoiding duplicate downloads, (6) Debugging with verbose logs.
version: 1.1.0
changelog: "v1.1.0: Added reasoning framework, decision trees, troubleshooting, self-checks"
metadata:
  openclaw:
    requires:
      bins:
        - python3
      pip:
        - playwright
        - requests
    emoji: "📌"
    category: "utility"
    homepage: https://github.com/KeXu9/pinterest-scraper
---

# Pinterest 图片抓取工具

这是一个功能齐全的 Pinterest 图片抓取工具，支持自动滚动和多种输出格式。

## 该工具的触发条件

当用户需要从 Pinterest 下载图片时，该工具会被激活。

## 工作流程

| 步骤 | 操作 | 原因 |
|------|--------|-----|
| 1 | **解析 URL** | 解析 Pinterest URL，确定要抓取的板块、用户或搜索内容 |
| 2 | **启动浏览器** | 使用 Playwright 浏览器，并开启隐身模式 |
| 3 | **自动滚动** | 逐步加载图片（Pinterest 使用无限滚动功能） |
| 4 | **提取图片 URL** | 提取图片的 URL，并根据需求选择质量 |
| 5 | **去重** | 通过哈希值检测重复的图片 |
| 6 | **下载图片** | 将图片保存到指定的输出文件夹 |
| 7 | **通知用户** | 可选：将图片发送到 Telegram |

---

## 设置

（相关设置代码请参见 **```bash
pip install playwright requests
playwright install chromium
```**）

---

## 决策树

### 您想做什么？

（相关决策流程请参见 **```
├── Download images from a board/user
│   └── Use: -u "URL" -s [scrolls]
│
├── Get highest quality possible
│   └── Use: -q originals
│
├── Get smaller/faster downloads
│   └── Use: -q 736x or 236x
│
├── Send images to phone
│   └── Use: --telegram --token X --chat Y
│
├── Resume interrupted scrape
│   └── Use: --resume
│
└── Debug issues
    └── Use: -v (verbose logging)
```**）

### 图片质量选择

| 图片质量 | 适用场景 | 文件大小 |
|---------|----------|-----------|
| 原图质量 | 最高质量，适合存档 | 文件最大 |
| 736x | 平衡较好的质量 | 文件中等大小 |
| 474x | 缩略图质量 | 文件较小 |
| 236x | 仅用于预览 | 文件最小 |
| 全部质量 | 保存所有版本的图片 | 文件总量最大 |

---

## 使用方法

### 命令行参数

（相关参数说明请参见 **```bash
python scrape_pinterest.py -u "URL" [options]
```**）

| 参数 | 说明 | 默认值 |
|--------|-------------|---------|
| `-u, --url` | Pinterest URL | 必填 |
| `-s, --scrolls` | 自动滚动的次数 | 50 |
| `-o, --output` | 输出文件夹 | ./pinterest_output |
| `-q, --quality` | 图片质量：原图/736x/474x/236x/全部 | 原图质量 |
| `-v, --verbose` | 开启详细日志记录 | 否 |
| `--telegram` | 将图片发送到 Telegram | 否 |
| `--token` | Telegram 机器人token | 未提供 |
| `--chat` | Telegram 聊天 ID | 未提供 |
| `--resume` | 从上次抓取处继续 | 否 |
| `--dedup` | 禁用去重 | 否 |
| `--no-dedup` | 启用去重 | 否 |
| `--telegram-only` | 仅发送已存在的图片 | 否 |

### 常见用法示例

（相关示例请参见 **```bash
# Basic scrape (50 scrolls, originals, current dir)
python scrape_pinterest.py -u "URL"

# Verbose mode (logs to console + scrape.log)
python scrape_pinterest.py -u "URL" -v

# More scrolls, custom output, medium quality
python scrape_pinterest.py -u "URL" -s 100 -o ./output -q 736x -v

# With Telegram delivery
python scrape_pinterest.py -u "URL" --telegram --token "TOKEN" --chat "CHAT_ID"

# Resume interrupted scrape
python scrape_pinterest.py -u "URL" --resume -v

# Show help
python scrape_pinterest.py --help
```**）

---

## Python API

该工具基于命令行界面，可以通过 Python 代码调用：

（相关 API 说明请参见 **```python
import subprocess
import os

# Run the scraper
result = subprocess.run(
    ['python3', 'scrape_pinterest.py', '-u', 'URL', '-s', '50', '-q', 'originals'],
    cwd='./scripts',
    capture_output=True,
    text=True
)

print(result.returncode)  # 0 = success
print(result.stdout)
```**）

---

## 主要功能

- **无限滚动**：自动滚动以加载更多图片 |
- **图片质量选择**：支持原图质量、736x、474x、236x 或全部质量 |
- **直接发送到 Telegram**：支持将图片发送到 Telegram |
- **去重功能**：通过哈希值检测重复的图片 |
- **继续抓取**：可以从上次抓取的位置继续 |
- **支持的 URL 类型**：板块、用户个人资料和搜索结果 |
- **详细日志记录**：通过 `-v` 参数开启详细日志记录（输出到控制台和 `scrape.log` 文件）

---

## 详细日志记录

使用 `-v` 或 `--verbose` 参数开启详细日志记录：

- 滚动进度（每滚动 10 次记录一次）
- 每次滚动找到的图片数量 |
- 下载进度 |
- 图片发送到 Telegram 的状态 |
- 错误和警告信息

**日志文件**：
- 控制台：INFO 级别
- `scrape.log`：DEBUG 级别（详细日志）

---

## 常见问题及解决方法

### 问题：未下载到图片

- **原因**：滚动次数不足，导致 Pinterest 未加载所有图片 |
- **解决方法**：增加 `-s` 参数的值（建议尝试 100-200） |

### 问题：无法找到浏览器

- **原因**：未安装 Playwright |
- **解决方法**：运行 `playwright install chromium` 安装 Playwright 和 Chromium 浏览器 |

### 问题：SSL 证书错误（Mac）

- **原因**：macOS 的 SSL 问题 |
- **解决方法**：在请求请求中设置 `verify=False` 参数 |

### 问题：出现重复图片

- **原因**：去重功能被禁用或失败 |
- **解决方法**：使用 `--dedup` 参数（默认为启用）

### 问题：无法继续抓取

- **原因**：状态文件丢失或 URL 发生变化 |
- **解决方法**：使用与上次抓取相同的 URL，并检查 `.scrape_state.json` 文件 |

### 问题：无法将图片发送到 Telegram

- **原因**：Token 或聊天 ID 不正确，或 Telegram 有发送限制 |
- **解决方法**：验证 Telegram 机器人 token 和聊天 ID；注意 Telegram 每批次最多只能发送 100 张图片 |

### 问题：详细日志无法记录

- **原因**：输出目录的写入权限问题 |
- **解决方法**：检查输出目录的写入权限设置 |

---

## 自我检查

- Pinterest URL 是否有效（板块/用户/搜索内容） |
- 是否安装了 Playwright（运行 `playwright install chromium`） |
- 选择的图片质量是否适合当前需求 |
- 输出目录是否存在且可写入 |
- 对于使用 Telegram 的情况，确保 Token 和聊天 ID 正确 |
- 对于继续抓取的情况，确保使用与上次相同的 URL |

---

## 注意事项

- Pinterest 的图片是动态加载的，需要自动滚动才能获取更多图片 |
- 在 macOS 上使用请求时，建议设置 `verify=False` 以避免 SSL 问题 |
- 状态信息会保存在 `.scrape_state.json` 文件中，用于下次继续抓取 |
- Telegram 每批次最多只能发送 100 张图片 |
- 详细日志会记录在 `scrape.log` 文件中 |

---

## 快速参考

| 功能 | 命令示例 |
|------|---------|
| 基本抓取 | `python scrape_pinterest.py -u "URL"` |
| 详细日志 | `python scrape_pinterest.py -u "URL" -v` |
- 高质量图片 | `python scrape_pinterest.py -u "URL" -q originals` |
- 小尺寸图片 | `python scrape_pinterest.py -u "URL" -q 236x` |
| 发送到 Telegram | `python scrape_pinterest.py -u "URL" --telegram --token X --chat Y` |
| 继续抓取 | `python scrape_pinterest.py -u "URL" --resume` |
| 自定义输出目录 | `python scrape_pinterest.py -u "URL" -o ./myfolder` |