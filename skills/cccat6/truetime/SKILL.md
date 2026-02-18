---
name: truetime
description: 确保在 UTC、服务器时间、基于 NTP 的时间、用户本地时间以及任意时区之间实现实时、准确的调度和计划功能。该功能可用于计时器、提醒设置、Cron 任务规划、计算特定时间（如几分钟、几个月或几年后）、绝对时间戳的转换、中文农历日期的显示，以及跨时区的协调。必须严格保证时间计算的准确性，防止用户输入的值被系统中的示例值所替代；所有目标时间的计算应首先以 UTC 为基准进行，并在执行前验证时间差值是否正确。
---
# TrueTime

使用此技能可避免因示例过时、单位错误、时区偏移或夏令时（DST）混淆导致的时间错误。

## 不可商量的规则

- 将用户提供的持续时间值视为权威数据。
- 绝不要将示例中的数值直接复制到实际执行中。
- 在计算之前，先从运行时时钟读取当前时间。
- 首先计算出UTC标准时间。
- 根据需要将时间转换为服务器时区、用户时区或其他时区的显示格式。
- 当时区信息缺失且结果可能发生变化时，要求用户进行澄清。

## 必需的工作流程

1. 精确提取时间计算的目的：
   - 捕获字面短语、数值、单位、时区提示以及目标日期/时间。
   - 保持原始请求的值不变（例如“1分钟”仍为“1分钟”）。
2. 读取当前实际时间。
   - 使用捆绑的脚本进行确定性计算：
     - 相对时间：`node {baseDir}/scripts/true_time.mjs --plus 1m --user-tz Asia/Shanghai`
     - 相对时间（日历单位）：`node {baseDir}/scripts/true_time.mjs --plus 1month2weeks --user-tz America/New_York --calendar-tz America/New_York`
     - 绝对时间：`node {baseDir}/scripts/true_time.mjs --target 2026-02-17T09:30:00 --target-tz Asia/Shanghai --user-tz America/Los_Angeles`
     - NTP时间源：`node {baseDir}/scripts/true_time.mjs --plus 1h --time-source ntp`
3. 将表达式解析为一个精确的时间差或一个精确的绝对时间戳。
4. 首先计算UTC目标时间。
5. 将UTC目标时间转换为服务器/用户/其他请求的时区以供显示。
6. 在执行前验证结果：
   - 确认`target_utc - now_utc`等于请求的时间差。
   - 确认时区偏移转换是否一致。
7. 除非目标调度器明确需要本地时区，否则使用UTC执行计划。
8. 在最终响应中同时提供绝对时间和相对时间的解释。

## 相对时间的规则

- 仅接受明确的单位：
  - 毫秒：`ms`, `msec`, `msecs`, `millisecond`, `milliseconds`
  - 秒：`s`, `sec`, `second`, `seconds`
  - 分钟：`m`, `min`, `minute`, `minutes`
  - 小时：`h`, `hr`, `hour`, `hours`
  - 天：`d`, `day`, `days`
  - 周：`w`, `week`, `weeks`
  - 月：`mo`, `mon`, `month`, `months`
  - 年：`y`, `yr`, `year`, `years`
  - 十年：`decade`, `decades`
  - 世纪：`century`, `centuries`
- 对于模糊的单位，应拒绝使用并避免猜测。
- 所有单位都支持小数值，包括日历单位。
  - 例如：`1.5m`, `0.25h`, `2.5day`, `250.5ms`, `1.5month`, `0.1year`, `0.5decade`, `0.01century`。
  - 小数分隔符优先使用`.`；``,``也作为输入并会被规范化处理。
- 固定单位的数值计算精确到毫秒。
- 日历单位的处理规则：
  - `month/year/decade/century`考虑日历因素，而非固定秒数。
  - 日历运算使用`--calendar-tz`（默认为用户时区 -> 服务器时区）。
  - 小数形式的日历值会被拆分为整数部分和小数部分。
  - 对于整月，使用日历调整后的月份长度来计算毫秒。
  - 对于月末的情况，结果会限制在最后一个有效日期（例如1月31日加上1个月 -> 2月28日或29日）。
- 保持验证示例的明确性：
  - `1.5m = 90s`
  - `250ms = 0.25s`
  - `1m = 60s`
  - `1h30m = 5400s`
  - `2d = 172800s`
  - `1.5year = 18 months`
  - `1decade = 10 years`
  - `0.5decade = 5 years`
  - `1century = 100 years`
  - `0.01century = 1 year`

## 绝对时间的规则

- 优先使用IANA时区名称（如`Asia/Shanghai`, `America/Los_Angeles`, `UTC`）。
- 避免使用含义模糊的缩写（如`CST`, `IST`），除非用户确认了其含义。
- 如果用户提供的日期时间没有指定时区，应询问用户或做出默认假设。
- 对于夏令时转换期，需明确说明所使用的时区规则。

## 时区目录和自定义

- 列出所有可用的运行时时区：
  - `node {baseDir}/scripts/true_time.mjs --list-timezones`
- 快速过滤常用时区：
  - `node {baseDir}/scripts/true_time.mjs --list-timezones | rg -i '^(UTC|Asia/(Shanghai|Tokyo|Kolkata)|America/(Los_Angeles|New_York)|Europe/(London|Paris|Berlin))$'`
- 用户自定义时区：
  - 接受`--list-timezones`输出中的任何有效IANA时区。
  - 通过`--user-tz <IANA>`传递用户时区。
  - 如果用户时区未知，在执行时间敏感的操作前应先询问用户。

示例和用户确认中常用的时区：

- `UTC`（无夏令时）
- `Asia/Shanghai`（北京时间，UTC+08:00，无夏令时）
- `Asia/Tokyo`（东京时间，UTC+09:00，无夏令时）
- `Asia/Kolkata`（印度时间，UTC+05:30，无夏令时）
- `America/Los_Angeles`（美国西部时间，PST UTC-08:00 / PDT UTC-07:00，有夏令时）
- `America/New_York`（美国东部时间，EST UTC-05:00 / EDT UTC-04:00，有夏令时）
- `America/Chicago`（美国中部时间，CST UTC-06:00 / CDT UTC-05:00，有夏令时）
- `America/Denver`（美国山区时间，MST UTC-07:00 / MDT UTC-06:00，有夏令时）
- `America/Phoenix`（亚利桑那州时间，MST UTC-07:00，通常无夏令时）
- `America/Anchorage`（阿拉斯加时间，AKST UTC-09:00 / AKDT UTC-08:00，有夏令时）
- `Pacific/Honolulu`（夏威夷时间，HST UTC-10:00，无夏令时）
- `Europe/London`（英国时间，GMT UTC+00:00 / BST UTC+01:00，有夏令时）
- `Europe/Paris`（中欧时间，CET UTC+01:00 / CEST UTC+02:00，有夏令时）
- `Europe/Berlin`（中欧时间，CET UTC+01:00 / CEST UTC+02:00，有夏令时）
- `Europe/Amsterdam`（中欧时间，CET UTC+01:00 / CEST UTC+02:00，有夏令时）

## 夏令时和标准时间的规则

- 对于夏令时区域（如`America/*`, `Europe/*`），不要假设固定的偏移量。
- 始终使用实际的目标日期进行计算，而不是“当前偏移量”。
- 对于夏令时转换期间的时间模糊情况，需要明确指定偏移量：
  - 在`America/Los_Angeles`中，`2026-11-01T01:30:00`是不确定的。
  - 要求用户选择`-07:00`（转换前）或`-08:00`（转换后），或在`--target`中指定偏移量。
- 对于夏令时调整期间的时间错误，需要纠正：
  - 在`America/Los_Angeles`中，`2026-03-08T02:30:00`这样的时间是不正确的。
  - 要求用户提供有效的本地时间（例如`01:30`或`03:30`）。
- 在夏令时风险较高的情况下，建议使用明确的偏移量：
  - `--target 2026-11-01T01:30:00-07:00`
  - `--target 2026-11-01T01:30:00-08:00`

## 中文农历

- 该工具默认输出中文农历日期时间字段：
  - `lunar_timezone`（默认为`Asia/Shanghai`，可通过`--lunar-tz`配置）
  - `now_lunar`
  - `target_lunar`
- 当用户需要中文农历信息时，使用这些字段。
- 对于执行/调度，仍使用公历UTC字段作为标准。
- 如果用户只提供了农历日期文本而没有公历对应时间，应在执行前请求确认或提供公历目标时间。

## 时间源策略（服务器 vs NTP）

- 默认时间源是服务器时钟（`--time-source server`）。
- 如果用户明确要求“不使用服务器时间”，则切换到公共NTP：
  - `--time-source ntp`
- 可选的NTP控制选项：
  - `--ntp-server <host>`（可重复输入或用逗号分隔）
  - `--ntp-timeout-ms <ms>`
- NTP模式示例：
  - `node {baseDir}/scripts/true_time.mjs --plus 30m --time-source ntp --ntp-server time.google.com`
- 如果所有NTP服务器都失败，应停止并报告错误，而不是默默地切换回服务器时间。

## 必须整合的环节

在以下操作之前，必须使用TrueTime进行时间计算：

- Cron操作（`cron add`, `cron update`, `cron wake`, `cron run`），当涉及时间或调度时。
- 日历操作（创建/更新事件、转换邀请时间、多时区会议安排）。
- 提醒操作（在X分钟后/小时后、明天HH:mm、下一个工作日、重复提醒）。
- 包含预计到达时间（ETA）、截止日期转换或跨时区承诺的规划任务。

## 服务器执行策略

- 将时间保存为UTC格式（`target_utc_iso`，可选还包括纪元秒）。
- 包含用户时区和服务器时区的相关字段。
- 如果调度器支持时区感知的执行，应明确传递时区信息。
- 如果调度器仅接受UTC时间，执行时保持UTC格式，并显示转换后的本地时间预览。
- 运行时说明：此技能的辅助脚本使用Node.js（`node .../true_time.mjs`）。
- 沙箱环境说明：默认的`openclaw-sandbox:bookworm-slim`可能不包含Node.js；请使用`openclaw-sandbox-common:bookworm-slim`，或在`agents.defaults.sandbox.docker.setupCommand`中安装Node.js。

## 高频示例

- 相对时间计算：
  - 北京时间，1分钟后：`node {baseDir}/scripts/true_time.mjs --plus 1m --user-tz Asia/Shanghai`
  - 北京时间，1.5分钟后：`node {baseDir}/scripts/true_time.mjs --plus 1.5m --user-tz Asia/Shanghai`
  - 东京时间，250.5毫秒后：`node {baseDir}/scripts/true_time.mjs --plus 250.5ms --user-tz Asia/Tokyo`
  - 东京时间，90分钟后：`node {baseDir}/scripts/true_time.mjs --plus 1h30m --user-tz Asia/Tokyo`
  - 美国西部时间，2小时后：`node {baseDir}/scripts/true_time.mjs --plus 2h --user-tz America/Los_Angeles`
  - 美国东部时间，45分钟后：`node {baseDir}/scripts/true_time.mjs --plus 45m --user-tz America/New_York`
  - 印度时间，1天后：`node {baseDir}/scripts/true_time.mjs --plus 1d --user-tz Asia/Kolkata`
  - 美国中部时间，1个月后：`node {baseDir}/scripts/true_time.mjs --plus 1month --user-tz America/Chicago --calendar-tz America/Chicago`
  - 美国中部时间，1.5个月后：`node {baseDir}/scripts/true_time.mjs --plus 1.5month --user-tz America/Chicago --calendar-tz America/Chicago`
  - 美国山区时间，1年后：`node {baseDir}/scripts/true_time.mjs --plus 1year --user-tz America/Denver --calendar-tz America/Denver`
  - 美国山区时间，0.1年后：`node {baseDir}/scripts/true_time.mjs --plus 0.1year --user-tz America/Denver --calendar-tz America/Denver`
  - 夏威夷时间，10年后：`node {baseDir}/scripts/true_time.mjs --plus 1decade --user-tz Pacific/Honolulu --calendar-tz Pacific/Honolulu`
  - 夏威夷时间，0.5十年后：`node {baseDir}/scripts/true_time.mjs --plus 0.5decade --user-tz Pacific/Honolulu --calendar-tz Pacific/Honolulu`
  - UTC时间，1世纪后：`node {baseDir}/scripts/true_time.mjs --plus 1century --user-tz UTC --calendar-tz UTC`
  - UTC时间，0.01世纪后：`node {baseDir}/scripts/true_time.mjs --plus 0.01century --user-tz UTC --calendar-tz UTC`

- 绝对时间和跨时区计算：
  - 北京本地绝对时间：`node {baseDir}/scripts/true_time.mjs --target 2026-02-18T09:00:00 --target-tz Asia/Shanghai --user-tz Asia/Shanghai`
  - 向美国东部显示伦敦会议时间：`node {baseDir}/scripts/true_time.mjs --target 2026-05-20T14:00:00 --target-tz Europe/London --user-tz America/New_York`
  - 向欧洲/柏林显示UTC目标时间：`node {baseDir}/scripts/true_time.mjs --target 2026-04-15T16:00:00Z --user-tz Europe/Berlin`
  - 通过明确偏移量解决夏令时模糊问题：`node {baseDir}/scripts/true_time.mjs --target 2026-11-01T01:30:00-07:00 --user-tz America/Los_Angeles`
  - `node {baseDir}/scripts/true_time.mjs --target 2026-11-01T01:30:00-08:00 --user-tz America/Los_Angeles`
  - 基于NTP的提醒时间：`node {baseDir}/scripts/true_time.mjs --plus 15m --time-source ntp --user-tz Asia/Shanghai`

## 输出规范

在发送或安排时间敏感的操作时，必须包含以下信息：

- `now_utc`
- `target_utc`
- `target_user_tz`（如果已知）
- `target_server_tz`
- `delta_milliseconds`
- `delta_seconds`
- `time_source`（服务器 | NTP | 自定义）
- `ntp_server`（当`time_source=ntp`时）
- `now_lunar`
- `target_lunar`
- 任何假设条件（如果有）

如果任何必需的字段未知或可能显著影响目标时间，则不要继续执行。