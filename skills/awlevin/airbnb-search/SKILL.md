---
name: airbnb-search
description: 搜索 Airbnb 的房源信息，包括价格、评分以及直接访问房源的链接。无需使用用户 API 密钥（直接使用 Airbnb 的公共前端 API 密钥）。适用于搜索 Airbnb 的住宿、度假租赁房源或查询房源价格。
license: MIT
metadata:
  author: Olafs-World
  version: "0.1.3"
---

# Airbnb 搜索

通过命令行搜索 Airbnb 的房源信息。返回价格、评分以及直接预订链接。

## 系统要求

- Python 3.8 及以上版本
- `requests` 库（通过 `uv run --with` 自动安装）

## 快速入门

```bash
# Run directly (no install needed)
uv run --with requests scripts/airbnb-search.py "Steamboat Springs, CO" --checkin 2025-03-01 --checkout 2025-03-03

# JSON output
uv run --with requests scripts/airbnb-search.py "Denver, CO" --checkin 2025-06-01 --checkout 2025-06-05 --json
```

## 可选参数

```
query                Search location (e.g., "Steamboat Springs, CO")
--checkin, -i DATE   Check-in date (YYYY-MM-DD)
--checkout, -o DATE  Check-out date (YYYY-MM-DD)
--min-price N        Minimum price filter
--max-price N        Maximum price filter
--min-bedrooms N     Minimum bedrooms filter
--limit N            Max results (default: 50)
--json               Output as JSON
--format FORMAT      table or json (default: table)
```

## 示例输出

```
📍 Steamboat Springs, CO
📊 Found 300+ total listings

==========================================================================================
Cozy Mountain Cabin 🏆
  2BR/1BA | ⭐4.92 | 127 reviews
  💰 $407 total
  🔗 https://airbnb.com/rooms/12345678
```

## 注意事项

- 为了获得准确的房价信息，必须提供日期
- 房价中包含清洁费用
- 无需用户 API 密钥——使用 Airbnb 的公共前端 API 密钥（硬编码，与 airbnb.com 网站上使用的密钥相同）
- 如果 Airbnb 更改其内部的 GraphQL API，该工具可能会失效
- 请遵守 API 的速率限制

## 链接

- [PyPI](https://pypi.org/project/airbnb-search/)
- [GitHub](https://github.com/Olafs-World/airbnb-search)