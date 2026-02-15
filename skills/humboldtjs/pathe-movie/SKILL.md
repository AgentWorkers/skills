---
name: pathe-movie
description: 通过 Pathé 的 JSON API 查找 Pathé Netherlands 的电影、海报、剧情描述、影院信息以及放映时间。当用户提到某部 Pathé 电影或节目、请求获取海报、询问剧情描述或评分，或者查询特定影院的放映时间时，系统应自动触发相应的操作。
---

# Pathé 电影查询技能

## 概述
- 在与 `https://www.pathe.nl/api` 进行通信时，务必使用正确的浏览器请求头（详见 `scripts/pathe_movie.py`）。
- 请使用 `config/pathe_movie_config.json` 中的配置来确定默认查询的影院，除非用户指定了其他影院。
- 所有可重用的辅助功能（如查询数据清洗、模糊匹配、最佳匹配结果选择以及后续请求的发起）都依赖于 `scripts/pathe_movie.py`。
- 在不确定如何操作时，请参考 `references/api.md` 以获取数据格式、字段名称和预期响应结构的信息。

## 搜索流程
1. 去除用户输入的电影名称中的填充词（如 `the`、`a`、`an`、`of`、`in`、`on`、`for`、`and` 等）。
2. 使用清洗后的查询参数调用 `/api/search/full?q=...`。
3. 如果返回多个结果，通过 `difflib` 进行模糊匹配以选择最匹配的电影名称。保留 `slug`、`poster`（使用 `poster.lg`）和 `contentRating` 字段以供后续请求使用。
4. 如果需要获取海报图片，请返回 `poster.lg` 的 URL；必要时可回退到 `poster.md` 或 `posterPath`。

## 电影详情流程
- 给定一个电影 slug，调用 `/api/show/{slug}?language=nl`。
- 获取 `contentRating.description` 和 `synopsis`（部分数据可能为空，需妥善处理），以及相关的额外信息（如 `genres`、`directors`、`actors` 和 `trailers`）。
- 海报图片的路径现在存储在 `posterPath` 中，只有在无法从搜索结果中获取海报时才会使用搜索结果中的 `poster` 字段。

## 电影院信息流程
- 调用 `/api/show/{slug}/cinemas?language=nl`。根据配置中的 `approvedCinemas` 过滤返回的电影院列表；除非用户另有要求。
- 对于需要详细信息的每家电影院，调用 `/api/cinema/{cinema}?language=nl` 来获取其官方名称、所在城市名称（`citySlug`）以及相关服务信息（`services`/`alerts`）。

## 上映时间查询
- 使用 `/api/show/{slug}/showtimes/{cinema}?language=en` 来获取上映时间信息。响应结果是一个按日期（`YYYY-MM-DD`）排序的字典，每个日期对应多个放映时间；每个放映时间条目至少包含 `time` 字符串（以及可选的 `screen`、`language`、`format` 等字段）。
- 如果返回的空数组表示当前没有安排放映，应返回相应的提示信息。

## 测试说明
- 执行 `/api/search/full?q=matrix` 以确认响应数据中包含 `slug`、`title`、`poster`、`contentRating` 和 `genres` 字段。
- 调用 `/api/show/the-matrix-41119` 以验证 `contentRating.description`、`synopsis` 和 `posterPath` 字段；注意 `synopsis` 可能为空，`posterPath` 也可能缺失，因此需要对其进行空值检查。
- 查询 `/api/cinema/pathe-zaandam` 以获取影院的名称、所在城市名称和服务信息（该影院没有放映时间信息，因此返回的数据主要为静态信息）。
- 调用 `/api/show/iron-lung-51335/showtimes/pathe-zaandam` 以确认该电影的上映时间列表；如果列表为空，需正确处理这种情况。
- 调用 `/api/shows?language=nl` 以了解数据结构：响应中包含多个电影条目，每个条目包含 `slug`、`posterPath`、`contentRating` 和 `next24ShowtimesCount`。

## 媒体文件传输说明
- 在通过 WhatsApp 发送海报图片之前，务必先将它们下载到本地（例如保存到 `/tmp` 目录）。这样 gateway 才能正确读取文件。
- 当用户通过 WhatsApp 明确请求海报图片时，需要在消息中的 `media` 字段提供本地文件的路径（例如 `/tmp/bluey_poster.jpg`）。WhatsApp 的文档说明指出，出站媒体文件可以接受本地路径，这样可以确保实际发送的是图片文件而非 URL。
- 在消息中提供的文本描述应简洁明了（例如：“这是您请求的 Bluey 海报图片”），并确保使用下载后的图片文件进行展示。

请始终按照这些说明操作，以确保用户查询电影信息、查看海报、获取电影描述、查询电影院信息或上映时间时，该技能能够准确返回 Pathé Netherlands 的相关结果。