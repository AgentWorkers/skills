---
name: beeminder
description: **Beeminder API**：用于目标跟踪和习惯管理工具。  
该API可用于查看Beeminder设定的目标、添加数据点、查看即将到期的目标、管理个人承诺以及追踪日常习惯。  
触发事件包括：  
- “beeminder”（表示Beeminder应用程序被触发）  
- “goals due”（表示有目标即将到期）  
- “add datapoint”（表示添加了新的数据点）  
- “track habit”（表示正在追踪某个习惯）  
- “goal status”（表示目标的状态发生变化）  
- “derail”（表示目标执行过程中出现了偏差）。
---

# Beeminder API

提供对 Beeminder 的直接 REST API 访问，无需依赖任何命令行工具（CLI）。

## 设置

需要设置两个环境变量：
- `BEEMINDER_USERNAME`：Beeminder 的用户名
- `BEEMINDER_AUTH_TOKEN`：从 https://www.beeminder.com/api/v1/auth_token.json 获取的个人认证令牌（需要登录后获取）

所有示例中都使用了以下代码块：
```bash
BASE="https://www.beeminder.com/api/v1/users/$BEEMINDER_USERNAME"
```

## 功能

### 列出所有目标
```bash
curl -s "$BASE/goals.json?auth_token=$BEEMINDER_AUTH_TOKEN" | jq '[.[] | {slug, safebuf, baremin, limsum}]'
```

### 获取单个目标
```bash
curl -s "$BASE/goals/GOAL.json?auth_token=$BEEMINDER_AUTH_TOKEN"
```

关键字段：
- `slug`：目标标识符
- `safebuf`：安全缓冲天数（0 表示今天到期；负数表示目标处于“危险”状态）
- `baremin`：今天至少需要完成的任务量
- `limsum`：人类可读的总结信息（例如：“+1，2 天后到期”）
- `closedate`：目标偏离计划的日期（以 Unix 时间戳表示）
- `rate`：完成任务的目标频率
- `runits`：任务完成的时间单位（天/周/月/年）
- `headsum`：当前任务完成情况的总结
- `goalval`：目标完成值（如果没有设定最终目标，则为 `null`）
- `gunits`：任务单位（例如：“小时”、“页数”）

### 今天到期的目标
```bash
curl -s "$BASE/goals.json?auth_token=$BEEMINDER_AUTH_TOKEN" \
  | jq '[.[] | select(.safebuf <= 0)] | sort_by(.losedate) | .[] | {slug, baremin, limsum}'
```

### N 天内到期的目标
```bash
curl -s "$BASE/goals.json?auth_token=$BEEMINDER_AUTH_TOKEN" \
  | jq --arg cutoff "$(date -d '+2 days' +%s)" \
    '[.[] | select(.losedate <= ($cutoff | tonumber))] | sort_by(.losedate) | .[] | {slug, baremin, limsum}'
```

## 数据点

### 添加数据点
```bash
curl -s -X POST "$BASE/goals/GOAL/datapoints.json" \
  -d "auth_token=$BEEMINDER_AUTH_TOKEN" \
  -d "value=N" \
  -d "comment=TEXT"
```
可选参数：`-d "requestid=UNIQUE_ID"` 用于实现幂等重试（可以重复请求而不会导致数据重复）。

### 获取最近的数据点
```bash
curl -s "$BASE/goals/GOAL/datapoints.json?auth_token=$BEEMINDER_AUTH_TOKEN&count=5&sort=daystamp"
```

### 更新数据点
```bash
curl -s -X PUT "$BASE/goals/GOAL/datapoints/DATAPOINT_ID.json" \
  -d "auth_token=$BEEMINDER_AUTH_TOKEN" \
  -d "value=N" \
  -d "comment=TEXT"
```

### 删除数据点
```bash
curl -s -X DELETE "$BASE/goals/GOAL/datapoints/DATAPOINT_ID.json?auth_token=$BEEMINDER_AUTH_TOKEN"
```

## 常用操作模式

### 检查并报告到期任务
```bash
curl -s "$BASE/goals.json?auth_token=$BEEMINDER_AUTH_TOKEN" \
  | jq '[.[] | select(.safebuf <= 1)] | sort_by(.safebuf) | .[] | {slug, baremin, limsum, safebuf}'
```

### 实现幂等重试的功能
```bash
curl -s -X POST "$BASE/goals/GOAL/datapoints.json" \
  -d "auth_token=$BEEMINDER_AUTH_TOKEN" \
  -d "value=1" \
  -d "comment=done" \
  -d "requestid=GOAL-$(date +%Y%m%d)"
```

## 注意事项

- 基本 URL 必须为 `https://www.beeminder.com/api/v1/`（必须包含 `https` 和 `www`）
- 所有响应均为 JSON 格式
- 使用 `jq` 工具解析响应数据
- 日期戳采用 `YYYYMMDD` 格式
- 时间戳为 Unix 时间戳（以秒为单位）