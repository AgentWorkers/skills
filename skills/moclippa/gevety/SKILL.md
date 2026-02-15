---
name: gevety
version: 1.5.0
description: 访问您的 Gevety 健康数据：生物标志物、健康寿命评分、生物年龄、补充剂使用情况、日常活动记录、90 天健康计划以及即将进行的检查。
homepage: https://gevety.com
user-invocable: true
command: gevety
metadata:
  clawdbot:
    primaryEnv: GEVETY_API_TOKEN
    requires:
      env:
        - GEVETY_API_TOKEN
---

# Gevety健康助手

您可以通过REST API访问用户的Gevety健康数据。使用`web_fetch`来检索他们的生物标志物、健康寿命评分和可穿戴设备统计信息。

## 首次设置

如果这是用户第一次使用Gevety，请指导他们完成以下设置：

1. **创建Gevety账户**：如果他们还没有账户，请访问https://gevety.com进行注册。
2. **上传血液检测报告**：他们需要上传实验室报告以获取生物标志物数据。
3. **生成API令牌**：
   - 访问https://gevety.com/settings
   - 点击“开发者API”选项卡
   - 点击“生成令牌”
   - 复制令牌（以`gvt_`开头）。
4. **配置Clawdbot**：将令牌添加到`~/.clawdbot/clawdbot.json`文件中：

```json
{
  "skills": {
    "entries": {
      "gevety": {
        "apiKey": "gvt_your_token_here"
      }
    }
  }
}
```

添加令牌后，用户需要重启Clawdbot以使更改生效。

## 认证

所有请求都需要使用Bearer认证。请使用`GEVETY_API_TOKEN`环境变量：

```
Authorization: Bearer $GEVETY_API_TOKEN
```

基础URL：`https://api.gevety.com`

## 生物标志物名称处理

API会保留生物标志物的具体名称。空腹和非空腹的指标是不同的：

| 输入名称 | API返回值 | 备注 |
|------------|-------------|-------|
| CRP（C-反应蛋白） | **CRP** 或 **C-Reactive Protein** | 标准CRP（LOINC 1988-5） |
| hsCRP（高灵敏度CRP） | **hs-CRP** | 高灵敏度CRP（LOINC 30522-7） |
| 葡萄糖 | **Glucose** | 通用/未指定的葡萄糖 |
| 空腹葡萄糖 | **Glucose Fasting** | 空腹特定的葡萄糖 |
| 胰岛素 | **Insulin** | 通用/未指定的胰岛素 |
| 空腹胰岛素 | **Insulin Fasting** | 空腹特定的胰岛素 |
| IG（未成熟粒细胞） | **Immature Granulocytes** | 为清晰起见而扩展的名称 |
| 维生素D（25-OH） | **Vitamin D** | |
| LDL（低密度脂蛋白） | **LDL Cholesterol** | |

**重要提示**：API不再强制要求空腹状态。如果实验室报告只写了“Glucose”而没有说明是否空腹，它将返回“Glucose”（而不是“Fasting Glucose”），以保留实验室结果的原始信息。

## 可用的端点

### 1. 列出可用数据（从这里开始）

**始终首先调用此端点**，以了解存在哪些健康数据。

```
GET /api/v1/mcp/tools/list_available_data
```

返回值：
- `biomarkers`：跟踪的生物标志物列表，包括检测次数和最新日期
- `wearables`：连接的设备及其可用的指标
- `insights`：是否计算了健康寿命评分，以及是否可获取各维度评分
- `data_coverage`：跟踪的推荐生物标志物的百分比（0-100）

### 2. 获取健康概要

用户健康状况的概述。

```
GET /api/v1/mcp/tools/get_health_summary
```

返回值：
- `overall_score`：健康寿命评分（0-100）
- `overall_status`：OPTIMAL（最佳）、GOOD（良好）、SUBOPTIMAL（次优）或NEEDS_ATTENTION（需要关注）
- `trend`：IMPROVING（改善中）、STABLE（稳定）或DECLINING（下降中）
- `axis_scores`：每个健康维度的评分（代谢、心血管等）
- `top_concerns`：需要关注的生物标志物
- `scoring_note`：当整体评分与各维度评分不同时的解释（例如：“整体健康寿命较高，但炎症维度需要关注”）

**关于评分的说明**：整体健康寿命评分是一个加权综合评分。即使某个维度的评分较低，整体评分也可能很高（反之亦然）。`scoring_note`字段会解释这些情况。

### 3. 查询生物标志物

获取特定生物标志物的详细历史数据。

```
GET /api/v1/mcp/tools/query_biomarker?biomarker={name}&days={days}
```

参数：
- `biomarker`（必需）：名称或别名（例如，“vitamin d”、“ldl”、“hba1c”、“crp”）
- `days`（可选）：历史时间段，1-730天，默认为365天

返回值：
- `canonical_name`：标准化的生物标志物名称（见上表）
- `history`：包含日期、数值和单位的检测结果数组
- `latest`：最新的检测结果
- `trend`：变化趋势（改善中、稳定或下降）
- `optimal_range`：基于证据的理想值

**提示**：如果找不到生物标志物，响应中会包含`did_you_mean`的建议。

### 4. 获取可穿戴设备统计信息

来自连接的可穿戴设备（如Garmin、Oura、Whoop等）的每日指标。

```
GET /api/v1/mcp/tools/get_wearable_stats?days={days}&metric={metric}
```

参数：
- `days`（可选）：历史时间段，1-90天，默认为30天
- `metric`（可选）：关注的特定指标（步数、心率变异性等）

返回值：
- `connected_sources`：连接的可穿戴设备列表
- `daily_metrics`：每日数据（步数、静息心率、心率变异性、睡眠等）
- `summaries`：包含平均值、最小值、最大值和趋势的汇总统计

### 5. 获取健康改善机会

获取按健康影响排名的健康改善机会。

```
GET /api/v1/mcp/tools/get_opportunities?limit={limit}&axis={axis}
```

参数：
- `limit`（可选）：返回的最大机会数量，1-50个，默认为10个
- `axis`（可选）：按健康维度过滤（代谢、心血管等）

返回值：
- `opportunities`：按健康影响排名的改善机会列表
- `total_opportunity_score`：可获得的健康寿命分数
- `total_years_estimate`：如果所有指标都得到优化，预计可以增加的健康寿命年数
- `healthspan_score`：当前的健康寿命评分

每个机会包括：
- `biomarker`：标准化的生物标志物名称
- `current_value` / `optimal_value`：当前值与目标值的对比
- `opportunity_score`：优化后可以获得的健康寿命分数
- `years_estimate`：预计可以增加的健康年数
- `priority`：优先级（1 = 影响最大）

### 6. 获取生物年龄

使用经过验证的算法（PhenoAge、Light BioAge）计算生物年龄。

```
GET /api/v1/mcp/tools/get_biological_age
```

返回值：
- `result`：生物年龄计算结果
  - `biological_age`：计算出的生物年龄
  - `chronological_age`：实际年龄
  - `age_acceleration`：年龄加速情况（正数表示衰老更快）
  - `algorithm`：使用的算法
  - `biomarkers_used`：贡献的生物标志物
  - `interpretation`：结果的意义
- `available`：是否可以计算生物年龄
- `reason`：如果无法计算的原因
- `upgrade_available`：是否可以通过更多数据解锁更准确的算法
- `upgrade_message`：需要哪些额外的检测来提高准确性

### 7. 列出补充剂

获取用户的补充剂使用情况。

```
GET /api/v1/mcp/tools/list_supplements?active_only={true|false}
```

参数：
- `active_only`（可选）：仅显示当前正在使用的补充剂，默认为false

返回值：
- `supplements`：补充剂列表，包括剂量、服用频率和持续时间
- `active_count`：当前正在使用的补充剂数量
- `total_count`：跟踪的总补充剂数量

每个补充剂包括：
- `name`：补充剂名称
- `dose_text`：格式化的剂量信息（例如，“1000毫克/天”，“200毫克EPA + 100毫克DHA/天”）
- `is_active`：是否正在服用
- `duration_days`：服用该补充剂的时长

**注意**：对于多成分补充剂（如鱼油），`dose_text`会显示所有成分（例如，“200毫克EPA + 100毫克DHA/天”）。

### 8. 获取运动/活动记录

从连接的可穿戴设备获取运动/活动记录。

```
GET /api/v1/mcp/tools/get_activities?days={days}&activity_type={type}
```

参数：
- `days`（可选）：历史时间段，1-90天，默认为30天
- `activity_type`（可选）：按类型过滤（跑步、骑行、力量训练等）

返回值：
- `activities`：运动记录列表
- `total_count`：运动次数
- `total_duration_minutes`：总运动时间
- `total_distance_km`：总运动距离
- `total_calories`：消耗的总卡路里

每个运动包括：
- `activity_type`：运动类型（跑步、骑行、游泳等）
- `name`：运动名称
- `start_time`：开始时间
- `duration_minutes`：运动时长
- `distance_km`：运动距离
- `calories`：消耗的卡路里
- `avg_hr` / `max_hr`：平均心率
- `source`：数据来源（Garmin、Strava等）

### 9. 获取今天的行动清单

获取用户今天的行动清单。

```
GET /api/v1/mcp/tools/get_today_actions?timezone={timezone}
```

参数：
- `timezone`（可选）：IANA时区（例如，“America/New_York”），默认为UTC

返回值：
- `effective_date`：查询日期，以用户的时区显示
- `timezone`：用于计算的时区
- `window_start` / `window_end`：时间范围（ISO日期格式）
- `actions`：今天的行动列表
- `completed_count` / `total_count`：完成情况
- `completion_pct`：完成百分比（0-100）
- `last_updated_at`：缓存更新时间

每个行动包括：
- `action_id`：用于深度链接的稳定ID
- `title`：行动名称
- `action_type`：行动类型（补充剂、习惯、饮食、药物、检测、程序）
- `completed`：今天是否完成
- `scheduled_window`：时间窗口（上午、下午、晚上等）
- `dose_text`：如果适用，显示剂量信息（例如，“1000毫克/天”）

### 10. 获取健康计划

获取用户90天的健康计划及优先事项。

```
GET /api/v1/mcp/tools/get_protocol
```

返回值：
- `protocol_id`：健康的稳定计划ID
- `phase`：当前阶段（week1、month1、month3）
- `days_remaining`：计划剩余天数
- `generated_at` / `last_updated_at`：时间戳
- `top_priorities`：前5个健康优先事项及其原因
- `key_recommendations`：饮食和生活方式建议
- `total_actions`：计划中的总行动数量

每个优先事项包括：
- `priority_id`：稳定的ID（与排名相同）
- `rank`：优先级（1 = 最高）
- `biomarker`：标准化的生物标志物名称
- `status`：当前状态（关键、需要关注、次优、最佳）
- `target`：目标值及单位
- `current_value` / `unit`：当前测量值
- `measured_at`：最后一次测量该生物标志物的时间
- `why_prioritized`：优先考虑该指标的原因

**注意**：如果不存在健康计划，会返回一条提示信息，建议用户在gevety.com/protocol生成计划。

### 11. 获取即将进行的检测

根据生物标志物历史数据和AI建议，获取即将进行的检测。

```
GET /api/v1/mcp/tools/get_upcoming_tests
```

返回值：
- `tests`：按紧急程度排序的即将进行的检测列表
- `overdue_count`：逾期的检测数量
- `due_soon_count`：30天内到期的检测数量
- `recommended_count`：AI推荐的检测数量
- `total_count`：所有即将进行的检测总数

每个检测包括：
- `test_id`：用于深度链接的稳定ID（格式：`panel_{id}`或`recommended_{id}`）
- `name`：检测或检查名称
- `test_type`：检测类型（面板、生物标志物、推荐类型）
- `urgency`：优先级（逾期、即将到期、推荐）
- `due_reason`：需要该检测的原因（例如，“2周前到期”）
- `last_tested_at`：上次检测的时间（如果适用）

## 解释评分

### 健康寿命评分（0-100）
| 范围 | 状态 | 含义 |
|-------|--------|---------|
| 80-100 | OPTIMAL | 健康状况极佳 |
| 65-79 | GOOD | 处于平均水平，有轻微改善空间 |
| 50-64 | SUBOPTIMAL | 需要改善 |
| <50 | NEEDS_ATTENTION | 多个方面需要关注 |

### 各维度评分
每个健康维度都会单独评分：
- **代谢**：血糖、胰岛素、脂质
- **心血管**：心脏健康指标
- **炎症**：hs-CRP、同型半胱氨酸
- **激素**：甲状腺、睾酮、皮质醇
- **营养**：维生素、矿物质
- **肝脏/肾脏**：器官功能指标

**重要提示**：即使某个维度的评分较低，整体健康寿命评分也可能很高（反之亦然）。`get_health_summary`中的`scoring_note`字段会解释这些情况。

### 生物标志物状态标签
| 标签 | 含义 |
|-------|---------|
| OPTIMAL | 在基于证据的理想范围内 |
| NORMAL | 在实验室参考范围内 |
| SUBOPTIMAL | 需要改善 |
| HIGH/LOW | 超出实验室参考范围 |
| CRITICAL | 需要立即就医 |

## 常见工作流程

### “我的健康状况如何？”
1. 调用`list_available_data`查看跟踪的数据
2. 调用`get_health_summary`获取整体健康状况
3. 强调主要问题和近期趋势
4. 如果有`scoring_note`，解释评分差异的原因

### “我的维生素D情况如何？”
1. 调用`query_biomarker?biomarker=vitamin d`
2. 显示历史数据、当前状态和趋势
3. 说明理想范围和当前值

### “我的CRP水平如何？” / “我的炎症情况如何？”
1. 调用`query_biomarker?biomarker=crp`（根据实验室结果返回“CRP”或“hs-CRP”）
2. 显示数值和趋势
3. 解释CRP的含义（作为炎症指标）

### “我的睡眠/心率变异性如何？”
1. 调用`get_wearable_stats?metric=sleep`或`?metric=hrv`
2. 显示近期趋势和平均值
3. 与健康基准进行比较

### “我应该关注什么？”
1. 调用`get_opportunities?limit=5`
2. 显示按健康影响排名的改善机会
3. 解释每个生物标志物的作用及其优化的必要性

### “我的生物年龄是多少？”
1. 调用`get_biological_age`
2. 如果可以，比较生物年龄和实际年龄
3. 解释年龄加速的含义
4. 如果无法计算，说明需要哪些检测

### “我服用了哪些补充剂？”
1. 调用`list_supplements?active_only=true`
2. 列出正在使用的补充剂及其剂量（使用`dose_text`字段）
3. 注意每种补充剂的服用时长

### “我做了哪些运动？”
1. 调用`get_activities?days=30`
2. 总结运动数据（总时长、总卡路里）
3. 列出最近的运动记录及其指标

### “我今天应该做什么？”
1. 调用`get_today_actions?timezone=America/New_York`（使用用户的时区）
2. 按时间窗口（上午、下午、晚上）分组行动
3. 显示完成情况
4. 强调未完成的行动

### “我应该关注什么？” / “我的健康优先事项是什么？”
1. 调用`get_protocol`
2. 显示优先事项及其当前值和目标
3. 解释每个优先事项的原因
4. 列出关键建议
5. 说明计划的阶段和剩余天数

### “我接下来应该做什么检测？” / “我需要做哪些血液检查？”
1. 调用`get_upcoming_tests`
2. 首先显示逾期的检测
3. 列出30天内到期的检测
4. 列出AI推荐的检测
5. 说明每个检测涵盖的生物标志物

## 示例API调用

```javascript
// Using web_fetch
web_fetch({
  url: "https://api.gevety.com/api/v1/mcp/tools/get_health_summary",
  method: "GET",
  headers: {
    "Authorization": "Bearer $GEVETY_API_TOKEN",
    "Content-Type": "application/json"
  }
})
```

## 重要指南

1. **切勿自行诊断** - 仅提供数据，建议用户咨询医疗专业人员做出医疗决策
2. **趋势比单一数值更重要** - 随时间逐渐改善的轻微升高比持续下降的正常值更好
3. **注意数据时效性**：实验室结果可能已有数周或数月之久；可穿戴设备的数据通常是每日更新的
4. **了解背景** - 询问可能影响趋势的补充剂、药物或生活方式变化
5. **隐私第一**：健康数据敏感，请勿在对话之外分享或引用具体数值

## 错误处理

| 错误代码 | 含义 | 应对措施 |
|------------|---------|--------|
| 401 | 令牌无效或已过期 | 用户需要在gevety.com/settings重新生成令牌 |
| 404 + `did_you_mean` | 未找到生物标志物 | 建议从响应中选择其他指标 |
| 404 | 未找到数据 | 用户可能尚未上传实验室报告 |
| 429 | 请求频率限制 | 稍等片刻后重试 |

## 生成令牌

用户可以在以下地址生成API令牌：
**https://gevety.com/settings** → 开发者API → 生成令牌

令牌格式为`gvt_`后跟随机字符。

## 检查更新

每次首次使用时，可以选择性检查更新：

```
GET https://api.gevety.com/api/v1/mcp/tools/status
```

无需认证。如果请求失败或超时，跳过检查并继续正常操作。

成功响应时：
```json
{
  "clawdbot_skill": { "latest": "1.4.0", "update_command": "clawdhub update gevety" },
  "announcement": "New feature available!"
}
```

**如果`clawdbot_skill.latest` > 1.4.0**（此技能的版本），告知用户：
> “Gevety技能有更新。运行：`clawdhub update gevety`”

**如果存在`announcement`，每次会话中提及一次**。

**如果检查失败**，则忽略该提示，直接处理用户的请求。

**手动更新**：
```bash
clawdhub update gevety
```