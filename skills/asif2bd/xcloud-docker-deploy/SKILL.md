---
name: xcloud-docker-deploy
description: "将任何 `docker-compose.yml` 文件适配以便在 xCloud 上部署。该方案解决了以下 4 个常见问题：  
(1) 需从源代码构建的应用程序——生成 GitHub Actions 脚本以完成构建并推送至 GitHub Container Registry (GHCR)；  
(2) 代理配置冲突（Caddy/Traefik/nginx-proxy）——解决这些冲突，并添加使用单一端口的 `nginx-router`；  
(3) 需要使用多个端口的应用程序——通过 `nginx-router` 对所有服务进行路由；  
(4) 外部配置文件——将配置文件内嵌到 `docker-compose.yml` 中。  
适用于用户希望在 xCloud 上部署 Docker 应用程序，但其 `docker-compose.yml` 文件与 xCloud 的要求不兼容的情况，或者希望让现有的应用程序能够在 xCloud 上正常运行的场景。"
license: Apache-2.0
metadata:
  version: 1.0.0
  author: Asif2BD
  homepage: https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill
  source: https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill
  tags: docker, xcloud, deployment, devops, docker-compose
  platforms: openClaw, claude-code, claude-ai, cursor, windsurf, any
  security_verified: true
  no_network_calls: true
  no_executables: true
---
# 使用 xCloud 进行 Docker 部署

请根据实际情况调整 `docker-compose.yml` 文件，以使其能够与 [xCloud](https://xcloud.host) 配合使用——这是一个基于 Git Push 的 Docker 部署平台。

## xCloud 的工作原理

```
git push → xCloud runs: docker-compose pull && docker-compose up -d
```

**xCloud 从不执行 `docker build` 命令**。所有 Docker 镜像必须预先构建在公共注册库中。xCloud 负责处理 SSL、反向代理和域名路由功能——您的应用程序代码中不应重复实现这些功能。

在做出任何更改之前，请先阅读 `references/xcloud-constraints.md` 以了解完整的规则集。

---

## 第一步：确定适用的场景

检查提供的 `docker-compose.yml` 文件：

| 信号 | 场景 |
|--------|----------|
| `build:` 或 `build: context: .` | **场景 A** — 从源代码构建 |
| Caddy / Traefik / nginx-proxy 服务 | **场景 B** — 代理冲突 |
| 多个服务使用多个 `ports:` | **场景 B** — 多端口配置 |
| 使用 `./nginx.conf:/etc/nginx/...` 进行卷挂载 | **场景 B** — 使用外部配置文件 |
| 每个服务都包含 `build:` 语句 | **场景 C** — 多服务构建 |

一个 `docker-compose.yml` 文件可能同时触发多个场景（先处理场景 A，再处理场景 B）。

---

## 场景 A — 从源代码构建

> 详情请参阅 `references/scenario-build-source.md`。

**操作步骤：**
1. 从 `docker-compose.yml` 中删除 `build:` 指令。
2. 将 `image:` 替换为 `ghcr.io/OWNER/REPO:latest`。
3. 使用 `assets/github-actions-build.yml` 模板生成 `.github/workflows/docker-build.yml` 文件。
4. 根据所有的 `${VAR}` 变量生成 `.env.example` 文件。

**交付成果：**
- 修改后的 `docker-compose.yml` 文件
- `.github/workflows/docker-build.yml` 文件
- `.env.example` 文件
- xCloud 部署的相关步骤（详见输出格式）

---

## 场景 B — 代理冲突 / 多端口配置 / 使用外部配置文件

> 详情请参阅 `references/scenario-proxy-conflict.md`。

**操作步骤：**
1. 完全移除 Caddy/Traefik/nginx-proxy 服务。
2. 从应用程序服务中删除 SSL 相关配置以及多端口设置（替换为 `expose:`）。
3. 通过 `configs:` 块为 `nginx-router` 服务添加配置。
4. 暴露一个端口（默认为 `3080`），以便 xCloud 进行代理。

**交付成果：**
- 修改后的 `docker-compose.yml` 文件（包含 `nginx-router` 和 `configs:` 块）
- `.env.example` 文件
- xCloud 部署的相关步骤

---

## 场景 C — 多服务构建

> 详情请参阅 `references/scenario-multi-service-build.md`。

当多个服务都包含 `build:` 指令时（例如前端、后端和 worker 服务分别构建）：

**操作步骤：**
1. 为每个包含 `build:` 指令的服务创建一个独立的 GHCR 镜像路径。
2. 生成一个 GitHub Actions 工作流，以并行构建所有镜像。
3. 更新 `docker-compose.yml` 文件，使用所有的 GHCR 镜像地址。

**交付成果：**
- 修改后的 `docker-compose.yml` 文件（所有 `build:` 指令均已移除）
- `.github/workflows/docker-build.yml` 文件（采用并行构建策略）
- `.env.example` 文件

---

## 输出格式

请始终生成完整的、可直接复用的输出结果：

```
## Modified docker-compose.yml
[full file]

## .github/workflows/docker-build.yml  (Scenario A/C only)
[full file]

## .env.example
[full file]

## xCloud Deploy Steps
1. Push repo to GitHub
2. (Scenario A/C) Wait for GitHub Actions to build image — check Actions tab
3. Server → New Site → Custom Docker → connect repo
4. Exposed port: [PORT]
5. Env vars to add: [list from .env.example]
6. Deploy
```

---

## 规则

- **切勿** 在最终的 `docker-compose.yml` 文件中包含 `build:` 指令——xCloud 会忽略该指令。
- **切勿** 将数据库端口暴露给外部主机（删除 `"5432:5432"` 等配置）——应使用 `expose:` 进行内部暴露。
- **切勿** 包含 Caddy、Traefik、nginx-proxy 或 Let’s Encrypt 的配置信息。
- **务必** 保留 `environment:`, `volumes:`, `healthcheck:` 以及 worker/sidecar 服务的配置。
- **对于通过 `nginx-router` 服务的端口配置，**始终使用 `expose:` 而不是 `ports:`。
- **如果需要使用 WebSockets**，请在 nginx 配置中添加相应的升级头部信息（详见代理冲突相关的参考文档）。
- 如果不确定如何使用内联配置语法（`configs.content:`），请考虑使用 heredoc 的 `command:` 语法。

---

## 示例

请查看 `examples/` 目录中的示例文件：
- `examples/rybbit-analytics.md` — 包含 Caddy 和多端口配置的应用程序（场景 B）
- `examples/custom-app-dockerfile.md` — 从源代码构建的应用程序（场景 A）
- `examples/fullstack-monorepo.md` — 多服务构建的应用程序（场景 C）