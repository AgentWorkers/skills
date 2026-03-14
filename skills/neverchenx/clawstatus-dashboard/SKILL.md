---
name: clawstatus-dashboard
description: 从 GitHub 安装、更新、运行并验证公共的 ClawStatus 仪表板。当需要将 ClawStatus 部署到本地或局域网主机上、刷新现有的代码仓库、重启用户服务，或者验证仪表板是否能够在端口 8900 上访问时，请使用该工具。
---
# ClawStatus 仪表板

请从公开的 GitHub 仓库安装或刷新 ClawStatus，然后确认仪表板是否可以正常访问。

该仪表板包含以下功能：
- 过去 15 天的每日令牌实际消耗量图表
- 活动令牌与未活动令牌的分布情况
- 可用于 Overview 代理和 Cron 作业的模态模型切换功能
- Cron 作业的执行频率显示（便于人类阅读，例如：每天 07:00），以及手动触发运行的按钮
- 被禁用的 Cron 作业会自动隐藏
- 状态颜色编码：正常 = 绿色，错误 = 红色
- 下一次执行时间以倒计时形式显示（例如：5 分 30 秒）
- 支持中文/英文语言切换，并可保存用户偏好设置
- OpenClaw 的状态颜色编码（绿色/黄色/红色）
- 可配置的刷新速度（最快/较快/中等/较慢）
- 无需依赖 Bootstrap，也不使用 CDN

## 快速入门

1. 运行 `scripts/install_or_update.sh [目标目录]` 命令，以克隆或更新仓库，并将其安装到可编辑的模式。
2. 启动或重启应用程序：
   - 在前台运行：`clawstatus --host 0.0.0.0 --port 8900 --no-debug`
   - 通过 systemd 用户服务启动：`systemctl --user restart clawstatus.service`
3. 验证访问权限：
   - 本地访问：`curl -I http://127.0.0.1:8900/`
   - 局域网访问：`curl -I http://<局域网IP>:8900/`

## 工作流程

### 安装或更新

- 使用 `scripts/install_or_update.sh` 命令进行常规设置。
- 默认的目标目录为 `~/ClawStatus`。
- 如果该目录不存在，脚本会从 `https://github.com/NeverChenX/ClawStatus.git` 克隆仓库；否则直接使用现有的代码库。

### 运行

可以选择以下方式之一：
- 在前台运行命令以快速手动执行操作。
- 如果系统已经配置了用户服务，可以使用 `systemctl --user restart clawstatus.service` 来重启应用程序。

### 验证

安装或重启后，务必通过 HTTP 响应头来验证仪表板的正常运行情况。

如需命令示例，请参阅 `references/commands.md` 文件。