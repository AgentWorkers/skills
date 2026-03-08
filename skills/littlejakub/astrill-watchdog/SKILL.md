# astrill-watchdog

该脚本用于监控在 Ubuntu 系统上运行的 Astrill VPN 客户端（使用 deb GUI 包），并在 StealthVPN 隧道中断时自动重启 Astrill。

## 功能说明

该脚本每 30 秒检查一次 `tun0` 网络接口的连接状态，并通过 `ping` 命令验证连接是否正常。如果检测到连接中断，脚本会执行以下操作：
- 使用 `pkill astrill` 命令终止 Astrill 的进程树（包括 `asproxy` 和 `asovpnc` 子进程）——无需使用 `sudo` 权限；
- 使用 `setsid /autostart` 命令以完整的桌面环境（包括 `DISPLAY`、`DBUS` 和 `WAYLANDDISPLAY`）重新启动 Astrill，确保其 GUI 和 Wayland 组件能够正常初始化；
- Astrill 会自动重新连接到用户上次使用的服务器。

如果重启失败，脚本会记录错误日志（级别为 CRITICAL），并继续执行下一次检查循环。该脚本不会主动退出。

## 系统要求

- Ubuntu Linux 系统；
- 安装了 Astrill 的 deb GUI 包（路径：`/usr/local/Astrill/astrill`）；
- 系统自带的 `ping`、`ip`、`pgrep`、`pkill` 和 `setsid` 命令工具；
- 必须有活跃的桌面会话（`DISPLAY`、`DBUS` 和 `WAYLAND` 配置已启用），以便 Astrill 能够正常重启。

## 安装过程

```bash
bash setup.sh
```

安装过程不需要使用 `sudo` 权限。脚本会创建一个 systemd 用户单元，并在系统登录时自动启动该服务。

## 使用方法

```bash
astrill-watchdog.sh start    # start watchdog (also done by systemd on login)
astrill-watchdog.sh stop     # stop watchdog
astrill-watchdog.sh status   # health summary + last 20 log lines
astrill-watchdog.sh once     # single health check + restart if needed, then exit
```

## 相关文件

- `~/.config/astrill-watchdog/astrill-watchdog.sh`：监控脚本；
- `~/.config/systemd/user/astrill-watchdog.service`：systemd 用户单元配置文件；
- `~/.local/state/astrill-watchdog/watchdog.log`：日志文件（每达到 5000 行会自动旋转）；
- `~/.local/state/astrill-watchdog/watchdog.pid`：进程 ID 文件。

## 配置说明

请编辑 `astrill-watchdog.sh` 文件顶部的配置部分：

```bash
CHECK_INTERVAL=30      # seconds between health checks
RECONNECT_WAIT=60      # seconds to wait after restart before health check
PING_HOST="8.8.8.8"
PING_COUNT=3
PING_TIMEOUT=3
LOG_MAX_LINES=5000
```

配置完成后，需要重新启动 Astrill 服务：
```
systemctl --user restart astrill-watchdog.service
```

## 日志与调试信息

```bash
# Live log tail
tail -f ~/.local/state/astrill-watchdog/watchdog.log

# Systemd journal
journalctl --user -u astrill-watchdog.service -n 30

# Full status summary
astrill-watchdog.sh status
```
（注：由于提供的代码片段中没有包含具体的日志记录和调试信息部分，此处保留了注释格式。实际应用中需要根据实际情况添加相应的日志记录和调试逻辑。）