---
name: useclick-link-shortening-analytics
description: >
  **具备计划意识的使用**  
  利用 UseClick 的链接缩短功能及分析 API，可处理地理链接、联盟链接、链接管理、二维码生成以及自定义/品牌化域名相关操作。当用户希望将 UseClick 集成到代码中、自动化流程或人工智能代理中时，这些功能非常实用——例如用于创建/管理短链接、获取点击分析数据、配置地理定位设置，或将功能可用性与价格层级关联起来。此外，在构建仪表盘或进行生产环境集成之前，如果用户需要了解受计划限制的功能的相关升级信息，这些 API 也能提供必要的帮助。
---
# UseClick.io：链接缩短与分析服务

为 UseClick API 用户提供准确、基于计划限制的集成指导。

## 快速入门流程

1. 确认用户拥有 UseClick 账户及 API 密钥（可在 `/dashboard/account/api-keys` 获取）。
2. 使用基础 URL `https://useclick.io/api/v1`。
3. 通过 `Authorization: Bearer uc_live_...` 头部信息进行身份验证。
4. 首先使用 `GET /auth/verify` 核对用户凭据。
5. 根据 `references/api.md` 中提供的端点来构建集成工作流程。
6. 在建议使用高级功能之前，请先查阅 `references/pricing-and-limits.md` 以了解计划限制和功能可用性。

## 响应与错误处理规则

1. 优先参考 `references/api.md` 中定义的、与后端一致的响应格式，而非营销宣传内容。
2. 将非 2xx 状态码视为需要处理的错误：
   - `401 UNAUTHORIZED`：API 密钥无效或缺失。
   - `403 FEATURE_NOT_AVAILABLE`：请求的功能需要更高级别的计划。
   - `403 LINK_LIMIT_REACHED`：用户已达到其计划允许的链接使用上限。
   - `400 SLUG_ALREADY_EXISTS` 或 `400 RESERVED_SLUG`：链接 slug 冲突或已被预留。
   - `429 RATE_LIMIT_EXCEEDED`：达到速率限制，请使用 `X-RateLimit-Reset` 重试。
3. 提及可用的速率限制相关头部信息：
   - `X-RateLimit-Limit`
   - `X-RateLimit-Remaining`
   - `X-RateLimit-Reset`

## 基于计划的指导原则

1. 在提供实施步骤之前，务必将用户请求的操作与相应的计划限制进行匹配。
2. 如果请求的功能不在当前计划范围内，提供两种解决方案：
   - 使用当前计划的兼容替代方案。
   - 通过 `https://useclick.io/pricing` 进行升级。
3. 明确说明：所有计划都支持 API 访问，但功能的使用仍受计划限制的约束。

## 工作流程模板

除非用户另有要求，否则请遵循以下默认流程：

1. **链接创建流程**：
   - 验证 API 密钥。
   - 先创建仅包含基本参数（`target_url`，可选 `slug`）的链接。
   - 仅在计划支持的情况下添加高级功能字段。
2. **链接管理流程**：
   - 分页显示链接列表。
   - 通过 slug 查读特定链接。
   - 安全地更新可修改的链接字段。
   - 根据请求删除链接。
3. **分析流程**：
   - 分页获取链接点击数据。
   - 可选地按 `link Slug` 进行过滤。
   - 在客户端汇总数据以供仪表盘使用。
4. **地理定位流程**：
   - 确认用户使用的是 Starter+ 计划。
   - 读取现有的地理定位规则。
   - 使用大写的 ISO-2 国家代码创建针对特定国家的规则。
   - 通过 `country_code` 查询参数删除链接。

## 准确性保障措施

1. 不要自行创建新的端点、参数或响应字段。
2. 默认情况下不声明支持 `Retry-After` 功能；请依赖 `X-RateLimit-Reset` 机制进行重试。
3. 在发现文档内容与后端实际行为不一致时，及时进行说明并遵循后端的实际处理方式。
4. 提供可用的实现指导，必要时提供 cURL 示例或代码片段。

## 参考资源

- API 接口规范及示例：`references/api.md`
- 价格层级、限制及升级规则：`references/pricing-and-limits.md`
- 可复用的集成模板：`references/workflows.md`
- 市场发布检查清单：`references/clawhub-publish.md`