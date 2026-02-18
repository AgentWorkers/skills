---
name: securevibes-scanner
description: 对代码库执行由人工智能驱动的应用程序安全扫描。当需要扫描代码以查找安全漏洞、生成威胁模型、审查代码中的安全问题、验证发现的结果、提出修复建议或验证补救措施时，请使用该功能。该功能会在针对项目或代码库的安全扫描、威胁模型分析、安全审查、漏洞评估、代码审计或与应用程序安全（AppSec）相关的请求触发。
env:
  - name: ANTHROPIC_API_KEY
    required: true
    description: Anthropic API key for Claude-powered analysis
  - name: SECUREVIBES_MAX_TURNS
    required: false
    description: Max Claude conversation turns per subagent phase (default 50)
dependencies:
  - name: securevibes
    type: pip
    version: ">=0.3.0"
    url: https://pypi.org/project/securevibes/
    repository: https://github.com/anshumanbh/securevibes
links:
  homepage: https://securevibes.ai
  repository: https://github.com/anshumanbh/securevibes
  pypi: https://pypi.org/project/securevibes/
author: anshumanbh
---
# SecureVibes 扫描器

这是一个基于人工智能（AI）的安全平台，利用 Claude AI 来检测系统漏洞。它采用多子代理的工作流程：评估 → 威胁建模 → 代码审查 → 报告生成 → 可选的动态应用安全测试（DAST）。

## 先决条件

1. 安装命令行界面（CLI）：
   ```bash
   pip install securevibes
   ```
2. 设置您的 Anthropic API 密钥：
   ```bash
   export ANTHROPIC_API_KEY=your-key-here
   ```

## 安全注意事项

- **始终使用 `scripts/scan.sh` 包装脚本**：该脚本会在调用 `securevibes` 之前验证路径并拒绝任何 shell 元字符。
- **切勿将未经过滤的用户输入插入到 shell 命令中**。该脚本使用 `realpath` 来安全地解析路径，并拒绝包含 `;`, `|`, `&`, `$`, 单引号或其他元字符的路径。
- **扫描目标必须是本地目录**。请先将远程仓库克隆到已知的安全位置，然后再将解析后的路径传递给包装脚本。
- **DAST 扫描会向您提供的 `--target-url` 发送网络请求**。请仅对您拥有权限或允许测试的应用程序进行此类扫描。

## 执行模型

扫描过程分为 4 个阶段，耗时约 10-30 分钟。建议将扫描任务设置为后台作业（通过 cron 或子代理执行），而不是在命令行中直接运行。

### 运行扫描

1. 将目标仓库克隆到本地目录。
2. 运行包装脚本：
   ```bash
   bash scripts/scan.sh /path/to/repo --force --debug
   ```
3. 扫描结果将保存在 `/path/to/repo/.securevibes/` 目录下。

### 推荐的后台执行方式（针对 OpenClaw 用户）

- 使用 `sessionTarget: "isolated"` 和 `payload.kind: "agentTurn"` 来安排扫描任务。
- 设置 `payload.timeoutSeconds: 2700`（45 分钟），以确保所有阶段都能完成。
- 使用 `delivery.mode: "announce"` 在扫描完成后接收通知。

`agentTurn` 消息应指示子代理执行以下操作：
1. 进入仓库并使用 `git pull` 获取最新代码。
2. 清除之前的 `.securevibes/` 文件夹中的扫描结果。
3. 通过包装脚本运行 `securevibes scan . --force`。
4. 读取并汇总 `.securevibes/scan_report.md` 中的扫描结果。

结果的存储位置、与之前扫描结果的对比方式以及通知的发送方式由您的代理配置决定。

## 命令参考

### 扫描命令

```bash
securevibes scan <path> [options]
```

| 选项          | 描述                          |
|------------------|--------------------------------------|
| `-f, --format`     | 输出格式（默认：markdown, json, text, table）         |
| `-o, --output`     | 自定义输出路径                        |
| `-s, --severity`     | 过滤漏洞严重程度（critical, high, medium, low）       |
| `-m, --model`     | 使用的 Claude 模型（例如：sonnet 或 haiku，以降低计算成本/加快速度） |
| `--subagent`     | 仅运行某个阶段：assessment, threat-modeling, code-review, report-generator, dast |
| `--resume-from`    | 从特定阶段继续执行扫描                    |
| `--dast`       | 启用动态测试（需要提供 `--target-url`）           |
| `--target-url`     | DAST 的目标 URL（例如：http://localhost:3000）         |
| `--force`       | 跳过提示信息并覆盖现有结果文件             |
| `--quiet`       | 以最小化输出显示结果                   |
| `--debug`       | 显示详细的调试信息                     |

### 查看报告

```bash
securevibes report <path>
```
用于查看之前保存的扫描报告。

## 用户指令与扫描参数的对应关系

| 用户指令            | 扫描参数                          |
|------------------|--------------------------------------|
| "扫描是否存在安全问题"      | `--force`                         |
| "快速进行安全检查"       | `-m haiku --force`                     |
| "对项目进行威胁建模"      | `--subagent threat-modeling --force`             |
| "仅审查代码"        | `--subagent code-review --force`             |
| "仅显示严重/高风险的漏洞"    | `-s high --force`                     |
| "进行全面审计（包含 DAST）"    | `--dast --target-url <url> --force`             |
| "以 JSON 格式输出报告"     | `-f json -o results.json --force`             |
| "从代码审查阶段继续扫描"    | `--resume-from code-review --force`             |
| "显示上次扫描的结果"     | `securevibes report <path>`                   |

## 子代理工作流程

各阶段按顺序执行，每个阶段都会基于前一个阶段的结果进行进一步处理：

1. **评估** → 架构分析与攻击面识别 → 生成 `.securevibes/SECURITY.md` 文件
2. **威胁建模** → 基于 STRIDE 的威胁分析 → 生成 `.securevibes/THREAT_MODEL.json` 文件
3. **代码审查** → 逐行检测漏洞 → 生成 `.securevibes/VULNERABILITIES.json` 文件
4. **报告生成** → 合并所有发现结果并生成 `.securevibes/scan_report.md` 文件
5. **DAST**（可选） → 对正在运行的应用程序进行动态安全测试

## 查看扫描结果

扫描完成后：
1. 阅读 `.securevibes/scan_report.md`（或结构化数据文件 `.securevibes/scan_results.json`）。
2. 按严重程度汇总漏洞（严重 > 高风险 > 中等 > 低风险）。
3. 突出显示最严重的 3 个漏洞及其所在文件位置及修复建议。
4. 提供后续步骤：执行 DAST 测试、修复具体问题、在修改后重新扫描。

## 相关链接

- **官方网站**：https://securevibes.ai
- **PyPI 仓库**：https://pypi.org/project/securevibes/
- **GitHub 仓库**：https://github.com/anshumanbh/securevibes/