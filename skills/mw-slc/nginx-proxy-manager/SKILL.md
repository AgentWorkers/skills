---
name: nginx-proxy-manager
description: 管理 Nginx Proxy Manager（NPM），用于实现反向代理和 SSL 加解密功能，以便与内部服务（如 staging 或 prod 环境下的应用程序）进行通信。该工具可用于创建/更新代理主机配置、申请/续订 Let's Encrypt 证书、强制实施 HTTPS 重定向规则、配置 WebSocket 支持，以及将域名/子域名路由到目标服务器。
---
# Nginx 代理管理器工作流程

使用此技能可以在 NPM 端终止 SSL 加密，并将流量路由到后端服务（测试环境/生产环境）。

## 所需输入信息

- 域名/子域名（例如：`staging.example.com`）
- 已经指向 NPM 公共 IP 的公共 DNS
- 上游目标主机/IP 及端口（例如：`10.10.10.227:3000`）
- 是否启用 Cloudflare 代理（如果使用）

## 认证（切勿硬编码敏感信息）

将凭据存储在技能文件之外（本地秘密文件或环境变量中）。

推荐的环境变量：
- `NPM_BASE_URL`（例如：`http://<npm-host>:81`）
- `NPM_IDENTITY`
- `NPM_SECRET`

示例令牌请求：

```bash
curl -sS -X POST "$NPM_BASE_URL/api/tokens" \
  -H 'Content-Type: application/json; charset=UTF-8' \
  --data "{\"identity\":\"$NPM_IDENTITY\",\"secret\":\"$NPM_SECRET\"}"
```

## 标准设置流程

1. 确认 DNS 能够解析到 NPM 的公共 IP。
2. 在 NPM 中创建或更新代理配置：
   - 域名：请求的主机名
   - 协议：`http`（如果上游使用 TLS，则为 `https`）
   - 转发主机名/IP：上游 IP/主机名
   - 转发端口：应用程序端口
   - 启用以下功能：
     - 阻止常见攻击
     - 支持 Websocket
3. SSL 配置：
   - 申请新的 SSL 证书（Let’s Encrypt）
   - 启用 `Force SSL` 功能
   - 启用 `HTTP/2` 支持
   - 仅在验证通过后启用 `HSTS` 功能
4. 保存并验证配置：
   - 使用 `curl -I https://<domain>` 命令，如果返回 `200/301`，则说明配置正确
   - 通过浏览器检查证书的有效性以及应用程序是否可访问

## 推荐的默认设置

- 尽可能使用私有 IP 作为上游服务器地址。
- 为不同环境使用不同的主机名：
  - `app.example.com` → 生产环境
  - `staging.example.com` → 测试环境
- 除非有特殊需求，否则避免使用通配符证书。

## 故障排除

- 证书颁发失败：
  - 检查 DNS 的 A/AAAA 记录
  - 确保端口 80/443 可以访问 NPM
  - 禁用冲突的 CDN TLS 模式，或将其设置为 Full/Strict 模式
- 502 错误（Bad Gateway）：
  - 确认上游容器/服务正在运行
  - 检查目标端口是否正确以及本地防火墙规则是否正确
- 重定向循环：
  - 避免重复启用 HTTPS（可能是应用程序和代理配置错误导致的）

## 发布前的检查清单

在共享或发布此配置之前：
- 删除所有真实的 IP 地址、域名、电子邮件地址和令牌信息。
- 仅保留占位符（如 `example.com` 和 `<npm-host>`）。
- 确保配置文件中不包含任何本地凭据文件路径或敏感信息。

## 安全规则

- 除非有明确要求，否则不要删除现有的生产环境代理主机。
- 对生产环境中的域名进行更改时，先创建配置快照或导出原有配置。
- 尽可能在测试环境中先应用更改。