---
name: ampersend
description: Ampersend CLI：用于代理支付的命令行工具
metadata: { "openclaw": { "requires": { "bins": ["ampersend"] } } }
---
# Ampersend CLI

Ampersend CLI 是用于管理智能账户钱包的工具，允许代理执行支付操作。

## 设置

```bash
npm install -g @ampersend_ai/ampersend-sdk@beta
```

如果未进行配置，所有命令都会返回设置指南。要配置，请执行以下操作：

```bash
ampersend config init
# {"ok": true, "data": {"sessionKeyAddress": "0x...", "status": "pending_agent"}}

# Register sessionKeyAddress in Ampersend dashboard, then:
ampersend config set-agent <SMART_ACCOUNT_ADDRESS>
# {"ok": true, "data": {"status": "ready", ...}}

ampersend config status
# {"ok": true, "data": {"status": "ready", "source": "file", ...}}
# source: "env" | "file" | "none"
```

## 命令

### fetch

发送 HTTP 请求，并自动处理 x402 支付请求。

```bash
ampersend fetch <url>
ampersend fetch -X POST -H "Content-Type: application/json" -d '{"key":"value"}' <url>
```

| 选项          | 描述                                      |
| ------------- | -------------------------------------------- |
| `-X <方法>`     | HTTP 方法（默认：GET）                         |
| `-H <头部>`     | 以“键: 值”的格式设置请求头部（可重复使用）         |
| `-d <数据>`     | 请求体                                   |

## 输出结果

所有命令的返回结果均为 JSON 格式。请首先检查 `ok` 字段以确认请求是否成功。

```json
{ "ok": true, "data": { ... } }
```

```json
{ "ok": false, "error": { "code": "...", "message": "..." } }
```

对于 `fetch` 命令，成功返回的结果包含 `data.status`、`data.body` 以及 `data.payment`（如果支付已完成的话）。