---
name: whoop
description: **访问 Whoop 可穿戴设备中的健康数据（睡眠、恢复状况、身体压力、心率变异性 HRV、锻炼记录）并生成交互式图表**  
当用户询问睡眠质量、恢复评分、身体压力水平、心率变异性趋势或锻炼数据时，可以使用该功能；同时，用户也可以通过 Whoop 设备获取健康相关的可视化图表。
---

# Whoop

通过 Whoop API 查询健康指标，并生成交互式的 HTML 图表。

## 设置（仅首次使用）

### 1. 创建一个 Whoop 开发者应用

1. 访问 [developer-dashboard.whoop.com](https://developer-dashboard.whoop.com)
2. 使用您的 Whoop 账户凭据登录
3. 如果有提示，创建一个团队（名称随意）
4. 点击 **创建应用**（或访问 [apps/create](https://developer-dashboard.whoop.com/apps/create)）
5. 填写以下信息：
   - **应用名称**：任意名称（例如：“Clawdbot”）
   - **权限范围**：选择 ALL：`read:recovery`, `read:cycles`, `read:workout`, `read:sleep`, `read:profile`, `read:body_measurement`
   - **重定向 URI**：`http://localhost:9876/callback`
6. 点击 **创建** — 您将获得一个 **客户端 ID** 和 **客户端密钥**

### 2. 进行身份验证

使用您的凭据运行 OAuth 登录流程：

```bash
python3 scripts/whoop_auth.py login \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

这将打开一个浏览器页面以进行 Whoop 授权。登录并批准访问权限。令牌会存储在 `~/.clawdbot/whoop-tokens.json` 文件中，并自动更新。

检查状态：`python3 scripts/whoop_auth.py status`

## 获取数据

使用 `scripts/whoop_data.py` 获取 JSON 数据：

```bash
# Sleep (last 7 days default)
python3 scripts/whoop_data.py sleep --days 14

# Recovery scores
python3 scripts/whoop_data.py recovery --days 30

# Strain/cycles
python3 scripts/whoop_data.py cycles --days 7

# Workouts
python3 scripts/whoop_data.py workouts --days 30

# Combined summary with averages
python3 scripts/whoop_data.py summary --days 7

# Custom date range
python3 scripts/whoop_data.py sleep --start 2026-01-01 --end 2026-01-15

# User profile / body measurements
python3 scripts/whoop_data.py profile
python3 scripts/whoop_data.py body
```

输出结果将以 JSON 格式显示在标准输出（stdout）中。解析这些数据以回答用户的问题。

## 生成图表

使用 `scripts/whoop_chart.py` 生成交互式的 HTML 可视化图表：

```bash
# Sleep analysis (performance + stages)
python3 scripts/whoop_chart.py sleep --days 30

# Recovery bars (color-coded green/yellow/red)
python3 scripts/whoop_chart.py recovery --days 30

# Strain & calories trend
python3 scripts/whoop_chart.py strain --days 90

# HRV & resting heart rate trend
python3 scripts/whoop_chart.py hrv --days 90

# Full dashboard (all 4 charts)
python3 scripts/whoop_chart.py dashboard --days 30

# Save to specific file
python3 scripts/whoop_chart.py dashboard --days 90 --output ~/Desktop/whoop.html
```

图表会自动在默认浏览器中打开。这些图表使用了 Chart.js 库，支持深色主题、数据卡片和工具提示。

## 回答问题

| 用户问题 | 操作 |
|-----------|--------|
| “我的睡眠情况如何？” | `whoop_data.py summary --days 7`，报告睡眠表现和时长 |
| “我的恢复情况如何？” | `whoop_data.py recovery --days 7`，报告恢复状况和趋势 |
| “显示过去一个月的图表” | `whoop_chart.py dashboard --days 30` |
| “我的心率变异性（HRV）有改善吗？” | `whoop_data.py recovery --days 30`，分析趋势 |
| “我这周训练了多少？” | `whoop_data.py workouts --days 7`，列出训练活动 |

## 关键指标

- **恢复情况**（0-100%）：绿色表示 ≥67%，黄色表示 34-66%，红色表示 <34%
- **压力水平**（0-21）：基于心率（HR）的每日劳累程度评分
- **睡眠表现**：实际睡眠时间与所需睡眠时间的对比
- **心率变异性（HRV）**（毫秒）：数值越高，恢复效果越好；可随时间跟踪变化
- **静息心率（RHR）**（每分钟跳动次数）：数值越低，心血管健康状况越好

## 健康分析

当用户询问他们的健康状况、数据趋势或需要相关见解时，请参考 `references/health_analysis.md`：
- 基于科学依据的心率变异性（HRV）、静息心率（RHR）、睡眠阶段、恢复情况、压力水平的解读
- 不同年龄和健康水平下的正常范围
- 数据模式识别（工作日影响、睡眠不足、过度训练的信号）
- 基于数据的可操作建议
- 需要就医的警示信号

### 分析工作流程
1. 获取数据：`python3 scripts/whoop_data.py summary --days N`
2. 阅读 `references/health_analysis.md` 以了解数据解读方法
3. 采用五步分析流程：状态 → 趋势 → 模式 → 见解 → 警示
4. 始终注明：本内容不构成医疗建议

## 参考资料

- `references/api.md` — API 终端详情、响应格式和分页规则
- `references/health_analysis.md` — 基于科学依据的健康数据分析指南