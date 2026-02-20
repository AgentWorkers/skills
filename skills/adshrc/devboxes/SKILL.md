---
name: devboxes
description: 使用可通过网页访问的 VSCode、VNC 以及通过 Traefik 或 Cloudflare Tunnels 进行的应用程序路由来管理开发环境容器（devboxes）。当用户需要创建、启动、停止、列出或管理 devboxes/开发环境，搭建开发容器，设置编码沙盒，或首次配置 devbox 基础设施（入职培训）时，可使用这些工具。
---
# Devbox 技能

Devbox 是基于 OpenClaw 沙箱技术的容器，运行自定义镜像，其中包含 VSCode Web、noVNC、Chromium（CDP）以及最多 5 个应用程序端口。这些端口通过 **Traefik** 或 **Cloudflare Tunnels** 进行路由。

OpenClaw 负责管理整个容器的生命周期。**主代理** 通过维护一个本地计数文件来为每个 Devbox 分配一个唯一的序列 ID，并将该 ID 传递给子代理任务。入口脚本（entrypoint）使用这个 ID 来配置 Traefik 路由并设置 `APP_URL_*` 环境变量。

## 文件位置

所有文件路径均相对于本 SKILL.md 的父目录。

**关键文件：**
- `references/setup-script-guide.md` — 项目设置脚本（`.openclaw/setup.sh`）的规范

## 架构

- **代理 ID：** `devbox`（在 `openclaw.json` 中配置）
- **沙箱模式：** `all` 或 `scope: session` — 每个会话使用一个容器
- **镜像：** `ghcr.io/adshrc/openclaw-devbox:latest`（从 GitHub Container Registry 下载）
- **网络：** `traefik`（用于 Traefik 路由）或默认的 Docker 网络（用于 Cloudflare Tunnel 路由）
- **浏览器：** `sandbox.browser.enabled: true`，通过端口 9222 使用 CDP

### ID 分配

**主代理** 的工作流程如下：
1. 在启动容器之前，读取并递增 `/home/node/.openclaw/.devbox-counter` 文件中的计数值。
2. 将分配的 `DEVBOX_ID` 通过任务描述传递给 Devbox 代理。
3. Devbox 代理必须将 `DEVBOX_ID` 设置为它的第一个环境变量。

### 入口脚本（entrypoint）

容器启动时，入口脚本会检查 `DEVBOX_ID` 是否已经作为环境变量存在，然后执行以下操作：
1. 根据 ID 构建 `APP_URL_1..5`、`VSCODE_URL`、`NOVNC_URL` 等环境变量。
2. 将配置写入 `/etc/devbox.env` 和 `/etc/profile.d/devbox.sh`（这两个文件在所有 shell 中都可用）。
3. 根据 `ROUTING_MODE` 的设置进行路由配置：
   - **`traefik`（默认模式）：将 Traefik 配置写入 `/traefik/devbox-{id}.yml` 文件。
   - **`cloudflared`：生成 Cloudflare 入口配置，通过 CF API 注册 DNS CNAME 记录，并启动 Cloudflare 隧道。

### 绑定挂载（在 `openclaw.json` 中配置）

| 代理路径                  | Devbox 容器路径                | 目的                                      |
| ------------------------------ | --------------------- | --------------------------------------------- |
| `/home/node/.openclaw/traefik` | `/traefik`            | 用于存储 Traefik 路由配置                        |

**重要说明：** 由于 OpenClaw 的安全限制，所有用户的权限默认被禁用。即使在 Devbox 中以 root 用户身份，也无法写入这些绑定挂载的目录，只能读取。目前的解决方法是在主机上将 `/home/node/.openclaw/traefik` 的路径设置为 `chmod 777` 权限。

### 固定路径

在 OpenClaw 容器内部，以下路径始终是固定的：
- **OpenClaw 数据目录：** `/home/node/.openclaw`
- **Traefik 动态配置文件：** `/home/node/.openclaw/traefik`（仅在使用 Traefik 路由时需要挂载）

## 上线流程

**重要说明：** 安装此技能后，必须按照以下流程完成上线配置。在完成上线流程并设置好基础设施之前，用户无法使用 Devbox 技能。

**注意：** 此流程在 **主代理** 上执行，而不是在沙箱环境中。主代理具有 `exec`、`gateway` 和文件系统的访问权限。

当用户请求设置 Devbox 技能时，请按照以下步骤操作：

### 第 1 步：验证 Docker 访问权限

确认您能够访问 Docker 套接字和 Docker 可执行文件：

```bash
which docker
docker version
```

如果无法访问，请中止操作，并告知用户需要运行 OpenClaw 容器，并执行以下命令：

```
-v /usr/bin/docker:/usr/bin/docker:ro
-v /var/run/docker.sock:/var/run/docker.sock
```

同时，用户还需要在主机上手动设置 `chmod 666 /var/run/docker.sock`，以便 OpenClaw 容器能够正常工作。完成这些操作后，用户可以再次请求设置 Devbox 技能。

### 第 2 步：收集配置信息

询问用户以下信息：
- **路由模式**：使用 Traefik 还是 Cloudflare Tunnel？
- **域名**：需要一个指向服务器的通配符 A 记录（例如 `*.example.com`）
- **GitHub 令牌**（可选）：用于在 Devbox 中克隆私有仓库

如果选择 **Cloudflare Tunnel**，还需要提供：
- **Cloudflare API 令牌**：该令牌需具备编辑 DNS 和 Tunnel 的权限

### 第 3 步：验证主机路径（仅在使用 Traefik 路由时需要）

确定 `/home/node/.openclaw` 在容器内的实际路径：

```bash
# Returns the host path that is mapped to /home/node/.openclaw inside the container
docker inspect --format='{{range .Mounts}}{{if eq .Destination "/home/node/.openclaw"}}{{.Source}}{{end}}{{end}}' $(hostname)
```

将此路径存储为 `HOST_OPENCLAW_PATH` 变量。如果 `HOST_OPENCLAW_PATH` 是系统目录，OpenClaw 无法创建 Devbox 容器。系统目录包括：/etc、/private/etc、/proc、/sys、/dev、/root、/boot、/run、/var/run、/private/var/run、/var/run/docker.sock、/private/var/run/docker.sock 和 /run/docker.sock。

如果 `HOST_OPENCLAW_PATH` 是系统目录，请中止操作，并告知用户需要更改 OpenClaw 容器的配置，使用非系统目录作为数据存储路径。例如，可以在主机上创建 `/home/openclaw` 或 `/opt/openclaw` 目录。

### 第 4 步：验证路由配置

#### 如果使用 Traefik 路由：
- 检查 `/home/node/.openclaw/traefik` 是否已正确挂载：

```bash
ls /home/node/.openclaw/traefik
```

如果未找到该目录，请中止操作，并告知用户需要在 OpenClaw 容器中添加挂载配置（例如 `-v path_to_traefik:/home/node/.openclaw/traefik`），然后重启容器。请注意，不能使用系统目录作为主机路径（这是 OpenClaw 沙箱的限制）。重启容器后，用户可以再次请求设置 Devbox 技能。

#### 如果使用 Cloudflare Tunnel：
- 验证 Cloudflare API 令牌和域名是否正确：

```bash
# 1. Get zone ID for the domain (extract root domain from the provided domain)
curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=${ROOT_DOMAIN}" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" | jq .

# 2. Get account ID from the zone response
# account_id = .result[0].account.id
# zone_id = .result[0].id
```

然后创建 Cloudflare 隧道：

```bash
# 4. Create a named tunnel
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/cfd_tunnel" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"name": "devboxes@'"$(hostname)"'", "config_src": "local", "tunnel_secret": "'$(openssl rand -base64 32)'"}' | jq .

# Extract tunnel_id and tunnel_token from the response
# tunnel_id = .result.id
# tunnel_token = .result.token
```

将相关配置值（`CF_API_TOKEN`、`CF_ZONE_ID`、`CF_ACCOUNT_ID`、`CF_TUNNEL_ID`、`CF_TUNNEL_TOKEN`）存储起来。

### 第 5 步：创建计数文件

```bash
echo "0" > /home/node/.openclaw/.devbox-counter
```

**重要说明：** 计数文件仅由主代理管理。计数文件只能递增，不能被重置或递减。

### 第 6 步：配置 OpenClaw

- 首先检查当前代理的配置：
```bash
node /app/openclaw.mjs config get agents
```

- 根据现有配置判断是否需要调整：
  - **主代理**：如果存在 `default: true` 的代理，请记录其索引，并在配置中添加 `subagents.allowAgents` 选项：
    ```bash
node /app/openclaw.mjs config set agents.list[{index}].subagents.allowAgents '["devbox"]' --json
```

  - 如果需要，将沙箱模式设置为 `off`（因为主代理不需要沙箱环境）：
    ```bash
node /app/openclaw.mjs config set agents.list[{index}].sandbox.mode "off"
```

  - 如果没有 `default: true` 的代理，可以在下一个索引位置创建一个新的代理：
    ```bash
node /app/openclaw.mjs config set agents.list[{index}] '{
  "id": "main",
  "default": true,
  "subagents": {
    "allowAgents": [
        "devbox"
    ]
  },
  "sandbox": {
    "mode": "off"
  }
}' --json
```

### 第 7 步：配置 Devbox 代理

  - 下载 Docker 镜像，确保 OpenClaw 可以正常使用该镜像：
    ```bash
docker pull ghcr.io/adshrc/openclaw-devbox:latest
```

  - 在 `agents.list` 中为 Devbox 代理添加相应的配置（包括沙箱和 Docker 配置）：
    ```bash
node /app/openclaw.mjs config set agents.list[{index}] '{
    "id": "devbox",
    "name": "Devbox Agent",
    "sandbox": {
      "mode": "all",
      "workspaceAccess": "none",
      "scope": "session",
      "docker": {
        "image": "ghcr.io/adshrc/openclaw-devbox:latest",
        "readOnlyRoot": false,
        "network": "traefik", # Only needed for Traefik routing mode, exclude otherwise
        "env": {
          "ENABLE_VNC": "true",
          "ENABLE_VSCODE": "true",
          "DEVBOX_DOMAIN": "{domain}",
          "APP_TAG_1": "app1",
          "APP_TAG_2": "app2",
          "APP_TAG_3": "app3",
          "APP_TAG_4": "app4",
          "APP_TAG_5": "app5",
          "GITHUB_TOKEN": "{github_token}",
          "ROUTING_MODE": "{traefik|cloudflared}",
          # Cloudflare Tunnel variables (only needed if using cloudflared routing, exclude otherwise)
          "CF_TUNNEL_TOKEN": "{cf_tunnel_token}",
          "CF_API_TOKEN": "{cf_api_token}",
          "CF_ZONE_ID": "{cf_zone_id}",
          "CF_TUNNEL_ID": "{cf_tunnel_id}",
        },
        "binds": [
          "{host_openclaw_path}/traefik:/traefik:rw" # Only needed for Traefik routing mode, exclude otherwise
        ]
      },
      "browser": {
        "enabled": true,
        "cdpPort": 9222
      },
      "prune": {
        "idleHours": 0,
        "maxAgeDays": 0
      }
    }
  }
]' --json
```

  - 确保代理之间可以互相通信，以便后续任务能够发送到 Devbox 代理：
    ```bash
node /app/openclaw.mjs config set tools.agentToAgent.enabled true
node /app/openclaw.mjs config set tools.sessions.visibility "all"
```

完成这些配置后，重启 `gateway` 以应用更改。如果重启失败（例如某些命令被禁用），请用户手动重启 OpenClaw 容器。

## 工作流程：创建 Devbox 容器

### 第 1 步：为主代理分配 ID

读取并递增计数文件中的值：

```bash
DEVBOX_ID=$(( $(cat /home/node/.openclaw/.devbox-counter) + 1 ))
echo "$DEVBOX_ID" > /home/node/.openclaw/.devbox-counter
```

### 第 2 步：创建子代理（由主代理执行）

使用 `devbox-<id>` 作为标签，并在任务中包含 `DEVBOX_ID`：

```python
sessions_spawn(
    agentId="devbox",
    label=f"devbox-{DEVBOX_ID}",
    task=f"Your task description. Your DEVBOX_ID is {DEVBOX_ID} — run `export DEVBOX_ID={DEVBOX_ID}` as your very first action before doing anything else. GitHub token is in $GITHUB_TOKEN. After exporting DEVBOX_ID, env vars (APP_URL_*, etc.) are in your shell via `source /etc/profile.d/devbox.sh`. ALWAYS use /workspace as the working directory! When cloning, the structure must be /workspace/<repo>."
)
```

### 第 3 步：向用户提供应用程序 URL

主代理已经获取了分配的 ID，然后提供以下 URL：
- VSCode：`https://vscode-{DEVBOX_ID}.{domain}`
- noVNC：`https://novnc-{DEVBOX_ID}.{domain}/vnc.html`
- 应用程序 URL：`https://{tag}-{DEVBOX_ID}.{domain}`

### 清理

OpenClaw 负责管理容器的生命周期——会话结束后，容器会被自动删除。遗留的 Traefik 路由配置不会造成问题。

## 环境变量

### 静态变量（在 `openclaw.json` 的 `sandbox.docker.env` 中设置）

| 变量            | 示例值                          | 说明                                      |
| -----------------| -------------------------- | ---------------------------------------------------- |
| `ROUTING_MODE`     | `traefik` 或 `cloudflared`     | 路由后端（默认：`traefik`）                         |
| `GITHUB_TOKEN`     | `ghp_...`         | 用于克隆私有仓库的 GitHub 令牌                         |
| `DEVBOX_DOMAIN`     | `example.com`         | 域名基础地址                              |
| `APP_TAG_1..5`     | `app1`, `app2`, ...       | 应用程序标签                               |
| `ENABLE_VNC`       | `true`          | 是否启用 noVNC 功能                             |
| `ENABLE_VSCODE`     | `true`          | 是否启用 VSCode Web                            |
| `CF_TUNNEL_TOKEN`    | `eyJ...`         | Cloudflare 隧道运行令牌                         |
| `CF_API_TOKEN`     | `abc123`         | 用于 DNS 注册的 Cloudflare API 令牌                     |
| `CF_ZONE_ID`     | `xyz789`         | 域名的 Cloudflare 区域 ID                         |
| `CF_TUNNEL_ID`     | `uuid`          | Cloudflare 隧道的 ID                             |

### 动态变量（由入口脚本生成，在所有 shell 中可用）

| 变量            | 示例值                          | 说明                                      |
| -----------------| -------------------------------------- | --------------------------- |
| `DEVBOX_ID`       | `1`                          | 自动分配的序列 ID                             |
| `APP_URL_1..5`     | `https://app1-1.example.com`       | 各应用程序的完整 URL                              |
| `APP_PORT_1..5`     | `8003..8007`         | 应用程序的内部端口                             |
| `VSCODE_URL`     | `https://vscode-1.example.com`       | VSCode Web 的 URL                             |
| `NOVNC_URL`     | `https://novnc-1.example.com/vnc.html`     | noVNC 的 URL                             |

### 端口配置

| 端口            | 服务                          |
| -----------------| ------------------------------ |
| 8000            | VSCode Web                          |
| 8002            | noVNC                            |
| 9222            | Chromium DevTools 协议（CDP）                    |
| 8003-8007         | 应用程序端口（1-5）                        |

## 浏览器

Devbox 代理通过 Chromium 的 CDP 协议（端口 9222）访问外部资源。子代理可以使用 `browser` 工具在容器内导航、截图和操作应用程序（使用 `http://localhost:{port}`）。

## 项目设置脚本

项目可以包含 `.openclaw/setup.sh` 脚本，该脚本在 Devbox 内运行。脚本可以通过 `/etc/profile.d/devbox.sh` 访问所有环境变量（`APP_URL_*`、`APP_PORT_*`、`DEVBOX_ID` 等）。

有关更多规范，请参阅 `references/setup-script-guide.md`。