---
name: hostex
description: "Hostex (hostex.io) OpenAPI v3.0 提供了一套用于查询和管理度假租赁房产、房间类型、预订信息、房源可用性、房源列表日历、访客消息、评论以及通过 Hostex API 发送 Webhook 的功能。当您需要使用 Hostex PAT（Hostex-Access-Token / HostexAccessToken）与 Hostex API 进行集成，或者需要进行安全的、基于业务逻辑的 API 调用时（默认为只读模式，支持通过明确确认进行可选的写入操作），请使用此 API。"
---

# Hostex API 技能（Node.js）

## 认证（PAT）

- 设置环境变量：`HOSTEX_ACCESS_TOKEN`
- 请求时需要添加头部信息：`Hostex-Access-Token: <PAT>`
- OpenAPI 的安全方案名称：`HostexAccessToken`

**默认建议**：使用只读权限的 PAT（`read-only`）。

## 日期/时区

- 所有日期参数均采用格式 `YYYY-MM-DD`
- 日期按照设置的时区进行解析（不使用 UTC 时间戳）

## OpenAPI 的官方文档来源

稳定的 OpenAPI JSON 文档：
- https://hostex.io/open_api/v3/config.json

可以使用 `scripts/openapi-sync.mjs` 脚本将官方文档内容缓存到本地文件 `references/openapi.json` 中。

## 快速命令（scripts）

所有脚本都需要 `HOSTEX_ACCESS_TOKEN` 作为参数。

### 只读操作（安全）

- 列出属性信息：
```bash
node skills/hostex/scripts/hostex-read.mjs list-properties --limit 20
```

- 按入住时间范围列出预订信息：
```bash
node skills/hostex/scripts/hostex-read.mjs list-reservations --start-check-in-date 2026-02-01 --end-check-in-date 2026-02-28 --limit 20
```

- 按预订代码列出预订信息：
```bash
node skills/hostex/scripts/hostex-read.mjs list-reservations --reservation-code 0-1234567-abcdef
```

- 查询房源可用性：
```bash
node skills/hostex/scripts/hostex-read.mjs get-availabilities --start 2026-02-10 --end 2026-02-20 --property-id 123
```

### 写入操作（受限制）

除非满足以下条件，否则禁止写入操作：
- `HOSTEX_ALLOW_WRITES=true`
- 并且传递参数 `--confirm`

- 发送消息：
```bash
HOSTEX_ALLOW_WRITES=true node skills/hostex/scripts/hostex-write.mjs send-message --conversation-id 123 --text "Hello!" --confirm
```

- 更新房源价格（单个时间范围示例）：
```bash
HOSTEX_ALLOW_WRITES=true node skills/hostex/scripts/hostex-write.mjs update-listing-prices \
  --channel-type airbnb \
  --listing-id 456 \
  --start 2026-02-10 \
  --end 2026-02-15 \
  --price 199 \
  --confirm
```

- 一次性更新多个时间范围的房源价格：
```bash
HOSTEX_ALLOW_WRITES=true node skills/hostex/scripts/hostex-write.mjs update-listing-prices \
  --channel-type booking_site \
  --listing-id 100541-10072 \
  --prices "2026-02-03..2026-02-05:599,2026-02-06..2026-02-07:699,2026-02-08..2026-02-09:599" \
  --confirm
```

- 创建预订（直接预订）示例：
```bash
HOSTEX_ALLOW_WRITES=true node skills/hostex/scripts/hostex-write.mjs create-reservation \
  --property-id 123 \
  --custom-channel-id 77 \
  --check-in-date 2026-02-10 \
  --check-out-date 2026-02-12 \
  --guest-name "Alice" \
  --currency USD \
  --rate-amount 200 \
  --commission-amount 0 \
  --received-amount 200 \
  --income-method-id 3 \
  --confirm
```

- 更新房源的可用性状态（例如：关闭/开放）示例：
```bash
# Close a property for a date range
HOSTEX_ALLOW_WRITES=true node skills/hostex/scripts/hostex-write.mjs update-availabilities \
  --property-ids "11322075" \
  --available false \
  --start-date 2026-02-03 \
  --end-date 2027-02-02 \
  --confirm
```

## 操作规范（强制要求）

在执行任何写入操作时：
1. **详细说明变更内容**（包括变更者、变更内容、变更时间以及变更幅度）。
2. 要求用户明确确认操作（例如通过输入 `CONFIRM`）。
3. 如果可能的话，建议先执行 `--dry-run`（模拟测试）操作。

## 注意事项

- 分页请求通常支持 `offset` 和 `limit` 参数（`limit` 最大为 100）。
- 绝不要在日志中显示 API 令牌；脚本会自动隐藏敏感信息。