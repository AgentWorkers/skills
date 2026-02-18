---
name: crusty-security
version: 1.3.0
description: >
  OpenClaw代理的安全与威胁扫描功能：  
  - 扫描文件及相关操作以检测恶意软件；  
  - 监控代理行为，识别潜在的安全风险；  
  - 审查主机系统的安全配置；  
  - 支持以下命令触发扫描：  
    - “扫描此文件”（Scan this file）  
    - “是否安全？”（Is this safe?）  
    - “病毒扫描”（Virus scan）  
    - “恶意软件检测”（Malware check）  
    - “安全扫描”（Security scan）  
    - “威胁检测”（Threat detection）  
    - “检查此下载内容”（Check this download）  
    - “隔离受感染的文件”（Quarantine infected files）  
    - “扫描我的系统”（Scan my system）  
    - “生成威胁报告”（Generate threat report）  
    - “定期扫描”（Scheduled scan）  
    - “审核主机安全配置”（Audit host security）  
    - “审核代理完整性”（Audit agent integrity）  
    - “生成安全报告”（Generate security report）  
    - “监控代理状态”（Monitor agent status）。
homepage: https://crustysecurity.com
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# Crusty Security — 安全与威胁扫描

## 概述

Crusty Security 保护 OpenClaw 代理免受各种真实威胁的攻击：下载文件中的恶意软件、来自 ClawHub 的受损技能、数据泄露、提示注入攻击以及主机级别的安全漏洞。它使用 ClamAV 进行文件扫描，并结合 AI 技术对代理进行静态分析。

**威胁模型：** 代理本身就是一个潜在的攻击面。提示注入攻击可能导致代码执行；恶意技能会以代理的权限运行。Crusty Security 既保护主机，也保护代理的完整性。

## 快速参考

| 任务 | 命令 |
|------|---------|
| 安装 ClamAV | `bash scripts/install_clamav.sh` |
| 扫描文件 | `bash scripts/scan_file.sh /path/to/file` |
| 扫描目录 | `bash scripts/scan_file.sh -r /path/to/dir` |
| 审计技能 | `bash scripts/audit_skill.sh /path/to/skill/` |
| 主机安全审计 | `bash scripts/host_audit.sh` |
| 监控代理完整性 | `bash scripts/monitor_agent.sh` |
| 生成安全报告 | `bash scripts/generate_report.sh` |

所有脚本的输出格式为 JSON。所有脚本都支持 `--help` 参数。所有路径都是相对于当前技能目录的。

## 设置（首次运行）

运行 `bash setup.sh` 即可完成设置：
1. 如果未安装 ClamAV，则会进行安装。
2. 配置 freshclam（适用于 macOS Homebrew 环境）。
3. （如果设置了 `CRUSTY_API_KEY`，）向仪表板发送初始心跳信号。
4. 进行初始的主机审计和 workspace 扫描（结果会立即显示在仪表板上）。
5. 检查需要创建哪些定时扫描任务。

**⚠️ 重要提示：** 设置完成后，必须使用 OpenClaw 的 cron 工具创建以下 cron 任务。`setup.sh` 负责 bash 级别的安装，但 cron 任务需要使用代理级别的工具。请在首次安装后立即执行这些任务，不要等待用户提示。

### 必需的 Cron 任务（首次安装时创建）

使用 OpenClaw 的 cron 工具（`cron add`）创建以下任务。请将 `{SKILL_DIR}` 替换为实际的技能目录路径，将 `{WORKSPACE}` 替换为 workspace 的路径（通常为 `/data/workspace`）：

| 名称 | 安排时间 | 目标会话 | 执行命令 |
|------|----------|---------------|---------|
| `crusty-daily-scan` | `0 3 * * *` | main / systemEvent | `每天执行一次扫描：bash {SKILL_DIR}/scripts/scan_file.sh --incremental -r {WORKSPACE} && bash {SKILL_DIR}/scripts/monitor_agent.sh` |
| `crusty-weekly-full` | `0 3 * * 0` | main / systemEvent | `每周执行一次全面扫描：bash {SKILL_DIR}/scripts/scan_file.sh -r {WORKSPACE} && bash {SKILL_DIR}/scripts/host_audit.sh && bash {SKILL_DIR}/scripts/generate_report.sh --output /tmp/crusty_logs/weekly_report.md` |
| `crusty-monthly-deep` | `0 4 1 * *` | main / systemEvent | `每月执行一次深度审计：bash {SKILL_DIR}/scripts/host_audit.sh --deep` |

### 仪表板 Cron 任务（仅当设置了 `CRUSTY_API_KEY` 时）

| 名称 | 安排时间 | 目标会话 | 执行命令 |
|------|----------|---------------|---------|
| `crusty-heartbeat` | 每 300000 毫秒（5 分钟） | main / systemEvent | `发送心跳信号：bash {SKILL_DIR}/scripts/dashboard.sh heartbeat` |
| `crusty-clawhub-sync` | 每 43200000 毫秒（12 小时） | isolated / agentTurn | `同步 ClawHub 安全信息：python3 {SKILL_DIR}/scripts/clawhub_sync.py --push` |

请先使用 `cron list` 命令检查已存在的 cron 任务（名称前缀为 `crusty-` 的任务可以忽略）。

详细配置信息请参阅 `references/setup.md`。

## 仪表板连接

如果用户设置了 `CRUSTY_API_KEY`，该技能会将扫描结果发送到 Crusty Security 仪表板（crustysecurity.com）：
- **心跳信号** 每 5 分钟自动发送一次，以显示代理状态。
- 扫描结果会在扫描命令中添加 `--push` 选项后发送到仪表板。
- `clawhub-sync` 通过 `python3 scripts/clawhub_sync.py --push` 同步技能信息。
- 如果未设置 `CRUSTY_API_KEY`，所有操作都在本地完成，数据不会被发送到外部。
- 仪表板不会主动与代理通信——数据仅从代理流向仪表板。

## 扫描工作流程

### 文件扫描

**触发条件：** “扫描此文件”、“此文件安全吗”、“检查此下载内容”、“病毒扫描”

1. 运行 `bash scripts/scan_file.sh <path>` 进行 ClamAV 本地扫描。
2. 报告扫描结果：
   - ✅ 无威胁：“未检测到威胁。使用 ClamAV 进行扫描，签名更新时间为 [date]。”
   - ⚠️ 可疑：“ClamAV 低置信度检测。建议隔离检查。”
   - 🚨 恶意软件：“检测到威胁：[名称]。建议隔离、删除或忽略。”

**对于目录：**
```bash
bash scripts/scan_file.sh -r /data/workspace      # Full recursive scan
bash scripts/scan_file.sh -r --incremental /data/workspace  # Skip unchanged files
```

**隔离流程：**
```bash
bash scripts/scan_file.sh --quarantine /path/to/file   # Move to quarantine
# Quarantine location: $CRUSTY_QUARANTINE (default: /tmp/crusty_quarantine)
# Manifest: /tmp/crusty_quarantine/manifest.json
```

**重要说明：**
- 如果可用，ClamAV 优先使用 `clamdscan`（守护进程）；否则使用 `clamscan`。
- 文件大小上限默认为 200MB（可通过 `CRUSTY_MAX_FILE_SIZE` 配置）。
- 加密文件会被标记为“未扫描”，无法检查其内容。
- ClamAV 支持处理 zip、rar、7z、tar、gz 格式的文件。

### 技能审计（供应链安全）

**触发条件：** “审计此技能”、“此技能安全吗”、“检查技能安全性”、“扫描技能”

`bash scripts/audit_skill.sh /path/to/skill/directory/`

**审计内容：**
- 🔴 **严重风险：** 使用 curl/wget 或 pip 进行攻击、反向 shell 模式、加密挖矿行为。
- 🟠 **较高风险：** 使用动态输入执行命令、base64 解码、数据泄露端口（如 webhook.site、ngrok 等）、凭证收集、二进制可执行文件、代理配置修改。
- 🟡 **中等风险：** 隐藏文件、系统文件访问权限、硬编码 IP 地址、混淆代码、持久化机制（如 cron、systemd）。
- 🔵 **较低/信息风险：** 文件体积较大、文档中包含凭证信息。

**使用场景：**
- 在从 ClawHub 安装任何技能之前。
- 在审查第三方提供的技能时。
- 定期审计所有已安装的技能：`for d in /data/workspace/skills/*/; do bash scripts/audit_skill.sh "$d"; done`

### 主机安全审计

**触发条件：** “审计主机”、“进行安全审计”、“检查主机安全性”

`bash scripts/host_audit.sh` 或 `bash scripts/host_audit.sh --deep`

**审计内容：**
- 可疑的 cron 任务（使用 curl 或其他命令进行攻击）、base64 编码、反向 shell 模式。
- 最近修改的系统文件（深度扫描）。
- SSH 密钥审计（过多密钥、无注释的密钥、root 用户登录权限）。
- 敏感文件的权限设置（如 `/etc/passwd` 可被全局读取）。
- ClamAV 签名更新情况。

**输出：** 安全性评分（0-100 分）及详细问题报告。

### 代理行为监控

**触发条件：** “检查代理完整性”、“监控代理状态”、“代理是否被入侵”

`bash scripts/monitor_agent.sh`

**审计内容：**
- `AGENTS.md`、`SOUL.md`、`MEMORY.md`、`TOOLS.md`、`USER.md` 文件的最近修改记录。
- 内存文件的变化（修改超过 10 个文件可能表示异常）。
- 异常的 cron 任务（非 `clawguard/freshclam/standard` 维护命令）。
- 可疑的出站连接（如 IRC 端口、后门端口、Tor）。
- 在 workspace 外创建的文件（如 `/tmp` 目录下的可执行文件、用户主目录的更改）。
- 异常进程（如 xmrig、nc -l、ncat、socat、chisel）。
- 高负载的 CPU 进程（可能表示挖矿行为）。
- 敏感文件的暴露（如 `.env` 文件、可被全局读取的 SSH 密钥）。

**输出：** 代理状态（正常/存在警告/被入侵迹象）及详细问题报告。

### 安全报告生成

**触发条件：** “生成安全报告”、“生成威胁报告”、“生成态势报告”

`bash scripts/generate_report.sh` 或 `bash scripts/generate_report.sh --days 30 --output report.md`

该脚本会将所有最近的扫描结果整合成 Markdown 格式的安全报告，内容包括：
- 扫描总结（总文件数、安全文件数、检测到的威胁、错误信息）。
- 威胁详情（包括文件路径和采取的措施）。
- 安全性评分（用表情符号表示）。
- 建议（如缺少哪些工具、需要安排的扫描任务）。

## 自动定时扫描

定时扫描任务在上面的 **设置（首次运行）** 部分中有详细说明。首次安装后请立即使用 OpenClaw 的 cron 工具创建这些任务。

要验证所有 cron 任务是否配置正确，请运行 `bash scripts/check_crons.sh`。

## 错误阳性处理

ClamAV 的错误阳性率较高。处理策略如下：
1. **如果仅 ClamAV 检测到威胁且来源已知安全，则很可能是误报。** 记录并忽略该结果。
2. **如果 ClamAV 检测到威胁且来源未知，则将文件隔离并进一步调查。**
3. **如果 ClamAV 检测到威胁且技能审计也发现了问题，则确认为真实威胁。** 立即将文件隔离。

**处理误报的方法：**
- 向 ClamAV 提交报告：https://www.clamav.net/reports/fp
- 将误报记录在扫描日志中以供后续参考。

## 隔离流程

**隔离位置：** `$CRUSTY_QUARANTINE`（默认为 `/tmp/crusty_quarantine`）
**隔离记录：** `manifest.json` 文件会记录文件的原始路径和修改时间。

**注意：** **切勿使用 `clamscan --remove` 命令直接删除文件。** 必须先隔离文件，再进行验证后再删除。

## 离线模式

Crusty Security 在离线模式下仍能提供基本的安全保护功能：
- ✅ 支持 ClamAV 扫描（使用本地签名库）。
- ✅ 支持技能审计（进行静态分析，无需网络连接）。
- ✅ 支持主机审计（本地检查）。
- ✅ 支持代理监控（本地检查）。
- **注意：** 在离线模式下，ClamAV 的签名库可能不是最新的（请在主机审计时检查签名库的更新情况）。

## 资源受限环境（如 Raspberry Pi）

- 对于内存小于 2GB 的主机：
  - `install_clamav.sh` 会自动检测内存不足并跳过守护进程模式。
  - 使用 `clamscan`（按需扫描）代替 `clamd`。
 - 使用 `--incremental` 选项进行增量扫描以减少扫描时间。
  - 技能审计和代理监控对系统资源的需求较低。

- 对于内存小于 1GB 的主机：
  - 可以选择不使用 ClamAV。
  - 仅使用技能审计和代理监控功能。
  - 这些工具主要基于 shell 和 Python 编写，对系统资源的需求很低。

## 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `CRUSTY_API_KEY` | （无） | 仪表板 API 密钥（格式为 `cg_live_...`） |
| `CRUSTY_DASHBOARD_URL` | `https://crustysecurity.com` | 仪表板地址 |
| `CRUSTY_QUARANTINE` | `/tmp/crusty_quarantine` | 隔离目录 |
| `CRUSTY_LOG_DIR` | `/tmp/crusty_logs` | 扫描日志目录 |
| `CRUSTY_MAX_FILE_SIZE` | `200M` | 最大文件扫描大小 |
| `CRUSTY_WORKSPACE` | 自动检测 | 代理的工作空间路径 |

> **兼容性说明：** `CLAWGUARD_*` 环境变量仍然可用，但已不建议使用。建议使用 `CRUSTY_*` 变量。

## 事件响应

当确认存在真实威胁时，请参考 `references/remediation.md` 以获取完整的应对措施。简要步骤如下：
1. **立即隔离** 相关文件。
2. **评估影响范围**：文件是否已被执行？是否修改了其他文件？
3. **检查持久化风险**：检查是否存在 cron 任务、SSH 密钥、shell 配置、systemd 服务。
4. **检查数据泄露情况**：检查是否有数据被泄露（如出站连接、DNS 查询、API 密钥的使用）。
5. **更新凭证**：如果凭证可能已被泄露，请立即更新。
6. **进行全面扫描**：`bash scripts/scan_file.sh -r /`
7. **记录事件**：详细记录整个事件过程。