---
name: lyrics-search
description: 使用 LrcApi 公共 API 按歌曲标题和艺术家名称搜索歌词。当用户请求查找、显示或打印某首歌曲的歌词时，可以使用此功能。
---
# 歌词搜索

通过 LrcApi 公共 API (`api.lrc.cx`) 搜索歌词。

## API

```
GET https://api.lrc.cx/lyrics?title={title}&artist={artist}
```

- 以 `text/plain` 格式返回包含时间戳的 LRC 格式歌词
- `artist` 参数是可选的，但可以提高搜索准确性
- 中文/特殊字符需要使用 URL 编码

## 使用方法

1. 通过 `web_fetch` 函数访问 API 地址以获取歌词
2. 响应内容为 LRC 格式，其中包含 `[mm:ss.xxx]` 格式的时间戳以及顶部的元数据行
3. 去除时间戳和元数据行（例如歌手信息、制作人信息等，这些信息通常位于 `[00:00]`–`[00:24]` 范围内），以便更清晰地显示歌词
4. 如需打印歌词，将其格式化为纯文本，并包含歌曲标题、歌手名称以及元数据信息

## 示例

```
web_fetch("https://api.lrc.cx/lyrics?title=世界赠予我的&artist=王菲")
```

## 注意事项

- 公共 API 的响应速度可能较慢，请设置合理的超时时间
- 如果没有找到结果，可以尝试仅使用 `title` 参数进行搜索（省略 `artist` 参数）
- 如果仍然没有结果，可以尝试使用不同的歌曲名称拼写进行搜索