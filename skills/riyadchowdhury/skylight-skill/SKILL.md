---
name: skylight
description: 与Skylight Calendar框架进行交互——可以管理日历事件、家务任务、待办事项列表以及奖励信息。适用于用户需要查看/创建日历事件、管理家庭事务、处理购物清单或待办事项、查看奖励积分，或与Skylight智能显示屏进行交互的场景。
homepage: https://ourskylight.com
metadata:
  clawdbot:
    emoji: 📅
    requires:
      bins:
        - curl
      env:
        - SKYLIGHT_FRAME_ID
    primaryEnv: SKYLIGHT_EMAIL
---

# Skylight 日历

通过非官方 API 控制 Skylight 日历的功能。

## 设置

配置环境变量：
- `SKYLIGHT_URL`：基础 URL（默认值：`https://app.ourskylight.com`）
- `SKYLIGHT_FRAME_ID`：您的日历 ID — 请登录 [ourskylight.com](https://ourskylight.com/)，点击您的日历，然后从 URL 中复制该 ID（例如，`4197102` 来自 `https://ourskylight.com/calender/4197102`）

**身份验证（请选择一种方式）：**

**选项 A - 电子邮件/密码（推荐）：**
- `SKYLIGHT_EMAIL`：您的 Skylight 账户邮箱
- `SKYLIGHT_PASSWORD`：您的 Skylight 账户密码

**选项 B - 预先捕获的令牌：**
- `SKYLIGHT_TOKEN`：完整的授权头信息（例如，`Basic abc123...`）

## 身份验证

### 选项 A：使用电子邮件/密码登录（推荐）

通过输入电子邮件和密码登录后，系统会生成一个令牌：

```bash
# Login and get user credentials
LOGIN_RESPONSE=$(curl -s -X POST "$SKYLIGHT_URL/api/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'"$SKYLIGHT_EMAIL"'",
    "password": "'"$SKYLIGHT_PASSWORD"'",
    "name": "",
    "phone": "",
    "resettingPassword": "false",
    "textMeTheApp": "true",
    "agreedToMarketing": "true"
  }')

# Extract user_id and user_token from response
USER_ID=$(echo "$LOGIN_RESPONSE" | jq -r '.data.id')
USER_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.data.attributes.token')

# Generate Basic auth token (base64 of user_id:user_token)
SKYLIGHT_TOKEN="Basic $(echo -n "${USER_ID}:${USER_TOKEN}" | base64)"

# Now use $SKYLIGHT_TOKEN for all API requests
```

登录接口返回以下信息：
- `data.id`：用户 ID
- `data.attributes.token`：用户令牌

将这两个信息组合成 `{user_id}:{user_token}`，然后使用 Base64 编码进行基本身份验证。

### 选项 B：通过代理捕获令牌

如果您希望手动捕获令牌，请按照以下步骤操作：
1. 安装 Proxyman/Charles/mitmproxy 并信任其根证书。
2. 为 `app.ourskylight.com` 启用 SSL 代理。
3. 登录 Skylight 应用程序并捕获所有 API 请求。
4. 复制 `Authorization` 头信息（例如，`Basic <token>`）。

令牌在用户登出后会失效；重新登录时需要重新捕获令牌。

## API 格式

API 响应采用 JSON 格式，包含 `data`、`included` 和 `relationships` 字段。

## 日历事件

### 列出事件
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/calendar_events?date_min=2025-01-27&date_max=2025-01-31" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Accept: application/json"
```

查询参数：
- `date_min`（必填）：开始日期（YYYY-MM-DD 格式）
- `date_max`（必填）：结束日期（YYYY-MM-DD 格式）
- `timezone`：时区字符串（可选）
- `include`：相关资源的 CSV 列表（`categories`、`calendar_account`、`event_notification_setting`）

### 列出源日历
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/source_calendars" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

## 家务任务

### 列出家务任务
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/chores?after=2025-01-27&before=2025-01-31" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

查询参数：
- `after`：开始日期（YYYY-MM-DD 格式）
- `before`：结束日期（YYYY-MM-DD 格式）
- `include_late`：是否包含逾期任务（布尔值）
- `filter`：根据 `linked_to_profile` 进行过滤

### 创建家务任务
```bash
curl -s -X POST "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/chores" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "chore",
      "attributes": {
        "summary": "Take out trash",
        "status": "pending",
        "start": "2025-01-28",
        "start_time": "08:00",
        "recurring": false
      },
      "relationships": {
        "category": {
          "data": {"type": "category", "id": "CATEGORY_ID"}
        }
      }
    }
  }'
```

家务任务的属性：
- `summary`：任务标题
- `status`：`pending`（待处理）或 `completed`（已完成）
- `start`：开始日期（YYYY-MM-DD 格式）
- `start_time`：开始时间（HH:MM 格式，可选）
- `recurring`：是否重复执行（布尔值）
- `recurrence_set`：重复任务的规则（RRULE 格式）
- `reward_points`：奖励积分（整数，可选）
- `emoji_icon`：表情符号（可选）

## 列表（购物/待办事项）

### 列出所有列表
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/lists" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

### 获取列表中的项目
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/lists/{listId}" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

响应包含 `data.attributes.kind`（`shopping` 或 `to_do`）以及包含列表项的 `included` 数组。

列表项的属性：
- `label`：项目名称
- `status`：`pending`（待处理）或 `completed`（已完成）
- `section`：分类名称（可选）
- `position`：排序顺序

## 任务框

### 创建任务框项
```bash
curl -s -X POST "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/task_box/items" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "task_box_item",
      "attributes": {
        "summary": "Pack lunches"
      }
    }
  }'
```

任务框的属性：
- `summary`：任务标题
- `emoji_icon`：表情符号（可选）
- `routine`：是否重复执行（布尔值）
- `reward_points`：奖励积分（整数，可选）

## 分类

### 列出分类
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/categories" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

分类用于将家务任务分配给家庭成员。属性包括：
- `label`：分类名称（例如，“Mom”（妈妈），“Dad”（爸爸），“Kids”（孩子）
- `color`：十六进制颜色代码（#RRGGBB）
- `profile_pic_url`：头像 URL

## 奖励

### 列出奖励
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/rewards" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

可选查询参数：`redeemed_at_min`（日期时间），用于按兑换日期过滤奖励。

### 列出奖励积分
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/reward_points" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

## 日历信息

### 获取日历详情
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

### 列出设备
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/devices" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

## 注意事项：

- 该 API 是非官方的，通过反向工程实现的；接口可能会发生变化。
- 令牌在用户登出后会失效；需要时需要重新获取。
- 如果数据未发生变化，响应会返回 304 Not Modified（未修改）状态。
- 使用 `jq` 工具解析 JSON 格式的 API 响应。
- `frame_id` 是您的家庭标识符；所有资源都与该日历相关联。