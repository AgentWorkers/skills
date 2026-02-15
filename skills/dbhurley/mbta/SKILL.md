---
name: mbta
description: 实时MBTA交通预测服务，涵盖波士顿地区的地铁、公交、通勤铁路和渡轮。您可以查询出发时间、搜索站点/路线、查看服务公告，并使用实时仪表板获取相关信息。该服务适用于需要了解波士顿交通状况、列车时刻表、出行建议或MBTA服务状态的场景。
metadata: {"clawdbot":{"requires":{"bins":["python3"],"pip":["requests"]}}}
---

# MBTA 交通服务

通过 v3 API 查询 MBTA 的实时列车信息。

## 设置

```bash
# Optional but recommended for higher rate limits
export MBTA_API_KEY=your_key_here  # Free at https://api-v3.mbta.com/portal

# Install dependencies
pip install requests pyyaml flask  # flask only needed for dashboard
```

## 快速命令

```bash
cd skills/mbta

# Next departures from a stop
python scripts/mbta.py next --stop place-alfcl  # Alewife
python scripts/mbta.py next --stop place-harsq --route Red  # Harvard, Red Line only

# Search for stop IDs
python scripts/mbta.py stops --search "Porter"
python scripts/mbta.py stops --search "Kendall"

# List routes
python scripts/mbta.py routes              # All routes
python scripts/mbta.py routes --type rail  # Subway only
python scripts/mbta.py routes --type bus   # Buses

# Service alerts
python scripts/mbta.py alerts              # All alerts
python scripts/mbta.py alerts --route Red  # Red Line alerts

# All configured departures (uses config.yaml)
python scripts/mbta.py departures --config config.yaml

# Start web dashboard
python scripts/mbta.py dashboard --config config.yaml --port 6639
```

## 配置

编辑 `config.yaml` 文件以设置您的目的地站点：

```yaml
panels:
  - title: "My Station"
    walk_minutes: 5  # Filter out trains you can't catch
    services:
      - label: "Red Line"
        destination: "to Alewife"
        route_id: "Red"
        stop_id: "place-harsq"
        direction_id: 0  # 0 or 1 for direction
        limit: 3
```

关键字段：
- `walk_minutes`：过滤掉出发时间早于此时间的列车
- `direction_id`：0 = 出站/北向；1 = 进站/南向（具体线路可能有所不同）
- `headsign_contains`：可选过滤器（例如，输入 “Ashmont” 可以排除 Braintree 站点）

## 查找站点/路线 ID

```bash
# Search stops
python scripts/mbta.py stops --search "Davis"
# Returns: place-davis: Davis

# Get routes
python scripts/mbta.py routes --type rail
# Returns route IDs like "Red", "Orange", "Green-E"
```

## JSON 输出

添加 `--json` 选项以获取机器可读的输出格式：

```bash
python scripts/mbta.py next --stop place-alfcl --json
python scripts/mbta.py departures --config config.yaml --json
```

## 常见站点 ID

| 站点 | 站点 ID |
|---------|---------|
| Alewife | place-alfcl |
| Harvard | place-harsq |
| Kendall/MIT | place-knncl |
| Park Street | place-pktrm |
| South Station | place-sstat |
| North Station | place-north |
| Back Bay | place-bbsta |
| Downtown Crossing | place-dwnxg |

## 回答用户问题

**“下一班红线列车什么时候到？”**
```bash
python scripts/mbta.py next --stop place-alfcl --route Red
```

**“我现在出发能赶上地铁吗？”**
根据出发时间与步行所需时间进行判断：如果下一班列车的到达时间在 `walk_minutes` 之内，建议 “现在就出发！”

**“橙线列车有延误吗？”**
```bash
python scripts/mbta.py alerts --route Orange
```

**“有哪些公交车可以到达 Harvard？”**
```bash
python scripts/mbta.py stops --search "Harvard"
# Then check routes at that stop
python scripts/mbta.py next --stop <stop_id>
```