---
name: CORS
description: 正确配置跨源资源共享（Cross-Origin Resource Sharing, CORS），以避免安全问题和调试麻烦。
metadata: {"clawdbot":{"emoji":"🔀","os":["linux","darwin","win32"]}}
---

## 预检触发条件（Preflight Triggers）

- 以下请求头不被允许：Accept、Accept-Language、Content-Language、Content-Type（某些情况下允许）；
- Content-Type 必须为 `application/x-www-form-urlencoded`、`multipart/form-data` 或 `text/plain`；
- 请求方法不能为 PUT、DELETE、PATCH 或任何自定义方法；
- 请求体中包含 `ReadableStream`；
- XMLHttpRequest.upload 事件监听器被触发；
- 一个触发条件即表示需要进行预检；简单的请求会直接跳过 OPTIONS 请求。

## 凭据模式（Credentials Mode）

- `Access-Control-Allow-Origin: *` 与使用凭证不兼容——必须指定具体的来源域名；
- 如果需要使用 cookies 或认证信息，必须设置 `Access-Control-Allow-Credentials: true`；
- 使用 Fetch API 时，设置 `credentials: 'include'`；使用 XMLHttpRequest 时，设置 `withCredentials = true`；
- 在不使用凭证的模式下，即使请求来自同一来源域名，也不会发送 cookies。

## 星号（*）的局限性

- 星号（*）不能匹配子域名（例如，`*.example.com` 是无效的）；
- 不能在需要使用凭证的情况下使用星号（*）——必须根据请求动态指定来源域名；
- `Access-Control-Allow-Headers: *` 在大多数浏览器中可用，但并非所有浏览器都支持——为确保兼容性，请明确列出允许的请求头；
- `Access-Control-Expose-Headers: *` 也存在类似问题——需要明确列出需要暴露的请求头。

## 来源域名验证（Origin Validation）

- 需要将 `Origin` 请求头与允许列表进行匹配——切勿盲目信任请求头（存在安全风险）；
- 正则表达式匹配可能存在问题（例如，`example.com` 可能匹配到 `evilexample.com`）——请确保模式匹配准确；
- 如果 `Origin` 请求头为空，通常会拒绝此类请求（尤其是来自沙箱环境或 file:// 协议的请求）；
- 如果请求头缺失，需要根据请求的来源域名或客户端类型进行特殊处理。

## Vary 请求头（Critical）

- 当响应内容依赖于请求来源域名时，必须包含 `Vary: Origin` 请求头；
- 如果不包含 `Vary: Origin`，CDN 或代理服务器可能会将响应缓存到某个来源域名，导致其他来源的请求出现问题（违反 CORS 规则）；
- 为了确保预检缓存的正确性，还应添加 `Vary: Access-Control-Request-Headers` 和 `Vary: Access-Control-Request-Method` 请求头。

## 可暴露的请求头（Exposed Headers）

- 默认情况下，JavaScript 只能读取 `Cache-Control`、`Content-Language`、`Content-Type`、`Expires`、`Last-Modified` 和 `Pragma` 等请求头；
- 自定义请求头在未被 `Access-Control-Expose-Headers` 列出时对 JavaScript 是不可见的；
- 如 `X-Request-ID`、`X-RateLimit-*` 等请求头，需要明确设置才能被 JavaScript 读取。

## 预检缓存（Preflight Caching）

- `Access-Control-Max-Age` 的值为 86400 秒（24 小时），可显著减少 OPTIONS 请求的频率；
- Chrome 浏览器的缓存时长上限为 2 小时，Firefox 浏览器为 24 小时——超过这个时间的值会被自动缩短；
- 缓存是针对每个来源域名、URL 和请求特性单独进行的，而不是全局缓存；
- 在开发阶段可以将缓存时长设置为 0 或省略该字段——这样可以避免缓存配置的变更被意外应用。

## 调试（Debugging）

- 如果在浏览器中看到 CORS 错误，说明请求已经到达服务器并返回了响应——请查看服务器日志；
- 如果预检失败，服务器应在返回 OPTIONS 请求时附带 CORS 相关的响应头（状态码为 2xx）；否则（状态码为 404/500），表示预检失败；
- 如果使用 `mode: 'no-cors` 进行请求，虽然请求可以成功，但响应内容可能为空——这通常不是预期的结果；
- 网络标签页会显示 CORS 错误信息，控制台则会显示具体缺失了哪些请求头。

## 常见的服务器错误（Common Server Mistakes）

- 仅在主处理程序中设置 CORS 请求头，而忽略了 OPTIONS 请求——这会导致预检失败；
- 在错误响应之后才设置 CORS 请求头——这会导致 4xx/5xx 状态码的请求缺少 CORS 请求头，从而影响错误处理；
- 代理服务器可能会删除请求头——请确认请求头确实被发送到了客户端；
- `Access-Control-Allow-Origin: *"https://example.com"` 的写法是错误的——应该使用单一的来源域名，而不是列表形式。

## 安全性（Security）

- 切勿盲目信任 `Origin` 请求头——请先将其与允许列表进行匹配；
- 如果需要从公共网络访问本地服务器（localhost），Chrome 浏览器要求设置 `Access-Control-Allow-Private-Network: true`；
- CORS 仅阻止响应的读取，并不阻止请求的发送——服务器仍然会处理请求；
- 对于敏感的 API，不要仅依赖 CORS；建议结合身份验证和 CSRF 令牌来增强安全性。