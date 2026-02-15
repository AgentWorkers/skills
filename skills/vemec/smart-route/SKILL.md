---
name: smart-route
description: 使用 Google Routes API 计算考虑交通状况的路线、行驶时间以及地点之间的距离。当用户询问“X 地点的交通情况”、“到 Y 地点需要多长时间”、“去 Z 地点的最佳路线”或“驾驶时间”时，可以使用该 API。返回的 JSON 数据包含行驶时间、距离以及一个直接的 Google Maps 导航链接。
metadata:
  openclaw:
    emoji: 🚦
    requires:
      bins:
        - node
      env:
        - GOOGLE_ROUTES_API_KEY
---

# Google 路线查询工具

通过 Google 路线 API（v2）获取实时交通信息和路线信息。

## 使用场景

当用户提出以下问题时，可立即使用此功能：
- “去 X 地点的交通情况如何？”
- “开车到 Y 地点需要多长时间？”
- “请给我提供从 A 到 Z 的路线。”
- “A 和 B 之间的距离是多少？”

## 使用方法

此功能通过执行一个 Node.js 脚本来实现。需要一个已启用 “Routes API” 功能的 API 密钥。

### 命令

```bash
node skills/smart-route/scripts/get_route.js --origin "Origin Address" --destination "Destination Address" [--mode DRIVE|BICYCLE|WALK]
```

### 输出格式

脚本返回一个 JSON 对象：

```json
{
  "origin": "Union Square, San Francisco, CA",
  "destination": "Golden Gate Bridge, San Francisco, CA",
  "mode": "DRIVE",
  "duration": "30 min",
  "distance": "13.5 km",
  "traffic_duration_seconds": 1835,
  "route_link": "https://www.google.com/maps/dir/?api=1&origin=...&destination=...&travelmode=driving"
}
```

### 示例

- **查询旧金山的交通情况：**
  `node skills/smart-route/scripts/get_route.js --origin "Union Square, San Francisco, CA" --destination "Golden Gate Bridge, San Francisco, CA"`

- **查询洛杉矶的驾驶时间：**
  `node skills/smart-route/scripts/get_route.js --origin "Los Angeles, CA" --destination "Santa Monica, CA" --mode DRIVE`

## 配置

### 隐私与安全

- **通信范围**：此功能仅与 `routes.googleapis.com` 通信。
- **数据处理的注意事项**：
  - 除了下面指定的变量外，不会读取本地文件或其他环境变量。
  - **个人身份信息（PII）处理**：用户提供的起点和终点地址会被发送到 Google 路线 API，并以 JSON 格式显示在输出中。用户应将这些地址视为可能包含敏感信息（PII）的数据。
- **凭证要求**：必须通过环境变量提供 API 密钥。出于安全考虑，禁止通过命令行参数（CLI）传递密钥（以避免在进程列表中泄露敏感信息）。

### API 凭证

此功能需要一个已启用 “Routes API” 功能的 **Google Cloud API 密钥**。

- **相关变量**：`GOOGLE_ROUTES_API_KEY`
  - 该脚本会在运行时检查此环境变量的存在性。
- **严格模式**：如果该变量缺失，脚本将立即退出并显示错误，而不会尝试使用其他密钥，从而确保不会误用错误的凭证。

### 设置说明

1. 打开 [Google Cloud 控制台](https://console.cloud.google.com/)。
2. 为您的项目启用 “Routes API” 功能。
3. 在 “凭证” 设置中生成 API 密钥。
4. 将密钥导出到您的环境中：
    ```bash
    export GOOGLE_ROUTES_API_KEY="your_api_key_here"
    ```