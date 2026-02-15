---
name: strava
description: 使用 Strava API 加载并分析 Strava 活动数据、统计信息以及训练记录。
homepage: https://developers.strava.com/
metadata: {"clawdbot":{"emoji":"🏃","requires":{"bins":["curl"],"env":["STRAVA_ACCESS_TOKEN"]},"primaryEnv":"STRAVA_ACCESS_TOKEN"}}
---

# Strava 技能

该技能用于与 Strava 交互，以加载活动数据、分析训练记录并跟踪健康数据。

## 设置

### 1. 创建 Strava API 应用程序

1. 访问 https://www.strava.com/settings/api
2. 创建一个应用程序（测试时使用 `http://localhost` 作为回调地址）
3. 记下您的 **客户端 ID** 和 **客户端密钥**

### 2. 获取初始 OAuth 令牌

在浏览器中访问以下 URL（将 `CLIENT_ID` 替换为实际值）：
```
https://www.strava.com/oauth/authorize?client_id=CLIENT_ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=activity:read_all
```

授权后，您将被重定向到 `http://localhost/?code=AUTHORIZATION_CODE`

将获取到的代码兑换为令牌：
```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d code=AUTHORIZATION_CODE \
  -d grant_type=authorization_code
```

系统会返回 `access_token` 和 `refresh_token`。

### 3. 配置凭据

将凭据添加到 `~/.clawdbot/clawdbot.json` 文件中：
```json
{
  "skills": {
    "entries": {
      "strava": {
        "enabled": true,
        "env": {
          "STRAVA_ACCESS_TOKEN": "your-access-token",
          "STRAVA_REFRESH_TOKEN": "your-refresh-token",
          "STRAVA_CLIENT_ID": "your-client-id",
          "STRAVA_CLIENT_SECRET": "your-client-secret"
        }
      }
    }
  }
}
```

或者使用环境变量：
```bash
export STRAVA_ACCESS_TOKEN="your-access-token"
export STRAVA_REFRESH_TOKEN="your-refresh-token"
export STRAVA_CLIENT_ID="your-client-id"
export STRAVA_CLIENT_SECRET="your-client-secret"
```

## 使用方法

### 列出最近的活动

获取最近 30 项活动：
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?per_page=30"
```

获取最近 10 项活动：
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?per_page=10"
```

### 按日期筛选活动

获取指定日期之后的活动（Unix 时间戳）：
```bash
# Activities after Jan 1, 2024
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?after=1704067200"
```

获取指定日期范围内的活动：
```bash
# Activities between Jan 1 - Jan 31, 2024
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?after=1704067200&before=1706745600"
```

### 获取活动详情

获取特定活动的详细信息（将 `ACTIVITY_ID` 替换为实际值）：
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/activities/ACTIVITY_ID"
```

### 获取运动员信息

获取已认证运动员的个人信息：
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete"
```

### 获取运动员统计数据

获取运动员的统计数据（将 `ATHLETE_ID` 替换为实际值）：
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athletes/ATHLETE_ID/stats"
```

### 分页

浏览活动列表：
```bash
# Page 1 (default)
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?page=1&per_page=30"

# Page 2
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?page=2&per_page=30"
```

## 令牌刷新

访问令牌每 6 小时会过期。可以使用辅助脚本进行刷新：
```bash
bash {baseDir}/scripts/refresh_token.sh
```

或者手动刷新：
```bash
curl -s -X POST https://www.strava.com/oauth/token \
  -d client_id="${STRAVA_CLIENT_ID}" \
  -d client_secret="${STRAVA_CLIENT_SECRET}" \
  -d grant_type=refresh_token \
  -d refresh_token="${STRAVA_REFRESH_TOKEN}"
```

响应中会包含新的 `access_token` 和 `refresh_token`。请使用这两个令牌更新您的配置文件。

## 常见数据字段

活动对象包含以下字段：
- `name` — 活动名称
- `distance` — 距离（米）
- `moving_time` — 移动时间（秒）
- `elapsed_time` — 总时间（秒）
- `total_elevation_gain` — 海拔升高量（米）
- `type` — 活动类型（跑步、骑行、游泳等）
- `sport_type` — 具体运动类型
- `start_date` — 开始时间（ISO 8601 格式）
- `average_speed` — 平均速度（米/秒）
- `max_speed` — 最高速度（米/秒）
- `average_heartrate` — 平均心率（如有）
- `max_heartrate` — 最高心率（如有）
- `kudos_count` — 获得的点赞数

## 速率限制

- 每 15 分钟内允许发送 200 条请求
- 每天允许发送 2,000 条请求

如果超过速率限制，响应中会包含 `X-RateLimit-*` 标头。

## 提示

- 转换 Unix 时间戳：`date -d @TIMESTAMP`（Linux）或 `date -r TIMESTAMP`（macOS）
- 将米转换为公里：除以 1000
- 将米转换为英里：除以 1609.34
- 将米/秒转换为公里/小时：乘以 3.6
- 将米/秒转换为英里/小时：乘以 2.237
- 将秒转换为小时：除以 3600
- 如果有 `jq`，可以使用它来解析 JSON 数据；否则可以使用 `grep`/`sed` 进行基本数据提取

## 示例

获取上周的跑步活动及其距离：
```bash
LAST_WEEK=$(date -d '7 days ago' +%s 2>/dev/null || date -v-7d +%s)
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?after=${LAST_WEEK}&per_page=50" \
  | grep -E '"name"|"distance"|"type"'
```

获取最近活动的总距离：
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?per_page=10" \
  | grep -o '"distance":[0-9.]*' | cut -d: -f2 | awk '{sum+=$1} END {print sum/1000 " km"}'
```

## 错误处理

如果收到 401 Unauthorized 错误，说明您的访问令牌已过期。请运行令牌刷新命令。

如果遇到速率限制错误，请等待限制时间窗口重置（查看 `X-RateLimit-Usage` 标头）。