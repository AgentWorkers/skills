---
name: ipinfo
description: 使用 ipinfo.io API 进行 IP 地理定位查询。将 IP 地址转换为包括城市、地区、国家、邮政编码、时区和坐标在内的地理数据。该功能适用于 IP 地理定位、IP 数据丰富化或地理分布分析等场景。
homepage: https://ipinfo.io
metadata:
  { "openclaw": { "emoji": "🌍", "requires": { "bins": ["curl"] }, "primaryEnv": "IPINFO_TOKEN" } }
---

# IPinfo 地理定位服务

这是一个免费的 IP 地理定位 API。基本使用无需 API 密钥（每月 50,000 次请求）；如需更高的请求限制，可以使用可选的令牌。

## 配置

`IPINFO_TOKEN` 环境变量是 **可选的**——即使不设置该变量，该服务也能使用免费 tier 进行基本操作。您可以通过 OpenClaw 仪表板 UI 或手动设置该变量来配置更高的请求限制：

- **仪表板 UI**：在 OpenClaw 仪表板中配置 `IPINFO_TOKEN`（可选）
- **环境变量**：`export IPINFO_TOKEN="your-token"`
- **查询参数**：`?token=YOUR_TOKEN`（用于一次性请求）

## 快速查询

- 单个 IP 地址的查询：
  ```bash
curl -s "https://ipinfo.io/8.8.8.8"
```

- 当前设备的 IP 地址：
  ```bash
curl -s "https://ipinfo.io/json"
```

- 使用环境变量中的令牌进行查询（可选）：
  ```bash
curl -s "https://ipinfo.io/8.8.8.8?token=${IPINFO_TOKEN}"
```

- 或者直接传递令牌：
  ```bash
curl -s "https://ipinfo.io/8.8.8.8?token=YOUR_TOKEN"
```

## 响应格式

JSON 响应包含以下信息：

- `ip`：IP 地址
- `hostname`：反向 DNS 解析得到的主机名
- `city`：城市名称
- `region`：所在州/地区
- `country`：ISO 3166-1 标准的两字母国家代码
- `postal`：邮政编码
- `timezone`：IANA 定义的时区
- `loc`：坐标（格式为“纬度, 经度”）
- `org`：组织/ASN（自治系统编号）相关信息

## 提取特定字段

- 使用 `jq` 工具提取数据：
  ```bash
curl -s "https://ipinfo.io/8.8.8.8" | jq -r '.city, .country, .loc'
```

- 仅提取国家信息：
  ```bash
curl -s "https://ipinfo.io/8.8.8.8" | jq -r '.country'
```

- 解析坐标数据：
  ```bash
curl -s "https://ipinfo.io/8.8.8.8" | jq -r '.loc' | tr ',' '\n'
```

## 批量处理

- 同时处理多个 IP 地址：
  ```bash
for ip in 8.8.8.8 1.1.1.1 208.67.222.222; do
  if [ -n "$IPINFO_TOKEN" ]; then
    echo "$ip: $(curl -s "https://ipinfo.io/$ip?token=$IPINFO_TOKEN" | jq -r '.city, .country' | tr '\n' ', ')"
  else
    echo "$ip: $(curl -s "https://ipinfo.io/$ip" | jq -r '.city, .country' | tr '\n' ', ')"
  fi
done
```

## Python 使用方法

- 使用环境变量中的令牌：
  ```python
import os
import requests

# Without token (free tier)
response = requests.get("https://ipinfo.io/8.8.8.8")
data = response.json()
print(f"{data['city']}, {data['country']}")
print(f"Coordinates: {data['loc']}")
```

- 或者直接传递令牌：
  ```python
response = requests.get("https://ipinfo.io/8.8.8.8", params={"token": "YOUR_TOKEN"})
```

## 请求限制

- 免费 tier：每月 50,000 次请求，约 1 次请求/秒
- 使用令牌后，请求限制会根据所选套餐而增加
- 通过 OpenClaw 仪表板 UI 或环境变量配置 `IPINFO_TOKEN`

## 常见用途

- 对 IP 地址进行地理定位
- 为 IP 列表添加位置信息
- 按国家筛选 IP 地址
- 根据坐标计算 IP 之间的距离
- 获取 IP 地址的时区信息