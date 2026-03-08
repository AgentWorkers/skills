---
name: felo-youtube-subtitling
description: "使用 Felo YouTube Subtitling API 获取 YouTube 视频的字幕/旁白。适用于用户请求获取 YouTube 字幕、从视频中提取字幕、通过视频 ID 或 URL 获取字幕文本的情况，或者当使用类似 `/felo-youtube-subtitling` 的明确命令时。该 API 支持指定语言以及可选的时间戳参数。"
---
# Felo YouTube 字幕提取技能

## 使用场景

当用户需要执行以下操作时，可以使用此技能：

- 从 YouTube 视频中获取字幕或标题
- 根据视频 ID 或视频 URL 提取字幕内容
- 获取指定语言的字幕（例如：en、zh-CN）
- 获取带有时间戳的字幕数据（用于分析或翻译）

**触发关键词示例**：
- YouTube 字幕、获取字幕、视频字幕、提取字幕、Felo YouTube 字幕提取

**不适用场景**：
- 实时搜索（请使用 `felo-search`）
- 网页内容提取（请使用 `felo-web-fetch`）
- 生成幻灯片（请使用 `felo-slides`）

## 设置

### 1. 获取 API 密钥

1. 访问 [felo.ai](https://felo.ai)
2. 进入“设置” -> “API 密钥”
3. 创建并复制您的 API 密钥

### 2. 配置环境变量

**Linux/macOS**：
```bash
export FELO_API_KEY="your-api-key-here"
```

**Windows PowerShell**：
```powershell
$env:FELO_API_KEY="your-api-key-here"
```

## 使用方法

### 方法一：使用捆绑的脚本或封装的命令行工具

**脚本**（来自仓库）：
```bash
node felo-youtube-subtitling/scripts/run_youtube_subtitling.mjs --video-code "dQw4w9WgXcQ" [options]
```

**封装的命令行工具**（安装完成后使用 `npm install -g felo-ai`）：
```bash
felo youtube-subtitling -v "dQw4w9WgXcQ" [options]
# 简化形式：-v（视频代码）、-l（语言）、-j（JSON格式）

**参数说明**：
| 参数 | 默认值 | 说明 |
|--------|---------|-------------|
| --video-code | / -v | YouTube 视频 URL 或视频 ID（例如：`https://youtube.com/watch?v=ID` 或 `dQw4w9WgXcQ`） |
| --language | - | 字幕语言代码（例如：`en`、`zh-CN`） |
| --with-time | false | 是否包含每个字幕片段的时间戳 |
| --json | -j | 是否以 JSON 格式输出完整 API 响应 |

**输入格式**：
- 可以输入完整的 YouTube 链接或 11 位的视频 ID：
  - 支持的 URL 格式：`https://www.youtube.com/watch?v=ID`、`https://youtu.be/ID`、`https://youtube.com/embed/ID`
  - 或纯视频 ID：`dQw4w9WgXcQ`

**示例**：
```bash
# 使用视频 URL：
node felo-youtube-subtitling/scripts/run_youtube_subtitling.mjs --video-code "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
felo youtube-subtitling -v "https://youtu.be/dQw4w9WgXcQ"

# 使用视频 ID：
node felo-youtube-subtitling/scripts/run_youtube_subtitling.mjs -v "dQw4w9WgXcQ" --language zh-CN

# 带时间戳：
node felo-youtube-subtitling/scripts/run_youtube_subtitling.mjs -v "dQw4w9WgXcQ" --with-time --json
```

### 方法二：使用 curl 调用 API

```bash
curl -X GET "https://openapi.felo.ai/v2/youtube/subtitling?video_code=dQw4w9WgXcQ" \
  -H "Authorization: Bearer $FELO_API_KEY"
```

## API 参考

- **端点**：`GET /v2/youtube/subtitling`
- **基础 URL**：`https://openapi.felo.ai`（如需更改，请使用环境变量 `FELO_API_BASE`
- **认证**：`Authorization: Bearer YOUR_API_KEY`

### 查询参数

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|------|---------|-------------|
| video_code | string | 是 | YouTube 视频 ID（例如：dQw4w9WgXcQ） |
| language | string | 否 | 字幕语言代码（例如：en、zh-CN） |
| with_time | boolean | 否 | 是否包含每个字幕片段的时间戳 |

### 响应格式（200 状态码）

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "title": "视频标题",
    "contents": [
      { "start": 0.32, "duration": 14.26, "text": "字幕内容" }
    ]
  }
}
```

- 当 `with_time` 为 `false` 时，`start` 和 `duration` 可能为空或为 0。
- `contents[]` 中的 `text` 字段始终存在。

### 错误代码

| HTTP 状态码 | 描述 |
|---------|--------|
| 400 | 参数验证失败（例如：缺少 video_code） |
| 401 | API 密钥无效或已过期 |
| 500/502 | 提取字幕失败（可能是因为视频无法获取字幕） |

## 输出格式

- 不使用 `--json` 选项时：输出视频标题以及每个字幕片段的文本（每行一个或合并显示）。
- 使用 `--json` 选项时：输出完整的 API 响应。

**失败情况**：
- 如果无法获取字幕或 API 出错，会在标准错误输出（stderr）中显示错误信息，并退出程序（退出代码为 1）。
**示例**：
```
提取视频 dQw4w9WgXcQ 的字幕失败：YOUTUBE_SUBTITLING_FAILED
```

## 重要说明**

- 并非所有视频都配有字幕；某些视频可能无法通过此 API 获取字幕。
- 输入的语言代码必须与视频中可用的字幕语言代码相匹配。
- 该技能需要使用与 Felo 其他技能相同的 API 密钥（`FELO_API_KEY`）。

## 参考资料

- [Felo YouTube 字幕提取 API 文档](https://openapi.felo.ai/docs/api-reference/v2/youtube-subtitling.html)
- [Felo 开放平台文档](https://openapi.felo.ai/docs/)
```