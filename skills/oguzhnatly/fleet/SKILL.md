---
name: fleet
type: installable-cli
install: "clawhub install fleet"
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - python3
        - curl
    optionalBins:
      - gh
    install:
      - id: clawhub
        kind: clawhub
        slug: fleet
        label: "Install fleet via ClawHub"
description: "OpenClaw的多代理舰队管理命令行界面（CLI）：该工具作为协调代理，用于监控代理网关、调度任务以及观察整个代理舰队。所有操作仅限于本地环境（使用环回网络），同时支持明确指定的外部端点。安装前需获得操作员的许可。"
triggers: "check agents, fleet status, run sitrep, health check, dispatch task, send task to agent, steer agent, watch agent, parallel tasks, kill agent, fleet log, backup config, show agents, fleet report, how many agents online, CI status, what skills installed, trust score, which agent is reliable, fleet trust, fleet score, agent reliability, who should I assign, best agent for task"
requires:
  binaries:
    - bash>=4.0
    - python3>=3.10
    - curl
  optionalBinaries:
    - gh
envVars:
  optional:
    - name: FLEET_CONFIG
      description: "Override path to fleet config (default: ~/.fleet/config.json)"
    - name: FLEET_LOG
      description: "Override dispatch log path (default: ~/.fleet/log.jsonl)"
    - name: FLEET_STATE_DIR
      description: "Override state directory (default: ~/.fleet/state)"
    - name: FLEET_TRUST_WINDOW_HOURS
      description: "Override trust scoring window in hours (default: 72)"
    - name: FLEET_NO_UPDATE_CHECK
      description: "Set to 1 to disable background GitHub update check entirely"
    - name: LINEAR_API_KEY
      description: "Linear API key for CI ticket integration (optional, referenced in examples/solo-empire/config.json)"
    - name: NO_COLOR
      description: "Disable colored output"
installSpec:
  method: clawhub
  command: "clawhub install fleet"
  manual: "git clone https://github.com/oguzhnatly/fleet.git && fleet/bin/fleet init"
  initRequired: true
  initWrites:
    - "~/.fleet/config.json (chmod 600 immediately on creation, stores agent tokens in plaintext)"
    - "~/.local/bin/fleet (symlink to binary)"
    - "~/.bashrc or ~/.zshrc or ~/.profile (PATH export appended only if ~/.local/bin not already present)"
  initReads:
    - "~/.openclaw/openclaw.json (read-only, one-time workspace path detection)"
    - "127.0.0.1:40000-50000 (loopback port scan, one-time gateway discovery)"
  skipInit: "Clone repo, create ~/.fleet/config.json from templates/configs/minimal.json, add bin/ to PATH manually. No automatic writes."
updateSpec:
  command: "fleet update"
  source: "api.github.com/repos/oguzhnatly/fleet/releases/latest"
  verification: "SHA256 verified against fleet.sha256 published with each release. Extraction halts on mismatch."
  backgroundCheck: "Once per 24h, non-blocking. Disable with FLEET_NO_UPDATE_CHECK=1"
permissions:
  reads:
    - "~/.fleet/ (config, state, logs, backups created by fleet itself)"
    - "~/.openclaw/openclaw.json (read-only, fleet init only, workspace path detection)"
    - "~/.openclaw*/agents/*/sessions/<fleet-session-id>.jsonl (fleet watch: only fleet-named sessions)"
    - "/proc/meminfo (Linux only, fleet sitrep)"
  writes:
    - "~/.fleet/ (all fleet-created data)"
    - "~/.local/bin/fleet (symlink, fleet init)"
    - "~/.bashrc or ~/.zshrc or ~/.profile (PATH export, fleet init, only if not already present)"
  network:
    - "127.0.0.1:<agent-ports> (loopback only, operator config)"
    - "api.github.com/repos/<operator-repos>/actions/runs (fleet ci, operator gh CLI auth)"
    - "api.github.com/repos/oguzhnatly/fleet/releases/latest (background update check, 24h cache)"
    - "Operator-configured endpoint URLs (fleet health only)"
sensitive:
  storedPlaintext:
    - "~/.fleet/config.json: agent gateway auth tokens"
  hardening: "chmod 600 applied automatically by fleet init. Documented in SECURITY.md."
agentScope:
  permitted:
    - "Run fleet commands within operator-configured scope"
    - "Run fleet init to create config and link binary"
    - "Run fleet update after operator explicitly requests it"
  notPermitted:
    - "Implement fleet functionality by other means if fleet commands fail"
    - "Autonomously run system package managers (apt-get, brew, dnf, apk, etc.) to install dependencies"
    - "Run any command requiring root or sudo without explicit operator instruction in the current conversation"
    - "Read session files fleet did not create"
    - "Scan addresses outside operator config"
    - "Modify OpenClaw config files"
    - "Run commands outside fleet management"
---
# 舰队：多智能体舰队管理

## 目的、权限与信任

**适用对象：** 由操作员（负责设置和运行 OpenClaw 舰队的用户）明确配置的协调 AI 智能体。操作员有意安装此技能，因为该技能能够实现自主舰队管理。

**这里的“授权”意味着什么：** 安装此技能即表示操作员同意以下所有操作。该技能仅会与操作员自己的智能体网关（回环地址）、通过其认证的 `gh CLI` 访问操作员的 GitHub 仓库，以及定期（每 24 小时一次）从 `api.github.com` 获取舰队更新信息。它不会超出安装用户的权限范围，也不会对操作员已控制的本地舰队之外的任何内容进行操作。

**为什么某些操作看起来具有侵入性：** 该技能是为 AI 协调智能体设计的，而非供最终用户手动操作。协调智能体对舰队有完整的了解，因此在设置步骤中请求确认会中断其工作。操作员安装此技能正是为了实现自主运行。列出的每个具有侵入性的操作都有具体的操作目的。

**此技能绝对不会做什么（硬性限制）：**
- 未经操作员明确指示，绝不会安装需要 `root` 或 `sudo` 权限的软件
- 绝不会修改安装用户 `~/.fleet/`、`~/.local/bin/` 目录以及 shell 配置文件（`~/.bashrc`、`~/.zshrc`、`~/.profile`）之外的文件
- 除了以下情况外，绝不会连接外部服务：(1) 操作员配置的回环网关；(2) 用于健康检查的操作员配置的端点 URL；(3) 通过其认证的 `gh CLI` 访问操作员的 GitHub 仓库以获取持续集成（CI）状态；(4) 通过 `api.github.com/repos/oguzhnatly/fleet/releases/latest` 进行后台更新检查（有文档记录，非阻塞式，每 24 小时一次，可通过设置 `FLEET_NO_UPDATE_CHECK=1` 禁用）
- 绝不会泄露配置信息、令牌或会话数据
- 未经操作员明确指示，绝不会修改 OpenClaw 的配置
- 绝不会在操作员未安装它的系统上运行
- 绝不会删除或覆盖非自身创建的数据（如舰队配置文件、状态文件）
- 绝不会执行与舰队管理或依赖项设置无关的命令

**信任边界：** 所有操作都在本地进行。舰队仅与 `127.0.0.1`（回环地址）通信，以连接到操作员自己的智能体网关。外部调用仅限于 GitHub API（通过操作员的认证 `gh` CLI）和操作员配置的健康检查端点 URL。

---

### CLI 工具包
用于管理、调度和观察 OpenClaw 智能体网关的舰队。协调智能体使用该工具包来监控员工、分配任务、指导正在运行的会话、查看实时输出以及审查调度历史记录。

## 安全模型
舰队在一个严格定义的信任边界内运行。本节对此进行了明确说明，以便任何安全扫描器、审核员或操作员都可以验证其范围。

### 网络范围
舰队仅建立以下 HTTP 连接：
1. `127.0.0.1` 回环端口：操作员自己的智能体网关（在 `~/.fleet/config.json` 中配置）
2. GitHub API：通过操作员的认证 `gh` CLI 会话，仅用于读取操作员明确列出的仓库的 CI 状态
3. `endpoints[]` 中的 URL：用于根据操作员配置的 URL 进行健康检查

舰队从不开放监听端口，从不接受传入连接，也从不主动连接到操作员配置之外的任何地址。

### 文件系统范围
舰队仅读取和写入以下文件：
- `~/.fleet/`：舰队配置、状态、日志、备份（均由舰队自身创建）
- `~/.local/bin/fleet`：指向舰队二进制文件的符号链接（由 `fleet init` 创建，位于标准的 XDG 路径）
- Shell 配置文件（`~/.bashrc`、`~/.zshrc`、`~/.profile`）：仅在 `PATH` 中尚未包含 `~/.local/bin` 时，才会添加 `export PATH="$HOME/.local/bin:$PATH"`
- 会话输出（用于 `fleet watch`）：读取舰队为指定智能体创建的 `~/.openclaw*/agents/*/sessions/<fleet-session-id>.jsonl` 文件。该文件可能包含该智能体会话的对话记录。舰队不会读取它未创建的会话、其他用户的会话或协调智能体的主会话（除非明确传递了 `--all` 标志）。

舰队从不读取或写入安装用户主目录之外的文件。舰队也不会访问它未创建的会话。在 `fleet init` 期间，舰队会读取 `~/.openclaw/openclaw.json` 以自动检测工作区路径（仅读，不会写入）。舰队不会修改 OpenClaw 的配置文件。

### 凭据范围
舰队仅从 `~/.fleet/config.json` 读取认证令牌。这些令牌属于操作员自己的智能体，并以明文形式存储在该文件中。舰队绝不会将它们传输到回环网络之外。舰队也不会读取其他凭证存储（如 ssh 密钥、云凭证、浏览器存储或操作系统密钥链）。建议的加固措施：`chmod 600 ~/.fleet/config.json`。

### 权限范围
舰队绝不会调用 `sudo`。舰队也不会请求提升权限。所有需要系统级包管理器（如 `apt-get`、`brew`）的安装命令都会以当前用户身份运行，并在上面的兼容性脚本中明确列出。

---

## 快速参考

| 情况 | 操作 |
|-----------|--------|
| 向智能体发送任务 | `fleet task coder "add pagination to /api/spots"` |
| 查看智能体的操作情况 | `fleet watch coder` |
| 查看协调智能体的操作情况 | `fleet watch coordinator` |
| 在任务进行中发送纠正指令 | `fleet steer coder "also add rate limiting"` |
| 停止智能体的当前任务 | `fleet kill coder` |
| 查看所有最近的调度和结果 | `fleet log` |
| 将任务分解到多个智能体 | `fleet parallel "<task>" --dry-run`（先制定计划，根据信任度选择智能体） |
| 检查所有智能体是否存活 | `fleet agents` |
| 发现异常需要全面了解情况 | `fleet sitrep` |
| 快速健康检查 | `fleet health` |
| 检查所有仓库的持续集成状态 | `fleet ci` |
| 查看哪些智能体最可靠 | `fleet trust` |
| 详细检查某个智能体的可靠性 | `fleet score coder` |
| 检查特定类型的任务可靠性 | `fleet score coder --type code` |
| 检查特定仓库的持续集成状态 | `fleet ci <name>` |
| 查看安装了哪些技能 | `fleet skills` |
| 在更改前备份所有内容 | `fleet backup` |
| 在出现问题后恢复 | `fleet restore` |
| 首次设置 | `fleet init` |
| 用户询问“舰队运行情况如何？” | `fleet agents`（提供总结） |
| 用户询问“发生了什么变化？” | `fleet sitrep`（报告变化） |
| 定时生成每日报告 | `fleet sitrep 12`（通过 cron） |
| 部署前 | `fleet health` + `fleet ci` |

## 自动设置
**目的：** 这些步骤确保舰队二进制文件在首次运行时可用。它们仅修改安装用户已拥有的文件。不需要也不使用 `root` 权限。

**修改的内容：** 调整舰队二进制文件的执行权限，在 `~/.local/bin/` 目录中创建符号链接（标准的用户本地二进制目录路径），以及如果 `~/.local/bin` 不在 `PATH` 中，则修改用户 shell 配置文件中的 `PATH`。

**为什么默认不显示确认提示：** 操作员特意安装此技能是为了让协调智能体自主处理设置。对自动设置的同意是在安装时给出的。

**明确的退出选项：** 如果操作员没有明确授权自动设置（例如，在全面部署前评估该技能），请在此处停止并在此之前询问操作员。需要询问的问题是：“Fleet 需要将其二进制文件链接到 `~/.local/bin/fleet` 并可能向您的 shell 配置文件中添加 `PATH` 导出。可以吗？”

**Shell 配置文件修改规则：** 仅当 `~/.local/bin` 不在 `PATH` 中时，才添加 `PATH` 导出。首先使用 `echo $PATH | grep -q "$HOME/.local/bin"` 进行检查。如果已经存在，则完全跳过配置文件修改。

`fleet init` 会自动检测正在运行的网关（通过扫描操作员舰队使用的回环端口），从现有的 OpenClaw 配置中获取工作区路径，创建 `~/.fleet/config.json`，创建二进制文件的符号链接，并仅在 `PATH` 中尚未包含 `~/.local/bin` 时将其添加到 shell 配置文件中。所有更改都限制在安装用户的主目录范围内。

### 通过 ClawHub 设置
### 手动设置
### 手动配置

## 配置
Fleet 读取 `~/.fleet/config.json`。可以自动生成或手动创建。

### 自动检测设置
### 手动配置
创建 `~/.fleet/config.json`：

### 配置参考
| 字段 | 类型 | 是否必需 | 描述 |
|-------|------|----------|-------------|
| `workspace` | 字符串 | 是 | 主工作区目录的路径 |
| `gateway.port` | 数字 | 是 | 主协调智能体网关的端口 |
| `gateway.name` | 字符串 | 否 | 显示名称（默认：“coordinator”） |
| `gateway.role` | 字符串 | 否 | 角色描述 |
| `gateway.model` | 字符串 | 否 | 模型标识符 |
| `agents[]` | 数组 | 否 | 员工智能体网关 |
| `agents[].name` | 字符串 | 是 | 唯一的智能体标识符 |
| `agents[].port` | 数字 | 是 | 网关端口编号 |
| `agents[].role` | 字符串 | 否 | 该智能体的角色 |
| `agents[].model` | 字符串 | 否 | 使用的模型 |
| `agents[].token` | 字符串 | 否 | API 调用的认证令牌 |
| `endpoints[]` | 数组 | 否 | 健康检查的 URL |
| `endpoints[].name` | 字符串 | 是 | 显示名称 |
| `endpoints[].url` | 字符串 | 是 | 完整的检查 URL |
| `endpoints[].expectedStatus` | 数字 | 否 | 预期的 HTTP 状态码（默认：200） |
| `endpoints[].timeout` | 数字 | 否 | 超时时间（默认：6 秒） |
| `repos[]` | 数组 | 否 | 用于持续集成的 GitHub 仓库 |
| `repos[].name` | 字符串 | 是 | 显示名称 |
| `repos[].repo` | 字符串 | GitHub 仓库的格式 |
| `services[]` | 数组 | 否 | 需要检查的系统守护进程名称 |
| `linear.teams[]` | 数组 | 否 | 票务计数的线性团队键 |
| `linear.apiKeyEnv` | 字符串 | 否 | API 密钥的环境变量名 |
| `skillsDir` | 字符串 | 否 | ClawHub 技能目录的路径 |

### 环境变量
| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `FLEET_CONFIG` | 配置文件的路径 | `~/.fleet/config.json` |
| `FLEET_WORKSPACE` | 覆盖工作区路径 | 配置 `workspace` 的值 |
| `FLEET_STATE_DIR` | 状态持久化目录 | `~/.fleet/state` |
| `NO_COLOR` | 禁用彩色输出（设置时） | （未设置） |

## 命令：详细参考

### `fleet task <agent> "<prompt>"`
向指定的智能体发送任务并实时流式显示响应。

**要求：** `~/.fleet/config.json` 中的 `agents[].token` 中包含智能体令牌。

**选项：**
- `--type code` | `review` | `research` | `deploy` | `qa`：覆盖任务类型（如果省略，则从提示中自动推断）
- `--timeout <minutes>` | 响应超时（默认：30 秒）
- `--no-wait`：立即执行并忽略结果

**输出：**
### `fleet steer <agent> "<message>"`
向正在执行任务的智能体发送会话中的纠正指令。该指令会路由到与 `fleet task` 相同的会话中，因此智能体可以了解上下文。

**输出：**
### `fleet watch <agent> [--all]`
实时显示智能体的活动会话输出。轮询舰队为该智能体创建的会话文件，显示新到达的消息。

- 默认：查看 `fleet-{agent}` 会话（由 `fleet task` 创建的会话）
- `--all`：查看智能体的完整主会话
- `coordinator`：始终查看主协调智能体的会话

**输出：**
### `fleet kill <agent> [--force]`
向智能体的会话发送优雅的停止信号。智能体会确认并归档会话。并将该智能体的所有待处理日志条目标记为“已指导”。

### `fleet parallel "<task>" [--dry-run]`
按类型将高级任务分解为子任务，将每个子任务分配给合适的智能体，并同时调度。

**在执行前务必先使用 `--dry-run` 来查看分解计划。** 在实际调度前需要确认。

**`--dry-run` 的输出：**
### `fleet log [--agent <name>] [--outcome <status>] [--limit <n>] [--all]`
显示所有舰队任务的调度历史记录。可以根据智能体、结果和计数进行过滤。

**结果：`success`、`failure`、`timeout`、`steered`、`pending`

**输出：**
### `fleet trust [--window <hours>] [--json]`
显示所有配置智能体的信任矩阵，该矩阵根据以下公式计算得出：

- **quality_score**：每个任务结果的加权平均值。`success`=1.0，`steered`=0.5，`failure`/`timeout`=0.0。任务中的每次指导操作都会使分数降低最多 30%。
- `speed_multiplier`：如果平均任务持续时间 ≤5分钟，则为 1.0；超过 30分钟，则降至 0.5。
- **Recency**：窗口内的任务（默认 72小时）计分为 2倍；7天内的任务计分为 1倍；更旧的任务计分为 0.5倍。
- **Trend**：比较过去 7天与当前 7天的情况。`↑` 表示改进，`↓` 表示下降，`→` 表示稳定，`★` 表示新智能体。

**输出：**
### `fleet score [<agent>] [--window <hours>] [--type <task_type>]`
显示单个智能体的详细任务类型可靠性分解（或所有智能体的汇总表）。

**输出（单个智能体）：**
### `fleet score [<agent>] [--window <hours>] [--type <task_type>]`
### 跨验证（v3.5）**
对于代码或部署成功的智能体，`fleet score` 会检查每个任务是否在 1 小时内完成了 GitHub 持续集成（CI）运行。没有相应 CI 活动的任务会被标记为未验证。需要 `gh` CLI 和配置中的 `repos`。

**使用场景：** 当智能体的信任分数意外偏低或偏高时：`fleet score` 可以显示具体是哪些任务类型导致了这一结果。使用 `--type code` 可以仅查看代码相关的任务历史。

### `fleet health`
检查主网关和所有配置的端点以及系统守护进程。

**使用场景：** 快速操作检查，部署前，故障排除。

**输出：**
### `fleet agents`
显示所有配置的智能体网关的实时健康状态、响应时间和模型。

**使用场景：** 用户询问智能体情况，调试智能体问题，每日检查。

**输出：**
### `fleet sitrep [hours]`
旗舰命令。生成包含差异跟踪的结构化状态报告。

**使用场景：** 每日报告，定时 cron 任务，“发生了什么变化？”问题。

**参数：**
- `hours`：回顾周期（默认：4小时）。仅影响显示内容，差异始终与上次运行进行比较。

**检查内容：**
1. 所有智能体网关（在线/离线）
2. 所有配置仓库的持续集成状态
3. 所有配置端点的健康状况
4. 每个团队的线性票务计数
5. VPS 资源使用情况（内存、磁盘）

**差异跟踪：** 状态保存在 `~/.fleet/state/sitrep.json` 中。每次运行都会与上次运行进行比较，仅显示变化部分。

**输出：**
### `cron 集成示例：**
### `fleet ci [filter]`
显示所有配置仓库的 GitHub 持续集成状态，以及每个仓库的最后 3 次运行结果。

**使用场景：** 在推送之前，部署之后，调查故障。

**要求：** 必须安装并认证 `gh` CLI。

**参数：**
- `filter`：可选，按名称过滤仓库（不区分大小写）

**输出：**
### `fleet skills`
列出所有安装的 ClawHub 技能及其版本、描述和功能。

**使用场景：** 清点检查，“我能做什么？”，计划制定。

**输出：**
### `fleet backup`
备份 OpenClaw 配置、cron 作业、舰队配置和认证配置文件。

**使用场景：** 在进行重大更改之前，更新之前，作为安全措施。

**备份位置：`~/.fleet/backups/<timestamp>/`

### `fleet restore`
从最新备份中恢复。

**使用场景：** 在配置更改失败后，或者更新失败之后。

**注意：** 恢复后需要重启网关：`openclaw gateway restart`

### `fleet init`
交互式设置，自动检测正在运行的网关并创建初始配置。

**使用场景：** 首次设置，新机器，新舰队。

**自动检测：**
- 扫描常见的网关端口（48391，然后每隔 20 个端口扫描到 48600）
- 从 `~/.openclaw/openclaw.json` 中读取工作区路径
- 发现正在运行的员工智能体

### `fleet update`
自动升级命令。从 GitHub 获取最新版本并自动安装。

### `version banner`
当有新版本可用时，每个舰队命令会在输出前在标准错误输出（stderr）中打印一条警告信息：

### `fleet update`
GitHub 检查作为独立的后台进程每 24 小时运行一次，因此不会对正常舰队命令产生任何延迟影响。结果会缓存在 `~/.fleet/state/update_check.json` 中。

## 舰队模式
Fleet 支持多种组织架构。根据您的需求选择合适的模式：

### 单独帝国模式
一个协调者，2-5 名员工。最适合独立开发者和个人创始人。

### 开发团队模式
团队领导协调专业开发人员。最适合复杂产品。

### 研究实验室模式
专为知识工作设计的专用智能体。最适合内容分析和研究工作。

### 请参阅仓库中的 `examples/`，其中包含每种模式的即用配置文件。

## 故障排除

### 常见问题
| 问题 | 原因 | 解决方法 |
|---------|-------|-----|
| `fleet: command not found` | 未在 PATH 中 | 使用 `ln -sf path/to/fleet/bin/fleet ~/.local/bin/fleet` |
| `No config found` | 配置文件缺失 | 运行 `fleet init` 或创建 `~/.fleet/config.json` |
| 所有智能体显示“unreachable” | 智能体未运行 | 先启动智能体网关 |
| CI 显示“error” | `gh` 未认证 | 运行 `gh auth login` |
| SITREP 显示“first run” | 没有之前的状态 | 首次运行时正常，第二次运行时会显示差异 |
| 智能体显示“auth failed” | 配置中的令牌错误 | 更新配置中的令牌以匹配智能体的认证信息 |

### 调试

### 架构
Fleet 是模块化的。每个组件都有单一的功能：

### 添加新命令：
创建 `lib/commands/yourcommand.sh`，定义 `cmd_yourcommand()`，然后在 `bin/fleet` 中添加相应的处理逻辑。

## 与其他技能的集成
### 与 `ontology` 技能集成
如果安装了 `ontology` 技能，Fleet 可以查询知识图谱：

### 与 `self-improving-agent` 技能集成
将舰队运行中的学习内容记录到 `.learnings/` 文件中：
- 智能体停机模式 → `ERRORS.md`
- 持续集成失败模式 → `LEARNINGS.md`
- 配置改进 → 提交到 `TOOLS.md`

## 依赖项安装
Fleet 需要以下三个组件：**bash 4+**、**python3 3.10+** 和 **curl**。以下是针对不同平台的完整安装指南。安装缺失的依赖项后，运行 `fleet init`。

**操作员需要执行的操作：** 本节中的命令由操作员手动执行，而不是由智能体自动执行。智能体不得代表操作员运行系统包管理器。如果缺少依赖项，智能体会报告问题，操作员需要使用相应的命令进行安装。

**如果需要 `root` 权限（例如，在某些系统中需要 `apt-get`）：** 命令会明确显示。如果无法使用 `root` 权限，建议使用用户级别的安装方式（`--user`、`pyenv`、`$HOME/.local`）。

### 第 1 步：检查您已有的环境
### 第 2 步：安装缺失的依赖项

#### bash 4+
| 平台 | 命令 |
|----------|---------|
| **macOS**（预装 bash 3.2） | `brew install bash`：然后舰队会自动检测 `/opt/homebrew/bin/bash` 并通过 `#!/usr/bin/env bash` 设置 |
| **Ubuntu/Debian** | `sudo apt-get update && sudo apt-get install -y bash`（通常已安装 5.x） |
| **Alpine** | `apk add bash`（Alpine 默认使用 busybox ash） |
| **RHEL/CentOS/Fedora** | `sudo dnf install bash` 或 `sudo yum install bash` |
| **Arch** | `sudo pacman -S bash` |
| **FreeBSD** | `pkg install bash` |
| **Windows (WSL)** | WSL 中已包含 bash。如果使用 Git Bash，则已安装 bash 4+ |
| **Docker (minimal images)** | `RUN apk add --no-cache bash python3 curl`（Alpine）或 `RUN apt-get update && apt-get install -y bash python3 curl`（Debian） |
| **无法使用 `root` 权限** | 下载 bash 源代码，然后在本地编译：`./configure --prefix=$HOME/.local && make && make install`：之后设置 `export PATH="$HOME/.local/bin:$PATH` |
| **NixOS** | `nix-env -iA nixpkgs.bash` |

**在 macOS 上安装完成后：** 使用 `which bash` 确认是否安装了 Homebrew bash（在 Apple Silicon 上为 `/opt/homebrew/bin/bash`，在 Intel 上为 `/usr/local/bin/bash`）。`#!/usr/bin/env bash` 会选择 `PATH` 中最早的 `bash` 版本。**

#### python3 3.10+
| 平台 | 命令 |
|----------|---------|
| **macOS** | `brew install python@3.12` |
| **Ubuntu/Debian** | `sudo apt-get install -y python3` |
| **Alpine** | `apk add python3` |
| **RHEL/CentOS** | `sudo dnf install python3` |
| **Arch** | `sudo pacman -S python` |
| **无法使用 `root` 权限** | 使用 `pyenv`：`curl https://pyenv.run \| bash && pyenv install 3.12 && pyenv global 3.12` |

**Fleet 仅使用 python3 进行 JSON 解析**。不需要 `pip` 包或虚拟环境。**

#### curl
| 平台 | 命令 |
|----------|---------|
| **几乎所有平台** | 预装。使用 `curl --version` 进行检查 |
| **Alpine** | `apk add curl` |
| **Minimal Docker** | `apt-get install -y curl` 或 `apk add curl` |

#### gh CLI（可选，用于 `fleet ci`）
| 平台 | 命令 |
|----------|---------|
| **macOS** | `brew install gh` |
| **Ubuntu/Debian** | 查看 [cli.github.com/packages](https://cli.github.com/packages) |
| **其他平台** | `conda install gh --channel conda-forge` |

如果 `gh` 无法安装，`fleet ci` 会显示警告，但其他命令仍可正常使用。不要因为 `gh` 未安装而阻止舰队设置。

### 第 3 步：如果确实无法安装 bash 4+**
这种情况应该很少见，但如果您在无法安装 bash 4+ 的受限系统中：
1. **尝试使用 bash 3.2 运行。** 虽然 Fleet 的版本检查会拒绝，但大多数命令仍然可以使用 POSIX 兼容的功能。`bin/fleet` 文件中的第 10-22 行仅用于显示有用的错误信息，并不影响命令的实际运行。如果这些行不起作用，请报告问题。
2. **报告兼容性问题。** 如果由于 bash 版本或依赖项缺失导致 Fleet 无法运行，请向操作员报告具体的错误信息以及 `bash --version`、`python3 --version` 和 `curl --version` 的输出。请操作员使用第 2 步中的平台指南安装缺失的依赖项。不要尝试通过其他方式复制 Fleet 的功能。

**注意：** `bin/fleet` 文件中唯一需要编辑的部分是版本检查部分（第 10-22 行）。这些行仅用于显示有用的错误信息，其他部分都是用于实现命令逻辑的，不应进行修改。

### 第 4 步：在没有所需依赖项的环境中
如果当前环境中无法安装 bash 4+、python3 3.10+ 和 curl，则 Fleet 无法运行。请向操作员报告缺失的依赖项，并请求他们提供一个支持这些依赖项的环境。不要尝试通过其他方式复制 Fleet 的功能。

## 最佳实践
1. **在每日早晨的 cron 任务中运行 `fleet sitrep`：** 在问题升级之前发现夜间出现的问题。
2. **在更新网关配置之前运行 `fleet backup`：** 以便在出现问题时可以轻松恢复。
3. **在部署之前使用 `fleet health`：** 确保一切正常。
4. **在配置更改后运行 `fleet agents`：** 确认所有智能体是否已重新上线。
5. **使用 `fleet ci` 时按仓库过滤结果：** 在调试特定服务时避免干扰。
6. **将令牌保存在配置文件中，将密钥保存在环境变量中：** 令牌是本地存储的，API 密钥属于敏感信息。