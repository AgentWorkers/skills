---
name: zyla-api-hub-skill
description: **Zyla API Hub 技能——将您的 OpenClaw AI 代理转变为现实世界的操作工具。**  
借助 Zyla API Hub 提供的 10,000 多个可立即使用的 API，为您的 OpenClaw AI 代理增添强大功能：实时获取天气信息、金融数据、支持翻译服务、验证电子邮件地址、进行地理位置定位等。
metadata: {"openclaw":{"requires":{},"primaryEnv":"ZYLA_API_KEY","homepage":"https://zylalabs.com/openclaw/connect"}}
---

# Zyla API Hub 技能

将您的 OpenClaw AI 代理转变为一个能够处理实际任务的工具。通过 Zyla API Hub 提供的 10,000 多个可用于生产的 API，您可以轻松访问天气、金融、翻译、电子邮件验证、地理位置等信息。所有这些服务都可通过一个统一的 API 密钥进行访问，支持按使用量计费的模式，并且没有供应商锁定限制。

## 设置

如果 `ZYLA_API_KEY` 未配置，请指导用户完成以下操作：
1. 访问 https://zylalabs.com/openclaw/connect 以获取 API 密钥。
2. 或者，如果插件已安装，请运行 `/zyla connect`（系统会自动打开浏览器）。
3. 将获取到的 API 密钥添加到 `~/.openclaw/openclaw.json` 文件中的 `skills.entries.zyla-api-hub-skill.apiKey` 配置项中。

**注意**：切勿要求用户在聊天中直接输入 API 密钥，应引导他们通过配置文件进行设置，并在设置完成后确认密钥的有效性。

## 快速入门——热门 API

这些 API 可以直接使用，无需先在目录中搜索。每个 API 都包含了 API ID、端点详情和参数。

```markdown
<!-- POPULAR_APIS_START -->
<!-- 该部分由 npx tsx scripts/generate-popular.ts 自动生成 -->
<!-- 在发布前运行此命令，以便更新为最新的热门 API 列表（前 20 个） -->
```

### 按邮政编码查询天气的 API（ID：781）
- **使用场景**：用户查询特定邮政编码地区的天气、温度、天气预报或气候信息。
- **类别**：天气与环境
- **调用方式**：`npx tsx {baseDir}/scripts/zyla-api.ts call --api 781 --endpoint <endpoint_id> --params '{"zip":"10001"}`

### 货币转换 API（示例）
- **使用场景**：用户需要查询货币兑换率或进行外汇交易。
- **类别**：金融
- **调用方式**：`npx tsx {baseDir}/scripts/zyla-api.ts call --api <id> --endpoint <endpoint_id> --params '{"from":"USD","to":"EUR","amount":"100"}`

### 电子邮件验证 API（示例）
- **使用场景**：用户需要验证或检查电子邮件地址的有效性。
- **类别**：数据验证
- **调用方式**：`npx tsx {baseDir}/scripts/zyla-api.ts call --api <id> --endpoint <endpoint_id> --params '{"email":"test@example.com"}`

> **提示**：运行 `npx tsx {baseDir}/scripts/generate-popular.ts` 可以根据实时 API 目录重新生成此部分的列表，其中包含真实的 API ID 和端点信息。

<!-- POPULAR_APIS_END -->
```

## 查找其他 API

对于未在上述列表中的 API，您可以在目录中搜索相应的信息：

```bash
# Search by keyword
npx tsx {baseDir}/scripts/zyla-catalog.ts search "recipe"

# List APIs by category
npx tsx {baseDir}/scripts/zyla-catalog.ts list --category "Finance"

# Get endpoints for a specific API
npx tsx {baseDir}/scripts/zyla-catalog.ts endpoints --api 781
```

## 调用 API

### 推荐使用辅助脚本（推荐方式）

```bash
# Basic call
npx tsx {baseDir}/scripts/zyla-api.ts call \
  --api <api_id> \
  --endpoint <endpoint_id> \
  --params '{"key":"value"}'

# Specify HTTP method (default: GET)
npx tsx {baseDir}/scripts/zyla-api.ts call \
  --api <api_id> \
  --endpoint <endpoint_id> \
  --method POST \
  --params '{"key":"value"}'

# Get info about an API
npx tsx {baseDir}/scripts/zyla-api.ts info --api <api_id>

# Check health and remaining quota
npx tsx {baseDir}/scripts/zyla-api.ts health
```

### 备用方案：使用 curl

```bash
curl -H "Authorization: Bearer $ZYLA_API_KEY" \
  "https://zylalabs.com/api/{api_id}/{api_slug}/{endpoint_id}/{endpoint_slug}?param=value"
```

**API 调用格式**：`https://zylalabs.com/api/{api_id}/{api_name_slug}/{endpoint_id}/{endpoint_name_slug}`

- `api_id` 和 `endpoint_id` 是用于路由的数字 ID。
- `api_name_slug` 和 `endpoint_name_slug` 是更易于阅读的 URL 格式名称。

## 错误处理
- **401 Unauthorized**：API 密钥无效或已过期。请用户运行 `/zyla connect` 或访问 https://zylalabs.com/openclaw/connect 以获取新密钥。
- **403 Forbidden**：可能是订阅问题。按使用量计费的方案应能自动处理此类情况；如果问题持续存在，请用户联系技术支持。
- **429 Too Many Requests**：达到请求速率限制。请检查响应头中的 `X-Zyla-RateLimit-Minute-Remaining`，稍后重试。
- **404 Not Found**：API 或端点不存在。请使用目录验证相关 ID 的正确性。
- **5xx Server Error**：上游 API 出现问题。请稍后（2-5 秒后）重新尝试。

## 请求速率限制

所有 API 响应中都会包含以下头部信息：
- `X-Zyla-RateLimit-Minute-Limit`：每分钟的请求上限。
- `X-Zyla-RateLimit-Minute-Remaining`：当前分钟内剩余的请求次数。
- `X-Zyla-API-Calls-Monthly-Used`：本 billing cycle（计费周期）内的总调用次数。
- `X-Zyla-API-Calls-Monthly-Remaining`：本周期内剩余的调用次数。

## 计费方式
- **按使用量计费**：无需支付月费。每次 API 调用均按实际费率计费。
- 计费在每个计费周期结束时通过 Stripe 完成。
- 可通过运行 `npx tsx {baseDir}/scripts/zyla-api.ts health` 命令查看当前的使用情况。