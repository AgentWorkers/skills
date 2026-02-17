---
name: exec-error-doctor
description: 诊断并解决跨工具的执行相关命令故障（包括 OpenClaw 的执行输出、Shell 错误、GitHub CLI 错误、ClawHub CLI 错误、缺失的二进制文件、身份验证失败、JSON 字段不匹配、权限错误、超时以及平台状态的临时变化）。当命令返回非零值、发送 SIGKILL 信号、遇到 ENOENT 错误、未知的 JSON 字段或其他类似的执行故障时，使用该功能以快速进行故障排查并确定具体的修复措施。
---
# 执行错误诊断工具（Exec Error Doctor）

该工具用于快速排查执行失败的问题，确定根本原因，并采取针对性的修复措施，而非简单地重复尝试。

## 快速工作流程：

1. 对原始错误日志进行分类处理：
   - `scripts/exec_error_triage.sh <error_text_or_file>`
2. 根据 `references/error-taxonomy.md` 中的分类信息应用相应的修复方案。
3. 在必要时使用更安全的工具或脚本重新执行相关操作：
   - 检查 GitHub 存储库的架构变更：`scripts/gh_search_repos_safe.sh`
   - 确保 ClawHub 的发布操作正常进行：`scripts/clawhub_publish_safe.sh`
4. 通过再次执行任务来确认问题是否已解决，并记录结果。

## 标准命令：

### 通用错误分类工具：
```bash
bash scripts/exec_error_triage.sh "Unknown JSON field: nameWithOwner"
```

### 安全的 GitHub 存储库搜索工具（支持架构变更检测）：
```bash
bash scripts/gh_search_repos_safe.sh "safe-exec skill" 15
```

### 安全的 ClawHub 发布工具（支持重试机制）：
```bash
bash scripts/clawhub_publish_safe.sh ./my-skill my-skill "My Skill" 1.0.0 "Initial release"
```

## 规则：

- 在进行修复之前，优先对错误进行分类。
- 如果发布操作已经成功完成，但仍然出现“Skill not found”的错误，应将其视为暂时性问题。
- 对于 `gh search repos --json` 命令，建议使用 `fullName` 而不是 `nameWithOwner` 作为搜索参数。
- 区分暂时性错误（可通过重试解决）和严重错误（如认证问题、权限问题或参数错误）。

## 资源：

- `references/error-taxonomy.md`：错误类别与修复方案的映射关系。
- `scripts/exec_error_triage.sh`：基于模式的错误分类脚本。
- `scripts/gh_search_repos_safe.sh`：用于执行安全 GitHub 存储库搜索的脚本。
- `scripts/clawhub_publish_safe.sh`：用于执行安全 ClawHub 发布操作的脚本，并支持重试机制。