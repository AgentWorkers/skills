---
name: openclaw-doctor-pro
description: OpenClaw 的全面诊断、错误修复及技能推荐工具
license: MIT
version: 1.0.0
homepage: https://github.com/PhenixStar/openclaw-doctor-pro
user-invocable: true
disable-model-invocation: false
metadata:
  {
    "openclaw": {
      "emoji": "🏥",
      "requires": {
        "bins": ["python3"],
        "env": []
      },
      "install": [
        {
          "id": "pip-deps",
          "kind": "shell",
          "command": "pip install click rich requests beautifulsoup4",
          "label": "Install Python dependencies"
        }
      ]
    }
  }
---

# OpenClaw Doctor Pro

OpenClaw Doctor Pro 是一款功能强大的诊断工具，专门用于修复 OpenClaw 中出现的错误，并为用户推荐合适的技能（ClawHub 技能）。

## 使用场景

当用户需要执行以下操作时，可以激活 OpenClaw Doctor Pro：
- 诊断 OpenClaw 的错误或问题
- 自动修复常见故障
- 查找并推荐适合的 ClawHub 技能
- 进行全面的系统健康检查
- 首次配置 OpenClaw
- 更新文档和缓存数据

## 提供的工具

### 错误修复工具
用于诊断并自动修复 OpenClaw 中出现的错误。
```bash
# Diagnose by error code
python3 {baseDir}/scripts/error-fixer.py --error 401

# Analyze log file
python3 {baseDir}/scripts/error-fixer.py --input /path/to/log

# Auto-fix safe issues
python3 {baseDir}/scripts/error-fixer.py --error EADDRINUSE --auto-fix

# List errors by category
python3 {baseDir}/scripts/error-fixer.py --category authentication
```

### 技能推荐工具
能够智能地为用户推荐合适的 ClawHub 技能。
```bash
# Recommend for channel
python3 {baseDir}/scripts/skill-recommender.py --channel whatsapp --top 5

# Recommend by use case
python3 {baseDir}/scripts/skill-recommender.py --use-case "image generation"

# Auto-detect from config
python3 {baseDir}/scripts/skill-recommender.py --auto-detect

# Check for updates
python3 {baseDir}/scripts/skill-recommender.py --check-updates
```

### 高级诊断工具
提供更全面的系统诊断功能。
```bash
# Full diagnostics
python3 {baseDir}/scripts/enhanced-doctor.py

# Deep scan with log analysis
python3 {baseDir}/scripts/enhanced-doctor.py --deep

# JSON output
python3 {baseDir}/scripts/enhanced-doctor.py --json
```

### 自动更新工具
确保所有参考信息和缓存数据始终保持最新状态。
```bash
# Check what's outdated
python3 {baseDir}/scripts/self-updater.py --check

# Update everything
python3 {baseDir}/scripts/self-updater.py --update

# Update only skill cache
python3 {baseDir}/scripts/self-updater.py --update --skills-only
```

### 配置向导
为首次使用 OpenClaw 的用户提供交互式的配置流程。
```bash
# Interactive setup
python3 {baseDir}/scripts/setup-wizard.py

# Check prerequisites only
python3 {baseDir}/scripts/setup-wizard.py --check-only
```

## 参考文件
- [错误目录](references/error-catalog.md) - 详细的错误索引
- [自动修复功能](references/auto-fix-capabilities.md) - 自动修复与手动修复的对比
- [诊断命令](references/diagnostic-commands.md) - 命令行界面快速参考
- [故障排除流程](references/troubleshooting-workflow.md) - 故障排查步骤指南
- [认证错误](references/authentication-errors.md) - 与认证相关的错误处理
- [速率限制错误](references/rate-limiting-errors.md) - 流量限制相关问题
- [网关错误](references/gateway-errors.md) - 网络连接问题
- [通道错误](references/channel-errors.md) - 与特定通道相关的错误
- [沙箱错误](references/sandbox-errors.md) - Docker 运行环境中的问题
- [配置错误](references/configuration-errors.md) - 配置设置问题
- [安装错误](references/installation-errors.md) - 安装过程中的问题
- [ClawHub 集成](references/clawhub-integration.md) - 技能管理相关内容

## 模板文件
- [错误报告](templates/error-report.md) - 用于记录诊断结果的格式化文档
- [推荐报告](templates/recommendation-report.md) - 包含技能推荐内容的格式化文档