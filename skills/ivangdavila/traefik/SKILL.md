---
name: Traefik
description: 避免常见的Traefik使用错误：路由器优先级设置、TLS配置问题、Docker标签语法错误以及中间件顺序问题。
metadata: {"clawdbot":{"emoji":"🔀","os":["linux","darwin","win32"]}}
---

## 路由器基础
- 路由器必须同时具备 `rule`（规则）和 `service`（服务）配置——缺少其中任何一个都会导致路由器无法正常工作。
- 规则的优先级：默认情况下，规则长度较长的规则优先生效；可以通过显式设置 `priority` 来覆盖这一规则。
- `Host()` 的匹配不区分大小写——例如 `Host(\`example.com\`)` 会匹配 `Example.com`。
- 多个主机：使用 `Host(\`a.com\`) || Host(\`b.com\`)` 来表示“或”逻辑。

## Docker 标签语法
- 标签应用于容器层面，而非 Compose 服务层面——Swarm 使用 `deploy.labels` 进行配置。
- 在 Docker Compose 中，使用反引号（``）来定义规则，例如 `Host(\`example.com\`)`。
- 如果 `exposedByDefault` 设置为 `false`，可以通过 `traefik.enable=true` 来启用每个容器的标签功能。
- 服务名称可以由容器自动生成，也可以通过 `traefik.http.services.myservice.loadbalancer.server.port=80` 显式设置。

## TLS 和证书
- 当使用 `EntryPoint websecure` 时，需要配置 TLS 参数；否则会使用默认的 HTTP 协议（端口 443）。
- 使用 Let’s Encrypt 证书时，必须配置 `certificatesResolvers.myresolver.acme.email`；否则注册会失败。
- HTTP 挑战需要端口 80 被开放；对于通配符地址或端口 80 被关闭的情况，需要使用 DNS 挑战机制。
- 设置 `tls=true` 可以启用 TLS；`tls.certResolver=myresolver` 可以自动处理证书相关配置。
- 使用 staging URL 进行 ACME 证书测试，可以避免遇到速率限制问题。

## EntryPoints（入口点）
- 可以在静态配置文件中定义入口点，例如 `--entrypoints.web.address=:80`。
- 在入口点级别将 HTTP 请求重定向到 HTTPS，这种方式比在每个路由器中单独配置中间件更简洁。
- 路由器通过 `entryPoints=web,websecure` 来绑定多个入口点（用逗号分隔）。

## 中间件
- 中间件的执行顺序很重要——位于前面的中间件会先于后面的中间件执行。
- 中间件只需定义一次，就可以被多个路由器共享使用，例如 `middlewares=auth,compress`。
- 常用的中间件包括 `stripPrefix`、`redirectScheme`、`basicAuth`、`rateLimit`。
- 使用 `basicAuth` 时，需要使用 `htpasswd` 格式的密码；在 Docker Compose 中，`$` 字符需要用 `$$` 来转义。

## 服务配置
- 当容器暴露多个端口时，需要通过 `loadbalancer.server.port` 来指定负载均衡器的端口——Traefik 无法自动判断。
- 健康检查的路径为 `healthcheck.path=/health`，用于筛选出不健康的容器。
- 对于需要保持会话状态的应用程序，可以使用 `loadbalancer.sticky.cookie.name=srv_id` 来设置粘性会话。

## 常见错误
- 如果路由器没有配置入口点（`entryPoint`），可能会导致预期的行为无法实现。
- 如果在多个网络环境中使用 Traefik，忘记配置 `traefik.docker.network`，Traefik 可能会选择错误的网络。
- 如果 ACME 证书配置没有正确保存，证书可能会被重新生成，从而导致速率限制问题。
- 如果在 production 环境中将 API 开放给未经认证的访问者（`api.insecure=true`），会带来安全风险。
- 如果没有使用 `stripPrefix`，后端服务可能会接收到完整的请求路径，可能导致 404 错误。
- 如果服务运行在不同的端口上，每个服务都需要单独设置端口标签。

## 文件提供者（File Provider）
- 设置 `watch=true` 可以实现热重载——文件更改时无需重启 Traefik。
- 文件提供者可以与 Docker 提供者共存，适用于外部服务的配置。
- 路由器、服务和中间件的配置都可以使用 YAML 文件进行定义，其概念与 Docker 标签类似。

## 调试
- 使用 `--log.level=DEBUG` 可以获取详细的日志信息，有助于故障排查。
- 通过仪表板可以查看路由器的状态、服务和中间件的运行情况，以验证配置是否正确。
- `--api.insecure=true` 仅适用于本地开发环境；在生产环境中应使用认证机制来保护 API 安全性。