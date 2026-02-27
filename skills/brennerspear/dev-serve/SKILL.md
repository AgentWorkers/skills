---
name: dev-serve
description: 通过 Caddy 在通配符子域名下启动和管理由 tmux 支持的开发服务器。
---
# dev-serve — 一键式开发服务器托管服务

您可以通过 `tmux` 会话启动开发服务器，并通过 Caddy 将其暴露在 `<project>.YOUR_DOMAIN` 地址上。只需执行一条命令即可启动或关闭服务器。

## 设置

1. **安装脚本：**
   ```bash
   cp scripts/dev-serve.sh ~/.local/bin/dev-serve
   chmod +x ~/.local/bin/dev-serve
   ```

2. **设置您的域名**：
   - 在您的 shell 配置文件中设置 `DEV_SERVE_DOMAIN` 变量；
   - 或者直接编辑脚本中的 `DOMAIN` 变量。

3. **系统要求：**
   - 运行中的 Caddy 服务，支持通配符 DNS 和 TLS 协议（详情请参考 [caddy](https://clawhub.com/skills/caddy) 技能文档）；
   - 需要 `tmux`、`jq` 和 `curl` 工具；
   - Caddy 的管理 API 需要访问 `localhost:2019`。

## 命令行接口 (CLI)

```bash
dev-serve up <repo-path> [port]      # Start dev server + add Caddy route
dev-serve down <name>                # Stop dev server + remove Caddy route
dev-serve ls                         # List active dev servers
dev-serve restart <name>             # Restart dev server (keep Caddy route)
```

## 工作原理

1. 从仓库文件夹名称生成子域名（例如：`~/projects/myapp` → `myapp.YOUR_DOMAIN`）；
2. 从 `package.json` 文件的 `scripts.dev` 部分检测到启动开发服务器的命令（支持 Vite、Next、Nuxt、SvelteKit 等框架）；
3. 如果存在 Vite 配置文件，会自动更新 `allowedHosts` 列表；
4. 在名为 `dev-<name>` 的 `tmux` 会话中启动开发服务器，参数为 `--host 0.0.0.0 --port <port>`；
5. 在 `Caddyfile` 中配置相应的路由和仪表板链接；
6. 通过 Caddy 的管理 API 重新加载配置（无需使用 `sudo` 或重启服务器）；
7. 进行端到端验证：等待服务器启动后，通过 HTTPS 协议发送请求并检查响应状态（确保返回 2xx 或 3xx 状态码，最长等待时间 90 秒）。

## 示例

```bash
# Start with auto-assigned port (starts at 5200, skips used ports)
dev-serve up ~/projects/myapp
# → https://myapp.YOUR_DOMAIN

# Explicit port
dev-serve up ~/projects/myapp 5200

# Override dev command
DEV_CMD="bun dev" dev-serve up ~/projects/myapp 5300

# Stop and clean up
dev-serve down myapp

# List what's running
dev-serve ls
```

## 配置参数

| 参数          | 默认值       | 说明                                      |
|---------------|------------|-----------------------------------------|
| `DEV_SERVE_DOMAIN` | （必须设置）    | 您的通配符域名（例如：`mini.example.com`）             |
| `DEV_SERVE_STATE_DIR` | `~/.config/dev-serve` | 存储状态数据的目录                          |
| `CADDYFILE`     | `~/.config/caddy/Caddyfile` | Caddy 配置文件的路径                        |
| `CADDY_ADMIN`     | `http://localhost:2019` | Caddy 管理 API 的地址                        |
| `DEV_CMD`       | （自动检测）     | 用于启动开发服务器的命令                         |

## 端口约定

- **永久性服务**：使用 3100 系列端口（直接在 `Caddyfile` 中配置）；
- **开发服务器**：使用 5200 系列端口（由 `dev-serve` 自动分配）。

## Vite 的 `allowedHosts` 设置

Vite 会阻止来自未知主机的请求。`dev-serve` 会自动更新 `vite.config.ts` 文件（或 `.js`/`.mts`/`.mjs` 文件），以允许特定的子域名访问。如果自动更新失败，系统会提示手动修改配置。

## 架构图

```
Browser (Tailscale / LAN / etc.)
  → DNS: *.YOUR_DOMAIN → your server IP
    → Caddy (HTTPS with auto certs)
      → reverse_proxy localhost:<port>
        → Dev server (in tmux session)
```

## 相关技能

- **[caddy](https://clawhub.com/skills/caddy)**：必需技能。用于配置支持通配符和 TLS 协议的 Caddy 反向代理。

## 常见问题解决方法

- **开发服务器无法启动：**  
  ```bash
tmux attach -t dev-<name>    # see what happened
```

- **证书配置失败（curl 命令返回错误码 35）：**  
  等待 30–60 秒，直到 DNS-01 挑战完成。查看 `/var/log/caddy-error.log` 日志文件。

- **Caddy 重新加载失败：**  
  ```bash
caddy reload --config ~/.config/caddy/Caddyfile --address localhost:2019
```

- **Vite 报错 403：**  
  子域名未添加到 `allowedHosts` 列表中。请手动在 `vite.config.ts` 文件中添加该域名：  
  ```ts
server: { allowedHosts: ['myapp.YOUR_DOMAIN'] }
```