---
name: garmin-connect
description: "Garmin Connect 与 Clawdbot 的集成：通过 OAuth 每 5 分钟同步一次健身数据（步数、心率、卡路里消耗、锻炼记录以及睡眠情况）。"
---

# Garmin Connect Skill

将您所有的Garmin健身数据同步到Clawdbot：

- 🚶 **日常活动**：步数、心率、消耗的卡路里、活跃时间、行驶距离
- 😴 **睡眠**：睡眠时长、睡眠质量以及深度睡眠/快速眼动睡眠/浅睡眠的分布
- 🏋️ **锻炼**：最近的锻炼记录（包括行驶距离、持续时间、消耗的卡路里、心率）
- ⏱️ **实时同步**：每5分钟通过Cron任务自动同步一次

## 快速入门

### 1. 安装依赖项

```bash
pip install -r requirements.txt
```

### 2. OAuth身份验证（一次性设置）

```bash
python3 scripts/garmin-auth.py your-email@gmail.com your-password
```

此操作会将您的OAuth会话信息保存到`~/.garth/session.json`文件中——完全在本地存储，非常安全。

### 3. 测试同步

```bash
python3 scripts/garmin-sync.py
```

您应该会看到包含当天统计数据的JSON输出。

### 4. 设置5分钟间隔的Cron任务

将以下命令添加到您的crontab中：

```bash
*/5 * * * * /home/user/garmin-connect-clawdbot/scripts/garmin-cron.sh
```

或者手动执行：

```bash
*/5 * * * * python3 /home/user/garmin-connect-clawdbot/scripts/garmin-sync.py ~/.clawdbot/.garmin-cache.json
```

### 5. 在Clawdbot中使用

将相关代码导入并应用于您的脚本中：

```python
from scripts.garmin_formatter import format_all, get_as_dict

# Get all formatted data
print(format_all())

# Or get raw dict
data = get_as_dict()
print(f"Steps today: {data['summary']['steps']}")
```

## 主要特性

✅ 基于OAuth的身份验证（安全，无需存储密码）
✅ 支持所有数据指标：日常活动、睡眠记录、锻炼数据
✅ 本地缓存（快速访问数据）
✅ 支持每5分钟自动同步
✅ 易于与Clawdbot集成
✅ 支持多用户使用

## 收集的数据类型

### 日常活动（`summary`）
- `steps`：每日步数
- `heart_rate_resting`：静息心率（每分钟跳动次数）
- `calories`：总消耗卡路里
- `active_minutes`：高强度运动时间（分钟）
- `distance_km`：行驶距离（公里）

### 睡眠（`sleep`）
- `duration_hours`：总睡眠时间
- `duration_minutes`：睡眠时长（分钟）
- `quality_percent`：睡眠质量评分（0-100）
- `deep_sleep_hours`：深度睡眠时长
- `rem_sleep_hours`：快速眼动睡眠时长
- `light_sleep_hours`：浅睡眠时长
- `awake_minutes`：睡眠期间清醒的时间

### 锻炼（`workouts`）
- 每次锻炼的详细信息：
  - `type`：锻炼类型（跑步、骑行等）
  - `name`：锻炼名称
  - `distance_km`：行驶距离（公里）
  - `duration_minutes`：锻炼时长（分钟）
  - `calories`：消耗的卡路里
  - `heart_rate_avg`：平均心率
  - `heart_rate_max`：最高心率

## 数据缓存位置

默认情况下，数据缓存路径为：`~/.clawdbot/.garmin-cache.json`

您可以通过以下命令自定义缓存位置：

```bash
python3 scripts/garmin-sync.py /custom/path/cache.json
```

## 相关文件

| 文件名 | 用途 |
|------|---------|
| `garmin-auth.py` | OAuth身份验证设置（仅运行一次） |
| `garmin-sync.py` | 主要同步逻辑（每5分钟运行一次） |
| `garmin-formatter.py` | 数据格式化工具 |
| `garmin-cron.sh` | Cron任务触发脚本 |
| `requirements.txt` | Python项目所需的依赖库列表 |

## 常见问题解答

### OAuth身份验证失败

- 检查电子邮件和密码是否正确
- 关闭Garmin账户的双因素认证（或使用应用内提供的密码）
- 可能是由于Garmin服务器的速率限制，请等待5分钟后重试

### 未显示任何数据

1. 确保您的Garmin设备已与Garmin Connect应用程序同步
2. 等待2-3分钟让数据同步完成
3. 查看Garmin Connect网站或应用程序中的数据
4. 之后再次运行`garmin-sync.py`脚本

### Cron任务执行权限问题

如果遇到权限问题，请检查您的系统设置

```bash
chmod +x scripts/garmin-cron.sh
chmod +x scripts/garmin-sync.py
chmod +x scripts/garmin-auth.py
```

### 缓存文件未找到

请至少运行一次`garmin-sync.py`以生成缓存文件：

```bash
python3 scripts/garmin-sync.py
```

## 使用示例

```python
from scripts.garmin_formatter import format_all, get_as_dict

# Get formatted output
print(format_all())

# Get raw data
data = get_as_dict()
if data:
    print(f"Sleep: {data['sleep']['duration_hours']}h")
    print(f"Steps: {data['summary']['steps']:,}")
```

## 许可证

本技能遵循MIT许可证——您可以自由使用、修改或衍生作品。

---

专为[Clawdbot](https://clawd.bot)开发 | 可在[ClawdHub](https://clawdhub.com)上获取更多信息