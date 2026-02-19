---
name: devboxes
description: 使用可通过网页访问的 VSCode、VNC 以及通过 Traefik 或 Cloudflare Tunnels 进行的应用程序路由功能来管理开发环境容器（devboxes）。当用户需要创建、启动、停止、列出或管理 devboxes/开发环境、启动开发容器、设置编码沙箱，或首次配置 devbox 基础设施（入职培训时）时，可使用这些工具。
---
# Devbox 技能

Devbox 是一个基于 OpenClaw 沙箱的容器，运行自定义镜像，其中包含 VSCode Web、noVNC、Chromium（CDP）以及最多 5 个应用程序端口。这些端口通过 **Traefik** 或 **Cloudflare Tunnels** 进行路由。

OpenClaw 负责管理整个容器的生命周期。容器会自动完成注册过程：入口点会自动分配一个 ID，生成 Traefik 路由规则，并设置 `APP_URL_*` 环境变量。主代理仅负责生成并报告各个应用程序的 URL。

## 文件位置

所有路径均相对于本 SKILL.md 文件的父目录计算。

**关键文件：**
- `references/setup-script-guide.md` — 项目设置脚本（如 `.openclaw/setup.sh`）的规范

## 架构

- **代理 ID：** `devbox`（在 `openclaw.json` 中配置）
- **沙箱模式：** `all` 或 `scope: session` — 每个会话使用一个容器
- **镜像：** `ghcr.io/adshrc/openclaw-devbox:latest`（从 GitHub Container Registry 下载）
- **网络：** `traefik`（用于 Traefik 路由）或默认的 Docker 网络（用于 Cloudflare Tunnel 路由）
- **浏览器：** `sandbox.browser.enabled: true`，在端口 9222 上启用 CDP

### 自动注册（入口点）

容器的入口点会自动执行以下操作：
1. 读取并递增 `/shared/.devbox-counter` 文件中的计数器值，从而生成 `DEVBOX_ID`。
2. 根据标签、域名和 ID 生成 `APP_URL_1..5`、`VSCODE_URL`、`NOVNC_URL`。
3. 将相关信息写入 `/etc/devbox.env` 和 `/etc/profile.d/devbox.sh`（这两个文件在所有 shell 中可用）。
4. 根据 `ROUTING_MODE` 的设置进行路由配置：
   - **`traefik`（默认模式）：将 Traefik 配置写入 `/traefik/devbox-{id}.yml` 文件。
   - **`cloudflared`：生成 Cloudflare 入口配置文件，通过 CF API 注册 DNS CNAME 记录，并启动 Cloudflare 隧道。

### 绑定挂载（在 `openclaw.json` 中配置）

| 代理路径                                      | Devbox 容器路径                | 用途                          |
| -------------------------------------- | ------------------------- | -------------------------------------- |
| `/home/node/.openclaw/.devbox-counter`          | `/shared/.devbox-counter`         | 用于记录容器 ID                      |
| `/home/node/.openclaw/traefik`                | `/traefik`                | 用于存储 Traefik 路由配置                |

**注意：** 这两个路径必须对沙箱容器具有写入权限（UID 1000）。计数器文件需要设置为 `chmod 666`，并且 Traefik 相关目录的权限应设置为 `1000:1000`（在主机配置时设置）。

### 固定路径

在 OpenClaw 容器内部，以下路径始终是不变的：
- **OpenClaw 数据目录：** `/home/node/.openclaw`
- **Traefik 动态配置文件：** `/home/node/.openclaw/traefik`（仅在使用 Traefik 路由时需要挂载）

## 上线流程

**重要提示：** 安装此技能后，必须按照以下流程进行上线配置。用户必须完成上线流程并设置好基础设施后才能使用 Devbox 技能。

**此流程在主代理上执行，而不是在沙箱环境中。** 主代理具有 `exec`、`gateway` 和文件系统的访问权限。

当用户请求设置 Devbox 技能时，请按照以下步骤操作：

### 第 1 步：验证 Docker 前提条件

确认用户可以访问 Docker 套接字和 Docker 可执行文件：
```bash
which docker
docker version
```

如果无法访问，请让用户运行以下命令来启动 OpenClaw 容器：
```
-v /usr/bin/docker:/usr/bin/docker:ro
-v /var/run/docker.sock:/var/run/docker.sock
```

并手动将 `/var/run/docker.sock` 的权限设置为 `666`，以便 OpenClaw 容器能够正常工作。之后用户可以重新尝试设置 Devbox 技能。

### 第 2 步：验证主机路径映射

确定 `/home/node/.openclaw` 在容器内的实际路径：
```bash
# Returns the host path that is mapped to /home/node/.openclaw inside the container
docker inspect --format='{{range .Mounts}}{{if eq .Destination "/home/node/.openclaw"}}{{.Source}}{{end}}{{end}}' $(hostname)
```

将此路径存储为 `HOST_OPENCLAW_PATH`。如果 `HOST_OPENCLAW_PATH` 是系统目录，OpenClaw 无法创建 Devbox 容器。

系统目录包括：/etc、/private/etc、/proc、/sys、/dev、/root、/boot、/run、/var/run、/private/var/run、/var/run/docker.sock、/private/var/run/docker.sock 和 /run/docker.sock。

如果 `HOST_OPENCLAW_PATH` 是系统目录，请让用户更改 OpenClaw 容器的配置，使用非系统目录作为数据存储路径。例如，可以在主机上创建 `/home/openclaw` 或 `/opt/openclaw` 目录。

### 第 3 步：收集信息并确定路径

询问用户以下信息：
- **路由模式**：使用 Traefik 还是 Cloudflare Tunnel？
- **域名**：需要设置一个通配符 A 记录指向服务器（例如 `*.example.com`）
- **GitHub 令牌**（可选）：用于在 Devbox 中克隆私有仓库

如果选择 **Cloudflare Tunnel**，还需询问以下信息：
- **Cloudflare API 令牌**：用户需要具备编辑 DNS 和隧道配置的权限

### 第 4 步：验证前提条件

#### 如果使用 Traefik 路由模式：

```bash
# Check that /home/node/.openclaw/traefik is mounted
ls /home/node/.openclaw/traefik
```

如果 `/home/node/.openclaw/traefik` 不存在，请让用户将 `-v path_to_traefik:/home/node/.openclaw/traefik` 添加到 OpenClaw 容器的配置中，然后重启容器。

#### 如果使用 Cloudflare Tunnel：

验证 Cloudflare API 令牌和域名：
```bash
# 1. Verify token is valid
curl -s -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" | jq .

# 2. Get zone ID for the domain (extract root domain from the provided domain)
curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=${ROOT_DOMAIN}" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" | jq .

# 3. Get account ID from the zone response
# account_id = .result[0].account.id
# zone_id = .result[0].id
```

之后创建隧道：
```bash
# 4. Create a named tunnel
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/cfd_tunnel" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"name": "openclaw-devboxes", "tunnel_secret": "'$(openssl rand -base64 32)'"}' | jq .

# Extract tunnel_id and tunnel_token from the response
# tunnel_id = .result.id
# tunnel_token = .result.token
```

将以下信息存储起来：`CF_API_TOKEN`、`CF_ZONE_ID`、`CF_ACCOUNT_ID`、`CF_TUNNEL_ID`、`CF_TUNNEL_TOKEN`。

### 第 5 步：创建计数器文件

```bash
echo "0" > /home/node/.openclaw/.devbox-counter
chmod 666 /home/node/.openclaw/.devbox-counter
```

**注意：** 计数器值不会被重置，只会持续递增。

### 第 6 步：配置 OpenClaw

首先检查当前的代理配置：
```bash
node /app/openclaw.mjs config get agents
```

然后根据现有配置调整相关设置：

#### 主代理

- 如果存在 `default: true` 的代理，请记录其索引，并将其添加到 `subagents.allowAgents` 列表中：
```bash
node /app/openclaw.mjs config set agents.list[{index}].subagents.allowAgents '["devbox"]' --json
```

（如果需要，将沙箱模式设置为 `off`，因为主代理不需要沙箱环境）：
```bash
node /app/openclaw.mjs config set agents.list[{index}].sandbox.mode "off"
```

**否则**，在列表中的下一个索引处创建一个新的代理，并设置相应的配置：
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

#### Devbox 代理

1. 下载 Docker 镜像，确保 OpenClaw 可以使用该镜像：
```bash
docker pull ghcr.io/adshrc/openclaw-devbox:latest
```

2. 在 `agents.list` 中为 Devbox 代理添加相应的配置。根据需要调整沙箱和 Docker 配置（请使用占位符）：
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
          "{host_openclaw_path}/.devbox-counter:/shared/.devbox-counter:rw",
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

3. 设置代理之间的通信权限，以便后续任务能够发送到 Devbox 代理：
```bash
node /app/openclaw.mjs config set tools.agentToAgent.enabled true
node /app/openclaw.mjs config set tools.sessions.visibility "all"
```

完成这些配置后，重启 Gateway 以应用更改。如果重启后问题仍然存在（例如某些命令无法执行），请让用户手动重启 OpenClaw 容器。

## 工作流程：创建 Devbox 容器

### 第 1 步：创建子代理（主代理）

```python
sessions_spawn(
    agentId="devbox",
    label="devbox-{task_name}",
    task="Your task description. GitHub token is in $GITHUB_TOKEN. Env vars (DEVBOX_ID, APP_URL_*, etc.) are in your shell via `source /etc/profile.d/devbox.sh`. ALWAYS use /workspace as the working directory! When cloning, the structure must be /workspace/<repo>."
)
```

完成后，容器会自动完成注册过程，无需手动分配 ID 或配置 Traefik 路由。

### 第 2 步：向用户报告应用程序的 URL（主代理）

读取计数器值以获取分配的 ID，然后报告以下 URL：
- VSCode：`https://vscode-{id}.{domain}`
- noVNC：`https://novnc-{id}.{domain}/vnc.html`
- 应用程序 URL：`https://{tag}-{id}.{domain}`

### 清理

OpenClaw 负责管理容器的生命周期——会话结束后容器会被自动删除。遗留的 Traefik 路由配置不会造成问题。

## 环境变量

### 静态变量（在 `openclaw.json` 中的 `sandbox.docker.env` 中设置）

| 变量                | 示例值                         | 说明                                      |
| ---------------------- | -------------------------------------- | -------------------------------------- |
| `ROUTING_MODE`       | `traefik` 或 `cloudflared`         | 路由后端（默认：`traefik`）                     |
| `GITHUB_TOKEN`        | `ghp_...`                        | 用于克隆私有仓库的 GitHub 令牌                |
| `DEVBOX_DOMAIN`       | `oc.example.com`                    | 基础域名                                  |
| `APP_TAG_1..5`        | `app1`、`app2` 等                     | 应用程序标签                              |
| `ENABLE_VNC`          | `true`                          | 是否启用 noVNC                                  |
| `ENABLE_VSCODE`        | `true`                          | 是否启用 VSCode Web                            |
| `CF_TUNNEL_TOKEN`       | `eyJ...`                        | Cloudflare 隧道运行令牌                          |
| `CF_API_TOKEN`        | `abc123`                        | 用于 DNS 注册的 Cloudflare API 令牌                |
| `CF_ZONE_ID`        | `xyz789`                        | 用于配置 Cloudflare 隧道的域名 ID                |
| `CF_TUNNEL_ID`        | `uuid`                          | Cloudflare 隧道的 ID                              |

### 动态变量（由入口点生成，在所有 shell 中可用）

| 变量                | 示例值                         | 说明                                      |
| ---------------------- | -------------------------------------- | -------------------------------------- |
| `DEVBOX_ID`          | `1`                            | 自动生成的序列 ID                              |
| `APP_URL_1..5`        | `https://app1-1.oc.example.com`                   | 各应用程序的完整 URL                          |
| `APP_PORT_1..5`        | `8003..8007`                        | 应用程序的内部端口                          |
| `VSCODE_URL`        | `https://vscode-1.oc.example.com`                   | VSCode Web 的 URL                              |
| `NOVNC_URL`          | `https://novnc-1.oc.example.com/vnc.html`                | noVNC 的 URL                              |

### 端口

| 端口                | 服务                          |
| ---------------------- | -------------------------------------- |
| 8000                | VSCode Web                              |
| 8002                | noVNC                                  |
| 9222                | Chromium DevTools 协议（CDP）                   |
| 8003-8007            | 应用程序端口（1-5）                          |

## 浏览器

Devbox 代理通过 Chromium 的 CDP 功能访问网页（端口 9222）。子代理可以使用 `browser` 工具在容器内导航、截图和与应用程序交互（使用 `http://localhost:{port}`）。

## 项目设置脚本

项目可以包含 `.openclaw/setup.sh` 脚本，该脚本在 Devbox 内运行。脚本可以通过 `/etc/profile.d/devbox.sh` 访问所有环境变量（如 `APP_URL_*`、`APP_PORT_*`、`DEVBOX_ID` 等）。

具体规范请参考 `references/setup-script-guide.md`。