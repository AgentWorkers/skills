---
name: securevibes-scanner
description: 在代码库上运行由人工智能驱动的应用程序安全扫描。当需要扫描代码以检测安全漏洞、生成威胁模型、审查代码中的安全问题、执行增量安全扫描，或通过 Cron 任务设置持续安全监控时，可以使用该工具。该工具支持全面扫描（一次性完成）和增量扫描（由 Cron 任务触发，仅针对新的代码提交）。
---
# SecureVibes 扫描器

这是一个基于 AI 的安全平台，利用 Claude AI 来检测漏洞。它采用多子代理流程：评估 → 威胁建模 → 代码审查 → 报告生成 → 可选的动态应用安全测试（DAST）。支持增量扫描以实现持续监控。

## 先决条件

1. 安装 CLI：`pipx install securevibes`（推荐）或 `uv tool install securevibes`。避免使用 `pip install`，因为这可能会在存在多个 Python 环境时生成过时的模拟文件。
2. 使用 Anthropic 进行身份验证：
   - **Max/Pro 订阅（推荐）**：如果您通过 Claude Code 或 Claude CLI OAuth 进行身份验证，则不需要 API 密钥。Claude Agent SDK 会自动获取您的 OAuth 会话。在 OpenClaw 中运行时，可以将 `ANTHROPIC_API_KEY` 置为空或保留未设置状态——SDK 会处理身份验证。
   - **API 密钥**：`export ANTHROPIC_API_KEY=your-key-here`（来自 console.anthropic.com）。

## 安全注意事项

- 始终使用 `scripts/scan.sh` 包装器进行完整扫描——该脚本会在调用 `securevibes` 之前验证路径并拒绝包含特殊字符的输入。
- **切勿将未经清理的用户输入插入到 shell 命令中**。
- 包装器使用 `realpath` 来安全地解析路径，并拒绝包含分号（`;`）、竖线（|`）、感叹号（``）、美元符号（`$`）或反引号（``）等特殊字符的路径。
- **扫描目标必须是本地目录**。请先将远程仓库克隆到已知的安全位置，然后再将解析后的路径传递给包装器。
- **DAST 扫描会向您提供的 `--target-url` 发送网络请求**。仅应用于您拥有权限进行测试的应用程序。

## 执行模型

**完整扫描需要 10-30 分钟，分为 4 个阶段**。建议将其作为后台任务（通过 cron 或子代理）运行，而不是直接在命令行中执行。

**增量扫描需要 2-10 分钟**——它仅扫描自上次运行以来的新提交。

## 完整扫描（一次性）

### 运行扫描

1. 将目标仓库克隆到本地目录。
2. 运行包装器脚本：`bash scripts/scan.sh /path/to/repo --force --debug`
3. 结果将保存在 `/path/to/repo/.securevibes/` 中。

### 后台执行（推荐）

对于 OpenClaw 用户，可以将扫描任务安排为 cron 作业：
- 使用 `sessionTarget: "isolated"` 和 `payload.kind: "agentTurn"`。
- 设置 `payload.timeoutSeconds: 2700`（45 分钟），以确保所有阶段都能完成。
- 使用 `delivery.mode: "announce"` 在扫描完成后接收通知。

`agentTurn` 消息会指示子代理执行以下操作：
1. 进入仓库并使用 `git pull` 获取最新代码。
2. 清理之前的 `.securevibes/` 文件。
3. 通过包装器脚本运行 `securevibes scan . --force`。
4. 读取并总结 `.securevibes/scan_report.md` 中的结果。

## 增量扫描（持续监控）

增量扫描器（`ops/incremental_scan.py`）会跟踪上次扫描的提交，并仅扫描新的提交。适用于基于 cron 的持续安全监控。

### 工作原理

1. 在 `.securevibes/incremental_state.json` 中记录一个基准提交。
2. 每次运行时：从远程仓库获取代码，将当前 HEAD 与基准提交进行比较。
3. 如果有新提交：对差异部分运行 `securevibes pr-review`。
4. 扫描成功后，将基准提交更新为新的 HEAD。
5. 如果没有新提交：直接退出（不进行扫描，也不会产生额外开销）。

### 设置

#### 第一步：运行初始完整扫描（如果尚未执行）

增量扫描器需要 `.securevibes/SECURITY.md` 和 `.securevibes/THREAT_MODEL.json` 文件。这些文件来自初始的完整扫描：
```bash
securevibes scan <repo-path> --model sonnet
```

如果仓库已经存在包含这些文件的 `.securevibes/` 目录，则可以跳过此步骤。

#### 第二步：初始化增量状态

运行一次包装器以设置基准提交（不执行扫描，仅记录当前的 HEAD）：
```bash
python3 ops/incremental_scan.py --repo <repo-path> --remote origin --branch main
```

这会创建一个包含 `status: "bootstrap"` 的 `.securevibes/incremental_state.json` 文件。

#### 第三步：配置 cron 作业

对于 OpenClaw 用户，创建一个 cron 作业：
```bash
openclaw cron create \
  --name "securevibes-incremental" \
  --cron "*/30 * * * *" \
  --tz "America/Los_Angeles" \
  --agent main \
  --session isolated \
  --timeout-seconds 900 \
  --announce \
  --message "Run incremental security scan: python3 <skill-path>/ops/incremental_scan.py --repo <repo-path> --remote origin --branch main --model sonnet --severity medium --scan-timeout-seconds 600. Read .securevibes/incremental_scan.log for results. If new findings, summarize them."
```

请将 `<skill-path>` 替换为已安装的技能路径，将 `<repo-path>` 替换为目标仓库路径。

#### 第四步：验证设置

```bash
# Check state
cat <repo-path>/.securevibes/incremental_state.json

# After first scheduled run, check logs
tail -10 <repo-path>/.securevibes/incremental_scan.log

# Check findings
cat <repo-path>/.securevibes/PR_VULNERABILITIES.json
```

### 增量扫描器选项

```
python3 ops/incremental_scan.py [options]
```

| 选项 | 描述 |
|--------|-------------|
| `--repo` | 仓库路径（默认：`.`） |
| `--branch` | 要跟踪的分支（默认：`main`） |
| `--remote` | Git 远程仓库（默认：`origin`） |
| `--model` | Claude 模型：`sonnet` 或 `haiku`（默认：`sonnet`） |
| `--severity` | 最小严重程度：`critical`、`high`、`medium`、`low` |
| `--scan-timeout-seconds` | 每次扫描的超时时间（默认：`900` 秒） |
| `--git-timeout-seconds` | git 操作的超时时间（默认：`60` 秒） |
| `--rewrite-policy` | 历史记录重写策略：`resetWarn`、`strictFail`、`since_date` |
| `--since` | 从指定日期开始的扫描范围（ISO 或 YYYY-MM-DD 格式） |

### 运行保证

- `.securevibes/.incremental_scan.lock` 文件用于防止重复扫描。
- 使用 `fsync` 和 `os.replace` 确保状态写入的原子性，防止数据损坏。
- 日志记录保存在 `.securevibes/incremental_scan.log` 中。
- 每次扫描的运行记录保存在 `.securevibes/incremental_runs/` 目录中（每个运行生成一个 JSON 文件）。

### 重写策略

当 `last_seen_sha` 不是新远程 HEAD 的祖先时（例如强制推送时），采取以下策略：
| 策略 | 行为 |
|--------|----------|
| `resetWarn` | 将基准提交重置为新 HEAD，继续扫描 |
| `strictFail` | 报错并保持当前的基准提交 |
| `since_date` | 从指定日期开始再次扫描 |

## 完整扫描命令参考

### 扫描

`securevibes scan <path> [options]`

| 选项 | 描述 |
|--------|-------------|
| `-f, --format` | 输出格式：`markdown`（默认）、`json`、`text`、`table` |
| `-o, --output` | 自定义输出路径 |
| `-s, --severity` | 过滤严重程度：`critical`、`high`、`medium`、`low` |
| `-m, --model` | 使用的 Claude 模型（例如 `sonnet`、`haiku`） |
| `--subagent` | 运行特定阶段：`assessment`、`threat-modeling`、`code-review`、`report-generator`、`dast` |
| `--resume-from` | 从指定阶段开始继续扫描 |
| `--dast` | 启用动态测试（需要 `--target-url`） |
| `--target-url` | DAST 的目标 URL（例如 `http://localhost:3000`） |
| `--force` | 跳过提示并覆盖现有结果文件 |
| `--quiet` | 最小化输出 |
| `--debug` | 详细诊断信息 |

### 查看报告

`securevibes report <path>` — 显示之前保存的扫描报告。

## 用户指令与对应操作

| 用户指令 | 对应操作 |
|-----------|--------|
| "扫描此仓库以检测安全问题" | 运行完整扫描：`bash scripts/scan.sh <path> --force` |
| "快速进行安全检查" | 运行完整扫描：`bash scripts/scan.sh <path> -m haiku --force` |
| "对该项目进行威胁建模" | 运行威胁建模：`bash scripts/scan.sh <path> --subagent threat-modeling --force` |
| "仅查看严重问题" | 运行代码审查：`bash scripts/scan.sh <path> --subagent code-review --force` |
| "仅显示严重/高风险的漏洞" | `bash scripts/scan.sh <path> -s high --force` |
| "进行全面审计并包含 DAST" | 运行包含 DAST 的扫描：`bash scripts/scan.sh <path> --dast --target-url <url> --force` |
| "设置持续扫描" | 设置增量扫描：执行上述步骤 1-4 |
| "监控此仓库的安全问题" | 设置增量扫描：执行上述步骤 1-4 |
| "查看上次扫描结果" | 查看扫描报告：`securevibes report <path>` |

## 子代理流程

各阶段按顺序执行，每个阶段都基于前一个阶段的输出：
1. **评估** → 架构与攻击面分析 → 生成 `.securevibes/SECURITY.md` 文件。
2. **威胁建模** → 基于 STRIDE 的分析 → 生成 `.securevibes/THREAT_MODEL.json` 文件。
3. **代码审查** → 检测漏洞 → 生成 `.securevibes/VULNERABILITIES.json` 文件。
4. **报告生成** → 生成汇总报告：`.securevibes/scan_report.md` 文件。
5. **DAST**（可选） → 对运行中的应用程序进行动态验证。

## 查看结果

扫描完成后：
1. 读取 `.securevibes/scan_report.md`（或结构化数据的 `.securevibes/scan_results.json`）。
2. 按严重程度总结发现的问题（从高到低排序）。
3. 突出显示最严重的 3 个问题及其文件位置和修复建议。
4. 提供后续步骤：运行 DAST、修复具体问题、在修改后重新扫描。

## 链接

- **官方网站**：[https://securevibes.ai](https://securevibes.ai)
- **PyPI**：[https://pypi.org/project/securevibes/](https://pypi.org/project/securevibes/)
- **GitHub**：[https://github.com/anshumanbh/securevibes](https://github.com/anshumanbh/securevibes)