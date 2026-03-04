---
name: dns-lookup
description: DNS记录查询、反向DNS查询、通过RDAP查询WHOIS信息以及IP地址的地理位置信息。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🌐"
    homepage: https://dns.agentutil.net
    always: false
---
# DNS查询

支持DNS记录的查询（A、AAAA、MX、TXT、CNAME、NS、SOA类型），反向DNS（PTR类型），WHOIS/RDAP域名信息查询，以及IP地址的地理位置查询。

## 数据处理

该功能会将域名和IP地址发送到外部API进行处理。服务在返回响应后会立即销毁输入数据，不会进行任何存储或日志记录。

## 接口端点

### DNS查询

```bash
curl -X POST https://dns.agentutil.net/v1/lookup \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com", "type": "MX"}'
```

支持查询的记录类型：A、AAAA、MX、TXT、CNAME、NS、SOA、ANY。默认查询类型为A。

### 反向DNS

```bash
curl -X POST https://dns.agentutil.net/v1/reverse \
  -H "Content-Type: application/json" \
  -d '{"ip": "8.8.8.8"}'
```

### WHOIS

```bash
curl -X POST https://dns.agentutil.net/v1/whois \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

### IP地理位置查询

```bash
curl -X POST https://dns.agentutil.net/v1/geoip \
  -H "Content-Type: application/json" \
  -d '{"ip": "8.8.8.8"}'
```

## 响应格式

```json
{
  "records": [{"type": "A", "value": "93.184.216.34", "ttl": 300}],
  "domain": "example.com",
  "query_type": "A",
  "request_id": "abc-123",
  "service": "https://dns.agentutil.net"
}
```

## 价格

- 免费 tier：每天10次查询，无需身份验证
- 付费 tier：每次查询0.001美元，通过x402协议进行支付（以USDC为单位）

## 隐私政策

免费 tier无需身份验证，不会收集任何个人数据。速率限制仅使用IP地址进行哈希处理。