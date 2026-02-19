---
name: bluepages
description: 请通过 Bluepages 查找钱包地址与 Twitter/Farcaster 账号之间的对应关系。当有人询问某个钱包的归属者、需要根据 Twitter/Farcaster 账号查找钱包地址、查询 0x 地址，或进行任何与钱包身份和地址相关的查询时，都可以使用该工具。
compatibility: >
  Requires MCP server (npx github:bluepagesdoteth/bluepages-mcp) and one of:
  BLUEPAGES_API_KEY or PRIVATE_KEY (Ethereum, for x402 payments).
metadata:
  author: bluepages
  version: "1.0.2"
  openclaw:
    emoji: 📘
    install:
      - kind: node
        package: "github:bluepagesdoteth/bluepages-mcp"
    homepage: https://bluepages.fyi/docs.html
    requires:
      env:
        - BLUEPAGES_API_KEY
        - PRIVATE_KEY
---
# Bluepages

Bluepages支持超过80万个经过验证的以太坊地址的查询，同时提供这些地址与Twitter/X账号的映射信息（包括Farcaster平台的数据）。

## 设置

使用Bluepages需要安装MCP（Master Control Panel）服务器：
```bash
npx -y github:bluepagesdoteth/bluepages-mcp
```
或者直接使用API进行查询（详见下文）。MCP服务器是推荐的使用方式。

## 认证

需要设置以下环境变量之一：
- **`BLUEPAGES_API_KEY`**（推荐）：使用此键可节省20%的费用，并且每分钟的请求次数限制是普通方式的2倍。
- **`PRIVATE_KEY`**：用于通过x402支付方式请求数据（费用为USDC）。

> **安全提示**：切勿使用主钱包的私钥。如果必须使用`PRIVATE_KEY`，请使用专门用于支付的代理钱包。

**使用`PRIVATE_KEY`时**，可以选择通过x402方式按请求付费，或者使用`get_api_key`和`purchase_credits`工具购买`BLUEPAGES_API_KEY`。

**不使用`PRIVATE_KEY`时**，用户需要从[bluepages.fyi/api-keys](https://bluepages.fyi/api-keys.html)获取API密钥，并将其设置为`BLUEPAGES_API_KEY`。

## 工具（快速参考）

| 工具                          | 费用                | 描述                                                         |
| --------------------------- | ---------------------- | -------------------------------------------------- |
| `check_address`            | 1个信用点（0.001美元）      | 检查地址是否存在相关数据                          |
| `check_twitter`            | 1个信用点（0.001美元）      | 检查Twitter账号是否存在相关数据                   |
| `get_data_for_address`     | 50个信用点（0.05美元）     | 获取地址的完整身份信息（未找到时免费）                   |
| `get_data_for_twitter`     | 50个信用点（0.05美元）     | 获取Twitter账号的完整身份信息（未找到时免费）                   |
| `batch_check`              | 40个信用点（0.04美元）     | 一次查询最多50个条目                                   |
| `batch_get_data`           | 40个信用点/每个找到的条目    | 获取最多50个条目的数据（使用x402支付方式：每批2.00美元）         |
| `batch_check_streaming`    | 与`batch_check`相同        | 适用于大量条目（100条以上）；显示查询进度                 |
| `batch_get_data_streaming` | 与`batch_get_data`相同        | 适用于大量条目（100条以上）；显示查询进度                 |
| `check_credits`            | 免费                | 检查剩余信用点数（仅限使用API密钥的情况）                   |
| `set_credit_alert`         | 免费                | 设置低信用点数警告阈值（仅限使用API密钥的情况）                   |
| `get_api_key`              | 免费                | 通过钱包签名获取/创建API密钥                               |
| `purchase_credits`         | 5–600美元（USDC）       | 通过x402方式购买信用点（仅限使用`PRIVATE_KEY`的情况）           |

## 输入格式

- **地址**：以`0x`开头，42个字符的十六进制字符串；不区分大小写。
- **Twitter账号**：可以包含`@`符号，也可以不包含。

## 节省费用的工作流程

- **单次查询**：先使用`check_address`或`check_twitter`（每个操作1个信用点），只有在找到相关数据后才使用`get_data_*`（每个操作50个信用点）。跳过这些步骤会在未找到数据时浪费信用点。
- **批量查询**：始终分两步进行——先使用`batch_check`查询，然后在找到相关数据后使用`batch_get_data`。这种方式相比一次性查询所有数据可节省约90%的费用。
- **处理大量条目（100条以上）**：使用`batch_check_streaming`或`batch_get_data_streaming`工具来获取查询进度。

## 请求限制

- API密钥：每分钟60次请求。
- x402支付方式：每分钟30次请求。
- 批量查询：每次请求最多查询50个条目。

## 替代方案：直接使用HTTP API

如果MCP服务器不可用，可以直接调用API。认证方式取决于您的设置：
- **API密钥**：在请求头中添加`X-API-KEY`。
- **使用`PRIVATE_KEY`的x402支付方式**：API端点会返回402错误代码并提示支付详情；用户需要使用`X-PAYMENT`头重新发送请求。

```bash
# With API key
curl "https://bluepages.fyi/check?address=0x..." -H "X-API-KEY: your-key"
curl "https://bluepages.fyi/data?address=0x..." -H "X-API-KEY: your-key"

# Batch check
curl -X POST "https://bluepages.fyi/batch/check" \
  -H "X-API-KEY: your-key" -H "Content-Type: application/json" \
  -d '{"addresses": ["0x...", "0x..."]}'
```

完整的API文档请参阅：[bluepages.fyi/docs](https://bluepages.fyi/docs.html)