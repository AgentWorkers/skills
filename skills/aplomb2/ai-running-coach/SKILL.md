---
name: ai-running-coach
description: **AI跑步教练**——通过即时通讯（IM）提供个性化训练建议，并根据Strava数据自动调整训练计划。适用于用户咨询跑步训练、训练计划、马拉松/半程马拉松/10公里/5公里赛事的准备工作、当天的训练安排、每周训练计划、跑步数据（最快成绩、最长距离、每周跑步里程）、Strava数据分析，或希望与AI跑步教练进行交流的情况。触发条件包括：跑步计划、训练计划、当天的训练内容、跑步数据、马拉松训练相关内容等。
---
# AI跑步教练

这款由OpenClaw驱动的跑步教练通过即时通讯（IM）提供个性化训练服务。其核心价值在于：**Strava数据会自动同步到系统中，AI会根据这些数据实时调整训练计划**。

## 设置

`arc`命令行工具（CLI）负责处理所有的API请求。API令牌存储在`~/.config/airunningcoach/config.json`文件中。

### 首次使用指南

如果尚未配置令牌（执行`arc config show`后返回“未设置”）：

1. 向用户发送以下欢迎信息：
```
🏃 Welcome to AI Running Coach!

To connect your account:
1. Register → https://airunningcoach.net/register
2. Choose Pro (3-day free trial, cancel anytime)
3. Connect Strava → Profile page
4. Generate API Token → Profile page
5. Paste your arc_xxx token here

Already have an account? Just paste your token!
```

2. 当用户输入令牌后，执行`arc config set-token <token>`，然后执行`arc config test`以验证连接是否成功。
3. 连接成功后，可以建议用户：“需要我查看您的Strava数据并为您制定训练计划吗？”

## 核心工作流程

### 1. 每日汇报
```bash
arc today    # Today's workout
arc week     # Full week view
```
将输出结果以友好的即时通讯消息格式呈现，并给予用户鼓励。

### 2. AI教练聊天（主要交互界面）
```bash
arc coach "user's message"
```
教练端点拥有完整的训练信息：当前训练计划、Strava跑步记录、身体状况反馈以及个人最佳成绩。所有对话都通过该界面进行：
- 训练相关问题（“我今天的配速应该多少？”）
- 数据查询（“我的5公里最快成绩是多少？”“这个月我跑了多少公里？”）
- 训练计划调整（“我受伤了，该怎么办？”）
- 动机激励

### 3. 通过即时通讯创建训练计划（对话式流程）

**切勿一次性询问所有参数**。应引导用户逐步完成以下步骤：

**步骤1**：询问用户“您打算训练的距离是多少？（5公里/10公里/半程马拉松/全程马拉松）”

**步骤2**：询问用户“您有多少时间进行训练？（4-16周）”

**步骤3**：询问用户“您的目标是什么？（参加某场比赛/提升整体体能/减肥）”
  - 如果用户有比赛目标，可以基于Strava数据给出建议。

**步骤4**：询问用户“有哪些日子无法跑步？（例如周一、周日）”

**步骤5**：确认用户的信息后，生成训练计划：
```bash
arc plan create --race <type> --weeks <n> [--target <time>] [--goal <goal>] [--mileage <level>]
```

如果用户有Strava跑步记录，系统会首先检查用户的实际里程：
```bash
arc strava summary
```
然后根据用户的平均每周里程自动填写`--mileage`参数。

### 4. Strava数据与记录
```bash
arc strava recent     # Last 5 activities
arc strava summary    # Full stats: records, PBs, weekly avg, monthly breakdown
```
当用户询问以下信息时，使用`strava summary`功能：
- “我的最快配速是多少？”
- “这个月我跑了多少公里？”
- “我最长的跑步距离是多少？”
- “我这个月的跑步量比上个月多吗？”

### 5. 自适应训练（动态调整）

当用户反馈感到疲劳或受伤时：
```bash
arc feedback --type <fatigue|injury|soreness|illness> --severity <1-5> --message "description"
```
系统会使用`arc coach`功能提供调整建议。教练会综合考虑用户的各种反馈。

当Strava数据显示以下情况时：
- 配速下降 → 建议用户休息或恢复
- 未完成训练 → 调整训练计划
- 配速超出预期 → 增加训练强度

### 6. 统计数据与进度跟踪
```bash
arc stats    # Completion rate, streaks, totals
```

## 命令参考

| 命令 | 功能 |
|---------|---------|
| `arc config set-token <t>` | 保存API令牌 |
| `arc config test` | 验证连接状态 |
| `arc today` | 查看今天的训练情况 |
| `arc week` | 查看本周的训练计划 |
| `arc stats` | 查看跑步统计数据 |
| `arc coach "msg"` | 与AI教练进行聊天 |
| `arc plan create --race X --weeks N` | 生成训练计划 |
| `arc strava recent` | 查看最近的跑步记录 |
| `arc strava summary` | 查看完整的Strava数据分析 |
| `arc feedback --type T --message "M"` | 报告身体状况 |

## 错误处理

- **401**：令牌过期 → 执行`arc config set-token <new_token>`（在个人资料页面重新生成令牌）
- **403**：需要订阅服务 → 访问https://airrunningcoach.net/choose-plan（提供3天免费试用）
- **404**：没有训练计划 → 开始对话式训练计划创建流程

## 外部接口

| 接口地址 | 发送的数据 |
|----------|-----------|
| `airunningcoach.net/api/v1/*` | API令牌、训练相关请求、训练计划参数 |

## 安全性与隐私政策

- 令牌存储在本地文件`~/.config/airunningcoach/config.json`中
- 所有数据均通过HTTPS协议传输至airrunningcoach.net
- Strava数据通过用户的OAuth授权进行访问

## 信任声明

本工具会向airrunningcoach.net发送用户的跑步数据和查询信息。仅在使用前确认您信任该服务。更多隐私政策请参阅：https://airrunningcoach.net/privacy