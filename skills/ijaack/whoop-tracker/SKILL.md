---
name: whoop
description: 通过 API 访问 WHOOP 健身追踪器的数据，包括恢复评分、睡眠指标、锻炼统计、每日身体压力以及身体测量数据。当用户询问他们的 WHOOP 数据、健身指标、恢复状态、睡眠质量、锻炼表现或希望跟踪健康趋势时，可以使用此功能。
---

# WHOOP API

通过官方的REST API从WHOOP可穿戴设备检索并分析健康数据。

## 使用示例
```bash
# Install (if using Clawdhub)
clawdhub install whoop-tracker

# From the skill root:
python3 scripts/get_recovery.py --today
python3 scripts/get_sleep.py --last
python3 scripts/get_workouts.py --days 7
python3 scripts/get_profile.py
```

## 先决条件

- Python 3.7及以上版本
- `requests`库：`pip3 install requests`  
  （或运行 `bash scripts/install.sh`）

## 快速入门

### 1. 注册应用程序
- 访问 https://developer.whoop.com
- 创建一个新的应用程序，并记下您的 `client_id` 和 `client_secret`
- 设置重定向URI（例如：`http://localhost:8080/callback`）

### 2. 保存凭据
```bash
mkdir -p ~/.whoop
cat > ~/.whoop/credentials.json <<EOF
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
EOF
chmod 600 ~/.whoop/credentials.json
```

### 3. 授权（请参阅 [references/oauth.md](references/oauth.md) 以获取完整指南）
- 在浏览器中打开授权URL
- 用户授权 → 系统会生成一个代码
- 使用 `WhoopClient.authenticate(code, redirect_uri)` 将代码兑换为令牌

### 4. 获取数据
所有脚本均从技能（skill）的根目录运行：

```bash
# Today's recovery
python3 scripts/get_recovery.py --today

# Last night's sleep
python3 scripts/get_sleep.py --last

# Recent workouts
python3 scripts/get_workouts.py --days 7

# User profile
python3 scripts/get_profile.py
```

## 核心数据类型

### 恢复状态
- **恢复评分**（0-100）：身体对压力的适应程度
- **心率变异性（HRV，单位：毫秒）**
- **静息心率**：早晨的基线心率
- **血氧饱和度（SPO2）**
- **皮肤温度**：与基线的温差（单位：°C）

### 睡眠数据
- **睡眠质量百分比**：实际睡眠质量与所需睡眠质量的对比
- **睡眠时长**：总睡眠时间及各睡眠阶段（REM、SWS、浅睡眠、清醒状态）
- **睡眠效率百分比**：实际睡眠时间与总睡眠时间的比例
- **睡眠规律性百分比**：睡眠时间的稳定性
- **呼吸频率**：每分钟的呼吸次数
- **睡眠需求/欠款**：当前的睡眠需求及累积的睡眠不足量

### 循环（每日压力指标）
- **压力评分**：心血管负荷（0-21分）
- **千焦（Kilojoules）**：能量消耗量
- **平均/最高心率**：每日心率指标

### 锻炼数据
- **压力评分**：特定活动的压力程度
- **运动类型**：进行的运动（跑步、骑行等）
- **心率区间**：在各个心率区间内的时间
- **距离/海拔**：GPS测量数据（如可用）

## API接口

基础URL：`https://api.prod.whoop.com`

请参阅 [references/api-reference.md](references/api-reference.md) 以获取包含响应模式的完整API接口文档。

**用户资料：**
- `GET /v1/user/profile/basic` — 名称、电子邮件
- `GET /v1/user/body_measurement` — 身高、体重、最高心率

**恢复状态：**
- `GET /v1/recovery` — 所有恢复数据（分页显示）
- `GET /v1/cycle/{cycleId}/recovery` — 某个周期的恢复数据

**睡眠数据：**
- `GET /v1/sleep` — 所有睡眠记录（分页显示）
- `GET /v1/sleep/{sleepId}` — 通过ID查询特定睡眠记录
- `GET /v1/cycle/{cycleId}/sleep` — 某个周期的睡眠数据

**循环数据：**
- `GET /v1/cycle` — 所有生理周期数据（分页显示）
- `GET /v1/cycle/{cycleId}` — 通过ID查询特定周期数据

**锻炼数据：**
- `GET /v1/workout` — 所有锻炼记录（分页显示）
- `GET /v1/workout/{workoutId}` — 通过ID查询特定锻炼记录

所有数据获取接口都支持 `start`、`end`（ISO 8601格式）、`limit`（最多25条记录）和 `nextToken`（分页游标）参数。

## 所需的OAuth权限范围

- `read:profile` — 用户名称和电子邮件
- `read:body_measurement` — 身高、体重、最高心率
- `read:recovery` — 恢复状态评分和心率变异性数据
- `read:sleep` — 睡眠指标和睡眠阶段数据
- `read:cycles` — 每日压力数据
- `read:workout` — 锻炼数据和活动信息

## 脚本

### `scripts/whoop_client.py`
核心API客户端功能：
- OAuth令牌存储与自动刷新
- 令牌过期检测（自动刷新）
- 速率限制处理（遇到429错误时进行重试）
- 自动分页功能（`iter_recovery`、`iter_sleep`、`iter_cycles`、`iter_workouts`）

### `scripts/get_recovery.py`
```bash
python3 scripts/get_recovery.py --today              # Today's recovery
python3 scripts/get_recovery.py --days 7             # Past week
python3 scripts/get_recovery.py --start 2026-01-20   # From date
python3 scripts/get_recovery.py --json               # Raw JSON output
```

### `scripts/get_sleep.py`
```bash
python3 scripts/get_sleep.py --last       # Last night
python3 scripts/get_sleep.py --days 7     # Past week
python3 scripts/get_sleep.py --json       # Raw JSON output
```

### `scripts/get_workouts.py`
```bash
python3 scripts/get_workouts.py --days 7             # Past week
python3 scripts/get_workouts.py --sport running       # Filter by sport
python3 scripts/get_workouts.py --json                # Raw JSON output
```

### `scripts/get_profile.py`
```bash
python3 scripts/get_profile.py            # Profile + body measurements
python3 scripts/get_profile.py --json     # Raw JSON output
```

### `scripts/install.sh`
```bash
bash scripts/install.sh                   # Install pip dependencies + setup guide
```

## 故障排除

### “ModuleNotFoundError: No module named 'requests'”
请安装 `requests` 库：`pip3 install requests` 或运行 `bash scripts/install.sh`

### “Credentials not found at ~/.whoop/credentials.json”
请在 `~/.whoop/credentials.json` 文件中创建包含 `client_id` 和 `client_secret` 的配置文件（参见快速入门步骤2）。

### “Not authenticated”
请完成OAuth授权流程（请参阅 [references/oauth.md]）。

### “401 Unauthorized”（令牌刷新失败）
您的刷新令牌已过期，请重新从授权URL进行授权。

### “429 Too Many Requests”
达到速率限制。系统会在 `Retry-After` 时间间隔后自动重试。

### 结果为空
请检查您指定的日期范围——使用 `--days 7` 或更宽的时间范围。确保您的OAuth权限范围包含您要请求的数据类型。

## 参考资料

- [references/oauth.md](references/oauth.md) — OAuth设置、令牌管理、授权流程
- [references/api-reference.md](references/api-reference.md) — 完整的API接口文档及响应模式