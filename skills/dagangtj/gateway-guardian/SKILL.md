# Gateway Guardian

这是一个监控并自动重启 OpenClaw 网关的守护进程（watchdog daemon）。

## 使用方法

```bash
./guardian.sh
```

以后台守护进程的形式运行：
```bash
nohup ./guardian.sh &
```

## 主要功能

- 监控网关进程的运行状态
- 在网关进程崩溃时自动重启
- 支持配置检查间隔
- 记录重启事件
- 支持在 macOS 和 Linux 系统上运行

## 配置方法

编辑 `guardian.sh` 文件以自定义配置参数：
- `CHECK_INTERVAL`：检查间隔（单位：秒，默认值：30 秒）
- `MAX_RESTARTS`：允许的最大重启次数（超过该次数后会触发警报，默认值：5 次）
- `LOG_FILE`：日志文件的路径

## 系统要求

- 必须安装 OpenClaw
- 需要具备 Bash shell 环境