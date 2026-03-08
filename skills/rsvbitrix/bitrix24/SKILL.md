---
name: bitrix24
description: 通过 REST API 和官方的 Bitrix24 MCP 文档服务器来与 Bitrix24 进行交互。当 OpenClaw 或 Codex 需要管理 CRM 交易、联系人、潜在客户、公司、任务、检查列表、注释、日历事件、驱动器文件和文件夹、聊天记录、通知、用户、部门，以及进行 Webhook 设置或 OAuth 设置时，或者需要在发起调用之前找到特定的 Bitrix24 方法、事件或文章时，可以使用这些接口。
metadata:
  openclaw:
    requires:
      env:
        - BITRIX24_WEBHOOK_URL
      bins:
        - curl
      mcp:
        - url: https://mcp-dev.bitrix24.tech/mcp
          transport: streamable_http
          tools:
            - bitrix-search
            - bitrix-app-development-doc-details
            - bitrix-method-details
            - bitrix-article-details
            - bitrix-event-details
    primaryEnv: BITRIX24_WEBHOOK_URL
    emoji: "B24"
    homepage: https://github.com/rsvbitrix/openclaw-bitrix24
    aliases:
      - Bitrix24
      - bitrix24
      - Bitrix
      - bitrix
      - b24
      - Битрикс24
      - битрикс24
      - Битрикс
      - битрикс
    tags:
      - bitrix24
      - bitrix
      - b24
      - crm
      - tasks
      - calendar
      - drive
      - chat
      - messenger
      - im
      - webhook
      - oauth
      - mcp
      - Битрикс24
      - CRM
      - задачи
      - чат
---
# Bitrix24

您可以使用以下技能通过两种方式与 Bitrix24 进行交互：

- 通过 `BITRIX24_WEBHOOK_URL` 发送直接的 REST 请求；
- 通过 Bitrix24 的 MCP 服务器（地址：`https://mcp-dev.bitrix24.tech/mcp`）查询官方文档。

此次更新的基准是基于之前的 OpenClaw 项目（地址：`https://github.com/rsvbitrix/openclaw-bitrix24`），尤其是其旧的 `skills/bitrix24` 模块及其设置说明。

## 开始使用

1. 如果用户需要设置指导、凭据、Webhook 配置或 OAuth 相关信息，请阅读 `references/access.md`。
2. 如果 Webhook 调用失败、环境变量设置不正确或设置过程不明确，请先阅读 `references/troubleshooting.md` 并运行 `scripts/check_webhook.py`，再让用户进行手动调试。
3. 如果不清楚具体的 Bitrix24 方法、事件或文档内容，请先阅读 `references/mcp-workflow.md` 并进行搜索，然后再进行操作。
4. 根据具体任务，查阅相应的文档文件：
   - `references/crm.md`：关于客户关系管理（CRM）的相关内容
   - `references/tasks.md`：关于任务管理的相关内容
   - `references/chat.md`：关于聊天功能的相关内容
   - `references/calendar.md`：关于日历功能的相关内容
   - `references/drive.md`：关于文件存储和管理的相关内容
   - `references/users.md`：关于用户管理的相关内容

## REST 请求模式

使用 Webhook URL 作为前缀，并在后面加上 `<方法>.json`：

```bash
curl -s "${BITRIX24_WEBHOOK_URL}<method>.json" -d '<params>'
```

示例：

```bash
curl -s "${BITRIX24_WEBHOOK_URL}crm.deal.list.json" \
  -d 'select[]=ID&select[]=TITLE&select[]=STAGE_ID'
```

`BITRIX24_WEBHOOK_URL` 的格式如下：

```text
https://your-portal.bitrix24.ru/rest/<user_id>/<webhook>/
```

如果仅需要查询 Bitrix24 的文档信息（无需使用 Webhook），即使 Webhook 尚未配置，MCP 服务器仍然可以正常使用。

## MCP 工作流程

请按照以下顺序使用官方的 MCP 文档服务器：

1. 使用 `bitrix-search` 查找所需的方法、事件或文档的标题。
2. 使用 `bitrix-method-details` 查阅 REST 方法的详细信息。
3. 使用 `bitrix-event-details` 查阅事件相关的文档。
4. 使用 `bitrix-article-details` 查阅常规文档的内容。
5. 使用 `bitrix-app-development-doc-details` 查阅与 OAuth、安装回调、BX24 SDK 和应用程序开发相关的内容。

**重要提示：** 当任务较为敏感或方法种类较多时，切勿凭记忆猜测方法名称。请先进行搜索，再请求详细信息。

## 共享规则

- 尽量使用 `filter[...]` 进行服务器端过滤，并使用 `select[]` 来缩小搜索结果范围。
- 在创建自定义字段之前，先使用 `*.fields` 或用户字段发现机制。
- 对于列表相关的操作，使用 `start` 或特定方法的 `START` 参数进行分页处理。
- 当方法需要日期时间值时，请使用 ISO 8601 格式的日期时间字符串。
- 将 `ACCESS_DENIED`、`insufficient_scope`、`QUERY_LIMIT_EXCEEDED` 和 `expired_token` 视为正常操作结果。
- 对于 `imbot.*` 类型的请求，请保持使用相同的 `CLIENT_ID`，不要将其视为公共机器人标识符。
- 如果 Webhook 调用失败，请先自行诊断问题：检查 `BITRIX24_WEBHOOK_URL`、附近的 `.env` 文件，规范化 URL，查看 `user.current.json` 的内容，并总结具体的问题原因，而不是让用户先进行通用性的检查。
- 绝不要将完整的 Webhook 密钥返回给用户；在诊断信息中应对该密钥进行加密处理。
- 当需要查看特定于门户的配置信息时，请使用 `bitrix-method-details` 核对字段名称和示例。
- 对于涉及大量数据或跨实体操作的场景，请在查阅 MCP 文档后，优先使用批量处理或专门的导入方法。

## 相关文档参考

- `references/access.md`：关于 Webhook、OAuth、安装回调以及旧版系统的配置说明。
- `references/troubleshooting.md`：关于 Webhook 配置、DNS 故障、环境变量加载和自我诊断的解决方案。
- `references/mcp-workflow.md`：关于文档查询和工具选择的指导。
- `references/crm.md`：关于客户关系管理（CRM）的相关内容，包括交易、联系人、潜在客户、公司和活动等。
- `references/tasks.md`：关于任务管理、待办事项列表、评论以及已弃用的任务 API 的说明。
- `references/chat.md`：关于聊天功能（包括 `im.*`、`imbot.*`、通知、对话记录和文件传输到聊天的流程）的相关内容。
- `references/calender.md`：关于日历功能的相关内容，包括日历章节、事件、参与者、重复事件安排和可用性检查。
- `references/drive.md`：关于文件存储、文件夹管理、文件操作以及外部链接的处理流程。
- `references/users.md`：关于用户管理、部门信息、组织结构查询以及聊天工具相关的搜索功能。

请仅阅读与当前任务相关的文档文件。