---
name: grounding-lite
description: **Google Maps Grounding Lite MCP**：通过 `mcporter` 实现位置搜索、天气查询及路线规划的功能。
homepage: https://developers.google.com/maps/ai/grounding-lite
metadata: {"clawdbot":{"emoji":"🗺️","requires":{"bins":["mcporter"],"env":["GOOGLE_MAPS_API_KEY"]},"primaryEnv":"GOOGLE_MAPS_API_KEY","install":[{"id":"node","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter (npm)"}]}}
---

# Grounding Lite

Google Maps Grounding Lite MCP 提供基于 AI 的地理位置数据。目前仍处于测试阶段（预发布版本），在预览期间可免费使用。

## 设置

1. 启用相关 API：`gcloud beta services enable mapstools.googleapis.com`
2. 从 [Cloud Console](https://console.cloud.google.com/apis/credentials) 获取 API 密钥。
3. 设置环境变量：`export GOOGLE_MAPS_API_KEY="YOUR_KEY"`
4. 配置 mcporter：
   ```bash
   mcporter config add grounding-lite \
     --url https://mapstools.googleapis.com/mcp \
     --header "X-Goog-Api-Key=$GOOGLE_MAPS_API_KEY" \
     --system
   ```

## 工具

- **search_places**：用于查找地点、企业和地址。返回包含 Google Maps 链接的 AI 摘要信息。
- **lookup_weather**：提供当前天气状况及未来 48 小时/7 天的天气预报。
- **compute_routes**：计算旅行距离和所需时间（不提供实时导航路线）。

## 命令

```bash
# Search places
mcporter call grounding-lite.search_places textQuery="pizza near Times Square NYC"

# Weather
mcporter call grounding-lite.lookup_weather location='{"address":"San Francisco, CA"}' unitsSystem=IMPERIAL

# Routes
mcporter call grounding-lite.compute_routes origin='{"address":"SF"}' destination='{"address":"LA"}' travelMode=DRIVE

# List tools
mcporter list grounding-lite --schema
```

## 参数

**search_places**：`textQuery`（必填），`locationBias`，`languageCode`，`regionCode`

**lookup_weather**：`location`（必填：地址/经纬度/地点 ID），`unitsSystem`，`date`，`hour`

**compute_routes**：`origin`（起点），`destination`（终点），`travelMode`（驾驶/步行）

## 注意事项

- 使用限制：
  - `search_places`：每分钟 100 次请求（每天最多 1000 次）。
  - `lookup_weather`：每分钟 300 次请求。
  - `compute_routes`：每分钟 300 次请求。
- 用户界面输出中必须包含 Google Maps 的链接，并注明数据来源。
- 仅适用于未使用用户数据训练的模型。