---
name: brew-audit
version: 1.0.0
description: 审计 Homebrew 安装情况：检查是否存在过时的软件包，以及是否有进行清理或系统维护的必要。此功能适用于在 macOS 上需要了解 Homebrew 更新情况、系统维护状态或软件包健康状况时使用。
metadata: {"clawdbot":{"emoji":"🍺","homepage":"https://brew.sh","requires":{"bins":["brew"],"os":["darwin"]}}}
---
# Homebrew 审计工具

快速审计您的 Homebrew 安装环境，检查是否存在过时的软件包、需要清理的旧版本以及系统健康问题。

## 使用方法

```bash
# Full audit (outdated + cleanup + doctor + summary)
bash scripts/brew-audit.sh

# Specific sections
bash scripts/brew-audit.sh --section outdated
bash scripts/brew-audit.sh --section cleanup
bash scripts/brew-audit.sh --section doctor

# JSON output (outdated only)
bash scripts/brew-audit.sh --json --section outdated
```

## 审计内容

### 📦 过时的软件包
列出所有可更新为新版本的软件包（formulae 和 casks），并显示当前版本与可用版本的信息。

### 🧹 清理旧版本
显示可以删除的旧版本数量以及预计节省的磁盘空间。运行 `brew cleanup` 命令即可完成清理。

### 🩺 系统健康检查
运行 `brew doctor` 命令，检测以下问题：
- 没有源代码的软件包（“孤儿包”）
- 已被弃用或禁用的软件包（需要替换）
- 权限问题、损坏的符号链接或配置错误

### 📊 统计结果
显示软件包的总数、分类以及 Homebrew 的使用情况。

## 使用场景
- 定期系统维护（每周/每月）
- 在进行重大系统升级之前
- 当磁盘空间不足时
- 在发现构建失败后（通过 `brew doctor` 检查）

## 更新软件包
审计完成后，您可以执行以下操作来更新软件包：
```bash
brew upgrade              # upgrade all outdated
brew upgrade <formula>    # upgrade specific package
brew cleanup              # remove old versions
```