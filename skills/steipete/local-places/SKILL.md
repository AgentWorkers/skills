---
name: local-places
description: 通过本地主机上的 Google Places API 代理来搜索地点（餐厅、咖啡馆等）。
homepage: https://github.com/Hyaxia/local_places
metadata: {"clawdbot":{"emoji":"📍","requires":{"bins":["uv"],"env":["GOOGLE_PLACES_API_KEY"]},"primaryEnv":"GOOGLE_PLACES_API_KEY"}}
---

# 📍 本地地点查询

*快速查找附近的地点*

使用本地的 Google Places API 代理来搜索附近的地点。操作流程分为两步：首先确定用户的位置，然后进行搜索。

## 设置

```bash
cd {baseDir}
echo "GOOGLE_PLACES_API_KEY=your-key" > .env
uv venv && uv pip install -e ".[dev]"
uv run --env-file .env uvicorn local_places.main:app --host 127.0.0.1 --port 8000
```

需要将 `GOOGLE_PLACES_API_KEY` 设置在 `.env` 文件或环境变量中。

## 快速入门

1. **检查服务器：** `curl http://127.0.0.1:8000/ping`

2. **确定用户位置：**
```bash
curl -X POST http://127.0.0.1:8000/locations/resolve \
  -H "Content-Type: application/json" \
  -d '{"location_text": "Soho, London", "limit": 5}'
```

3. **搜索地点：**
```bash
curl -X POST http://127.0.0.1:8000/places/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "coffee shop",
    "location_bias": {"lat": 51.5137, "lng": -0.1366, "radius_m": 1000},
    "filters": {"open_now": true, "min_rating": 4.0},
    "limit": 10
  }'
```

4. **获取地点详情：**
```bash
curl http://127.0.0.1:8000/places/{place_id}
```

## 对话流程

1. 如果用户输入“附近”或提供模糊的位置信息 → 先确定用户的具体位置。
2. 如果搜索结果有多个 → 显示编号列表，让用户选择所需地点。
3. 询问用户的偏好（如类型、是否需要立即打开、评分、价格等级）。
4. 根据用户选择的地点进行搜索。
5. 显示搜索结果，包括地点名称、评分、地址和开放状态。
6. 提供获取详细信息或进一步精炼搜索条件的选项。

## 过滤条件

- `filters.types`：必须选择一种类型（例如：“餐厅”、“咖啡馆”、“健身房”）。
- `filters.price_levels`：整数范围 0-4（0 表示免费，4 表示非常昂贵）。
- `filters.min_rating`：评分范围 0-5，以 0.5 为间隔。
- `filters.open_now`：布尔值，表示是否需要立即打开地点。
- `limit`：搜索结果数量为 1-20 个；定位结果数量为 1-10 个。
- `location_bias.radius_m`：必须大于 0（表示搜索半径）。

## 响应格式

```json
{
  "results": [
    {
      "place_id": "ChIJ...",
      "name": "Coffee Shop",
      "address": "123 Main St",
      "location": {"lat": 51.5, "lng": -0.1},
      "rating": 4.6,
      "price_level": 2,
      "types": ["cafe", "food"],
      "open_now": true
    }
  ],
  "next_page_token": "..." 
}
```

在后续请求中，使用 `next_page_token` 作为分页参数来获取更多结果。