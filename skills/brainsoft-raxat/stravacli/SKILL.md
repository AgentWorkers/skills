---
name: stravacli
description: 使用 `stravacli` 终端工具来访问 Strava 数据（包括运动员资料、活动记录、路线信息、分段数据、所属俱乐部、装备信息以及上传的文件），并执行一些有限的写入操作（如更新或上传活动数据）。该工具会在用户请求 Strava 的各项数据指标、历史记录或导出功能时被触发；同时，它也支持通过命令行接口（CLI）实现 Strava 的自动化操作。
---
# stravacli

使用 `stravacli` 通过终端执行 Strava 相关操作。

## 设置

- 确保 `stravacli` 可执行文件已在系统的 `PATH` 环境变量中：`stravacli --version`
- 在执行数据相关命令之前，请先进行身份验证：
  - 本地登录：`stravacli auth login`
  - 无界面模式（Headless/VPS）登录：`stravacli auth login --remote`，随后执行 `stravacli auth login --auth-url '<callback-url>'`
- 验证身份验证状态：`stravacli auth status`

## 读取命令（默认推荐使用）

- 运动员个人信息：`stravacli athlete me --json`
- 运动员统计数据：`stravacli athlete stats --json`
- 运动员训练区间信息：`stravacli athlete zones --json`
- 活动列表：`stravacli activities list --per-page 10 --json`
- 活动详情：`stravacli activities get <id> --json`
- 活动中的分段信息：`stravacli activities laps <id> --json`
- 活动数据流：`stravacli activities streams <id> --json`
- 路线列表/获取：`stravacli routes list --json` / `stravacli routes get <id> --json`
- 导出路线文件：`stravacli routes export <id> --format gpx --out ./route.gpx`
- 标记重要路段/探索路线：`stravacli segments starred --json`，`stravacli segments explore --bounds <swlat,swlng,nelat,nelng> --json`
- 俱乐部信息：`stravacli clubs list --json`
- 配件信息：`stravacli gear get <id> --json`
- 上传状态查询：`stravacli uploads get <uploadId> --json`

## 写入命令（执行前请确认操作意图）

- 更新活动元数据：`stravacli activities update <id> --name '新名称' --description '...'`
- 上传活动文件：`stravacli activities upload --file ./run.fit --yes --json`

在执行写入操作之前，请务必确认操作意图。

## 输出格式规范

- 当需要解析或重新使用输出结果时，请使用 `--json` 选项。
- 用户信息输出应简洁明了，包括关键数据和标识符。
- 如果命令因身份验证问题失败，请先执行 `stravacli auth status`，然后重新登录。