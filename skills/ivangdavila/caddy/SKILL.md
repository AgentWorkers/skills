---
name: Caddy
description: 将 Caddy 配置为反向代理，实现自动 HTTPS 加密，并使用简单的 Caddyfile 语法进行配置。
metadata: {"clawdbot":{"emoji":"🔒","requires":{"bins":["caddy"]},"os":["linux","darwin","win32"]}}
---

# Caddy 配置规则

## 自动 HTTPS
- Caddy 会自动配置 SSL 证书——除非有特殊需求，否则无需手动配置 Let’s Encrypt。
- 域名必须能够被公众访问，以便进行 HTTP 挑战（验证）；对于内部域名或通配符域名，应使用 DNS 挑战机制。
- 端口 80 和 443 必须是空闲的——即使仅使用 HTTPS，Caddy 也需要这两个端口（80 端口用于处理 ACME 挑战并执行重定向）。
- Let’s Encrypt 有速率限制——在测试期间请使用临时证书颁发机构（staging CA）以避免达到生产环境的限制。

## Caddyfile 语法
- 缩进非常重要——代码块的定义依赖于缩进，而不是括号。
- 站点配置块的开始括号前需要有一个空格：例如 `example.com {`，而不是 `example.com{`。
- 使用 `caddy fmt --overwrite` 命令来修复格式问题——这可以解决大多数语法错误。
- 在应用配置之前，请使用 `caddy validate --config /etc/caddy/Caddyfile` 命令进行验证。

## 反向代理
- Caddy 会自动添加 `X-Forwarded-For`、`X-Forwarded-Proto` 和 `X-Forwarded-Host` 头信息——无需手动添加。
- WebSocket 功能默认即可使用——无需特殊配置。
- 多个后端会自动进行负载均衡——默认使用随机分配策略，可以通过 `lb_policy` 配置进行更改。
- 被标记为“失败”的后端会自动从负载均衡中移除。

## Docker 网络配置
- 使用容器名称作为主机名：例如 `reverse_proxy container_name:3000`。
- Caddy 和后端必须属于同一个 Docker 网络——默认的桥接网络不支持 DNS 解析。
- 在使用 Docker Compose 时，同一网络中的服务名称可以直接用作主机名。

## 配置管理
- 使用 `caddy reload` 命令重新加载配置——重新加载配置不会中断现有连接。
- 配置更改是原子性的（即：如果新配置验证失败，旧配置仍然有效）。
- 可以使用 `caddy adapt --config Caddyfile` 命令在应用配置之前进行预览，查看解析后的 JSON 输出。

## 证书存储
- 证书默认存储在 `~/.local/share/caddy` 目录中——请在重新安装 Caddy 时保持这一设置不变。
- 对于 Docker 环境，需要挂载 `/data` 和 `/config` 目录作为数据卷——如果这些目录丢失，将需要重新请求所有证书。
- 如果有多个 Caddy 实例，需要共享证书存储空间，否则它们之间可能会发生证书冲突。

## 调试
- 启用调试日志记录：在全局配置选项块的第一行添加 `debug`。
- 可以通过 `/data/caddy/certificates/` 目录查看证书的状态。
- 常见问题：DNS 尚未解析到服务器——在这种情况下，证书验证会失败，但系统不会显示错误信息。

## 安全头信息
- Caddy 默认不会自动添加安全头信息——需要手动添加 `X-Frame-Options` 和 `X-Content-Type-Options`。
- 服务 HTTPS 时，HSTS（HTTP Strict Transport Security）会自动启用——无需手动配置。

## 性能
- Caddy 能够处理数千个并发连接，无需额外调优。
- 支持 HTTP/3 协议（通过 `servers { protocols h1 h2 h3 }` 配置）。
- 文本内容会自动进行压缩。