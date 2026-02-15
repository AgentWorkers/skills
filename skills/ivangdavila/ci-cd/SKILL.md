---
name: "CI-CD"
description: "自动化构建、测试和部署过程，适用于网页应用、移动应用以及后端应用程序。"
---

## 使用场景

触发条件：自动化部署、持续集成（CI）、管道设置（pipeline setup）、GitHub Actions、GitLab CI、构建失败（build failure）、自动部署（automatic deployment）、CI配置（CI configuration）、发布自动化（release automation）。

## 平台选择

| 技术栈 | 推荐平台 | 原因 |
|-------|-------------|-----|
| Web 应用（Next.js、Nuxt、静态网站） | Vercel、Netlify | 零配置、自动部署、提供预览网址（preview URLs） |
| 移动应用（iOS/Android/Flutter） | Codemagic、Bitrise + Fastlane | 预先配置的签名流程（signing process）、应用商店上传（app store upload） |
| 后端应用/Docker | GitHub Actions、GitLab CI | 完全的控制权、支持自托管运行器（self-hosted runners） |
| 单一代码库（Monorepo） | Nx/Turborepo + GitHub Actions | 能够检测到问题并进行构建缓存（problem detection and build caching） |

**决策流程：** 如果平台支持自动部署（如 Vercel、Netlify），则无需使用自定义的 CI 工具。仅在需要测试、自定义构建或部署到自有基础设施时，才使用 GitHub Actions。

## 快速入门模板

有关可复制粘贴的工作流程模板，请参阅 `templates.md`。

## 常见管道配置问题

| 问题 | 影响 | 解决方法 |
|---------|--------|-----|
| 使用 `latest` 镜像标签 | 构建过程可能出错 | 固定版本标签：例如 `node:20.11.0` |
| 未缓存依赖项 | 每次构建耗时增加 5–10 分钟 | 将 `node_modules` 和 `.next/cache` 文件缓存起来 |
| 工作流文件中包含敏感信息 | 信息可能泄露到日志或 Pull Request 中 | 使用平台提供的安全机制（platform secrets）或 OIDC（OpenID Connect） |
| 未设置 `timeout-minutes` | 构建任务会无限期运行，消耗资源 | 必须设置 `timeout-minutes: 15` |
| 无并发控制 | 快速推送时会导致重复构建 | 按分支或 Pull Request 分组构建任务 |
| 每次推送都进行构建 | 浪费资源 | 仅在推送到主分支（main branch）时进行构建，Pull Request 时进行测试 |

## 移动应用特有的问题：代码签名（Code Signing）

这是移动应用开发中的主要难题。iOS 需要证书和配置文件；Android 需要密钥库。

**解决方法：** 使用 **Fastlane Match** 功能——将证书和配置文件存储在 Git 仓库中，并在团队和 CI 系统间同步。

```bash
# One-time setup
fastlane match init
fastlane match appstore

# In CI
fastlane match appstore --readonly
```

有关 iOS、Android 和 Flutter 的详细 CI/CD 配置指南，请参阅 `mobile.md`。

## Web 应用特有的问题：构建缓存（Build Caching）

Next.js 和 Nuxt 应用的构建过程在没有缓存的情况下会很慢。如果出现 “No Cache Detected” 警告，说明需要重新构建整个项目。

```yaml
# GitHub Actions: persist Next.js cache
- uses: actions/cache@v4
  with:
    path: .next/cache
    key: nextjs-${{ hashFiles('**/package-lock.json') }}
```

有关特定框架的配置细节，请参阅 `web.md`。

## 调试构建失败的问题

| 错误类型 | 可能原因 | 检查方法 |
|---------------|--------------|-------|
| 本地可以正常运行，但在 CI 中失败 | 环境差异 | 检查 Node.js 版本、环境变量和操作系统设置 |
| 偶尔失败 | 测试不稳定或资源限制 | 优化测试逻辑或增加构建超时时间 |
| 错误代码 `ENOENT` / 文件未找到 | 构建顺序问题或依赖项缺失 | 检查项目的 `needs:` 配置 |
| 结束代码 137 | 内存不足 | 使用更大的运行器或优化应用程序资源使用 |
| 证书/签名相关错误 | 证书过期或凭证不匹配 | 使用 Fastlane 的 `Match` 功能重新生成证书 |

## 本文档未涵盖的内容

- 容器编排（Kubernetes） → 请参阅 `k8s` 文档 |
- 服务器配置 → 请参阅 `server` 文档 |
- 监控与可观测性（Monitoring and Observability） → 请参阅 `monitoring` 文档