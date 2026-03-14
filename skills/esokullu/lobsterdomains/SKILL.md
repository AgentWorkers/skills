---
name: lobsterdomains
description: 通过加密货币（USDC、USDT、ETH、BTC）注册域名。您可以查询域名的可用性，查看1000多个顶级域名（TLD）的定价信息，并使用以太坊（Ethereum）、Arbitrum、Base或Optimism平台上的链上稳定币完成域名注册。
homepage: https://lobsterdomains.xyz
emoji: 🦞
metadata:
  clawbot:
    primaryEnv: LOBSTERDOMAINS_API_KEY
    requires:
      bins: []
      env:
        - LOBSTERDOMAINS_API_KEY
---
# LobsterDomains — 一款基于人工智能的域名注册服务，支持加密货币支付

您可以使用加密货币进行域名注册。该服务支持多种链上的USDC/USDT稳定币（Ethereum、Arbitrum、Base、Optimism），以及原生ETH和Bitcoin。

## 认证

请访问 [https://lobsterdomains.xyz/api-keys](https://lobsterdomains.xyz/api-keys) 获取您的API密钥（需要使用Ethereum钱包登录）。

所有请求都需要一个Bearer令牌：

```
Authorization: Bearer ld_your_api_key_here
```

请设置以下环境变量：

```bash
export LOBSTERDOMAINS_API_KEY="ld_your_api_key_here"
```

## 基本URL

```
https://lobsterdomains.xyz
```

## 工具

### 1. 检查域名可用性

检查域名是否可用并获取价格信息。

**参数：**
- `domain`（必填）：要检查的域名（例如：`example.com`）

**响应：**
```json
{
  "available": true,
  "domain": "example.com",
  "price": "13.50",
  "currency": "USDC"
}
```

### 2. 获取当前价格

检索当前的ETH和BTC价格（以USD为单位），以便进行价格转换。

```
GET /api/v1/prices
```

### 3. 查看顶级域名（TLD）的价格

查看所有支持的最高域名（TLD）的价格信息。

```
GET https://lobsterdomains.xyz/pricing
```

### 4. 注册域名

在完成链上支付后完成域名注册。

**请求体：**
```json
{
  "domain": "example.com",
  "years": 1,
  "currency": "USDC",
  "chain": "base",
  "txHash": "0x...",
  "contact": {
    "firstName": "Jane",
    "lastName": "Doe",
    "organization": "Example Inc",
    "email": "jane@example.com",
    "phone": "+1.5551234567",
    "address": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "postalCode": "94105",
    "country": "US"
  },
  "nameservers": ["ns1.example.com", "ns2.example.com"]
}
```

**字段：**
- `domain`（必填）：要注册的域名
- `years`（必填）：注册期限（1–10年）
- `currency`（必填）：`USDC`、`USDT`、`ETH` 或 `BTC`
- `chain`（对于稳定币/ETH必填）：`ethereum`、`arbitrum`、`base` 或 `optimism`
- `txHash`（必填）：证明支付的链上交易哈希
- `contact`（必填）：注册人的联系信息，包含2位国家代码
- `nameservers`（可选）：自定义DNS服务器；默认为afraid.org

**响应：**
```json
{
  "orderId": "abc123",
  "domain": "example.com",
  "status": "registered",
  "opensrsUsername": "...",
  "opensrsPassword": "...",
  "managementUrl": "https://..."
}
```

> **重要提示：** 响应中包含`opensrsUsername`和`opensrsPassword`，用于购买后的DNS管理和域名转移。**请务必将这些凭据直接提供给用户**，并提醒他们安全存储这些凭据（例如，使用密码管理器）。切勿将这些凭据保存在聊天记录、日志或任何文件中。这些是敏感的第三方凭据，可授予对注册域名的完全控制权。

### 5. 查询订单

检索订单历史记录。

**返回最多50条最新订单。** 结果中可能包含OpenSRS的管理凭据——请务必直接将这些凭据提供给用户，并提醒他们安全保存。

## 支付详情

**推荐支付方式：** USDC或USDT稳定币（保留6位小数）

**收款地址：**
```
0x8939E62298779F5fE1b2acda675B5e85CfD594ab
```

**支持的链：**
- Ethereum主网
- Arbitrum
- Base
- Optimism

原生ETH和Bitcoin也支持支付，但需要通过 `/api/v1/prices` 进行价格验证。

## 示例工作流程

1. **检查域名可用性：** `GET /api/v1/domains/check?domain=coolstartup.com`
2. **与用户确认价格**
3. **用户在其选择的链上发送稳定币支付**
4. **获取用户的交易哈希**
5. **完成注册：** 使用交易哈希和联系信息发送 `POST /api/v1/domains/register` 请求
6. **安全地传递凭据** —— 将OpenSRS的管理凭据提供给用户，并提醒他们保存在密码管理器中