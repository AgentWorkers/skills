---
name: "SSL"
version: "1.0.2"
description: "配置 HTTPS，管理 TLS 证书，并调试安全连接问题。"
---

## 触发条件

- SSL证书更新时
- 设置HTTPS时
- 使用Let's Encrypt时
- 使用certbot时
- TLS配置更改时
- 证书过期时
- 页面中存在混合内容（HTTP与HTTPS资源混合）时
- 证书链出现错误时

## 核心任务

| 任务 | 使用的工具/方法 |
|------|-------------|
| 获取免费证书 | `certbot`, `acme.sh`, `Caddy`（自动获取） |
| 检查证书状态 | `openssl s_client -connect host:443` |
| 查看证书详细信息 | `openssl x509 -in cert.pem -text -noout` |
| 测试配置 | `ssllabs.com/ssltest` 或 `testssl.sh` |
| 转换证书格式 | 请参阅 `formats.md` |

## 常用证书操作命令

```bash
# Let's Encrypt with certbot (most common)
certbot certonly --nginx -d example.com -d www.example.com

# Check expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# Verify chain is complete
openssl s_client -connect example.com:443 -servername example.com
# Look for "Verify return code: 0 (ok)"
```

## 常见错误及解决方法

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| 证书已过期 | 证书的有效期已过 | 使用 `certbot renew` 命令更新证书 |
| 无法验证证书 | 证书缺少中间证书 | 在配置文件中添加完整的证书链 |
| 主机名不匹配 | 证书未覆盖当前域名 | 获取适用于正确域名的证书或添加SAN（Subject Alternative Name） |
| 页面中存在混合内容 | HTTPS页面中包含HTTP资源 | 将所有URL更改为HTTPS，或使用 `//` 来处理混合内容 |
| `ERR_CERT_AUTHORITY_INVALID` | 证书为自签名证书或来自不受信任的CA | 使用Let's Encrypt或安装受信任的CA证书 |

有关详细的故障排除步骤，请参阅 `troubleshooting.md`。

## 服务器配置示例

**Nginx:**
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
}
```

**Apache:**
```apache
SSLEngine on
SSLCertificateFile /path/to/cert.pem
SSLCertificateKeyFile /path/to/privkey.pem
SSLCertificateChainFile /path/to/chain.pem
```

有关Node.js、Caddy、Traefik和HAProxy的配置，请参阅 `servers.md`。

## 证书续期

Let's Encrypt证书的有效期为90天。建议始终使用自动化工具进行续期：

```bash
# Test renewal
certbot renew --dry-run

# Cron (certbot usually adds this)
0 0 * * * certbot renew --quiet
```

## 证书类型

| 类型 | 适用场景 |
|------|----------|
| 单域名证书 | 仅适用于一个网站（例如 example.com） |
| 通配符证书 (*.domain.com) | 适用于所有子域名 |
| 多域名证书（SAN） | 一个证书可覆盖多个不同的域名 |
| 自签名证书 | 仅用于本地开发环境——浏览器会发出警告 |

## 本文档未涵盖的内容

- 应用程序认证（JWT、OAuth） → 请参阅 `oauth` 文档 |
- SSH密钥管理 → 请参阅 `linux` 或相关服务器配置文档 |
- VPN/隧道设置 → 请参阅网络配置相关文档 |
- 防火墙配置 → 请参阅服务器/基础设施配置相关文档