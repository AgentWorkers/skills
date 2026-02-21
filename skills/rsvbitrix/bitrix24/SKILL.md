---
name: bitrix24
description: 通过 REST API 管理 Bitrix24 CRM 中的交易、联系人、潜在客户、任务、日历、文件存储以及消息功能。
version: 0.1.0
metadata:
  openclaw:
    requires:
      env:
        - BITRIX24_WEBHOOK_URL
      bins:
        - curl
    primaryEnv: BITRIX24_WEBHOOK_URL
    emoji: "B24"
    homepage: https://github.com/rsvbitrix/openclaw-bitrix24
    tags:
      - crm
      - tasks
      - productivity
      - bitrix24
      - bitrix
      - b24
---
# Bitrix24

您可以通过其 REST API 来管理 Bitrix24 门户。所有 API 调用都使用 `BITRIX24_WEBHOOK_URL` 中指定的 Webhook URL。

## API 调用模式

```bash
curl -s "${BITRIX24_WEBHOOK_URL}<method>.json" -d '<params>' | jq .result
```

**速率限制**：**每秒 2 次请求**。可以使用 `batch` 参数批量发送最多 50 个请求。

## 模块

每个模块的详细说明请参阅相应的支持文件：

- **crm.md** — 客户关系管理（CRM）：交易、联系人、潜在客户、公司、活动、状态
- **tasks.md** — 任务：创建、更新、完成、委派、待办事项列表、评论
- **calendar.md** — 日历：事件、创建/列出/更新
- **drive.md** — 文件驱动器：存储空间、文件夹、文件、上传/下载
- **chat.md** — 消息传递：发送消息、通知、聊天管理
- **users.md** — 用户：搜索、按 ID 获取用户信息、部门信息、用户结构

在对该模块进行 API 调用之前，请先阅读相关文件。

## 常用模式

### 分页
每页返回 50 条结果。使用 `start` 参数进行分页：
```
&start=0   → page 1
&start=50  → page 2
```
响应中包含 `total` 和 `next` 字段。

### 过滤
```
filter[FIELD]=value       exact match
filter[>FIELD]=value      greater than
filter[<FIELD]=value      less than
filter[>=FIELD]=value     greater or equal
filter[%FIELD]=value      LIKE (contains)
filter[!FIELD]=value      not equal
```

### 日期格式
ISO 8601 格式：`2026-03-01T18:00:00+03:00`

### 多字段值（电话、电子邮件）
```
fields[PHONE][0][VALUE]=+79001234567
fields[PHONE][0][VALUE_TYPE]=WORK
fields[EMAIL][0][VALUE]=user@example.com
fields[EMAIL][0][VALUE_TYPE]=WORK
```

### 批量请求
可以将最多 50 个请求合并到一个请求中：
```bash
curl -s "${BITRIX24_WEBHOOK_URL}batch.json" \
  -d 'cmd[deals]=crm.deal.list&cmd[contacts]=crm.contact.list' | jq .result
```

### 错误处理
发生错误时，响应中会包含 `error` 和 `error_description` 字段。常见错误包括：
- `QUERY_LIMIT_EXCEEDED` — 达到速率限制，请稍后重试
- `ACCESS_DENIED` — 没有足够的权限执行此操作
- `NOT_FOUND` — 指定 ID 的实体不存在