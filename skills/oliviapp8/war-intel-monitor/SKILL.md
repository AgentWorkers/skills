---
name: war-intel-monitor
description: 实时战争情报监控与紧急警报系统，专为冲突地区设计。适用于用户需要追踪军事冲突、接收紧急警报、监控疏散方案或在战时情况下评估安全风险的情况。该系统支持基于位置的威胁评估功能，可计算距离军事目标的距离，并具备高度的可定制性。
---
# 战争情报监控系统

实时冲突监控系统，具备基于位置的威胁评估功能。

## 设置

使用前，请在 `config.json` 中配置用户信息：

```json
{
  "user_location": {
    "name": "Your Location Name",
    "coordinates": [latitude, longitude],
    "shelter_primary": "Nearest shelter location",
    "shelter_secondary": "Backup shelter location"
  },
  "evacuation_target": "Target city/country",
  "known_targets": [
    {"name": "Military Base A", "distance_km": 20, "type": "military"},
    {"name": "Airport", "distance_km": 15, "type": "infrastructure"},
    {"name": "Port", "distance_km": 25, "type": "infrastructure"}
  ],
  "emergency_contacts": {
    "police": "emergency number",
    "ambulance": "emergency number",
    "embassy": "embassy number"
  }
}
```

## 监控工作流程

### 1. 设置 Cron 任务

创建两个监控任务：

**紧急监控（每 30 分钟一次）**
```
Execute war intel monitoring:
1. Search latest news: [conflict keywords]
2. Check for red alert keywords (airspace closed, missile launch, air raid, explosion)
3. If emergency detected, send alert immediately
4. Include distance from user location for each target mentioned

Alert format:
🚨 [RED ALERT] {event}
📍 Distance from you: ~{X}km
⚡ Immediate actions: {actions}
📊 Next 24-72h forecast: {prediction}
```

**每日简报（每天三次）**
```
Generate daily briefing:
1. Search past 6 hours news
2. Check airspace status
3. Query flight prices and availability to evacuation target
4. Provide risk assessment and recommendations
```

### 2. 警报等级

| 等级 | 触发条件 | 应对措施 |
|-------|---------|----------|
| 🔴 红色 | 领空关闭、导弹发射、直接攻击 | 立即寻找避难所，执行相应行动指令 |
| 🟡 黄色 | 军事集结、外交关系破裂、油价上涨超过 10% | 做好准备，密切监视相关信号 |
| 🟢 绿色 | 常规监控 | 每日接收简报 |

### 3. 警报模板

```
🚨 [ALERT LEVEL] {Event Type}

📍 Location: {target_name}
📏 Distance from you: ~{distance}km

⚡ Immediate Actions:
1. {action_1}
2. {action_2}
3. {action_3}

📊 Situation Assessment:
{brief_analysis}

🔗 Source: {source}
```

### 4. 简报模板

```
📋 Daily Briefing - {date}

🎯 Situation Summary:
{overview}

📍 Recent Incidents (with distances):
| Target | Distance | Status |
|--------|----------|--------|
| {name} | {km}km | {status} |

✈️ Evacuation Options:
- Flight availability: {status}
- Prices: {price_range}
- Recommendation: {recommendation}

🛡️ Risk Assessment: {level}
{reasoning}
```

## 安全指南

### 避难优先选择
1. 地下停车场或地下室
2. 带有窗户但墙壁坚固的浴室
3. 内部走廊（远离外墙）
4. 最底层的内室

### 应急物品清单
- [ ] 护照及复印件
- [ ] 现金（当地货币及美元）
- [ ] 手机 + 充电器 + 电源银行
- [ ] 水瓶
- [ ] 高热量零食
- [ ] 工作手套（用于清理碎片）
- [ ] 手电筒
- [ ] 基本急救用品
- [ ] 重要文件

### 遇到攻击时
1. 立即远离窗户
2. 如果听到爆炸声，立即趴倒在地面上
3. 保护头部和颈部
4. 等待 10-15 秒后再移动
5. 检查是否有受伤情况，然后评估周围环境

## 信息来源

### 官方来源（优先级）
- 国家应急管理机构
- 国防部声明
- 大使馆警报
- 民用航空管理部门

### 开源情报（OSINT）来源
- FlightRadar24（领空状况）
- MarineTraffic（航运路线）
- 经核实的新闻机构
- 政府官方社交媒体

### 经济指标
- 石油价格（布伦特原油/WTI）
- 货币汇率波动
- 预测市场（Polymarket）
- 航班价格趋势

## 自定义设置

编辑 `config.json` 以自定义以下内容：
- 您的位置和坐标
- 已知的军事/基础设施目标及其距离
- 疏散目的地
- 紧急联系人
- 本地语言的警报关键词