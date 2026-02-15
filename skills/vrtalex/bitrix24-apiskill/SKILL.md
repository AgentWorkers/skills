---
name: bitrix24-agent
description: 设计、实现、调试并优化 AI 代理与 Bitrix24 REST API 之间的集成（包括 Webhook、OAuth 2.0、权限范围、事件处理、批量操作等功能）。当需要将 AI 助手/代理连接到 Bitrix24、自动化 CRM 任务/聊天流程、处理 Bitrix24 发生的事件时，可运用这些技术；同时，还需要负责选择合适的认证模型，并解决 Bitrix24 API 相关的错误及性能问题。
---

# Bitrix24 代理（高效且可靠）

使用此技能以最少的令牌使用量实现正确的 Bitrix24 集成。

## 默认模式：高效（Lean）

除非用户要求详细信息，否则遵循以下限制：

- 在执行第一个可操作步骤之前，最多加载 2 个参考文件。
- 从 `references/packs.md` 开始。
- 仅打开一个目标文件：`references/catalog-<pack>.md`。
- 仅在用户请求工作流程/链（workflow/chain）时，才打开 `references/chains-<pack>.md`。
- 仅在需要了解认证架构、权限限制、事件可靠性或遇到未知错误时，才打开 `references/bitrix24.md`。

响应格式限制：

- 使用简洁的输出（目标 + 下一步操作 + 一个命令）。
- 不要重复文档内容。
- 除非明确请求，否则不要输出大量 JSON 数据。
- 避免重复已提供的指导信息；仅返回变更内容。

## 路由工作流程（Routing Workflow）

1. 确定用户意图：
- 方法调用（method call）
- 故障排除（troubleshooting）
- 架构决策（architecture decision）
- 事件/可靠性设置（event/reliability setup）

术语标准化（产品词汇）：

- “collabs”、“workgroups”、“projects”、“social network groups” -> `collab`（以及用于 Scrum 的 `boards`）。
- “Copilot”、“CoPilot”、“BitrixGPT”、“AI prompts” -> `platform`（`ai.*`）。
- “open lines”、“contact center connectors”、“line connectors” -> `comms`（`imopenlines.*`, `imconnector.*`）。
- “feed”、“live feed”、“news feed” -> `collab`（`log.*`）。
- “sites”、“landing pages”、“landing” -> `sites`（`landing.*`）。
- “booking”、“calendar”、“work time”、“time tracking” -> `services`（`booking.*`, `calendar.*`, `timeman.*`）。
- “orders”、“payments”、“catalog”、“products” -> `commerce`（`sale.*`, `catalog.*`）。
- “consents”、“consent”、“e-signature”、“sign” -> `compliance`（`userconsent.*`, `sign.*`）。

2. 快速选择认证方式：
- 单一门户/内部系统：使用 Webhook。
- 多门户/生命周期功能：使用 OAuth。

3. 选择最基本的插件包（packs）：
- 默认使用 `core` 包。
- 仅添加所需的插件包：`comms`, `automation`, `collab`, `content`, `boards`, `commerce`, `services`, `platform`, `sites`, `compliance`, `diagnostics`。

4. 在执行操作时遵循安全规则：
- 首选使用 `scripts/bitrix24_client.py` 和 `scripts/offline_sync_worker.py`；
- 强制使用允许列表（allowlist），并添加 `--confirm-write` 或 `--confirm-destructive` 参数；
- 尽可能确保写操作是幂等的（idempotent）。

5. 仅在出现以下情况时才深入参考详细信息：
- `WRONG_AUTH_TYPE`（认证类型错误）、`insufficient_scope`（权限不足）、`QUERY_LIMIT_EXCEEDED`（查询次数超出限制）、`expired_token`（令牌过期）；
- 离线事件丢失问题；
- OAuth 刷新过程中的竞争问题或租户隔离问题。

## 质量保障规则（Quality Guardrails）

- 绝不要泄露 Webhook/OAuth 密钥。
- 权限范围必须最小化。
- 禁止使用嵌套的批量操作（nested batches）。
- 在线事件的传递不保证成功；对于无丢失要求的处理，使用离线流程。
- 在兼容的情况下优先使用 REST 3.0；必要时回退到 REST 2.0。

## 参考文件加载结构（Reference Loading Map）

- `references/packs.md`：包含插件包及其加载策略。
- `references/catalog-<pack>.md`：提供方法列表。
- `references/chains-<pack>.md`：介绍实现流程。
- `references/bitrix24.md`：仅在需要更详细的协议信息时使用。

有用的搜索快捷方式：

```bash
rg -n "^# Catalog|^# Chains" references/catalog-*.md references/chains-*.md
rg -n "WRONG_AUTH_TYPE|insufficient_scope|QUERY_LIMIT_EXCEEDED|expired_token" references/bitrix24.md
rg -n "offline|event\\.bind|event\\.offline|application_token" references/bitrix24.md
```

## 脚本（Scripts）

- `scripts/bitrix24_client.py`：用于方法调用、插件包管理、权限验证和审计。
- `scripts/offline_sync_worker.py`：负责离线队列处理，包括重试和延迟队列（DLQ）功能。