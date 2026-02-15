---
name: trainingpeaks
description: 从 TrainingPeaks 获取实时训练计划、锻炼数据、健康指标（CTL/ATL/TSB）以及个人记录。该功能采用基于 cookie 的身份验证方式（无需 API 密钥）。建议与其他与耐力训练、自行车运动、跑步或游泳相关的训练辅助工具结合使用，以获得最佳训练效果。
---

# TrainingPeaks Skill

这是一个用于访问 TrainingPeaks 内部 API 的命令行工具（CLI）。该工具完全基于 Python 标准库开发，无需依赖任何第三方库（如 pip）。

## 设置：获取认证 cookie

1. 使用浏览器登录 [TrainingPeaks](https://app.trainingpeaks.com)。
2. 打开浏览器的开发者工具（DevTools），选择“应用程序”（Application）→“Cookies”，然后查找名为 `Production_tpAuth` 的 cookie。
3. 复制该 cookie 的值（它是一个经过编码的字符串）。

完成这些步骤后，你就可以使用该 CLI 进行认证了。

#### 或者，你也可以通过设置环境变量来简化认证过程（这对持续集成（CI）脚本非常有用）：

####

认证凭据存储在 `~/.trainingpeaks/` 目录下，文件的权限设置为 `0600`。

## 命令

### `auth <cookie>` — 进行认证

该命令用于存储和验证 `Production_tpAuth` cookie，并将其转换为 Bearer token，同时将运动员 ID 存储在缓存中。

####

### `auth-status` — 检查认证状态

####

### `profile [--json]` — 运动员信息

####

### `workouts <start> <end> [--filter all|planned|completed] [--json]`

该命令用于列出指定日期范围内的训练记录（最多查询 90 天内的记录）。

####

输出列包括：日期（Date）、训练名称（Title）、运动项目（Sport）、训练状态（Status，✓/○ 表示已完成/未完成）、计划时长（Planned duration）、实际时长（Actual duration）、总训练量（TSS）以及训练距离（Distance）。

### `workout <id> [--json]` — 训练详情

####

该命令用于获取单次训练的详细信息，包括训练描述、教练评论以及所有相关数据。

####

### `fitness [--days 90] [--json]` — 体能数据

####

该命令用于获取运动员的体能数据（CTL）、疲劳程度（ATL）和训练状态（TSB）。

####

#### 输出内容包括当前的体能/疲劳/训练状态总结，以及过去 14 天的每日数据。

### `peaks <sport> <pr_type> [--days 3650] [--json]` — 个人最佳成绩

####

该命令用于按运动项目和指标查询运动员的个人最佳成绩。

**有效的个人最佳成绩类型：**

| 运动项目 | 类型          |
|---------|--------------|
| 自行车   | `power5sec`, `power1min`, `power5min`, `power10min`, `power20min`, `power60min`, `power90min`, `hR5sec`, `hR1min`, `hR5min`, `hR10min`, `hR20min`, `hR60min`, `hR90min` |
| 跑步     | `hR5sec`–`hR90min`, `speed400Meter`, `speed800Meter`, `speed1K`, `speed5K`, `speed5Mi`, `speed10K`, `speed10Mi`, `speedHalfMarathon`, `speedMarathon`, `speed50K` |

## 令牌管理

- Bearer token 被缓存到 `~/.trainingpeaks/token.json` 文件中。
- 令牌的有效期为约 1 小时，会自动从存储的 cookie 中重新获取。
- Cookie 的有效期为数周，存储在 `~/.trainingpeaks/cookie` 文件中。
- 如果 cookie 过期，系统会提示用户重新认证。

## 文件位置

| 文件名        | 用途                        |
|-------------|---------------------------|
| `~/.trainingpeaks/cookie` | 存储 `Production_tpAuth` cookie           |
| `~/.trainingpeaks/token.json` | 存储 OAuth Bearer token 及其有效期         |
| `~/.trainingpeaks/config.json` | 存储运动员 ID 和账户信息               |

## 注意事项

- 所有日期均采用 `YYYY-MM-DD` 格式。
- 最大查询范围为 90 天内的训练记录。
- API 请求之间至少需要等待 150 毫秒（实现速率限制）。
- 环境变量 `TP_AUTH_COOKIE` 可覆盖本地存储的 cookie。
- 默认输出格式为人类可读的文本；使用 `--json` 选项可获取原始的 API 响应数据。