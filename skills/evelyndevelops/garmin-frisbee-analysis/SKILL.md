---
name: garmin-frisbee-analysis
description: Ultimate Frisbee性能分析工具，由Garmin数据提供支持。你可以询问诸如“在昨天的比赛中我完成了多少次冲刺？”、“我在得分间隙的恢复速度是否足够快？”、“我比上次比赛时更疲劳吗？”等问题。该工具能够分析冲刺次数与疲劳程度、最高速度、心率区间、身体能量储备（Body Battery）、心率变异性（HRV）趋势以及睡眠质量，并生成交互式仪表盘。你可以对比不同比赛之间的数据、训练与比赛的表现，同时追踪整个赛季的体能变化。专为竞技级Ultimate Frisbee选手设计。
version: 1.1.1
author: Evelyn & Claude
homepage: https://github.com/EvelynDevelops/garmin-frisbee-analysis
metadata: {"clawdbot":{"emoji":"🥏","requires":{"env":["GARMIN_EMAIL","GARMIN_PASSWORD"]},"install":[{"id":"garminconnect","kind":"python","package":"garminconnect","label":"Install garminconnect (pip)"},{"id":"fitparse","kind":"python","package":"fitparse","label":"Install fitparse (pip)"},{"id":"gpxpy","kind":"python","package":"gpxpy","label":"Install gpxpy (pip)"},{"id":"garmin-auth","kind":"shell","command":"python3 scripts/garmin_auth.py login","label":"Authenticate with Garmin Connect"}]}}
---
# Garmin Frisbee 分析工具

本工具专为终极飞盘（Ultimate Frisbee）运动员设计，用于分析他们的健康和运动数据。可生成交互式 HTML 仪表板，用于赛后回顾、赛事疲劳追踪、训练负荷优化以及整个赛季的数据趋势对比。

## 两种安装方式

1. **Clawdbot Skill**（本指南推荐）——与 Clawdbot 结合使用，支持自然语言查询和主动监控。
2. **MCP 服务器**（[参见 MCP 设置指南](references/mcp_setup.md)——与 Claude Desktop 配合使用，作为 MCP 服务器。

---

## 首次设置

### 1. 安装依赖库

```bash
pip3 install garminconnect fitparse gpxpy
```

### 2. 配置凭据

> **安全提示**：切勿将密码直接写入 `config.json` 文件并提交。建议使用环境变量进行存储。

#### 推荐的环境变量设置方法：

在您的 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`）中添加以下内容：

```bash
export GARMIN_EMAIL="your-email@example.com"
export GARMIN_PASSWORD="your-password"
```

或者通过 Clawdbot 的技能设置进行配置：

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

### 3. 进行身份验证

```bash
python3 scripts/garmin_auth.py login
python3 scripts/garmin_auth.py status   # verify
```

---

## 飞盘数据分析脚本

### 比赛/训练后分析

可深入分析单次运动数据，包括冲刺次数、速度、心率区间等。

**仪表板包含：**
- 综合信息：运动时长、距离、冲刺次数、最高速度、冲刺疲劳指数、高强度运动距离。
- 速度时间线，标注冲刺峰值。
- 冲刺峰值速度趋势（用于检测疲劳：后期冲刺是否变慢？）
- 心率区间分布（1–6 区）。

**冲刺判断标准**：速度超过 14.4 公里/小时且持续时间达到 2 秒以上。

**冲刺疲劳指数**：最后 3 次冲刺峰值除以前 3 次冲刺峰值。若结果小于 0.85，则表示存在明显疲劳。

---

### 比赛回顾仪表板

提供多日赛事的全面数据概览：疲劳曲线、比赛强度、心率恢复情况以及夜间睡眠质量（通过心率变异性 HRV 进行评估）。

**仪表板包含：**
- 赛事期间身体疲劳变化曲线（包含赛前基线数据）。
- 每场比赛的平均/最高心率对比。
- 比赛后的心率恢复曲线（30 分钟时间段，所有比赛数据叠加显示）。
- 每个比赛夜间的睡眠时长及 HRV 数据。
- 所有检测到的运动记录。

---

### 数据对比分析

可对比不同训练课程、比赛或整个赛季的数据。

**活动分类**依据名称关键词：
- 比赛：`game`、`match`、`tournament`、`vs`、`finals`
- 训练：`practice`、`training`、`train`、`drill`、`scrimmage`

**仪表板包含：**
- 随时间变化的最高速度趋势（训练和比赛数据以不同颜色区分显示）。
- 每项活动的平均心率（按强度分类显示）。
- 每项活动当天的晨间 HRV 数据。
- 运动量趋势（时长和距离随时间的变化情况）。
- 完整的活动记录表。

---

## 其他 Garmin 数据分析

--- 

## 健康数据图表

--- 

## 常见问题解答

| 玩家问题 | 对应脚本 | 报告内容 |
|-------------|--------|----------------|
| “我完成了多少次冲刺？” | `frisbee_activity.py --latest` | 冲刺次数、冲刺疲劳指数 |
| “我的最高速度是多少？” | `frisbee_activity.py --latest` | 综合信息中的最高速度（单位：公里/小时） |
| “比赛结束时我是否感到疲劳？” | `frisbee_activity.py --latest` | 如果冲刺疲劳指数小于 0.85，则表示疲劳 |
| “我的心率升高了多久？” | `frisbee_activity.py --latest` | 心率处于第 4–6 区间的时间占比 |
| “我在比赛间隙恢复得够快吗？” | `frisbee_tournament.py` | 通过心率恢复曲线判断 |
| “我是否为比赛做好了准备？” | `frisbee_tournament.py` | 比赛前身体疲劳状况 |
| “我的训练强度够高吗？” | `frisbee_compare.py --mode cross` | 训练和比赛时的平均心率对比 |
| “这个赛季我的表现有进步吗？” | `frisbee_compare.py --mode season` | 最高速度和 HRV 变化趋势 |
| “比赛期间的睡眠质量如何？” | `frisbee_tournament.py` | 睡眠恢复情况图表 |

---

## 数据来源（Garmin 265S）

| 可获取的指标 | 数据来源 |
|--------|-----------|
| 冲刺次数和速度 | ✅ 来自 Garmin 的 FIT 文件分析 |
| 最高速度 | ✅ FIT 文件中的 `speed` 字段 |
| 冲刺疲劳指数 | ✅ 根据速度时间序列计算得出 |
| 心率区间 | ✅ 来自 Garmin 的 HR 数据 |
| 心率恢复（HRR） | ✅ 日内心率变化数据 |
| 身体疲劳指数（Body Battery） | ✅ 来自 Garmin 的 API |
| 睡眠质量（HRV） | ✅ 来自 Garmin 的 API |
| 总运动距离 | ✅ FIT 文件 + Garmin API 数据 |
| 高强度运动距离 | ✅ 根据速度阈值计算得出 |
| 接地时间 | ❌ 需要使用 HRM-Run Pod（非手腕设备） |

---

## 关键飞盘数据指标解释

### 冲刺疲劳指数
最后 3 次冲刺峰值速度与前 3 次的比值：大于等于 0.95 表示状态稳定；介于 0.85–0.95 之间表示略有下降；小于 0.85 表示疲劳明显。该指标可用于判断比赛过程中速度是否下降。

### 心率恢复（HRR）
比赛结束后心率下降的速度。下降越快，说明心血管健康状况越好，恢复能力越强。在多日赛事中，如果后期比赛的 HRR 曲线较为平缓，则表示累积疲劳。

### 身体疲劳指数（0–100）
赛前值是判断运动准备状态的关键指标：大于等于 70 表示状态良好；50–69 表示可以正常比赛；小于 50 表示表现可能受到影响。

### 心率区间
- **第 4 区（70–80% 最大心率）**：表示持续的高强度运动。
- **第 5–6 区（80–100% 最大心率）**：表示爆发性冲刺或激烈的比赛场景。
- 训练中频繁出现第 4–6 区表示训练强度足够。

---

## 常见问题解决方法

- **“FIT 文件下载失败”**：检查活动 ID，某些活动类型可能不支持 FIT 文件导出。
- **未检测到冲刺**：可能是活动数据中未包含速度信息，或者使用了非 GPS 模式的设备。
- **HRR 曲线为空**：可能是当天没有心率数据；请确认 Garmin 设置中已启用“全天心率监测”功能。
- **活动分类错误**：请使用如“game vs X”或“practice”等关键词为活动命名。
- **令牌过期**：重新运行 `python3 scripts/garmin_auth.py login` 命令进行登录。

---

## 隐私政策

- 凭据信息存储在本地文件 `~/.clawdbot/garmin-tokens.json` 中。
- 所有数据仅传输到 Garmin 的官方服务器。
- 可通过 `rm ~/.clawdbot/garmin-tokens.json` 文件删除令牌。

---

## 参考资料

- `references/api.md` — Garmin Connect API 详细信息
- `references/health_analysis.md` — 数据指标的科学解读
- `references/mcp_setup.md` — Claude Desktop 的 MCP 设置指南

---

## 版本信息

- **版本**：1.0.0
- **创建时间**：2026-03-11
- **更新时间**：2026-03-11
- **作者**：Evelyn & Claude
- **许可证**：MIT 许可证
- **依赖库**：garminconnect, fitparse, gpxpy