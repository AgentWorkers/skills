---
name: nyne-enrichment
description: 您可以使用 Nyne Enrichment API 通过电子邮件、电话号码、LinkedIn URL 或姓名来获取人员的详细信息。该 API 可返回联系信息、社交资料、工作经历、教育背景以及可选的社交媒体帖子。支持“lite”模式（需消耗 3 个信用点数）、新闻推送插件以及由人工智能辅助的深度搜索功能。数据检索采用异步方式，通过轮询来实现。
---
# Nyne 信息丰富服务

可以通过电子邮件、电话号码、LinkedIn URL 或姓名来获取某人的详细信息。该服务可返回联系信息、社交资料、工作经历、教育背景以及可选的社交媒体动态。

**重要提示：** 此 API 是异步的。您需要发送 POST 请求以提交请求，系统会返回一个 `request_id`，之后您需要通过 GET 请求持续轮询直到操作完成。

## 代理操作指南

在向用户展示结果时，应显示**所有可用的数据**，并逐一解释每个部分：

1. **身份信息** — 显示名称、个人简介、所在地、性别
2. **联系方式** — 工作邮箱、个人邮箱以及备用邮箱
3. **社交资料** — LinkedIn、Twitter、GitHub、Instagram 账号及粉丝数量
4. **工作经历** — 所有工作单位的信息（包括单位名称、工作起始/结束日期及当前状态）
5. **教育背景** — 学校名称、所学学位及学习时间
6. **新闻动态**（如用户请求）—— 最新的社交媒体帖子及其互动情况

如果响应中缺少某个字段，说明未找到相关数据，应直接跳过该字段。

在**简化模式**下，仅返回 5 个字段：显示名称、名字、姓氏、第一个工作单位以及 LinkedIn URL。

## 设置

**必需的环境变量：**
- `NYNE_API_KEY` — 您的 Nyne API 密钥
- `NYNE_API_SECRET` — 您的 Nyne API 密码

请在 [https://api.nyne.ai](https://api.nyne.ai) 获取这些凭据。

```bash
export NYNE_API_KEY="your-api-key"
export NYNE_API_SECRET="your-api-secret"
```

**验证环境变量是否已设置：**
```bash
echo "Key: ${NYNE_API_KEY:0:8}... Secret: ${NYNE_API_SECRET:0:6}..."
```

## 注意：JSON 处理

API 响应中的 JSON 字符串可能包含控制字符，这些字符可能导致 `jq` 解析工具出错。所有示例都使用了 `nyne_parse` 辅助函数来清理和重新编码 JSON 数据。请在每个会话中仅定义一次该函数：

```bash
nyne_parse() {
  python3 -c "
import sys, json, re
raw = sys.stdin.read()
clean = re.sub(r'[\x00-\x1f]+', ' ', raw)
data = json.loads(clean)
json.dump(data, sys.stdout)
"
}
```

## 快速入门

通过电子邮件发送请求，并持续轮询直到操作完成：

```bash
nyne_parse() {
  python3 -c "
import sys, json, re
raw = sys.stdin.read()
clean = re.sub(r'[\x00-\x1f]+', ' ', raw)
data = json.loads(clean)
json.dump(data, sys.stdout)
"
}

# Submit enrichment request
curl -s -X POST "https://api.nyne.ai/person/enrichment" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $NYNE_API_KEY" \
  -H "X-API-Secret: $NYNE_API_SECRET" \
  -d '{"email": "someone@example.com"}' | nyne_parse > /tmp/nyne_enrich.json

REQUEST_ID=$(jq -r '.data.request_id' /tmp/nyne_enrich.json)
echo "Request submitted: $REQUEST_ID"

# Poll until complete (checks every 3s, times out after 6 min)
SECONDS_WAITED=0
while [ $SECONDS_WAITED -lt 360 ]; do
  curl -s "https://api.nyne.ai/person/enrichment?request_id=$REQUEST_ID" \
    -H "X-API-Key: $NYNE_API_KEY" \
    -H "X-API-Secret: $NYNE_API_SECRET" | nyne_parse > /tmp/nyne_enrich.json
  STATUS=$(jq -r '.data.status' /tmp/nyne_enrich.json)
  echo "Status: $STATUS ($SECONDS_WAITED seconds elapsed)"
  if [ "$STATUS" = "completed" ]; then
    jq '.data.result' /tmp/nyne_enrich.json
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "Enrichment failed."
    jq . /tmp/nyne_enrich.json
    break
  fi
  sleep 3
  SECONDS_WAITED=$((SECONDS_WAITED + 3))
done

if [ $SECONDS_WAITED -ge 360 ]; then
  echo "Timed out after 6 minutes. Resume polling with request_id: $REQUEST_ID"
fi
```

## 提交信息丰富请求（POST 请求）

**端点：** `POST https://api.nyne.ai/person/enrichment`

**请求头：**
```
Content-Type: application/json
X-API-Key: $NYNE_API_KEY
X-API-Secret: $NYNE_API_SECRET
```

### 输入参数

至少需要提供一个标识符：

| 参数 | 类型 | 说明 |
|-----------|------|-------------|
| `email` | 字符串 | 电子邮件地址（优先使用工作邮箱） |
| `phone` | 字符串 | 电话号码（例如：“+14155551234”） |
| `social_media_url` | 字符串 | LinkedIn、Twitter 或 GitHub 的 URL |
| `name` | 字符串 | 全名（与 `company` 或 `city` 一起使用以消除歧义） |
| `company` | 字符串 | 公司名称（有助于区分同名人员） |
| `city` | 字符串 | 城市名称（支持缩写：SF、NYC、LA） |

**输入优先级：** LinkedIn URL（最佳）> 电子邮件（工作邮箱）> 电话号码（匹配率最低）。同时提供 LinkedIn 和电子邮件地址时，可获得最佳结果。

### 高级参数

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `ai_enhanced_search` | 布尔值 | `false` | 启用 AI 驱动的深度搜索，以获取更多社交资料。处理时间较长。 |
| `lite_enrich` | 布尔值 | `false` | 仅返回基本信息（5 个字段），消耗 3 个信用点 |
| `newsfeed` | 数组 | 可选 | 需要获取的社交媒体来源：`["linkedin", "twitter", "instagram", "github", "facebook"]` 或 `["all"]`。不能将 `"all"` 与特定来源同时使用。找到数据时会额外收取 6 个信用点。 |
| `strict_email_check` | 布尔值 | `false` | 启用严格的电子邮件验证（可能导致无结果） |
| `callback_url` | 字符串 | 可选 | 异步通知的 Webhook URL |

### 示例

- **通过电子邮件查询：**
```bash
curl -s -X POST "https://api.nyne.ai/person/enrichment" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $NYNE_API_KEY" \
  -H "X-API-Secret: $NYNE_API_SECRET" \
  -d '{"email": "someone@example.com"}' | nyne_parse > /tmp/nyne_enrich.json

REQUEST_ID=$(jq -r '.data.request_id' /tmp/nyne_enrich.json)
echo "Request ID: $REQUEST_ID"
```

- **通过 LinkedIn URL 查询：**
```bash
curl -s -X POST "https://api.nyne.ai/person/enrichment" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $NYNE_API_KEY" \
  -H "X-API-Secret: $NYNE_API_SECRET" \
  -d '{"social_media_url": "https://linkedin.com/in/johndoe"}' | nyne_parse > /tmp/nyne_enrich.json

REQUEST_ID=$(jq -r '.data.request_id' /tmp/nyne_enrich.json)
```

- **通过姓名和公司名称查询：**
```bash
curl -s -X POST "https://api.nyne.ai/person/enrichment" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $NYNE_API_KEY" \
  -H "X-API-Secret: $NYNE_API_SECRET" \
  -d '{"name": "Jane Smith", "company": "Acme Corp", "city": "SF"}' | nyne_parse > /tmp/nyne_enrich.json

REQUEST_ID=$(jq -r '.data.request_id' /tmp/nyne_enrich.json)
```

- **包含新闻动态：**
```bash
curl -s -X POST "https://api.nyne.ai/person/enrichment" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $NYNE_API_KEY" \
  -H "X-API-Secret: $NYNE_API_SECRET" \
  -d '{"email": "someone@example.com", "newsfeed": ["linkedin", "twitter"]}' | nyne_parse > /tmp/nyne_enrich.json

REQUEST_ID=$(jq -r '.data.request_id' /tmp/nyne_enrich.json)
```

- **简化模式（3 个信用点）：**
```bash
curl -s -X POST "https://api.nyne.ai/person/enrichment" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $NYNE_API_KEY" \
  -H "X-API-Secret: $NYNE_API_SECRET" \
  -d '{"email": "someone@example.com", "lite_enrich": true}' | nyne_parse > /tmp/nyne_enrich.json

REQUEST_ID=$(jq -r '.data.request_id' /tmp/nyne_enrich.json)
```

- **启用 AI 搜索：**
```bash
curl -s -X POST "https://api.nyne.ai/person/enrichment" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $NYNE_API_KEY" \
  -H "X-API-Secret: $NYNE_API_SECRET" \
  -d '{"email": "someone@example.com", "ai_enhanced_search": true}' | nyne_parse > /tmp/nyne_enrich.json

REQUEST_ID=$(jq -r '.data.request_id' /tmp/nyne_enrich.json)
```

**提交请求后：**
```json
{
  "success": true,
  "data": {
    "request_id": "abc123-...",
    "status": "queued",
    "message": "Enrichment request queued. Use GET /person/enrichment?request_id=... to check status."
  }
}
```

## 获取结果（GET 请求）

**端点：** `GET https://api.nyne.ai/person/enrichment?request_id={id}`

**请求头：** 与上述相同，需包含 `X-API-Key` 和 `X-API-Secret`。

### 检查请求状态**

```bash
curl -s "https://api.nyne.ai/person/enrichment?request_id=$REQUEST_ID" \
  -H "X-API-Key: $NYNE_API_KEY" \
  -H "X-API-Secret: $NYNE_API_SECRET" | nyne_parse > /tmp/nyne_enrich.json

jq '{status: .data.status, completed: .data.completed}' /tmp/nyne_enrich.json
```

### 完整的轮询流程

```bash
SECONDS_WAITED=0
TIMEOUT=360  # 6 minutes

while [ $SECONDS_WAITED -lt $TIMEOUT ]; do
  curl -s "https://api.nyne.ai/person/enrichment?request_id=$REQUEST_ID" \
    -H "X-API-Key: $NYNE_API_KEY" \
    -H "X-API-Secret: $NYNE_API_SECRET" | nyne_parse > /tmp/nyne_enrich.json
  STATUS=$(jq -r '.data.status' /tmp/nyne_enrich.json)

  echo "[$(date +%H:%M:%S)] Status: $STATUS ($SECONDS_WAITED s)"

  case "$STATUS" in
    completed)
      jq '.data.result' /tmp/nyne_enrich.json
      break
      ;;
    failed)
      echo "Enrichment failed:"
      jq '.data' /tmp/nyne_enrich.json
      break
      ;;
    *)
      sleep 3
      SECONDS_WAITED=$((SECONDS_WAITED + 3))
      ;;
  esac
done

if [ "$STATUS" != "completed" ] && [ "$STATUS" != "failed" ]; then
  echo "Timed out. Resume polling with request_id: $REQUEST_ID"
fi
```

## 响应结构

当 `status` 为 `completed` 时，响应内容如下：

```json
{
  "success": true,
  "timestamp": "2025-09-05T21:45:25Z",
  "data": {
    "request_id": "abc123-...",
    "status": "completed",
    "completed": true,
    "created_on": "2025-09-05T21:45:06",
    "completed_on": "2025-09-05T21:45:12",
    "result": {
      "displayname": "...",
      "firstname": "...",
      "lastname": "...",
      "bio": "...",
      "location": "...",
      "gender": "...",
      "fullphone": [...],
      "altemails": [...],
      "best_work_email": "...",
      "best_personal_email": "...",
      "social_profiles": {...},
      "organizations": [...],
      "schools_info": [...],
      "newsfeed": [...],
      "probability": "high"
    }
  }
}
```

**所有字段均为可选**——仅在找到相关信息时才会包含。如果无法找到此人，则不会产生费用。

### 结果字段

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `displayname` | 字符串 | 全显示名称 |
| `firstname` | 字符串 | 名字 |
| `lastname` | 字符串 | 姓氏 |
| `bio` | 字符串 | 个人简介/标题 |
| `location` | 字符串 | 所在地 |
| `gender` | 字符串 | 性别 |
| `fullphone` | 数组 | 电话号码（格式为 `{fullphone, type}`） |
| `altemails` | 数组 | 备用邮箱地址 |
| `best_work_email` | 字符串 | 最可能的工作邮箱 |
| `best_personal_email` | 字符串 | 最可能的个人邮箱 |
| `social_profiles` | 对象 | LinkedIn、Twitter、GitHub、Instagram 的详细信息（包含 URL、用户名及粉丝数量） |
| `organizations` | 数组 | 工作经历（包含单位名称、职位、工作起始/结束日期及当前状态） |
| `schools_info` | 数组 | 教育背景（包含学校名称、学位、所学专业及学习时间） |
| `newsfeed` | 数组 | 社交媒体动态（如用户请求）：`{source, type, content, date_posted, url, engagement}` |
| `probability` | 字符串 | 匹配置信度：“high”、“medium”、“low”（仅在 `probability_score: true` 时显示） |

### 社交资料对象

```json
{
  "linkedin": {"url": "...", "username": "...", "followers": 542, "connections": 1243},
  "twitter": {"url": "...", "username": "...", "followers": 1234, "following": 567, "posts": 892},
  "github": {"url": "...", "username": "...", "followers": 89, "following": 45},
  "instagram": {"url": "...", "username": "...", "followers": 500}
}
```

### 新闻动态条目

```json
{
  "source": "linkedin",
  "type": "post",
  "content": "...",
  "date_posted": "2025-09-01T14:30:00Z",
  "url": "...",
  "author": {"display_name": "...", "username": "...", "profile_url": "..."},
  "engagement": {"likes": 42, "comments": 5, "shares": 3, "total_reactions": 50}
}
```

### 简化模式响应

当 `lite_enrich` 为 `true` 时，仅返回以下字段：
- `displayname`、`firstname`、`lastname`
- 第一个工作单位的名称及职位
- LinkedIn URL

## 有用的 `jq` 过滤器

轮询完成后，处理后的响应数据会保存在 `/tmp/nyne_enrich.json` 文件中：

```bash
# Full result
jq '.data.result' /tmp/nyne_enrich.json

# Identity summary
jq '.data.result | {displayname, bio, location, gender}' /tmp/nyne_enrich.json

# All emails
jq '.data.result | {best_work_email, best_personal_email, altemails}' /tmp/nyne_enrich.json

# Social profiles
jq '.data.result.social_profiles' /tmp/nyne_enrich.json

# Work history
jq '.data.result.organizations' /tmp/nyne_enrich.json

# Education
jq '.data.result.schools_info' /tmp/nyne_enrich.json

# Phone numbers
jq '.data.result.fullphone' /tmp/nyne_enrich.json

# Newsfeed posts (if requested)
jq '.data.result.newsfeed[] | {source, date_posted, content, engagement}' /tmp/nyne_enrich.json

# LinkedIn info specifically
jq '.data.result.social_profiles.linkedin' /tmp/nyne_enrich.json

# Current job
jq '[.data.result.organizations[] | select(.endDate_formatted.is_current == true)]' /tmp/nyne_enrich.json
```

## 错误处理

| HTTP 状态码 | 错误信息 | 说明 |
|-----------|-------|-------------|
| 400 | `missing_parameters` | 未提供必要的参数 |
| 400 | `invalid_newsfeed` | 社交媒体来源参数无效（不能同时使用 “all” 和特定来源） |
| 401 | `invalid_credentials` | API 密钥/密码无效 |
| 403 | `subscription_required` | 用户未订阅该服务 |
| 404 | `request_not_found` | 用于检查状态的请求 ID 无效 |
| 429 | `rate_limit_exceeded` | 请求次数超出限制 |
| 500 | `internal_error` | 服务器内部错误 |

## 不同模式及其使用场景

### 标准信息丰富（6 个信用点）
默认模式。返回完整的联系信息、社交资料、工作经历和教育背景。适用于大多数查询场景。

```json
{"email": "someone@example.com"}
```

### 简化信息丰富（3 个信用点）
`lite_enrich: true` — 仅返回基本信息：`displayname`、`firstname`、`lastname`、`organizations` 数组中的第一个工作单位名称以及 `social_profiles.linkedin.url`。启用此模式后，所有高级功能（如 `ai_enhanced_search`、`newsfeed` 和 `strict_email_check`）将被禁用。适用于仅需基本信息且希望降低成本的情况。

```json
{"email": "someone@example.com", "lite_enrich": true}
```

### 启用 AI 搜索（6 个信用点，处理时间较长）
`ai_enhanced_search: true` — 启用 AI 驱动的深度搜索，以获取更多社交资料。处理时间较长（可能长达几分钟）。仅当需要全面的信息且能接受较长的处理时间时使用。

```json
{"email": "someone@example.com", "ai_enhanced_search": true}
```

### 新闻动态功能（找到数据时额外收费 6 个信用点）
`newsfeed: [...]` — 从指定来源请求社交媒体动态数据。有效来源：`["linkedin", "twitter", "instagram", "github", "facebook"]` 或 `["all"]`。不能将 `"all"` 与特定来源同时使用。找到数据时会额外收费。适用于需要查看某人的动态或了解其活跃度的情况。

### 严格电子邮件验证
`strict_email_check: true` — 启用严格的电子邮件验证。由于验证严格，可能会导致无结果。适用于对电子邮件准确性要求极高的情况。

### 未找到匹配结果（0 个信用点）
如果无法找到此人，则不会产生费用。

## 请求限制

- **每分钟**：60 次请求 |
- **每小时**：1,000 次请求 |
- **每月**：取决于订阅计划