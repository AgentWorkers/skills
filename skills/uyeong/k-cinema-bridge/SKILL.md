---
name: k-cinema-bridge
description: 查询韩国多厅影院（Lotte Cinema、CGV、Megabox）的票房排名以及包含KOBIS详细信息的即将上映电影数据。当用户询问当前正在放映的韩国电影、票房排名、即将上映的电影，或希望根据类型、导演、演员或评分获得电影推荐时，可以使用该功能。
homepage: https://uyeong.github.io/k-cinema-bridge/
allowed-tools: WebFetch
---

# k-cinema-bridge

这是一个提供韩国多厅影院（Lotte Cinema、CGV、Megabox）票房信息以及即将上映电影数据的JSON API，其中包含来自KOBIS（韩国电影委员会）的详细信息，如电影类型、导演和演员阵容。数据每天在UTC时间00:00自动更新。

## API参考

- 基本URL：`https://uyeong.github.io/k-cinema-bridge`
- 所有端点均支持通过`GET`请求访问，无需身份验证。
- `info`字段可能为`null`，因此在访问前请务必进行`null`检查。

| 端点 | 描述 |
|---|---|
| GET /api/boxoffice.json | 来自所有渠道的综合票房数据（`{lotte, cgv, megabox}`） |
| GET /api/boxoffice/{source}.json | 按来源划分的票房数据（`BoxOfficeMovie[]`） |
| GET /api/upcoming.json | 来自所有渠道的即将上映电影数据（`{lotte, cgv, megabox}`） |
| GET /api/upcoming/{source}.json | 按来源划分的即将上映电影列表（`UpcomingMovie[]`） |

有效的来源值：`lotte`、`cgv`、`megabox`

## 数据模型

### BoxOfficeMovie

```
source: "lotte" | "cgv" | "megabox"
rank: number          -- Box office rank (starting from 1)
title: string         -- Movie title
rating: string        -- Audience rating
posterUrl: string     -- Poster image URL
info?: MovieInfo      -- KOBIS detailed info (may be null)
```

### UpcomingMovie

```
source: "lotte" | "cgv" | "megabox"
title: string         -- Movie title
rating: string        -- Audience rating
posterUrl: string     -- Poster image URL
releaseDate: string   -- Release date (YYYY-MM-DD, may be an empty string)
info?: MovieInfo      -- KOBIS detailed info (may be null)
```

### MovieInfo

```
code, title, englishTitle, originalTitle: string
runtime: string (minutes)
productionYear, openDate (YYYYMMDD), productionStatus, type: string
nations: string[]     -- Production countries
genres: string[]
directors: {name, englishName}[]
actors: {name, englishName, role, roleEnglish}[]
showTypes: {group, name}[]
companies: {code, name, englishName, part}[]
audits: {number, grade}[]
staff: {name, englishName, role}[]
```

## 使用说明

### 推荐热门电影

当用户请求电影推荐或询问热门电影时：

1. 调用`GET {BASE_URL}/api/boxoffice.json`以获取来自所有渠道的综合票房数据。
2. 识别在多个渠道中出现且排名较低的电影（排名越低，人气越高）。
3. 显示排名靠前的电影，包括其标题、评分以及`info.genres`中提供的电影类型（如有的话）。

### 公布即将上映的电影

当用户询问即将上映的电影时：

1. 调用`GET {BASE_URL}/api/upcoming.json`以获取即将上映的电影数据。
2. 根据`releaseDate`（YYYY-MM-DD）筛选结果，以匹配用户请求的时间范围。
3. 提供电影类型、导演和演员等详细信息（如`info`字段中有这些信息的话）。

### 按类型、导演或演员搜索电影

当用户询问特定类型的电影、导演或演员时：

1. 分别调用`GET {BASE_URL}/api/boxoffice.json`和`GET {BASE_URL}/api/upcoming.json`。
2. 使用`info`字段进行筛选：
    - 类型：与`info.genres`匹配
    - 导演：与`info.directors[].name`匹配
    - 演员：与`info.actors[].name`匹配
3. 在访问嵌套属性之前，请务必进行`null`检查。

### 按观众评分筛选电影

当用户询问适合特定年龄段的电影时：

1. 使用`rating`字段进行筛选。该字段始终存在，无需依赖`info`字段。
2. 已知的评分值包括：“전체 관람가”（适合所有年龄段）、“12세 관람가”（12岁以上）、“15세 관람가”（15岁以上）、“청소년 관람불가”（仅限成人）。

### 查询特定影院的信息

当用户询问特定影院的信息时：

1. 调用`GET {BASE_URL}/api/boxoffice/{source}.json`或`GET {BASE_URL}/api/upcoming/{source}.json`。
2. 有效的来源值：`lotte`、`cgv`、`megabox`。

### 比较不同影院的排名

当用户希望比较不同影院的排名时：

1. 调用`GET {BASE_URL}/api/boxoffice.json`以获取综合数据。
2. 找出在多个渠道中标题相同的电影，并比较它们的排名。

## 响应指南

- 以用户使用的语言进行响应。
- 在展示电影列表时，包括标题、排名、上映日期、评分以及电影类型（如果有的话）。
- 如果电影的`info`字段为`null`，仅显示基本字段（标题、排名、评分、海报链接），不要猜测缺失的详细信息。
- 在比较不同影院的排名时，使用表格格式以便于清晰展示结果。