---
name: quality-gates
model: fast
category: testing
description: 在开发的每个阶段都设置质量检查点——从提交代码（pre-commit）到部署完成（post-deploy）——并提供相应的配置示例、阈值表、绕过规则（bypass protocols），以及与持续集成/持续部署（CI/CD）系统的集成方案。这些内容可用于设置质量自动化流程、配置CI管道、制定代码覆盖率阈值，或定义部署要求。
version: 1.0
---

# 质量检查机制

在开发的每个阶段都要实施质量检查。每个检查点都明确了需要检查的内容、执行的时间点，以及是否会导致开发流程的停滞。

---

## 使用场景

- **提交代码前**：在代码被记录到版本历史之前，捕获代码格式错误、类型错误以及敏感信息（如密码）等问题。
- **合并代码前**：确保所有测试用例都通过，代码覆盖率达到最低要求，并且代码已经过审查。
- **部署前**：验证集成测试的结果、进行安全扫描，并检查性能指标是否符合标准。
- **代码审查期间**：确认所有自动化检查都通过，并满足人工审查的要求。
- **部署后**：监控系统的运行状态、错误率以及性能指标。

---

## 检查点概述

| 检查点 | 执行时间 | 检查内容 | 是否会阻止开发流程继续？ |
|------|------|--------|-----------|
| 提交前 | `git commit` | 代码格式检查、类型检查、敏感信息扫描 | 是 |
| 推送前 | `git push` | 单元测试、构建验证 | 是 |
| 合并前 | 提交请求（PR/MR）的审批 | 全部测试用例通过、代码审查完成、代码覆盖率达标 | 是 |
| 部署前（测试环境） | 将代码部署到测试环境 | 集成测试、性能测试、安全扫描 | 是 |
| 部署前（生产环境） | 将代码部署到生产环境 | 测试环境验证、负载测试、回滚计划准备 | 是 |
| 部署后 | 部署完成后 | 系统健康状况检查、错误率监控、性能基准测试 | 发出警报 |

---

## 提交前检查的配置方法

### 使用 Husky 和 lint-staged（Node.js）

```json
{
  "lint-staged": {
    "*.{js,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yaml}": ["prettier --write"]
  }
}
```

### 使用其他工具进行提交前检查（Python）

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks:
      - id: mypy
```

### 敏感信息扫描（提交前钩子）

```bash
#!/bin/sh
# .git/hooks/pre-commit
gitleaks protect --staged --verbose
if [ $? -ne 0 ]; then
  echo "Secrets detected. Commit blocked."
  exit 1
fi
```

---

## 持续集成/持续部署（CI/CD）中的检查点配置

### 使用 GitHub Actions

```yaml
name: Quality Gates
on:
  pull_request:
    branches: [main]

jobs:
  lint-and-typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck

  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm test -- --coverage
      - name: Check coverage threshold
        run: |
          COVERAGE=$(jq '.total.lines.pct' coverage/coverage-summary.json)
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      - uses: gitleaks/gitleaks-action@v2

  build:
    needs: [lint-and-typecheck, unit-tests, security-scan]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
```

将这些检查点设置为**必需的状态检查**，确保只有在所有检查都通过后才能合并代码。

---

## 代码覆盖率检查

| 检查类型 | 最低要求 | 备注 |
|------|-------------------|-------|
| 单元测试 | 80% 的代码覆盖率 | 包括每个文件和整体代码 |
| 集成测试 | 60% 的集成点被覆盖 | 包括 API 接口和数据库查询 |
| 端到端测试 | 所有关键路径都必须被覆盖 | 包括认证逻辑和核心业务流程 |
| **不允许覆盖率下降**：新代码不能降低整体覆盖率 |

### 强制执行覆盖率要求

```json
// jest.config.js or vitest.config.ts
{
  "coverageThreshold": {
    "global": {
      "branches": 75,
      "functions": 80,
      "lines": 80,
      "statements": 80
    }
  }
}
```

对于“不允许覆盖率下降”的规则，需要在持续集成（CI）过程中将当前分支的覆盖率与基准分支进行比较，如果覆盖率下降则拒绝合并。

---

## 安全检查

### 依赖项扫描

| 开发框架 | 使用工具 | 命令 |
|-----------|------|---------|
| Node.js | npm audit | `npm audit --audit-level=high` |
| Python | pip-audit | `pip-audit --strict` |
| Rust | cargo audit | `cargo audit` |
| Go | govulncheck | `govulncheck ./...` |
| 通用工具 | Trivy | `trivy fs --severity HIGH,CRITICAL .` |

### 敏感信息检测

| 工具 | 适用场景 | 命令 |
|------|----------|---------|
| gitleaks | 提交前和持续集成过程中 | `gitleaks protect --staged` |
| TruffleHog | 深度历史代码扫描 | `trufflehog git file://. --only-verified` |
| detect-secrets | 基线对比扫描 | `detect-secrets scan --baseline .secrets.baseline` |

---

## 性能检查

### 包大小控制

```json
{
  "bundlesize": [
    { "path": "dist/main.*.js", "maxSize": "150 kB" },
    { "path": "dist/vendor.*.js", "maxSize": "250 kB" },
    { "path": "dist/**/*.css", "maxSize": "30 kB" }
  ]
}
```

### Lighthouse 持续集成（CI）中的性能阈值

```json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["error", { "minScore": 0.9 }],
        "first-contentful-paint": ["error", { "maxNumericValue": 2000 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }]
      }
    }
  }
}
```

### API 响应时间限制

| API 类型 | P50% 响应时间 | P95% 响应时间 | P99% 响应时间 |
|---------------|-----|-----|-----|
| 读取（GET 请求） | < 100 毫秒 | < 300 毫秒 | < 500 毫秒 |
| 写入（POST/PUT 请求） | < 200 毫秒 | < 500 毫秒 | < 1000 毫秒 |
| 搜索/聚合请求 | < 300 毫秒 | < 800 毫秒 | < 2000 毫秒 |
| 系统健康检查 | < 50 毫秒 | < 100 毫秒 | < 200 毫秒 |

通过负载测试工具（如 k6、Artillery）在持续集成过程中执行这些检查，并设置通过/失败的阈值。

---

## 代码审查

### 所需的审批流程

| 修改范围 | 所需的审批流程 |
|--------------|--------------------|
| 标准代码修改 | 至少需要 1 个审批 |
| 基础设施相关、认证机制、支付逻辑、数据模型修改 | 需要 2 个审批 |
| 依赖项更新、加密相关修改 | 需要安全团队的审批 |

### 代码所有者（CODEOWNERS）

```text
# .github/CODEOWNERS
*                    @team/engineering
/infra/              @team/platform
/src/auth/           @team/security
/src/payments/       @team/payments @team/security
*.sql                @team/data-engineering
Dockerfile           @team/platform
```

---

## 检查点豁免机制

### 何时可以豁免检查

- 针对对用户产生影响的紧急修复操作。
- 对于简单的修改（如拼写错误或注释修改），如果自动化检查过于繁琐，可以豁免。
- 由于上游代码问题导致持续集成（CI）流程失败时的依赖项更新（非由当前团队代码引起）。

### 每次豁免检查时需要提供的文档

1. **豁免理由**：说明为什么当前检查点无法通过。
2. **风险评估**：说明跳过检查可能带来的潜在问题。
3. **后续处理流程**：提供跟踪问题解决过程的 ticket 链接。
4. **审批人**：批准豁免的资深工程师或团队负责人的姓名。

---

## 绝对禁止的行为

- **绝不要**永久关闭任何检查点——必须解决根本问题，不能移除这些安全保障措施。
- **绝不要**将敏感信息提交到任何代码分支——即使只是用于测试；代码历史记录是永久保存的。
- **绝不要**为了通过部署而跳过测试——如果测试失败，说明代码尚未准备好。
- **绝不要**合并那些未通过必要检查的代码——这样做会损害团队的信任。
- **绝不要**将覆盖率阈值设置为 0%——即使覆盖率很低，也比没有好。
- **绝不要**为了加快速度而跳过安全扫描——生产环境中的安全漏洞造成的损失远大于持续集成（CI）所花费的时间。
- **绝不要**仅依赖部署后的检查——部署后的监控只能发现已经发生的问题，而无法预防问题；忽略警报会违背检查机制的初衷。