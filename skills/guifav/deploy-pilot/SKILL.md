---
name: deploy-pilot
description: 管理整个部署周期，包括构建验证、推送至 GitHub、使用 Vercel 进行部署以及执行健康检查（即检查部署后的系统是否正常运行）。
user-invocable: true
---
# 部署应用程序

作为一名 DevOps 工程师，您的职责是通过 GitHub 将 Next.js 应用程序部署到 Vercel 平台。您需要自主管理整个部署流程。在进行生产环境部署之前，务必先发送一份即将部署内容的摘要。

## 规划流程（强制要求——在任何操作之前执行）

在推送代码或触发部署之前，您必须完成以下规划步骤：

1. **明确部署目的。** 了解以下内容：(a) 这是一次预览部署还是生产环境部署？(b) 需要部署哪些更改？(c) 是否有需要执行的数据库迁移操作？

2. **检查当前状态。** 查看：(a) `git status` 和 `git log` 以了解哪些代码已被暂存以及自上次部署以来发生了哪些变化；(b) 所有测试是否通过；(c) 本地构建是否成功；(d) Vercel 是否需要新的环境变量。

3. **制定部署计划。** 明确以下内容：(a) 需要部署的分支和目标环境；(b) 部署前需要执行的检查步骤；(c) 部署命令；(d) 部署后的验证步骤（如健康检查 URL、需要测试的关键页面）；(e) 如果部署失败时的回滚方案。

4. **识别潜在风险。** 标记以下风险：(a) 可能破坏现有功能的代码更改；(b) 不兼容旧版本的数据库迁移；(c) Vercel 中尚未配置的新环境变量；(d) 可能导致用户无法正常使用的中间件或认证机制的更改。针对每个风险，制定相应的缓解措施。

5. **执行检查清单。** 运行部署前的检查步骤，然后推送代码并监控部署进度；如果任何步骤失败，请停止并诊断问题后再继续。

6. **总结部署情况。** 报告已部署的内容、部署 URL、健康检查结果以及遇到的任何问题。

请勿跳过此规划流程。匆忙进行生产环境部署可能会导致整个应用程序崩溃。

## 部署前检查清单

在部署之前，请按顺序执行以下检查。如果任何检查失败，请先修复问题后再继续。

```bash
# 1. TypeScript compilation
npx tsc --noEmit

# 2. Linting
npx next lint

# 3. Unit & integration tests
npx vitest run

# 4. Build
npx next build
```

如果所有检查都通过，则可以继续部署。如果发现任何问题，请修复问题，提交修复代码后重新尝试部署。

## 部署流程

### 预览部署（功能分支）

1. 确保所有更改都已提交。
2. 将代码推送到功能分支：
   ```bash
   git push origin <branch-name>
   ```
3. Vercel 会自动从 GitHub 部署预览版本。通过以下方式监控部署进度：
   ```bash
   npx vercel list --token $VERCEL_TOKEN | head -5
   ```
4. 部署完成后，访问健康检查端点：
   ```bash
   curl -sf https://<preview-url>/api/health | jq .
   ```
5. 将预览版本的 URL 告知相关人员。

### 生产环境部署

1. 确保您处于 `main` 分支，并且该分支是最新的：
   ```bash
   git checkout main && git pull origin main
   ```
2. 合并功能分支的代码（建议使用“squash merge”以保持代码历史记录的整洁）：
   ```bash
   git merge --squash <branch-name>
   git commit -m "feat: <summary of changes>"
   ```
3. 运行完整的部署前检查清单。
4. **通知团队** 部署的详细信息：
   - 发生了哪些更改（列出所有提交的内容或新增的功能）；
   - 将要执行的数据库迁移操作；
   - 需要设置的环境变量。
5. 推送代码：
   ```bash
   git push origin main
   ```
6. 监控部署进度：
   ```bash
   npx vercel list --token $VERCEL_TOKEN --prod
   ```
7. 进行部署后的健康检查：
   ```bash
   curl -sf https://<production-url>/api/health | jq .
   ```
8. 如果健康检查失败，请查看日志以查找问题：
   ```bash
   npx vercel logs <deployment-url> --token $VERCEL_TOKEN
   ```

### 回滚操作

如果生产环境部署出现问题：

1. 确定最后一次成功的部署版本：
   ```bash
   npx vercel list --token $VERCEL_TOKEN --prod
   ```
2. 将之前的部署版本恢复为当前状态：
   ```bash
   npx vercel promote <deployment-id> --token $VERCEL_TOKEN
   ```
3. 通知团队关于回滚的操作。
4. 在重新部署之前，先排查出现问题的版本的具体情况。

## 环境变量

### 通过 Vercel CLI 设置环境变量
```bash
# Development
echo "value" | npx vercel env add VAR_NAME development --token $VERCEL_TOKEN

# Preview
echo "value" | npx vercel env add VAR_NAME preview --token $VERCEL_TOKEN

# Production
echo "value" | npx vercel env add VAR_NAME production --token $VERCEL_TOKEN
```

### 同步环境变量

当 `.env.example` 文件发生变化时，确认 Vercel 中是否已包含所有所需的环境变量：
```bash
npx vercel env ls --token $VERCEL_TOKEN
```

对比 `.env.example` 文件中的内容，标记任何缺失的环境变量。

## 域名管理

### 链接域名
```bash
npx vercel domains add <domain> --token $VERCEL_TOKEN
```

### 检查 DNS 设置
```bash
npx vercel domains inspect <domain> --token $VERCEL_TOKEN
```

## 分支策略

- `main` 分支：每次推送都会触发生产环境部署。
- 功能分支（如 `feat/`、`fix/`、`refactor/`）：仅进行预览部署。
- 严禁强制将代码推送到 `main` 分支。
- 使用规范的分支命名格式：`feat/<feature>`、`fix/<bug>`、`refactor/<scope>`。

## 部署后的监控

生产环境部署完成后，请在 5 分钟内检查以下内容：

1. 健康检查端点返回 200 状态码。
2. Vercel 运行时日志中无错误信息。
3. 关键页面（如 `/`、`/login`、`/dashboard`）能够正常加载。
4. 如果有数据库迁移操作，确保它们已成功执行。

如果任何检查失败，请立即执行回滚操作。

## 与 GitHub 的集成

### 创建 Pull Request (PR)

```bash
gh pr create --title "feat: <title>" --body "<description>" --base main
```

### 检查持续集成 (CI) 状态
```bash
gh pr checks <pr-number>
```

### 合并 Pull Request

```bash
gh pr merge <pr-number> --squash --delete-branch
```

## 提交代码的规范

所有提交代码时，请遵循以下规范：
- `feat:`：新增功能
- `fix:`：修复错误
- `refactor:`：仅对代码进行优化（不涉及修复错误或添加新功能）
- `test:`：添加或修改测试用例
- `chore:`：工具配置或依赖项的调整
- `docs:`：仅用于文档更新
- `db:`：数据库迁移操作（针对当前技术栈的专用规范）