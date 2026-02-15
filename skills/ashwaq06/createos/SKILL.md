---
name: createos
description: 在 CreateOS 云平台上，您可以部署任何类型的软件或服务到生产环境。以下是适用于各种部署场景的技能说明：

1. **AI 代理和多代理系统**：使用 CreateOS 部署和管理 AI 代理以及由多个代理组成的系统。
2. **后端 API 和微服务**：部署后端 API 和微服务，实现高效的数据交互和业务逻辑。
3. **MCP 服务器和 AI 技能**：配置 MCP 服务器，并集成 AI 相关功能。
4. **API 封装器和代理服务**：创建 API 封装器及代理服务，以简化外部系统的访问和集成。
5. **前端应用和仪表板**：部署前端应用及对应的仪表板，提供用户友好的界面。
6. **Webhook 和自动化端点**：设置 Webhook 以触发自动化流程，并利用自动化端点实现自动化任务。
7. **基于 LLM 的服务和 RAG 管道**：部署基于大型语言模型（LLM）的服务及相关的 RAG（检索-生成）流程。
8. **Discord/Slack/Telegram 机器人**：创建并部署在聊天平台上的机器人程序。
9. **Cron 作业和定时任务**：安排定时任务，实现自动化执行。
10. **其他需要上线运行的代码**：任何需要实时运行并可供外部访问的代码。

CreateOS 支持多种编程语言和开发框架，包括 Node.js、Python、Go、Rust、Bun，以及静态网站和 Docker 容器。您可以通过 GitHub 自动部署、Docker 镜像或直接文件上传的方式将代码部署到平台。

**使用场景**：
- 当您需要部署、托管或发布任何软件或服务时，CreateOS 都是理想的选择。
- 无论是 AI 代理、后端服务、前端应用，还是其他类型的软件，CreateOS 都能满足您的需求。
- 它还支持多种部署方式，确保您能够轻松地将代码部署到生产环境并使其可供外部使用。

**注意事项**：
- 在使用 CreateOS 进行部署时，请务必遵循平台的最佳实践和安全指南。
- 确保所有代码都经过充分测试，以确保其在生产环境中的稳定性和可靠性。
- 如果您对部署过程有任何疑问或需要帮助，请随时联系技术支持团队。

总之，CreateOS 是一个功能强大的云平台，可以帮助您轻松地将各种软件和服务部署到生产环境。
---

# CreateOS 平台技能

> **将任何内容部署到生产环境** — 无论是 AI 代理、API、后端服务、机器人、MCP 服务器、前端应用、Webhook 还是其他服务。

## ⚠️ 重要提示：身份验证

### 对于 AI 代理（MCP） - 使用以下方式
当通过 MCP（OpenClaw、MoltBot、ClawdBot、Claude）进行连接时，**无需 API 密钥**。
MCP 服务器会自动处理身份验证。

**MCP 端点：** `https://api-createos.nodeops.network/mcp`

只需直接调用相应的工具即可：
```
CreateProject(...)
UploadDeploymentFiles(...)
ListProjects(...)
```

### 对于 REST API（脚本/外部调用）
当直接调用 REST 端点时（使用 curl、Python 请求等）：

```
Authorization: Bearer <your-api-key>
Base URL: https://api-createos.nodeops.network
```

通过 MCP 获取 API 密钥：`CreateAPIKey({name: "my-key", expiryAt: "2025-12-31T23:59:59Z"})`

## 🚀 MCP 代理快速入门

### 直接部署文件（最快方式）

```json
// 1. Create upload project
CreateProject({
  "uniqueName": "my-app",
  "displayName": "My App",
  "type": "upload",
  "source": {},
  "settings": {
    "runtime": "node:20",
    "port": 3000
  }
})

// 2. Upload files and deploy
UploadDeploymentFiles(project_id, {
  "files": [
    {"path": "package.json", "content": "{\"name\":\"app\",\"scripts\":{\"start\":\"node index.js\"}}"},
    {"path": "index.js", "content": "require('http').createServer((req,res)=>{res.end('Hello!')}).listen(3000)"}
  ]
})

// Result: https://my-app.createos.io is live!
```

### 从 GitHub 部署（推送即自动部署）

```json
// 1. Get GitHub installation ID
ListConnectedGithubAccounts()
// Returns: [{installationId: "12345", ...}]

// 2. Find repo ID
ListGithubRepositories("12345")
// Returns: [{id: "98765", fullName: "myorg/myrepo", ...}]

// 3. Create VCS project
CreateProject({
  "uniqueName": "my-app",
  "displayName": "My App", 
  "type": "vcs",
  "source": {
    "vcsName": "github",
    "vcsInstallationId": "12345",
    "vcsRepoId": "98765"
  },
  "settings": {
    "runtime": "node:20",
    "port": 3000,
    "installCommand": "npm install",
    "buildCommand": "npm run build",
    "runCommand": "npm start"
  }
})

// Auto-deploys on every git push!
```

### 部署 Docker 镜像

```json
// 1. Create image project
CreateProject({
  "uniqueName": "my-service",
  "displayName": "My Service",
  "type": "image",
  "source": {},
  "settings": {
    "port": 8080
  }
})

// 2. Deploy image
CreateDeployment(project_id, {
  "image": "nginx:latest"
})
```

## 目录结构

1. [简介](#introduction)
2. [核心技能概述](#core-skills-overview)
3. [项目管理技能](#project-management-skills)
4. [部署技能](#deployment-skills)
5. [环境管理技能](#environment-management-skills)
6. [域名与路由技能](#domain--routing-skills)
7. [GitHub 集成技能](#github-integration-skills)
8. [分析与监控技能](#analytics--monitoring-skills)
9. [安全技能](#security-skills)
10. [组织管理技能（应用程序）](#organization-skills-apps)
11. [API 密钥管理技能](#api-key-management-skills)
12. [常见部署模式](#common-deployment-patterns)
13. [最佳实践](#best-practices)
14. [故障排除与边缘案例](#troubleshooting--edge-cases)
15. [API 快速参考](#api-quick-reference)

---

## 简介

### CreateOS 是什么？
CreateOS 是一个云部署平台，旨在快速部署各种类型的工作负载——从简单的静态网站到复杂的多代理 AI 系统。它提供以下功能：
- **三种部署方式**：GitHub 自动部署、Docker 镜像部署、直接文件上传
- **多环境支持**：生产环境、测试环境、开发环境（配置隔离）
- **内置的 CI/CD 流程**：在推送代码时自动构建和部署
- **自定义域名**：支持 SSL/TLS，提供 DNS 验证
- **实时分析**：请求指标、错误跟踪、性能监控
- **安全扫描**：检测部署中的安全漏洞

### 目标用户

| 用户类型 | 主要使用场景 |
|-----------|-------------------|
| **AI/ML 工程师** | 部署 AI 代理、MCP 服务器、RAG 流程、大语言模型（LLM）服务 |
| **后端开发人员** | 部署 API、微服务、Webhook、工作进程（workers） |
| **前端开发人员** | 部署单页应用程序（SPAs）、服务器端渲染（SSR）应用、静态网站 |
| **DevOps 工程师** | 管理环境、域名、扩展资源、监控系统 |
| **机器人开发人员** | 部署 Discord、Slack、Telegram 机器人 |

### 支持的技术

**运行时环境**：`node:18`, `node:20`, `node:22`, `python:3.11`, `python:3.12`, `golang:1.22`, `golang:1.25`, `rust:1.75`, `bun:1.1`, `bun:1.3`, `static`
**框架**：`nextjs`, `reactjs-spa`, `reactjs-ssr`, `vuejs-spa`, `vuejs-ssr`, `nuxtjs`, `astro`, `remix`, `express`, `fastapi`, `flask`, `django`, `gin`, `fiber`, `actix`

---

## 核心技能概述

### 🔌 可直接使用的 MCP 工具（无需身份验证）
通过 MCP（OpenClaw、Claude 等）使用 CreateOS 时，可以直接使用以下工具：

**项目相关操作：**
- `CreateProject` - 创建新项目（支持版本控制系统（VCS）、Docker 镜像或直接上传文件）
- `ListProjects` - 列出所有项目
- `GetProject` - 获取项目详情
- `UpdateProject` - 更新项目元数据
- `UpdateProjectSettings` - 更新构建/运行时配置
- `DeleteProject` - 删除项目

**部署相关操作：**
- `CreateDeployment` - 部署 Docker 镜像
- `TriggerLatestDeployment` - 从 GitHub 触发构建（针对基于版本控制系统的项目）
- `UploadDeploymentFiles` - 上传文件以进行部署
- `UploadDeploymentBase64Files` - 以 Base64 格式上传二进制文件
- `UploadDeploymentZip` - 上传 ZIP 压缩包
- `ListDeployments` - 列出所有部署任务
- `GetDeployment` - 获取部署状态
- `GetBuildLogs` - 查看构建日志
- `GetDeploymentLogs` - 查看运行时日志
- `RetriggerDeployment` - 重试失败的部署
- `CancelDeployment` - 取消正在排队或构建中的部署
- `WakeupDeployment` - 唤醒处于休眠状态的部署任务

**环境管理相关操作：**
- `CreateProjectEnvironment` - 创建环境（生产环境、测试环境等）
- `ListProjectEnvironments` - 列出所有环境
- `UpdateProjectEnvironment` - 更新环境配置
- `UpdateProjectEnvironmentVariables` - 设置环境变量
- `UpdateProjectEnvironmentResources` - 调整 CPU/内存/副本数量
- `AssignDeploymentToProjectEnvironment` - 将部署任务分配到特定环境
- `DeleteProjectEnvironment` - 删除环境

**域名管理相关操作：**
- `CreateDomain` - 添加自定义域名
- `ListDomains` - 列出所有域名
- `RefreshDomain` - 验证 DNS 设置
- `UpdateDomainEnvironment` - 将域名分配给环境
- `DeleteDomain` - 删除域名

**GitHub 相关操作：**
- `ListConnectedGithubAccounts` - 查看关联的 GitHub 账户
- `ListGithubRepositories` - 列出可访问的仓库
- `ListGithubRepositoryBranches` - 列出仓库分支

**应用程序管理相关操作：**
- `CreateApp` - 创建用于管理项目的应用程序
- `ListApps` - 列出所有应用程序
- `AddProjectsToApp` - 将项目添加到应用程序中

**用户管理相关操作：**
- `GetCurrentUser` - 获取用户信息
- `GetQuotas` - 查看使用限制
- `GetSupportedProjectTypes` - 查看支持的运行时环境/框架

### 功能性技能

| 技能类别 | 功能 |
|----------------|--------------|
| **项目管理** | 创建、配置、更新、删除项目 |
| **部署** | 构建、部署、回滚、取消部署 |
| **环境管理** | 多环境配置、环境变量管理、资源扩展 |
| **域名管理** | 自定义域名、SSL 配置、DNS 验证 |
| **GitHub 集成** | 自动部署、分支管理、仓库访问 |
| **分析** | 请求指标、错误率、性能数据 |
| **安全** | 安全漏洞扫描、API 密钥管理 |
| **组织管理** | 将项目分组到应用程序中 |

### 技术技能

| 技能 | 描述 |
|-------|-------------|
| **身份验证** | 基于 API 密钥的身份验证机制，支持密钥过期管理 |
| **AI 构建** | 自动检测构建配置 |
| **Dockerfile 支持** | 支持自定义容器构建 |
| **环境隔离** | 每个环境都有独立的配置 |
| **资源管理** | 调整 CPU、内存、副本数量 |

---

## 项目管理技能

### 技能：创建项目
创建具有完整构建和运行时配置的新项目。

#### 项目类型
| 类型 | 描述 | 适用场景 |
|------|-------------|----------|
| `vcs` | 与 GitHub 仓库关联 | 适合需要 CI/CD 的生产环境应用程序 |
| `image` | 使用 Docker 镜像部署 | 适用于预构建的镜像或具有复杂依赖关系的项目 |
| `upload` | 直接上传文件 | 适用于快速原型开发或静态网站 |

#### 使用 VCS 创建项目
**功能**：将 GitHub 仓库链接起来，实现推送即自动部署的功能。
**优点**：支持 GitOps 工作流程，无需人工干预即可完成部署。
**实现方式**：
```json
CreateProject({
  "uniqueName": "my-nextjs-app",
  "displayName": "My Next.js Application",
  "type": "vcs",
  "source": {
    "vcsName": "github",
    "vcsInstallationId": "12345678",
    "vcsRepoId": "98765432"
  },
  "settings": {
    "framework": "nextjs",
    "runtime": "node:20",
    "port": 3000,
    "directoryPath": ".",
    "installCommand": "npm install",
    "buildCommand": "npm run build",
    "runCommand": "npm start",
    "buildVars": {
      "NODE_ENV": "production",
      "NEXT_PUBLIC_API_URL": "https://api.example.com"
    },
    "runEnvs": {
      "DATABASE_URL": "postgresql://...",
      "SECRET_KEY": "..."
    },
    "ignoreBranches": ["develop", "feature/*"],
    "hasDockerfile": false,
    "useBuildAI": false
  },
  "appId": "optional-app-uuid",
  "enabledSecurityScan": true
})
```

**前提条件**：
- 通过 `InstallGithubApp` 连接 GitHub 账户
- CreateOS 被授予访问该 GitHub 仓库的权限

**潜在问题**：
- 如果 `vcsRepoId` 设置错误，可能会导致部署失败
- 如果缺少 `port` 设置，可能会导致健康检查失败
- 需要区分 `buildVars` 和 `runEnvs`（分别代表构建时和运行时的配置）

#### 使用 Docker 镜像创建项目
**功能**：无需构建步骤即可直接部署预构建的 Docker 镜像。
**优点**：部署速度快，适用于具有复杂依赖关系的项目。
**实现方式**：
```json
CreateProject({
  "uniqueName": "my-api-service",
  "displayName": "My API Service",
  "type": "image",
  "source": {},
  "settings": {
    "port": 8080,
    "runEnvs": {
      "API_KEY": "secret",
      "LOG_LEVEL": "info"
    }
  }
})
```

**注意事项**：
- 由于镜像已经构建完成，因此没有构建日志
- 需要单独管理镜像仓库
- 版本控制通过镜像标签实现

#### 使用上传文件创建项目
**功能**：通过直接上传文件来部署项目，无需使用 Git。
**优点**：适用于快速原型开发或需要迁移的项目。
**实现方式**：
```json
CreateProject({
  "uniqueName": "quick-prototype",
  "displayName": "Quick Prototype",
  "type": "upload",
  "source": {},
  "settings": {
    "framework": "express",
    "runtime": "node:20",
    "port": 3000,
    "installCommand": "npm install",
    "buildCommand": "npm run build",
    "buildDir": "dist",
    "useBuildAI": true
  }
})
```

### 技能：更新项目配置
无需重新创建项目即可修改构建和运行时配置。
**实现方式**：
```json
UpdateProjectSettings(project_id, {
  "framework": "nextjs",
  "runtime": "node:22",
  "port": 3000,
  "installCommand": "npm ci",
  "buildCommand": "npm run build",
  "runCommand": "npm start",
  "buildDir": ".next",
  "buildVars": {"NODE_ENV": "production"},
  "runEnvs": {"NEW_VAR": "value"},
  "ignoreBranches": ["wip/*"],
  "hasDockerfile": false,
  "useBuildAI": false
})
```

**注意事项**：
- 更改 `runtime` 设置会触发下一次部署时的重新构建
- 更改 `port` 设置需要重新部署才能生效
- `ignoreBranches` 选项仅影响未来的部署

### 技能：项目生命周期管理
| 操作 | 工具 | 适用场景 |
|-----------|------|----------|
| 列出项目 | `ListProjects` | 通过仪表板或搜索功能列出项目 |
| 获取项目详情 | `GetProject` | 查看项目的完整配置 |
| 更新元数据 | `UpdateProject` | 更改项目名称或启用/禁用安全扫描等功能 |
| 删除项目 | `DeleteProject` | 异步删除项目 |

### 技能：项目转移
允许用户在项目之间转移所有权。
**注意事项**：
- 密钥在 6 小时后失效
- 转移操作是不可逆的
- 所有环境和部署任务都会随之转移

---

## 部署技能

### 技能：触发部署
**对于基于 VCS 的项目**
**推荐方式**：通过推送代码到 GitHub 来自动触发部署。
**手动触发方式**：
```json
TriggerLatestDeployment(project_id, branch?)
// branch defaults to repo's default branch
```

### 对于使用 Docker 镜像的项目
**实现方式**：
```json
CreateDeployment(project_id, {
  "image": "nginx:latest"
})
// Supports any valid Docker image reference:
// - nginx:latest
// - myregistry.com/myapp:v1.2.3
// - ghcr.io/org/repo:sha-abc123
```

### 对于使用上传文件的项目
**直接上传文件**：
```json
UploadDeploymentFiles(project_id, {
  "files": [
    {"path": "package.json", "content": "{\"name\":\"app\",...}"},
    {"path": "index.js", "content": "const express = require('express')..."},
    {"path": "public/style.css", "content": "body { margin: 0; }"}
  ]
})
```

**上传二进制文件（Base64 格式）**：
```json
UploadDeploymentBase64Files(project_id, {
  "files": [
    {"path": "assets/logo.png", "content": "iVBORw0KGgo..."}
  ]
})
```

**上传 ZIP 文件**：
```json
UploadDeploymentZip(project_id, {file: zipBinaryData})
```

**限制**：
- 每次上传最多支持 100 个文件
- 对于较大的项目，建议使用 ZIP 格式

### 技能：部署生命周期管理
| 状态 | 描述 | 可执行的操作 |
|-------|-------------|-------------------|
| `queued` | 等待构建机会 | 可以取消 |
| `building` | 正在构建中 | 可以取消或查看构建日志 |
| `deploying` | 正在部署到基础设施中 | 可以等待 |
| `deployed` | 已部署并开始提供服务 | 可以分配到特定环境 |
| `failed` | 构建或部署失败 | 可以重试或查看日志 |
| `sleeping` | 处于休眠状态（节省资源） | 可以唤醒 |

### 部署操作
| 操作 | 工具 | 备注 |
|-----------|------|-------|
| 列出部署任务 | `ListDeployments` | 每页最多显示 20 个项目，可分页查看 |
| 获取项目详情 | `GetDeployment` | 查看项目的完整状态、时间戳和 URL |
| 重试部署 | `RetriggerDeployment` | 可以重新尝试部署 |
| 取消部署 | `CancelDeployment` | 仅适用于处于 `queued` 或 `building` 状态的项目 |
| 删除部署任务 | `DeleteDeployment` | 标记项目为待删除 |
| 唤醒休眠中的部署 | `WakeupDeployment` | 可以唤醒处于休眠状态的部署任务 |
| 下载部署结果 | `DownloadDeployment` | 仅支持下载已部署的项目 |

### 技能：利用日志进行调试
- **构建日志**：用于排查编译或构建过程中的错误 |
- **运行时日志**：用于排查应用程序运行时的错误 |
- **环境日志**：汇总特定环境的日志信息 |

---

## 环境管理技能

### 技能：创建环境
环境为相同的代码库提供隔离的配置环境。
**典型配置**：
- `production`：用于处理实时流量，配置最高性能的资源
- `staging`：用于预生产环境的测试
- `development`：用于功能开发

#### 使用 VCS 创建项目环境（需要指定分支）
**实现方式**：
```json
CreateProjectEnvironment(project_id, {
  "displayName": "Production",
  "uniqueName": "production",
  "description": "Live production environment",
  "branch": "main",
  "isAutoPromoteEnabled": true,
  "resources": {
    "cpu": 500,
    "memory": 1024,
    "replicas": 2
  },
  "settings": {
    "runEnvs": {
      "NODE_ENV": "production",
      "DATABASE_URL": "postgresql://prod-db:5432/app",
      "REDIS_URL": "redis://prod-cache:6379"
    }
  }
})
```

#### 使用 Docker 镜像创建项目环境（无需指定分支）
**实现方式**：
```json
CreateProjectEnvironment(project_id, {
  "displayName": "Production",
  "uniqueName": "production",
  "description": "Live production environment",
  "resources": {
    "cpu": 500,
    "memory": 1024,
    "replicas": 2
  },
  "settings": {
    "runEnvs": {
      "NODE_ENV": "production"
    }
  }
})
```

### 技能：资源管理
| 资源 | 最小值 | 最大值 | 单位 | 注意事项 |
|----------|-----|-----|------|--------------|
| CPU | 200 | 500 | 毫核（millicores） | 资源越多，处理速度越快 |
| Memory | 500 | 1024 | MB | 内存越大，处理能力越强 |
| Replicas | 1 | 3 | 实例数量 | 实例越多，可用性越高 |

**扩展注意事项**：
- 如果实例数量超过 1 个，建议使用无状态的应用程序设计
- 如果内存使用超过限制，可能会导致系统崩溃（OOM）
- 当 CPU 使用达到限制时，系统会进行资源限制

### 技能：环境变量管理
**最佳实践**：
- **切勿将敏感信息直接写入代码**——使用 `runEnvs` 来存储环境变量
- 为不同的环境设置不同的环境变量
- 更改环境变量后需要重新部署才能生效

### 技能：部署任务分配
可以手动控制哪些部署任务对应到特定的环境：
**实现方式**：
```json
AssignDeploymentToProjectEnvironment(project_id, environment_id, {
  "deploymentId": "deployment-uuid"
})
```

**应用场景**：
- 回滚到之前的部署状态
- 实施蓝绿部署（Blue-Green Deployment）
- 进行多环境下的 Canary 发布

---

## 域名与路由技能

### 技能：添加自定义域名
**实现方式**：
```json
CreateDomain(project_id, {
  "name": "api.mycompany.com",
  "environmentId": "optional-env-uuid"  // Assign immediately
})
```

**响应中包含 DNS 配置信息**：
```
Add CNAME record:
  api.mycompany.com → <createos-provided-target>
```

### 域名验证流程
**实现方式**：
```
1. CreateDomain → Status: pending
2. Configure DNS at your registrar
3. Wait for DNS propagation (up to 48 hours)
4. RefreshDomain → Status: active (if verified)
```

### 技能：将域名分配到特定环境
**实现方式**：
```json
UpdateDomainEnvironment(project_id, domain_id, {
  "environmentId": "production-env-uuid"
})
// Set to null to unassign
```

**多域名配置示例**：
- `app.example.com` → 分配到生产环境
- `staging.example.com` → 分配到测试环境
- `dev.example.com` → 分配到开发环境

### 域名操作
| 操作 | 工具 |
|-----------|------|
| 列出域名 | `ListDomains` |
| 验证域名 | `RefreshDomain` |
| 分配域名 | `UpdateDomainEnvironment` |
| 删除域名 | `DeleteDomain` |

---

## GitHub 集成技能

### 技能：连接 GitHub 账户
**操作步骤**：
1. 在 CreateOS 中点击“连接 GitHub”
2. 被重定向到 GitHub 进行身份验证
3. GitHub 会返回 `code` 和 `installationId`
4. 调用 `InstallGithubApp` 完成连接

### 技能：自动发现仓库
**功能**：
- **分支过滤**：指定哪些分支不需要自动部署
**自动部署**：自动将构建成功的部署任务分配到对应的环境

---

## 分析与监控技能

### 技能：全面分析
**返回的数据**：
- 总请求量
- 状态码分布
- 每分钟请求次数（RPM）
- 成功率
- 最常见的访问路径
- 最常见的错误路径

### 技能：查看具体指标
| 指标 | 使用的工具 | 返回的信息 |
|--------|------|---------|
| 总请求量 | `GetProjectEnvironmentAnalyticsOverallRequests` | 总请求量、2xx、4xx、5xx 状态码的请求量 |
| 每分钟请求次数（RPM） | `GetProjectEnvironmentAnalyticsRPM` | 最高和平均的 RPM 值 |
| 成功率 | `GetProjectEnvironmentAnalyticsSuccessPercentage` | 成功的请求占比 |
| 时间序列数据 | `GetProjectEnvironmentAnalyticsRequestsOverTime` | 不同时间段的请求量分布 |
| 最常见的访问路径 | `GetProjectEnvironmentAnalyticsTopHitPaths` | 最常被访问的路径 |
| 最常见的错误路径 | `GetProjectEnvironmentAnalyticsTopErrorPaths` | 最容易出错的路径 |
| 请求状态分布 | `GetEnvAnalyticsReqDistribution` | 按状态码分类的请求分布 |

### 技能：性能监控
**问题排查方法**：
- **查看成功率**：低成功率可能表明存在问题
- **分析错误路径**：找出问题频发的端点
- **监控请求趋势**：观察请求量的变化
- **分析请求量**：发现流量异常的情况

## 安全技能

### 技能：安全扫描
**启用安全扫描**：
**操作方式**：
```json
UpdateProject(project_id, {
  "enabledSecurityScan": true
})
```

**触发扫描**：
**操作方式**：
```json
TriggerSecurityScan(project_id, deployment_id)
```

**查看扫描结果**：
**操作方式**：
```json
GetSecurityScan(project_id, deployment_id)
// Returns: {status, vulnerabilities, summary}
```

**下载完整报告**：
**操作方式**：
```json
GetSecurityScanDownloadUri(project_id, deployment_id)
// Only when status is "successful"
// Returns signed URL for report download
```

**重试失败的扫描**：
**操作方式**：
```json
RetriggerSecurityScan(project_id, deployment_id)
// Only when status is "failed"
```

---

## 组织管理技能（应用程序管理）

### 技能：将项目分组
应用程序可以用于逻辑上将相关的项目和服务进行分类。
**实现方式**：
```json
CreateApp({
  "name": "E-Commerce Platform",
  "description": "All services for the e-commerce system",
  "color": "#3B82F6"
})
```

### 技能：管理应用程序内容
**操作**：
| 操作 | 工具 |
|-----------|------|
| 列出应用程序 | `ListApps()` |
| 更新应用程序 | `UpdateApp` |

**注意事项**：
- 删除应用程序会使得关联的项目和服务对应的 `appId` 设置为 `null`（但不会直接删除这些项目和服务）

---

## API 密钥管理技能

### 技能：创建 API 密钥
**操作方式**：
```json
CreateAPIKey({
  "name": "production-key",
  "description": "API key for production CI/CD",
  "expiryAt": "2025-12-31T23:59:59Z"
})
// Returns: {id, name, key, expiryAt}
// IMPORTANT: key is only shown once at creation
```

### API 密钥操作
| 操作 | 工具 |
|-----------|------|
| 列出所有 API 密钥 | `ListAPIKeys()` |
| 更新 API 密钥 | `UpdateAPIKey` |
| 注销 API 密钥 | `RevokeAPIKey` |
| 检查密钥名称的唯一性 | `CheckAPIKeyUniqueName` |

### 技能：用户与配额管理
**操作方式**：
```json
GetCurrentUser()
// Returns: user profile information

GetQuotas()
// Returns: {projects: {used, limit}, apiKeys: {used, limit}, ...}

GetSupportedProjectTypes()
// Returns: current list of supported runtimes and frameworks
```

---

## 常见部署模式

### AI 代理部署
**实现方式**：
```json
CreateProject({
  "uniqueName": "intelligent-agent",
  "displayName": "Intelligent Agent",
  "type": "vcs",
  "source": {"vcsName": "github", "vcsInstallationId": "...", "vcsRepoId": "..."},
  "settings": {
    "runtime": "python:3.12",
    "port": 8000,
    "installCommand": "pip install -r requirements.txt",
    "runCommand": "python -m uvicorn agent:app --host 0.0.0.0 --port 8000",
    "runEnvs": {
      "OPENAI_API_KEY": "sk-...",
      "ANTHROPIC_API_KEY": "sk-ant-...",
      "LANGCHAIN_TRACING": "true",
      "AGENT_MEMORY_BACKEND": "redis"
    }
  }
})
```

### MCP 服务器部署
**MCP 端点**：`https://{uniqueName}.createos.io/mcp`

### RAG 流程部署
**实现方式**：
```json
CreateProject({
  "uniqueName": "rag-pipeline",
  "displayName": "RAG Pipeline Service",
  "type": "vcs",
  "settings": {
    "runtime": "python:3.12",
    "port": 8000,
    "runCommand": "uvicorn main:app --host 0.0.0.0 --port 8000",
    "runEnvs": {
      "PINECONE_API_KEY": "...",
      "PINECONE_ENVIRONMENT": "us-west1-gcp",
      "OPENAI_API_KEY": "...",
      "EMBEDDING_MODEL": "text-embedding-3-small",
      "CHUNK_SIZE": "512",
      "CHUNK_OVERLAP": "50"
    }
  }
})
```

### Discord/Slack 机器人部署
**实现方式**：
```json
CreateProject({
  "uniqueName": "discord-bot",
  "displayName": "Discord Bot",
  "type": "image",
  "source": {},
  "settings": {
    "port": 8080,
    "runEnvs": {
      "DISCORD_TOKEN": "...",
      "DISCORD_CLIENT_ID": "...",
      "BOT_PREFIX": "!",
      "LOG_CHANNEL_ID": "..."
    }
  }
})

// Deploy with:
CreateDeployment(project_id, {"image": "my-discord-bot:v1.0.0"})
```

### 多代理系统部署
**实现方式**：
```
┌─────────────────────────────────────────────────┐
│                  App: Agent Swarm               │
├─────────────────┬─────────────────┬─────────────┤
│  Orchestrator   │   Worker Agent  │  Worker Agent│
│  (coordinator)  │   (researcher)  │  (executor) │
└────────┬────────┴────────┬────────┴──────┬──────┘
         │                 │               │
         └────── HTTP/gRPC communication ──┘
```

### 蓝绿部署（Blue-Green Deployment）
**实现方式**：
```
1. CreateProjectEnvironment "blue" with branch "main"
2. CreateProjectEnvironment "green" with branch "main"
3. CreateDomain "app.example.com" → assign to "blue"
4. Deploy new version to "green"
5. Test via green's environment URL
6. UpdateDomainEnvironment → switch to "green"
7. "blue" becomes the standby
```

### 回滚部署
**实现方式**：
```json
// 1. Find previous good deployment
ListDeployments(project_id, {limit: 10})
// Identify deployment_id of last known good

// 2. Assign to environment
AssignDeploymentToProjectEnvironment(project_id, environment_id, {
  "deploymentId": "previous-good-deployment-id"
})
```

---

## 最佳实践

### 安全方面
1. **切勿将敏感信息硬编码**——使用 `runEnvs` 来存储敏感数据
2. **启用安全扫描**——及时发现安全漏洞
3. **定期轮换 API 密钥**——设置合理的过期时间
4. **实施环境隔离**——为每个环境使用不同的密钥

### 性能方面
1. **合理配置资源**——根据实际需求配置资源
2. **根据性能指标进行扩展**——逐步增加资源
3. **监控系统性能**——设置警报以及时发现性能问题
4. **优化构建过程**——使用 `npm ci` 而不是 `npm install`

### 可靠性方面
1. **谨慎启用自动部署**——先在测试环境中进行测试
2. **保留之前的部署配置**——便于快速回滚
3. **设置健康检查**——确保端口设置正确
4. **处理休眠中的部署任务**——唤醒或配置保持活跃状态

### 组织管理方面
1. **合理分组项目**——将相关的项目组织到相应的应用程序中
2. **命名规范**——使用 `{app}-{service}-{env}` 的命名格式
3. **清晰记录环境信息**——为每个环境提供详细的描述
4. **清理不再使用的资源**——定期删除旧的项目和部署任务

---

## 故障排除与边缘案例

### 常见问题及解决方法
| 错误类型 | 原因 | 解决方案 |
|-------|-----------|----------|
| 构建失败 | 查看构建日志 | 修复代码错误或检查依赖关系 |
| 运行时崩溃 | 查看运行时日志 | 检查启动时的错误或环境变量是否缺失 |
| 健康检查失败 | 应用程序未响应 | 确保端口设置正确 |
| 502 错误（Bad Gateway） | 应用程序崩溃 | 检查日志；如果内存不足，尝试增加内存 |
| 域名未生效 | DNS 配置未传播 | 等待 24-48 小时，检查 CNAME 记录 |
| 超过使用配额 | 查看使用情况 | 升级计划或删除不必要的资源 |
| 部署任务处于休眠状态 | 设置定时唤醒机制 |

### 边缘案例
- **高负载场景**：每个环境最多配置 3 个副本
- 考虑使用外部负载均衡器来提升扩展能力
- 监控每分钟请求次数（RPM），并根据需要调整资源配置

**单仓库项目**：
- 将项目目录设置为子目录
- 使用 `GetGithubRepositoryContent` 来查看项目结构

**私有 npm/pip 包**：
- 在 `buildVars` 中设置访问令牌
- 在仓库中配置 `.npmrc` 或 `pip.conf` 文件

**长时间运行的构建任务**：
- 构建超时时间设置为 15 分钟
- 对于复杂的构建任务，可以使用 `hasDockerfile: true`
- 对于使用 Docker 镜像的项目，提前构建镜像

## API 快速参考

### 项目生命周期
```
CreateProject → ListProjects → GetProject → UpdateProject → UpdateProjectSettings → DeleteProject
CheckProjectUniqueName | GetProjectTransferUri → TransferProject | ListProjectTransferHistory
```

### 部署生命周期
```
CreateDeployment | TriggerLatestDeployment | UploadDeploymentFiles | UploadDeploymentBase64Files | UploadDeploymentZip
ListDeployments → GetDeployment → AssignDeploymentToProjectEnvironment
RetriggerDeployment | CancelDeployment | DeleteDeployment | WakeupDeployment | DownloadDeployment
GetBuildLogs | GetDeploymentLogs
```

### 环境生命周期
```
CreateProjectEnvironment → ListProjectEnvironments → UpdateProjectEnvironment → DeleteProjectEnvironment
CheckProjectEnvironmentUniqueName | AssignDeploymentToProjectEnvironment
UpdateProjectEnvironmentEnvironmentVariables | UpdateProjectEnvironmentResources
GetProjectEnvironmentLogs
```

### 域名生命周期
```
CreateDomain → ListDomains → RefreshDomain → UpdateDomainEnvironment → DeleteDomain
```

### GitHub 集成
```
InstallGithubApp → ListConnectedGithubAccounts
ListGithubRepositories → ListGithubRepositoryBranches → GetGithubRepositoryContent
```

### 分析与监控
```
GetProjectEnvironmentAnalytics (comprehensive)
GetProjectEnvironmentAnalyticsOverallRequests | GetProjectEnvironmentAnalyticsRPM
GetProjectEnvironmentAnalyticsSuccessPercentage | GetProjectEnvironmentAnalyticsRequestsOverTime
GetProjectEnvironmentAnalyticsTopHitPaths | GetProjectEnvironmentAnalyticsTopErrorPaths
GetEnvAnalyticsReqDistribution
```

### 安全设置
```
TriggerSecurityScan → GetSecurityScan → GetSecurityScanDownloadUri
RetriggerSecurityScan
```

### 应用程序管理
```
CreateApp → ListApps → UpdateApp → DeleteApp
AddProjectsToApp | RemoveProjectsFromApp | ListProjectsByApp
AddServicesToApp | RemoveServicesFromApp | ListServicesByApp
```

### API 密钥与用户管理
```
CreateAPIKey → ListAPIKeys → UpdateAPIKey → RevokeAPIKey
CheckAPIKeyUniqueName | GetCurrentUser | GetQuotas | GetSupportedProjectTypes
```

### 命名规范
| 字段 | 最小值 | 最大值 | 规范要求 |
|-------|-----|-----|---------|
| 项目唯一名称 | 4 | 32 | 必须包含字母、数字和短横线 |
| 项目显示名称 | 4 | 48 | 必须包含字母、数字和短横线 |
| 描述 | 4 | 最长 2048 个字符 | 可以包含任意字符 |
| 环境唯一名称 | 4 | 32 | 必须包含字母、数字和短横线 |
| 环境显示名称 | 4 | 48 | 最长 48 个字符 | 必须包含字母、数字和短横线 |
| API 密钥名称 | 4 | 48 | 最长 48 个字符 | 必须包含字母、数字 |
| 域名 | 3 | 255 | 必须是有效的域名 |

*最后更新时间：2025 年 1 月*