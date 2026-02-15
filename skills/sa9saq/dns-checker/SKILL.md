---
description: 执行DNS查询，检查记录类型，并验证数据在DNS服务器之间的传播情况。
---

# DNS查询

用于查询和分析任何域名的DNS记录。

## 指令

1. **完整记录查询**：
   ```bash
   dig example.com ANY +noall +answer
   ```

2. **特定记录类型**：
   ```bash
   dig example.com A +short        # IPv4
   dig example.com AAAA +short     # IPv6
   dig example.com MX +short       # Mail
   dig example.com TXT +short      # TXT (SPF, DKIM, etc.)
   dig example.com CNAME +short    # Alias
   dig example.com NS +short       # Nameservers
   dig example.com SOA +short      # Authority
   ```

3. **DNS记录传播检查**（查询多个DNS服务器）：
   ```bash
   for dns in 8.8.8.8 1.1.1.1 9.9.9.9 208.67.222.222; do
     echo "$dns: $(dig @$dns example.com A +short)"
   done
   ```

4. **反向DNS查询**：
   ```bash
   dig -x 8.8.8.8 +short
   ```

5. **报告格式**：
   ```
   🌐 DNS Report — example.com

   | Type  | Value | TTL |
   |-------|-------|-----|
   | A     | 93.184.216.34 | 3600 |
   | AAAA  | 2606:2800:220:1:... | 3600 |
   | MX    | 10 mail.example.com | 3600 |
   | NS    | ns1.example.com | 86400 |

   ## Propagation (A record)
   | DNS Server | Provider | Result | Match |
   |-----------|----------|--------|-------|
   | 8.8.8.8   | Google   | 93.184.216.34 | ✅ |
   | 1.1.1.1   | Cloudflare | 93.184.216.34 | ✅ |
   ```

## 特殊情况

- **NXDOMAIN**：域名不存在 — 请检查是否有拼写错误
- **SERVFAIL**：DNS服务器错误 — 请尝试其他解析器
- **迁移期间TTL值较低**：请注意，DNS记录的传播可能需要长达TTL指定的时间
- **通配符记录**（如`*.example.com`）：请查询具体的子域名以进行验证
- **DNSSEC**：如果需要安全验证，请使用`dig +dnssec`命令

## 所需工具

- `dig`（来自`dnsutils`或`bind-utils`）或`nslookup`
- 可选：`whois`（用于获取域名注册信息）
- 不需要API密钥