---
name: web-monitor
description: 监控网页内容的变化并接收警报。可以跟踪URL、检测更新、查看差异。适用于需要监视网站、跟踪页面变化、监控新帖子/内容、设置页面变更警报或检查网站是否更新的场景。支持使用CSS选择器进行有针对性的监控。
---

# 网页监控器

用于跟踪网页的变化，存储快照，计算差异，并支持CSS选择器。

## 快速入门

```bash
# Add a URL to watch
uv run --with beautifulsoup4 python scripts/monitor.py add "https://example.com" --name "Example"

# Add with CSS selector (monitor specific section)
uv run --with beautifulsoup4 python scripts/monitor.py add "https://example.com/pricing" -n "Pricing" -s ".pricing-table"

# Check all watched URLs for changes
uv run --with beautifulsoup4 python scripts/monitor.py check

# Check one specific URL
uv run --with beautifulsoup4 python scripts/monitor.py check "Example"

# List watched URLs
uv run --with beautifulsoup4 python scripts/monitor.py list

# View last diff
uv run --with beautifulsoup4 python scripts/monitor.py diff "Example"

# View current snapshot
uv run --with beautifulsoup4 python scripts/monitor.py snapshot "Example" --lines 50

# Remove
uv run --with beautifulsoup4 python scripts/monitor.py remove "Example"
```

## 命令

| 命令 | 参数 | 说明 |
|---------|------|-------------|
| `add` | `<url> [-n name] [-s selector]` | 添加要监控的URL，并生成初始快照 |
| `remove` | `<url-or-name>` | 停止监控某个URL |
| `list` | `[-f json]` | 列出所有被监控的URL及其统计信息 |
| `check` | `[url-or-name] [-f json]` | 检查是否有变化（全部或单个URL） |
| `diff` | `<url-or-name>` | 显示最后一次记录的差异 |
| `snapshot` | `<url-or-name> [-l lines]` | 显示当前的快照 |

## 输出符号

- 🔔 页面内容已更改（显示差异预览）
- ✅ 无变化
- 📸 生成了初始快照
- ❌ 获取数据时出错

## 数据存储位置

数据存储在`~/.web-monitor/`目录下（可通过`WEB_monitor_DIR`环境变量进行覆盖）：
- `watches.json` — 监控列表配置文件
- `snapshots/` — 存储的网页内容及差异文件

## 提示

- 使用`--selector`来监控特定元素（如价格、文章列表等）
- 使用`--format json`进行程序化检查（例如集成心跳检测功能）
- CSS选择器的使用需要`beautifulsoup4`库（通过`--with`标志进行配置）
- 文本会经过处理，以减少时间戳、空白字符和广告等不必要的信息对结果的影响