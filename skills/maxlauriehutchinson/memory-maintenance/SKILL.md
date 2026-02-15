---
name: memory-maintenance
version: 1.0.0
description: "OpenClaw代理的智能内存管理功能：会定期审查每日记录，建议更新MEMORY.md文件内容，维护目录的整洁性，并自动清理旧文件。特别推荐用于内存使用量持续增长的代理。"
homepage: https://github.com/MaxLaurieHutchinson/memory-maintenance
author: 
  name: "Max Hutchinson"
  email: "max.hutchinson258@gmail.com"
  url: "https://github.com/MaxLaurieHutchinson"
tags: ["memory", "maintenance", "automation", "agent-improvement", "workflow"]
metadata:
  openclaw:
    emoji: 🧹
    requires: 
      bins: ["gemini", "jq"]
      env: ["GEMINI_API_KEY"]
    install:
      - id: setup
        kind: script
        script: ./scripts/install.sh
        label: "Install memory maintenance"
---

# 内存维护技能

该技能为 OpenClaw 代理提供智能的内存管理功能：它会定期审查每日记录，建议对 `MEMORY.md` 文件进行更新，维护目录的整洁性，并自动清理旧文件。

## 功能概述

每次会话开始时，代理都会处于“初始状态”。如果不进行维护，将会出现以下问题：
- 每日的记录会不断堆积，难以查找；
- 重要的决策可能会被埋没在旧会话中的信息中；
- 界面窗口中会显示大量无关的历史数据；
- 用户每天都需要重复进行相同的上下文设置。

该技能自动化了这些繁琐的工作，帮助用户保持代理内存的整洁性和可用性。

## 主要功能

- **内容审查**：分析每日记录，并提出对 `MEMORY.md` 文件的更新建议；
- **目录维护**：监控内存/目录的命名问题、文件碎片化以及磁盘空间占用情况；
- **自动清理**：将超过 7 天的旧记录归档，并遵循 30 天的保留策略；
- **默认为“安全模式”**：任何内容变更都需要用户批准后才能自动应用。

## 推荐模型

该技能适用于轻量级模型。我们推荐以下模型：
- **主要模型**：`gemini-2.5-flash`（性能快速，成本效益高）；
- **备用模型**：`gemini-2.5-flash-lite`（在达到速率限制时使用）。

这两种模型都能高效地处理结构化数据的输出和分析任务。

## 快速入门

```bash
# Install the skill
clawhub install memory-maintenance

# Configure (optional)
# Edit config/settings.json to customize schedule, retention, etc.

# Run manually
openclaw skill memory-maintenance run

# Or let it run automatically via cron (configured during install)
```

## 架构

```
Daily Session Notes (memory/YYYY-MM-DD.md)
    ↓
Review Agent (scheduled daily)
    ↓
Structured Suggestions (JSON)
    ↓
Human Review (markdown report)
    ↓
Approved Updates → MEMORY.md
    ↓
Auto-Cleanup (archive old files)
```

## 工作流程

1. **每日审查**（默认在 23:00 进行）：
   - 扫描可配置的回顾周期（默认为 7 天）；
   - 检查内存/目录的状态；
   - 通过大型语言模型（LLM）生成更新建议；
   - 生成结构化的 JSON 数据和人类可读的 Markdown 报告。

2. **人工审核**：
   - 阅读 `agents/memory/review-v2-YYYY-MM-DD.md` 文件；
   - 审批或拒绝这些建议。

3. **应用更改**：
   ```bash
   # Dry run (preview)
   openclaw skill memory-maintenance apply --dry-run 2026-02-05
   
   # Apply safe changes (archiving, cleanup)
   openclaw skill memory-maintenance apply --safe 2026-02-05
   
   # Apply all (requires confirmation)
   openclaw skill memory-maintenance apply --all 2026-02-05
   ```

4. **自动清理**（在审核通过后执行）：
   - 将超过设定时间的记录归档；
   - 删除超过保留期限的归档文件；
   - 清理错误日志。

## 配置

请编辑 `config/settings.json` 文件以进行配置：

```json
{
  "schedule": {
    "enabled": true,
    "time": "23:00",
    "timezone": "Europe/London"
  },
  "review": {
    "lookback_days": 7,
    "model": "gemini-2.5-flash",
    "max_suggestions": 10
  },
  "maintenance": {
    "archive_after_days": 7,
    "retention_days": 30,
    "consolidate_fragments": true,
    "auto_archive_safe": true
  },
  "safety": {
    "require_approval_for_content": true,
    "require_approval_for_delete": true,
    "trash_instead_of_delete": true
  }
}
```

## 安全性

- **内容建议**：永远不会自动应用（必须经过人工审核）；
- **安全维护操作**：归档操作会自动执行（使用 `--safe` 参数）；
- **高风险操作**（如删除、重命名文件）：需要使用 `--all` 参数并获取用户确认；
- **已删除文件的恢复**：被删除的文件会被保存到 `agents/memory/.trash/` 目录中（可在保留期限内恢复）。

## 命令

```bash
# Run review manually
openclaw skill memory-maintenance review

# Apply changes
openclaw skill memory-maintenance apply [--dry-run|--safe|--all] DATE

# Run cleanup
openclaw skill memory-maintenance cleanup

# Check status
openclaw skill memory-maintenance status

# View stats
openclaw skill memory-maintenance stats
```

## 与 `MEMORY.md` 的集成

该技能会针对 `MEMORY.md` 文件中的标准章节提出更新建议，包括：
- 代理身份和核心偏好设置；
- 基础设施/配置信息；
- 内存管理策略；
- 备份与迁移方案；
- 联系人信息；
- 计划任务；
- 内容创建与项目管理；
- 正在运行的项目。

## 文件结构

- `agents/memory/review-v2-YYYY-MM-DD.json`：结构化的更新建议；
- `agents/memory/review-v2-YYYY-MM-DD.md`：人类可读的报告；
- `agents/memory/stats.json`：汇总的统计数据。

## 归档机制

- `agents/memory/archive/YYYY-MM/`：按月分类的归档文件；
- `agents/memory/.trash/`：可恢复的已删除文件。

## 系统要求

- OpenClaw 版本需大于或等于 2026.2.0；
- 需安装 Gemini CLI（使用 `brew install gemini-cli` 命令安装）；
- 需安装 `jq` 工具（使用 `brew install jq` 命令安装）；
- 需拥有 Google AI Studio 提供的 Gemini API 密钥。

## 故障排除

- 如果出现 “Gemini 失败” 的错误，请检查 `.env` 文件中是否设置了 `GEMINI_API_KEY`；
- 如果没有生成任何建议，请确认 `memory/YYYY-MM-DD.md` 文件中是否存在每日记录；
- 如果出现 “维护任务过多”的情况，可以运行 `openclaw skill memory-maintenance apply --safe` 命令来归档旧文件；
- 如需调整归档策略，请修改 `config/settings.json` 文件中的 `archive_after_days` 参数。

## 开发者

该技能由 **Max Hutchinson** 开发，作为 AI 代理基础设施探索项目的一部分。

- GitHub 仓库：[@MaxLaurieHutchinson](https://github.com/MaxLaurieHutchinson)
- 使用的代理模型：Ash（OpenClaw）

## 许可证

采用 MIT 许可证——允许自由使用、修改和分发。

---

*该技能属于混合代理架构的一部分，旨在帮助代理持续优化其性能。*