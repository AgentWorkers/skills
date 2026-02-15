---
name: garmin-health-analysis
description: 以自然的方式与您的 Garmin 设备进行交流：“我滑雪时的最快速度是多少？”、“我昨晚的睡眠质量如何？”、“下午 3 点我的心率是多少？”您可以查看 20 多种健康指标（睡眠阶段、身体能量储备、心率变异性、最大摄氧量、训练状态、身体成分、血氧饱和度），下载 FIT/GPX 文件以进行路线分析，随时查询海拔高度和行进速度，并生成交互式的健康仪表盘。从简单的“显示我本周的训练记录”到深入的“分析我的恢复情况与训练负荷”，Garmin 设备都能满足您的各种需求。
version: 1.2.2
author: EversonL & Claude
homepage: https://github.com/eversonl/ClawdBot-garmin-health-analysis
metadata: {"clawdbot":{"emoji":"⌚","requires":{"env":["GARMIN_EMAIL","GARMIN_PASSWORD"]},"install":[{"id":"garminconnect","kind":"python","package":"garminconnect","label":"Install garminconnect (pip)"},{"id":"fitparse","kind":"python","package":"fitparse","label":"Install fitparse (pip)"},{"id":"gpxpy","kind":"python","package":"gpxpy","label":"Install gpxpy (pip)"}]}}
---

# 加明健康分析（Garmin Health Analysis）

从Garmin Connect查询健康指标，并生成交互式的HTML图表。

## 两种安装方式

本技能支持**两种不同的设置方式**：

1. **Clawdbot技能**（本指南推荐）——与Clawdbot结合使用，实现自动化和主动健康监测
2. **MCP服务器**（[参见MCP设置指南](references/mcp_setup.md)——与标准Claude Desktop结合使用，作为MCP服务器

请选择符合您使用场景的安装方式。您也可以同时使用这两种方式！

---

## Clawdbot技能设置（仅首次使用）

### 1. 安装依赖库

```bash
pip3 install garminconnect
```

### 2. 配置凭据

您有三种方式来提供Garmin Connect的凭据：

#### 选项A：Clawdbot配置（推荐——通过UI配置）

将凭据添加到`~/.clawdbot/clawdbot.json`文件中：

```json
{
  "skills": {
    "entries": {
      "garmin-health-analysis": {
        "enabled": true,
        "env": {
          "GARMIN_EMAIL": "your-email@example.com",
          "GARMIN_PASSWORD": "your-password"
        }
      }
    }
  }
}
```

**提示**：您也可以通过Clawdbot的技能设置面板来设置这些凭据。

#### 选项B：本地配置文件

在技能目录下创建一个配置文件：

```bash
cd ~/.clawdbot/skills/garmin-health-analysis
# or: cd <workspace>/skills/garmin-health-analysis
cp config.example.json config.json
# Edit config.json and add your email and password
```

**config.json**文件内容：
```json
{
  "email": "your-email@example.com",
  "password": "your-password"
}
```

**注意**：`config.json`文件被Git忽略，以保护您的凭据安全。

#### 选项C：命令行

在认证时直接传递凭据：
```bash
python3 scripts/garmin_auth.py login \
  --email YOUR_EMAIL@example.com \
  --password YOUR_PASSWORD
```

### 3. 认证

登录Garmin Connect并保存会话令牌：

```bash
python3 scripts/garmin_auth.py login
```

系统会优先使用以下来源的凭据：
1. 命令行参数（`--email`、`--password`）
2. 本地配置文件（`config.json`）
3. 环境变量（`GARMIN_EMAIL`、`GARMIN_PASSWORD`）
4. Clawdbot配置文件（`skills.entries.garmin-health-analysis.env`）

会话令牌存储在`~/.clawdbot/garmin-tokens.json`文件中，并会自动刷新。

检查认证状态：
```bash
python3 scripts/garmin_auth.py status
```

## 获取数据

使用`scripts/garmin_data.py`获取JSON数据：

```bash
# Sleep (last 7 days default)
python3 scripts/garmin_data.py sleep --days 14

# Body Battery (Garmin's recovery metric)
python3 scripts/garmin_data.py body_battery --days 30

# HRV data
python3 scripts/garmin_data.py hrv --days 30

# Heart rate (resting, max, min)
python3 scripts/garmin_data.py heart_rate --days 7

# Activities/workouts
python3 scripts/garmin_data.py activities --days 30

# Stress levels
python3 scripts/garmin_data.py stress --days 7

# Combined summary with averages
python3 scripts/garmin_data.py summary --days 7

# Custom date range
python3 scripts/garmin_data.py sleep --start 2026-01-01 --end 2026-01-15

# User profile
python3 scripts/garmin_data.py profile
```

输出结果为JSON格式，直接输出到标准输出（stdout）。解析这些数据以回答用户的问题。

## 生成图表

使用`scripts/garmin_chart.py`生成交互式的HTML可视化图表：

```bash
# Sleep analysis (hours + scores)
python3 scripts/garmin_chart.py sleep --days 30

# Body Battery recovery chart (color-coded)
python3 scripts/garmin_chart.py body_battery --days 30

# HRV & resting heart rate trends
python3 scripts/garmin_chart.py hrv --days 90

# Activities summary (by type, calories)
python3 scripts/garmin_chart.py activities --days 30

# Full dashboard (all 4 charts)
python3 scripts/garmin_chart.py dashboard --days 30

# Save to specific file
python3 scripts/garmin_chart.py dashboard --days 90 --output ~/Desktop/garmin-health.html
```

图表会自动在默认浏览器中打开。这些图表使用了Chart.js库，具有现代的渐变设计、统计卡片和交互式工具提示。

## 回答问题

| 用户问题 | 操作 |
|-----------|--------|
| “我昨晚的睡眠情况如何？” | `garmin_data.py summary --days 1`，报告睡眠时长和评分 |
| “我这周的恢复情况如何？” | `garmin_data.py body_battery --days 7`，报告平均恢复情况和趋势 |
| “显示我上个月的健康状况” | `garmin_chart.py dashboard --days 30` |
| “我的心率变异性（HRV）有改善吗？” | `garmin_data.py hrv --days 30`，分析变化趋势 |
| “我这周进行了哪些锻炼？” | `garmin_data.py activities --days 7`，列出锻炼详情 |
| “我的静息心率是多少？” | `garmin_data.py heart_rate --days 7`，报告平均静息心率及变化趋势 |

## 关键指标

### 体细胞能（Body Battery，0-100分）
Garmin基于心率变异性（HRV）、压力、睡眠和活动情况的专有恢复指标：
- **高（75-100分）**：完全恢复，适合高强度活动
- **中（50-74分）**：能量中等，适合日常活动
- **低（25-49分）**：能量不足，需要恢复
- **非常低（0-24分）**：能量耗尽，应优先休息

### 睡眠评分（Sleep Score，0-100分）
根据睡眠时长、睡眠阶段和睡眠干扰情况评估的整体睡眠质量：
- **优秀（90-100分）**：恢复效果最佳
- **良好（80-89分）**：睡眠质量一般，但存在小问题
- **一般（60-79分）**：睡眠质量尚可，但有待改善
- **较差（0-59分）**：睡眠质量严重不足

### 心率变异性（HRV）
以毫秒为单位测量，数值越高通常表示恢复能力越好：
- 反映神经系统平衡和恢复能力
- 可以跟踪随时间的变化趋势（数值上升表示恢复情况改善）
- 受睡眠、压力、训练负荷和健康状况的影响
- 正常范围因人而异（20-200+毫秒）

### 静息心率（Resting Heart Rate，bpm）
通常情况下，心率越低表示心血管健康状况越好：
- **运动员**：40-60 bpm
- **健康成年人**：60-70 bpm
- **普通成年人**：70-80 bpm
- 心率突然升高可能表示压力、疾病或过度训练

### 压力水平（Stress Levels）
根据全天的心率变异性分析：
- **低压力**：处于休息和恢复状态
- **中等压力**：进行日常活动时
- **高压力**：处于高强度身体活动或精神压力状态

## 健康分析

当用户需要了解健康状况或趋势时，请参考`references/health_analysis.md`：
- 所有指标的科学依据解读
- 不同年龄和健康水平的正常范围
- 模式检测（每周趋势、恢复周期、训练负荷平衡）
- 基于数据的实用建议
- 需要休息或就医的警告信号

### 分析流程
1. 获取数据：`python3 scripts/garmin_data.py summary --days N`
2. 阅读`references/health_analysis.md`以了解分析框架
3. 应用分析框架：状态 → 趋势 → 模式 → 活动洞察 → 建议
4. 始终注明：本工具提供的信息仅供参考，不构成医疗建议

## 故障排除

### 认证问题
- **“凭据无效”**：请重新核对电子邮件/密码，或尝试直接登录Garmin Connect网站
- **“令牌过期”**：重新运行登录命令：`python3 scripts/garmin_auth.py login ...`
- **“请求过多”**：Garmin设置了请求限制；请等待几分钟后再试

### 数据缺失
- 某些指标需要特定的Garmin设备（例如，体细胞能指标需要支持HRV功能的设备）
- 如果未佩戴设备，历史数据可能存在缺失
- 新账户可能没有完整的历史记录

### 库问题
- 如果`garminconnect`导入失败：`pip3 install --upgrade garminconnect`
- Garmin偶尔会更新API；如果请求失败，请更新相关库

## 隐私声明

- 凭据存储在本地文件`~/.clawdbot/garmin-tokens.json`中
- 会话令牌会自动刷新
- 数据仅发送到Garmin的官方服务器
- 您可以随时通过删除`garmin-tokens.json`文件来撤销访问权限

## 对比：Garmin vs Whoop

| 功能 | Garmin | Whoop |
|---------|--------|-------|
| **恢复指标** | 体细胞能（0-100分） | 恢复评分（0-100%） |
| **心率变异性（HRV）跟踪** | 支持（夜间平均值） | 支持（详细数据） |
| **睡眠阶段** | 轻度睡眠、深度睡眠、REM睡眠、清醒状态 | 轻度睡眠、SWS睡眠、REM睡眠、清醒状态 |
| **活动跟踪** | 内置GPS，支持多种运动模式 | 提供压力评分（0-21分） |
| **压力监测** | 全天压力水平 | 不直接提供 |
| **API** | 非官方API（garminconnect） | 官方OAuth接口 |
| **设备类型** | 手表、健身追踪器 | 仅支持可穿戴手环 |

## 参考资料

- `references/api.md` — Garmin Connect API详细信息（非官方）
- `references/health_analysis.md` — 基于科学的健康数据解读
- [garminconnect库](https://github.com/cyberjunky/python-garminconnect) — Python API封装库
- [Garmin Connect](https://connect.garmin.com) — 官方网站

## 版本信息

- **创建时间**：2026-01-25
- **作者**：EversonL & Claude
- **版本**：1.2.0
- **依赖库**：garminconnect、fitparse、gpxpy（Python库）
- **许可证**：MIT许可证