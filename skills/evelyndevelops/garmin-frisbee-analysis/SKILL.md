---
name: garmin-frisbee-analysis
description: Ultimate Frisbee性能分析工具，由Garmin的数据支持。你可以询问诸如“在昨天的比赛中我完成了多少次冲刺？”、“我在得分间隙的恢复速度是否足够快？”、“我比上次比赛时更疲劳吗？”等问题。该工具能够分析冲刺次数、疲劳程度、最高速度、心率区间、身体能量状态（Body Battery）、心率变异性（HRV）趋势以及睡眠质量，并生成交互式仪表板。你可以对比不同比赛之间的数据、训练与比赛的表现，同时追踪整个赛季的体能变化。专为竞技级别的Ultimate Frisbee运动员设计。
version: 1.0.0
author: Evelyn & Claude
homepage: https://github.com/EvelynDevelops/garmin-frisbee-analysis
metadata: {"clawdbot":{"emoji":"🥏","requires":{"env":["GARMIN_EMAIL","GARMIN_PASSWORD"]},"install":[{"id":"garminconnect","kind":"python","package":"garminconnect","label":"Install garminconnect (pip)"},{"id":"fitparse","kind":"python","package":"fitparse","label":"Install fitparse (pip)"},{"id":"gpxpy","kind":"python","package":"gpxpy","label":"Install gpxpy (pip)"}]}}
---
# Garmin Frisbee 分析工具

本工具专为 Ultimate Frisbee 运动员设计，用于分析他们的健康数据和运动表现。它能够生成交互式 HTML 仪表板，帮助运动员进行赛后回顾、跟踪比赛疲劳情况、优化训练负荷，并对比整个赛季的数据趋势。

## 两种安装方式

1. **Clawdbot Skill**（本指南推荐的方式）——与 Clawdbot 结合使用，支持自然语言查询和主动监控功能。
2. **MCP 服务器**（[详见 MCP 设置指南](references/mcp_setup.md)——与 Claude Desktop 配合使用，作为 MCP 服务器。

---

## 首次使用前的设置

### 1. 安装依赖库

```bash
pip3 install garminconnect fitparse gpxpy
```

### 2. 配置凭证

#### 选项 A：使用 Clawdbot 进行配置（推荐）

```json
{
  "skills": {
    "entries": {
      "garmin-frisbee-analysis": {
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

#### 选项 B：使用本地配置文件

```bash
cp config.example.json config.json
# Edit config.json with your email and password
```

#### 选项 C：通过命令行配置

```bash
python3 scripts/garmin_auth.py login --email YOUR_EMAIL --password YOUR_PASSWORD
```

### 3. 进行身份验证

```bash
python3 scripts/garmin_auth.py login
python3 scripts/garmin_auth.py status   # verify
```

---

## Frisbee 数据分析脚本

### 比赛/训练后分析

可深入分析单次运动数据，包括冲刺次数、速度、心率区间等。

```bash
# Most recent activity
python3 scripts/frisbee_activity.py --latest

# Specific date
python3 scripts/frisbee_activity.py --date 2026-03-08

# Specific activity ID
python3 scripts/frisbee_activity.py --activity-id 12345678

# Save to file
python3 scripts/frisbee_activity.py --latest --output ~/Desktop/game.html
```

**仪表板包含：**
- 总结信息：运动时长、距离、冲刺次数、最高速度、冲刺疲劳指数、高强度运动距离
- 速度时间线（标出冲刺关键点）
- 冲刺峰值速度趋势（用于判断疲劳情况：后期冲刺速度是否下降）
- 心率区间分布（第 1 区至第 6 区）

**冲刺判定标准**：速度超过 14.4 公里/小时且持续时间达到 2 秒以上。

**冲刺疲劳指数**：最后 3 次冲刺峰值与最初 3 次冲刺峰值的比值。若比值小于 0.85，则表示存在明显疲劳。

---

### 比赛回顾仪表板

提供多日比赛的全面数据概览：疲劳曲线、比赛强度、心率恢复情况以及夜间睡眠质量（通过心率变异性 HRV 指标评估）。

```bash
python3 scripts/frisbee_tournament.py \
  --start 2026-03-08 \
  --end 2026-03-10 \
  --name "Spring Tournament 2026" \
  --output ~/Desktop/tournament.html
```

**仪表板包含：**
- 比赛期间每天的身体疲劳程度（包含比赛前一天的基线数据）
- 每场比赛的平均/最高心率对比
- 比赛后的心率恢复曲线（30 分钟窗口内所有比赛数据叠加显示）
- 每晚的睡眠时长及心率变异性数据
- 所有比赛活动的详细记录

---

### 数据对比分析

支持对比不同训练课程、比赛结果或整个赛季的数据。

```bash
# Training vs training (last 90 days)
python3 scripts/frisbee_compare.py --mode training --days 90

# Game vs game
python3 scripts/frisbee_compare.py --mode tournament --days 180

# Training intensity vs game intensity
python3 scripts/frisbee_compare.py --mode cross --days 60

# Full season overview
python3 scripts/frisbee_compare.py --mode season --days 180

# Save output
python3 scripts/frisbee_compare.py --mode season --days 180 --output ~/Desktop/season.html
```

**活动分类**依据名称关键词进行区分：
- 比赛：`game`、`match`、`tournament`、`vs`、`finals`
- 训练：`practice`、`training`、`train`、`drill`、`scrimmage`

**仪表板包含：**
- 随时间变化的最佳速度趋势（训练和比赛数据以不同颜色显示）
- 每项活动的平均心率（按强度分类）
- 每项活动当天的晨间心率变异性（HRV）数据
- 活动时长和距离的总体趋势
- 完整的活动记录表

---

## 其他 Garmin 数据分析功能

```bash
# Sleep
python3 scripts/garmin_data.py sleep --days 14

# Body Battery
python3 scripts/garmin_data.py body_battery --days 30

# HRV
python3 scripts/garmin_data.py hrv --days 30

# Heart rate
python3 scripts/garmin_data.py heart_rate --days 7

# Activities
python3 scripts/garmin_data.py activities --days 30

# Stress
python3 scripts/garmin_data.py stress --days 7

# Combined summary
python3 scripts/garmin_data.py summary --days 7

# Custom date range
python3 scripts/garmin_data.py sleep --start 2026-01-01 --end 2026-01-15
```

## 健康数据图表

```bash
python3 scripts/garmin_chart.py sleep --days 30
python3 scripts/garmin_chart.py body_battery --days 30
python3 scripts/garmin_chart.py hrv --days 90
python3 scripts/garmin_chart.py activities --days 30
python3 scripts/garmin_chart.py dashboard --days 30
```

---

## 常见问题解答

| 运动员问题 | 对应脚本 | 报告内容 |
|-------------|--------|----------------|
| “我完成了多少次冲刺？” | `frisbee_activity.py --latest` | 冲刺次数、冲刺疲劳指数 |
| “我的最高速度是多少？” | `frisbee_activity.py --latest` | 总结信息中的最高速度（单位：公里/小时） |
| “比赛结束时我是否感到疲劳？” | `frisbee_activity.py --latest` | 冲刺疲劳指数（小于 0.85 表示疲劳） |
| “我的心率升高了多久？” | `frisbee_activity.py --latest` | 心率处于第 4 区至第 6 区的时间占比 |
| “我在比赛间隙恢复得够快吗？” | `frisbee_tournament.py` | 心率恢复曲线对比 |
| “我是否为比赛做好了准备？” | `frisbee_tournament.py` | 比赛前身体疲劳程度 |
| “我的训练强度够高吗？” | `frisbee_compare.py --mode cross` | 训练和比赛期间的平均心率对比 |
| “这个赛季我的表现有进步吗？” | `frisbee_compare.py --mode season` | 最高速度和心率变异性趋势 |
| “比赛期间的睡眠质量如何？” | `frisbee_tournament.py` | 比赛期间的睡眠质量分析 |

---

## 数据来源（Garmin 265S）

| 可获取的数据指标 | 来源 |
|--------|-----------|
| 冲刺次数和速度 | ✅ Garmin FIT 文件分析 |
| 最高速度 | ✅ Garmin FIT 文件中的 `speed` 字段 |
| 冲刺疲劳指数 | ✅ 根据速度时间序列计算得出 |
| 心率区间 | ✅ Garmin FIT 文件中的心率数据及最高心率 |
| 心率恢复（HRV） | ✅ Garmin API 提供的日内心率数据 |
| 身体疲劳程度（Body Battery） | ✅ Garmin API 提供的数据 |
| 睡眠质量（包括睡眠阶段和心率变异性） | ✅ Garmin API 提供的数据 |
| 总运动距离 | ✅ Garmin FIT 文件 + Garmin API 数据 |
| 高强度运动距离 | ✅ 根据速度阈值计算得出 |
| 与地面的接触时间 | ❌ 需要使用 HRM-Run Pod（非手腕式设备） |

---

## 关键指标解释

### 冲刺疲劳指数
最后 3 次冲刺峰值速度与最初 3 次冲刺峰值速度的比值：
- ≥ 0.95：表现稳定
- 0.85–0.95：略有下降
- < 0.85：表示疲劳明显

### 心率恢复（HRV）
比赛结束后心率下降的速度。曲线越陡峭，说明心血管健康状况越好，恢复能力越强；在比赛后期曲线越平缓，表示疲劳累积。

### 身体疲劳程度（0–100 分）
比赛前的身体疲劳程度是判断运动准备状态的关键指标：
- ≥ 70：状态良好，可以参赛
- 50–69：勉强可接受
- < 50：可能影响运动表现

### 心率区间
- **第 4 区（70–80% 最大心率）**：表示持续进行高强度运动
- **第 5–6 区（80–100% 最大心率）**：表示爆发性冲刺或激烈的比赛场景
- 训练中频繁出现第 4–6 区的心率，说明训练强度适中

---

## 常见问题解决

- **“无法下载 Garmin FIT 文件”**：检查活动 ID，某些活动类型可能不支持 FIT 文件导出。
- **未检测到冲刺数据**：可能是活动未包含速度数据，或使用了非 GPS 模式的设备。
- **HRV 曲线为空**：可能是当天没有记录到心率数据，请确保在 Garmin 设置中启用了“全天心率监测”功能。
- **活动分类错误**：请使用如“game vs X”或“practice”等关键词为活动命名。
- **令牌过期**：重新运行 `python3 scripts/garmin_auth.py` 进行登录操作。

---

## 隐私政策

- 凭证信息存储在本地文件 `~/.clawdbot/garmin-tokens.json` 中。
- 所有数据仅传输至 Garmin 的官方服务器。
- 可通过 `rm ~/.clawdbot/garmin-tokens.json` 删除令牌文件。

---

## 参考资料

- `references/api.md`：Garmin Connect API 的详细信息
- `references/health_analysis.md`：基于科学原理的数据解读方法
- `references/mcp_setup.md`：Claude Desktop 的 MCP 设置指南

---

## 版本信息

- **版本**：1.0.0
- **创建时间**：2026-03-11
- **更新时间**：2026-03-11
- **作者**：Evelyn 和 Claude
- **许可证**：MIT 许可证
- **依赖库**：garminconnect、fitparse、gpxpy