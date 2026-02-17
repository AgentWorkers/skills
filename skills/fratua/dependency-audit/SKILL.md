---
name: dependency-audit
description: 智能依赖项健康检查功能：包括安全审计、过时依赖项的检测、未使用的依赖项的识别，以及优先级的更新计划制定。
version: 1.0.0
author: Sovereign Skills
tags: [openclaw, agent-skills, automation, productivity, free, dependencies, security, audit]
triggers:
  - audit dependencies
  - check dependencies
  - dependency audit
  - security audit
  - outdated packages
---
# dependency-audit — 智能依赖项健康检查

该工具可检测您的项目所使用的包管理器，执行安全审计，识别过时或未使用的依赖项，并生成优先级排序的更新计划。

## 步骤

### 1. 检测包管理器

在项目根目录中查找以下文件：

| 文件名 | 所使用的包管理器 | 审计命令 |
|------|-----------|--------------|
| `package.json` | Node.js (npm/yarn/pnpm) | `npm audit` |
| `requirements.txt` / `pyproject.toml` / `Pipfile` | Python | `pip audit` |
| `Cargo.toml` | Rust | `cargo audit` |
| `go.mod` | Go | `govulncheck ./...` |
| `Gemfile` | Ruby | `bundle audit check` |

如果找到多个包管理器，请对所有包管理器执行审计；如果没有找到任何包管理器，请停止操作并通知用户。

### 2. 执行安全审计

**Node.js:**
```bash
npm audit --json 2>/dev/null
# Parse: advisories, severity (critical/high/moderate/low), affected package, fix available
```

**Python:**
```bash
pip audit --format=json 2>/dev/null || pip audit 2>/dev/null
# If pip-audit not installed: pip install pip-audit
```

**Rust:**
```bash
cargo audit --json 2>/dev/null
# If not installed: cargo install cargo-audit
```

### 3. 检查过时的依赖项

**Node.js:**
```bash
npm outdated --json 2>/dev/null
# Shows: current, wanted (semver-compatible), latest
```

**Python:**
```bash
pip list --outdated --format=json 2>/dev/null
```

**Rust:**
```bash
cargo outdated -R 2>/dev/null
# If not installed: cargo install cargo-outdated
```

### 4. 识别未使用的依赖项

**Node.js — 使用 depcheck:**
```bash
npx depcheck --json 2>/dev/null
```
该工具会报告未使用的依赖项以及缺失的依赖项。如果 `npx` 命令执行失败，可以手动扫描源代码文件：
```bash
# List all deps from package.json, then grep for imports
# Flag any dep not found in any .js/.ts/.jsx/.tsx file
```

**Python:** 比较代码中引用的依赖项与实际安装的依赖项：
```bash
# Extract imports from .py files
grep -rh "^import \|^from " --include="*.py" . | sort -u
# Compare against requirements.txt entries
```

### 5. 生成优先级排序的更新计划

将审计结果按优先级进行分类：

```markdown
## 🔴 Critical — Security Vulnerabilities
| Package | Severity | Current | Fixed In | Command |
|---------|----------|---------|----------|---------|
| lodash | CRITICAL | 4.17.19 | 4.17.21 | `npm install lodash@4.17.21` |

## 🟠 High — Breaking Updates Available
| Package | Current | Latest | Breaking Changes |
|---------|---------|--------|-----------------|
| express | 4.18.2 | 5.0.0 | New router API |

## 🟡 Medium — Minor/Patch Updates
| Package | Current | Latest | Command |
|---------|---------|--------|---------|
| axios | 1.5.0 | 1.6.2 | `npm install axios@1.6.2` |

## 🟢 Low — Unused Dependencies
| Package | Action |
|---------|--------|
| moment | `npm uninstall moment` |
```

### 6. 提供安全的更新命令

对于批量更新，生成可复制的更新命令：

```bash
# Security fixes (safe — patch updates only)
npm audit fix

# All compatible updates (non-breaking)
npm update

# Specific breaking update (test thoroughly)
npm install express@5.0.0
```

**针对 Python 的更新命令:**
```bash
pip install --upgrade package_name
```

### 7. 输出审计结果摘要

```markdown
# Dependency Health Report — [project-name]
**Date:** 2025-02-15 | **Ecosystem:** Node.js (npm)

| Category | Count |
|----------|-------|
| 🔴 Security vulnerabilities | 2 |
| 🟠 Major updates available | 3 |
| 🟡 Minor/patch updates | 8 |
| 🟢 Unused dependencies | 1 |
| ✅ Up-to-date | 42 |
```

## 特殊情况处理

- **包锁定文件冲突**: 如果 `package-lock.json` 与实际安装的依赖项不一致，请先运行 `npm install`。
- **使用私有仓库**: `npm audit` 可能会失败——建议使用 `--registry=https://registry.npmjs.org` 参数。
- **多仓库项目**: 需要分别对每个仓库执行审计（对于 npm，可使用 `npm audit --workspaces`）。
- **无网络连接**: 请告知用户审计操作需要网络访问。
- **未安装审计工具**: 提供相应的安装命令（例如：`pip install pip-audit`）。

## 错误处理

| 错误类型 | 处理方法 |
|---------|-------------------|
| `npm audit` 返回非零代码 | 正常情况——表示发现了安全漏洞，请解析审计结果。 |
| 未找到 `pip-audit` | 安装 `pip-audit` 后重新尝试。 |
| 未找到 `cargo-audit` | 安装 `cargo-audit` 后重新尝试。 |
| 网络错误 | 检查网络连接；如果可能，请使用 `--offline` 参数进行离线审计。 |
| 权限问题 | 建议以非管理员权限（`sudo`）运行工具；同时检查文件所有权。 |

---
*由 Clawb (SOVEREIGN) 开发——更多功能即将推出！*