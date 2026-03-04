---
name: garmin-connect-pro
version: 1.3.0
description: 想要像 @steipete 一样保持健康和健美吗？现在你可以实时追踪自己每一步的健康进展了！这个工具能够将你所有的 Garmin Connect 数据导入 OpenClaw：包括你的运动记录、睡眠情况、心率、压力水平、身体状态、训练准备情况、最大摄氧量（VO2 max），以及那些你一直忽略的比赛预测数据。它兼容 Fenix、Forerunner、Index 体重秤等所有 Garmin 设备。此外，它还支持自然语言查询（例如：“我昨晚的睡眠质量如何？”）、ASCII 图表展示、周与周之间的数据对比，以及 FIT/GPX 文件的下载功能。
metadata:
  openclaw:
    emoji: "⌚"
    requires:
      bins: [python3]
      pips: [garminconnect>=0.2.38]
    config:
      environment:
        GARMIN_EMAIL:
          description: Garmin Connect email (alternative to credentials file)
          required: false
          secret: true
        GARMIN_PASSWORD:
          description: Garmin Connect password (alternative to credentials file)
          required: false
          secret: true
      files:
        - path: ~/.config/garmin-connect/credentials.json
          description: Garmin Connect login credentials (email + password). Used if env vars not set.
          required: false
          permissions: "600"
          containsSecrets: true
        - path: ~/.config/garmin-connect/tokens/
          description: OAuth tokens (auto-generated after login)
          required: false
          containsSecrets: true
    security:
      - Credentials can be provided via GARMIN_EMAIL/GARMIN_PASSWORD environment variables OR credentials file
      - If using credentials file: stored in plaintext at ~/.config/garmin-connect/credentials.json with 600 permissions
      - OAuth tokens cached at ~/.config/garmin-connect/tokens/
      - Third-party library 'garminconnect' handles all Garmin API communication - audit at https://github.com/cyberjunkie/garminconnect
      - No direct external transmission except via garminconnect library to Garmin servers
      - Cron jobs with stored credentials increase exposure - consider using environment variables or secure credential storage
---
# Garmin Connect Pro

这是 OpenClaw 中最全面的 Garmin Connect 功能。您可以从 Fenix、Forerunner、Index 体重秤或其他 Garmin 设备中获取活动记录、健康数据、睡眠分析、心率、压力水平、身体电量、训练状态、最大摄氧量（VO2 max）等信息。

## 安全性与隐私

⚠️ **重要安全提示：**

### 认证方式选项

**选项 1：环境变量（推荐用于定时任务）**
```bash
export GARMIN_EMAIL="your-email@example.com"
export GARMIN_PASSWORD="your-password"
```
- 更适合自动化/定时任务使用
- 不会存储在磁盘上
- 使用定时任务时不会留下明文文件

**选项 2：认证文件**
```bash
mkdir -p ~/.config/garmin-connect
echo '{"email": "your-email@example.com", "password": "your-password"}' > ~/.config/garmin-connect/credentials.json
chmod 600 ~/.config/garmin-connect/credentials.json
```
- 以明文形式存储（任何具有文件访问权限的进程都可以读取）
- 文件权限设置为 600（仅所有者可读写）
- 建议不要将此文件包含在备份中

### 第三方库

该功能使用 `garminconnect` Python 库来与 Garmin 的 API 进行通信。
- **源代码：** https://github.com/cyberjunkie/garminconnect
- **安全建议：** 如果有严格的安全要求，请对库进行审计

### 数据传输

通过官方的 `garminconnect` 库，所有数据仅传输给 Garmin，不会发送给任何第三方。

## 设置

### 首次登录

```bash
# Install dependency
pip3 install garminconnect

# Option A: Use environment variables (recommended)
export GARMIN_EMAIL="your-email@example.com"
export GARMIN_PASSWORD="your-password"

# Option B: Use credentials file
mkdir -p ~/.config/garmin-connect
echo '{"email": "your-email@example.com", "password": "your-password"}' > ~/.config/garmin-connect/credentials.json
chmod 600 ~/.config/garmin-connect/credentials.json

# Login (generates OAuth tokens)
python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py login
```

## 主要功能

| 功能 | 说明 |
|---------|-------------|
| **自然语言查询** | 例如：“我的睡眠情况如何？”、“我的身体电量是多少？”、“今天应该训练吗？” |
| **ASCII 图表** | 以图表形式显示步数、心率、压力水平和电量变化趋势 |
| **周对比** | 与上周的数据进行对比 |
| **比赛预测** | 预测 5K、10K、半程马拉松和马拉松的比赛成绩 |
| **身体成分** | 体重、肌肉质量、脂肪百分比 |
| **最大摄氧量追踪** | 通过活动数据评估心肺健康状况 |
| **数据导出** | 可导出活动记录文件（FIT/GPX 格式） |
| **训练效果分析** | 分析有氧和无氧运动的健康影响 |
| **活动中的心率区间** | 显示在每个心率区间内的时间 |
| **可视化输出** | 通过表情符号快速查看数据 |

## 快速入门

```bash
# Ask questions naturally
python3 scripts/garmin.py ask "how did I sleep?"
python3 scripts/garmin.py ask "what's my training readiness?"

# Daily summary
python3 scripts/garmin.py summary

# Trends with charts
python3 scripts/garmin.py trends --days 7
python3 scripts/garmin.py chart steps --days 14

# Compare weeks
python3 scripts/garmin.py compare

# Download activities
python3 scripts/garmin.py download --id 123456 --format fit
```

## 命令

### 自然语言查询
```bash
python3 scripts/garmin.py ask "how did I sleep?"
python3 scripts/garmin.py ask "am I stressed?"
python3 scripts/garmin.py ask "how many steps today?"
```

### 日常指标
```bash
python3 scripts/garmin.py summary              # Full daily summary
python3 scripts/garmin.py stats --today        # Steps, HR, calories
python3 scripts/garmin.py sleep --today        # Sleep stages
python3 scripts/garmin.py hr --today           # Heart rate data
python3 scripts/garmin.py hrv --today          # HRV
python3 scripts/garmin.py stress --today       # Stress levels
python3 scripts/garmin.py body-battery --today # Energy level
```

### 活动记录
```bash
python3 scripts/garmin.py activities --limit 5
python3 scripts/garmin.py activity --id 123456 --full
python3 scripts/garmin.py download --id 123456 --format fit
```

### 训练与表现分析
```bash
python3 scripts/garmin.py training --today     # Readiness + intensity
python3 scripts/garmin.py vo2max              # VO2 max + predictions
python3 scripts/garmin.py body                 # Body composition
python3 scripts/garmin.py race                 # Race predictions
```

### 数据趋势
```bash
python3 scripts/garmin.py week --days 7
python3 scripts/garmin.py trends --days 14
python3 scripts/garmin.py compare              # Week vs week
python3 scripts/garmin.py chart steps --days 30
```

## 示例输出

### 自然语言查询结果
```
🔋 Body Battery:
   Current: 45%
   ⚠️ Moderate - lighter activity recommended
```

### 周度数据对比
```
📊 WEEK VS WEEK
─────────────────────────────────────────────────
Metric          This Week   Last Week   Change
─────────────────────────────────────────────────
Steps              42,500      38,200    ↑ 11.3%
Distance (km)         35.2        28.9   ↑ 21.8%
Calories            18,500      17,200     ↑ 7.6%
Resting HR            56.0        57.5     ↓ 2.6%
```

### ASCII 图表示例
```
📈 STEPS - Last 7 Days
──────────────────────────────────────────────
10000 │       █           █
 8000 │   █   █   █       █
 6000 │   █   █   █   █   █
 4000 │   █   █   █   █   █   █
 2000 │   █   █   █   █   █   █   █
    0 └────────────────────────────────
      Mon  Tue  Wed  Thu  Fri  Sat  Sun
```

## 定时任务设置

⚠️ **安全提示：** 使用环境变量比将认证信息存储在磁盘上更安全。

### 选项 A：环境变量（推荐）

```bash
# In your crontab or OpenClaw cron config:
GARMIN_EMAIL="your-email@example.com" GARMIN_PASSWORD="your-password" python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py summary
```

### 选项 B：认证文件

```bash
# Morning briefing at 6:30
openclaw cron add --name "Morning Fitness" --cron "30 6 * * *" \
  --message "python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py summary"

# Midday check at 12:00
openclaw cron add --name "Midday Check" --cron "0 12 * * *" \
  --message "python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py ask 'body battery'"

# Evening summary at 20:00
openclaw cron add --name "Evening Summary" --cron "0 20 * * *" \
  --message "python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py week --days 1"
```

**注意：** 使用包含认证信息的脚本的定时任务会增加被攻击的风险。建议：
- 使用权限受限的专用 Garmin 账户
- 优先使用环境变量而非认证文件
- 在安全、隔离的系统中运行脚本

## 可获取的数据

| 数据类别 | 指标 |
|----------|---------|
| **活动记录** | 活动名称、类型、持续时间、距离、消耗卡路里、心率区间、训练效果、海拔变化、步数 |
| **日常统计数据** | 步数、总距离、爬楼层数、总卡路里（静息/活动/基础代谢率）、心率（静息/最大值）、压力水平、身体电量 |
| **睡眠数据** | 睡眠总时长、深度睡眠时间、浅睡眠时间、快速眼动睡眠时间、清醒时间、睡眠质量评分 |
| **心率数据** | 静息心率、最低/最高心率、心率区间、心率变异性（HRV） |
| **训练数据** | 训练状态评分、高强度训练时间、有氧/无氧运动的影响 |
| **身体数据** | 体重、肌肉质量、脂肪百分比（通过 Index 体重秤获取） |
| **运动表现** | 最大摄氧量（VO2 max）、比赛成绩预测（5K/马拉松） |
| **健康数据** | 血氧饱和度（SpO2）、呼吸频率、水分摄入量、压力变化趋势 |
| **设备信息** | 使用的设备（Fenix、Forerunner、Index 体重秤）及固件版本、电池电量 |

## JSON 格式输出

在命令后添加 `--json` 选项即可导出数据（适用于脚本编写）：

```bash
python3 scripts/garmin.py summary --json | jq '.totalSteps'
python3 scripts/garmin.py activities --json | jq '.[0].averageHR'
python3 scripts/garmin.py export --days 30 --json > monthly_export.json
```

## 系统要求

- Python 3.7 及以上版本
- `garminconnect` 库（通过 `pip install garminconnect` 安装）
- 已将设备同步到 Garmin Connect 账户

## 常见问题解决方法

### “认证失败”
- 确认认证文件或环境变量中的电子邮件和密码是否正确
- 删除临时认证令牌：`rm -rf ~/.config/garmin-connect/tokens/`
- 重新登录

### “某日期的数据缺失”
- 可能是设备尚未同步数据
- 睡眠数据通常在早晨同步后才会显示
- 某些指标（如心率变异性 HRV、训练状态）需要经过夜间处理才能获取

### 限制机制

- Garmin 可能会对频繁的 API 请求设置访问限制
- 在批量请求之间添加延迟

## 实际效果

这个工具本身不会让您变得更健康，但它能帮助您更好地关注自己的健康数据。您的 Garmin 设备已经记录了您的运动情况——现在 OpenClaw 也能提醒您了。

---

*想像 @steipete 那样保持健康吗？现在您可以精确地记录自己每一步的运动轨迹了。*