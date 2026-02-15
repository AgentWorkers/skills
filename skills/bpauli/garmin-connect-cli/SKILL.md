---
name: garmin-connect
description: Garmin Connect CLI（命令行界面）可用于管理各种与Garmin设备相关的功能，包括活动记录、健康数据、身体成分分析、锻炼计划、设备设置、目标设定等。
homepage: https://github.com/bpauli/gccli
metadata:
  {
    "openclaw":
      {
        "emoji": "⌚",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["gccli"] },
        "install":
          [
            {
              "id": "homebrew",
              "kind": "homebrew",
              "formula": "bpauli/tap/gccli",
              "bins": ["gccli"],
              "label": "Homebrew (recommended)",
            },
            {
              "id": "source",
              "kind": "source",
              "url": "https://github.com/bpauli/gccli",
              "bins": ["gccli"],
              "label": "Build from source (Go 1.24+)",
            },
          ],
      },
  }
---

# gccli

`gccli` 是用于查询 Garmin Connect 中的健康、健身和活动数据的工具，需要使用 Garmin 的单点登录（SSO）进行身份验证。

## 设置（只需一次）

- `gccli auth login you@example.com`（会打开浏览器进行 Garmin SSO 登录）
- 无界面模式：`gccli auth login you@example.com --headless`（可使用 `--mfa-code <code>` 进行多因素认证）
- 设置默认账户：`export GCCLI_ACCOUNT=you@example.com`
- 验证身份：`gccli auth status`

## 输出格式

- 默认输出为易于阅读的表格格式；使用 `--json` 或 `-j` 可以获得 JSON 格式，`--plain` 可以获得 TSV 格式。
- 数据输出到标准输出（stdout），错误信息输出到标准错误输出（stderr）。
- 在程序化解析输出时，请始终使用 `--json` 格式。

## 日期缩写

- `today`：今天
- `yesterday`：昨天
- `3d`：3 天前
- `YYYY-MM-DD`：指定日期
- 使用 `--start`/`--end` 标志可以指定日期范围

## 常用命令

- 查看身份验证状态：`gccli auth status`
- 获取身份验证令牌（用于脚本编程）：`gccli auth token`
- 删除身份验证凭据：`gccli auth remove`
- 列出所有活动：`gccli activities list --limit 20`
- 按类型列出活动：`gccli activities list --type running`
- 统计活动数量：`gccli activities count`
- 搜索活动：`gccli activities search --start-date 2024-01-01 --end-date 2024-12-31`
- 查看活动详情：`gccli activity details <id>`
- 查看活动的分段数据：`gccli activity splits <id>`
- 查看活动的天气情况：`gccli activity weather <id>`
- 查看活动的心率区间：`gccli activity hr-zones <id>`
- 查看活动的功率区间：`gccli activity power-zones <id>`
- 查看活动的训练组：`gccli activity exercise-sets <id>`
- 查看活动使用的装备：`gccli activity gear <id>`
- 下载活动数据（FIT 格式）：`gccli activity download <id> --format fit`
- 下载活动数据（GPX 格式）：`gccli activity download <id> --format gpx --output track.gpx`
- 上传活动数据：`gccli activity upload ./activity.fit`
- 创建新的活动：`gccli activity create --name "Morning Run" --type running --date 2024-06-15T07:30:00 --duration 1800 --distance 5000`
- 重命名活动：`gccli activity rename <id> "New Name"`
- 修改活动类型：`gccli activity retype <id> running`
- 删除活动：`gccli activity delete <id> --force`
- 查看健康状况摘要：`gccli health summary [date]`
- 查看每日步数：`gccli health steps [date]`
- 查看指定日期内的每日步数范围：`gccli health steps daily --start 2024-01-01 --end 2024-01-31`
- 查看每周步数：`gccli health steps weekly --weeks 4`
- 查看心率数据：`gccli health hr [date]`
- 查看静息心率：`gccli health rhr [date]`
- 查看爬升的楼层数：`gccli health floors [date]`
- 查看睡眠数据：`gccli health sleep [date]`
- 查看呼吸数据：`gccli health respiration [date]`
- 查看血氧饱和度：`gccli health spo2 [date]`
- 查看心率变异性（HRV）：`gccli health hrv [date]`
- 查看压力水平：`gccli health stress [date]`
- 查看每周的压力水平：`gccli health stress weekly --weeks 4`
- 查看身体能量储备：`gccli health body-battery [date]`
- 查看身体能量储备范围：`gccli health body-battery range --start 2024-01-01 --end 2024-01-31`
- 查看训练准备情况：`gccli health training-readiness [date]`
- 查看训练状态：`gccli health training-status [date]`
- 查看健康年龄：`gccli health fitness-age [date]`
- 查看最大摄氧量（VO2max）等指标：`gccli health max-metrics [date]`
- 查看乳酸阈值：`gccli health lactate-threshold`
- 查看骑行时的最大功率输出（FTP）：`gccli health cycling-ftp`
- 查看比赛预测：`gccli health race-predictions [date]`
- 查看比赛预测范围：`gccli health race-predictions range --start 2024-01-01 --end 2024-06-30`
- 查看耐力评分：`gccli health endurance-score [date]`
- 查看爬坡评分：`gccli health hill-score [date]`
- 查看高强度训练时间：`gccli health intensity-minutes [date]`
- 查看每周的高强度训练时间：`gccli health intensity-minutes weekly --start 2024-01-01 --end 2024-01-31`
- 查看健康事件：`gccli health events [date]`
- 查看身体成分：`gccli body composition [date]`
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
- 预订训练计划：`gccli workouts schedule add <id> 2024-06-20`
- 查看已预订的训练计划：`gccli workouts schedule list 2024-06-20`
- 删除预订的训练计划：`gccli workouts schedule remove <schedule-id>`（使用 `--force` 可跳过确认）
- 创建跑步训练计划：`gccli workouts create "Easy Run" --type run --step "warmup:5m" --step "run:20m@pace:5:00-5:30" --step "cooldown:5m"`
- 创建带有心率目标的训练计划：`gccli workouts create "HR Run" --type run --step "warmup:10m" --step "run:20m@hr:140-160" --step "cooldown:10m"`
- 创建骑行训练计划：`gccli workouts create "FTP Intervals" --type bike --step "warmup:10m" --step "run:5m@power:250-280" --step "recovery:3m" --step "run:5m@power:250-280" --step "cooldown:10m"`
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
- 解除装备与活动的关联：`gccli gear unlink <uuid> <activity-id>`
- 查看目标进度：`gccli goals list --status active`
- 查看已获得的徽章：`gccli badges earned`
- 查看可获得的徽章：`gccli badges available`
- 查看正在进行的徽章挑战：`gccli badges in-progress`
- 查看所有挑战：`gccli challenges list`
- 查看与徽章相关的挑战：`gccli challenges badge`
- 查看个人记录：`gccli records`
- 查看个人资料：`gccli profile`
- 修改个人资料设置：`gccli profile settings`
- 查看水分摄入情况：`gccli hydration [date]`
- 添加水分摄入记录：`gccli hydration add 500`
- 查看训练计划：`gccli training plans --locale en`
- 查看训练计划详情：`gccli training plan <id>`
- 查看月经周期：`gccli wellness menstrual-cycle --start-date 2024-01-01 --end-date 2024-03-31`
- 查看孕期健康状况：`gccli wellness pregnancy-summary`
- 重新加载数据：`gccli reload [date]`

## 注意事项

- 为了避免重复输入，建议将 `GCCLI_ACCOUNT` 设置为 `you@example.com`。
- 在脚本编程中，使用 `--json` 生成 JSON 格式输出，使用 `--plain` 生成 TSV 格式输出。
- 支持的日期格式包括 `today`、`yesterday`、`3d` 和 `YYYY-MM-DD`。
- 身份验证令牌安全存储在操作系统的密钥环中（macOS 的 Keychain、Linux 的 Secret Service，或文件存储）。
- 如果遇到 401 错误，令牌会自动刷新；如果遇到 429 或 5xx 错误，系统会尝试重试。
- 对于 Garmin China 账户，请使用 `export GCCLI_DOMAIN=garmin.cn`。
- 在删除活动或训练计划之前，请先确认操作（或使用 `--force` 选项）。
- 支持的数据下载格式包括 FIT、GPX、TCX 和 KML。
- 训练计划的步骤格式为 `type:duration[@target:low-high]`，其中：
  - `type` 可以是 `warmup`（热身）、`run`（跑步）、`recovery`（恢复）或 `cooldown`（冷却）；
  - `target` 可以是 `pace`（配速，单位：分钟）、`hr`（心率，单位：bpm）、`power`（功率，单位：瓦特）或 `cadence`（踏频）。