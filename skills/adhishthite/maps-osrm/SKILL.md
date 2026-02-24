---
name: maps
description: >
  **使用免费API（OSRM + Nominatim/OSM）进行距离计算、路线规划及地理编码**  
  当用户询问两地之间的距离、行驶时间、路线信息，或者需要将地名转换为坐标时，可以使用这些免费API。这些API无需API密钥即可使用。系统要求安装Python 3.6或更高版本。
metadata:
  openclaw:
    requires:
      bins: [python3]
---
# 地图服务

提供免费的距离计算/路线规划（使用OSRM）和地理编码（使用Nominatim/OSM）功能，无需使用API密钥。

## 地理编码（将地名转换为坐标）

```bash
bash scripts/geocode.sh "Times Square, New York"
```

该功能可将地名转换为对应的经纬度坐标，并返回显示名称。当用户提供地名而非坐标时，应优先使用此功能。

## 距离与路线计算

```bash
bash scripts/distance.sh <origin_lat>,<origin_lon> <dest_lat>,<dest_lon> [mode]
```

支持以下出行方式：`driving`（默认）、`foot`、`bicycle`。

示例：
```bash
# Manhattan to JFK Airport
bash scripts/distance.sh 40.7580,-73.9855 40.6413,-73.7781 driving

# Golden Gate Park to Fisherman's Wharf (walking)
bash scripts/distance.sh 37.7694,-122.4862 37.8080,-122.4177 foot
```

## 工作流程：

1. 如果用户提供地名，先使用`geocode.sh`进行地理编码；
2. 将获取到的经纬度坐标传递给`distance.sh`进行距离计算；
3. 结果以公里（km）和分钟（minutes）为单位显示。

## 限制说明：

- **OSRM**：提供免费的公共演示服务，没有硬性请求限制，但请合理使用资源；
- **Nominatim**：每秒最多允许1次请求（遵循OSM的使用政策），请求时需包含`User-Agent`字段；
- 该服务不提供实时交通数据，路线规划结果基于道路类型和行驶速度估算得出；
- 路线规划仅针对公路网络，不包含公共交通信息。