---
name: timeless
description: 查询和管理 Timeless 会议、会议室、会议记录以及 AI 文档。可以将播客剧集和 YouTube 视频导入 Timeless 进行转录。当用户需要查询会议信息、搜索会议记录、阅读会议摘要、列出会议室、创建会议室、在会议室中添加或删除对话内容、处理 Timeless 的共享链接、上传会议录像，或与 Timeless AI 交流会议内容时，都可以使用该功能。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TIMELESS_ACCESS_TOKEN
      bins:
        - curl
        - node
      anyBins:
        - yt-dlp
    primaryEnv: TIMELESS_ACCESS_TOKEN
    emoji: "\u23F0"
    homepage: https://github.com/supertools/timeless-skills
---
# Timeless

> **来源**: [github.com/supertools/timeless-skills](https://github.com/supertools/timeless-skills)

**交互功能**：  
您可以与 [Timeless](https://timeless.day) 的会议数据进行交互，包括搜索会议、阅读会议记录、获取人工智能生成的摘要、浏览会议室、上传录制内容、与 AI 助手聊天，以及捕获 podcasts 或 YouTube 视频以进行转录。

## API 参考  
有关完整的端点文档（包含响应格式、状态枚举和详细示例），请参阅 `api-reference.md`（位于该技能文件夹中）。

## 先决条件  
- 环境变量 `TIMELESS_ACCESS_TOKEN`（在 [my.timeless.day/api-token](https://my.timeless.day/api-token) 获取令牌）  
- 用于下载 YouTube 视频的 `yt-dlp` 工具（通过包管理器安装：`apt install yt-dlp`、`brew install yt-dlp` 或 `pip install yt-dlp`；或者将 `YTDLP_PATH` 设置为已存在的二进制文件路径。）

**在 OpenClaw 中的设置：**  
```bash
openclaw config patch env.vars.TIMELESS_ACCESS_TOKEN=<your_token>
```

## 基本 URL  
```
https://my.timeless.day
```

## 认证头  
所有请求都需要包含以下认证头：  
```
Authorization: Token $TIMELESS_ACCESS_TOKEN
```

---

## 操作  

### 1. 列出会议  
**必填参数**：`include` 必须设置为 `owned` 或 `shared`。  
| 参数 | 类型 | 描述 |  
|-----------|------|-------------|  
| `include` | 字符串 | **必填**。值可为 `owned` 或 `shared` |  
| `search` | 字符串 | 按标题或参与者搜索会议 |  
| `start_date` | 字符串 | 开始日期（格式：YYYY-MM-DD） |  
| `end_date` | 字符串 | 结束日期（格式：YYYY-MM-DD） |  
| `status` | 字符串 | `COMPLETED`、`SCHEDULED`、`PROCESSING`、`FAILED` |  
| `page` | 整数 | 页码（默认值：1） |  
| `per_page` | 整数 | 每页显示的结果数量（默认值：20） |  

**响应格式：**  
`{ count, next, previous, results: [{ uuid, title, start_ts, end_ts, status, primary_conversation_uuid, host_user, conversation_source, created_at }] }`  

**关键字段说明：**  
- `uuid`：空间的唯一标识符  
- `primary_conversation_uuid`：会议记录的唯一标识符  

> 要获取所有会议的信息，需要分别执行两次请求（`include=owned` 和 `include=shared`），然后合并结果。  

---

### 2. 列出会议室  
查询参数与列出会议相同（会议室数据不包含 `start_ts`、`end_ts` 和 `status` 字段）。  
**响应格式：**  
`{ count, next, previous, results: [{ uuid, title, host_user, created_at }] }`  

---

### 3. 获取会议室信息（会议或会议室的详细信息）  
会议室有三个访问级别：  
**按顺序尝试，直到成功为止：**  

#### 3a. 私人会议室（仅限您自己使用）  
```bash
curl -s "https://my.timeless.day/api/v1/spaces/{uuid}/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN"
```  

#### 3b. 工作室会议室（团队内共享）  
> 共享会议室需要 `host_uuid`。该 ID 可从列出会议或会议室的响应中的 `host_user_uuid` 字段获取。  
```bash
curl -s "https://my.timeless.day/api/v1/spaces/{uuid}/workspace/?host_uuid={hostUuid}" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN"
```  

#### 3c. 公共会议室（公开共享）  
**响应内容包括：**  
- `conversations[]`：该会议室中的录制内容（每个记录包含 `uuid`、`name`、`start_ts`、`end_ts`、`status`、`language`）  
- `artifacts[]`：人工智能生成的文档（`type` 字段示例：`"summary"`；内容存储在 `content.body` 中）  
- `contacts[]`：每个联系人对应的对话记录  
- `organizations[]`：每个组织对应的对话记录  
- `threads[]`：AI 聊天记录（使用 `threads[0].uuid` 与助手聊天）  

**收集会议室中的所有对话记录：**  
从 `conversations[]`、`contacts[].conversations[]` 和 `organizations[].conversations[]` 中提取唯一的对话记录 ID。  

---

### 4. 获取会议记录  
**响应格式：**  
```json
{
  "items": [
    { "text": "...", "start_time": 0.5, "end_time": 3.2, "speaker_id": "speaker_0" }
  ],
  "speakers": [
    { "id": "speaker_0", "name": "Alice Johnson" }
  ],
  "language": "he"
}
```  

**获取对话记录的唯一 ID 的方法：**  
- 从列出会议的响应中获取：`primary_conversation_uuid`  
- 从会议室信息中获取：`conversations[].uuid`  

**将对话记录转换为可读文本：**  
通过将 `speaker_id` 映射到对应的发言者名称来实现。  
```
[00:00:00] Alice Johnson: ...
[00:00:03] Bob Smith: ...
```  

---

### 5. 获取录制内容的 URL  
**响应格式：**  
`{ "media_url": "https://storage.googleapis.com/...signed..." }`  
> 该 URL 有时间限制，需要根据需要重新获取。  

---

### 6. 上传录制内容  
**上传流程分为三步：**  
```bash
# Step 1: Get presigned URL
curl -X POST "https://my.timeless.day/api/v1/conversation/storage/presigned-url/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"file_name": "recording.mp3", "file_type": "audio/mpeg"}'

# Step 2: Upload file to the presigned URL
curl -X PUT "PRESIGNED_URL" \
  -H "Content-Type: audio/mpeg" \
  --upload-file recording.mp3

# Step 3: Trigger processing
curl -X POST "https://my.timeless.day/api/v1/conversation/process/media/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"language": "he", "filename": "Recording Title"}'
```  
**步骤 3 的响应格式：**  
`{ "event_uuid": "...", "space_uuid": "..." }`  

**使用辅助脚本上传：**  
`bash scripts/upload.sh FILE_PATH LANGUAGE [TITLE]`  

**支持的格式：**  
mp3、wav、m4a、mp4、webm、ogg  

---

### 7. 解码 Timeless 共享链接  
URL（如 `https://my.timeless.day/m/ENCODED_ID`）包含两个 Base64 编码的短 ID（每个 ID 22 个字符）。  

**解码方法（Shell）：**  
```bash
ENCODED="the_part_after_/m/"
DECODED=$(echo "$ENCODED" | base64 -d)
SPACE_ID=$(echo "$DECODED" | cut -c1-22)
HOST_ID=$(echo "$DECODED" | cut -c23-44)
```  
**解码方法（Python）：**  
```python
import base64

def decode_timeless_url(url):
    encoded = url.rstrip('/').split('/m/')[-1]
    combined = base64.b64decode(encoded).decode()
    return combined[:22], combined[22:]  # (space_id, host_id)
```  
解码后，使用获取会议室信息的接口来访问相关内容（先尝试访问私人会议室，然后是工作组会议室，最后是公共会议室）。  

---

### 8. 与 Timeless AI 聊天  
您可以询问关于会议或会议室的问题：  
#### 第一步：发送消息  
**获取对话记录的唯一 ID：**  
从会议室的 `threads[0].uuid` 中获取。  

#### 第二步：等待回复  
**每隔 2-3 秒轮询一次**，直到 `is_running` 的值为 `false`。AI 的回复是 `messages` 数组中 `role` 为 `assistant` 的那条消息。  

---

### 9. 创建会议室  
**响应格式：**  
完整的会议室对象。提取 `uuid` 以用于添加资源。  

---

### 10. 向会议室添加/删除对话记录  
**每次添加或删除对话记录时都需要调用相应的 API。**  
对话记录的 ID 可从列出会议的响应（`primary_conversation_uuid`）或会议室信息（`conversations[].uuid`）中获取。  

## 常见工作流程  
### 导出所有会议记录  
1. 使用 `include=owned&status=COMPLETED&per_page=100` 列出所有已完成会议的记录。  
2. 分页浏览所有记录。  
3. 对于每个会议，使用 `primary_conversation_uuid` 获取其会议记录。  

### 从会议室获取所有信息  
1. 获取会议室的 `uuid`。  
2. 从 `conversations[]`、`contacts[].conversations[]` 和 `organizations[].conversations[]` 中收集所有对话记录的 ID（去除重复项）。  
3. 获取每个对话记录的记录。  

### 搜索和阅读  
1. 使用 `search=your+query` 列出会议。  
2. 选择目标会议，获取其 `primary_conversation_uuid`。  
3. 获取会议记录。  
4. （可选）使用 `artifacts[]` 获取会议摘要。  

---

## 自动化流程  
**Timeless` 目前不支持 Webhook 功能。**  
要实现自动检测新会议的自动化流程，可以使用 **定时任务（cron）和状态文件**。  

**自动化流程示例：**  
定时任务每 5-10 分钟运行一次，执行以下操作：  
1. 读取状态文件（`timeless-processed.json`）；如果文件不存在，则创建一个空数组。  
2. 查询已完成的会议：`GET /api/v1/spaces/meeting/?include=owned&status=COMPLETED&start_date=YYYY-MM-DD`  
3. 如果会议的 `uuid` 已经在状态文件中，则跳过该会议。  
4. 对于新会议，获取所需的数据（会议记录、会议室信息、文档），然后执行自动化逻辑。  
5. 将处理过的会议 ID 添加到状态文件中。  
6. **如果没有新会议，则静默退出**，无需通知用户。  

**状态文件格式：**  
```json
{
  "processed": ["uuid-1", "uuid-2", "uuid-3"],
  "last_check": "2026-03-05T12:00:00Z"
}
```  
**关键规则：**  
- 状态文件中的会议 ID 仅会被处理一次，以避免重复处理。  
- 定期删除过时的会议 ID（例如，超过 30 天的会议），以保持文件大小适中。  
- 如果自动化需要处理共享会议的数据，还需包含 `include=shared` 的参数。  

**在 OpenClaw 中设置定时任务：**  
```
openclaw cron add "timeless-poll" --schedule "*/5 * * * *" --task "Check for new completed Timeless meetings. Read timeless-processed.json for state. Poll the API. For new meetings: [your automation here]. If nothing new, reply HEARTBEAT_OK."
```  

### 新会议的处理方式  
当定时任务检测到新完成的会议时，您可以获取以下信息：  
- **会议记录**（通过 `Get Transcript` 获取包含发言者信息的完整文本）  
- **人工智能生成的摘要和行动项**（通过 `Get Space` 和 `artifacts[]` 获取）  
- **参会者和元数据**（通过 `Get Space` 和 `conversations[].event.attendees` 获取）  
- **录制内容的 URL**（通过 `Get Recording` 获取）  
- **与 Timeless AI 聊天**（通过 “Chat with Timeless AI” 功能提问）  

**这些功能可以与其他工具或 API 结合使用**：  
- 自动生成会议总结报告或文档  
- 将会议数据导入仪表板，跟踪会议主题、行动项或会议负载变化  
- 根据规则（如参与者、标题或主题）自动整理会议室内容  
- 将摘要或行动项推送到 Slack、电子邮件、Notion 或 CRM 等工具  
- 对会议记录进行情感分析或提取自定义字段  
- 构建可搜索的会议知识库  

**自动化流程始终如下：**  
定期检查新会议，获取数据，然后执行相应的操作。  

---

## 捕获媒体内容  
**媒体内容捕获脚本位于 `scripts/` 文件夹中：**  
- **搜索播客**：`bash scripts/podcast.sh search "podcast name"`  
- **列出剧集**：`bash scripts/podcast.sh episodes FEED_URL [limit]`  
- **下载播客文件**：`bash scripts/podcast.sh download MP3_URL /tmp/episode.mp3`  
- **上传到 Timeless**：`bash scripts/upload.sh /tmp/episode.mp3 en "Episode Title"`  
- **清理临时文件夹 `/tmp` 中的文件**  

### 捕获 YouTube 视频内容  
**步骤如下：**  
1. 获取视频信息：`bash scripts/youtube.sh info "YOUTUBE_URL"`  
2. 下载视频：`bash scripts/youtube.sh download "YOUTUBE_URL" /tmp/video.mp4`  
3. **上传到 Timeless**：`bash scripts/upload.sh /tmp/video.mp4 en "Video Title"`  
- **下载的文件为 MP4 格式（包含视频和音频）**；无需使用 ffmpeg。  

---  

## 将内容添加到会议室  
**上传完成后，将视频文件添加到 Timeless 会议室中：**  
1. 上传操作会返回一个 `space_uuid`。  
2. 轮询 `GET /api/v1/spaces/{space_uuid}/`，直到 `is_processing` 的值为 `false`。  
3. 从会议室响应中获取 `conversation_uuid`。  
4. 使用 `POST /api/v1/spaces/{room_uuid}/resources/` 添加视频文件（格式：`{"resource_type": "CONVERSATION", "resource_uuid": "CONV_uuid"`）。  
**创建新会议室的步骤：**  
`POST /api/v1/spaces/`，参数设置为 `{"has_onboarded": true, "space_type": "ROOM", "title": "My Collection"}`  

---

## 注意事项：**  
- 长播客文件可能较大（100-300MB），下载可能需要一段时间。  
- 下载 YouTube 视频需要 `yt-dlp`；如果未安装该工具，脚本会失败并显示错误信息。  
- 上传完成后，请务必清理 `/tmp` 文件夹中的文件。  
- 如果系统路径中未包含 `yt-dlp`，请设置环境变量 `YTDLP_PATH`。  

## 错误处理**  
| 错误代码 | 处理方式 |  
|------|--------|  
| 401 | 令牌过期。请在 [my.timeless.day/api-token] 重新认证。 |  
| 403 | 无访问权限。请尝试使用工作组或公共会议室的 API。 |  
| 404 | 未找到相关资源。请检查会议 ID。 |  
| 429 | 请求频率受限。请稍后再试。 |  

## 请求限制**  
虽然官方没有明确限制，但请遵守以下规则：  
- 连续请求之间至少间隔 0.5 秒。  
- 每分钟最多发送 60 次请求。  
- 使用分页功能，避免一次性获取所有数据。