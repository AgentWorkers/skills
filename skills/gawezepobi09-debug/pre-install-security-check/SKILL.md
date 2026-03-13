---
name: security-check
description: 🔒 对外部代码和依赖项进行预安装安全验证。自动分析 GitHub 仓库、npm 包、PyPI 库以及 shell 脚本中的风险。集成 CVE 数据库（如 Snyk、Safety DB），在安装前检测潜在的安全漏洞。会显示风险等级（✅ 安全 / ⚠️ 需审查 / ❌ 危险），并提供相应的处理建议。这是 OpenClaw 首个全面的安全功能——在下载未经验证的代码之前保护您的系统。
tags: security, dependencies, vulnerability, safety, audit, npm, pypi, github, cve, snyk, supply-chain, pre-install
license: MIT
---
# 安全检查

在安装外部代码和依赖项之前进行安全验证。

## 核心原则

**下载前务必进行验证。** 外部代码（GitHub 仓库、npm 包、PyPI 库、脚本）可能包含恶意代码、漏洞或供应链攻击风险。此功能会在执行潜在危险的命令之前自动进行安全检查。

## 适用场景

在以下操作之前自动触发安全检查：
- `git clone <url>` — 下载 GitHub/GitLab 仓库
- `pip install <package>` — 安装 Python 包
- `npm install <package>` — 安装 Node.js 包
- `curl <url> | bash` — 运行 Shell 脚本
- 下载任何需要执行的外部代码

## 工作原理

### 1. 识别代码类型

确定要安装的代码类型：
- GitHub URL → 检查 GitHub 仓库
- PyPI 包名 → 检查 PyPI 包
- npm 包名 → 检查 npm 包
- 直接 URL → 检查脚本或文件

### 2. 收集安全指标

根据代码类型收集以下信息：
**对于 GitHub 仓库：**
- 星星数量（stars）、分支数量（forks）、关注者数量（watchers）
- 最后一次提交日期
- 开启的 issue（尤其是带有 `security` 标签的 issue）
- 贡献者数量
- 许可证类型
- 是否有代码规范（Code of Conduct）

**对于 PyPI 包：**
- 每月的下载量
- 发布频率
- 维护者信息
- 已知的 CVE（通过 Safety DB 查询）
- 依赖项数量

**对于 npm 包：**
- 每周下载量
- 依赖项数量（依赖项越少越好）
- 源代码链接
- 许可证类型
- 已知的漏洞（通过 Snyk 查询）

### 3. 计算风险评分

使用基于阈值的评分方法（灵感来自 Skantek）：

```
Risk Score = 0

# Positive signals (reduce risk):
- High stars/downloads: -10
- Recent activity (< 30 days): -5
- Well-known maintainer: -5
- Clear license: -3
- Few dependencies: -5

# Negative signals (increase risk):
- No activity (> 1 year): +15
- No license: +10
- Many dependencies: +5 per 10 deps
- Known CVEs: +20 per CVE
- Suspicious patterns: +25
```

**风险等级：**
- `Score < 0` → ✅ **安全**（可自动继续）
- `0 <= Score < 15` → ⚠️ **需要审核**（显示摘要并请求确认）
- `Score >= 15` → ❌ **危险**（强烈警告，需要手动批准）

### 4. 显示摘要

展示检查结果：

```
🔒 Security Check: <package/repo>

Risk Level: ⚠️ REVIEW

Metrics:
  ✅ Stars: 15.2k | Forks: 3.1k
  ⚠️  Last commit: 8 months ago
  ✅ License: MIT
  ⚠️  Open security issues: 2
  ✅ Dependencies: 5

Known Issues:
  - CVE-2024-12345 (Medium severity, patched in v1.2.3)

Recommendation: Update to v1.2.3+ before installing.

Proceed? [Y/n]
```

### 5. 请求确认

根据风险等级：
- ✅ 安全 → 通知用户，自动继续（除非用户明确要求审核）
- ⚠️ 需要审核 → 显示摘要并请求确认
- ❌ 危险 → 强烈警告，需要明确批准

## 实现模式

```python
# Before: git clone https://github.com/user/repo
# After:
1. Detect: GitHub repo
2. Fetch metrics via GitHub API
3. Calculate risk score
4. Show summary
5. Ask confirmation if needed
6. Proceed or abort
```

## 集成方式

### GitHub API
```bash
curl -s "https://api.github.com/repos/{owner}/{repo}"
```

返回：星星数量（stars）、分支数量（forks）、更新时间（updated_at）、开启的 issue 数量（open_issues_count）、许可证类型（license）

### PyPI JSON API
```bash
curl -s "https://pypi.org/pypi/{package}/json"
```

返回：每月下载量（downloads）、发布次数（releases）、维护者信息（maintainers）

### npm 注册表
```bash
curl -s "https://registry.npmjs.org/{package}"
```

返回：下载量（通过 npm-stat 获取）、依赖项数量（dependencies）、许可证类型（license）

### 漏洞数据库
- **Snyk**（npm）：https://security.snyk.io
- **Safety DB**（Python）：https://github.com/pyupio/safety-db
- **GitHub Advisory**：https://github.com/advisories

## 来自研究的最佳实践

参考 Adyen 的 Skantek 和 GitHub 的 Dependabot 的建议：
1. **减少依赖项数量** — 每个依赖项都会增加风险
2. **定期重新扫描** — 需要监控零日漏洞
3. **使用私有注册表**（可选）—— 仅用于已批准的包
4. **基于阈值的评分** — 不是简单地判断代码是否安全，而是评估风险等级
5. **兼容性检查** — 确保更新不会破坏持续集成（CI）测试

## 安全措施
- **未经用户同意，切勿绕过安全检查** — 必须始终通知用户安全检查结果
- **高风险包不得自动安装** — 需要手动批准
- **记录所有决策** — 记录安装的内容及原因
- **限制 API 调用频率** — GitHub、npm、PyPI 都有限制 API 调用的频率

## 示例工作流程

### 示例 1：安全的包
```
User: pip install requests

Security Check:
✅ SAFE: requests (PyPI)
  - Downloads: 50M/month
  - Last release: 2 weeks ago
  - License: Apache 2.0
  - Dependencies: 5
  - Known CVEs: 0

Proceeding with installation...
```

### 示例 2：存在风险的仓库
```
User: git clone https://github.com/suspicious/tool

Security Check:
❌ DANGEROUS: suspicious/tool
  - Stars: 12
  - Last commit: 3 years ago
  - Open issues: 45 (3 security labels)
  - No license
  - Risk score: 35

⚠️  This repository shows multiple red flags.
   Consider alternatives or manual code review.

Proceed anyway? [y/N]
```

### 示例 3：需要更新
```
User: npm install left-pad

Security Check:
⚠️  REVIEW: left-pad@1.0.0
  - Downloads: 2M/week
  - CVE-2024-xxxxx: Prototype pollution (High)
  - Fixed in: v1.0.1

Recommendation: Install v1.0.1 instead.

Use latest version? [Y/n]
```

## 未来改进方向

随着功能的完善：
1. **本地缓存** — 将风险评分缓存 24 小时，以减少 API 调用次数
2. **模式检测** — 检查代码中是否存在可疑模式（如评估语句、执行语句、Shell 命令）
3. **集成到持续集成/持续部署（CI/CD）流程** — 阻止安装含有漏洞的依赖项
4. **自定义规则** — 允许用户定义风险阈值和黑名单
5. **生成安全审计日志**

## 参考资料

有关详细实现指南，请参阅：
- `references/skantek-approach.md` — Adyen 的实现方法
- `references/vulnerability-databases.md` — 如何查询漏洞数据库