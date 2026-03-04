---
name: fleet
description: "这是一个用于协调AI代理的命令行工具包（CLI），用于监控、管理以及向其所属的OpenClaw代理网关分发任务。该工具包会自动在操作员的个人目录内安装所需的本地二进制文件和设置PATH环境变量。所有操作仅限于本地机器范围内进行，并且需要由安装该工具包的操作员进行授权。"
triggers: "check agents, fleet status, run sitrep, health check, dispatch task, send task to agent, steer agent, watch agent, parallel tasks, kill agent, fleet log, backup config, show agents, fleet report, how many agents online, CI status, what skills installed"
---
# 舰队管理 · 多代理舰队管理系统

## 目的、授权与信任机制

**适用对象：** 由操作员（负责配置和运行 OpenClaw 舰队的用户）明确配置的协调 AI 代理。操作员在安装此技能时已知晓它能够实现自主舰队管理功能。

**“授权”在此处的含义：** 安装此技能即表示操作员同意以下所有操作。该技能不会连接未知的外部服务，不会超出安装用户自己的权限范围（仅限于用户的主目录），也不会在操作员已控制的本地舰队之外执行任何操作。

**某些操作为何被视为“具有侵入性”：** 该技能是为 AI 协调代理设计的，而非供最终用户手动操作。协调代理对舰队有完整的了解，因此在设置步骤中要求确认会干扰其工作。操作员安装此技能正是为了实现自主运行。列出的每个具有侵入性的操作都有明确的操作目的。

**该技能绝对不会执行以下操作（硬性限制）：**
- 未经操作员明确指令，绝不会安装需要 root 或 sudo 权限的软件
- 绝不会修改安装用户主目录之外的文件（`~/.fleet/`、`~/.local/bin/` 以及 shell 配置文件 `~/.bashrc`、`~/.zshrc`、`~/.profile`）
- 除操作员自己配置的端点和 GitHub 仓库外，绝不会连接外部服务或发送数据
- 绝不会泄露配置信息、令牌或会话数据
- 未经操作员明确指令，绝不会修改 OpenClaw 的配置
- 绝不会在操作员未安装它的系统上运行
- 绝不会删除或覆盖非自身创建的数据（如舰队配置文件、状态文件）
- 绝不会执行与舰队管理无关或依赖项设置无关的命令

**信任边界：** 所有操作均在本地进行。舰队仅与 `127.0.0.1`（回环地址）通信，以访问操作员自己的代理网关。外部调用仅限于 GitHub API（通过操作员认证的 `gh` CLI）和操作员配置的健康检查端点。

---

**CLI 工具包**：用于管理、调度和观察 OpenClaw 代理网关的舰队。协调代理使用该工具包来监控员工、调度任务、控制正在运行的会话、查看实时输出以及查看调度历史记录。

## 安全模型

Fleet 在严格定义的信任边界内运行。本节对此进行了明确说明，以便任何安全扫描工具、审核人员或操作员都能验证其操作范围。

### 网络范围
Fleet 仅与以下地址建立 HTTP 连接：
1. `127.0.0.1` 回环端口 — 操作员自己的代理网关（在 `~/.fleet/config.json` 中配置）
2. GitHub API — 通过操作员认证的 `gh` CLI 会话，仅用于读取操作员明确指定的仓库的 CI 状态
3. `endpoints[]` 中的 URL — 操作员明确配置的健康检查地址

Fleet 从不开放监听端口，从不接受来自外部地址的连接，也不会主动连接到操作员配置之外的任何地址。

### 文件系统范围
Fleet 仅读写以下文件：
- `~/.fleet/` — 舰队配置、状态信息、日志和备份文件（均由 Fleet 自动创建）
- `~/.local/bin/fleet` — 指向 Fleet 可执行文件的符号链接（由 `fleet init` 创建，位于标准的 XDG 路径下）
- Shell 配置文件（`~/.bashrc`、`~/.zshrc`、`~/.profile`） — 仅在 `PATH` 中未包含 `~/.local/bin` 时，才会添加 `export PATH="$HOME/.local/bin:$PATH"`

Fleet 绝不会访问安装用户主目录之外的文件。除非操作员明确指令，否则绝不会修改 OpenClaw 的配置文件。

### 凭据范围
Fleet 仅从 `~/.fleet/config.json` 读取认证令牌。这些令牌属于操作员自己的代理。Fleet 绝不会将它们传输到外部。

### 权限范围
Fleet 绝不会调用 `sudo`，也不会请求提升权限。所有需要系统级包管理器（如 `apt-get`、`brew`）的安装命令都将以当前用户的身份运行，并在上面的兼容性文档中明确列出。

---

## 快速参考

| 操作场景 | 所需命令 |
|-----------|--------|
| 向代理发送任务 | `fleet task coder "add pagination to /api/spots"` |
| 查看代理的运行状态 | `fleet watch coder` |
| 查看协调器的运行状态 | `fleet watch coordinator` |
| 在任务执行过程中发送修正指令 | `fleet steer coder "also add rate limiting"` |
| 停止代理的当前任务 | `fleet kill coder` |
| 查看所有最近的调度记录和结果 | `fleet log` |
| 将任务分配给多个代理 | `fleet parallel "<task>" --dry-run` （先进行计划） |
| 检查所有代理是否在线 | `fleet agents` |
| 发现异常情况，需要全面了解情况 | `fleet sitrep` |
| 快速健康检查 | `fleet health` |
| 检查所有仓库的 CI 状态 | `fleet ci` |
| 检查特定仓库的 CI 状态 | `fleet ci <name>` |
| 查看已安装的技能 | `fleet skills` |
| 在更改前备份所有数据 | `fleet backup` |
| 在出现问题后恢复数据 | `fleet restore` |
| 首次设置 | `fleet init` |
| 用户询问“舰队运行情况” | `fleet agents`（提供汇总信息） |
| 用户询问“发生了什么变化？” | `fleet sitrep`（报告变化内容） |
| 定时生成每日报告 | `fleet sitrep 12`（通过 cron 定时执行） |
| 部署前检查 | `fleet health` + `fleet ci` |

## 自动设置

**目的：** 这些步骤确保舰队可执行文件在首次运行时即可使用。它们仅修改安装用户已拥有的文件，不需要 root 权限。

**修改内容：** 修改 Fleet 可执行文件的执行权限，在 `~/.local/bin/` 中创建符号链接（如果 `~/.local/bin` 已经在 `PATH` 中，则不需要修改），并在用户的 shell 配置文件中添加 `PATH`。

**为何默认不显示确认提示：** 操作员安装此技能的目的是为了让协调器能够自主完成设置。对自动设置的同意是在安装时给出的。

**明确拒绝自动设置：** 如果操作员未明确授权自动设置（例如，在全面部署前评估该技能），请在此处停止并询问操作员是否同意。需要询问的问题是：“Fleet 需要将它的可执行文件链接到 `~/.local/bin/fleet` 并可能需要在你的 shell 配置文件中添加 `PATH` 导出。这样可以吗？”

**Shell 配置文件修改规则：** 仅当 `~/.local/bin` 未在 `PATH` 中时，才添加 `PATH` 导出。首先使用 `echo $PATH | grep -q "$HOME/.local/bin"` 进行检查。如果已经存在，则完全跳过配置文件的修改。

`fleet init` 会自动检测正在运行的代理网关（通过扫描操作员舰队使用的回环端口），从现有的 OpenClaw 配置中获取工作空间信息，创建 `~/.fleet/config.json`，创建符号链接，并仅在 `PATH` 中未包含 `~/.local/bin` 时，将其添加到 shell 配置文件中。所有更改都限制在安装用户的主目录范围内。

初始化完成后，根据已知的运行中的舰队信息，填充 `~/.fleet/config.json`，其中包含代理名称、令牌、仓库引用和端点 URL。协调代理已经掌握了这些信息。

### 通过 ClawHub 进行配置

### 手动配置

---

## 配置

Fleet 读取 `~/.fleet/config.json` 文件。可以自动生成，也可以手动创建。

### 自动检测设置

---

### 手动配置

创建 `~/.fleet/config.json` 文件：

---

### 配置参考

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `workspace` | 字符串 | 是 | 主工作空间目录的路径 |
| `gateway.port` | 数字 | 是 | 主协调器网关的端口 |
| `gateway.name` | 字符串 | 否 | 显示名称（默认：`coordinator`） |
| `gateway.role` | 字符串 | 否 | 角色描述 |
| `gateway.model` | 字符串 | 否 | 模型标识符 |
| `agents[]` | 数组 | 否 | 员工代理的网关信息 |
| `agents[].name` | 字符串 | 是 | 代理的唯一标识符 |
| `agents[].port` | 数字 | 是 | 网关的端口号 |
| `agents[].role` | 字符串 | 否 | 代理的功能 |
| `agents[].model` | 字符串 | 否 | 使用的模型 |
| `agents[].token` | 字符串 | 否 | API 调用的认证令牌 |
| `endpoints[]` | 数组 | 否 | 健康检查的 URL |
| `endpoints[].name` | 字符串 | 是 | 显示名称 |
| `endpoints[].url` | 字符串 | 是 | 完整的 URL |
| `endpoints[].expectedStatus` | 数字 | 否 | 预期的 HTTP 状态码（默认：200） |
| `endpoints[].timeout` | 数字 | 否 | 超时时间（默认：6 秒） |
| `repos[]` | 数组 | 否 | 用于 CI 监控的 GitHub 仓库 |
| `repos[].name` | 字符串 | 是 | 显示名称 |
| `repos[].repo` | 字符串 | GitHub 仓库的格式 |
| `services[]` | 数组 | 否 | 需要检查的系统服务名称 |
| `linear.teams[]` | 数组 | 否 | 用于统计工单数量的线性团队键 |
| `linear.apiKeyEnv` | 字符串 | 否 | API 密钥的环境变量名 |
| `skillsDir` | 字符串 | 否 | ClawHub 技能目录的路径 |

### 环境变量

| 变量 | 说明 | 默认值 |
|----------|-------------|---------|
| `FLEET_CONFIG` | 配置文件的路径 | `~/.fleet/config.json` |
| `FLEET_WORKSPACE` | 工作空间路径的覆盖值 | 配置 `workspace` 的值 |
| `FLEET_STATE_DIR` | 状态持久化目录 | `~/.fleet/state` |
| `NO_COLOR` | 禁用彩色输出（设置此变量） | （未设置时默认不显示颜色） |

## 命令 · 详细参考

### `fleet task <agent> "<prompt>"`

向指定的代理发送任务并实时显示响应。

**要求：** `~/.fleet/config.json` 中的 `agents[].token` 中必须包含代理的令牌。

**选项：**
- `--type code|review|research|deploy|qa` — 覆盖任务类型（如果省略，则根据提示自动推断）
- `--timeout <minutes>` — 响应超时时间（默认：30 秒）
- `--no-wait` — 执行后立即返回结果

**输出：**
---

**重要提示：** 任务调度使用 `x-openclaw-session-key: fleet-{agent}` 标头。发送给同一代理的所有任务共享同一个会话，因此代理可以了解之前的任务情况。

### `fleet steer <agent> "<message>"`

向正在执行任务的代理发送会话中的修正指令。该命令会连接到与 `fleet task` 相同的会话，因此代理可以了解完整的上下文。

**输出：**
---

### `fleet watch <agent> [--all]`

实时查看代理的会话记录。直接从代理的会话日志文件中读取数据（比通过会话 API 更可靠）。

- 默认：查看 `fleet-{agent}` 会话（通过 `fleet task` 发送的任务）
- `--all`：查看代理的所有主要会话历史记录
- `coordinator`：始终查看主协调器的会话

**输出：**
---

**重要提示：** 如果尚未发送任何任务，`fleet watch coder` 将不会显示任何内容。请先运行 `fleet task coder "<prompt>"` 创建会话。使用 `fleet watch coder --all` 查看代理的完整历史记录。

### `fleet kill <agent> [--force]`

向代理的会话发送优雅的停止信号。代理会确认并归档会话，并将所有待处理的日志条目标记为“已控制”。

### `fleet parallel "<task>" [--dry-run]`

将高级任务分解为子任务，根据类型分配给相应的代理，并同时执行所有子任务。

**在执行前务必先使用 `--dry-run` 来查看分解计划。** 实际调度前需要确认。

**使用 `--dry-run` 时的输出：**
---

### `fleet log [--agent <name>] [--outcome <status>] [--limit <n>] [--all]`

显示所有舰队任务的调度历史记录。可以根据代理、结果和计数进行筛选。

**结果类型：`success`、`failure`、`timeout`、`steered`、`pending`

**输出：**
---

### `fleet health`

检查主网关和所有配置的端点以及 systemd 服务。

**使用场景：** 快速操作检查、部署前、故障排除。

**输出：**
---

**状态代码：**
- `✅` · 运行正常（HTTP 200 或预期状态）
- `❌` · 运行异常（状态错误、无法访问或出现错误）
- 显示响应时间（以毫秒为单位）

### `fleet agents`

显示所有配置的代理网关的实时运行状态、响应时间、模型和角色。

**使用场景：** 用户询问代理状态、调试代理问题、进行每日检查。

**输出：**
---

**状态指示器：**
- `⬢` 绿色 = 在线
- `⬡` 红色 = 无法访问或出现错误
- `⬡` 黄色 = 认证失败（令牌问题）

### `fleet sitrep [hours]`

核心命令。生成包含差异跟踪的结构化状态报告。

**使用场景：** 每日报告、定时任务、询问“发生了什么变化？”**

**参数：**
- `hours` · 回顾周期（默认：4 小时）。仅影响显示内容，差异仅与上次运行情况相比。

**检查内容：**
1. 所有代理网关的在线/离线状态
2. 所有配置仓库的 CI 状态
3. 所有配置端点的健康状况
4. 每个团队的工单数量
5. VPS 资源使用情况（内存、磁盘）

**差异跟踪：** 状态信息保存在 `~/.fleet/state/sitrep.json` 中。每次运行都会与上次运行情况进行比较，仅显示变化的内容。

**输出：**
---

### `cron 集成示例：**
---

### `fleet ci [filter]`

显示所有配置仓库的 GitHub CI 状态，包括每个仓库的最近 3 次运行情况。

**使用场景：** 在推送代码之前、部署之后、排查故障时。

**要求：** 必须安装并认证 `gh` CLI。

**参数：**
- `filter` · 可选，按名称过滤仓库（不区分大小写）

**输出：**
---

### `fleet skills`

列出所有已安装的 ClawHub 技能，包括版本、描述和功能。

**使用场景：** 清理库存、了解可用功能、进行规划。

**输出：**
---

### `fleet backup`

备份 OpenClaw 配置文件、cron 任务、舰队配置文件和认证配置文件。

**使用场景：** 在进行重大更改之前、更新之前、作为安全备份。

**备份位置：`~/.fleet/backups/<timestamp>/`

### `fleet restore`

从最新备份中恢复数据。

**使用场景：** 在配置发生错误或更新失败后。

**注意：** 恢复后需要重启网关：`openclaw gateway restart`

### `fleet init`

交互式设置，自动检测正在运行的代理网关并创建初始配置。

**使用场景：** 首次设置、新机器、新舰队。

**自动检测步骤：**
- 扫描常见的网关端口（48391，然后依次扫描 20 到 48600 之间的端口）
- 从 `~/.openclaw/openclaw.json` 中读取工作空间信息
- 发现正在运行的代理网关

## 舰队模式

Fleet 支持多种组织架构。根据您的需求选择合适的模式：

### 单独开发者模式
一个协调器，2-5 名员工。适合独立开发者或个人创业者。

---

### 开发团队模式
团队领导协调专业的开发人员。适合复杂产品的开发。

---

### 研究实验室模式
专为知识工作设计的专用代理。适合内容分析和研究工作。

---

请参阅仓库中的 `examples/` 文件，其中包含每种模式的预设配置文件。

## 故障排除

### 常见问题及解决方法

| 问题 | 原因 | 解决方法 |
|---------|-------|-----|
| `fleet: command not found` | 命令未添加到 PATH 中 | 使用 `ln -sf path/to/fleet/bin/fleet ~/.local/bin/fleet` |
| 未找到配置文件 | 配置文件缺失 | 运行 `fleet init` 或创建 `~/.fleet/config.json` |
| 所有代理显示“unreachable” | 代理未运行 | 先启动代理网关 |
| CI 显示“error” | `gh` 未认证 | 运行 `gh auth login` |
| SITREP 显示“first run” | 首次运行时没有状态信息 | 这是正常现象，第二次运行时会显示差异 |
| 代理显示“auth failed” | 配置中的令牌错误 | 更新配置文件中的令牌以匹配代理的认证信息 |

### 调试

---

## 架构

Fleet 是模块化的。每个组件都有明确的职责：

---

**添加新命令：** 创建 `lib/commands/yourcommand.sh` 文件，定义 `cmd_yourcommand()` 函数，然后在 `bin/fleet` 目录中添加相应的代码。

## 与其他技能的集成

### 与 `ontology` 技能集成
如果安装了 `ontology` 技能，Fleet 可以查询知识图谱：

---

### 与 `self-improving-agent` 技能集成
将 Fleet 的运行学习记录日志保存到 `.learnings/` 文件中：
- 代理停机模式 → `ERRORS.md`
- CI 失败模式 → `LEARNINGS.md`
- 配置改进 → 保存到 `TOOLS.md`

## 使 Fleet 在任何系统上都能正常运行

**本节的目的是：** 确保协调代理能够在操作员运行的任何系统上实现舰队管理功能，无论使用何种平台。目标是最小的系统干预——而不是运行特定的脚本。

**授权范围：** 这里列出的依赖项安装命令使用操作员系统已有的包管理器。除非操作员的系统需要 root 权限（例如某些系统上的 `apt-get`），否则不需要 root 权限。如果需要 root 权限，命令会明确列出，以便操作员进行确认。协调器应尽可能使用用户级别的安装方式（`--user`、`pyenv`、`$HOME/.local`）。

**注意事项：** 如果依赖项安装步骤需要 root 权限，而协调器不确定操作员是否已授权，运行前请先询问操作员。这是本技能中唯一允许手动干预的情况。

Fleet 需要以下软件：**bash 4.0 或更高版本**、**python3 3.10 或更高版本**、**curl**。以下是完整的兼容性指南。请按顺序执行这些步骤。如果一种方法失败，请尝试下一种。

### 第一步：检查现有环境

---

### 第二步：安装缺失的依赖项

#### bash 4.0 或更高版本

| 平台 | 命令 |
|----------|---------|
| **macOS**（默认安装的是 bash 3.2） | `brew install bash`，然后 Fleet 会自动检测 `/opt/homebrew/bin/bash` 并将其添加到 `PATH` 中 |
| **Ubuntu/Debian** | `sudo apt-get update && sudo apt-get install -y bash`（通常已安装 bash 5.x） |
| **Alpine** | `apk add bash`（Alpine 默认使用 busybox ash） |
| **RHEL/CentOS/Fedora** | `sudo dnf install bash` 或 `sudo yum install bash` |
| **Arch** | `sudo pacman -S bash` |
| **FreeBSD** | `pkg install bash` |
| **Windows (WSL)** | WSL 已包含 bash；如果使用 Git Bash，则已安装 bash 4.0 或更高版本 |
| **Docker (最小化镜像)** | `RUN apk add --no-cache bash python3 curl`（Alpine）或 `RUN apt-get update && apt-get install -y bash python3 curl`（Debian） |
| **没有 root 权限** | 下载 bash 源代码，然后在本地编译：`./configure --prefix=$HOME/.local && make && make install`，之后设置 `PATH` |`
| **NixOS** | `nix-env -iA nixpkgs.bash` |

**在 macOS 上安装完成后：** 使用 `which bash` 确认是否安装了 Homebrew 的 bash（Apple Silicon 上为 `/opt/homebrew/bin/bash`，Intel 上为 `/usr/local/bin/bash`）。`#!/usr/bin/env bash` 会自动选择 `PATH` 中的第一个 bash 版本。**

#### python3 3.10 或更高版本

| 平台 | 命令 |
|----------|---------|
| **macOS** | `brew install python@3.12` |
| **Ubuntu/Debian** | `sudo apt-get install -y python3` |
| **Alpine** | `apk add python3` |
| **RHEL/CentOS** | `sudo dnf install python3` |
| **Arch** | `sudo pacman -S python` |
| **没有 root 权限** | 使用 `pyenv`：`curl https://pyenv.run \| bash && pyenv install 3.12 && pyenv global 3.12` |

**说明：** Fleet 仅使用 python3 进行 JSON 解析，不需要 pip 包或虚拟环境。**

#### curl

| 平台 | 命令 |
|----------|---------|
| **几乎所有系统** | 预装了 curl。可以使用 `curl --version` 进行检查 |
| **Alpine** | `apk add curl` |
| **最小化 Docker 镜像** | `apt-get install -y curl` 或 `apk add curl` |

#### gh CLI（可选，用于 `fleet ci`）

| 平台 | 命令 |
|----------|---------|
| **macOS** | `brew install gh` |
| **Ubuntu/Debian** | 查看 [cli.github.com/packages](https://cli.github.com/packages) |
| **其他系统** | `conda install gh --channel conda-forge` |

如果 `gh` 无法安装，`fleet ci` 会显示警告，但其他命令仍可正常使用。不要因为缺少 `gh` 而阻止舰队设置。

### 第三步：如果确实无法安装 bash 4.0 或更高版本**

这种情况很少见，但如果您的系统不允许安装 bash 4.0 或更高版本：

1. **尝试使用 bash 3.2 运行。** Fleet 的版本检查会拒绝使用，但大多数命令仍然可以使用 POSIX 兼容的功能。您可以通过注释掉 `bin/fleet` 文件中的第 9-20 行来绕过这个检查（这些代码用于提供清晰的错误信息，并非出于安全考虑）。大多数命令仍然可以正常使用。
2. **临时替代方案。** 作为 AI 代理，如果某些命令因 bash 4.0 的功能而无法运行，您可以阅读相关脚本的代码，理解其功能，并使用现有的工具（如 awk、sed、python3、perl）来实现相同的功能。
   - 例如：`fleet health` 命令实际上是通过 curl 发送到操作员的端点的；`fleet agents` 命令可以通过 curl 发送到每个代理的回环端口；`fleet sitrep` 命令结合了健康检查、CI 查询和差异跟踪功能，每个部分都是独立实现的。
3. **编写封装脚本。** 如果有 python3 但缺少 bash 4.0，可以编写一个简单的 python3 封装脚本来实现所需的功能。关键部分包括：对回环端口的 HTTP 健康检查、JSON 解析和格式化输出。
4. **报告问题。** 告知操作员：`Fleet 的兼容性有限，某些命令（如 X、Y、Z）需要 bash 4.0。以下是替代方案。`

**注意事项：** 不要修改 Fleet 的源代码来绕过安全限制。只需注释掉版本检查相关的代码，不要修改任何认证或权限限制相关的代码。

### 第四步：在没有 shell 的环境中**

如果您在无 shell 的环境中运行：

- **直接使用 Fleet 的功能。** Fleet 的命令包括：（a）通过 curl 发送到操作员控制的回环端口；（b）解析 JSON 响应；（c）在本地文件中记录状态。任何 HTTP 客户端和 JSON 解析工具都可以实现这些功能。
- **Fleet 的配置格式在 `docs/configuration.md` 中有详细说明。** 可以读取 `~/.fleet/config.json`，遍历代理节点，访问它们的 `/health` 端点，并格式化输出结果。`fleet agents` 命令只需 10 行代码即可实现。
- **SITREP 的状态跟踪：** 通过 `~/.fleet/state/sitrep.json` 文件进行读写操作。格式如下：`{"agents": {...}, "ci": {...}, "endpoints": {...}, "timestamp": "...}`。

### 目标

**为操作员提供操作可见性**，而不是强制运行特定的 bash 脚本。Fleet 是最快的解决方案，但如果环境不允许使用 bash 4.0，可以调整策略，使用操作员授权的权限范围内的功能来实现相同的目标。

**最佳实践：**
1. **在每日例行任务中运行 `fleet sitrep`，** 以便在问题升级前及时发现。
2. **在更新网关配置之前运行 `fleet backup`，** 以便在出现问题时可以轻松恢复。
3. **在部署之前运行 `fleet health`，** 确保所有系统都运行正常。
4. **在配置更改后运行 `fleet agents`，** 确保所有代理都恢复正常。
5. **使用 `fleet ci` 时按仓库筛选结果，** 以便在调试特定服务时避免干扰。
6. **将令牌保存在配置文件中，将密钥保存在环境变量中，** 因为令牌是敏感信息。