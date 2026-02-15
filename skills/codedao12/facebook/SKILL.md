---
name: facebook
description: OpenClaw技能：用于Facebook Graph API工作流程，专注于通过直接HTTPS请求进行页面发布、评论操作以及页面管理。
---

# Facebook Graph API 技能（高级）

## 目的
提供一份面向生产环境的指南，用于使用 Facebook Graph API 构建页面（Pages）的相关工作流程：发布帖子、管理评论以及通过直接的 HTTPS 请求安全地操作页面内容。

## 适用场景
- 需要实现页面发布和评论管理功能。
- 希望获得专业的命令设计及安全的操作指导。
- 更倾向于使用直接的 HTTP 请求而非 SDK。

## 不适用场景
- 需要使用高级广告或营销 API。
- 必须使用复杂的基于浏览器的 OAuth 流程。

## 快速入门
- 阅读 `references/graph-api-overview.md` 以了解基础 URL、版本和请求模式。
- 阅读 `references/page-posting.md` 以了解页面发布的工作流程及相关字段。
- 阅读 `references/comments-moderation.md` 以了解评论操作和审核流程。
- 阅读 `references/permissions-and-tokens.md` 以了解访问类型和权限范围。
- 阅读 `references/webhooks.md` 以了解订阅和验证步骤。
- 阅读 `references/http-request-templates.md` 以了解具体的 HTTP 请求格式。

## 必需输入
- Facebook 应用程序 ID 和应用程序密钥（App ID and App Secret）。
- 目标页面 ID（Target Page ID）。
- 令牌策略：用户令牌 → 页面访问令牌（Token strategy: user token → Page access token）。
- 所需的权限及审核状态（Required permissions and review status）。

## 预期输出
- 明确的页面工作流程计划、权限检查清单以及操作规范。

## 操作注意事项
- 仅使用最低权限级别的权限（Use least-privilege permissions）。
- 处理请求速率限制和重试机制（Handle rate limits and retries）。
- 仅记录必要的标识符（Log minimal identifiers）。

## 安全注意事项
- 绝不要记录令牌或应用程序密钥（Never log tokens or app secrets）。
- 验证 Webhook 签名（Validate webhook signatures）。