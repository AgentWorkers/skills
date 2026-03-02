---
name: stravacli
description: 使用 `stravacli` 终端工具来访问 Strava 的数据（包括运动员资料、活动记录、路线信息、分段数据、所属俱乐部、装备信息以及上传的文件），并执行一些有限的写入操作（如更新或上传活动记录）。当用户需要查询 Strava 的数据指标、历史记录或进行自动化操作时，该工具会被触发。
---
# stravacli

使用 `stravacli` 通过终端执行与 Strava 相关的操作。

## 先决条件

本功能依赖于外部 CLI 项目：
- 项目来源：https://github.com/Brainsoft-Raxat/strava-cli

在使用本功能之前，请先安装 `stravacli`：
- 推荐的安装方式（使用二进制文件）：
  - 从以下链接下载最新版本：https://github.com/Brainsoft-Raxat/strava-cli/releases/latest
- 或者使用 Go 语言安装：
  - `go install github.com/Brainsoft-Raxat/strava-cli/cmd/stravacli@latest`

安装完成后，请确认 `stravacli` 已添加到系统的 `PATH` 环境变量中：
- `stravacli --version` （用于查看版本信息）

## 设置

- 在执行数据相关操作之前，请先进行身份验证：
  - 在本地设备上：`stravacli auth login`
  - 在无界面的环境中（如 VPS）：`stravacli auth login --remote`，随后执行 `stravacli auth login --auth-url '<callback-url>'` 完成身份验证
- 验证身份验证状态：`stravacli auth status`

## 可用的命令（默认为读取操作）

- 查看运动员个人信息：`stravacli athlete me --json`
- 查看运动员统计数据：`stravacli athlete stats --json`
- 查看运动员的活动区域：`stravacli athlete zones --json`
- 列出所有活动：`stravacli activities list --per-page 10 --json`
- 查看活动详情：`stravacli activities get <id> --json`
- 查看活动的各个分段：`stravacli activities laps <id> --json`
- 查看活动数据流：`stravacli activities streams <id> --json`
- 列出/获取路线信息：`stravacli routes list --json` / `stravacli routes get <id> --json`
- 导出路线文件（格式为 gpx）：`stravacli routes export <id> --format gpx --out ./route.gpx`
- 查看/探索被标记为星标的路线段：`stravacli segments starred --json` / `stravacli segments explore --bounds <swlat,swlng,nelat,nelng> --json`
- 查看俱乐部信息：`stravacli clubs list --json`
- 查看装备信息：`stravacli gear get <id> --json`
- 查看上传状态：`stravacli uploads get <uploadId> --json`

## 可用的写入操作（执行前请先确认）

- 更新活动元数据：`stravacli activities update <id> --name '新名称' --description '...'`
- 上传活动数据文件：`stravacli activities upload --file ./run.fit --yes --json`

在执行任何写入操作之前，请务必确认操作意图。

## 输出格式规范

- 当需要解析或重用输出结果时，请使用 `--json` 选项。
- 用户信息输出应简洁明了，包括关键指标和相应 ID。
- 如果命令执行失败并出现身份验证错误，请先使用 `stravacli auth status` 命令检查身份验证状态，然后重新登录。