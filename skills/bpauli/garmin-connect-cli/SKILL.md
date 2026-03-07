---
name: garmin-connect
description: Garmin Connect CLI（命令行接口）可用于管理各种与Garmin设备相关的功能，包括活动记录、健康数据、身体成分分析、锻炼计划、设备设置、目标设置等。
homepage: https://github.com/bpauli/gccli
metadata: {"clawdbot":{"emoji":"⌚","os":["darwin","linux"],"requires":{"bins":["gccli"]},"install":[{"id":"homebrew","kind":"brew","formula":"bpauli/tap/gccli","bins":["gccli"],"label":"Homebrew (recommended)"},{"id":"source","kind":"source","url":"https://github.com/bpauli/gccli","bins":["gccli"],"label":"Build from source (Go 1.24+)"}]}}
---
# gccli

`gccli` 是用于查询 Garmin Connect 中的健康、健身和活动数据的命令行工具，需要使用 Garmin 的单点登录（SSO）进行身份验证。

## 设置（仅需执行一次）

- `gccli auth login you@example.com`（会打开浏览器进行 Garmin SSO 登录）
- 无界面模式：`gccli auth login you@example.com --headless`（如果使用多因素认证，请添加 `--mfa-code <code>`）
- 设置默认账户：`export GCCLI_ACCOUNT=you@example.com`
- 验证登录状态：`gccli auth status`

## 输出格式

- 默认输出为易于阅读的表格格式。可以使用 `--json` 或 `-j` 选项获取 JSON 格式，`--plain` 选项获取 TSV 格式。
- 数据输出到标准输出（stdout），错误信息输出到标准错误输出（stderr）。
- 在程序化解析输出时，请务必使用 `--json` 选项。

## 日期缩写

- `today`：今天
- `yesterday`：昨天
- `3d`：3 天前
- `YYYY-MM-DD`：指定日期
- 使用 `--start`/`--end` 选项指定日期范围

## 常用命令

- 查看登录状态：`gccli auth status`
- 获取认证令牌（用于脚本编程）：`gccli auth token`
- 删除认证信息：`gccli auth remove`
- 列出所有活动：`gccli activities list --limit 20`
- 按类型列出活动：`gccli activities list --type running`
- 统计活动数量：`gccli activities count`
- 搜索活动：`gccli activities search --start-date 2024-01-01 --end-date 2024-12-31`
- 查看活动详情：`gccli activity details <id>`
- 查看活动的分段信息：`gccli activity splits <id>`
- 查看活动的天气情况：`gccli activity weather <id>`
- 查看活动的心率区间：`gccli activity hr-zones <id>`
- 查看活动的功率区间：`gccli activity power-zones <id>`
- 查看活动的训练组信息：`gccli activity exercise-sets <id>`
- 查看活动使用的装备：`gccli activity gear <id>`
- 下载活动数据（FIT 格式）：`gccli activity download <id> --format fit`
- 下载活动数据（GPX 格式）：`gccli activity download <id> --format gpx --output track.gpx`
- 上传活动数据：`gccli activity upload ./activity.fit`
- 创建新活动：`gccli activity create --name "Morning Run" --type running --date 2024-06-15T07:30:00 --duration 1800 --distance 5000`
- 重命名活动：`gccli activity rename <id> "New Name"`
- 修改活动类型：`gccli activity retype <id> running`
- 删除活动：`gccli activity delete <id> --force`
- 查看健康状况摘要：`gccli health summary [date]`
- 查看每日步数：`gccli health steps [date]`
- 查看每日步数范围：`gccli health steps daily --start 2024-01-01 --end 2024-01-31`
- 查看每周步数：`gccli health steps weekly --weeks 4`
- 查看心率数据：`gccli health hr [date]`
- 查看静息心率：`gccli health rhr [date]`
- 查看爬升的楼层数：`gccli health floors [date]`
- 查看睡眠数据：`gccli health sleep [date]`
- 查看呼吸数据：`gccli health respiration [date]`
- 查看血氧饱和度：`gccli health spo2 [date]`
- 查看心率变异性（HRV）：`gccli health hrv [date]`
- 查看压力水平：`gccli health stress [date]`
- 查看每周压力水平：`gccli health stress weekly --weeks 4`
- 查看身体电量：`gccli health body-battery [date]`
- 查看身体电量范围：`gccli health body-battery range --start 2024-01-01 --end 2024-01-07`
- 查看训练准备情况：`gccli health training-readiness [date]`
- 查看训练状态：`gccli health training-status [date]`
- 计算健康年龄：`gccli health fitness-age [date]`
- 查看最大摄氧量（VO2max）等指标：`gccli health max-metrics [date]`
- 查看乳酸阈值：`gccli health lactate-threshold`
- 查看骑行时的 FTP 值：`gccli health cycling-ftp`
- 查看比赛预测数据：`gccli health race-predictions [date]`
- 查看比赛预测范围：`gccli health race-predictions range --start 2024-01-01 --end 2024-06-30`
- 查看耐力评分：`gccli health endurance-score [date]`
- 查看爬坡评分：`gccli health hill-score [date]`
- 查看训练强度数据：`gccli health intensity-minutes [date]`
- 查看每周训练强度：`gccli health intensity-minutes weekly --start 2024-01-01 --end 2024-01-31`
- 查看健康事件：`gccli health events [date]`
- 查看身体成分数据：`gccli body composition [date]`
- 查看身体成分范围：`gccli body composition --start 2024-01-01 --end 2024-01-31`
- 查看体重变化：`gccli body weigh-ins --start 2024-01-01 --end 2024-01-31`
- 增加体重：`gccli body add-weight 75.5 --unit kg`
- 修改身体成分数据：`gccli body add-composition 75.5 --body-fat 15.2 --muscle-mass 35.0`
- 查看血压数据：`gccli body blood-pressure --start 2024-01-01 --end 2024-01-31`
- 添加新的血压记录：`gccli body add-blood-pressure --systolic 120 --diastolic 80 --pulse 65`
- 列出所有训练计划：`gccli workouts list --limit 20`
- 查看训练计划详情：`gccli workouts detail <id>`
- 下载训练计划数据（FIT 格式）：`gccli workouts download <id> --output workout.fit`
- 上传训练计划数据（JSON 格式）：`gccli workouts upload ./workout.json`
- 预约训练计划：`gccli workouts schedule add <id> 2024-06-20`
- 查看已预约的训练计划：`gccli workouts schedule list 2024-06-20`
- 删除预约的训练计划：`gccli workouts schedule remove <schedule-id>`（使用 `--force` 可跳过确认）
- 删除训练计划：`gccli workouts delete <id>`
- 创建跑步训练计划（包含配速信息）：`gccli workouts create "Easy Run" --type run --step "warmup:5m" --step "run:20m@pace:5:00-5:30" --step "cooldown:5m"`
- 创建带有心率目标的训练计划：`gccli workouts create "HR Run" --type run --step "warmup:10m" --step "run:20m@hr:140-160" --step "cooldown:10m"`
- 创建骑行训练计划（包含功率目标）：`gccli workouts create "FTP Intervals" --type bike --step "warmup:10m" --step "run:5m@power:250-280" --step "recovery:3m" --step "run:5m@power:250-280" --step "cooldown:10m"`
- 列出所有课程：`gccli courses list`
- 将课程添加到收藏夹：`gccli courses favorites`
- 查看课程详情：`gccli courses detail <id>`
- 从 GPX 文件导入课程数据（默认为骑行课程，私密模式）：`gccli courses import route.gpx`
- 通过名称导入课程：`gccli courses import route.gpx --name "Sunday Ride"`
- 按类型导入课程：`gccli courses import route.gpx --type gravel_cycling`
- 导入公开课程：`gccli courses import route.gpx --privacy 1`
- 将课程数据发送到设备：`gccli courses send <course-id> <device-id>`
- 删除课程：`gccli courses delete <id>`（使用 `-f` 可跳过确认）
- 列出所有设备：`gccli devices list`
- 修改设备设置：`gccli devices settings <device-id>`
- 设置主要设备：`gccli devices primary`
- 查看最近使用的设备：`gccli devices last-used`
- 查看设备警报设置：`gccli devices alarms`
- 查看设备的太阳能数据：`gccli devices solar <device-id> --start 2024-06-01 --end 2024-06-30`
- 列出所有装备：`gccli gear list`
- 查看装备统计信息：`gccli gear stats <uuid>`
- 查看装备的使用情况：`gccli gear activities <uuid> --limit 20`
- 设置装备默认值：`gccli gear defaults`
- 将装备与活动关联：`gccli gear link <uuid> <activity-id>`
- 解除装备关联：`gccli gear unlink <uuid> <activity-id>`
- 查看目标进度：`gccli goals list --status active`
- 查看已获得的徽章：`gccli badges earned`
- 查看可获得的徽章：`gccli badges available`
- 查看正在进行的徽章挑战：`gccli badges in-progress`
- 查看所有挑战任务：`gccli challenges list`
- 查看与徽章相关的挑战：`gccli challenges badge`
- 查看个人最佳成绩：`gccli records`
- 查看个人资料：`gccli profile`
- 修改个人资料设置：`gccli profile settings`
- 查看水分摄入情况：`gccli hydration [date]`
- 添加水分摄入记录：`gccli hydration add 500`
- 查看训练计划：`gccli training plans --locale en`
- 查看训练计划详情：`gccli training plan <id>`
- 查看月经周期数据：`gccli wellness menstrual-cycle --start-date 2024-01-01 --end-date 2024-03-31`
- 查看孕期健康信息：`gccli wellness pregnancy-summary`
- 重新加载数据：`gccli reload [date]`

## 注意事项

- 为避免重复输入账户信息，建议设置环境变量 `GCCLI_ACCOUNT=you@example.com`。
- 在脚本中使用 `--json` 选项获取 JSON 格式输出，`--plain` 选项获取 TSV 格式输出。
- 支持的日期格式包括 `today`、`yesterday`、`3d` 和 `YYYY-MM-DD`。
- 认证令牌会安全地存储在操作系统的密钥链（macOS Keychain、Linux Secret Service）中；如果遇到 401 错误，系统会自动重试；遇到 429/5xx 错误时，系统会采用指数级重试策略。
- 对于 Garmin China 账户，请设置 `export GCCLI_DOMAIN=garmin.cn`。
- 在删除活动或训练计划前请先确认操作（或使用 `--force` 选项跳过确认）。
- 支持的下载格式包括 FIT、GPX、TCX 和 KML。
- 训练计划的步骤格式为 `type:duration[@target:low-high]`，其中 `type` 可选值包括 `warmup`（热身）、`run`（跑步）、`recovery`（恢复）和 `cooldown`（冷却），`target` 可选值包括 `pace`（配速，单位：分钟）、`hr`（心率，单位：bpm）和 `power`（功率，单位：瓦特）以及 `cadence`（踏频）。