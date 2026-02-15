---
description: 执行详细的DNS查询，检查记录类型，并验证DNS信息在多台服务器之间的传播情况。
---

# DNS查询

用于查询和分析任何域名的DNS记录。

## 功能

- **记录查询**：可以查询A记录、AAAA记录、MX记录、TXT记录、CNAME记录、NS记录、SOA记录和PTR记录
- **传播检查**：查询多个公共DNS服务器以验证DNS记录的传播情况
- **反向DNS查询**：根据IP地址查询PTR记录
- **WHOIS查询**：获取域名的基本注册信息

## 使用方法

您可以要求代理执行以下操作：
- “查询example.com的DNS记录”
- “检查gmail.com的MX记录”
- “newsite.com的DNS记录是否已经传播完毕？”
- “对8.8.8.8进行反向DNS查询”

## 工作原理

该工具使用`dig`、`nslookup`和`whois`命令来执行DNS查询：

```bash
dig example.com ANY +noall +answer
dig @8.8.8.8 example.com A
dig @1.1.1.1 example.com A
dig -x 8.8.8.8
```

## 所需软件/库

- `dig`或`nslookup`（来自`dnsutils`/`bind-utils`）
- 可选：`whois`
- 不需要API密钥