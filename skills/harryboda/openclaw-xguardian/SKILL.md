---
name: openclaw-xguardian
description: 在 macOS 上构建、配置并安装一个 24 小时不间断运行的 OpenClaw 监控系统；包括搭建 Go 项目框架、将 OpenClaw 配置到 launchd 服务中，以及调整系统的健康检查与恢复机制。该系统可用于创建或共享 OpenClaw 监护服务、将其部署到 Mac 设备上，或用于排查其恢复/日志记录功能的相关问题。
---
# OpenClaw XGuardian

## 概述
OpenClaw XGuardian 是一个基于 macOS 的守护进程（launchd），用于确保 OpenClaw 持续运行，在系统故障时自动恢复，并仅记录必要的操作事件。

## 工作流程
1. 从提供的资源文件中创建项目框架。
2. 配置相关路径和 OpenClaw 的命令行工具（CLI）的安装位置。
3. 编译 Go 语言编写的二进制文件。
4. 安装守护进程（LaunchAgent），并重新加载系统设置。
5. 通过日志文件和启动/恢复测试来验证系统的正常运行。

## 具体步骤

### 1) 从资源文件中创建项目框架
将模板项目复制到目标工作区：

```bash
cp -R /Users/xiong/.codex/skills/openclaw-xguardian/assets/guardian/* <TARGET_WORKSPACE>/
```

这会复制以下文件：
- `go.mod`
- `cmd/openclaw-guardian/main.go`
- `config.sample.json`
- `launchd/com.openclaw.guardian.plist`

### 2) 配置路径
编辑用户配置文件 `~/.openclaw-guardian/config.json`（该文件可以从 `config.sample.json` 生成）。
关键配置字段包括：
- `openclaw_bin`：`which openclaw` 命令返回的 OpenClaw 可执行文件的绝对路径。
- `config_path`：通常为 `~/.openclaw/openclaw.json`。
- `gateway_plist_path`：通常为 `~/Library/LaunchAgents/ai.openclaw.gateway.plist`。
- `log_path`：例如 `~/.openclaw-guardian/guardian.log`，用于存储日志文件。
- `verbose_logs`：默认值为 `false`，以减少日志输出量。
- `log_health_ok`：默认值为 `false`，以避免不必要的日志记录。

### 3) 编译二进制文件
```bash
go build -o bin/openclaw-guardian ./cmd/openclaw-guardian
```

### 4) 安装守护进程（LaunchAgent）
编辑 `launchd/com.openclaw.guardian.plist`，并设置以下参数：
- `ProgramArguments`：二进制文件的路径加上配置文件的路径。
- `EnvironmentVariables/PATH`：添加 Node.js 和 OpenClaw 的安装路径。
- `StandardOutPath`/`StandardErrorPath`：指定日志文件的路径。

然后安装守护进程并重新加载系统设置：

```bash
mkdir -p ~/Library/LaunchAgents
cp launchd/com.openclaw.guardian.plist ~/Library/LaunchAgents/
launchctl unload ~/Library/LaunchAgents/com.openclaw.guardian.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/com.openclaw.guardian.plist
```

### 5) 验证系统运行
- 查看日志文件：`tail -n 80 ~/.openclaw-guardian/guardian.log`。
- 可选操作：停止 OpenClaw 服务，确认系统能够正常恢复。

## 故障排除
- 如果出现 “env: node: No such file or directory” 错误，需要在 LaunchAgent 的 `PATH` 环境变量中添加 Node.js 的安装路径，并确保 `openclaw_bin` 的路径设置正确。
- 如果安装过程中出现问题，请确保 `gateway_plist_path` 指向正确的文件（`~/Library/LaunchAgents/ai.openclaw.gateway.plist`）；此时应重新启动守护进程而不是重新安装。
- 如果日志记录过多，保持 `verbose_logs` 和 `log_health_ok` 的值为 `false`。

## 资源文件
相关资源文件位于 `assets/` 目录下，其中包含项目模板：`assets/guardian/`。