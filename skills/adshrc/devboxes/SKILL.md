---
name: devboxes
description: 使用可通过网页访问的 VSCode、VNC 以及 Traefik 进行应用程序路由来管理开发环境容器（devboxes）。当用户需要创建、启动、停止、列出或管理 devboxes/开发环境，启动开发容器，设置编码沙箱，或首次配置 devbox 基础设施（入职培训）时，可使用这些工具。
---
# Devbox 技能

Devbox 是基于 OpenClaw 沙箱技术的容器，运行自定义镜像，其中包含 VSCode Web、noVNC、Chromium（CDP）以及最多 5 个应用程序端口，这些端口通过 Traefik 进行路由管理。

OpenClaw 负责管理整个容器的生命周期。容器会自动完成自我注册：入口脚本会自动分配一个 ID，生成 Traefik 路由，并设置 `APP_URL_*` 环境变量。主代理仅负责启动容器并报告相应的 URL 地址。

## 文件位置

所有脚本都保存在技能的 `scripts/` 目录中。路径引用均相对于此 SKILL.md 文件的父目录。

**关键文件：**
- `scripts/Dockerfile` 和 `scripts/entrypoint.sh`：用于构建 devbox 镜像（发布地址为 `ghcr.io/adshrc/openclaw-devbox:latest`）
- `scripts/.devbox-counter`：用于记录容器实例的顺序 ID（通过挂载到 `/shared/.devbox-counter` 文件中）

## 架构

- **代理 ID：** `devbox`（在 `openclaw.json` 中配置）
- **沙箱模式：** `all` 或 `scope: session`（每个会话对应一个容器）
- **镜像：** `ghcr.io/adshrc/openclaw-devbox:latest`（从 GitHub Container Registry （GHCR）拉取，不进行本地构建）
- **网络：** `traefik`（用于路由管理和 Git 访问）
- **浏览器：** `sandbox.browser.enabled: true`，通过端口 9222 使用 CDP 协议

### 自我注册（入口脚本）

容器入口脚本会自动执行以下操作：
1. 读取并递增 `/shared/.devbox-counter` 文件中的计数器值，从而生成 `DEVBOX_ID`。
2. 根据标签、域名和 ID 生成 `APP_URL_1..5`、`VSCODE_URL`、`NOVNC_URL`。
3. 将这些信息写入 `/etc/devbox.env` 和 `/etc/profile.d/devbox.sh`（在所有 shell 环境中可用）。
4. 将 Traefik 配置写入 `/traefik/devbox-{id}.yml` 文件（Traefik 会自动读取该配置）。

### 挂载配置（在 `openclaw.json` 中配置）

| 代理路径            | Devbox 容器路径            | 用途                |
|------------------|------------------|-------------------|
| `scripts/.devbox-counter`     | `/shared/.devbox-counter`       | 用于存储容器实例 ID          |
| `/etc/traefik/dynamic`     | `/traefik`             | 用于存储 Traefik 动态配置        |

**注意：** 以上两个路径必须具有写入权限（`chmod 666` 或 `chmod 777`），因为沙箱容器运行时具有 `CapDrop: ALL` 权限。

### 固定路径

在 OpenClaw 容器内部，以下路径始终不变：
- **OpenClaw 数据目录：** `/home/node/.openclaw`
- **Traefik 动态配置目录：** `/etc/traefik/dynamic`（必须挂载到容器中）

如果 `/etc/traefik/dynamic` 不存在，说明 OpenClaw 容器未正确挂载该目录。用户需要在 `docker run` 命令中添加 `-v $HOME/traefik/dynamic:/etc/traefik/dynamic` 并重新启动容器。

## 上线流程

该流程在 **主代理** 上执行，而非沙箱环境中。主代理具有 `exec`、`gateway` 和文件系统的访问权限。

当用户请求设置 Devbox 技能时，执行以下步骤：

### 第 1 步：收集信息并确定路径

- 询问用户以下信息：
  - **域名**：使用通配符 DNS（如 `*.domain`）指向目标服务器（例如 `oc.example.com`）
  - **GitHub 令牌**（可选）：用于在 Devbox 内部克隆私有仓库

### 第 2 步：检查前提条件

```bash
# Docker access
docker info > /dev/null 2>&1

# Traefik network exists
docker network ls | grep traefik

# Check that /etc/traefik/dynamic is mounted
ls /etc/traefik/dynamic

# Pull the image (NOT build)
docker pull ghcr.io/adshrc/openclaw-devbox:latest
```

- 如果 `traefik` 网络不存在，执行 `docker network create traefik` 命令创建网络。
- 如果 `/etc/traefik/dynamic` 不存在，提示用户需要在 `docker run` 命令中添加 `-v $HOME/traefik/dynamic:/etc/traefik/dynamic` 并重新启动容器。

### 第 3 步：创建计数器文件

```bash
# Relative to this skill's directory
echo "0" > scripts/.devbox-counter
chmod 666 scripts/.devbox-counter
```

### 第 4 步：确保 Traefik 动态配置目录可写

```bash
chmod 777 /etc/traefik/dynamic
```

### 第 5 步：配置 OpenClaw

使用 `gateway config.patch` 命令添加 Devbox 代理。**切勿** 让用户手动编辑 `openclaw.json`。正确的操作是使用该命令将 Devbox 代理添加到代理列表中：

```json
{
  "agents": {
    "list": [
      {
        "id": "devbox",
        "name": "Devbox",
        "sandbox": {
          "mode": "all",
          "workspaceAccess": "none",
          "scope": "session",
          "browser": {
            "enabled": true,
            "cdpPort": 9222
          },
          "docker": {
            "image": "ghcr.io/adshrc/openclaw-devbox:latest",
            "readOnlyRoot": false,
            "network": "traefik",
            "env": {
              "DEVBOX_DOMAIN": "{domain}",
              "APP_TAG_1": "api",
              "APP_TAG_2": "app",
              "APP_TAG_3": "dashboard",
              "APP_TAG_4": "app4",
              "APP_TAG_5": "app5",
              "ENABLE_VNC": "true",
              "ENABLE_VSCODE": "true",
              "GITHUB_TOKEN": "{github_token}"
            },
            "binds": [
              "/home/node/.openclaw/workspace/skills/devbox/scripts/.devbox-counter:/shared/.devbox-counter:rw",
              "/etc/traefik/dynamic:/traefik:rw"
            ]
          }
        }
      }
    ]
  }
}
```

**注意：** 在应用配置更新时，首先需要读取当前配置（`gateway config.get`），然后将 Devbox 代理信息合并到现有的 `agents.list` 数组中，并确保主代理的配置中包含 `subagents: { allowAgents: ["devbox"]`。最后使用 `gateway config.apply` 应用更新。

### 第 6 步：测试

重新启动 OpenClaw 后，启动一个测试容器以验证自我注册功能和 URL 是否正常工作。

## 启动 Devbox 的工作流程

### 第 1 步：启动子代理（由主代理执行）

```python
sessions_spawn(
    agentId="devbox",
    label="devbox-{task_name}",
    task="Your task description. GitHub token is in $GITHUB_TOKEN. Env vars (DEVBOX_ID, APP_URL_*, etc.) are in your shell via `source /etc/profile.d/devbox.sh`."
)
```

至此，容器即可完成自我注册，无需手动分配 ID 或配置 Traefik。

### 第 2 步：向用户报告 URL 地址（由主代理执行）

读取计数器值以获取分配的 ID，然后报告以下 URL：
- VSCode：`https://vscode-{id}.{domain}`
- noVNC：`https://novnc-{id}.{domain}/vnc.html`
- 应用程序 URL：`https://{tag}-{id}.{domain}`

### 清理

OpenClaw 负责管理容器的生命周期：会话结束后，容器会被自动删除。遗留的 Traefik 路由配置不会造成问题（Traefik 会针对失效的后端返回 502/404 错误）。

## 环境变量

### 静态变量（在 `openclaw.json` 中设置）

| 变量            | 示例值            | 说明                          |
|------------------|------------------|-----------------------------------|
| `GITHUB_TOKEN`      | `ghp_...`          | 用于克隆仓库的 GitHub 令牌                |
| `DEVBOX_DOMAIN`     | `oc.example.com`       | 域名基础地址                      |
| `APP_TAG_1..5`     | `api`, `app`, ...       | 应用程序的路由标签                    |
| `ENABLE_VNC`       | `true`           | 是否启用 noVNC                      |
| `ENABLE_VSCODE`      | `true`           | 是否启用 VSCode Web                    |

### 动态变量（由入口脚本生成，在所有 shell 中可用）

| 变量            | 示例值            | 说明                          |
|------------------|------------------|-----------------------------------|
| `DEVBOX_ID`       | `1`             | 自动分配的顺序 ID                    |
| `APP_URL_1..5`     | `https://api-1.oc.example.com`     | 各应用程序的完整 URL                    |
| `APP_PORT_1..5`     | `8003..8007`       | 应用程序的内部端口                      |
| `VSCODE_URL`      | `https://vscode-1.oc.example.com`     | VSCode Web 的 URL                      |
| `NOVNC_URL`      | `https://novnc-1.oc.example.com/vnc.html`     | noVNC 的 URL                        |

## 端口配置

| 端口            | 服务                          |
|------------------|------------------|--------------------------------------|
| 8000            | VSCode Web                        |
| 8002            | noVNC                          |
| 9222            | Chromium DevTools 协议（CDP）                |
| 8003-8007         | 应用程序端口（1-5）                    |

## 浏览器

Devbox 代理通过 Chromium 的 CDP 协议（端口 9222）访问外部资源。子代理可以使用 `browser` 工具在容器内导航、截图和与应用程序交互（使用 `http://localhost:{port}`）。

## 项目设置脚本

项目可以包含 `.openclaw/setup.sh` 脚本，该脚本在 Devbox 内部执行。脚本可以通过 `/etc/profile.d/devbox.sh` 访问所有环境变量（如 `APP_URL_*`、`APP_PORT_*`、`DEVBOX_ID` 等）。

有关编写脚本的规范，请参考 `references/setup-script-guide.md`。