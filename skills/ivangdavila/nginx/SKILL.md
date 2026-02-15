---
name: Nginx
slug: nginx
version: 1.0.1
description: 配置 Nginx 以实现反向代理、负载均衡、SSL 解密以及高性能的静态文件服务。
---

## 使用场景

当用户需要深入了解 Nginx 的配置时（从基本的服务器配置到生产环境的设置），可以使用本文档。代理服务器（Agent）负责处理反向代理、SSL 加密、缓存以及性能调优等任务。

## 快速参考

| 主题 | 文件名 |
|-------|------|
| 反向代理配置 | `proxy.md` |
| SSL/TLS 配置 | `ssl.md` |
| 性能调优 | `performance.md` |
| 常见配置示例 | `examples.md` |

## 匹配规则

- 首先匹配精确的路径（`=`），然后是带有前缀的路径（`^~`），接着是正则表达式（`~`/`~*`），最后是最长前缀匹配。
- `location /api` 匹配 `/api`、`/api/`、`/api/anything`；`location = /api` 仅匹配 `/api`。
- `location ~ \.php$` 是一个区分大小写的正则表达式；`~*` 是不区分大小写的匹配方式。
- `^~` 用于在匹配到前缀时停止正则搜索，适用于静态文件的处理。

## `proxy_pass` 中的路径处理

- `proxy_pass http://backend` 会保留请求的路径（例如：`/api/users` 会被处理为 `/api/users`）。
- `proxy_pass http://backend/` 会替换请求的路径（例如：`/api/users` 会被处理为 `/users`）。
- 常见错误：忘记添加斜杠会导致路径错误或路由问题。可以使用 `curl -v` 命令来检查实际的请求路径。

## `try_files` 的使用

- `try_files $uri $uri/ /index.html`：首先尝试查找文件，如果找不到文件，则查找目录；如果仍然找不到，则返回默认的 `index.html`。
- `try_files` 的最后一个参数用于指定重定向行为（例如：`=404` 表示返回 404 错误）。
- `$uri/` 表示尝试查找带有 `index` 文件的目录；如果找不到，则返回 `index.html`。
- 不适用于需要代理处理的请求路径，应直接使用 `proxy_pass`。

## 代理头信息

- `proxy_set_header Host $host`：让后端服务器看到的是原始请求的域名，而不是代理服务器的 IP 地址。
- `proxy_set_header X-Real-IP $remote_addr`：记录客户端的 IP 地址。
- `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for`：用于记录请求的转发路径。
- `proxy_set_header X-Forwarded-Proto $scheme`：用于判断请求是否使用 HTTPS 协议。

## 上游服务器（Upstream）

- 在 `upstream` 块中定义上游服务器：`upstream backend { server 127.0.0.1:3000; }`。
- `proxy_pass http://backend` 会使用上游服务器的功能，包括负载均衡。
- 通过 `max_fails` 和 `fail_timeout` 参数进行健康检查，判断上游服务器是否可用。
- `keepalive 32` 可以减少连接开销，提高连接效率。

## SSL/TLS 配置

- `ssl_certificate` 文件应包含完整的证书链（包括根证书和中间证书）。
- `ssl_certificate_key` 文件是私钥，需要设置严格的权限。
- `ssl_protocols TLSv1.2 TLSv1.3`：启用最新的 SSL 协议。
- `ssl_prefer_server_ciphers on`：让服务器选择合适的加密算法，而不是客户端。

## 常见错误

- 在执行 `nginx -s reload` 之前，应先使用 `nginx -t` 命令测试配置。
- 配置文件中缺少分号会导致语法错误，此时系统会给出模糊的错误提示。
- 不应在 `location` 块中使用 `root` 指令，除非确实需要覆盖服务器的根目录配置。
- `alias` 和 `root` 的作用不同：`alias` 是用于替换路径，而 `root` 是用于指定应用程序的根目录。
- 在 `if` 语句中使用变量可能会导致逻辑错误，因为变量可能在条件判断时被错误解析。

## 变量说明

- `$uri` 是解码后的、规范化的请求路径（例如：`/foo%20bar` 会被处理为 `/foo bar`）。
- `$request_uri` 包含完整的请求路径（包括查询字符串）。
- `$args` 包含查询参数；`$arg_name` 用于访问特定的查询参数。
- `$host` 来自 `Host` 头信息；`$server_name` 来自配置文件。

## 性能优化

- `worker_processes auto`：根据 CPU 核心数量自动配置工作进程数。
- `worker_connections 1024`：每个工作进程的连接数，总连接数等于工作进程数乘以 `worker_connections`。
- `sendfile on`：启用内核级的文件传输功能。
- `gzip on`：仅对文本文件启用压缩；`gzip_types` 可指定支持的压缩格式（例如：`text/plain application/json ...`）。
- `gzip_min_length 1000`：设置最小压缩文件大小，避免对小文件进行压缩。

## 日志记录

- `access_log off`：关闭静态资源的日志记录，减少 I/O 开销。
- 使用 `log_format` 定义自定义日志格式，可以记录响应时间和上游服务器的处理时间。
- `error_log` 的日志级别包括 `debug`、`info`、`warn`、`error`；`debug` 级别的日志信息最详细。
- 可以使用 `map` 和 `if` 来实现条件化的日志记录，例如：在某些情况下跳过健康检查日志。