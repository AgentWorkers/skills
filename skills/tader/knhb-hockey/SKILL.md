---
name: knhb-hockey
description: 查询荷兰曲棍球比赛的日程和结果，数据来源为 KNHB Match Center (hockeyweerelt.nl)。该平台可用于查找荷兰的曲棍球俱乐部、球队、即将举行的比赛以及比赛结果。
---

# KNHB曲棍球比赛中心

通过荷兰曲棍球联合会（KNHB）的比赛中心API查询俱乐部、球队和比赛信息。

## API基础URL

```
https://publicaties.hockeyweerelt.nl/mc
```

## API端点

### 列出所有俱乐部
```bash
curl -s "https://publicaties.hockeyweerelt.nl/mc/clubs" | jq '.data[]'
```

响应包含：`id`, `name`, `abbreviation`, `city`, `district.name`, `logo`, `hockey_types[]`

### 按名称或城市搜索俱乐部
```bash
curl -s "https://publicaties.hockeyweerelt.nl/mc/clubs" | jq '.data[] | select(.name | test("Westland"; "i"))'
curl -s "https://publicaties.hockeyweerelt.nl/mc/clubs" | jq '.data[] | select(.city | test("Delft"; "i"))'
```

### 查看某个俱乐部的球队信息
```bash
curl -s "https://publicaties.hockeyweerelt.nl/mc/clubs/{clubId}/teams" | jq '.data[]'
```

响应包含：`id`, `name`, `short_name`, `type` (Veld/Zaal), `category_group`, `category_name`, `next_match_date`

### 获取某支球队的即将进行的比赛
```bash
curl -s "https://publicaties.hockeyweerelt.nl/mc/teams/{teamId}/matches/upcoming" | jq '.data[]'
```

### 获取某支球队的正式比赛记录（已进行的比赛）
```bash
curl -s "https://publicaties.hockeyweerelt.nl/mc/teams/{teamId}/matches/official" | jq '.data[]'
```

比赛响应包含：
- `datetime` — ISO 8601格式（UTC）
- `location.city`, `location.street`, `location.description`
- `home_team.name`, `home_team.club_name`
- `away_team.name`, `away_team.club_name`
- `home_score`, `away_score` — 对于即将进行的比赛，此字段可能为`null`
- `competition`, `poule`, `status`, `field`

## 常见查询

### 查找某个俱乐部并列出其所有球队
```bash
# Find club ID
CLUB_ID=$(curl -s "https://publicaties.hockeyweerelt.nl/mc/clubs" | jq -r '.data[] | select(.name | test("Westland"; "i")) | .id' | head -1)

# List teams
curl -s "https://publicaties.hockeyweerelt.nl/mc/clubs/${CLUB_ID}/teams" | jq -r '.data[] | "\(.id) \(.name) (\(.type)) - next: \(.next_match_date)"'
```

### 获取某支球队的下一场比赛信息
```bash
curl -s "https://publicaties.hockeyweerelt.nl/mc/teams/{teamId}/matches/upcoming" | jq '.data[0] | {
  date: .datetime,
  home: .home_team.name,
  away: .away_team.name,
  location: .location.city,
  field: .field
}'
```

### 以美观的方式格式化比赛日程
```bash
curl -s "https://publicaties.hockeyweerelt.nl/mc/teams/{teamId}/matches/upcoming" | jq -r '.data[] | "\(.datetime | split("T")[0]) \(.datetime | split("T")[1] | split(".")[0] | .[0:5]) - \(.home_team.name) vs \(.away_team.name) @ \(.location.city)"'
```

## 球队类别

- **Senioren**：成年球队（H1, D1等）
- **Junioren**：U18-U21年龄段
- **Jongste Jeugd**：青少年球队（前缀为MO/JO）
  - MO = 女子青少年队（Meisjes Onder）
  - JO = 男子青少年队（Jongens Onder）
  - 例如：MO11 = 女子11岁以下球队

## 注意事项

- **日期时间采用UTC格式** — 阿姆斯特丹冬季时间为CET（UTC+1），夏季时间为CEST（UTC+2）
- 使用`date`命令或适当的日期库进行转换，以获取正确的星期几
- `type: "Veld"` 表示室外曲棍球，`type: "Zaal"` 表示室内曲棍球
- **不同类型的球队拥有不同的ID** — 请同时查询室外和室内球队的信息以获取完整的比赛日程
- 室外赛季：约9月-6月，室内赛季：约11月-3月