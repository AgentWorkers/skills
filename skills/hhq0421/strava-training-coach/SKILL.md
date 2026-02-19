---
name: strava-training-coach
description: >
  这款经过安全加固的AI训练辅助工具能够在训练损伤发生之前就提前预防它们。它通过监控Strava数据中的危险里程峰值、训练强度不平衡以及恢复时间不足等问题，然后通过Discord或Slack发送智能提醒。
  适用场景：
  - 监控训练负荷，防止过度训练和受伤
  - 自动生成包含趋势分析的每周训练报告
  - 在每周里程或训练强度出现危险性波动时接收提醒
  - 跟踪长期的健身趋势和恢复模式
  - 在达成重要训练目标（如个人最佳成绩、保持训练连贯性等）时收到通知
  安全特性：
  - 无硬编码的敏感信息——所有凭据均通过环境变量进行管理
  - 对所有外部数据进行输入验证
  - 日志中的敏感数据会被加密处理
  - 通知发送具有速率限制机制
  - 令牌存储具有安全权限控制
  - Webhook URL经过严格验证
homepage: https://developers.strava.com/docs/reference/
metadata: {"clawdbot":{"emoji":"🏃","tags":["fitness","strava","running","injury-prevention","training","alerts","discord","slack","security"],"requires":{"env":["STRAVA_CLIENT_ID","STRAVA_CLIENT_SECRET","DISCORD_WEBHOOK_URL or SLACK_WEBHOOK_URL"]}}}
---
# Strava训练助手  
一个基于人工智能的训练伙伴，能在您察觉之前识别受伤风险。  

## 重要性  
大多数跑步伤害都遵循相同的模式：训练量过大且过于急促。等到您感到疼痛时，损伤已经存在好几天了。这款助手会每天监控您的Strava数据，并在问题演变成伤害之前向您发出警报，帮助您保持训练的连贯性，避免因受伤而被迫中断训练。  

## 功能介绍  
- **急性负荷警报**：每周跑步里程增加30%以上？在您的膝盖感到不适之前，您就会收到通知。  
- **强度监控**：过多的高强度训练会损害恢复能力。  
- **恢复提示**：如果连续休息时间过长，系统会提醒您适当恢复。  
- **智能进步记录**：系统会根据地形和天气条件，准确记录您的进步情况。  
- **每周报告**：不仅显示总里程，还分析每周的训练趋势。  

## 快速入门  
### 1. 连接Strava  
```bash
# Set your Strava API credentials (required)
export STRAVA_CLIENT_ID=your_id
export STRAVA_CLIENT_SECRET=your_secret

# Authenticate (opens browser for OAuth)
python3 scripts/auth.py
```  
您的Strava访问令牌（tokens）会安全地存储在`~/.config/strava-training-coach/`目录中，权限设置为0600。  

### 2. 设置通知（必选）  
**Discord:**  
```bash
export DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
export NOTIFICATION_CHANNEL=discord
```  
**Slack:**  
```bash
export SLACK_WEBHOOK_URL=https://hooks.slack.com/...
export NOTIFICATION_CHANNEL=slack
```  
⚠️ **注意：** Webhook地址必须通过环境变量设置，禁止使用硬编码的URL。  

### 3. （可选）集成Oura  
```bash
export OURA_ENABLED=true
```  
需要使用Oura的CLI进行身份验证。  

### 4. 启动助手  
```bash
# Daily training check + alerts
python3 scripts/coach_check.py

# Weekly summary report  
python3 scripts/weekly_report.py
```  
**建议使用cron任务进行自动化监控：**  
```json
{
  "name": "Training Coach - Daily Check",
  "schedule": {"kind": "every", "everyMs": 86400000},
  "command": "python3 scripts/coach_check.py"
}
```  

## 安全性  
本工具在设计时充分考虑了安全性：  

### 凭据管理  
- **避免硬编码敏感信息**：所有凭据均通过环境变量传递。  
- **安全存储令牌**：令牌以0600权限保存。  
- **符合XDG安全标准**：配置文件存储在`~/.config/strava-training-coach/`。  
- **令牌验证**：使用结构化数据验证令牌的有效性。  

### 输入验证  
- **日期格式检查**：确保日期符合ISO8601标准。  
- **数值范围限制**：所有阈值都有明确的限制。  
- **类型转换**：确保数据类型正确转换。  
- **Webhook地址验证**：验证地址是否符合Discord/Slack的格式要求。  

### 数据保护  
- **日志加密**：敏感数据在日志中会被屏蔽。  
- **临时文件安全**：状态文件具有适当的权限设置。  
- **防止数据泄露**：错误信息经过加密处理。  
- **频率限制**：每种类型的警报每天最多发送1次。  

### 网络安全  
- **仅使用HTTPS**：所有API请求均通过TLS协议传输。  
- **超时处理**：所有请求都有30秒的超时限制。  
- **重试机制**：最多尝试3次，采用指数级退避策略。  
- **证书验证**：使用标准的SSL证书进行验证。  

## 配置  
所有阈值均为可选设置，系统会提供合理的默认值并进行验证。  
```bash
# Training thresholds (validated ranges)
MAX_WEEKLY_MILEAGE_JUMP=30     # 5-100%, default: 30
MAX_HARD_DAY_PERCENTAGE=25     # 5-100%, default: 25
MIN_EASY_RUN_HEART_RATE=145    # 100-200 bpm, default: 145

# Feature flags
OURA_ENABLED=false             # Enable Oura integration
distVERBOse=false              # Enable debug logging
```  

## 示例警报  
### 受伤风险提示  
> “⚠️ 训练负荷警报：每周跑步里程增加45%（从18英里增加到26英里）。每周里程增加超过10%会增加受伤风险，请考虑安排轻松的训练日。”  
> “🫁 训练强度过高：本周有60%的训练属于中等或高强度。轻松的训练日应让心率保持在145次/分钟以下。”  
> “💤 休息日连续5天未运动：建议进行20分钟的散步或瑜伽来帮助恢复。”  

### 成就记录  
> “🎉 新最佳成绩：5公里跑用时22分30秒——这是你今年最快的平地跑步成绩！”  
> “🔥 30天连续运动：持续性的训练比高强度训练更重要。”  
> “✅ 基础训练完成：连续4周进行80/20的轻松训练，可以开始加入更有结构的训练计划。”  

### 每周报告（周日）  
- 实际每周里程与目标里程对比  
- 训练强度分布（轻松/中等/高强度）  
- 近4周的训练趋势  
- 下周的训练建议  

## 训练理念  
- **80/20原则**：80%的时间进行轻松训练，20%的时间进行高强度训练。  
- **每周增幅限制**：每周里程增幅不超过10%。  
- **坚持为先**：定期训练，避免突然加大训练强度。  
- **及早发现风险**：在问题演变成伤害之前及时预警。  

更多关于预防受伤的详细信息，请参阅`references/training-principles.md`。  

## 相关文件  
- `scripts/auth.py`：Strava OAuth配置文件  
- `scripts/coach_check.py`：每日训练分析和警报功能  
- `scripts/weekly_report.py`：每周总结报告  
- `scripts/refresh_token.py`：用于刷新过期令牌的脚本  
- `references/training-principles.md`：受伤预防指南  

## 功能特点  
- **智能提醒**：仅在工作真正重要时才会发送警报（如里程突变、训练强度异常或取得显著进步时）。  
- **避免骚扰**：不会频繁发送不必要的通知（Strava本身就提供了这些功能）。  

## 使用限制  
- 每次检查最多发送1-2次API请求。  
- Strava允许每15分钟发送100次请求，每天最多1000次。  
- 每月的日常检查大约需要30次请求。