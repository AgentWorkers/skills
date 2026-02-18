---
name: mufi-calendar
description: Google Calendar 与 Naver Calendar 的集成管理：支持韩语自然语言事件解析以及提醒功能。
metadata: {"clawdbot":{"emoji":"📆","requires":{"bins":["node","python3"]},"install":[{"id":"npm","kind":"npm","packages":["@google-cloud/calendar"],"label":"Install Google Calendar Node.js library"}]}}
---
# MUFI 日历

一款用于集成管理 Google 日历和 Naver 日历的工具，专为韩国中小企业客户设计。

## 主要功能

- ✅ 与 Google 日历同步（查询、添加、修改、删除日程）
- ✅ 支持韩语自然语言解析（例如：“明天下午3点的会议”可自动转换为日程）
- ✅ 日程提醒功能（通过 cron 任务实现）
- 🚧 与 Naver 日历同步（支持浏览器自动化操作或 iCal 订阅方式）

## 设置步骤

### 1. 设置 Google 日历 API

在 Google Cloud Console 中创建 OAuth 2.0 客户 ID：
1. 访问：https://console.cloud.google.com/apis/credentials
2. 选择“OAuth 2.0 客户 ID”，然后选择“桌面应用”
3. 生成 JSON 文件，保存到 `~/.secrets/google-calendar-credentials.json`

### 2. 初始认证

打开浏览器，使用 Google 账户进行认证。认证完成后，系统会生成 `~/.secrets/google-calendar-token.json` 文件。

### 3. 环境变量（可选）

### 使用方法

### 查询日程

### 添加日程（支持自然语言输入）

### 修改日程

### 删除日程

### 设置日程提醒

### 韩语自然语言解析规则

`scripts/parse-korean.js` 脚本能够识别以下格式：

- **日期**：今天、明天、后天、下周一、2026年2月20日
- **时间**：上午9点、下午3点、15:00、3:30
- **时长**：1小时、30分钟（系统会自动计算结束时间）

**示例：**

### 与 Naver 日历的同步（测试阶段）

由于 Naver 日历没有官方 API，目前支持两种同步方式：

### 方法 1：iCal 订阅（仅支持读取）

1. 进入 Naver 日历设置，复制 iCal 地址。
2. 将地址保存到 `~/.secrets/naver-calendar-ical-url.txt` 文件中。
3. 运行 `node scripts/sync-naver.js` 脚本，将 Naver 日历数据同步到 Google 日历。

### 方法 2：浏览器自动化操作（支持读写）

使用 OpenClaw 浏览器操作 Naver 日历：

**注意**：需要保持登录状态；如果 Naver 日历的界面发生变化，需要重新修改相关脚本。

## 输出格式

- **文本格式**（默认输出方式）
- **JSON 格式**

## 通过 Discord 发送提醒

系统可以将日程提醒通过 Discord 发送给用户：

**注意**：此功能依赖于 `openclaw` 的 `message` 命令行工具。

## 常见问题及解决方法

| 问题 | 解决方案 |
|------|------|
| 401 Unauthorized | 重新执行 `node scripts/auth.js` 脚本以重新认证 |
| 令牌过期 | 删除 `~/.secrets/google-calendar-token.json` 文件并重新认证 |
| 韩语解析失败 | 明确指定 `--start` 和 `--end` 参数 |
| 需要登录 Naver 日历 | 使用 OpenClaw 浏览器登录 Naver.com 后再尝试操作 |

## 参考资料

- Google 日历 API：https://developers.google.com/calendar/api/v3/reference
- 自然语言解析：使用 `chrono-node` 库并添加韩语解析规则
- 由于 Naver 日历没有官方 API，目前只能采用上述替代方案进行同步。