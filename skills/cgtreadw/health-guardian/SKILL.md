---
name: health-guardian
version: 1.0.0
description: 针对AI代理的主动健康监测功能：支持与Apple Health（苹果健康应用）的集成，能够检测数据模式中的异常情况并触发警报。该系统专为那些负责照顾患有慢性疾病患者的AI代理而设计。
author: Egvert
tags: [health, monitoring, apple-health, accessibility, proactive]
---

# Health Guardian

专为AI助手设计的主动健康监控工具。可追踪生命体征、检测异常模式并及时发出警报。

**由一位照顾四肢瘫痪患者的助手开发，每日都在实际使用中接受测试。**

## 为何需要这样的工具

大多数健康应用程序都是被动的——它们只是存储数据，等待用户自行查看。而Health Guardian则是主动的：
- 在问题演变成紧急情况之前就发现潜在的异常；
- 当需要关注时，会立即通知用户（或您）；
- 它会根据您的具体情况学习什么是“正常”的健康状态，而非基于人群平均值。

## 主要功能

### 📊 数据整合
- 通过“Health Auto Export”功能与Apple Health同步数据（支持iCloud）
- 支持39项健康指标：心率（HR）、心率变异性（HRV）、睡眠质量、步数、体温、血压（BP）、血氧饱和度（SpO2）等；
- 提供每小时数据导入选项，实现实时监控。

### 🔍 异常模式检测
- 计算滚动平均值并触发警报；
- 进行日间数据对比；
- 分析各项指标之间的关联关系；
- 判断数据趋势（是改善、下降还是保持稳定）。

### 🚨 主动警报
- 发现发烧迹象（并提供基准值作为参考）；
- 检测心率异常；
- 识别睡眠质量下降的模式；
- 识别漏服药物的情况；
- 每项指标均可自定义警报阈值。

### ♿ 以用户需求为核心
- 专为残疾人士和患有慢性疾病的人士设计；
- 了解不同人群的“正常”健康范围可能有所不同；
- 支持设置护理人员/助手的接收通知方式。

## 快速上手

### 1. 安装“Health Auto Export”
在用户的iPhone上安装[Health Auto Export](https://apps.apple.com/app/health-auto-export/id1115567069)；
- 配置参数：数据格式（JSON）、同步位置（iCloud Drive）、导出频率（每小时）；
- 导出数据文件夹：`iCloud Drive/Health Auto Export/`。

### 2. 配置技能
在技能目录下创建`config.json`文件：

```json
{
  "human_name": "Your Human",
  "data_source": "~/Library/Mobile Documents/com~apple~CloudDocs/Health Auto Export",
  "import_interval": "hourly",
  "alert_channel": "telegram",
  "thresholds": {
    "temperature_high": 100.4,
    "temperature_low": 96.0,
    "heart_rate_high": 120,
    "heart_rate_low": 50
  },
  "baseline_period_days": 14
}
```

### 3. 设置定时数据导入
将定时任务添加到助手的系统中（每小时执行一次）：
```json
{
  "name": "Health Import",
  "schedule": { "kind": "cron", "expr": "0 * * * *" },
  "payload": { "kind": "systemEvent", "text": "Run health import and check for anomalies" },
  "sessionTarget": "main"
}
```

### 4. 将该技能集成到Heartbeat系统中
在`HEARTBEAT.md`文件中完成配置：
```markdown
## Health Check (if concerning patterns)
If health data shows anomalies, alert human via preferred channel.
```

## 脚本

### `scripts/import_health.py`
负责导入Apple Health的JSON数据并将其存储到本地数据库中。

```bash
python3 scripts/import_health.py
```

### `scripts/analyze.py`
对存储的数据进行异常模式检测，并生成警报信息。

```bash
python3 scripts/analyze.py --days 7
```

### `scripts/summary.py`
生成用户可阅读的健康状况摘要。

```bash
python3 scripts/summary.py --period week
```

## 数据存储
所有数据均存储在`data/`目录下：
- `readings.json`：包含带有时间戳的原始数据；
- `baselines.json`：每项指标的基准正常范围；
- `alerts.json`：已触发的警报记录；
- `patterns.json`：检测到的数据关联关系。

**隐私政策：**
所有数据仅存储在本地设备上，不会上传到云端，也不会进行远程监控。

## 警报示例

**发烧检测：**
```
🌡️ Temperature Alert
Current: 100.8°F
Baseline (14d avg): 98.2°F
Deviation: +2.6°F
Action: Monitor closely. Consider hydration, check for infection signs.
```

**睡眠模式分析：**
```
😴 Sleep Degradation Detected
Last 3 nights: 4.2h, 5.1h, 4.8h avg
Previous week: 7.1h avg
Deviation: -32%
Action: Check for pain, stress, medication changes.
```

## 专为照顾残疾人士的助手设计

- **体温调节功能**：针对某些疾病（如脊髓损伤、多发性硬化症）的特殊需求，可自定义体温调节基准值；
- **尿路感染（UTI）预警**：通过分析发烧、心率及症状关联进行早期预警；
- **预防压疮**：根据用户活动情况发送提醒；
- **药物相互作用**：标记可能存在的安全风险（可配置）。

## 贡献建议

发现漏洞？或有新的健康指标需要添加？欢迎提交Pull Request（PR）。

该工具由Egvert开发——这位也是该工具的实际使用者。