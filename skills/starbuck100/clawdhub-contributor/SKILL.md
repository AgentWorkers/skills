---
name: clawdhub-contributor
description: 通过发现未知的技能、报告漏洞以及分享技能教程来为 ClawdHub 生态系统做出贡献。系统提供了三种贡献模式（被动模式/主动模式/全模式），让您能够根据自己的需求来控制自己的贡献程度。
metadata: {"openclaw":{"requires":{"bins":["bash","jq"]}}}
---

# ClawdHub 贡献者插件

该插件为您的代理程序添加了贡献功能，通过分析技能、报告错误以及分享有用的技能组合来帮助扩展 ClawdHub 生态系统。

## 模式

| 模式 | 功能 |
|------|-------------|
| **被动模式** | 仅支持错误报告和技能使用记录（默认安全模式） |
| **主动模式** | 启用自动扫描功能：在本地分析未知技能并生成报告 |
| **全模式** | 包含上述所有功能，同时支持可选的遥测数据收集 |

您可以通过 `config/default.json` 文件或 `CLAWDHUB_CONTRIB_MODE` 环境变量来设置模式。

## 功能

### 自动扫描（主动模式/全模式）

分析本地技能目录，并生成结构化的质量/安全报告：

```bash
bash scripts/scout.sh /path/to/skill-directory
```

输出：包含依赖信息、质量评分和安全状态的 JSON 报告。
**完全离线** — 无需网络连接，仅进行静态分析。

### 错误报告（所有模式）

报告技能使用过程中出现的错误，并附带经过处理的系统上下文信息：

```bash
bash scripts/report-bug.sh <skill-slug> <error-message> [context]
```

输出：可用于 API 提交的 JSON 错误报告。会收集操作系统和节点版本信息，但**绝不会**泄露主机名、IP 地址或用户名。

### 技能组合分享（所有模式）

分享解决特定任务所需的一系列技能组合：

```bash
bash scripts/submit-recipe.sh <task-description> <skill1> [skill2] [skill3] ...
```

输出：可用于 API 提交的 JSON 技能组合信息。

## 配置

编辑 `config/default.json` 文件：

```json
{
  "mode": "passive",
  "telemetry": false,
  "autoScout": false,
  "bugReports": true,
  "recipes": true
}
```

| 键 | 类型 | 描述 |
|-----|------|-------------|
| `mode` | 字符串 | `passive`（被动模式）、`active`（主动模式）或 `full`（全模式） |
| `telemetry` | 布尔值 | 是否启用匿名使用数据统计（仅限全模式） |
| `autoScout` | 布尔值 | 在遇到未知技能时自动进行扫描（仅限主动模式/全模式） |
| `bugReports` | 布尔值 | 是否启用错误报告功能 |
| `recipes` | 布尔值 | 是否启用技能组合分享功能 |

## 命令汇总

| 命令 | 所需模式 | 描述 |
|---------|--------------|-------------|
| `scripts/scout.sh <dir>` | 主动模式 | 分析指定目录中的技能 |
| `scripts/report-bug.sh <slug> <msg> [ctx>` | 任意模式 | 生成错误报告 |
| `scripts/submit-recipe.sh <task> <skills...>` | 任意模式 | 生成技能组合信息 |

## 安全性说明

- 所有脚本均不访问网络 |
- 不会收集任何凭据、IP 地址或用户名 |
- 所有输出均为经过处理的 JSON 格式 |
- 扫描过程仅进行读取操作（仅进行静态分析）