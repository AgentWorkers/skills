---
name: tunneling
description: 使用 `tinyfi.sh` 创建免费的 SSH 隧道，将本地端口暴露到互联网上。当您需要共享正在运行的本地应用程序、测试 Webhook、演示原型，或为任何本地服务获取公共 HTTPS URL 时，都可以使用此方法——无需注册或身份验证。
---

# TinyFish 隧道服务 (tinyfi.sh)

通过 SSH 隧道为本地运行的应用程序创建即时的公共 HTTPS URL。完全免费，无需注册账户，只需安装 SSH 即可使用。

## 预先检查（必填）

确认 SSH 是否可用（通常情况下都是可用的）：

```bash
which ssh && echo "SSH available" || echo "SSH not found — install OpenSSH first"
```

## 快速入门

将本地端口暴露到互联网：

```bash
ssh -o StrictHostKeyChecking=accept-new -R 80:localhost:<PORT> tinyfi.sh
```

请将 `<PORT>` 替换为您应用程序正在运行的端口。该命令将输出一个公共 URL，格式为 `https://<random>.tinyfi.sh`。

## 自定义子域名

请求特定的子域名（而非随机生成的子域名）：

```bash
ssh -o StrictHostKeyChecking=accept-new -R myname:80:localhost:<PORT> tinyfi.sh
```

这样您就可以获得 `https://myname.tinyfi.sh` 这样的 URL。

## 保持连接稳定（防止连接中断）

对于长时间运行的隧道，添加保持连接的机制以防止连接中断：

```bash
ssh -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=60 -R 80:localhost:<PORT> tinyfi.sh
```

## 使用指南

为用户启动隧道时，请按照以下步骤操作：

1. 如果尚未指定，请询问需要暴露的端口。
2. 在后台运行 SSH 命令，以便代理程序可以持续工作。
3. 隧道建立后，将公共 URL 告知用户。
4. 只要 SSH 连接保持有效，隧道就会一直保持开放状态。

## 常用端口

| 框架/工具           | 默认端口         |
|------------------|--------------|
| Next.js / React / Express | 3000           |
| Vite                | 5173            |
| Django             | 8000            |
| Flask              | 5000            |
| Go (net/http)         | 8080            |
| Ruby on Rails        | 3000            |
| PHP (内置)           | 8000            |

## 使用限制

- 每个 IP 地址每分钟最多 5 次 SSH 连接。
- 每个 IP 地址每分钟最多 100 次 HTTP 请求。
- 最多支持 50 个并发连接。
- 连接闲置超过 48 小时后将自动断开。