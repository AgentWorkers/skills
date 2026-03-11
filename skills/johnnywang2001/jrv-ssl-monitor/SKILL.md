---
name: jrv-ssl-monitor
description: >
  **检查一个或多个域名的 SSL/TLS 证书有效期、颁发机构、协议以及附加主体名称（SANs）**  
  适用于需要验证 SSL 证书、监控证书有效期、确认 HTTPS 是否正常工作、审计域名安全性或检查证书是否即将到期的场景。支持自定义端口和警告阈值。该工具完全依赖 Python 的标准 `ssl` 模块，无需任何外部依赖。
---
# SSL证书监控工具

该工具用于检查任何域名的SSL证书状态，包括有效期、颁发机构、协议版本以及Subject Alternative Names（SAN）等信息。

## 快速入门

```bash
python3 scripts/check_ssl.py example.com
python3 scripts/check_ssl.py example.com google.com github.com --warn-days 30
python3 scripts/check_ssl.py internal.host --port 8443 --json
```

## 主要功能

- **有效期检查**：可配置警告阈值，显示剩余天数
- **多域名支持**：通过一条命令检查多个域名
- **证书详细信息**：显示证书的主题名称（Subject）、颁发机构、使用的协议版本、序列号以及SAN信息
- **错误处理**：能够检测DNS请求失败、连接超时、验证错误或连接被拒绝等情况
- **退出代码**：0表示一切正常；1表示存在警告；2表示证书已过期或检查失败（适用于定时任务/持续集成/持续部署流程）
- **无依赖库**：仅使用Python标准库

## 命令行参数

| 参数 | 说明 |
|------|-------------|
| `--warn-days N` | 警告阈值（以天为单位，默认值：14） |
| `--port PORT` | 需要检查的端口（默认值：443） |
| `--json` | 以结构化JSON格式输出结果 |
| `--timeout N` | 连接超时时间（以秒为单位，默认值：10） |

## 使用场景

- 用于每日定时任务，监控生产环境中的域名SSL证书状态
- 在部署前验证证书的有效性
- 一次性审计公司所有域名的SSL证书状态
- 作为持续集成/持续部署（CI/CD）流程中的证书健康检查环节