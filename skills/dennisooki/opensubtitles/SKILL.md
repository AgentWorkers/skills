---
name: opensubtitles
description: >
  **只读型 OpenSubtitles 技能**  
  该技能通过 API 搜索并下载字幕，随后根据时间戳提取特定场景的上下文信息，以便用户能够了解剧集中的具体情节（同时避免剧透）。适用于用户询问“在某个时间点发生了什么”或需要字幕相关背景信息的情况。该技能与 `trakt-readonly` 技能（用于播放进度控制）配合使用效果更佳。  
  **使用要求：**  
  需要具备 OpenSubtitles API 密钥以及有效的 `User-Agent` 标头。
metadata: {"openclaw":{"requires":{"env":["OPENSUBTITLES_API_KEY","OPENSUBTITLES_USER_AGENT"],"bins":["curl","jq","awk"]},"primaryEnv":"OPENSUBTITLES_API_KEY","emoji":"📝"}}
---
# OpenSubtitles

使用此技能可以获取指定时间戳周围的字幕信息。该技能仅支持读取操作，不支持上传或修改字幕文件。

## 设置

用户需在以下链接获取API密钥：https://www.opensubtitles.com/consumers

**必需的环境变量：**
- `OPENSUBTITLES_API_KEY`
- `OPENSUBTITLES_USER_AGENT`（例如：`OpenClaw 1.0`）

**可选参数（用于下载）：**
- `OPENSUBTITLES_USERNAME`
- `OPENSUBTITLES_PASSWORD`
- `OPENSUBTITLES_TOKEN`（如果已登录）
- `OPENSUBTITLES_BASE_URL`（登录响应中提供的主机名，例如：`api.opensubtitles.com`）

## 命令

所有脚本位于 `{baseDir}/scripts/` 目录下。

### 搜索字幕

```
{baseDir}/scripts/opensubtitles-api.sh search --query "Show Name" --season 3 --episode 5 --languages en
```

优先使用字幕的ID（如imdb或tmdb提供的ID）。对于电视剧集，可以使用父ID进行搜索。搜索时会自动处理重定向（脚本已使用`-L`参数）。

### 登录（使用Token）

```
{baseDir}/scripts/opensubtitles-api.sh login
```

**注意：** 登录操作存在频率限制：每秒1次、每分钟10次、每小时30次。如果收到401错误，请停止重试。后续请求请使用登录响应中的`base_url`作为`OPENSUBTITLES_BASE_URL`。

### 请求下载链接

在下载之前，请先检查本地字幕缓存（详见下文）。只有当文件尚未缓存时，才调用下载API。

```
OPENSUBTITLES_TOKEN=... {baseDir}/scripts/opensubtitles-api.sh download-link --file-id 123
```

### 提取指定时间戳的字幕内容

下载 `.srt` 文件后（默认时间范围为时间戳前10分钟）：

在Windows系统中，可以使用`findstr`或PowerShell的`Select-String`命令来实现与awk相似的功能（可参考相应的Shell脚本）。具体使用哪种工具取决于系统的实际情况。

```
{baseDir}/scripts/subtitle-context.sh ./subtitle.srt 00:12:34,500
```

**自定义时间范围：**

```
{baseDir}/scripts/subtitle-context.sh ./subtitle.srt 00:12:34,500 --window-mins 5
```

## 与Trakt的协同使用

将此技能与`trakt-readonly`结合使用，以便识别当前正在播放的剧集。当Trakt支持播放进度显示功能后，更新`trakt`技能，以便提供更精确的时间戳，从而避免显示剧透内容。

## 缓存

下载的字幕文件存储在 `{baseDir}/storage/subtitles/` 目录下（如果目录不存在则创建）。文件名格式如下：
`{baseDir}/storage/subtitles/<file_id>__<language>.srt`

在调用 `/download` 命令之前，请先检查缓存，以避免浪费每日有限的下载次数。

## 安全注意事项：
- **严禁** 存储或泄露API密钥、密码或Token。
- 仅使用 `https://api.opensubtitles.com/api/v1`（或登录响应返回的 `base_url`）进行请求。
- 不要缓存下载链接。
- 为提高搜索准确性，优先使用字幕的ID而非模糊查询。
- **避免浪费下载资源**：将下载的字幕文件保存在本地，并在再次调用下载API之前检查缓存。
- 如果请求下载，请在用户响应中包含剩余的下载配额信息。
- 字幕内容应包含时间戳前10分钟到时间戳之间的所有字幕信息（默认设置），除非用户另有指定。
- 用户可以通过调整 `--window-mins` 参数来调整获取的字幕时间范围。
- 请仅从 `{baseDir}/storage/subtitles/` 目录中读取字幕文件，以防止随意访问文件。

## 参考资料：
- `references/opensubtitles-api.md`