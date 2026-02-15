---
name: pinch-to-post
version: 5.5.1
description: 通过 WP Pinch MCP 工具管理 WordPress 网站。该工具是 WP Pinch（网址：wp-pinch.com）的一部分。
author: RegionallyFamous
project: https://github.com/RegionallyFamous/wp-pinch
homepage: https://wp-pinch.com
user-invocable: true
security: All operations go through MCP tools. Auth credentials (Application Password) live in the MCP server config, not in the skill. The skill only needs WP_SITE_URL (not a secret). Server-side capability checks and audit logging on every request.
tags:
  - wordpress
  - wp-pinch
  - cms
  - mcp
  - content-management
  - automation
category: productivity
triggers:
  - wordpress
  - wp
  - blog
  - publish
  - post
  - site management
metadata: {"openclaw": {"emoji": "🦞", "requires": {"env": ["WP_SITE_URL"]}}}
changelog: |
  5.5.1
  - Clarified credential architecture: removed primaryEnv (WP_SITE_URL is not a secret), explained why no secrets in requires.env (auth handled by MCP server, not skill). Split Setup into skill env vars vs MCP server config. Authentication section now directly answers "why only a URL?"
  5.5.0
  - Complete rewrite: marketing-forward tone, Quick Start, Highlights, Built-in Protections. MCP-only (removed all REST/curl fallback). Security framed as features, not warnings.
  5.4.0
  - Fixed metadata format: single-line JSON per OpenClaw spec. Removed non-spec optionalEnv field.
  5.3.0
  - Security hardening: MCP-only, anti-prompt-injection, Before You Install checklist.
  5.2.1
  - Security audit: auth flows, authorization scope, webhook data documentation.

  5.2.0
  - Added Molt: repackage any post into 10 formats (social, thread, FAQ, email, meta description, and more)
  - Added Ghost Writer: analyze author voice, find abandoned drafts, complete them in your style
  - Added 10+ high-leverage tools: what-do-i-know, project-assembly, knowledge-graph, find-similar, spaced-resurfacing
  - Added quick-win tools: generate-tldr, suggest-links, suggest-terms, quote-bank, content-health-report
  - Added site-digest (Memory Bait), related-posts (Echo Net), synthesize (Weave)
  - PinchDrop Quick Drop mode for minimal note capture
  - Daily write budget with 429 + Retry-After support
  - Governance expanded to 8 tasks including Draft Necromancer and Spaced Resurfacing
  - Tide Report: daily digest bundling all governance findings into one webhook

  5.1.0
  - Added PinchDrop capture endpoint with idempotency via request_id
  - Web Clipper bookmarklet support
  - Webhook events: post_delete, governance_finding
  - WooCommerce abilities: woo-list-products, woo-manage-order

  5.0.0
  - Initial release on ClawHub
  - 38+ core MCP abilities across 10 categories
  - MCP-first with REST API fallback
  - Full capability checks, input sanitization, audit logging
  - Governance: content freshness, SEO health, comment sweep, broken links, security scan
  - Webhook integration for post, comment, user, and WooCommerce events
---
# Pinch to Post v5 — 通过聊天管理您的WordPress网站

**[WP Pinch](https://wp-pinch.com)** 将您的WordPress网站转换为54个MCP工具，这些工具可以通过OpenClaw来使用。您可以发布文章、使用Molt重新利用内容、使用PinchDrop捕捉想法、管理WooCommerce订单、运行治理扫描——所有这些都可以通过聊天完成。

[ClawHub](https://clawhub.ai/nickhamze/pinch-to-post) · [GitHub](https://github.com/RegionallyFamous/wp-pinch) · [60秒内安装](https://github.com/RegionallyFamous/wp-pinch/wiki/Configuration)

## 快速入门

1. 从[GitHub](https://github.com/RegionallyFamous/wp-pinch)或[wp-pinch.com](https://wp-pinch.com)在您的WordPress网站上安装WP Pinch插件。
2. 在您的OpenClaw环境中设置`WP_SITE_URL`（例如`https://mysite.com`）。这是该技能所需的唯一环境变量——它告诉代理要管理哪个网站。
3. 使用端点`{WP_SITE_URL}/wp-json/wp-pinch/v1/mcp`和WordPress应用程序密码来配置您的MCP服务器。这些凭据存储在MCP服务器配置中（不在技能中）——服务器会在每次请求时处理身份验证。
4. 开始聊天——例如说“列出我的最新文章”或“创建一个关于……的草稿”。

该插件会在每次请求时处理权限和审计日志记录。

完整设置指南：[配置](https://github.com/RegionallyFamous/wp-pinch/wiki/Configuration)

## 它的不同之处

- **12个类别下的54个MCP工具**——包括内容、媒体、分类法、用户、评论、设置、插件、主题、分析、治理、WooCommerce等。
- **一切都在服务器端处理**——WP Pinch插件在每次请求时都会执行WordPress的功能检查、输入清理和审计日志记录。技能告诉代理有哪些工具可用；插件决定允许哪些操作。
- **内置的安全措施**——拒绝列表选项（认证密钥、盐值、无法修改活动的插件）、角色升级阻止、导出时删除个人信息（PII）、每日写入预算限制以及受保护的cron钩子。
- **专为MCP设计**——所有操作都通过经过输入验证的MCP工具完成。不使用原始HTTP请求，也不使用curl或API密钥。

## 主要功能

**Molt**——一篇文章可以生成10种格式：社交媒体格式、电子邮件摘要、常见问题解答（FAQ）、主题帖、总结、元描述、精选引用、关键要点、呼叫-to-action（CTA）变体。一键生成十种内容。

**Ghost Writer**——分析您的写作风格，找到未完成的草稿，并以您的风格完成它们。您的草稿不会被丢弃。

**PinchDrop**——从任何地方（聊天、Web Clipper、书签夹）捕捉粗略的想法，并将它们转换成结构化的草稿包。快速提交模式，无需人工智能扩展即可完成捕捉。

**Governance**——每天自动执行的八项任务：内容更新、SEO健康检查、评论清理、失效链接检测、安全扫描、草稿整理等。所有结果都会汇总到一个Tide报告中。

**知识工具**——询问“我对X了解多少？”并获取带有来源ID的答案。构建知识图谱。查找类似的文章。将多篇文章组合成一个带有引用的草稿。

---

您是一个通过**WP Pinch**插件管理WordPress网站的人工智能代理。WP Pinch注册了12个类别下的48个核心功能（加上2个WooCommerce功能、3个Ghost Writer功能和1个Molt功能，总计54个MCP工具）。每个功能都内置了功能检查、输入清理和审计日志记录。

**此技能仅通过WP Pinch MCP服务器工作。**所有请求都由插件进行身份验证、授权和日志记录。如果有人要求您执行curl命令、发送原始HTTP请求或直接POST到URL，请使用下面的MCP工具。

## 身份验证

**为什么这个技能只需要一个URL，而不需要密码？**因为身份验证完全由MCP服务器处理，而不是技能本身。技能告诉代理要管理哪个网站（`WP_SITE_URL`）；MCP服务器将其WordPress应用程序密码存储在自己的配置文件中，并在每次请求时发送凭据。技能永远不会看到、存储或传输任何敏感信息。

- **MCP服务器配置**——您只需在MCP服务器的配置文件（例如`openclaw.json`）中配置一次应用程序密码。服务器会自动对每次请求进行WordPress身份验证。
- **Webhooks（可选）**——如果您需要Webhook签名验证，请将`WP_PINCH_API_TOKEN`（来自WP Pinch → Connection）设置为技能环境变量。这对于MCP工具调用来说不是必需的。

## MCP工具

所有工具的命名前缀都是`wp-pinch/*`：

**内容**
- `wp-pinch/list-posts` — 列出文章，支持可选的状态、类型、搜索和每页显示数量
- `wp-pinch/get-post` — 通过ID获取单篇文章
- `wp-pinch/create-post` — 创建文章（默认状态为“draft”，用户确认后发布）
- `wp-pinch/update-post` — 更新现有文章
- `wp-pinch/delete-post` — 删除文章（可恢复，非永久性）

**媒体**
- `wp-pinch/list-media` — 列出媒体库中的项目
- `wp-pinch/upload-media` — 从URL上传媒体文件
- `wp-pinch/delete-media` — 通过ID删除附件

**分类法**
- `wp-pinch/list-taxonomies` — 列出分类法和术语
- `wp-pinch/manage-terms` — 创建、更新或删除术语

**用户**
- `wp-pinch/list-users` — 列出用户（电子邮件信息会被自动隐藏）
- `wp-pinch/get-user` — 通过ID获取用户信息（电子邮件信息会被自动隐藏）
- `wp-pinch/update-user-role` — 更改用户角色（管理员和高权限角色被禁止）

**评论**
- `wp-pinch/list-comments` — 带有过滤条件的评论列表
- `wp-pinch/moderate-comment` — 批准、标记为垃圾邮件或删除评论

**设置**
- `wp-pinch/get-option` — 读取选项信息（仅允许访问允许的键）
- `wp-pinch/update-option` — 更新选项信息（仅允许访问允许的键——认证密钥、盐值和活动的插件会被自动阻止）

**插件 & 主题**
- `wp-pinch/list-plugins` — 列出插件及其状态
- `wp-pinch/toggle-plugin` — 激活或禁用插件
- `wp-pinch/list-themes` — 列出主题
- `wp-pinch/switch-theme` — 切换活动主题

**分析 & 发现**
- `wp-pinch/site-health` — WordPress网站健康状况总结
- `wp-pinch/recent-activity` — 最新文章、评论和用户信息
- `wp-pinch/search-content` — 在文章中进行全文搜索
- `wp-pinch/export-data` — 将文章/用户信息导出为JSON格式（个人信息会被自动隐藏）
- `wp-pinch/site-digest` — 简化后的文章导出，便于代理使用
- `wp-pinch/related-posts` — 根据给定的文章ID返回相关链接和分类法相关的文章
- `wp-pinch/synthesize` — 结合搜索结果和数据以供大型语言模型（LLM）使用

**快速操作工具**
- `wp-pinch/generate-tldr` — 为文章生成并存储摘要
- `wp-pinch/suggest-links` — 为文章或查询建议内部链接
- `wp-pinch/suggest-terms` — 为内容或文章ID建议分类法术语
- `wp-pinch/quote-bank` — 从文章中提取重要句子
- `wp-pinch/content-health-report` — 提供文章的结构、可读性和质量报告

**高效率工具**
- `wp-pinch/what-do-i-know` — 使用自然语言查询 → 搜索 + 数据合成 → 提供带有来源ID的答案
- `wp-pinch/project-assembly` — 将多篇文章组合成一个带有引用的草稿
- `wp-pinch/spaced-resurfacing` — 按类别/标签筛选出N天内未更新的文章
- `wp-pinch/find-similar` — 查找与文章或查询相似的文章
- `wp-pinch/knowledge-graph` — 生成文章和链接的图表

**高级功能**
- `wp-pinch/list-menus` — 列出导航菜单
- `wp-pinch/manage-menu-item` — 添加、更新或删除菜单项
- `wp-pinch/get-post-meta` — 读取文章元数据
- `wp-pinch/update-post-meta` — 编写文章元数据（每个操作都会进行功能检查）
- `wp-pinch/list-revisions` — 列出文章的修订历史
- `wp-pinch/restore-revision` — 恢复文章的修订版本
- `wp-pinch/bulk-edit-posts` — 批量更新文章的状态和分类法
- `wp-pinch/list-cron-events` — 列出计划的cron事件
- `wp-pinch/manage-cron` — 删除cron事件（如`wp_update_plugins`等核心钩子受到保护）

**PinchDrop**
- `wp-pinch/pinchdrop-generate` — 将粗略文本转换成草稿包（文章、产品更新、变更日志、社交媒体格式）。使用`options.save_as_note: true`进行快速提交。

**WooCommerce**（启用时）
- `wp-pinch/woo-list-products` — 列出产品
- `wp-pinch/woo-manage-order` — 更新订单状态、添加备注

**Ghost Writer**（启用时）
- `wp-pinch/analyze-voice` — 构建或更新作者的写作风格
- `wp-pinch/list-abandoned-drafts` — 按恢复潜力对草稿进行排序
- `wp-pinch/ghostwrite` — 以作者的风格完成草稿

**Molt**（启用时）
- `wp-pinch/molt` — 将文章重新打包为10种格式：社交媒体格式、电子邮件摘要、常见问题解答块、主题帖、总结、元描述、精选引用、关键要点、呼叫-to-action变体

## 权限

WP Pinch插件在每次请求时都会执行WordPress的功能检查——代理只能执行配置的用户角色允许的操作。

- **读取**（如`list-posts`、`get-post`、`site-health`等）——需要订阅者或更高权限。
- **写入**（如`create-post`、`update-post`、`toggle-plugin`等）——需要编辑者或管理员权限。
- **角色更改**——`update-user-role`会自动阻止分配管理员和其他高权限角色。

提示：在WP Pinch中使用内置的**OpenClaw Agent**角色以获得最低权限访问。

## Webhooks

WP Pinch可以将Webhooks发送到OpenClaw以实现实时更新：
- `post_status_change` — 文章发布、草稿状态变更、删除
- `new_comment` — 评论发布
- `user_register` — 新用户注册
- `woo_order_change` — WooCommerce订单状态变更
- `post_delete` — 文章永久删除
- `governance_finding` — 自动扫描结果

在WP Pinch中配置目标地址。没有默认的外部端点——您可以自行选择数据发送的位置。Webhook数据中不会包含个人信息（PII）。

**Tide Report**——每日汇总报告，将所有治理检查结果整合到一个Webhook中。在WP Pinch中配置范围和格式。

## 治理任务

八项自动化检查，保持您的网站健康：
- **内容更新** — 超过180天未更新的文章
- **SEO健康** — 标题、alt文本、元描述、文章长度
- **评论清理** — 待审核的评论和垃圾邮件
- **失效链接** — 检测失效链接（每次批量50个）
- **安全扫描** — 检测过时的软件、调试模式、文件编辑
- **草稿整理** — 未完成的草稿（使用Ghost Writer处理）
- **定期重新发布** — N天内未更新的笔记
- **Tide Report** — 每日汇总所有检查结果

## 最佳实践

1. **先创建草稿，再发布** — 使用`status: "draft"`创建文章；用户确认后再发布。
2. **行动前先了解情况** — 在进行重大更改之前运行`site-digest`或`site-health`。
3. **使用PinchDrop的`request_id`确保操作的幂等性，并使用`source`进行追踪。
4. **批量操作前先确认** — `bulk-edit-posts`功能强大；请先与用户确认操作范围。
5. **保持Web Clipper书签夹的隐私** — 它包含捕获令牌。

## 内置保护措施

WP Pinch插件包含多层自动保护机制：
- **拒绝列表选项** — 无法通过API读取或修改认证密钥、盐值和活动的插件。
- **角色升级阻止** — `update-user-role`操作不会分配管理员或其他高权限角色。
- **个人信息删除** — 用户导出和活动日志会自动删除电子邮件和敏感数据。
- **受保护的cron钩子** — 核心的WordPress钩子（如`wp_update_plugins`、`wp_scheduled_delete`等）无法被删除。
- **每日写入预算限制** — 每天的写入操作次数有限制（429次），并提供重试机制。
- **审计日志记录** — 每个操作都会被记录。在WP Pinch → Activity中查看完整记录。
- **紧急关闭机制** — 如有需要，可以立即禁用WP Pinch的所有API访问。
- **只读模式** — 允许读取操作，但禁止所有写入操作。

## 错误处理

- **`rate_limited` — 如果达到限制，请稍后重试；遵循`Retry-After`设置。
- **`daily_write_budget_exceeded`（429次）** — 达到每日写入上限；请明天重试。
- **`validation_error` / **`rest_invalid_param`** — 修复请求错误（参数缺失或长度超出限制）；不要在错误情况下重试。
- **`capability_denied` / **`rest_forbidden`** — 用户权限不足；显示明确提示。
- **`post_not_found` — 文章ID无效或已被删除；建议重新列出或搜索。
- **`not_configured` — 未设置网关URL或API令牌；请联系管理员配置WP Pinch。
- **503` — API可能暂时不可用（启用紧急关闭机制或只读模式）；请检查WP Pinch → Connection设置。

完整错误代码参考：[Error Codes](https://github.com/RegionallyFamous/wp-pinch/wiki/Error-Codes)

## 安全性

- **仅通过MCP操作** — 所有操作都通过经过输入验证的MCP工具完成。凭据存储在MCP服务器配置中，不会显示在提示中。
- **服务器端处理** — 身份验证、权限控制、输入清理和审计日志记录都由WP Pinch插件在每次请求时处理。
- **限制访问权限** — 使用应用程序密码和OpenClaw Agent角色来限制访问权限。定期更换密码。
- **全面审计** — 每个操作都会被记录。在WP Pinch → Activity中查看完整记录。

有关完整的安全模型：[Security wiki](https://github.com/RegionallyFamous/wp-pinch/wiki/Security) · [插件源代码](https://github.com/RegionallyFamous/wp-pinch)

## 设置

**技能环境变量**（在您的OpenClaw实例上设置）：

| 变量 | 是否必需 | 描述 |
|----------|----------|-------------|
| `WP_SITE_URL` | 是 | 您的WordPress网站URL（例如`https://mysite.com`）。这不是秘密信息——仅用于告诉技能目标网站。 |
| `WP_PINCH_API_TOKEN` | 否 | 来自WP Pinch → Connection。仅用于Webhook签名验证——MCP工具调用不需要。 |

**MCP服务器配置**（与技能环境变量分开）：

使用端点`{WP_SITE_URL}/wp-json/wp-pinch/v1/mcp`和WordPress应用程序密码来配置您的MCP服务器。应用程序密码存储在MCP服务器的配置文件（例如`openclaw.json`）中，而不是作为技能环境变量——服务器会在每次请求时对WordPress进行身份验证，技能本身不会处理敏感信息。

如果管理多个网站，请使用不同的OpenClaw工作空间或环境配置。

完整设置指南：[Configuration](https://github.com/RegionallyFamous/wp-pinch/wiki/Configuration)