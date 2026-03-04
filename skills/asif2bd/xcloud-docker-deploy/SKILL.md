---
name: xcloud-docker-deploy
description: "将任何项目部署到 xCloud 服务器上——系统会自动识别项目所使用的开发框架（如 WordPress、Laravel、PHP、Node.js、Next.js、NestJS、Python、Go、Rust）；支持将项目部署到本地环境或 Docker 容器中；同时会自动生成适用于生产环境的 Dockerfile、docker-compose.yml 文件，以及用于 GitHub Actions 的持续集成/持续部署（CI/CD）配置文件 (.env.example)。即使用户没有任何 Docker 基础知识，也能轻松完成部署流程。"
license: Apache-2.0
version: "1.2.0"
author: "M Asif Rahman"
homepage: "https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill"
repository: "https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill"
tags:
  - docker
  - deployment
  - devops
  - xcloud
  - docker-compose
  - github-actions
  - wordpress
  - laravel
  - nextjs
  - nodejs
  - python
  - ci-cd
  - hosting
  - infrastructure
category: "DevOps & Deployment"
platforms:
  - claude-code
  - openClaw
  - claude-ai
  - cursor
  - windsurf
  - codex
  - any
security:
  verified: true
  no_network_calls: true
  no_executables: true
  sandboxed: true
install: |
  # Claude Code / Codex CLI
  cp -r xcloud-docker-deploy ~/.claude/skills/
  # OpenClaw
  # Drop skill folder into agent workspace skills/
---
# xCloud Docker 部署

请根据实际情况调整 `docker-compose.yml` 文件，以使其能够与 [xCloud](https://xcloud.host) 配合使用——这是一个基于 Git Push 的 Docker 部署平台。

## xCloud 的工作原理

```
git push → xCloud runs: docker-compose pull && docker-compose up -d
```

**xCloud 从不执行 `docker build` 操作**。所有 Docker 镜像必须预先构建在公共注册表中。SSL、反向代理和域名路由由 xCloud 处理——您的应用程序堆栈中不应重复这些功能。

在做出任何更改之前，请先阅读 `references/xcloud-constraints.md` 以了解完整的规则集。

---

## 第 0 阶段 — 首先检测项目类型

**首先，扫描项目目录中的以下文件：**

请阅读 `DETECT.md` 以获取完整的检测规则。快速判断项目类型：

| 在项目中找到 | 应用框架 | 所需操作 |
|---|---|---|
| `wp-config.php` 或 `wp-content/` | WordPress | 阅读 `references/xcloud-native-wordpress.md` |
| `composer.json` + `artisan` | Laravel | 阅读 `references/xcloud-native-laravel.md` |
| `package.json` + `next.config.*` | Next.js | 使用 `dockerfiles/nextjs.Dockerfile` 和 `compose-templates/nextjs-postgres.yml` |
| `package.json`（无框架配置） | Node.js | 阅读 `references/xcloud-native-nodejs.md` |
| `composer.json`（无 `artisan`） | PHP | 阅读 `references/xcloud-native-php.md` |
| `requirements.txt` 或 `pyproject.toml` | Python | 使用 `dockerfiles/python-fastapi.Dockerfile` |
| `go.mod` | Go | 手动生成 Dockerfile |
| 存在 `docker-compose.yml` | 使用现有的 Docker 配置 | 进入第 1 步 |
| 无 `docker-compose.yml` | 从源代码构建 | 生成 Dockerfile（参见下面的方案 A）

有关如何选择使用原生部署方式（Native）还是 Docker 部署方式的指南，请参阅 `references/xcloud-deploy-paths.md`。

---

## 第 1 步 — 确定适用的方案

检查提供的 `docker-compose.yml` 文件：

| 信号 | 对应的方案 |
|--------|----------|
| `build:` 或 `build: context: .` | **方案 A** — 从源代码构建 |
| 包含 Caddy/Traefik/nginx-proxy 服务 | **方案 B** — 存在代理冲突 |
| 多个服务使用 `ports:` | **方案 B** — 多端口配置 |
| 使用 `./nginx.conf:/etc/nginx/...` 进行卷挂载 | **方案 B** — 需要外部配置文件 |
| 每个服务都包含 `build:` 语句 | **方案 C** — 多服务构建 |

一个 `docker-compose.yml` 文件可能同时触发多个方案（先处理方案 A，再处理方案 B）。

---

## 方案 A — 从源代码构建

> 详情请参阅 `references/scenario-build-source.md`。

**操作步骤：**
1. 从 `docker-compose.yml` 中删除 `build:` 指令。
2. 将 `image:` 替换为 `ghcr.io/OWNER/REPO:latest`。
3. 使用 `assets/github-actions-build.yml` 模板生成 `.github/workflows/docker-build.yml`。
4. 根据所有的 `${VAR}` 变量生成 `.env.example` 文件。

**交付成果：**
- 修改后的 `docker-compose.yml` 文件
- `.github/workflows/docker-build.yml` 文件
- `.env.example` 文件
- xCloud 部署所需的步骤（参见输出格式）

---

## 方案 B — 代理冲突 / 多端口 / 外部配置

> 详情请参阅 `references/scenario-proxy-conflict.md`。

**操作步骤：**
1. 完全移除 Caddy/Traefik/nginx-proxy 服务。
2. 从应用程序服务中删除 SSL 相关配置和多端口设置（替换为 `expose:`）。
3. 通过 `configs:` 块添加 `nginx-router` 服务并配置其路由规则。
4. 暴露一个端口（默认为 `3080`），以便 xCloud 进行代理。

**交付成果：**
- 修改后的 `docker-compose.yml` 文件（包含 `nginx-router` 和 `configs:` 配置）
- `.env.example` 文件
- xCloud 部署所需的步骤

---

## 方案 C — 多服务构建

> 详情请参阅 `references/scenario-multi-service-build.md`。

当多个服务都包含 `build:` 指令时（例如前端、后端和 worker 服务分别构建）：

**操作步骤：**
1. 为每个包含 `build:` 指令的服务生成一个独立的 GHCR 镜像路径。
2. 创建一个 GitHub Actions 工作流，以便并行构建所有镜像。
3. 更新 `docker-compose.yml` 文件，使用所有的 GHCR 镜像地址。

**交付成果：**
- 修改后的 `docker-compose.yml` 文件（所有 `build:` 指令均已移除）
- `.github/workflows/docker-build.yml` 文件（采用矩阵策略进行构建）
- `.env.example` 文件

---

## 输出格式

请始终生成完整的、可以直接复用的输出文件：

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

- **切勿** 在最终的 `docker-compose.yml` 文件中包含 `build:` 指令——xCloud 会忽略这些指令。
- **切勿** 将数据库端口暴露给主机（例如 `5432:5432`）——应使用 `expose:` 进行内部暴露。
- **切勿** 包含 Caddy、Traefik、nginx-proxy 或 Let’s Encrypt 的配置信息。
- **务必** 保留 `environment:`, `volumes:`, `healthcheck:` 以及 worker/sidecar 服务的配置。
- **对于使用 nginx-router 的服务**，始终使用 `expose:` 而不是 `ports:` 来暴露端口。
- **如果使用 WebSockets**，请在 nginx 配置中添加相应的升级头信息（参见方案 B 的相关说明）。
- 如果不确定如何使用 `configs.content:` 的语法，可以使用 heredoc 的 `command:` 替代方案。

---

## 示例

请查看 `examples/` 目录中的示例文件：
- `examples/rybbit-analytics.md` — 包含 Caddy 和多端口的应用程序（方案 B）
- `examples/custom-app-dockerfile.md` — 从源代码构建（方案 A）
- `examples/fullstack-monorepo.md` — 多服务构建（方案 C）