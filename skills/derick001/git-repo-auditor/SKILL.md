---
name: git-repo-auditor
description: 审计 Git 仓库，检查是否存在安全问题、大文件、敏感数据以及仓库的健康状况指标。
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - git
        - python3
---
# Git 仓库审计工具

## 功能概述

这是一个命令行工具（CLI），用于审计 Git 仓库中的安全问题、代码质量缺陷以及仓库的健康状况。该工具会扫描仓库中的敏感数据、大文件以及常见的安全风险。

**主要功能：**
- **敏感数据检测**：使用正则表达式扫描 Git 历史记录中的 API 密钥、密码、令牌等敏感信息。
- **大文件检测**：识别仓库历史记录中可能影响性能的大文件（大于 10MB）。
- **安全风险检测**：检测硬编码的凭据、不安全的配置文件以及危险的权限设置。
- **仓库健康检查**：检查合并冲突、过时的分支等仓库维护问题。
- **合规性报告**：生成安全合规性报告，以供审计或团队审查使用。
- **多种输出格式**：提供人类可读的文本格式、JSON 格式和 CSV 格式，以便与其他工具集成。
- **自定义扫描**：允许用户配置自定义的正则表达式和文件扩展名进行扫描。
- **历史数据分析**：可以扫描整个 Git 历史记录或特定时间范围。
- **修复建议**：针对发现的安全问题提供相应的修复建议。

## 使用场景

- 需要对 Git 仓库进行安全合规性审计。
- 希望检测到意外提交的敏感数据。
- 准备将仓库开源发布。
- 需要识别可能影响性能的大文件。
- 新员工入职时，需要确保仓库的维护质量。
- 需要生成安全审计报告以满足合规性要求。
- 希望在持续集成/持续部署（CI/CD）流程中自动化安全扫描。
- 清理旧仓库时，需要识别其中存在的问题。

## 使用方法

基本命令如下：

```bash
# Scan current directory repository
python3 scripts/main.py scan .

# Scan specific repository path
python3 scripts/main.py scan /path/to/repo

# Scan with custom secrets patterns file
python3 scripts/main.py scan . --patterns custom-patterns.json

# Generate JSON report for automation
python3 scripts/main.py scan . --json

# Check only for large files (>50MB)
python3 scripts/main.py scan . --check large-files --threshold 50

# Scan specific branch or commit range
python3 scripts/main.py scan . --branch main --since "2024-01-01"

# Generate remediation report with suggested fixes
python3 scripts/main.py scan . --remediation

# List all branches with last commit age
python3 scripts/main.py branches .
```

## 示例

### 示例 1：基本安全扫描

```bash
python3 scripts/main.py scan ~/projects/my-app
```

**输出结果：**
```
🔍 Scanning repository: /home/user/projects/my-app
📊 Repository info: 247 commits, 5 branches, 3 contributors

🔐 SECURITY ISSUES FOUND (3):
⚠️  High: AWS_ACCESS_KEY_ID found in commit abc123 (2024-02-15)
    File: config/old-config.env
    Pattern: AWS_ACCESS_KEY_ID=AKIA.*
    Remediation: Rotate key immediately, remove from history with BFG

⚠️  Medium: Hardcoded database password in commit def456 (2024-01-20)
    File: src/database.js
    Pattern: password: "secret123"
    Remediation: Move to environment variables, use secret manager

⚠️  Low: Private key file extension in commit ghi789 (2023-12-05)
    File: backup/id_rsa.old
    Pattern: Private key file (.pem, .key, .ppk, id_rsa)
    Remediation: Remove file from repository history

💾 LARGE FILES FOUND (2):
📦 42MB: assets/video/demo.mp4 (commit xyz123)
📦 18MB: database/backup.sql (commit uvw456)

✅ Repository health: Good
⏰ Stale branches: 2 branches older than 90 days
```

### 示例 2：JSON 格式输出（用于 CI/CD 集成）

```bash
python3 scripts/main.py scan . --json > security-report.json
```

**输出示例（部分内容）：**
```json
{
  "repository": "/home/user/projects/my-app",
  "scan_date": "2024-03-06T10:30:00Z",
  "security_issues": [
    {
      "severity": "high",
      "type": "aws_access_key",
      "commit": "abc123",
      "date": "2024-02-15",
      "file": "config/old-config.env",
      "pattern": "AWS_ACCESS_KEY_ID=AKIA.*",
      "remediation": "Rotate key immediately, remove from history with BFG"
    }
  ],
  "large_files": [
    {
      "size_mb": 42,
      "path": "assets/video/demo.mp4",
      "commit": "xyz123"
    }
  ],
  "summary": {
    "total_issues": 3,
    "by_severity": {"high": 1, "medium": 1, "low": 1},
    "large_files_count": 2,
    "total_size_mb": 60
  }
}
```

### 示例 3：检查仓库健康状况

```bash
python3 scripts/main.py health .
```

**输出结果：**
```
📈 Repository Health Report: /home/user/projects/my-app

📊 Basic Metrics:
- Commits: 1,247
- Branches: 12 (3 active, 9 stale)
- Contributors: 8
- First commit: 2022-05-15
- Last commit: 2024-03-06

⚠️  Health Issues:
- Stale branches: 9 branches with no commits in >90 days
- Large files: 2 files >10MB in history
- Binary files: 45 binary files (consider Git LFS)
- Merge conflicts: 3 unresolved merge markers in code

✅ Good Practices:
- .gitignore present and comprehensive
- No secrets detected in recent commits
- Regular commit activity (avg 15 commits/week)
- Meaningful commit messages (87% good)

💡 Recommendations:
1. Clean up stale branches: git branch -d branch1 branch2...
2. Consider Git LFS for binary files
3. Resolve merge conflicts in: src/app.js, config/settings.yaml
```

### 示例 4：仅检测大文件

```bash
python3 scripts/main.py scan . --check large-files --threshold 20
```

**输出结果：**
```
💾 Large Files (>20MB) in Repository History:

1. assets/videos/presentation.mp4
   - Size: 42MB
   - Commit: xyz123 (2024-01-15)
   - Author: Jane Doe
   - Message: "Add presentation video"

2. database/backup/archive.sql.gz
   - Size: 38MB
   - Commit: uvw456 (2023-12-20)
   - Author: John Smith
   - Message: "Database backup"

Total: 2 files, 80MB
Recommendation: Consider using Git LFS for files >20MB
```

## 系统要求

- 确保已安装 Git 2.20 或更高版本，并且 Git 可以通过 `PATH` 变量找到。
- 需要 Python 3.x。
- 该工具不依赖外部 Python 库，仅使用标准库。

## 注意事项

- 扫描具有大量历史记录的仓库时，扫描速度可能会较慢。
- 敏感数据检测依赖于正则表达式，可能存在误报或漏报的情况。
- 该工具不会自动从历史记录中删除敏感数据，需要手动处理。
- 仅支持 Git 仓库，不支持其他版本控制系统（VCS）。
- 不支持扫描加密仓库。
- 大文件检测会扫描整个历史记录，可能会遗漏被忽略目录中的文件。
- 该工具不支持与外部密钥管理工具（如 Vault、AWS Secrets Manager）集成。
- 不提供实时监控功能，仅扫描历史提交记录。
- 仅支持文本文件的扫描，无法检测二进制文件中的敏感信息。
- 可能无法检测所有类型的敏感数据，可能需要自定义正则表达式。
- 扫描性能受仓库大小和历史记录长度的影响。
- 不支持自动扫描 Git 子模块。
- 不支持与外部密钥管理系统集成。
- 仅支持文本文件的扫描，无法检测二进制文件中的敏感信息。
- 不支持自定义 Git 钩子或预提交脚本的集成。
- 对于包含大量提交的仓库，扫描性能可能会受到影响。
- 不支持跨多个仓库的分布式扫描。
- 对于损坏的 Git 仓库，错误处理能力有限。
- 不支持扫描 Git 工作树或浅层克隆。
- 需要先克隆远程仓库才能进行扫描。
- 不提供新问题发现的自动通知功能。

## 目录结构

该工具可以直接在任何本地 Git 仓库上使用，无需特殊配置目录。用户可以提供自定义的正则表达式文件用于敏感数据检测。

## 错误处理

- 如果提供的仓库路径无效，会显示有用的错误信息及相应的解决方法。
- 如果 Git 命令执行失败，会显示错误原因及排查建议。
- 如果遇到权限问题，会提示检查仓库的访问权限。
- 如果正则表达式解析失败，会显示出错行号及问题所在。
- 如果内存不足，建议缩小扫描范围或调整扫描设置。

## 贡献方式

该工具由 Skill Factory 开发。如有问题或改进建议，请通过 OpenClaw 项目进行反馈。