---
name: cicd-pipeline-generator
description: 此技能适用于创建或配置用于自动化测试、构建和部署的 CI/CD（持续集成/持续部署）管道文件。您可以使用它来生成 GitHub Actions 工作流、GitLab CI 配置文件、CircleCI 配置文件，或其他 CI/CD 平台的配置文件。特别适合为 Node.js/Next.js 应用程序设置自动化管道，包括代码检查（linting）、测试、构建，以及将应用程序部署到 Vercel、Netlify 或 AWS 等平台。
---

# CI/CD 流程生成器

## 概述

本工具能够为多种平台（GitHub Actions、GitLab CI、CircleCI、Jenkins）生成可用于生产环境的 CI/CD 流程配置文件。它提供了模板和指导，帮助用户设置自动化工作流程，以实现代码检查（linting）、测试、构建和部署等功能，尤其适用于 Node.js/Next.js 项目。

## 核心功能

### 1. 平台选择

根据项目需求选择合适的 CI/CD 平台：

- **GitHub Actions**：适用于托管在 GitHub 上的项目，具有原生集成功能。
- **GitLab CI/CD**：适合需要复杂流程管理的 GitLab 仓库。
- **CircleCI**：针对 Docker 工作流程进行了优化，构建速度快。
- **Jenkins**：适用于自托管环境，具有高度可定制性。

详细的信息、平台优缺点及使用建议请参考 `references/platform-comparison.md`。

### 2. 流程配置生成

遵循以下原则生成流程配置：

#### 流程阶段

流程通常包括以下标准阶段：

1. **安装依赖项**：
   - 从仓库检出代码
   - 设置运行时环境（Node.js 版本）
   - 恢复缓存的依赖项
   - 使用 `npm ci` 安装依赖项
   - 为后续构建缓存依赖项

2. **代码检查（Linting）**：
   - 运行 ESLint 进行代码质量检查
   - 运行 TypeScript 类型检查
   - 在发现代码问题时立即停止构建

3. **测试**：
   - 执行单元测试
   - 执行集成测试
   - 生成代码覆盖率报告
   - 将覆盖率报告上传到Codecov、Coveralls 等服务

4. **构建**：
   - 创建生产环境的构建版本
   - 确认构建成功
   - 存储构建结果

5. **部署**：
   - 部署到测试环境（develop 分支）
   - 部署到生产环境（main 分支）
   - 运行部署后的测试

#### 缓存策略

实施有效的缓存机制以加快构建速度：
```yaml
# Cache node_modules based on package-lock.json
cache:
  key: ${{ hashFiles('package-lock.json') }}
  paths:
    - node_modules/
    - .npm/
```

#### 环境变量配置

配置必要的环境变量：
- `NODE_ENV`：设置为 `production` 以启用生产环境配置
- 平台特定的令牌：作为秘密信息存储
- 构建时的变量：传递给构建过程

### 3. 模板使用

使用 `assets/` 目录中的模板：

**GitHub Actions 模板**（`assets/github-actions-nodejs.yml`）：
- 包含代码检查、测试、构建和部署的多步骤工作流程
- 支持多版本 Node.js 的矩阵构建（可选）
- 集成 Vercel 部署
- 代码覆盖率报告功能

**GitLab CI 模板**（`assets/gitlab-ci-nodejs.yml`）：
- 多阶段流程
- 依赖项缓存
- 手动控制生产环境部署
- 自动化测试环境部署
- 支持代码覆盖率报告

使用模板的步骤：
1. 复制相应的模板文件
2. 将文件放置在正确的位置：
   - GitHub Actions：`.github/workflows/ci.yml`
   - GitLab CI：`.gitlab-ci.yml`
3. 自定义部署目标、环境变量和分支名称
4. 将所需的秘密信息添加到平台配置中

### 4. 部署配置

#### Vercel 部署

对于 GitHub Actions：
```yaml
- uses: amondnet/vercel-action@v25
  with:
    vercel-token: ${{ secrets.VERCEL_TOKEN }}
    vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
    vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
    vercel-args: '--prod'
```

**所需秘密信息**：
- `VERCEL_TOKEN`：从 Vercel 账户设置中获取
- `VERCEL_ORG_ID`：从 Vercel 项目设置中获取
- `VERCEL_PROJECT_ID`：从 Vercel 项目设置中获取

#### Netlify 部署
```yaml
- run: |
    npm install -g netlify-cli
    netlify deploy --prod --dir=.next
  env:
    NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
    NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

#### AWS S3 + CloudFront 部署
```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1

- run: |
    aws s3 sync .next/static s3://${{ secrets.S3_BUCKET }}/static
    aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_DIST_ID }} --paths "/*"
```

### 5. 测试集成

配置测试执行并生成相应的报告：

**Jest 配置**：
```yaml
- name: Run tests with coverage
  run: npm test -- --coverage --coverageReporters=text --coverageReporters=lcov

- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    files: ./coverage/lcov.info
    flags: unittests
```

**快速失败策略**：
```yaml
# Run quick tests first
jobs:
  lint:  # Fails in ~30 seconds
  test:  # Fails in ~2 minutes
  build: # Fails in ~5 minutes
    needs: [lint, test]
  deploy:
    needs: [build]
```

### 6. 基于分支的工作流程

根据分支的不同配置不同的流程行为：

**特性分支/拉取请求（Feature Branches/PRs）**：
- 仅执行代码检查和测试
- 不进行部署
- 在拉取请求中添加测试结果评论

**开发分支（Develop Branch）**：
- 执行代码检查和测试
- 部署到测试环境
- 自动部署

**主分支（Main Branch）**：
- 执行代码检查和测试
- 部署到生产环境
- 需要手动批准（可选）
- 创建发布标签

**示例**：
```yaml
deploy_staging:
  if: github.ref == 'refs/heads/develop'
  # Deploy to staging

deploy_production:
  if: github.ref == 'refs/heads/main'
  environment: production  # Requires manual approval
  # Deploy to production
```

## 工作流程决策树

按照以下决策树生成合适的 CI/CD 流程：

1. **选择哪个平台？**
   - 如果使用 GitHub，则使用 `assets/github-actions-nodejs.yml`
   - 如果使用 GitLab，则使用 `assets/gitlab-ci-nodejs.yml`
   - 如果使用 CircleCI 或 Jenkins，则使用 GitHub Actions 模板
   - 不确定时，请参考 `references/platform-comparison.md`

2. **需要哪些流程阶段？**
   - 必须包括：代码检查、测试、构建
   - 可选：安全扫描、端到端测试、性能测试
   - 如果需要部署，则添加部署阶段

3. **使用哪种部署方式？**
   - 如果使用 Vercel，则参考 Vercel 的部署示例
   - 如果使用 Netlify，则使用 Netlify 的 CLI 方法
   - 如果使用 AWS，则使用 AWS Actions 或 CLI
   - 如果需要自定义部署方式，则编写自定义脚本

4. **触发条件是什么？**
   - 在向 main/develop 分支推送代码时触发
   - 在收到拉取请求时触发
   - 在创建标签时触发
   - 可以手动触发流程

5. **需要哪些环境变量？**
   - 平台相关的令牌（Vercel、Netlify、AWS）
   - 外部服务的 API 密钥
   - 构建时的环境变量
   - 特定功能的配置标志

## 最佳实践

### 安全性
- 将所有秘密信息存储在平台提供的秘密管理工具中（切勿直接写入代码）
- 使用最小权限的令牌（尽可能只读）
- 定期轮换秘密信息
- 审查秘密信息的访问权限
- 绝不要记录秘密信息（使用 `***` 进行遮蔽）

### 性能
- 积极使用缓存机制
- 并行执行独立的构建任务
- 对于多版本测试，使用矩阵构建方式
- 实施快速失败策略：先执行快速检查，再执行耗时的任务
- 优化 Docker 层的缓存

### 可靠性
- 明确指定 Node.js 的版本（例如使用 `18.x` 而不是 `18`）
- 提交 `package-lock.json` 文件以锁定依赖版本
- 为不可靠的外部服务添加重试逻辑
- 设置合理的超时时间（最长 10-15 分钟）
- 对于非关键步骤，使用 `continue-on-error` 选项

### 可维护性
- 为复杂逻辑添加注释
- 使用可重用的工作流程和模板
- 保持配置的简洁性（避免重复编写代码）
- 对所有流程更改进行版本控制
- 在 README 文件中记录所需的秘密信息

## 常见模式

### 多环境部署
```yaml
deploy_staging:
  environment: staging
  if: github.ref == 'refs/heads/develop'

deploy_production:
  environment: production
  if: github.ref == 'refs/heads/main'
  needs: [deploy_staging]
```

### 矩阵测试（Matrix Testing）
```yaml
strategy:
  matrix:
    node-version: [16.x, 18.x, 20.x]
    os: [ubuntu-latest, windows-latest]
```

### 条件化步骤
```yaml
- name: Deploy
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  run: npm run deploy
```

### 构建结果管理
```yaml
- name: Upload build
  uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: .next/
    retention-days: 7

- name: Download build
  uses: actions/download-artifact@v4
  with:
    name: build-output
```

## 故障排除

### 流程失败
1. 查看动作/任务的日志以获取错误信息
2. 确认环境变量和秘密信息是否设置正确
3. 在将代码添加到流程之前，在本地测试相关命令
4. 查阅文档中关于平台特定问题的解决方法

### 构建速度慢
1. 检查缓存机制是否正常工作（查看缓存命中/未命中的日志）
2. 并行执行独立的构建任务
3. 如果可能，使用更快的构建工具
4. 优化依赖项的安装过程

### 部署失败
1. 确认部署所需的令牌是否有效
2. 查看平台的状态页面
3. 查看部署日志
4. 在本地测试部署相关的命令

## 资源

### 模板（`assets/` 目录）
- `github-actions-nodejs.yml`：完整的 GitHub Actions 工作流程模板
- `gitlab-ci-nodejs.yml`：完整的 GitLab CI 流程模板

### 参考文档（`references/` 目录）
- `platform-comparison.md`：详细的 CI/CD 平台比较、部署方式、最佳实践和常见模式的文档

## 示例用法

**用户请求**：“创建一个在 GitHub Actions 中运行测试并部署到 Vercel 的工作流程”

**步骤**：
1. 复制 `assets/github-actions-nodejs.yml` 模板
2. 如果不存在 `.github/workflows/` 目录，则创建该目录
3. 将文件保存为 `.github/workflows/ci.yml`
4. 更新部署相关的配置信息（特别是 Vercel 的认证信息）
5. 将 `VERCEL_TOKEN`、`VERCEL_ORG_ID`、`VERCELPROJECT_ID` 等秘密信息添加到 GitHub 仓库的设置中
6. 提交并推送更改以触发工作流程

**用户请求**：“设置 GitLab CI，包括测试环境和生产环境的部署”

**步骤**：
1. 复制 `assets/gitlab-ci-nodejs.yml` 模板
2. 将文件保存到仓库的根目录
3. 配置 GitLab CI/CD 的相关变量（如 `VERCEL_TOKEN` 等）
4. 设置生产环境的部署相关配置
5. 提交更改以触发 CI/CD 流程

## 高级配置

### 单一仓库支持（Monorepo Support）
```yaml
paths:
  - 'apps/frontend/**'
  - 'packages/**'
```

### 定时执行（Scheduled Runs）
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
```

### 外部服务集成（External Service Integration）
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### 安全扫描（Security Scanning）
```yaml
- name: Run security audit
  run: npm audit --audit-level=moderate

- name: Check for vulnerabilities
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```