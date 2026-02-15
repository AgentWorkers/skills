---
name: DNS
description: 正确配置DNS记录，确保TTL值设置合理，同时实现电子邮件认证和数据迁移策略。
metadata: {"clawdbot":{"emoji":"🌍","os":["linux","darwin","win32"]}}
---

## 迁移前的TTL设置

- 在更改记录前至少48小时内，将TTL值设置为300秒以上——确保当前的TTL值先过期。
- 在进行任何操作之前，请先检查当前的缓存TTL值：`dig +nocmd +noall +answer example.com`
- 迁移完成后，等待24小时确保系统稳定运行，再将TTL值恢复到3600至86400秒之间。
- 使用多个解析器（如Google的8.8.8.8、Cloudflare的1.1.1.1或本地ISP）进行测试——这些解析器会独立缓存域名信息。

## 电子邮件认证（三项要求均需满足）

- 单纯使用SPF是不够的，还需要DKIM和DMARC来确保邮件能够成功送达。
- DMARC记录的格式应为：`_dmarc.example.com TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"`
- SPF记录应为单个TXT记录，多个SPF记录会导致认证失败；如果需要引用多个来源，请使用`include:`指令。
- SPF记录的结尾应使用`-all`（拒绝所有邮件）或`~all`（软失败），绝对不能使用`+all`或`?all`。
- 配置完成后，使用mail-tester.com工具验证整个认证设置是否正确。

## CAA（Domain Authority Validation）记录

- CAA记录用于限制哪些证书颁发机构可以为该域名颁发证书，从而防止未经授权的证书发行。
- 基本格式：`example.com. CAA 0 issue "letsencrypt.org"`
- 如果使用通配符域名，则需要单独设置CAA记录：`CAA 0 issuewild "letsencrypt.org"`
- 发生安全事件时，需要设置`CAA 0 iodef "mailto:security@example.com"`以便及时报告。
- 如果不设置CAA记录，任何证书颁发机构都可以为该域名颁发证书；对于注重安全的域名，建议明确指定CAA颁发机构。

## www域的处理

- 需要同时配置“apex”和“www”这两个域名，或者将其中一个重定向到另一个；如果“www”未配置，可能会导致链接失效。
- 确定一个标准的域名形式并保持一致：要么“www”指向“apex”，要么“apex”指向“www”。
- 在进行重定向之前，两个域名都需要具备HTTPS证书。
- 配置完成后，需要分别测试这两个URL是否能够正常访问。

## 调试命令

- `dig +trace example.com`：显示从根域名开始的所有DNS解析过程，有助于定位问题所在。
- `dig @ns1.provider.com example.com`：直接查询权威DNS服务器，绕过缓存结果。
- 比较权威DNS服务器的响应与缓存中的响应是否一致——不一致可能表示DNS解析过程尚未完成。
- 需要检查所有相关的DNS记录类型——即使A记录、MX记录和TXT记录正确，也不能保证整个DNS系统正常工作。

## Cloudflare代理的行为

- 当使用Cloudflare代理时，源IP地址会被隐藏（显示为“orange cloud”），这可能会影响SSH连接、邮件传输和游戏服务器的运行；对于非HTTP请求，建议使用“grey cloud”代理。
- Cloudflare会忽略用户自定义的TTL设置，它自行控制DNS记录的缓存策略。
- 在Cloudflare环境中，将“CNAME”记录设置为“apex”可能会导致迁移后的DNS配置混乱。
- 只有在代理环境下才支持通用SSL证书；如果仅使用DNS解析，则需要使用源服务器的证书。

## 通配符DNS记录

- `*.example.com`不会自动匹配“apex.example.com”；这两个域名都需要单独设置DNS记录。
- 显式的子域名记录优先于通配符记录。
- 通配符域名需要单独的SSL证书；使用Let’s Encrypt服务进行SSL证书的颁发和验证。