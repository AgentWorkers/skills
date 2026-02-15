---
name: asl-control
description: 通过 REST API 监控和控制 AllStar Link 业余无线电节点
metadata: {"openclaw":{"emoji":"📡","requires":{"bins":["python3"],"env":["ASL_PI_IP","ASL_API_KEY"]}}}
---

# AllStar Link 节点控制

您可以通过 ASL Agent REST API 来控制和监控您的 AllStar Link 节点。

---

## 先决条件

此功能是一个**客户端**，它需要与独立运行在 Raspberry Pi（或网络中可访问的任何主机）上的 ASL3 代理后端进行通信。

**您需要：**

- 一台运行 `asl-agent` FastAPI 服务的 Raspberry Pi（服务器代码请参见本仓库的 `backend/` 目录）
- Raspberry Pi 必须能够从 OpenClaw 运行的位置被访问——推荐使用 Tailscale 进行连接
- Raspberry Pi 的 `config.yaml` 文件（位于 `/opt/asl-agent/config.yaml`）中包含您的 API 密钥和节点编号

**环境变量**（请在您的 secrets 文件中设置，例如 `~/.config/secrets/api-keys.env`）：

- `ASL_PI_IP` —— Raspberry Pi 的 IP 地址（建议使用 Tailscale 的 IP 地址，可以从任何地方访问）
- `ASL_API_KEY` —— 来自 Raspberry Pi `config.yaml` 的Bearer 令牌
- `ASL_API_BASE` —— （可选）如果您使用的端口不是 8073，请覆盖完整的基 URL。格式：`http://host:port`
- `ASL_STATE_DIR` —— （可选）覆盖 favorites/net 状态文件的存储路径。默认值：`~/.openclaw/state/asl-control/`

---

## 使用方法

所有命令都通过 Python 客户端执行。在使用前请先加载您的 secrets 文件：

```bash
source ~/.config/secrets/api-keys.env
python3 {baseDir}/scripts/asl-tool.py <command> [flags]
```

每个命令都支持 `--out json`（默认格式，机器可读）或 `--out text`（人类可读的简短命令）。

### 快速参考

```bash
# Status & monitoring
python3 {baseDir}/scripts/asl-tool.py status --out text
python3 {baseDir}/scripts/asl-tool.py nodes --out text
python3 {baseDir}/scripts/asl-tool.py report --out text
python3 {baseDir}/scripts/asl-tool.py audit --lines 20

# Connect / disconnect
python3 {baseDir}/scripts/asl-tool.py connect 55553 --out text
python3 {baseDir}/scripts/asl-tool.py connect 55553 --monitor-only --out text
python3 {baseDir}/scripts/asl-tool.py disconnect 55553 --out text

# Favorites
python3 {baseDir}/scripts/asl-tool.py favorites list
python3 {baseDir}/scripts/asl-tool.py favorites set mynet 55553
python3 {baseDir}/scripts/asl-tool.py favorites remove mynet
python3 {baseDir}/scripts/asl-tool.py connect-fav mynet --out text

# Net profiles (timed sessions, auto-disconnect default)
python3 {baseDir}/scripts/asl-tool.py net list
python3 {baseDir}/scripts/asl-tool.py net set ares 55553 --duration-minutes 90
python3 {baseDir}/scripts/asl-tool.py net start ares --out text
python3 {baseDir}/scripts/asl-tool.py net status --out text
python3 {baseDir}/scripts/asl-tool.py net tick --out text
python3 {baseDir}/scripts/asl-tool.py net stop --out text
python3 {baseDir}/scripts/asl-tool.py net remove ares

# Watch (JSON-line event stream)
python3 {baseDir}/scripts/asl-tool.py watch --interval 5 --emit-initial
```

### 状态文件

Favorites 和 net 会话状态文件存储在仓库之外，因此更新后仍会保留：

- `~/.openclaw/state/asl-control/favorites.json`
- `~/.openclaw/state/asl-control/net-profiles.json`
- `~/.openclaw/state/asl-control/net-session.json`

### Net tick（定时任务）

仅当 `net tick` 运行时才会自动断开连接。请将其设置为定时任务（cron）以强制执行：

```bash
* * * * * /bin/bash -c 'source ~/.config/secrets/api-keys.env && python3 /path/to/asl-tool.py net tick --out text >> ~/.openclaw/state/asl-control/tick.log 2>&1'
```

---

## 自然语言命令处理

当用户使用自然语言发出指令时，系统会将其转换为 Python 客户端的相应命令：

- “检查我的节点” -> `asl-tool.py report --out text`
- “当前连接了哪些节点？” -> `asl-tool.py nodes --out text`
- “连接到节点 55553” -> `asl-tool.py connect 55553 --out text`
- “仅以监控模式连接到节点 55553” -> `asl-tool.py connect 55553 --monitor-only --out text`
- “连接到 <favorite name>` -> `asl-tool.py connect-fav "<name>" --out text`
- “断开与节点 55553 的连接” -> `asl-tool.py disconnect 55553 --out text`
- “列出我的 favorites” -> `asl-tool.py favorites list --out text`
- “启动节点 <name>` -> `asl-tool.py net start <name> --out text`
- “查看网络状态” -> `asl-tool.py net status --out text`
- “显示审计日志” -> `asl-tool.py audit --lines 20 --out text`

---

## 注意事项

- 对于 `ASL_PI_IP`，建议使用 Tailscale 的 IP 地址（这样可以从网络中的任何位置访问）
- 由于节点上的 AllStar 调度器，某些节点在断开连接后可能会自动重新连接。这是 ASL 的配置行为，而非 API 的错误。如果需要强制保持断开连接，请先禁用调度器。
- 所有命令都会被记录在 Raspberry Pi 上的 `audit.log` 文件中。