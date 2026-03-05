---
name: whoop-lab
version: 1.0.0
description: "**功能说明：**  
用于获取、分析、绘制图表并跟踪 WHOOP 健康数据（包括恢复情况、心率变异性（HRV）、静息心率（RHR）、睡眠质量、身体压力水平以及锻炼情况）。  
**适用场景：**  
- 查询任何 WHOOP 指标；  
- 生成可视化图表或仪表板；  
- 规划、监控或报告健康相关实验（支持自动记录基线数据及锻炼后的数据变化）；  
- 将统计信息记录到 Obsidian 数据库中；  
- 将健康数据与个人生活状况关联起来进行分析；  
- 主动识别潜在的恢复趋势异常（如恢复速度减缓）。  
**技术特性：**  
- 支持 OAuth 认证和令牌刷新机制；  
- 全历史数据的分页查询功能；  
- 提供基于科学依据的指标解读（例如：不同年龄段的心率变异性范围、过度训练的预警信号、睡眠阶段的参考目标、药物使用对健康数据的影响等）。"
metadata:
  openclaw:
    emoji: "💪"
    homepage: https://www.paulbrennaman.me/lab/whoop-skill
    requires:
      bins:
        - python3
        - git
---
# WHOOP 技能

通过 WHOOP 开发者 API（v2）获取、解析、绘制图表并跟踪您的 WHOOP 数据。

## 数据目录

所有用户特定的数据都存储在 `~/.config/whoop-skill/` 中——该目录与技能安装目录分开，且安装目录为只读模式。

```
~/.config/whoop-skill/
  credentials.json   — OAuth tokens (created by auth.py on first setup)
  experiments.json   — experiment tracking data (created on first `plan` command)
  config.json        — optional path/timezone overrides (copy from config.example.json)
```

当您运行 `scripts/auth.py` 时，该目录和 `credentials.json` 会自动创建。您无需手动创建它们。

## 设置

> **开始之前：** 此技能需要一个 WHOOP 开发者应用程序来与 WHOOP API 进行身份验证。该应用程序是免费的，设置过程大约需要 2 分钟。

### 第 0 步 — 安装 Python 依赖项

```bash
pip install -r requirements.txt
```

### 第 1 步 — 选择回调方法

在创建 WHOOP 应用程序之前，先决定如何处理 OAuth 回调：

**选项 A — 本地服务器** （本地安装）
- **重定向 URI：** `http://localhost:8888/callback`
- 会在您的机器上运行一个临时服务器来自动捕获重定向请求
- 需要在安装 OpenClaw 的同一台机器上使用浏览器

**选项 B — 手动粘贴代码** （远程/云安装）
- **重定向 URI：** `http://localhost:8888/callback`
- 脚本会打印出一个授权 URL——在任意浏览器中打开该 URL，完成授权后，复制重定向 URL 中的 `?code=` 值并粘贴回脚本中
- 所有数据都不会通过任何外部服务器传输——完全独立运行

### 第 2 步 — 创建 WHOOP 开发者应用程序

1. 访问 https://developer-dashboard.whoop.com
2. 使用您的 WHOOP 账户登录
3. 如果有提示，创建一个团队（名称随意）
4. 点击 **创建应用程序** 并填写以下信息：
   - **应用程序名称：** 任意名称（例如 “我的 WHOOP 技能”）
   - **重定向 URI：** 第 1 步中选择的 URI（选项 A 或 B）
   - **权限范围：** 选择所有 `read:*` 权限范围 + `offline`
5. 复制您的 **客户端 ID** 和 **客户端密钥**——在下一步中会用到它们

### 第 3 步 — 运行设置脚本

```bash
python3 scripts/auth.py
```

此脚本将：
1. 请求您的客户端 ID 和客户端密钥
2. 询问您在第 1 步中选择了哪种回调方法（本地服务器或手动方式）
3. 指导您完成授权流程
4. 将凭据保存到 `~/.config/whoop-skill/credentials.json` 中

**自定义路径（可选）：**
将 `config.example.json` 从技能根目录复制到 `~/.config/whoop-skill/config.json`，并进行编辑以覆盖默认设置：
```json
{
  "creds_path": "~/.config/whoop-skill/credentials.json",
  "vault_path": "~/my-obsidian-vault",
  "daily_notes_subdir": "Daily Notes",
  "timezone": "America/New_York",
  "logged_by": "Assistant"
}
```

## 工作流程

1. 从 `~/.config/whoop-skill/credentials.json` 中加载凭据
2. 如果 `expires_at` 的时间已经过去（或在 60 秒内），运行 `scripts/refresh_token.py` 以获取新的访问令牌并更新文件
3. 调用相应的 API 端点（详见 `references/api.md`）
4. 以通俗易懂的方式解析并展示数据

## 常见请求

- **“我今天的恢复情况如何？”** → 获取最新的恢复分数、心率变异性（HRV）和心率（RHR）
- **“我昨晚的睡眠质量如何？”** → 获取最新的睡眠数据（表现百分比、睡眠阶段、持续时间）
- **“我今天的身体压力有多大？”** → 获取最新的身体压力指标和平均心率
- **“显示我最近的锻炼记录”** → 通过 `/activity/workout` 获取过去 5–7 天的锻炼记录
- **“给我一个健康总结”** → 结合恢复情况、睡眠数据和今天的身体压力指标来生成健康总结

## 令牌刷新

当访问令牌过期时，运行 `scripts/refresh_token.py`。该脚本会自动读取/写入 `~/.config/whoop-skill/credentials.json`。

如果要重新进行身份验证，请再次运行 `scripts/auth.py`。

## API 基本 URL

`https://api.prod.whoop.com/developer/v2`

所有请求都需要添加以下授权头：`Authorization: Bearer <access_token>`

有关端点详情、权限范围和响应格式的详细信息，请参阅 `references/api.md`。完整的官方 API 文档（包括错误代码和速率限制）请访问 https://developer.whoop.com/api。

---

## 数据获取 (`scripts/fetch.py`)

这是一个通用的 API 数据获取脚本，供其他脚本内部使用。

```bash
# Latest recovery
python3 scripts/fetch.py /recovery --limit 1

# Last 30 days of sleep
python3 scripts/fetch.py /activity/sleep --limit 30

# Workouts last 7 days
python3 scripts/fetch.py /activity/workout --limit 7

# Date-range fetch
python3 scripts/fetch.py /recovery --start 2026-02-01 --end 2026-02-28

# User profile
python3 scripts/fetch.py /user/profile/basic
```

输出结果以 JSON 格式显示在标准输出（stdout）中。

---

## 数据图表化 (`scripts/chart.py`)

使用 Chart.js（通过 CDN 提供）生成自包含的 HTML 图表。图表采用深色主题，包含平均值/最小值/最大值以及趋势箭头。图表会自动在浏览器中打开。

### 图表类型

| 图表类型 | 描述 |
|-------|-------------|
| `recovery` | 根据恢复分数用绿色/黄色/红色进行颜色编码的条形图 |
| `sleep` | 每晚的快速眼动（REM）/深度睡眠/浅度睡眠/清醒时间的堆叠条形图 |
| `hrv` | 带有 7 天滚动平均值的折线图 |
| `strain` | 带有卡路里作为次要轴的条形图 |
| `dashboard` | 同时显示四种图表的 2×2 网格布局 |

### 使用方法

```bash
# Recovery chart (30 days)
python3 scripts/chart.py --chart recovery --days 30

# Full dashboard
python3 scripts/chart.py --chart dashboard --days 30 --output ~/whoop-dashboard.html

# HRV trend (90 days), don't auto-open
python3 scripts/chart.py --chart hrv --days 90 --no-open

# Sleep breakdown
python3 scripts/chart.py --chart sleep --days 14

# Strain + calories
python3 scripts/chart.py --chart strain --days 21
```

### 参数说明

| 参数 | 默认值 | 描述 |
|------|---------|-------------|
| `--chart` | （必选） | 图表类型：恢复、睡眠、心率变异性（HRV）、身体压力、仪表盘 |
| `--days` | 30 | 要获取的历史数据天数 |
| `--output` | `/tmp/whoop-<chart>.html` | 输出文件路径 |
| `--no-open` | false | 不在浏览器中自动打开图表 |

### 图表生成（务必执行这两步）

运行 `chart.py` 后，脚本会将输出文件路径打印到标准输出。务必执行以下操作：
1. **将 HTML 文件附加到 Telegram 消息中**——以便远程用户立即收到图表
2. **在浏览器中自动打开图表**（默认设置，除非指定了 `--no-open`）——以便本地用户也能立即查看图表

这样无论是在本地还是远程，用户都能轻松使用该功能。该文件是自包含的、静态的，且安全可共享——不包含任何凭据或 API 调用。

---

## 实验跟踪 (`scripts/experiment.py`)

用于定义、监控和评估个人的健康实验。数据存储在 `~/.config/whoop-skill/experiments.json` 中。

### 支持的指标

`hrv`（心率变异性）、`recovery`（恢复情况）、`sleep_performance`（睡眠表现）、`rhr`（心率）、`strain`（身体压力）

### 命令

#### 规划新的实验
```bash
python3 scripts/experiment.py plan \
  --name "No alcohol for 30 days" \
  --hypothesis "HRV will increase 10%+ from baseline" \
  --start 2026-03-01 \
  --end 2026-03-31 \
  --metrics hrv,recovery,sleep_performance
```

系统会自动从 `--start` 之前的 14 天开始捕获基线数据。您也可以手动进行覆盖：
```bash
python3 scripts/experiment.py plan \
  --name "Cold plunge experiment" \
  --hypothesis "RHR will drop 3+ bpm" \
  --start 2026-03-10 --end 2026-04-10 \
  --metrics hrv,rhr \
  --baseline-hrv 45.0 \
  --baseline-rhr 58
```

#### 带有训练后数据分段的实验规划

当您的假设与训练后的恢复情况有关时，使用 `--segment-workouts` 参数。该工具会获取您的锻炼记录，识别符合条件的锻炼，并仅在每次锻炼后的 24–48 小时内测量恢复指标。

```bash
python3 scripts/experiment.py plan \
  --name "My supplement experiment" \
  --hypothesis "Post-strength recovery improves 10%+ vs baseline" \
  --start YYYY-MM-DD --end YYYY-MM-DD \
  --metrics hrv,recovery,rhr \
  --segment-workouts \
  --min-strain 5
```

参数说明：
- `--segment-workouts` — 启用训练后数据分段模式
- `--min-strain <float>` — 符合条件的最低身体压力阈值（默认值：5.0）。该参数用于过滤掉散步或瑜伽等轻度活动。
- `--days-after <range>` — 测量恢复期的时间范围，例如 `1-2`（锻炼后的第 1 和第 2 天）或 `1`（仅第二天）。默认值：`1-2`。

启用分段模式后，`status` 和 `report` 会显示两种视图：所有时间的整体平均值以及训练后的恢复情况。评估结果会基于训练后的数据。

#### 为现有实验添加分段

```bash
python3 scripts/experiment.py add-segmentation \
  --id <id> \
  --min-strain 5 \
  --days-after 1-2
```

修改已创建的实验以添加训练后数据分段，并根据新的时间段重新计算训练后的基线数据。

#### 列出所有实验
```bash
python3 scripts/experiment.py list
```

#### 检查实验进度
```bash
python3 scripts/experiment.py status --id <id>
```
显示当前平均值与基线的对比结果（包括百分比变化和趋势箭头）。如果启用了分段模式，还会显示整体情况和训练后的具体情况。

#### 最终报告
```bash
python3 scripts/experiment.py report --id <id>
```
提供完整的对比结果（是否达到目标、部分达到目标、未达到目标或无法确定），以及通俗易懂的总结。评估结果基于训练后的数据。

---

## Obsidian 日志记录 (`scripts/log_to_obsidian.py`) （可选）

> **此功能是完全可选的。** 如果您不使用 Obsidian，可以跳过此部分——其余功能仍然可以正常使用。要启用该功能，请在 `~/.config/whoop-skill/config.json` 中设置 `vault_path` 为您的 Obsidian 仓库目录。如果未配置仓库，脚本将不会执行相关操作。

> **注意：** 虽然脚本声明依赖于 `git`，但实际上只有在您的 Obsidian 仓库是 Git 仓库时才会调用 git 命令。如果仓库目录中没有 `.git` 文件，脚本会检测到这一点并仅写入每日日志，而不会执行任何 git 操作——因此实际上并不需要 git。

脚本会将今天的 WHOOP 数据添加到 Obsidian 的每日日志中，文件路径为：
`<vault_path>/Daily Notes/YYYY-MM-DD.md`（通过 `vault_path` 在 `~/.config/whoop-skill/config.json` 中配置）

写入日志后，脚本会执行 `git add -A && git commit && git push` 来提交和推送更改。

### 使用方法

```bash
# Log today
python3 scripts/log_to_obsidian.py

# Backfill a specific date
python3 scripts/log_to_obsidian.py --date 2026-03-01

# Preview without writing
python3 scripts/log_to_obsidian.py --dry-run
```

### 日志输出格式

```markdown
## 🏋️ WHOOP

| Metric | Value |
|--------|-------|
| Recovery | 82% 💚 |
| HRV | 54ms |
| Resting HR | 58 bpm |
| Sleep Performance | 91% |
| Sleep Duration | 7h 42m |
| Day Strain | 8.4 |

_Logged by Assistant at 7:15 AM ET_
```

- 如果每日日志不存在，则创建新的日志文件
- 如果 WHOOP 相关内容已经存在，则直接跳过该操作
- 该操作是幂等的——可以多次执行而不会产生问题

---

## 早晨简报集成

将以下代码片段添加到 `HEARTBEAT.md` 中，以便在早晨简报中包含 WHOOP 的恢复情况和心率变异性数据。

```markdown
## 🏋️ WHOOP Morning Check

Run on heartbeats between 06:00–10:00 ET:

1. Run: `python3 scripts/fetch.py /recovery --limit 1`
2. Extract `records[0].score.recovery_score` and `records[0].score.hrv_rmssd_milli`
3. Include in morning message:

   > 🏋️ **WHOOP** — Recovery: {score}% {emoji} | HRV: {hrv}ms
   > 
   > _(Green 💚 = push hard. Yellow 💛 = moderate. Red 🔴 = rest day.)_

4. If recovery < 34 (red), mention it proactively even if the user hasn't asked.
5. If Obsidian logging is configured, also run: `python3 scripts/log_to_obsidian.py`
```

**HEARTBEAT.md 的代码片段：**

```markdown
### WHOOP (run once, 06:00–10:00 ET)
- Fetch recovery: `python3 scripts/fetch.py /recovery --limit 1`
- Parse recovery_score + hrv_rmssd_milli from records[0].score
- Report: "🏋️ Recovery: {score}% | HRV: {hrv}ms" (add 💚/💛/🔴 based on score ≥67 / ≥34 / <34)
- If red recovery, mention proactively
- Log to Obsidian (if configured): `python3 scripts/log_to_obsidian.py`
```

---

## 健康数据分析

请参阅 `references/health_analysis.md`，其中包含以下内容的科学依据解释：
- 不同年龄段的 HRV（心率变异性）范围及其含义、趋势说明
- 根据健康水平解读静息心率
- 睡眠阶段的详细信息（深度睡眠/快速眼动/浅度睡眠的目标及影响）
- 恢复分数区间（绿色/黄色/红色）及推荐措施
- 身体压力等级及其与恢复情况的关联
- 血氧饱和度（SpO2）和皮肤温度的参考信息
- 过度训练的识别方法
- 何时需要就医的建议

---

## 参考资料

- `references/api.md` — 完整的 WHOOP API 端点参考
- `references/health_analysis.md` — 健康指标解读指南
- WHOOP 开发者控制台：https://developer-dashboard.whoop.com
- WHOOP API 文档：https://developer.whoop.com/api