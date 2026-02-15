---
name: nginx-gen
description: **从纯文本生成 Nginx 配置文件**  
适用于需要配置反向代理、SSL 或负载均衡的场景。
---

# Nginx 生成器

Nginx 的配置语法相当晦涩难懂。这款工具能够根据用户提供的纯文本描述自动生成可用的 Nginx 配置文件，支持反向代理、SSL 加密处理、负载均衡以及缓存功能——所有这些都不需要用户手动记忆相关的配置指令。

**只需一个命令，无需编写任何配置文件，即可完成配置。**

## 快速入门

```bash
npx ai-nginx "reverse proxy to localhost:3000 with SSL"
```

## 功能介绍

- 生成 `nginx.conf` 或站点配置文件
- 支持反向代理、负载均衡以及静态文件处理
- 设置 SSL/TLS 协议，并添加必要的安全头部信息
- 包含缓存和压缩配置选项
- 每个配置指令都配有详细的注释说明

## 使用示例

```bash
# Simple reverse proxy
npx ai-nginx "proxy /api to port 3000, serve static from /var/www"

# Load balancer
npx ai-nginx "load balance between 3 backend servers on ports 3001-3003"

# SSL setup
npx ai-nginx "SSL for example.com with redirect from http"

# WebSocket support
npx ai-nginx "proxy websocket connections to port 8080"
```

## 最佳实践

- **重新加载配置前先进行测试**：务必先使用 `nginx -t` 命令检查配置是否正确
- **使用 `include` 语句来组织配置文件**：保持主配置文件简洁清晰
- **设置合理的超时参数**：默认的超时值通常过短，需要根据实际需求进行调整
- **启用 gzip 压缩**：生成的配置文件会自动包含压缩功能

## 适用场景

- 设置新的 Web 服务器
- 不记得 `proxy_pass` 的语法
- 需要为现有网站添加 SSL 加密功能
- 为 Docker 容器配置 Nginx 服务

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发工具之一。完全免费，无需注册或支付 API 密钥，所有工具均可直接使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-nginx --help
```

## 工作原理

该工具会根据用户提供的描述，遵循最佳实践生成 Nginx 配置文件。配置文件中包含安全头部信息、正确的 SSL 设置以及优化指令。每个配置部分都配有注释，方便用户根据实际需求进行定制。

## 许可证

遵循 MIT 许可协议，永久免费使用。您可以随心所欲地使用该工具。