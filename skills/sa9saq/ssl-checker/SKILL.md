---
description: 检查任何域名的 SSL/TLS 证书的有效期、有效性、证书链以及配置信息。
---

# SSL检查工具

用于检查SSL/TLS证书：过期日期、颁发机构信息、证书链验证以及批量检测。

## 前提条件

- `openssl`（已安装在大多数系统中）
- 无需API密钥

## 使用说明

### 单个域名检查
```bash
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates -subject -issuer -ext subjectAltName
```

### 提取特定字段
```bash
# Expiry date only
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -enddate

# Days until expiry
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2 | xargs -I{} bash -c 'echo $(( ($(date -d "{}" +%s) - $(date +%s)) / 86400 )) days'

# Full certificate chain
echo | openssl s_client -servername example.com -connect example.com:443 -showcerts 2>/dev/null
```

### 批量检查（多个域名）
```bash
for domain in example.com google.com github.com; do
  expiry=$(echo | openssl s_client -servername $domain -connect $domain:443 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  echo "$domain: $expiry"
done
```

### 输出格式
```
## 🔒 SSL Certificate Report — <timestamp>

| Domain | Status | Expires | Days Left | Issuer |
|--------|--------|---------|-----------|--------|
| example.com | 🟢 Valid | 2025-06-15 | 128 | Let's Encrypt |
| expired.com | 🔴 Expired | 2024-12-01 | -39 | DigiCert |
| soon.com | 🟡 Expiring | 2025-02-20 | 12 | Comodo |

**Thresholds**: 🟢 > 30 days | 🟡 ≤ 30 days | 🔴 Expired or ≤ 7 days
```

## 特殊情况处理

- **非标准端口**：支持使用`domain:8443`语法来指定自定义端口。
- **连接被拒绝**：可能表示该主机不支持HTTPS服务。请明确报告错误，不要导致程序挂起。
- **自签名证书**：`openssl`会显示验证错误，但仍需提取证书详细信息。
- **需要SNI（Server Name Indication）**：务必使用`-servername`参数（某些服务器会根据主机名提供不同的证书）。
- **超时设置**：可以使用`-connect`选项设置超时时间，例如：`timeout 5 openssl s_client ...`
- **通配符证书**：当SAN（Subject Alternative Name）中包含`*.domain.com`时请特别注意。

## 安全性注意事项

- 仅连接443端口（或用户指定的端口），仅进行读取操作。
- 不涉及任何凭据或敏感数据。
- 验证域名输入：仅允许使用字母、数字和连字符（-）。