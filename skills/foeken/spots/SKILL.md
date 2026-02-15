---
name: spots
description: 使用基于网格的扫描方法进行全面的 Google Places 搜索。可以找到所有地点，而不仅仅是 Google 显示出来的那些地点。
metadata:
  clawdbot:
    emoji: 📍
    private: true
---

# spots

**发现谷歌未公开的隐藏宝藏。**

二进制文件路径：`~/projects/spots/spots` 或 `go install github.com/foeken/spots@latest`

## 使用方法

```bash
# Search by location name
spots "Arnhem Centrum" -r 800 -q "breakfast,brunch" --min-rating 4

# Search by coordinates (share location from Telegram)
spots -c 51.9817,5.9093 -r 500 -q "coffee"

# Get reviews for a place
spots reviews "Koffiebar FRENKIE"

# Export to map
spots "Amsterdam De Pijp" -r 600 -o map --out breakfast.html

# Setup help
spots setup
```

## 参数选项

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `-c, --coords` | 直接输入经纬度坐标 | - |
| `-r, --radius` | 搜索半径（米） | 500 |
| `-q, --query` | 搜索关键词 | breakfast,brunch,ontbijt,café,bakkerij |
| `--min-rating` | 最低评分（1-5分） | - |
| `--min-reviews` | 最少评论数 | - |
| `--open-now` | 仅显示当前营业中的店铺 | false |
| `-o, --output` | 输出格式（json/csv/map） | json |

## 设置要求

需要启用 Google 的 Places API 和 Geocoding API，并获取相应的 API 密钥。

```bash
spots setup  # full instructions
export GOOGLE_PLACES_API_KEY="..."
```

API 密钥存储在 1Password 中的路径：`op://Echo/Google API Key/credential`

## 项目来源

https://github.com/foeken/spots