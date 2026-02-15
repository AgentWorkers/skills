---
name: clawboard
description: "使用 OpenClaw 安装并操作 Clawboard。该工具可用于脚本化/手动安装、令牌设置、Docker 启动、日志插件配置以及验证等操作。"
---

# Clawboard

## 状态

- ClawHub：**尚未可用**。
- 安装路径：通过脚本化引导程序安装或手动从仓库安装。
- 如果缺少 OpenClaw 且用户需要 Chutes 提供者，请在创建 `https://chutes.ai` 账户后，先运行 `add_chutes.sh` 脚本（位于 `../../inference-providers/add_chutes.sh`）。

## 当前架构概览

- `web`（Next.js）：`http://localhost:3010`
- `api`（FastAPI + SQLite）：`http://localhost:8010`
- `classifier`（异步第二阶段工作器）：负责主题/任务分类
- `qdrant`（向量索引）：在内部 Docker 网络中提供密集检索功能
- `clawboard-logger` 插件：用于日志记录和响应时间统计

## 检索/搜索机制

- 使用密集向量 + BM25 算法 + 词汇匹配
- 采用互惠排名融合算法进行重新排序
- 主要使用 Qdrant，同时支持 SQLite 嵌入作为备用方案

## 目标

让用户能够成功安装并使用 Clawboard，具体要求如下：
1. `web`、`api` 和 `classifier` 都能正常运行。
2. `clawboard-logger` 插件已安装并启用。
3. 令牌流配置正确（写入数据及非本地读取操作均需依赖此配置）。
4. OpenClaw 网关已重启，并且用户能够成功登录到 Clawboard。

## 重要规则（仓库与已安装技能的关联）

- 仓库副本（版本控制）：`$CLAWBOARD_DIR/skills/clawboard`
- OpenClaw 所使用的安装路径：`$HOME/.openclaw/skills/clawboard`
- **默认安装方式为符号链接**（`~/.openclaw/skills/clawboard -> $CLAWBOARD_DIR/skills/clawboard`）。
- 运行时可以确定当前使用的是哪种安装模式：

### 符号链接模式（默认）

- 在符号链接模式下，仓库中的任何更改会立即反映在 OpenClaw 中。
- 在复制模式下，需要手动同步或复制更改后，更改才会更新到 OpenClaw。当 `SKILL.md`、`agents/`、`references/` 或 `scripts/` 文件发生变化时，需要执行同步操作：

### 复制模式

- 如果在复制模式下修改了 `~/.openclaw/skills/clawboard` 目录下的文件，请在提交前先将其同步回仓库：

### 开发环境与运行时注意事项

- Clawboard 代码的典型存放位置：
  - `~/[agent_name]/clawboard`
  - `~/[agent_name]/projects/clawboard`
- 脚本化安装会自动检测 OpenClaw 的工作区布局，并将代码安装到这些位置之一。
- 在处理 Clawboard 的前端/后端功能时，建议使用这些位置的 Git 仓库副本，而非 `~/.openclaw/skills/*` 目录。
- 安装完成后，假设以下 Docker 服务正在运行：
  - `CLAWBOARD_WEB_HOT_RELOAD=1`：表示使用 Next.js 的热重载功能（此时 `web` 服务会停止）。
  - `CLAWBOARD_WEB_HOT_RELOAD=0`：表示使用生产环境的 `web` 服务。
- 可用于检查运行状态的命令：
  - `docker compose ps`
  - `echo "$CLAWBOARD_WEB_hot_RELOAD"`（或从 `$CLAWBOARD_DIR/.env` 中读取）
  - `curl -s http://localhost:8010/api/health`
- 编辑代码时的注意事项：
  - 首先检查技能文件的安装路径（`test -L ~/.openclaw/skills/clawboard`）。
  - 如果使用符号链接模式，直接编辑仓库文件（`$CLAWBOARD_DIR/skills/clawboard/**`）。
  - 如果使用复制模式，编辑后需要执行同步操作（`bash scripts/sync_openclaw_skill.sh --to-openclaw --apply --force`）。
- 修改 `clawboard-logger` 插件后，需在 OpenClaw 中重新安装并启用该插件：
  - `openclaw plugins install -l "$CLAWBOARD_DIR/extensions/clawboard-logger"`
  - `openclaw plugins enable clawboard-logger`
  - `~/.openclaw/skills/clawboard-logger` 是可选的，可能默认不存在。如果环境中存在该文件，请确保其与仓库中的版本保持同步。

## 安装方式

### 1) 快速脚本安装（推荐）

使用以下脚本进行安装：

该脚本会自动检测你的 OpenClaw 工作区位置，并据此克隆或更新仓库。如果找到 `projects/`（或 `project/`）目录结构，则会将技能文件安装到该目录；否则会安装到 `~/clawboard` 目录。
- 脚本还生成令牌，并将 `CLAWBOARD_TOKEN` 存储在 `.env` 文件中。
- 脚本会检测浏览器访问的 URL（优先使用 Tailscale，否则使用本地地址），并设置 `CLAWBOARD_PUBLIC_API_BASE` 和 `CLAWBOARD_PUBLIC_WEB_URL`。
- 脚本会构建并启动相关的 Docker 服务。
- 确保 `web`、`api`、`classifier` 和 `qdrant` 服务都能正常运行。
- 把技能文件安装到 `$HOME/.openclaw/skills/clawboard`（默认为符号链接）。
- 安装并启用 `clawboard-logger` 插件。
- 通过 `openclaw config set` 命令配置插件参数。
- 确保 OpenClaw 的 OpenResponses 端点（`POST /v1/responses`）已启用，以便处理附件上传。
- 重启 OpenClaw 网关。
- 设置相关配置参数。

如果尚未安装 `openclaw` CLI，脚本仍会完成 Clawboard 的部署，并提供后续操作指南。
此外，当缺少 OpenClaw 时，脚本还会自动尝试安装 Chutes 插件。

**常用参数：**
- `--integration-level full|write|manual`（默认为 `write`）
- `--no-backfill`（等同于 `manual`）
- `--api-url http://localhost:8010`
- `--web-url http://localhost:3010`
- `--web-hot-reload` / `--no-web-hot-reload`
- `--public-api-base https://api.example.com`
- `--public-web-url https://clawboard.example.com`
- `--token <token>`
- `--title "<name>"`
- `--skill-symlink`（默认值）
- `--skill-copy`（用于禁用符号链接模式）
- `--update`

### 2) 手动安装

**前提条件：**
- 安装 `git`、`docker` 及 `openclaw` CLI
- 在 macOS 上安装 Docker Desktop

**安装步骤：**
1. 克隆仓库。
2. 生成令牌并配置环境变量。

**配置环境变量：**
- 在 `$CLAWBOARD_DIR/.env` 中设置 `CLAWBOARD_TOKEN=<value>`。
- 设置 `CLAWBOARD_PUBLIC_API_BASE=<浏览器可访问的 API 地址>`。
- 可选：设置 `CLAWBOARD_PUBLIC_WEB_URL=<浏览器可访问的 UI 地址>`。

**示例：**
- 本地地址：`http://localhost:8010`
- Tailscale 服务器：`http://100.x.y.z:8010`
- 自定义域名：`https://api.example.com`

**启动 Clawboard：**

**安装技能文件：**

**如果需要使用复制模式而非符号链接模式：**

**安装并启用日志插件：**

**配置插件：**

**启用附件处理功能：**

**重启 OpenClaw 网关：**

**注意事项：**
- OpenClaw 的配置文件存储在 `$HOME/.openclaw/openclaw.json` 中。
- 确保插件使用的令牌（`CLAWBOARD_TOKEN`）与 API 服务器的令牌一致。

### 3) 手动复制技能文件到 OpenClaw

使用以下命令进行手动安装：

**安全提示：**
- 所有写入操作及非本地读取操作均需使用 `CLAWBOARD_TOKEN`。
- 本地读取操作默认为无令牌访问（仅限读取）。
- 严格限制网络访问权限（使用防火墙或 Tailscale 的访问控制规则；除非特别需要，否则避免公开访问数据）。
- 使用 Docker Compose 时，默认情况下不会将相关服务绑定到主机端口；建议通过 API 进行读写操作。

## 验证步骤

运行以下命令进行验证：
- 确保 API 运行正常。
- 检查 `tokenRequired` 和 `tokenConfigured` 的配置是否正确。
- 确保 `logger` 插件已启用。
- 检查搜索端点是否能返回相关模式信息（当有向量数据时，还会显示 Qdrant 的相关信息）。
- 新的 OpenClaw 消息应记录在 Clawboard 的日志中。

## 可选辅助工具：

- 本地内存设置脚本：`$CLAWBOARD_DIR/skills/clawboard/scripts/setup-openclaw-local-memory.sh`
- **内存备份工具（GitHub 私有仓库）：**
  - 设置脚本：`$CLAWBOARD_DIR/skills/clawboard/scripts/setup-openclaw-memory-backup.sh`
  - 备份脚本：`$CLAWBOARD_DIR/skills/clawboard/scripts/backup_openclaw_curated_memories.sh`（仅在文件更改时执行备份操作）
  - 备份内容包括配置、主题、任务、日志以及可选的附件信息。
  - 配置文件存储路径：`$HOME/.openclaw/credentials/clawboard-memory-backup.json`（权限设置为 600）。
- Chutes 提供者辅助工具：`curl -fsSL https://raw.githubusercontent.com/sirouk/clawboard/main/inference-providers/add_chutes.sh | bash`

**参考文档：**
- `references/clawboard-api.md`
- `references/openclaw-hooks.md`
- `references/openclaw-memory-local.md`