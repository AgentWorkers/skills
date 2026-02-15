---
name: porkbun
description: 通过 API v3 管理 Porkbun 的 DNS 记录和域名。当 Codex 需要在 Porkbun 上创建、读取、更新或删除 DNS 记录、列出域名、配置 API 访问权限，或处理常见的记录类型（如 A、AAAA、CNAME、MX、TXT 等）时，可以使用此技能。该技能还包括一个名为 `scripts/porkbun-dns.js` 的 CLI 工具，用于可靠地执行 DNS 操作。
---

# Porkbun DNS管理

通过Porkbun的REST API v3来管理DNS记录和域名。

## 快速入门

### 设置API凭据

1. 生成API密钥：https://porkbun.com/account/api
2. 将凭据保存到配置文件：`~/.config/porkbun/config.json`
```json
{
  "apiKey": "your-api-key",
  "secretApiKey": "your-secret-api-key"
}
```

或者设置环境变量：
```bash
export PORKBUN_API_KEY="your-api-key"
export PORKBUN_SECRET_API_KEY="your-secret-api-key"
```

3. 为每个域名启用API访问：域名管理 → 详情 → API访问 → 启用

### 测试连接

```bash
node ~/.openclaw/workspace/skills/public/porkbun/scripts/porkbun-dns.js ping
```

## 使用CLI工具

`scripts/porkbun-dns.js`脚本提供了一种可靠且可预测的方式来执行DNS操作。可以直接使用该脚本来完成常见任务，而无需编写自定义代码。

### 常见操作

#### 列出域名
```bash
node scripts/porkbun-dns.js list
```

#### 列出DNS记录
```bash
node scripts/porkbun-dns.js records example.com
```

#### 创建记录
```bash
# A record
node scripts/porkbun-dns.js create example.com type=A name=www content=1.1.1.1 ttl=600

# CNAME
node scripts/porkbun-dns.js create example.com type=CNAME name=docs content=example.com

# MX record
node scripts/porkbun-dns.js create example.com type=MX name= content="mail.example.com" prio=10

# TXT record ( SPF for email)
node scripts/porkbun-dns.js create example.com type=TXT name= content="v=spf1 include:_spf.google.com ~all"
```

#### 编辑记录
```bash
# By ID (get ID from records command)
node scripts/porkbun-dns.js edit example.com 123456 content=2.2.2.2

# By type and subdomain (updates all matching records)
node scripts/porkbun-dns.js edit-by example.com A www content=2.2.2.2
```

#### 删除记录
```bash
# By ID
node scripts/porkbun-dns.js delete example.com 123456

# By type and subdomain
node scripts/porkbun-dns.js delete-by example.com A www
```

#### 获取特定记录
```bash
# All records
node scripts/porkbun-dns.js get example.com

# Filter by type
node scripts/porkbun-dns.js get example.com A

# Filter by type and subdomain
node scripts/porkbun-dns.js get example.com A www
```

## 记录类型

支持的记录类型：A、AAAA、CNAME、ALIAS、TXT、NS、MX、SRV、TLSA、CAA、HTTPS、SVCB、SSHFP

有关详细字段要求和示例，请参阅 [references/dns-record-types.md](references/dns-record-types.md)。

## 常见用法

### 网站设置

创建根A记录和www CNAME记录：
```bash
node scripts/porkbun-dns.js create example.com type=A name= content=192.0.2.1
node scripts/porkbun-dns.js create example.com type=CNAME name=www content=example.com
```

### 邮件配置

为Google Workspace设置MX记录：
```bash
node scripts/porkbun-dns.js create example.com type=MX name= content="aspmx.l.google.com" prio=1
node scripts/porkbun-dns.js create example.com type=MX name= content="alt1.aspmx.l.google.com" prio=5
node scripts/porkbun-dns.js create example.com type=MX name= content="alt2.aspmx.l.google.com" prio=5
node scripts/porkbun-dns.js create example.com type=MX name= content="alt3.aspmx.l.google.com" prio=10
node scripts/porkbun-dns.js create example.com type=MX name= content="alt4.aspmx.l.google.com" prio=10
```

添加SPF记录：
```bash
node scripts/porkbun-dns.js create example.com type=TXT name= content="v=spf1 include:_spf.google.com ~all"
```

### 动态DNS

更新主IP地址（可以脚本化/自动化）：
```bash
HOME_IP=$(curl -s ifconfig.me)
node scripts/porkbun-dns.js edit-by example.com A home content=$HOME_IP
```

### 通配符DNS

创建指向根域的通配符记录：
```bash
node scripts/porkbun-dns.js create example.com type=A name=* content=192.0.2.1
```

## 参考文档

- **[references/dns-record-types.md](references/dns-record-types.md)** - 所有DNS记录类型及字段要求的详细参考
- **[https://porkbun.com/api/json/v3/documentation](https://porkbun.com/api/json/v3/documentation)** - 完整的API文档

## 故障排除

### “API密钥未找到”
- 确认配置文件`~/.config/porkbun/config.json`存在
- 检查环境变量：`echo $PORKBUN_API_KEY`
- 确保已为特定域名启用了API访问

### “传递的类型无效”
- 记录类型必须为大写（例如，`A`，而不是`a`）
- 请参阅上述支持的类型列表

### HTTP错误
- 在https://porkbun.com/account/api验证API密钥的有效性
- 检查网络连接
- 确认API端点是`api.porkbun.com`（而非`porkbun.com`）

### TTL错误
- 最小TTL为600秒（10分钟）
- 默认TTL为600秒
- 常见值：300（动态）、3600（标准）、86400（稳定）

## 注意事项

- 最小TTL为600秒
- 使用“@”表示根域名记录
- 使用“*”表示通配符记录
- 包含空格的TXT记录需要加引号
- 允许设置多个具有不同优先级的MX记录
- API v3的当前主机名为`api.porkbun.com`