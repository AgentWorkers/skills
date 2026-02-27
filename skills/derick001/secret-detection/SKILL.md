---
name: secret-detection
description: 在提交之前使用 Git 钩子来检测敏感信息（如密码、API 密钥等）。
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      env: []
      bins: ["git", "python3"]
---
# 秘密检测

## 功能介绍

该工具提供了一个 Git 提交前钩子（pre-commit hook），用于扫描暂存区（staged area）中的文件，以检测常见的秘密信息（如 API 密钥、密码、令牌等）。如果检测到这些信息，该钩子会阻止提交操作，从而防止秘密信息意外泄露到公共仓库中。

**输入：**  
Git 暂存区的文件（由钩子自动扫描）或手动提供的文件路径。  
**输出：**  
包含行号的检测报告；如果检测到秘密信息，脚本会返回非零的退出码。

## 使用场景

- 当您处理的仓库可能包含敏感的凭据时。  
- 当您希望防止秘密信息被意外提交时。  
- 当您需要一个轻量级的、用于 Git 工作流的本地秘密检测工具时。  
- 当您希望在将代码推送到远程仓库之前执行安全检查时。

## 使用方法

### 安装  
```bash
# Install the hook in your git repository
./scripts/main.py install
```

### 手动扫描  
```bash
# Scan specific files
./scripts/main.py scan --file path/to/file

# Scan all staged files (like the hook does)
./scripts/main.py scan --staged
```

### 钩子行为  
- 该钩子在执行 `git commit` 操作时自动运行。  
- 如果检测到秘密信息，提交操作将被阻止。  
- 脚本会显示检测到的秘密信息（包括文件名和行号）。  
- 退出码 0 表示未发现秘密信息；退出码 1 表示发现了秘密信息。

## 示例

### 示例 1：安装钩子  
```bash
$ ./scripts/main.py install
✓ Pre-commit hook installed at .git/hooks/pre-commit
✓ Hook will scan for secrets on every commit
```

### 示例 2：检测到秘密信息并阻止提交  
```bash
$ git commit -m "Add config"
⚠️  Secret detected in config.yaml line 12: AWS_ACCESS_KEY_ID=AKIA...
⚠️  Secret detected in .env line 3: PASSWORD=secret123
✗ Commit blocked: 2 secrets found
```

### 示例 3：手动扫描  
```bash
$ ./scripts/main.py scan --staged
Scanning 3 staged files...
✓ config.yaml: clean
✓ .env: clean  
✓ src/main.py: clean
✓ No secrets found
```

## 系统要求  
- Git（用于安装钩子）。  
- Python 3.6 及以上版本（用于执行秘密检测）。  
- 不需要使用任何外部 API 密钥或服务。

## 限制事项  
- 仅能检测常见的秘密信息模式（如 AWS 密钥、GitHub 令牌、密码等）。  
- 可能会出现误报（例如，某些看似随机但实际并非秘密的字符串）。  
- 不会扫描二进制文件。  
- 需要为每个仓库单独安装该工具。  
- 该工具不能替代全面的秘密管理解决方案。  
- 为便于识别，脚本会仅输出检测到的秘密信息的前 20 个字符。