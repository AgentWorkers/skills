---
name: strava-training-coach
description: >
  **AI跑步教练：通过每日监控您的Strava训练负荷来预防受伤**  
  该工具利用基于证据的运动科学原理（如“80/20法则”及急性与慢性工作负荷比例），检测训练量突然增加、训练强度失衡以及恢复不足的情况，并在问题演变成伤害之前通过Discord或Slack发送智能提醒。  
  **适用场景：**  
  - **“我是否过度训练了？”**：分析每周的训练量和强度，评估受伤风险。  
  - **“查看我的训练负荷”**：每日查看您的Strava活动数据。  
  - **“生成训练报告”**：生成包含四周趋势的每周总结。  
  - **“我的跑步量是否安全？”**：计算急性与慢性工作负荷比例（ACWR）。  
  - **“设置自动训练提醒”**：通过cron任务安排每日检查。  
  - **监控心率**：确保轻松训练的日子确实如此（符合“80/20法则”）。  
  - **追踪恢复情况与训练连贯性**。  
  - **可选集成Oura手环**：获取睡眠质量和身体状态数据。  
  **区别于普通Strava数据功能：**  
  该AI教练会持续监控您的训练模式，并在问题出现前主动提醒您——其功能基于Seiler（2010年）、Gabbett（2016年）以及Stoggl & Sperlich（2014年）的研究成果。  
  **安全性保障：**  
  - 无硬编码的敏感信息；  
  - 输入内容经过验证；  
  - 日志会被加密处理；  
  - Webhook URL经过安全验证；  
  - 采用安全的令牌存储方式（XDG、0600权限限制）；  
  - 实施请求速率限制；  
  - 请求超时时间为30秒。
homepage: https://developers.strava.com/docs/reference/
metadata: {"clawdbot":{"emoji":"🏃","tags":["fitness","strava","running","injury-prevention","training","alerts","discord","slack","health","marathon","overtraining","recovery","80-20-rule","heart-rate","coaching","endurance"],"requires":{"env":["STRAVA_CLIENT_ID","STRAVA_CLIENT_SECRET","DISCORD_WEBHOOK_URL or SLACK_WEBHOOK_URL"]}}}
---
# Strava训练教练

这是一个基于人工智能的训练助手，能在您察觉之前就识别出受伤风险。

## 为什么这很重要

大多数跑步损伤都遵循相同的模式：训练量突然增加，且增加得过快。Nielsen等人（2014年）的研究发现，每周跑步距离增加超过30%的跑者，受伤率会显著上升。等到您感到疼痛时，损伤已经存在好几周了。

这款训练助手会每天监控您的Strava数据，并在问题发展成实际损伤之前及时提醒您——这样您就能保持训练的连贯性，避免因此而无法继续训练。

该工具基于**80/20极化训练模型**（Seiler, 2010；Stoggl & Sperlich, 2014）设计，这也是精英耐力教练用来培养优秀运动员的方法——他们注重训练的“智慧”，而不仅仅是强度。

## 您将获得什么

- **急性与慢性工作负荷比（ACWR）监控**——追踪您的急性与慢性工作负荷比例（Gabbett, 2016）。当ACWR > 1.5时，表示受伤风险较高。
- **急性负荷警报**——如果您的每周跑步里程增加了30%以上，系统会在您的膝盖感到疼痛之前就提醒您。
- **80/20强度检查**——如果高强度训练过多，影响恢复效果，系统会提供基于数据的建议。
- **恢复提示**——长时间不训练可能会影响您的训练效果，系统会给出相应的提醒。
- **每周报告**——每周日会生成总结报告，包括四周的训练趋势、ACWR值以及强度分布情况。
- **Oura集成**——可选的睡眠和体能状态评分，帮助您做出更明智的训练决策。

## 快速入门

### 1. 连接Strava

```bash
# Set your Strava API credentials (required)
export STRAVA_CLIENT_ID=your_id
export STRAVA_CLIENT_SECRET=your_secret

# Authenticate (opens browser for OAuth)
python3 scripts/auth.py
```

您的Strava访问令牌存储在`~/.config/strava-training-coach/strava_tokens.json`文件中，文件的权限设置为0600。

### 2. 设置通知（必选）

**Discord：**
```bash
export DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
export NOTIFICATION_CHANNEL=discord
```

**Slack：**
```bash
export SLACK_WEBHOOK_URL=https://hooks.slack.com/...
export NOTIFICATION_CHANNEL=slack
```

⚠️ **安全提示：** Webhook链接必须通过环境变量设置，禁止使用硬编码的URL。

### 3. 可选：启用Oura集成

```bash
export OURA_ENABLED=true
```

需要使用Oura的CLI进行身份验证。

### 4. 运行训练助手

```bash
# Daily training check + alerts
python3 scripts/coach_check.py

# Weekly summary report  
python3 scripts/weekly_report.py
```

**可选：** 使用cron任务自动执行监控：

```json
{
  "name": "Training Coach - Daily Check",
  "schedule": {"kind": "every", "everyMs": 86400000},
  "command": "python3 scripts/coach_check.py"
}
```

## 安全特性

为了确保数据安全，本工具在ClawHub上的使用遵循以下安全规范：

### 凭据管理
- **避免硬编码敏感信息**——所有凭据都通过环境变量传递。
- **安全存储令牌**——令牌以0600权限保存。
- **符合XDG安全标准**——配置文件存储在`~/.config/strava-training-coach/`目录下。
- **令牌验证**——使用结构化数据验证令牌的有效性。

### 输入验证
- **日期格式验证**——确保日期符合ISO8601标准。
- **数值范围验证**——所有阈值都有明确的限制。
- **类型检查**——进行安全的类型转换，并提供默认值。
- **Webhook链接验证**——确保链接格式正确（适用于Discord/Slack）。

### 数据保护
- **日志加密**——敏感数据在日志中会被屏蔽。
- **临时文件安全**——状态文件具有适当的权限设置。
- **防止数据泄露**——错误信息会以安全的方式显示。
- **请求频率限制**——每种类型的警报每天最多发送1次。

### 网络安全
- **仅使用HTTPS**——所有API请求都使用TLS协议。
- **超时处理**——所有请求都有30秒的超时限制。
- **重试机制**——最多尝试3次，每次尝试之间有指数级的延迟。
- **证书验证**——使用标准的SSL验证机制。

## 配置设置

所有阈值都是可选的，系统会提供合理的默认值并进行验证。

```bash
# Training thresholds (validated ranges)
MAX_WEEKLY_MILEAGE_JUMP=30     # 5-100%, default: 30
MAX_HARD_DAY_PERCENTAGE=25     # 5-100%, default: 25
MIN_EASY_RUN_HEART_RATE=145    # 100-200 bpm, default: 145

# Feature flags
OURA_ENABLED=false             # Enable Oura integration
VERBOSE=false                  # Enable debug logging
```

## 示例警报内容

### 受伤风险提示

> “您的每周跑步里程增加了45%（从18英里增加到26英里），ACWR值为1.62。Nielsen等人（2014年）的研究表明，每周跑步距离增加超过30%会显著提高受伤风险。您的急性与慢性工作负荷比例处于高风险区间（>1.5）。建议下周将训练量减少20-30%。”

> “您60%的训练属于中等或高强度训练（心率>145）。Seiler（2010年）发现，精英运动员约80%的训练强度低于他们的最大心率（VT1）。极化训练比中等强度训练更能有效提升最大摄氧量（Stoggl & Sperlich, 2014年）。”

> “您已经5天没有进行任何训练了。Mujika和Padilla（2000年）的研究表明，长时间不运动会导致最大摄氧量下降。建议进行20分钟的轻松散步或慢跑，以保持训练效果。”

### 成就提示

> “您已经连续30天坚持训练了！持续性的训练比高强度训练更有效。Hollozy和Coyle（1984年）的研究表明，反复的有氧运动可以增加线粒体密度。”

### 每周报告（每周日）

- 每周的跑步里程及环比变化百分比。
- 急性与慢性工作负荷比例（ACWR）及风险区间。
- 训练强度分布（轻松/中等/高强度）与80/20训练原则的对比。
- 过去四周的训练趋势可视化。
- 基于数据的下周训练建议。

## 训练理念（基于科学证据）

1. **极化训练**——80%的时间进行轻松训练，20%的时间进行高强度训练（Seiler & Kjerland, 2006；Stoggl & Sperlich, 2014）。
2. **保持合适的急性与慢性工作负荷比**——将ACWR值控制在0.8-1.3之间（Gabbett, 2016）。
3. **渐进式负荷增加**——避免每周训练量突然增加超过30%，以降低受伤风险（Nielsen等人，2014年）。
4. **持续性的训练比高强度更重要**——训练频率对线粒体和毛细血管的适应有显著影响（Hollozy & Coyle, 1984）。
5. **力量训练**——可以减少68%的运动损伤和50%的过度使用损伤（Lauersen等人，2014年）。

更多详细信息请参阅`references/training-principles.md`文件，其中包含30多篇科学参考文献。

## 相关文件

- `scripts/auth.py`——用于设置Strava OAuth访问权限（令牌存储在XDG配置目录中）。
- `scripts/coach_check.py`——每日训练分析和警报功能（经过安全加固）。
- `scripts/weekly_report.py**——每周日生成的报告（经过安全加固）。
- `references/training-principles.md**——基于科学证据的训练预防指南。

## 智能提醒，避免垃圾信息

系统仅在以下情况下发送警报：
- 检测到训练量突然增加。
- 训练强度模式异常。
- 达到显著的训练成果。
- 每周总结报告准备完成。

并非每次训练都会发送警报——这正是Strava的核心功能。

## 请求频率限制

- 每次检查最多发送1-2次API请求。
- Strava允许用户每15分钟发送100次请求，每天最多1000次。
- 每天的检查操作大约消耗30次请求。