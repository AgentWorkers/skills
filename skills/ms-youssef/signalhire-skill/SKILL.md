---
name: signalhire
description: 通过 SignalHire API 寻找并丰富联系人信息（搜索、人员详情及信用记录）
metadata:
  openclaw:
    # The skill only loads when a valid API key and callback URL are provided.  The
    # primary environment variable is used to inject the secret without ever
    # exposing it in the instructions.  The callback URL should point to the
    # connector service exposed publicly via a tunnel or reverse proxy.
    requires:
      env: SIGNALHIRE_API_KEY,SIGNALHIRE_CALLBACK_URL
    primaryEnv: SIGNALHIRE_API_KEY
---

# SignalHire 技能说明

这些技能为 OpenClaw 代理提供了三项高级功能。每项功能对应 SignalHire 文档中记录的一个 REST 端点。代理 **严禁** 直接调用这些端点，而应使用定义好的技能动作来执行相应的操作。以下内容总结了 API 的工作原理，包括速率限制、并发限制以及异步回调的工作流程。所有描述均基于 SignalHire 官方 API 文档。

## 1. 查看剩余信用额度

使用此动作可查询账户剩余的信用额度。SignalHire API 提供了一个专门的端点 `GET /api/v1/credits`，该端点会以 JSON 格式返回可用信用额度的数量。请求头中必须包含有效的 API 密钥。成功调用后，响应中会包含一个名为 `credits` 的字段，显示剩余的信用额度【821841938681143†L505-L529】。如果账户配置为“无联系人的资料”，可以使用 `withoutContacts=true` 的查询参数来调用相同的端点【821841938681143†L559-L566】。在每次调用 Person API 时，信用额度也会通过 `X-Credits-Left` 响应头返回【821841938681143†L559-L566】。

在启动大型数据 enrichment（丰富处理）任务之前，**必须** 先调用此动作，以避免在操作过程中信用额度耗尽。如果剩余信用额度少于需要处理的资料数量，应优雅地拆分或中止任务。

## 2. 搜索候选人资料

使用此动作可在 SignalHire 数据库中查找潜在候选人，且不会消耗信用额度。搜索 API 的端点是 `POST /api/v1/candidate/searchByQuery`【21055727237259†L100-L109】，它会返回候选人资料的摘要列表以及一个 `scrollId`。可以通过 `Scroll Search` 端点（此处未展示）来获取更多页面，直到所有结果都被获取完毕。只有联系 SignalHire 支持人员后才能使用搜索 API，且同时进行的请求数量受到严格限制，最多为 **三个**【21055727237259†L110-L116】。代理必须确保任何时候同时进行的 `searchByQuery` 请求数量不超过三个。

执行搜索时，请求体中应包含 `currentTitle`、`location`、`keywords`、`industry` 等字段（具体详见文档【21055727237259†L120-L177】）。`size` 参数用于控制每页返回的资料数量（默认为 10 个，最大为 100 个）。获取第一页结果后，代理应在 15 秒内立即发送滚动请求，以避免 `scrollId` 过期。搜索响应是同步的，会立即返回；无需回调。

## 3. 丰富联系人资料（Person API）

此动作可检索最多 100 个联系人的完整信息（包括电子邮件、电话号码和社交资料）。端点是 `POST /api/v1/candidate/search`【821841938681143†L126-L134】。每个联系人信息可以是 LinkedIn 资料链接、电子邮件地址、电话号码或 SignalHire 资料 UID【821841938681143†L120-L124】。请求体中 **必须** 包含一个 `callbackUrl` 参数；数据处理完成后，API 会将结果发送到该 URL【821841938681143†L126-L134】。监听该回调 URL 的服务器必须返回 HTTP 状态码 200 以确认收到数据。如果无法到达回调端点或在十秒内没有响应，SignalHire 会尝试重试最多三次【821841938681143†L187-L198】。只有当所有回调数据都被接收后，处理才算完成。

回调数据中包含一个对象数组，每个对象都有一个 `status` 字段，表示处理结果：`success`、`failed`、`credits_are_over`、`timeout_exceeded` 或 `duplicate_query`【821841938681143†L239-L249》。当状态为 `success` 时，回调数据中还会包含一个 `candidate` 对象，其中包含 `fullName`、`emails`、`phones`、`location` 等字段。这些结果会被连接器服务保存到 CSV 文件中；代理应在连接器报告任务完成后再处理这些数据。

Person API 也受到速率限制：每分钟最多只能处理 **600 个元素**【821841938681143†L490-L503】。代理必须实施节流机制，确保所有 Person API 请求的总处理数量不超过此限制。超出限制的请求将被拒绝，并返回 HTTP 状态码 429（“Too Many Requests”【821841938681143†L500-L503】）。为提高处理效率，每次请求可以批量处理最多 100 个元素，但总处理数量不得超过每分钟的限制。

## 代理的通用指导原则

1. **不要硬编码 API 密钥或回调 URL**。使用 OpenClaw 提供的环境变量：`SIGNALHIRE_API_KEY` 进行身份验证，使用 `SIGNALHIRE Callback_URL` 进行 Person API 的调用。这些值是在运行时提供的，严禁泄露。

2. **在启动大型数据丰富处理任务之前，务必检查剩余信用额度**。如果信用额度不足，应中止或拆分任务。

3. **遵守速率和并发限制**。同时进行的 Search API 请求数量不得超过三个【21055727237259†L110-L116】；每分钟通过 Person API 处理的元素数量不得超过 600 个【821841938681143†L490-L503】。对于收到 HTTP 状态码 429 的响应，应实施指数级退避策略。

4. **调用 Person API 时，务必提供有效的回调 URL**，并确保连接器服务可用且响应迅速。回调必须在十秒内返回 HTTP 状态码 200，否则结果将被丢弃【821841938681143†L187-L198】。

5. **等待任务完成**。提交 Person API 请求后，代理应轮询连接器提供的任务端点（详见 README 文件），直到收到所有结果。只有在确认所有结果都被接收后，才能继续处理 CSV 数据。

6. **处理回调返回的所有状态码**。对于 `failed`、`credits_are_over`、`timeout_exceeded` 和 `duplicate_query` 状态，将无法获取候选人资料；记录这些情况并继续执行后续操作。

7. **遵守法律和隐私规定**。SignalHire 的 API 使用受其服务条款、隐私政策及 GDPR 规定的约束。在存储或使用联系人数据时，必须尊重数据主体的权利并遵守退出选项【821841938681143†L559-L566】。

遵循以上指导原则，代理可以安全地将 SignalHire 的搜索和数据丰富功能集成到 OpenClaw 的工作流程中。