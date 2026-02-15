---
name: race-finder
description: 查找即将举行的比赛——包括跑步、越野跑、铁人三项、自行车、游泳和障碍赛等项目。可以通过地点、距离、运动类型和日期进行搜索。搜索结果会显示比赛详情以及注册链接。
---

# 赛事查找功能

该功能可搜索美国及全球范围内的即将举行的赛事信息，数据来源于RunSignUp——最大的耐力赛事注册平台。

## API

**基础URL:** `https://api.racefinder.net`

### 搜索赛事

```
GET /api/v1/races
```

所有参数均为可选。返回按日期排序的即将举行的赛事列表。

#### 查询参数

| 参数            | 类型     | 说明                                                         | 示例                |
|-----------------|---------|--------------------------------------------------|-------------------|
| `q`            | 字符串    | 按赛事名称搜索                                      | `q=Austin Marathon`     |
| `city`          | 字符串    | 城市名称                                        | `city=Austin`         |
| `state`          | 字符串    | 美国州代码                                        | `state=TX`           |
| `country`         | 字符串    | 两位字母的国家代码（默认：US）                               | `country=CA`           |
| `sport`          | 字符串    | 运动类型（详见下文）                                   | `sport=running`       |
| `distance`       | 字符串    | 赛事距离类别                                      | `distance=marathon`     |
| `start_date`      | 字符串    | 该日期或之后举行的赛事（格式：YYYY-MM-DD，默认：今天）       | `start_date=2026-06-01`     |
| `end_date`      | 字符串    | 该日期或之前举行的赛事（格式：YYYY-MM-DD）                       | `end_date=2026-12-31`     |
| `zipcode`       | 字符串    | 美国邮政编码（需配合`radius`参数使用）                         | `zipcode=78701`        |
| `radius`        | 字符串    | 以邮政编码为中心的搜索半径（单位：英里）                         | `radius=25`           |
| `page`          | 整数     | 当前页面编号（默认：1）                                    | `page=2`            |
| `per_page`       | 整数     | 每页显示的结果数量（默认：20，最大：50）                         | `per_page=10`          |

#### 运动类型选项

| 选项            | 说明                          |                          |
|-----------------|-----------------------------|-------------------------|
| `running`       | 跑步赛事                        |                          |
| `trail`         | 徒步跑及超长距离跑赛事                   |                          |
| `triathlon`      | 铁人三项及双项赛事                   |                          |
| `cycling`       | 自行车赛事                       |                          |
| `swimming`      | 游泳赛事                        |                          |
| `obstacle`     | 障碍赛及泥地跑赛事                   |                          |

#### 赛事距离选项

| 距离            | 范围                         |                          |
|-----------------|-----------------------------|-------------------------|
| `5k`            | 约2–4英里                        |                          |
| `10k`           | 约5–8英里                        |                          |
| `half-marathon`    | 约12–15英里                        |                          |
| `marathon`       | 约25–28英里                        |                          |
| `ultra`          | 30英里以上                        |                          |

#### 响应格式

```json
{
  "races": [
    {
      "id": "12345",
      "name": "Austin Marathon",
      "date": "2026-03-15",
      "start_time": "7:00 AM",
      "sport": "running",
      "city": "Austin",
      "region": "Texas",
      "country": "US",
      "distances": [
        {"name": "Marathon", "miles": 26.2, "km": 42.2, "category": "marathon"},
        {"name": "Half Marathon", "miles": 13.1, "km": 21.1, "category": "half-marathon"}
      ],
      "prices": [
        {"name": "Marathon — $120", "price": 120, "currency": "USD", "available": true}
      ],
      "image_url": "https://...",
      "details_url": "https://racefinder.net/race/12345",
      "register_url": "https://runsignup.com/Race/12345?rsu_aff=..."
    }
  ],
  "page": 1,
  "total_results": 20
}
```

**无需身份验证。**

## 使用示例

### 在某城市查找赛事

```bash
curl "https://api.racefinder.net/api/v1/races?city=Austin&state=TX"
```

### 在指定邮政编码附近查找马拉松赛事

```bash
curl "https://api.racefinder.net/api/v1/races?zipcode=78701&radius=50&distance=marathon"
```

### 查找今年夏天在科罗拉多州举行的徒步跑赛事

```bash
curl "https://api.racefinder.net/api/v1/races?state=CO&sport=trail&start_date=2026-06-01&end_date=2026-08-31"
```

### 按赛事名称搜索

```bash
curl "https://api.racefinder.net/api/v1/races?q=Ironman"
```

### 查找加利福尼亚州的5公里跑步赛事

```bash
curl "https://api.racefinder.net/api/v1/races?state=CA&sport=running&distance=5k"
```

## 代理使用提示：

- 当用户想了解赛事详情时，可使用`details_url`（该链接会指向racefinder.net上的赛事页面）。
- 当用户准备报名时，可使用`register_url`（该链接直接跳转到报名页面）。
- 默认搜索结果为从今天开始的赛事，按日期排序显示。
- 仅限美国地区：结合使用`zipcode`和`radius`参数进行地理位置搜索。
- 结合使用`sport`和`distance`参数来缩小搜索范围（例如：`sport=running&distance=half-marathon`）。
- `total_results`字段显示当前页面显示的结果数量；使用`page`参数进行分页浏览。