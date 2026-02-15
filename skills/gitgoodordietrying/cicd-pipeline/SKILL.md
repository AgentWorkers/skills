---
name: cicd-pipeline
description: 使用 GitHub Actions 创建、调试和管理持续集成/持续交付（CI/CD）管道。当用户需要设置自动化测试、部署、发布或工作流程时，可以使用此方法。内容包括工作流程语法、常见模式、秘钥管理、缓存、矩阵构建以及故障排除。
metadata: {"clawdbot":{"emoji":"🚀","requires":{"anyBins":["gh","git"]},"os":["linux","darwin","win32"]}}
---

# CI/CD 流程（GitHub Actions）

使用 GitHub Actions 设置和管理 CI/CD 流程。涵盖工作流创建、测试、部署、发布自动化以及调试等内容。

## 使用场景

- 在提交代码（push）或创建 Pull Request（PR）时设置自动化测试
- 创建部署流程（包括测试环境和生产环境）
- 使用变更日志和标签自动化发布流程
- 调试失败的 CI 流程
- 设置跨平台测试的矩阵构建（matrix builds）
- 在 CI 中管理密钥（secrets）和环境变量
- 通过缓存和并行处理优化 CI 流程

## 快速入门：为项目添加 CI 功能

### Node.js 项目

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

### Python 项目

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt
      - run: pytest
      - run: ruff check .
```

### Go 项目

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: "1.22"
      - run: go test ./...
      - run: go vet ./...
```

### Rust 项目

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: cargo test
      - run: cargo clippy -- -D warnings
```

## 常见模式

### 跨版本/操作系统的矩阵构建（matrix builds）

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: [18, 20, 22]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

### 条件化任务（conditional jobs）

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
```

### 缓存依赖项（cache dependencies）

```yaml
# Node.js (automatic with setup-node)
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: npm  # or yarn, pnpm

# Generic caching
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/pip
      ~/.cargo/registry
      node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-deps-
```

### 保存构建结果（save build outputs）

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/
    retention-days: 7

# Download in another job
- uses: actions/download-artifact@v4
  with:
    name: build-output
    path: dist/
```

### 定时执行（cron）

```yaml
on:
  schedule:
    - cron: "0 6 * * 1"  # Every Monday at 6 AM UTC
  workflow_dispatch:  # Also allow manual trigger
```

## 部署流程

### 在特定标签下部署到生产环境

```yaml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build
      - run: npm test

      # Create GitHub release
      - uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
          files: |
            dist/*.js
            dist/*.css
```

### 部署到多个环境

```yaml
name: Deploy

on:
  push:
    branches: [main, staging]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - run: |
          if [ "${{ github.ref }}" = "refs/heads/main" ]; then
            ./deploy.sh production
          else
            ./deploy.sh staging
          fi
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

### 使用 Docker 构建并推送代码

```yaml
name: Docker

on:
  push:
    branches: [main]
    tags: ["v*"]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 在发布时通过 npm 发布代码

```yaml
name: Publish

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: https://registry.npmjs.org
      - run: npm ci
      - run: npm test
      - run: npm publish --provenance
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## 密钥管理

### 通过 CLI 设置密钥

```bash
# Set a repository secret
gh secret set DEPLOY_TOKEN --body "my-secret-value"

# Set from a file
gh secret set SSH_KEY < ~/.ssh/deploy_key

# Set for a specific environment
gh secret set DB_PASSWORD --env production --body "p@ssw0rd"

# List secrets
gh secret list

# Delete a secret
gh secret delete OLD_SECRET
```

### 在工作流中使用密钥

```yaml
env:
  # Available to all steps in this job
  DATABASE_URL: ${{ secrets.DATABASE_URL }}

steps:
  - run: echo "Deploying..."
    env:
      # Available to this step only
      API_KEY: ${{ secrets.API_KEY }}
```

### 环境保护规则

- 通过 GitHub 用户界面或 API 设置部署前的审核流程
- 设置等待时间（wait timers）
- 限制可以提交代码的分支
- 定义自定义的部署分支策略

```bash
# View environments
gh api repos/{owner}/{repo}/environments | jq '.environments[].name'
```

## 工作流调试

### 重新运行失败的任务

```bash
# List recent workflow runs
gh run list --limit 10

# View a specific run
gh run view <run-id>

# View failed job logs
gh run view <run-id> --log-failed

# Re-run failed jobs only
gh run rerun <run-id> --failed

# Re-run entire workflow
gh run rerun <run-id>
```

### 使用 SSH 和 tmate 进行调试

```yaml
# Add this step before the failing step
- uses: mxschmitt/action-tmate@v3
  if: failure()
  with:
    limit-access-to-actor: true
```

### 常见故障及解决方法

- **“权限被拒绝”（Permission denied）**：检查脚本的权限设置
- **“找不到 Node 模块”（Node modules not found）**：确保 Node.js 模块已正确安装
- **“集成环境无法访问资源”（Resource not accessible by integration）**：检查网络连接或权限问题
- **缓存未恢复**：检查缓存配置是否正确
- **工作流未触发**：确认工作流文件位于默认分支，并检查触发事件（如 `push` 或 `pull_request`）是否正确，以及分支过滤条件是否准确

## 工作流验证

- 在提交代码前在本地验证工作流的正确性
- 将工作流以图表形式查看（view workflow as graph）

## 高级模式

- 重用工作流（reuse workflows）
- 防止重复执行（prevent duplicate runs）
- 使用路径过滤器（path filters）仅针对相关变更执行任务
- 在单仓库项目中仅测试被修改的包（monorepo: only test changed packages）

## 提示

- 在调试时，可以使用 `workflow_dispatch` 手动触发工作流
- 为确保供应链安全，使用特定的动作版本（如 `uses: actions/checkout@b4ffde...`）
- 对于非关键步骤（如代码检查），可以设置 `continue-on-error: true` 以允许流程继续执行
- 为防止构建过程无限循环，可以为任务设置超时时间（默认为 360 分钟）
- 使用 `outputs` 参数在任务之间传递数据
- 对于自托管的构建环境，使用 `runs-on: self-hosted` 并指定目标机器

---

（注：由于提供的 SKILL.md 文件内容较为简短，部分代码块（```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm test
      - run: npm run lint
``` 等）为空，因此在翻译中保留了占位符。在实际应用中，这些占位符需要被具体的代码示例所替换。）