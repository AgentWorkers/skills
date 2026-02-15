---
name: HTTP
description: 正确使用 HTTP 协议，包括选择合适的方法（如 GET、POST 等）、状态码（如 200、404 等）、请求头（headers）以及缓存策略。
metadata: {"clawdbot":{"emoji":"🌐","os":["linux","darwin","win32"]}}
---

## 重定向（常被混淆的概念）

- **307** 与 **308**：两者都会保留请求的方法（method）。**307** 是临时重定向，**308** 是永久重定向，分别用于 POST/PUT 请求的重定向。
- **301**/**302** 可能会将请求方法从 POST 更改为 GET（这是浏览器的行为），但不要用于带有请求体的 API 重定向。
- 重定向响应中必须包含 `Location` 头部，且该地址应该是绝对路径；相对路径可能在旧版本的客户端中导致问题。
- 重定向循环应限制在 5-10 次以内，否则会导致客户端崩溃。

## 缓存策略

- 对于敏感数据，使用 `Cache-Control: no-store`（禁止缓存）——这类数据永远不会被写入磁盘。
- `no-cache` 仍然会缓存数据，但每次请求都会重新验证数据是否需要缓存。
- `private, max-age=0, must-revalidate` 用于用户特定的、需要始终保持最新状态的数据。
- `public, max-age=31536000, immutable` 用于版本控制的静态资源。
- 如果响应内容依赖于某些头部信息（如 `Accept-Encoding`、`Authorization`），则需要在响应头中设置 `Vary` 头部；忽略 `Vary` 头部会导致缓存失效。

## 条件请求

- **ETag** 与 **If-None-Match**：推荐用于 API 请求，因为它们基于内容的哈希值进行判断。
- **强 ETag**（如 `"abc"`）与 **弱 ETag**（如 `W/"abc"`）的区别在于：弱 ETag 允许返回语义上等效的响应。
- **If-Match** 用于实现乐观锁机制：如果资源自上次读取后发生了变化，则更新请求会失败。
- 当 **If-Match** 失败时，应返回 412（Precondition Failed），而不是 409（Conflict）。

## CORS 预检触发条件

- 任何非 `Accept`、`Accept-Language`、`Content-Language`、`Content-Type` 的自定义头部都会触发 CORS 预检。
- 如果请求方法为 PUT、DELETE 或 PATCH，即使请求来源相同，也会触发预检。
- 如果请求体类型不是 `application/x-www-form-urlencoded`、`multipart/form-data` 或 `text/plain`，也会触发预检。
- 可读的请求体（ReadableStream）也会触发预检。
- 预检结果的缓存时间由 `Access-Control-Max-Age` 头部控制，通常设置为 86400 秒以减少不必要的预检请求。

## 安全头部（必须设置）

- `Strict-Transport-Security: max-age=31536000; includeSubDomains`：启用 HSTS（HTTP Strict Transport Security），一旦设置很难撤销。
- `X-Content-Type-Options: nosniff`：防止 MIME 冒充攻击。
- `X-Frame-Options: DENY` 或 `SAMEORIGIN`：防止点击劫持（clickjacking）。
- `Content-Security-Policy`：虽然复杂但至关重要，建议从 “report-only” 模式开始配置。

## 范围请求（Range Requests）

- `Accept-Ranges: bytes` 表示支持范围请求，客户端可以请求部分内容。
- `Range: bytes=0-1023` 表示请求前 1024 字节的内容；`Range: bytes=-500` 表示请求最后 500 字节的内容。
- 当请求的范围无效时，应返回 416（Range Not Satisfiable）错误，并在响应中包含 `Content-Range` 头部（例如：`Content-Range: bytes */5000`）。

## 错误响应的最佳实践

- 使用结构化的 JSON 格式返回错误信息：`{"error": {"code": "VALIDATION_FAILED", "message": "...", "details": [...]}`。
- 在错误响应中包含请求 ID，以便于日志追踪。
- 在生产环境中不要泄露堆栈跟踪信息，仅返回通用错误信息。
- 对于违反业务规则的情况（如重复的电子邮件地址、资金不足等），应返回 409（Conflict），而不仅仅是 400（Bad Request）。

## 重试机制

- 默认情况下，只有幂等请求（如 GET、PUT、DELETE、HEAD）才会被重试。
- POST 请求需要使用幂等性标识符（`Idempotency-Key`，例如：`Idempotency-Key: <client-generated-uuid>`）来控制重试行为。
- 采用指数级退避策略（1秒、2秒、4秒、8秒……），并加入随机延迟，以防止大量请求同时发起。
- 遵循 `Retry-After` 头部的规定，该头部可以指定重试间隔时间（以秒或 HTTP 日期格式表示）。
- 设置合理的超时时间（通常为 30 秒），避免无限等待。

## 常被忽略的头部信息

- **Vary** 头部：必须包含所有会影响响应结果的头部信息；如果没有设置 `Vary: Origin`，CORS 请求将无法正常工作。
- `Content-Disposition: attachment; filename="report.pdf"` 用于指定下载文件的名称。
- 如果请求中未包含 `X-Request-ID`，则应生成该头部并将其传递给下游服务。
- `Accept-Language` 头部用于提供本地化响应，同时提供优雅的回退机制。

## 连接行为

- 在 HTTP/1.1 协议中，如果没有 `Content-Length` 或使用了 `Transfer-Encoding: chunked`，则响应结束后连接会被关闭。
- 在 HTTP/2 协议中，数据传输是分块的（chunked），此时无法设置 `Content-Length`。
- HTTP/2 是二进制流式传输，不会在请求头阶段造成阻塞。
- 要升级到 WebSocket，需要在请求中使用 `Connection: Upgrade` 和 `Upgrade: websocket` 头部。