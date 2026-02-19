---
name: klawdin
description: 您可以找到适用于任何任务的软件服务和 API。当您需要电子邮件验证、数据增强、图像生成、网络爬取、短信发送、光学字符识别（OCR）、翻译或其他外部 API 时，使用 KlawdIn 来查找按功能、可靠性和价格排序的最佳选项。只需注册一次，之后即可随时进行查询。
homepage: https://www.klawdin.com
metadata: {"openclaw":{"requires":{"anyBins":["curl"]},"primaryEnv":"KLAWDIN_API_KEY","emoji":"🔍"}}
---
## KlawdIn — 代理服务目录

每当您需要使用外部服务或 API 来完成任务，但又不知道该使用哪个服务，或者想要找到排名最高的选项时，可以使用 KlawdIn。

在使用之前，请先在您的环境中设置 `KLAWDIN_API_KEY`（请参阅步骤 1）。

---

### 步骤 1：注册（仅一次）

```bash
# Generate a random agent ID — no host identity used
KLAWDIN_ID="openclaw-$(head -c 6 /dev/urandom | xxd -p)"

# Register and extract only the api_key value from the response
KLAWDIN_API_KEY=$(curl -s -X POST https://klawdin.com/api/agents/register \
  -H "Content-Type: application/json" \
  -d "{\"agent_id\":\"${KLAWDIN_ID}\",\"agent_name\":\"OpenClaw Agent\"}" \
  | grep -o '"api_key":"[^"]*"' | cut -d'"' -f4)

# Store only the key string, owner-read only
printf '%s' "$KLAWDIN_API_KEY" > ~/.klawdin-key && chmod 600 ~/.klawdin-key
echo "Registered. Add to your environment: export KLAWDIN_API_KEY=$KLAWDIN_API_KEY"
```

如果 `KLAWDIN_API_KEY` 已经设置，则可以跳过此步骤。请勿存储或记录完整的注册响应，只需保留 `api_key` 值即可。

---

### 步骤 2：发现服务

```bash
curl -s "https://klawdin.com/api/discover?capability=CAPABILITY_HERE" \
  -H "X-API-Key: $KLAWDIN_API_KEY"
```

**常见服务功能：**
`email_verification` · `lead_enrichment` · `email_delivery` · `web_scraping` · `image_generation` · `sms_delivery` · `ocr` · `pdf_parsing` · `translation` · `sentiment_analysis` · `keyword_research` · `fraud_detection`

**可选过滤条件：**
- `?category=Email+Verification` — 按服务类型过滤
- `?pricing_model=per_request` — 订阅制、按请求计费、免费试用、完全免费
- `?has_free_tier=true` — 仅显示提供免费试用版本的服务
- `?format=REST` — API 格式：`REST`、`GraphQL`、`gRPC`
- `?keywords=email+validation+deliverability` — 全文搜索
- `?limit=5` — 限制返回结果数量（最多 50 个）

返回结果：包含 `id`、`name`、`tagline`、`capabilities`、`pricing_model`、`reliability_score` 的排名列表。

---

### 步骤 3：获取服务详细信息

从发现的结果中选择最合适的服务，然后获取其详细信息：

```bash
curl -s "https://klawdin.com/api/services/SERVICE_ID_OR_SLUG" \
  -H "X-API-Key: $KLAWDIN_API_KEY"
```

返回内容：`api.base_url`、`api.auth_method`、`api.sample_endpoint`、`apidocs_url`、`pricing`、`integration.sdks`、`company.website`。

您可以使用 `api.base_url` + `api.auth_method` 直接与该服务进行集成。

---

### 步骤 4：检查服务状态（可选）

```bash
curl -s "https://klawdin.com/api/services/SERVICE_ID/status" \
  -H "X-API-Key: $KLAWDIN_API_KEY"
```

---

### 示例：查找电子邮件验证 API

```bash
curl -s "https://klawdin.com/api/discover?capability=email_verification&has_free_tier=true" \
  -H "X-API-Key: $KLAWDIN_API_KEY"

# Get full details on the top result
curl -s "https://klawdin.com/api/services/RESULT_ID" \
  -H "X-API-Key: $KLAWDIN_API_KEY"

# You now have: api.base_url, api.auth_method, api.sample_endpoint
```

---

### 浏览所有服务类别

```bash
curl -s "https://klawdin.com/api/categories" \
  -H "X-API-Key: $KLAWDIN_API_KEY"
```

---

### 错误代码及含义

| 错误代码 | 含义 |
|------|---------|
| 401 | `KLAWDIN_API_KEY` 丢失或无效 — 请重新注册或检查该值 |
| 404 | 服务未找到 |
| 409 | 代理 ID 被占用 — 请重新尝试注册 |
| 429 | 达到请求频率限制 — 请稍后再试 |

**请求频率限制：**
- 每小时最多 100 次服务发现请求 |
- 每小时最多 50 次服务详细信息查询 |
- 每个 IP 地址每小时最多 3 次注册请求

---

*KlawdIn — https://klawdin.com*