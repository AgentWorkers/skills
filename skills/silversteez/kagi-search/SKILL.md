---
name: kagi-search
description: 使用 Kagi Search API 进行网络搜索。当您需要从互联网上查找当前信息、事实或参考资料时，可以使用该 API。请确保在环境中设置了 `KAGI_API_KEY`。
---

> **注意：** Kagi Search API 目前仍处于测试阶段（beta）。如需申请 API 访问权限，请发送电子邮件至 support@kagi.com。您必须是 Kagi 的订阅用户才能使用该 API。

---

# Kagi Search CLI

使用 Kagi Search API 进行网页搜索，并提供清晰、易读的输出格式。

## 快速入门

```bash
export KAGI_API_KEY="your_api_key"
kagi-search "your search query"
# or run directly:
python3 scripts/kagi-search.py "your search query"
```

## 主要功能

- **清晰的输出**：每个搜索结果都包含标题、网址、内容片段和元数据
- **分页支持**：可以控制显示的结果数量和偏移量
- **JSON 模式**：提供原始 JSON 格式的数据，便于脚本编写
- **相关搜索**：显示相关查询结果（可选择性隐藏）
- **API 用量显示**：显示剩余的 API 使用量
- **快速且轻量级**：完全基于 Python 开发，无需依赖其他库

## 命令选项

| 选项 | 说明 |
|------|-------------|
| `query` | 搜索关键词（必填） |
| `-n, --limit` | 显示的结果数量（默认值：10） |
| `-s, --offset` | 分页的偏移量（默认值：0） |
| `--json` | 以原始 JSON 格式输出结果 |
| `--no-related` | 隐藏相关搜索结果 |
| `-h, --help` | 显示帮助信息 |

## 使用示例

```bash
# Basic search
kagi-search "python async await tutorial"

# Limit results
kagi-search "AI news" --limit 5

# Pagination
kagi-search "recipes" --offset 10 --limit 5

# JSON for scripting
kagi-search "github stars" --json | jq '.data[].url'

# Hide related searches
kagi-search "rust programming" --no-related
```

## 安装与配置

**环境要求：**
```bash
export KAGI_API_KEY="your_api_key"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

**配置 PATH 变量：**
```bash
# Make executable and add to PATH
chmod +x scripts/kagi-search.py
cp scripts/kagi-search.py ~/.local/bin/kagi-search
```

## 系统要求

- Python 3.7 及以上版本
- 需设置 `KAGI_API_KEY` 环境变量
- 确保设备能够访问互联网

## 输出格式

```
[Query: search terms]
[Results: 5]
[API Balance: $0.123]
[Time: 45ms]
----------------------------------------
=== Result Title ===
https://example.com
Snippet text here...
[2024-01-15]
---
Related: related query 1, related query 2
```