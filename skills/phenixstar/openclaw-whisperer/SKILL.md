---
name: openclaw-whisperer
description: OpenClaw的全面诊断、错误修复及技能推荐工具
license: MIT
version: 1.2.0
homepage: https://github.com/PhenixStar/openclaw-skills-collection
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "🏥"
    requires:
      bins:
        - python3
      env: []
    install:
      - id: pip-deps
        kind: shell
        command: "pip install click rich requests beautifulsoup4"
        label: Install Python dependencies
---

# OpenClaw Whisperer

这是一个专为 OpenClaw 设计的终极诊断、错误修复及技能推荐工具。

## v1.1.0 的新功能

- **互补技能**：发现能够协同工作的技能（包含 10 种技能之间的关联关系）
- **诊断钩子**：支持与 GitHub、Slack 和 Discord 的集成，用于发送错误通知（提供 9 种钩子配置选项）
- **修复跟踪**：记录修复操作的历史记录及成功率
- **智能评分**：通过补充技能的评分机制来优化技能推荐结果
- **丰富的显示界面**：改进了命令行界面（CLI）的显示效果及建议内容的格式

## 使用场景

当用户需要以下操作时，可激活该工具：
- 诊断 OpenClaw 的错误或问题
- 自动修复常见问题
- 查找并推荐具有互补功能的 ClawHub 技能
- 进行全面的系统健康检查
- 首次设置 OpenClaw
- 更新文档和缓存数据
- 跟踪修复操作的执行历史

## 提供的工具

### 错误修复工具
利用诊断钩子和修复跟踪功能来诊断并自动修复 OpenClaw 的错误。
```bash
# Diagnose by error code (triggers diagnostic hooks if configured)
python3 {baseDir}/scripts/error-fixer.py --error 401

# Analyze log file with recovery suggestions
python3 {baseDir}/scripts/error-fixer.py --input /path/to/log

# Auto-fix safe issues (tracks execution history)
python3 {baseDir}/scripts/error-fixer.py --error EADDRINUSE --auto-fix

# List errors by category with fix history
python3 {baseDir}/scripts/error-fixer.py --category authentication

# View fix execution history
python3 {baseDir}/scripts/error-fixer.py --show-history

# Test notification hooks (GitHub/Slack/Discord)
python3 {baseDir}/scripts/error-fixer.py --test-hooks
```

### 技能推荐工具
基于对互补技能的检测，提供智能的 ClawHub 技能推荐建议。
```bash
# Recommend for channel (includes complementary skills)
python3 {baseDir}/scripts/skill-recommender.py --channel whatsapp --top 5

# Recommend by use case with bonus scoring
python3 {baseDir}/scripts/skill-recommender.py --use-case "image generation"

# Auto-detect from config (enriched with complementary metadata)
python3 {baseDir}/scripts/skill-recommender.py --auto-detect

# Check for updates
python3 {baseDir}/scripts/skill-recommender.py --check-updates

# View complementary skills for installed skill
python3 {baseDir}/scripts/skill-recommender.py --complementary-for image-generator-pro
```

### 扩展诊断工具
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
确保参考信息和缓存数据的最新性。
```bash
# Check what's outdated
python3 {baseDir}/scripts/self-updater.py --check

# Update everything
python3 {baseDir}/scripts/self-updater.py --update

# Update only skill cache
python3 {baseDir}/scripts/self-updater.py --update --skills-only
```

### 设置向导
为首次使用的用户提供交互式的设置流程。
```bash
# Interactive setup
python3 {baseDir}/scripts/setup-wizard.py

# Check prerequisites only
python3 {baseDir}/scripts/setup-wizard.py --check-only
```

## 参考文件

- [错误目录](references/error-catalog.md)：详细的错误信息索引
- [自动修复功能](references/auto-fix-capabilities.md)：自动修复与手动修复的对比
- [诊断命令](references/diagnostic-commands.md)：命令行接口的使用指南
- [故障排除流程](references/troubleshooting-workflow.md)：问题解决流程
- [认证错误](references/authentication-errors.md)：与认证相关的错误信息
- [速率限制错误](references/rate-limiting-errors.md)：流量限制相关的问题
- [网关错误](references/gateway-errors.md)：网络连接问题
- [频道错误](references/channel-errors.md)：特定频道相关的问题
- [沙箱错误](references/sandbox-errors.md)：Docker 使用过程中的问题
- [配置错误](references/configuration-errors.md)：配置相关的问题
- [安装错误](references/installation-errors.md)：安装过程中的问题
- [ClawHub 集成](references/clawhub-integration.md)：ClawHub 技能管理相关的内容

## 数据文件（v1.1.0）

- [complementary-skills.json]：记录 10 种技能之间的关联关系
- [integration-hooks.json]：包含 9 种错误通知钩子的配置信息
- [fix-execution-history.json]：用于记录修复操作的元数据

## 模板文件

- [错误报告](templates/error-report.md)：诊断结果的输出格式
- [推荐报告](templates/recommendation-report.md)：技能推荐建议的格式