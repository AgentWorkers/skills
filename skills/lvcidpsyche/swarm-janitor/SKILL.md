---
name: swarm-janitor
description: 企业级 OpenClaw 工具：用于清理无主（即被遗忘或不再使用的）子代理进程、将转录文件归档到 SuperMemory 存储系统中，并在不会丢失任何数据的情况下释放磁盘空间。该工具具备试运行模式、可配置的保留策略以及全面的安全检查功能。
homepage: https://github.com/openclawdad/swarm-janitor
author: OpenClawdad (Redclay)
tags: [maintenance, cleanup, subagents, memory-management, enterprise]
metadata:
  clawdbot:
    emoji: 🧹
    requires:
      bins: [python3]
    install: []
---

# Swarm Janitor

这是一个企业级工具，用于管理 OpenClaw 的子代理（subagents）。

## 功能概述

该工具能够自动识别并清理那些被遗弃的子代理会话，同时通过 SuperMemory 系统将重要数据存档起来。

### 核心功能

- **扫描（Scan）**：分析会话目录，找出被遗弃或被放弃的子代理。
- **存档（Archive）**：在删除前将相关数据保存到 SuperMemory。
- **清理（Clean）**：安全地移除这些被遗弃的会话文件，释放磁盘空间。
- **报告（Report）**：生成详细的清理报告。

## 安全性

该工具采用了多重安全机制：

- ✅ **绝不删除正在运行的会话**：会检查相关进程的状态。
- ✅ **试运行模式（Dry-run mode）**：执行前会预览更改内容。
- ✅ **SuperMemory 备份**：删除前会先将数据存档到 SuperMemory。
- ✅ **可配置的保留策略**：允许用户自定义数据保留的时长。
- ✅ **详细日志记录**：所有操作都有完整的审计记录。

## 快速入门

```bash
# Preview what would be cleaned (dry-run)
python3 scripts/swarm_janitor.py --dry-run

# Archive old sessions to SuperMemory, then clean
python3 scripts/swarm_janitor.py --archive --clean

# Custom retention (7 days instead of default 3)
python3 scripts/swarm_janitor.py --retention-days 7 --clean
```

## 安装步骤

1. 将该工具复制到您的 OpenClaw 工作目录中：
   ```bash
   cp -r skills/swarm-janitor ~/.openclaw/workspace/skills/
   ```

2. 配置数据保留策略（可选）：
   ```bash
   # Edit config to customize
   nano references/config.yaml
   ```

3. 运行首次扫描：
   ```bash
   python3 ~/.openclaw/workspace/skills/swarm-janitor/scripts/swarm_janitor.py --dry-run
   ```

## 使用方式

### 日常维护（通过 Cron 任务）

```cron
# Run daily at 3 AM, archive sessions older than 3 days
0 3 * * * python3 ~/.openclaw/workspace/skills/swarm-janitor/scripts/swarm_janitor.py --archive --clean --retention-days 3 >> /var/log/swarm-janitor.log 2>&1
```

### 手动清理

```bash
# See what would be deleted
python3 scripts/swarm_janitor.py --dry-run --verbose

# Archive transcripts to SuperMemory
python3 scripts/swarm_janitor.py --archive

# Clean without archiving (not recommended)
python3 scripts/swarm_janitor.py --clean --no-archive

# Full report
python3 scripts/swarm_janitor.py --report --output json
```

### 紧急清理

```bash
# Aggressive cleanup with 1-day retention
python3 scripts/swarm_janitor.py --clean --retention-days 1 --force
```

## 配置设置

请参阅 [references/config.yaml] 文件，以配置以下内容：

- 数据保留策略
- 存档目的地
- 安全阈值
- 日志记录选项

## 工作原理

1. **发现（Discovery）**：扫描 `~/.openclaw/agents/main/sessions/` 目录。
2. **分析（Analysis）**：判断会话的创建时间、活动状态及文件大小。
3. **分类（Classification）**：区分被遗弃的会话和仍在运行的会话。
4. **存档（Archival）**：如果启用了 SuperMemory，会将相关数据保存到其中。
5. **清理（Clean）**：安全地移除被遗弃的会话文件。
6. **报告（Report）**：生成操作摘要。

## 安全机制

| 检查项 | 描述 |
|-------|-------------|
| 进程检查（Process Check） | 确认没有正在运行的进程占用这些会话。 |
| 年龄验证（Age Verification） | 仅删除超过设定时间的会话。 |
| 文件大小限制（Size Limits） | 对异常大的文件大小进行警告。 |
| 默认为试运行模式（Dry-Run by Default） | 执行前会显示预览结果。 |
| 先进行备份（Backup First） | 删除前会先将数据存档到 SuperMemory。 |

## 常见问题解答

**Q：出现 “权限被拒绝” 的错误**：请确保您具有对会话目录的写入权限。  
**Q：某些会话未被检测到**：请检查 `config.yaml` 文件中的路径是否与您的 OpenClaw 安装路径匹配。  
**Q：SuperMemory 存档失败**：请确认 SuperMemory 工具已配置有效的 API 密钥。  

## 企业级特性

- **审计日志（Audit Logging）**：所有操作都会附带时间戳记录。
- **可配置的策略（Configurable Policies）**：支持基于 YAML 的配置。
- **指标导出（Metrics Export）**：支持 JSON/CSV 格式的数据导出，便于监控。
- **试运行模式（Dry-Run Mode）**：允许在正式应用更改前进行测试。
- **保留策略（Retention Policies）**：支持基于时间或数量的删除规则。

## 许可证

MIT 许可证。该工具由 OpenClawdad（Redclay）为 OpenClaw 社区开发。