---
name: Analytics
description: 使用正确的 API 模式、速率限制以及 GDPR 合规性来部署以隐私保护为首要目标的分析系统。
---

## 关键实施注意事项

### Umami API 时间戳：
- 使用毫秒作为时间戳单位，而非秒。在 JavaScript 中使用 `Date.now()`；在 Python 中使用 `int(time.time() * 1000)`。

### Plausible API v2：
- 需要 `site_id` 参数，而非域名。请先从仪表板 URL 中获取 `site_id`。

### PostHog 事件：
- 事件属性必须能够被 JSON 序列化。切勿传递 DOM 元素或函数。

### 速率限制：
- Umami：每小时 600 次请求；
- Plausible：每小时 600 次请求；
- PostHog：每分钟 1000 次请求。当遇到 429 错误时，应实施指数退避策略（exponential backoff）。

## 环境特定设置

### 开发环境：
- 始终为本地测试使用单独的项目/站点。生产环境中的数据污染是不可逆的。

### 跟踪域名：
- 严禁在代码中硬编码域名。请使用环境变量来切换开发环境（localhost）和生产环境。

### 机器人过滤：
- 请在设置中启用机器人过滤功能。虽然隐私工具的机器人检测能力不如 Google Analytics 强，但仍需进行过滤。

## GDPR 合规性注意事项

- 即使对于以隐私保护为首要目标的工具，欧盟用户也需要明确同意才能被跟踪。
- 在进行数据跟踪之前，请检查用户的 IP 地理位置。

### 数据保留：
- 设置数据自动删除规则：
  - Umami：在设置 > 数据（Settings > Data）中配置；
  - Plausible：数据保留最多 30 天；
  - PostHog：在项目设置中配置。

### 无 cookie 警告：
- Umami 和 Plausible 不使用 cookie，但在收集用户标识符时仍需获得欧盟用户的同意。

## 运行时安全

- 在发送事件之前，请验证脚本是否已正确加载，并检查是否存在 `umami`、`plausible` 或 `posthog` 全局变量。

- **严禁在自定义事件中跟踪个人身份信息（PII）**，如电子邮件、姓名、IP 地址等，这违反了隐私保护原则。

- **PostHog 事件批量处理**：请通过 `/batch` 端点批量发送事件。Umami 和 Plausible 需要单独发送每个事件。

## 认证方式：

- **API 密钥的存储**：
  - 仅将 API 密钥存储在环境变量中，切勿硬编码。

- **Umami**：需要网站 ID 和 API 密钥的组合。

- **Plausible**：使用 bearer token 进行认证。

- **PostHog**：使用特定于项目的 API 密钥进行认证。