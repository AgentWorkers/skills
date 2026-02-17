---
name: hosting
description: **元技能：** 通过协调 GitHub API、Vercel/Netlify、域名 DNS 操作以及 API Gateway，实现本地 Web 项目零摩擦地部署到生产环境。适用于用户希望将本地网站部署到支持 SSL、持续集成/持续部署（CI/CD）环境，并可选配置自定义域名的场景。
homepage: https://clawhub.ai
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🚀","requires":{"bins":["git","node","npm","npx"],"env":["MATON_API_KEY"],"config":[]},"note":"Requires local installation of github-api, vercel or netlify, and optionally domain-dns-ops/api-gateway for custom infra or DNS operations."}}
---
## 目的

将本地的代码库或静态网站发布到生产环境，同时尽量减少 DevOps 阶段中的复杂性和摩擦。

**主要成果：**
1. 创建并同步代码库；
2. 触发部署流程；
3. 验证网站是否已成功上线；
4. 在需要时记录自定义域名的配置信息。

这是一项用于协调不同开发工具和服务的技能，但它本身不能保证系统的正常运行时间（uptime）或服务水平协议（SLA）。

## 必需安装的技能

**核心技能：**
- `github-api`（最新版本：`1.0.3`）
- 一种部署工具：
  - `vercel`（最新版本：`1.0.1`），或
  - `netlify`（最新版本：`1.0.0`）

**可选技能：**
- `domain-dns-ops`（最新版本：`1.0.0`，具体环境而定）
- `api-gateway`（最新版本：`1.0.29`）

**安装/更新步骤：**
（请参考相应的文档或命令行指南来完成安装和更新操作。）

## 验证步骤：**
（请参考相应的文档或命令行指南来完成验证操作。）

## 重要名称映射规则：**
- 如果用户请求使用 `/netlify`，则将其映射到 `/netlify` 服务。

## 必需的凭证

**强制要求：**
- `MATON_API_KEY`（用于 `github-api` 和 `api-gateway` 的身份验证）

**部署工具的认证方式：**
- **Vercel：** 使用 `vercel login` 或 `VERCEL_TOKEN` 进行登录认证。
- **Netlify：** 使用 `netlify login` 或 `NETLIFY_AUTH_TOKEN` 进行登录认证。

**（通过 `api-gateway` 进行自定义基础设施管理时的可选要求：**  
在 Maton 控制面板（`ctrl.maton.ai`）中配置相应的 OAuth 连接。

## 预部署检查：**
（请参考相应的文档或命令行指南来完成预部署检查。）

**强制要求：**
- 如果缺少必要的凭证或令牌，系统必须立即停止执行部署流程，并返回错误信息（例如 `MissingAPIKeys`）。
- 对于未受影响的部署阶段，应继续执行并标记输出为 `Partial`（部分完成）。

## 需要用户首先提供的输入信息：**
- `project_path`（项目路径）
- `repo_name`（代码库名称）
- `repo_visibility`（代码库的可见性，`private` 或 `public`）
- `deploy_target`（部署目标，`vercel` 或 `netlify`）
- `framework_hint`（可选，用于提示使用哪种部署工具）
- `custom_domain`（可选，用于指定自定义域名）
- `domain_provider`（可选，例如 Cloudflare 或 Namecheap 等域名服务提供商）
- `infra_mode`（部署模式，`frontend-static`、`fullstack-managed` 或 `vps-server`）

**注意事项：**
在明确指定部署目标和代码库可见性之前，切勿开始部署流程。

## 各工具的职责：

### `github-api`
- 用于创建代码库和配置远程同步：
  - 创建代码库（包括用户名和组织名）
  - 设置代码库的可见性
  - 保存远程仓库的元数据，以便后续进行推送和部署操作

**操作限制：**
- 需要 `MATON_API_KEY` 进行身份验证
- 使用 Maton 管理的 OAuth 连接
- 如果缺少或无效的凭证，会导致身份验证失败

### `vercel`
- 用于管理前端或全栈应用的部署：
  - 链接代码库到部署平台
  - 触发部署（使用 `vercel link` 或 `vercel --prod` 命令）
  - 检查部署和域名的状态
  - 根据需要管理域名的配置

### `netlify`
- 作为另一种部署工具：
  - 创建或链接代码库到 Netlify 服务器
  - 从 GitHub 自动触发持续集成/持续部署（CI/CD）流程
  - 支持手动部署或生产环境部署
  - 提供环境变量配置和域名管理功能

### `domain-dns-ops`
- 仅在特定环境下使用

**重要限制：**
- 该技能的具体配置依赖于特定环境（例如 `~/Projects/manager` 文件中的设置）
- 如果该配置文件不存在，则不能保证该技能在不同环境中也能正常使用

### `api-gateway`
- 用于在存在关联应用时进行额外的基础设施管理或 API 操作

**操作限制：**
- 需要 `MATON_API_KEY` 进行身份验证
- 每个目标服务都需要单独配置 OAuth 连接
- 如果连接失败，会返回 `400` 错误代码
- 如果缺少或无效的 Maton 凭证，会返回 `401` 错误代码

## 标准的流程步骤：

1. **代码检查**：
  - 扫描项目根目录，查找与开发框架相关的文件（如 `package.json`、`next.config.*`、`vite.config.*`、`index.html`、`dist/`、`build/`）
  - 确定项目的类型（Next.js、Vite、静态 HTML 等）
  - 确定默认的构建和发布路径

2. **Git 初始化**：
  - （如有需要）初始化 Git 仓库
  - 通过 `github-api` 创建远程仓库
  - 设置仓库的远程地址，提交代码并推送到远程仓库

3. **基础设施检查**：
  - 根据项目类型推荐合适的托管服务（Vercel 或 Netlify）
  - 如果支持自定义基础设施，提供相应的配置选项

**输出内容：**
- `ProjectDetection`：检测到的开发框架和构建/发布配置信息
- `RepoStatus`：代码库的详细信息（URL、默认分支、推送状态）
- `InfraGateStatus`：选择的托管服务、当前状态以及可能存在的阻碍因素及解决方法
- `DeploymentStatus`：网站的实时 URL、部署 ID 及最终状态（成功或失败）
- `CustomDomainPlan`：自定义域名的配置信息（包括所需 DNS 记录的设置位置和验证步骤）
- `NextActions`：如果仍有手动操作步骤，提供具体的命令或操作指南

## 质量控制：
- 在最终输出之前，务必验证以下内容：
  - 根据实际文件确认开发框架的类型
  - 确保远程仓库存在且推送路径有效
  - 确保部署 URL 可访问且状态正常
  - 确保自定义域名的配置正确无误
  - 所有缺失的凭证或连接问题都必须被及时披露

**错误处理机制：**
- 如果缺少 `MATON_API_KEY`，则返回错误信息并跳过相关部署步骤
- 如果缺少 Vercel 或 Netlify 的认证信息，返回错误信息并提供登录/令牌设置的指导
- 如果 Git 推送失败，返回错误信息并提示重试
- 如果部署过程中出现错误，返回构建日志和修复建议
- 如果自定义域名配置有问题，返回相应的域名设置步骤
- 如果使用的部署工具不支持某些功能，会明确说明限制并提供替代方案

**注意事项：**
- 除非网站能够正常访问，否则不得声称部署成功
- 在 DNS 和 HTTPS 配置完成之前，不得声称自定义域名已经生效
- 必须如实披露所有相关的限制和问题

**其他注意事项：**
- 绝不夸大部署的成功率
- 在 DNS 和 HTTPS 配置完成之前，不得声称自定义域名已经激活
- 必须如实告知用户所有相关的限制和问题