---
name: CertCheck
description: "SSL/TLS证书检查与分析工具。可检查任何域名的SSL证书，验证有效期、证书链的完整性，检测安全问题，并监控证书的有效性。在SSL证书过期前及时收到警报。"
version: "1.0.0"
author: "BytesAgain"
tags: ["ssl","tls","certificate","security","https","expiry","domain","devops"]
categories: ["Security", "System Tools", "Developer Tools"]
---# CertCheck  
用于检查 SSL 证书，确保在证书过期前及时发现并处理问题，避免影响网站正常运行。  
## 命令  
- `check <domain>` — 对指定域名进行全面的证书检查  
- `expiry <domain>` — 显示该域名证书的剩余有效期（以天为单位）  
- `chain <domain>` — 显示该域名的证书链（包含所有中间证书）  
- `batch <file>` — 从文件中批量检查多个域名  

## 使用示例  
```bash
certcheck check google.com
certcheck expiry github.com
certcheck chain example.com
```  
---  
由 BytesAgain 提供支持 | bytesagain.com