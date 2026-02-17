---
name: dep-audit
description: >
  **审计项目依赖项中的已知漏洞（CVEs）**  
  支持检测 npm、pip、Cargo 和 Go 项目的依赖关系中的已知安全漏洞（CVEs）。无需使用任何 API 密钥。默认设置为“仅报告”模式；执行修复命令前需要用户确认。
version: 0.1.3
author: CacheForge
tags: [security, audit, dependencies, cve, supply-chain, discord, discord-v2]
---
# 依赖项审计功能

该功能用于检测并报告项目中依赖项树中存在的已知漏洞。支持 **npm**、**pip (Python)**、**Cargo (Rust)** 和 **Go** 环境。

**无需任何 API 密钥或配置信息**，只需将工具指向项目目录即可使用。

## 激活方式

当用户提及以下关键词时，该功能会被激活：
- “audit”（审计）
- “vulnerability”（漏洞）
- “CVE”（通用漏洞编码）
- “dependency check”（依赖项检查）
- “supply chain”（供应链安全）
- “security scan”（安全扫描）

## 功能示例

- “审计该项目中的漏洞”
- “检查 ~/projects 目录下的所有仓库中是否存在已知的 CVE 漏洞”
- “是否有需要立即修复的严重漏洞？”
- “为该项目生成软件成分清单（SBOM）”

## 权限设置

```yaml
permissions:
  exec: true          # Required to run audit CLIs
  read: true          # Read lockfiles
  write: on-request   # SBOM generation writes sbom.cdx.json when user asks
  network: true       # Tools fetch advisory DBs
```

## 代理工作流程

请严格按照以下步骤操作：

### 第一步：检测

运行检测脚本，以识别项目的 `lockfile` 文件及可用的审计工具：

```bash
bash <skill_dir>/scripts/detect.sh <target_directory>
```

如果未指定目标目录，系统将使用当前工作目录（`.`）。

解析检测结果输出的 JSON 数据，记录哪些依赖项生态系统使用了 `lockfile` 文件，以及哪些审计工具可用。

### 第二步：审计每个依赖项生态系统

对于第一步中检测到的每个依赖项生态系统：
- **如果该审计工具可用**，则运行相应的脚本：
  ```bash
  bash <skill_dir>/scripts/audit-npm.sh <directory>
  bash <skill_dir>/scripts/audit-pip.sh <directory>
  bash <skill_dir>/scripts/audit-cargo.sh <directory>
  bash <skill_dir>/scripts/audit-go.sh <directory>
  ```

- **如果工具缺失**，向用户提示所需的工具名称及安装命令，并跳过该生态系统，继续审计其他生态系统。

> **注意：** `yarn.lock` 和 `pnpm-lock.yaml` 分别对应 `yarn` 和 `pnpm` 依赖项生态系统。在 v0.1.x 版本中，仅支持使用 `package-lock.json` 文件进行审计。如果仅存在 `yarn.lock` 或 `pnpm-lock.yaml` 文件，系统会提示用户当前版本不支持专门的审计工具，并建议手动运行 `yarn audit` 或 `pnpm audit`。

每个审计脚本会将处理结果以标准化 JSON 格式输出到标准输出（stdout）。

### 第三步：汇总结果

将每个生态系统的审计结果合并到一个统一的 JSON 文件中：

```bash
bash <skill_dir>/scripts/aggregate.sh <npm_result.json> <pip_result.json> ... 1>unified.json 2>report.md
```

汇总脚本会将处理后的 JSON 数据输出到标准输出（stdout），并将审计报告以 Markdown 格式输出到标准错误输出（stderr）：
- `2>report.md` 包含审计报告
- `1>unified.json` 包含汇总后的 JSON 数据

### 第四步：展示结果

向用户展示汇总后的 Markdown 报告，重点显示：
- 按严重程度分类的漏洞总数
- 首先展示严重和较高的漏洞（这些漏洞需要立即处理）
- 显示哪些生态系统已被审计，哪些被跳过

- 如果未发现任何漏洞：显示 “✅ 未发现已知漏洞”。
- 如果未找到 `lockfile` 文件：显示 “在 <dir> 目录中未找到 lockfile 文件。该功能支持 npm、pip、Cargo 和 Go 项目。”

### Discord v2 使用方式（OpenClaw v2026.2.14 及更高版本）

当用户位于 Discord 频道中时：
- 首先发送一条简短的消息，列出漏洞总数及严重/较高的漏洞信息。
- 保持消息长度在 1200 字符以内，避免使用过长的 Markdown 表格。
- 如果支持相关 Discord 功能，提供以下操作选项：
  - “查看完整报告”
  - “生成软件成分清单（SBOM）”
- 如果相关功能不可用，以编号列表的形式提供相同选项。
- 分段发送详细信息（每段不超过 15 行），以提高可读性。

### 第五步：提供修复建议（用户主动请求时）

如果用户请求修复漏洞：
- 列出每个漏洞的修复命令，包括对应的包名、当前版本和目标版本。
- 建议用户先创建一个临时分支：`git checkout -b dep-audit-fixes`
- 在执行任何修复命令之前，务必获取用户的明确确认。
- **严禁** 未经确认直接批量执行修复命令。

### 示例交互流程：
```
I found these fix commands:
  1. cd /home/user/project && npm audit fix
  2. pip install requests>=2.31.0

I recommend creating a branch first:
  git checkout -b dep-audit-fixes

Shall I run them? (yes/no)
```

### 第六步：生成软件成分清单（SBOM）（用户主动请求时）

```bash
bash <skill_dir>/scripts/sbom.sh <directory>
```

向用户报告生成后的 SBOM 文件的位置及包含的组件数量。

## 错误处理

| 错误情况 | 处理方式 |
|-----------|----------|
| 检测工具未找到 | 显示缺失的工具名称及安装命令，继续使用其他可用工具。 |
| 审计工具失败 | 记录错误信息，并显示 “[ecosystem] 的审计失败：[错误原因]”，继续审计其他生态系统。 |
- 检测超时（每个工具超过 30 秒） | 当启用 `timeout`/`gtimeout` 选项时，显示 “[ecosystem] 的审计超时，已跳过”，继续审计其他生态系统。 |
- 目标目录不存在或无法访问 | 显示 “未找到或无法访问目标目录”，并停止对该生态系统的审计。 |
- 未找到 lockfile 文件 | 显示 “未找到 lockfile 文件”，并列出支持的生态系统。 |
- 未安装 `jq` 工具 | 即使没有 `jq`，系统也能完成审计和结果汇总；但建议先安装该工具。 |
- `lockfile` 文件格式错误 | 显示该生态系统的解析错误，继续审计其他生态系统。 |

## 系统稳定性

- `aggregate.sh` 脚本现在可以处理混合格式的输入数据（包括有效结果和错误信息）。
- 无效的输入数据会被记录在汇总结果的 `errors` 部分，并在 Markdown 报告中以 “Skipped / Error Inputs” 标签显示。
- 如果没有有效的审计结果，汇总输出会将状态设置为 “error” 而不会导致程序崩溃。

## 安全性注意事项

- **默认模式下，该功能仅用于生成报告**，不会修改项目文件，除非用户明确请求并确认进行修复。
- 审计工具仅读取 `lockfile` 文件，不会执行项目代码。
- 修复命令（如 `npm audit fix`、`pip install --upgrade`）仅作为建议提供；执行前会请求用户确认。
- 该功能会查询已知的漏洞数据库（如 OSV、GitHub Advisory DB、RustSec），但无法检测零日漏洞或运行时漏洞。
- 所有数据仅限于系统内置的审计工具所使用的范围（即查询公开的安全数据库），不会发送到第三方服务。
- 该功能不收集任何使用数据，也不进行任何跟踪或上报行为。