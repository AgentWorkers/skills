---
name: nginx-gen
description: **从纯文本生成 Nginx 配置文件**  
用于配置 Nginx 服务器时使用。
---

# Nginx 生成器

别再在网上搜索 Nginx 配置片段了。直接描述你的需求，就能得到一个可用的 Nginx 配置文件。

**只需一个命令，无需编写任何配置代码，即可立即生效。**

## 快速入门

```bash
npx ai-nginx "reverse proxy port 3000 with SSL"
```

## 功能介绍

- 生成完整的 Nginx 配置文件
- 支持反向代理、SSL 加密、缓存功能以及速率限制
- 自动添加安全头部信息
- 配置符合规范的服务器块结构

## 使用示例

```bash
# Reverse proxy with SSL
npx ai-nginx "reverse proxy port 3000 with SSL and rate limiting"

# Static site
npx ai-nginx "serve static files from /var/www/html with caching"

# Load balancing
npx ai-nginx "load balance between 3 node servers" -o nginx.conf
```

## 最佳实践

- **务必使用 SSL**：Let’s Encrypt 提供免费的 SSL 证书
- **设置工作进程数量**：根据实际流量情况进行调整
- **启用 gzip 压缩**：压缩文本响应内容
- **添加安全头部信息**：防止常见的网络攻击

## 适用场景

- 设置新的 Nginx 服务器
- 为现有服务器添加反向代理功能
- 配置 SSL 代理的终结点
- 学习 Nginx 配置原理

## LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无付费门槛、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub：https://github.com/LXGIC-Studios
- Twitter：https://x.com/lxgicstudios
- Substack：https://lxgicstudios.substack.com
- 官网：https://lxgicstudios.com

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-nginx --help
```

## 工作原理

该工具会根据你提供的纯文本描述自动生成完整的 Nginx 配置文件。它内置了对 Nginx 语法及常见配置模式（如反向代理、SSL、缓存等）的最佳实践的理解。

## 许可证

采用 MIT 许可协议，永久免费。你可以随心所欲地使用这个工具。