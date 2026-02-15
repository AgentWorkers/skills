---
name: tesla-smart-charge
description: 智能特斯拉充电调度器，具备充电量限制管理功能。该工具每天会运行一次以检查调度文件，并仅在预设的日期进行充电。在充电过程中（默认为100%），以及充电结束后（默认为80%），系统会自动管理充电量限制。适用于以下场景：  
(1) 在特定计划好的日期为特斯拉充电；  
(2) 为保护电池健康而设置充电量限制；  
(3) 计算最佳的充电开始时间；  
(4) 设置每日自动检查机制，并实现灵活的充电计划安排。
---

# 特斯拉智能充电优化器

该工具可帮助您安排特斯拉汽车的充电计划，以在指定时间达到目标电池电量百分比。它通过 cron 任务每日运行，检查调度文件，并仅在预设的日期进行充电。

## 安全性与依赖项

**必备条件：**
- 环境变量：`TESLA_EMAIL`（您的特斯拉账户邮箱）
- 必需安装并正确配置 `tesla` 技能，该技能需包含特斯拉 API 凭据

**安全改进（v1.1.0 及以上版本）：**
- ✅ 无 shell 注入风险：使用参数列表而非 `shell=True`
- ✅ 邮箱验证：在使用前会验证 `TESLA_EMAIL` 的有效性
- ✅ 输入验证：充电百分比必须在 0-100% 的范围内
- ✅ 安全的环境变量传递：凭据通过环境变量传递，而非字符串插值
- ✅ 明确的依赖关系：元数据中声明了所需的环境变量和技能依赖项

## 快速入门

### 1. 设置充电计划

复制示例调度文件：

```bash
cp skills/tesla-smart-charge/references/tesla-charge-schedule-example.json \
   memory/tesla-charge-schedule.json
```

使用您的充电计划日期编辑 `memory/tesla-charge-schedule.json` 文件：

```json
{
  "charges": [
    {
      "date": "2026-02-01",
      "target_battery": 100,
      "target_time": "08:00"
    },
    {
      "date": "2026-02-03",
      "target_battery": 80,
      "target_time": "07:00"
    }
  ]
}
```

## Cron 配置（推荐）

### 选项 1：每日午夜检查（简单模式）

```bash
clawdbot cron add \
  --name "Tesla daily charge check" \
  --schedule "0 0 * * *" \
  --task "TESLA_EMAIL=your@email.com python3 /path/to/skills/tesla-smart-charge/scripts/tesla-smart-charge.py --check-schedule"
```

### 选项 2：每日检查 + 会话管理（推荐）

为了更好地管理充电限制，建议同时运行以下两个任务：
- **午夜执行（初始化每日充电计划）：**
```bash
clawdbot cron add \
  --name "Tesla daily charge check" \
  --schedule "0 0 * * *" \
  --task "TESLA_EMAIL=your@email.com python3 /path/to/skills/tesla-smart-charge/scripts/tesla-smart-charge.py --check-schedule"
```

- **在充电时段内每 30 分钟执行一次（管理充电会话限制）：**
```bash
clawdbot cron add \
  --name "Tesla session management" \
  --schedule "*/30 8-23 * * *" \
  --task "TESLA_EMAIL=your@email.com python3 /path/to/skills/tesla-smart-charge/scripts/tesla-smart-charge.py --manage-session"
```

第二个任务确保全天充电限制得到正确更新：
- ✅ 在充电会话期间：保持电池电量在 100%（或用户指定的百分比）；
- ✅ 会话结束后：将电池电量限制设置为 80%（或用户指定的百分比），以保护电池健康。

## 工作原理

**每天午夜（或 cron 任务运行时）：**
1. 脚本会检查 `memory/tesla-charge-schedule.json` 文件。
2. 如果当天日期在充电计划列表中，则执行充电计划：
   - 获取当前电池电量；
   - 计算最佳开始时间；
   - **将充电限制设置为会话期间的限制（默认为 100%）**；
   - 显示充电详情；
   - 显示**下一次预定充电日期**。
3. 如果当天没有充电计划，则将充电限制设置为 80%（默认值）；
   - 仍然会显示**下一次预定充电日期**。

**会话管理：**
- **充电会话期间**：充电限制为 `charge_limit_percent`（默认为 100%）；
- **充电会话结束后**：充电限制为 `post_charge_limit_percent`（默认为 80%）。

**效果：** 通过一个 cron 任务同时处理充电和限制管理，无需为每个日期创建单独的任务！

## 调度文件格式

```json
{
  "charges": [
    {
      "date": "2026-02-01",
      "target_battery": 100,
      "target_time": "08:00",
      "charge_limit_percent": 100,
      "post_charge_limit_percent": 80
    },
    {
      "date": "2026-02-03",
      "target_battery": 80,
      "target_time": "07:00",
      "charge_limit_percent": 100,
      "post_charge_limit_percent": 80
    }
  ]
}
```

**字段说明：**
- `date`：YYYY-MM-DD 格式（充电时间）；
- `target_battery`：目标电池电量百分比（默认为 100%）；
- `target_time`：充电应完成的小时:分钟（默认为 08:00）；
- `charge_limit_percent`：充电会话期间的限制百分比（默认为 100%，可选）；
- `post_charge_limit_percent`：充电会话结束后的限制百分比（默认为 80%，可选）。

## 环境变量配置

### 配置特斯拉账户邮箱

```bash
export TESLA_EMAIL="your@email.com"
```

### 可选：自定义充电功率

默认值：2.99 千瓦（家用充电器，约 13 安培，230 伏特）

您可以在 cron 任务中或手动调用时进行调整：

```bash
--charger-power 3.7      # 16A @ 230V
--charger-power 7.4      # 32A @ 230V (dual-phase)
```

## 命令

### 检查今天的充电计划

```bash
TESLA_EMAIL="your@email.com" python3 scripts/tesla-smart-charge.py --check-schedule
```

**输出结果：**
- ✅ 如果有充电计划：显示充电计划、充电限制及下一次充电日期；
- ❌ 如果没有充电计划：显示下一次预定充电日期，并将充电限制设置为 80%。

### 管理当前充电会话

```bash
TESLA_EMAIL="your@email.com" python3 scripts/tesla-smart-charge.py --manage-session
```

此命令用于管理当前的充电会话：
- **在充电会话期间**：将充电限制设置为会话期间的限制；
- **充电会话结束后**：将充电限制设置为会话结束后的限制；
- **如果没有充电会话**：将充电限制设置为 80%。

**提示：** 建议在充电期间每小时或每 30 分钟运行此命令，以实现实时限制管理。

### 显示所有预定充电计划

```bash
python3 scripts/tesla-smart-charge.py --show-schedule
```

### 显示上次充电计划

```bash
python3 scripts/tesla-smart-charge.py --show-plan
```

## 示例

### 每日充电 100%（周一至周五）

```json
{
  "charges": [
    {"date": "2026-02-02", "target_battery": 100, "target_time": "08:00"},
    {"date": "2026-02-03", "target_battery": 100, "target_time": "08:00"},
    {"date": "2026-02-04", "target_battery": 100, "target_time": "08:00"},
    {"date": "2026-02-05", "target_battery": 100, "target_time": "08:00"},
    {"date": "2026-02-06", "target_battery": 100, "target_time": "08:00"}
  ]
}
```

### 为保护电池健康，每 3 天充电 80%

```json
{
  "charges": [
    {"date": "2026-02-01", "target_battery": 80, "target_time": "07:00"},
    {"date": "2026-02-04", "target_battery": 80, "target_time": "07:00"},
    {"date": "2026-02-07", "target_battery": 80, "target_time": "07:00"}
  ]
}
```

### 可变目标电量百分比

```json
{
  "charges": [
    {"date": "2026-02-01", "target_battery": 100, "target_time": "08:00"},
    {"date": "2026-02-02", "target_battery": 80, "target_time": "07:00"},
    {"date": "2026-02-03", "target_battery": 60, "target_time": "06:00"}
  ]
}
```

## 充电时间估算

充电时间计算公式如下：

```
energy_needed_kwh = (battery_capacity × (target - current) / 100) / charge_efficiency
charge_time_hours = energy_needed_kwh / charger_power_kw
start_time = target_time - charge_time_hours - margin_minutes
```

其中：
- `battery_capacity`：车辆电池容量（千瓦时，默认为 75 千瓦时）；
- `charger_power_kw`：充电器功率（千瓦，默认为 2.99 千瓦）；
- `charge_efficiency`：充电效率（约 0.92）；
- `margin_minutes`：达到目标电量前的缓冲时间（默认为 5 分钟）。

**示例：** 电池容量为 75 千瓦时，当前电量为 50%，使用 2.99 千瓦的充电器在 08:00 充电至 100%：
- 所需电量：(75 × 50% / 100) / 0.92 = 40.8 千瓦时；
- 充电时间：40.8 / 2.99 ≈ 13.6 小时；
- 开始时间：前一天 08:00 - 13.6 小时 - 5 分钟 ≈ 前一天 18:25。

## 工作流程提示

- **添加新的充电计划：** 修改 `memory/tesla-charge-schedule.json` 文件，cron 任务会在下次运行时自动更新；
- **提前规划：** 可提前几周添加充电计划，脚本会自动处理日期逻辑；
- **只需一个 cron 任务**：无需为每个日期创建单独的任务；
- **查看下次充电计划：** 每次运行时都会显示下一次预定充电日期。

## 参数说明

**手动使用 `--target-time` 参数时：**

```bash
python3 scripts/tesla-smart-charge.py \
  --target-time "HH:MM" \
  --target-battery 100 \
  --charger-power 2.99 \
  --battery-capacity 75 \
  --margin-minutes 5
```

**使用 `--check-schedule` 参数时：** 从 JSON 文件中读取充电计划信息。

## 参考资料**
- **CRON_SETUP.md**：完整的 cron 集成指南；
- **API_REFERENCE.md**：高级参数和计算公式；
- **tesla-charge-schedule-example.json**：调度文件模板。