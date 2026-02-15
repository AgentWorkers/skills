---
name: bambu-cli
description: 使用 `bambu-cli` 操作和排查 BambuLab 打印机的故障（包括查看设备状态、启动/暂停/恢复/停止打印、管理文件、控制摄像头、处理 GCode 文件、执行 AMS（自动校准）命令、调整运动参数、控制风扇和灯光、配置设备参数以及执行诊断功能）。当用户需要控制或监控 BambuLab 打印机、设置打印参数或访问相关代码时，可以使用 `bambu-cli`；同时，还需要将用户的需求转化为符合规范的安全命令，确保命令包含正确的参数、输出格式和确认信息。
---

# Bambu CLI

## 概述
使用 `bambu-cli` 可以通过 MQTT/FTPS/摄像头等方式配置、监控和控制 BambuLab 打印机，生成精确的命令并设置安全默认值。

## 默认值与安全性
- 确认目标打印机（配置文件或 IP/串行端口）并确定优先级：标志（flags）> 环境变量（env）> 项目配置（project config）> 用户配置（user config）。
- 避免在标志中直接使用访问代码；仅使用 `--access-code-file` 或 `--access-code-stdin`。
- 对于具有破坏性的操作（如停止打印、删除文件、发送 GCode、校准、重启等），需要用户确认；仅在用户明确同意的情况下使用 `--force`/`--confirm`。
- 如果支持，提供 `--dry-run` 选项以预览操作结果。
- 输出格式可选：默认为人类可读格式；`--json` 用于结构化输出；`--plain` 用于键值对格式的输出。

## 快速入门
- 配置打印机配置文件：`bambu-cli config set --printer <name> --ip <ip> --serial <serial> --access-code-file <path> --default`
- 查看打印机状态：`bambu-cli status`
- 监控打印机状态：`bambu-cli watch --interval 5`
- 开始打印：`bambu-cli print start <file.3mf|file.gcode> --plate 1`
- 暂停/恢复/停止打印：`bambu-cli print pause|resume|stop`
- 拍摄摄像头截图：`bambu-cli camera snapshot --out snapshot.jpg`

## 任务指南
### 设置与配置
- 使用 `config set/list/get/remove` 管理打印机配置文件。
- 通过环境变量（`BAMBU_PROFILE`、`BAMBU_IP`、`BAMBU_SERIAL`、`BAMBU_ACCESS_CODE_FILE`、`BAMBU_TIMEOUT`、`BAMBU_NO_CAMERA`、`BAMBU_MQTT_PORT`、`BAMBU_FTP_PORT`、`BAMBU_CAMERA_PORT`）避免在脚本中使用标志。
- 配置文件位置：用户目录下 `~/.config/bambu/config.json`；项目目录下 `./.bambu.json`。

### 监控
- 使用 `status` 获取一次性设备状态；使用 `watch` 定期更新设备状态（`--interval`、`--refresh`）。
- 使用 `--json` 或 `--plain` 格式便于脚本编写。

### 打印
- 使用 `print start <file.3mf|file.gcode>` 开始打印。
- 使用 `--plate <n|path>` 选择打印的板号或 GCode 文件路径。
- 如果文件已存在于打印机上，使用 `--no-upload` 选项；不要与 `.gcode` 输入一起使用该选项。
- 控制自动运动系统（AMS）：`--no-ams`、`--ams-mapping "0,1"`、`--skip-objects "1,3"`。
- 如需禁用流动校准，使用 `--flow-calibration=false`。

### 文件与摄像头
- 使用 `files list [--dir <path>]` 列出文件；`files upload <local> [--as <remote>]` 上传文件。
- `files download <remote> --out <path|->` 下载文件；`--force` 选项允许将数据写入终端（TTY）。
- 使用 `files delete <remote>` 删除文件（需用户确认）。
- `camera snapshot --out <path|->` 拍摄摄像头截图；`--force` 选项允许将截图输出到终端。

### 位置、温度、风扇、灯光控制
- 使用 `home` 设置打印机原位；`move z --height <0-256>` 移动打印机。
- 使用 `temps get|set` 设置温度（`--bed`、`--nozzle`、`--chamber`）；至少需要设置一个参数。
- 使用 `fans set` 设置风扇速度（`--part/--aux/--chamber`，范围 0-255 或 0-1）。
- 使用 `light on|off|status` 控制灯光状态。

### GCode 与校准
- 使用 `gcode send <line...>` 或 `gcode send --stdin` 发送 GCode（需用户确认；`--no-check` 可跳过验证）。
- 避免同时使用 `--access-code-stdin` 和 `gcode send --stdin`；建议使用访问代码文件。
- 如需禁用某些校准功能，使用 `calibrate` 选项（`--no-bed-level`、`--no-motor-noise`、`--no-vibration`）。

### 故障排除
- 使用 `doctor` 检查与 MQTT/FTPS/摄像头端口的 TCP 连接；如果摄像头端口无法访问，建议使用 `--no-camera` 选项。
- 默认端口为：MQTT 8883、FTPS 990、摄像头 6000（除非另有配置）。

## 参考资料
有关所有命令和标志的详细信息，请参阅 `references/commands.md`。