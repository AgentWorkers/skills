---
name: Binance API
slug: binance
version: 1.0.0
homepage: https://clawic.com/skills/binance
description: 通过安全的 REST、WebSocket 和 SDK 工作流程来操作 Binance Spot API，这些流程支持签名请求、速率限制控制，并优先在测试网（testnet）上执行操作。
changelog: Initial release with production-safe Binance Spot API workflows for REST, WebSocket, signing, and testnet validation.
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["curl","openssl","jq"],"env":["BINANCE_API_KEY","BINANCE_API_SECRET"]},"os":["linux","darwin","win32"]}}
---
# Binance 现货 API 操作

## 设置

首次使用时，请阅读 `setup.md` 以了解集成偏好设置和默认的安全环境配置。

## 使用场景

当用户需要获取 Binance 的市场数据、下达或管理现货订单，或排查终端工作流程中涉及的 API 调用问题时，可参考本文档。该技能会负责处理请求签名、参数验证、速率限制控制以及 WebSocket 数据的同步。

## 架构

相关数据存储在 `~/binance/` 目录下。具体结构请参阅 `memory-template.md`。

```text
~/binance/
├── memory.md            # API mode, symbols, and execution preferences
├── runbooks.md          # Repeatable workflows that worked in production
├── incidents.md         # Failures, response codes, and fixes
└── snapshots/           # Symbol filters and pre-trade validation captures
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 设置配置 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 快速入门命令 | `quickstart.md` |
| 认证与签名 | `auth-signing.md` |
| 市场数据格式 | `market-data.md` |
| 数据流与 WebSocket API | `websocket.md` |
| SDK 与 CLI 配置 | `sdk-cli.md` |
| 速率限制与错误处理 | `errors-limits.md` |
| 现货测试网操作 | `testnet.md` |
| 故障排查 | `troubleshooting.md` |

## 所需工具

- `curl`
- `openssl`
- `jq`
- `BINANCE_API_KEY` 和 `BINANCE_API_SECRET`（用于生成签名）
- 可选：`BINANCE_BASE_URL`、`BINANCE_WS_BASE` 和 `BINANCE_TESTNET=1`

**注意：**切勿将 API 密钥或敏感信息存储在仓库文件中。

## 数据存储路径

- `~/binance/memory.md`：存储配置信息和环境模式设置
- `~/binance/runbooks.md`：保存经过验证的工作流程脚本
- `~/binance/incidents.md`：记录系统故障和错误日志
- `~/binance/snapshots/`：保存 `exchangeInfo` 数据及参数捕获结果

## 核心规则

### 1. 默认情况下从现货测试网开始使用
- 仅在获得明确许可后才能使用生产环境。
- 对于每个新的订单或账户操作，务必先在测试网环境中进行测试。

### 2. 确保时间戳和签名正确
- 在发送签名请求前，请确保服务器时间与本地时间一致，并设置合理的 `recvWindow` 值。
- 签名前需对参数进行排序，并将所有签名字段包含在请求字符串中。

### 3. 下单前验证符号过滤器
- 从 `exchangeInfo` 中获取符号过滤器，并确保 `PRICE_FILTER`、`LOT_SIZE` 和 `MIN_NOTIONAL` 的值符合要求。
- 对于可能失败的请求，需在发送前在本地进行验证。

### 4. 先发送测试订单再发送正式订单
- 对于任何新的请求数据，先调用 `POST /api/v3/order/test`。
- 只有在确认数据格式和过滤器正确后，才能继续发送 `POST /api/v3/order` 请求。

### 5. 通过用户事件确认订单状态
- 在网络质量较差的情况下，将订单响应视为临时结果。
- 最终状态需通过 `executionReport` 事件和 REST 查询来确认。

### 6. 遵守速率限制并快速重试
- 解析响应中的速率限制信息，并主动进行重试控制。
- 遇到 `429` 或 `418` 错误时，应暂停重试并采用指数级退避策略，避免连续多次失败。

### 7. 保持使用范围明确且透明
- 仅使用 Binance 官方指定的端点和用户请求的符号。
- 禁止修改本技能文件或任何无关的本地文件。

## 常见问题与注意事项

- 本地时钟偏差可能导致 `-1021` 错误或伪造的认证失败。
- 更改参数后重复使用旧签名可能导致 `-1022` 错误。
- 即使账户余额充足，如果发送的订单数量与 `stepSize` 不匹配，也会导致请求失败。
- 从放置响应中直接判断订单状态可能导致部分订单未完成或被取消。
- 打开持续超过 24 小时的市场数据流会导致连接中断。
- 忽略 `429` 错误响应可能导致临时账户封禁。

## 外部接口

本技能仅使用以下官方 Binance API 接口：

| 接口 | 发送的数据 | 用途 |
|---------|-----------|---------|
| `https://api.binance.com` 和 `https://api-gcp.binance.com` | 签名的交易/账户参数、市场查询参数 | 现货交易 REST 接口 |
| `https://api1.binance.com` 至 `https://api4.binance.com` | 同上 | 备用的生产环境 REST 服务器 |
| `https://data-api.binance.vision` | 仅公开市场数据参数 | 公开市场数据 |
| `wss://stream.binance.com:9443` 和 `wss://stream.binance.com:443` | 数据流订阅和监听键数据 | 现货市场数据流 |
| `wss://data-stream.binance.vision` | 仅市场数据流订阅 | 公开市场数据流 |
| `wss://ws-api.binance.com:443/ws-api/v3` | 签名/未签名的 WebSocket API 请求 | 现货 WebSocket API |
| `https://testnet.binance.vision`, `wss://stream.testnet.binance.vision`, `wss://ws-api.testnet.binance.vision/ws-api/v3` | 测试网订单/账户数据 | 现货测试网验证 |

**注意：**不会向外部发送任何其他数据。

## 安全与隐私

**会离开您机器的数据：**
- API 密钥标识符、账户参数及交易相关数据
- 请求的符号、时间间隔以及市场数据流订阅信息

**保留在本地的数据：**
- 操作过程中的内存数据及故障日志（`~/binance/` 目录）
- 会话期间生成的辅助脚本和运行脚本

**本技能不会：**
- 向未声明的服务发送数据
- 未经确认即下达生产环境订单
- 将 API 密钥存储在仓库文件中
- 修改本技能的定义文件

## 信任说明

使用本技能意味着您将请求数据发送至 Binance 的基础设施。仅当您信任 Binance 并愿意共享交易数据时，才建议安装此技能。

## 相关技能

如用户确认需要，可使用以下命令安装相关技能：
- `clawhub install <slug>`：
  - `api`：构建和调试可靠的 HTTP API 请求流程
  - `auth`：处理 API 认证、签名及凭证安全
  - `bash`：自动化 shell 操作
  - `bitcoin`：在分析加密货币交易时添加 BTC 相关信息

## 反馈建议

- 如觉得本技能有用，请给 `clawhub` 评分（例如：`clawhub star binance`）
- 保持更新：`clawhub sync`