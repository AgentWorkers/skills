---
name: gevety
version: 1.6.0
description: 访问您的 Gevety 健康数据——包括生物标志物、健康寿命评分、生物年龄、所服用的补充剂、日常活动记录、90 天健康计划、即将进行的检查、实验室报告以及健康相关内容。
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

您可以通过REST API访问用户的Gevety健康数据。使用`web_fetch`来检索他们的生物标志物、健康寿命评分以及可穿戴设备的统计数据。

## 首次设置

如果这是用户首次使用Gevety，请指导他们完成以下设置：

1. **创建Gevety账户**：如果他们还没有账户，请在https://gevety.com注册。
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

API会保留生物标志物的具体名称。空腹和非空腹的检测结果是有区别的：

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
| LDL（低密度脂蛋白胆固醇） | **LDL Cholesterol** | |

**重要提示**：API不再强制要求空腹检测。如果实验室报告只写了“Glucose”而没有说明是否为空腹检测，系统会返回“Glucose”（而不是“Fasting Glucose”），以保留原始报告的上下文。

## 可用的端点

### 1. 列出可用数据（从这里开始）

**始终首先调用此端点**，以了解有哪些健康数据被跟踪。

```
GET /api/v1/mcp/tools/list_available_data
```

返回内容：
- `biomarkers`：包含检测次数和最新日期的跟踪生物标志物列表
- `wearables`：连接的设备及其可用的指标
- `insights`：健康寿命评分是否已计算以及各健康维度的评分是否可用
- `data_coverage`：跟踪的推荐生物标志物的百分比（0-100）

### 2. 获取健康概览

用户健康状况的概览。

```
GET /api/v1/mcp/tools/get_health_summary
```

返回内容：
- `overall_score`：健康寿命评分（0-100）
- `overall_status`：OPTIMAL（最佳）、GOOD（良好）、SUBOPTIMAL（次优）或NEEDS_ATTENTION（需要关注）
- `trend`：IMPROVING（改善中）、STABLE（稳定）或DECLINING（下降中）
- `axis_scores`：每个健康维度的评分
- `top_concerns`：需要关注的生物标志物
- `scoring_note`：当整体评分与各维度评分不一致时的解释（例如：“整体健康寿命较高，但炎症维度需要关注”）

**关于评分的说明**：整体健康寿命评分是一个加权综合评分。即使某个维度的评分较低，整体评分也可能较高（反之亦然）。`scoring_note`字段会解释这些情况。

### 3. 查询生物标志物

获取特定生物标志物的详细历史数据。

```
GET /api/v1/mcp/tools/query_biomarker?biomarker={name}&days={days}
```

参数：
- `biomarker`（必需）：名称或别名（例如：“vitamin d”、“ldl”、“hba1c”、“crp”）
- `days`（可选）：历史时间段，1-730天，默认为365天

返回内容：
- `canonical_name`：标准化的生物标志物名称（参见上表）
- `history`：包含日期、数值和单位的检测结果数组
- `latest`：最新的检测结果
- `trend`：变化趋势（IMPROVING、STABLE、DECLINING）及变化百分比
- `optimal_range`：基于证据的理想值

**提示**：如果未找到该生物标志物，响应中会包含`did_you_mean`的建议。

### 4. 获取可穿戴设备统计数据

来自连接的可穿戴设备（如Garmin、Oura、Whoop等）的每日指标。

```
GET /api/v1/mcp/tools/get_wearable_stats?days={days}&metric={metric}
```

参数：
- `days`（可选）：历史时间段，1-90天，默认为30天
- `metric`（可选）：关注的特定指标（步数、心率变异性等）

返回内容：
- `connected_sources`：连接的可穿戴设备列表
- `daily_metrics`：每日数据（步数、静息心率、心率变异性、睡眠等）
- `summaries`：包含平均值、最小值、最大值和趋势的汇总统计

### 5. 获取健康改善机会

获取按健康影响排序的健康改善机会。

```
GET /api/v1/mcp/tools/get_opportunities?limit={limit}&axis={axis}
```

参数：
- `limit`（可选）：返回的最大机会数量，1-50个，默认为10个
- `axis`（可选）：按健康维度筛选

返回内容：
- `opportunities`：按健康影响排序的改善机会列表
- `total_opportunity_score`：可获得的健康寿命积分
- `total_years_estimate`：如果所有指标都得到优化后的预计健康寿命
- `healthspan_score`：当前的健康寿命评分

每个机会包括：
- `biomarker`：标准化的生物标志物名称
- `current_value` / `optimal_value`：当前值与理想值
- `opportunity_score`：优化后可以获得的健康寿命积分
- `years_estimate`：预计可以增加的健康寿命年数
- `priority`：优先级（1 = 影响最大）

### 6. 计算生物年龄

使用经过验证的算法（PhenoAge、Light BioAge）计算生物年龄。

```
GET /api/v1/mcp/tools/get_biological_age
```

返回内容：
- `result`：生物年龄计算结果
  - `biological_age`：计算出的生物年龄
  - `chronological_age`：实际年龄
  - `age_acceleration`：年龄加速情况（正数表示衰老更快）
  - `algorithm`：使用的算法
  - `biomarkers_used`：参与计算的生物标志物
  - `interpretation`：结果的意义
- `available`：是否可以计算生物年龄
- `reason`：如果无法计算的原因
- `upgrade_available`：是否可以通过更多数据解锁更准确的算法
- `upgrade_message`：需要哪些额外检测来提高准确性

### 7. 获取补充剂信息

获取用户的补充剂使用情况。

```
GET /api/v1/mcp/tools/list_supplements?active_only={true|false}
```

参数：
- `active_only`（可选）：仅显示当前正在使用的补充剂，默认为false

返回内容：
- `supplements`：包含剂量、服用频率和服用时间的补充剂列表
- `active_count`：当前正在使用的补充剂数量
- `total_count`：总共跟踪的补充剂数量

每个补充剂包括：
- `name`：补充剂名称
- `dose_text`：格式化的剂量信息（例如：“每天1000毫克”）
- `is_active`：是否正在服用
- `duration_days`：服用该补充剂的时长

**注意**：对于多成分补充剂（如鱼油），`dose_text`会显示所有成分的剂量（例如：“每天200毫克EPA + 100毫克DHA”）。

### 8. 获取运动记录

获取来自连接的可穿戴设备的运动记录。

```
GET /api/v1/mcp/tools/get_activities?days={days}&activity_type={type}
```

参数：
- `days`（可选）：历史时间段，1-90天，默认为30天
- `activity_type`（可选）：按运动类型筛选（跑步、骑行、力量训练等）

返回内容：
- `activities`：包含各项运动记录的列表
- `total_count`：运动次数
- `total_duration_minutes`：总运动时间
- `total_distance_km`：总运动距离
- `total_calories`：总消耗的卡路里

每个运动包括：
- `activity_type`：运动类型（跑步、骑行等）
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
- `timezone`（可选）：IANA时区（例如：“America/New_York”），默认为UTC

返回内容：
- `effective_date`：查询日期的用户时区
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
- `dose_text`：如果适用，包含剂量信息

### 10. 获取90天健康计划

获取用户的90天健康计划及其优先事项。

```
GET /api/v1/mcp/tools/get_protocol
```

返回内容：
- `protocol_id`：健康计划的稳定ID
- `phase`：当前阶段（week1、month1、month3）
- `days_remaining`：计划剩余的天数
- `generated_at` / `last_updated_at`：时间戳
- `top_priorities`：前5个健康优先事项及其原因
- `key_recommendations`：饮食和生活方式建议
- `total_actions`：计划中的总行动数量

每个优先事项包括：
- `priority_id`：稳定的ID（与排名相同）
- `rank`：优先级（1 = 最高）
- `biomarker`：标准化的生物标志物名称
- `status`：当前状态（关键、关注中、次优、最佳）
- `target`：目标值及单位
- `current_value` / `unit`：当前测量值
- `measured_at`：上次测量该生物标志物的时间
- `why_prioritized`：优先考虑该指标的原因

**注意**：如果不存在健康计划，系统会返回提示信息，并建议用户在gevety.com/protocol生成计划。

### 11. 获取即将进行的检测

根据生物标志物历史数据和AI建议，获取即将进行的检测。

```
GET /api/v1/mcp/tools/get_upcoming_tests
```

返回内容：
- `tests`：按紧急程度排序的即将进行的检测列表
- `overdue_count`：逾期的检测数量
- `due_soon_count`：30天内到期的检测数量
- `recommended_count`：AI推荐的检测数量
- `total_count`：所有即将进行的检测总数

每个检测包括：
- `test_id`：用于深度链接的稳定ID（格式：`panel_{id}`或`recommended_{id}`）
- `name`：检测或检查的名称
- `test_type`：检测类型（面板、生物标志物、推荐检测）
- `urgency`：优先级（逾期、即将到期、推荐）
- `due_reason`：需要进行该检测的原因（例如：“2周前到期”）
- `last_tested_at`：上次检测的时间（如果适用）

### 12. 获取检测报告列表

获取上传的实验室报告列表，包括日期和生物标志物数量。

```
GET /api/v1/mcp/tools/list_test_results?limit={limit}&start_date={date}&end_date={date}
```

参数：
- `limit`（可选）：返回的最大报告数量，1-50份，默认为10份
- `start_date`（可选）：筛选日期（YYYY-MM-DD）
- `end_date`（可选）：筛选结束日期（YYYY-MM-DD）

返回内容：
- `reports`：实验室报告列表
- `total_reports`：报告总数

每个报告包括：
- `report_id`：报告的稳定ID
- `report_date`：实验室检测的日期
- `source`：报告的上传方式（PDF、电子邮件、手动上传）
- `lab_name`：实验室名称（如果有的话）
- `biomarker_count`：该报告中包含的生物标志物数量
- `filename`：原始报告文件名（如果以PDF格式上传）

### 13. 获取所有生物标志物信息

一次性获取所有跟踪的生物标志物信息，包括当前值、状态分类和趋势。

```
GET /api/v1/mcp/tools/list_all_biomarkers?category={category}&status={status}
```

参数：
- `category`（可选）：按类别筛选（例如：“代谢”、“心血管”）
- `status`（可选）：按状态筛选（最佳、次优、高、低、临界高、临界低）

返回内容：
- `biomarkers`：所有生物标志物的列表，包括最新值
- `total_count`：生物标志物的总数
- `counts_by_status`：按状态分类的统计（最佳、次优、高、低、临界高、临界低）

每个生物标志物包括：
- `name`：标准化的生物标志物名称
- `category`：健康类别（代谢、心血管等）
- `latest_value`：最新的检测值
- `unit`：测量单位
- `status`：状态分类（最佳、次优、高、低、临界高、临界低、未知）
- `last_test_date`：上次检测的时间
- `trend_direction`：自上次检测以来的变化趋势（增加、减少、稳定）

### 14. 获取个性化健康内容推荐

根据生物标志物信息获取个性化的健康内容推荐。

```
GET /api/v1/mcp/tools/get_content_recommendations?limit={limit}&category={category}
```

参数：
- `limit`（可选）：推荐的推荐数量，1-20条，默认为5条
- `category`（可选）：按内容类别筛选

返回内容：
- `recommendations`：推荐的文章列表
- `total_available`：可用的推荐文章总数

每个推荐包括：
- `content_id`：内容的稳定ID
- `title`：文章标题
- `summary`：简要摘要
- `category`：内容类别
- `relevance_reason`：推荐内容与用户的相关性原因
- `quality_score`：内容的质量评分（仅显示高质量内容）

## 解读评分

### 健康寿命评分（0-100）
| 范围 | 状态 | 含义 |
|-------|--------|---------|
| 80-100 | OPTIMAL | 健康状况极佳 |
| 65-79 | GOOD | 处于平均水平，有轻微改善空间 |
| 50-64 | SUBOPTIMAL | 需要改善 |
| <50 | NEEDS_ATTENTION | 多个方面需要关注 |

### 各健康维度的评分
每个健康维度都会单独评分：
- **代谢**：血糖、胰岛素、血脂
- **心血管**：心脏健康指标
- **炎症**：hs-CRP、同型半胱氨酸
- **激素**：甲状腺、睾酮、皮质醇
- **营养**：维生素、矿物质
- **肝脏/肾脏**：器官功能指标

**重要提示**：即使整体评分较高，某个维度的评分也可能较低（反之亦然）。`get_health_summary`中的`scoring_note`字段会解释这些情况。

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
3. 突出需要关注的重点和近期趋势
4. 如果有`scoring_note`，解释评分差异的原因

### “告诉我关于我的维生素D的情况”
1. 调用`query_biomarker?biomarker=vitamin d`
2. 展示历史数据、当前状态和趋势
3. 说明理想范围与当前值的情况

### “我的CRP是多少？” / “我的炎症情况如何？”
1. 调用`query_biomarker?biomarker=crp`（根据实验室报告返回“CRP”或“hs-CRP”）
2. 展示数值和趋势
3. 解释CRP的测量意义（作为炎症指标）

### “我的睡眠/心率变异性如何？”
1. 调用`get_wearable_stats?metric=sleep`或`?metric=hrv`
2. 显示近期趋势和平均值
3. 与健康基准进行比较

### “我应该关注什么？”
1. 调用`get_opportunities?limit=5`
2. 展示按健康影响排序的改善机会
3. 解释每个生物标志物的作用及其优化的意义

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
2. 总结运动情况（总时长、消耗的卡路里、总距离）
3. 列出最近的运动记录及关键指标

### “我今天应该做什么？”
1. 调用`get_today_actions?timezone=America/New_York`（使用用户的时区）
2. 按时间窗口（上午、下午、晚上）分组行动
3. 显示完成情况
4. 突出未完成的行动

### “我应该关注什么？” / “我的健康优先事项是什么？”
1. 调用`get_protocol`
2. 展示优先事项及其当前值和目标
3. 解释每个优先事项的原因
4. 列出关键建议
5. 说明协议的阶段和剩余天数

### “我接下来应该做什么检测？” / “我需要做哪些血液检测？”
1. 调用`get_upcoming_tests`
2. 突出逾期的检测（优先处理）
3. 列出30天内到期的检测
4. 提及AI推荐的检测
5. 说明每个检测涵盖的生物标志物

### “显示我的实验室报告” / “我上次做血液检测是什么时候？”
1. 调用`list_test_results?limit=10`
2. 显示报告列表，包括日期、实验室名称和生物标志物数量
3. 说明报告的上传方式（PDF、电子邮件、手动输入）

### “全面了解我的生物标志物情况”
1. 调用`list_all_biomarkers`
2. 按类别（代谢、心血管等）分组
3. 突出任何临界或高/低的值
4. 显示状态（例如：“12个最佳指标，3个次优指标，1个高指标”）
5. 显示趋势（增加/减少/稳定）

### “我应该阅读哪些健康文章？” / “有什么健康文章适合我？”
1. 调用`get_content_recommendations?limit=5`
2. 显示推荐的文章列表
3. 提供文章标题和推荐理由
4. 解释每篇文章与用户生物标志物的相关性

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

1. **切勿自行诊断** - 清晰地展示数据，但始终建议咨询医疗专业人员做出医疗决策
2. **趋势比单一数值更重要** - 随时间逐渐改善的轻微升高比持续下降的正常数值更值得关注
3. **注意数据时效性** - 实验室报告可能已有数周/数月之久；可穿戴设备的数据通常是每日更新的
4. **上下文很重要** - 询问可能影响数据趋势的补充剂、药物或生活方式变化
5. **隐私第一** - 健康数据敏感；请勿在对话之外分享或引用具体数值

## 错误处理

| 错误代码 | 含义 | 应对措施 |
|------------|---------|--------|
| 401 | 令牌无效或已过期 | 用户需要在gevety.com/settings重新生成令牌 |
| 404 + `did_you_mean` | 未找到生物标志物 | 建议从响应中选择其他选项 |
| 404 | 未找到数据 | 用户可能尚未上传实验室报告 |
| 429 | 请求次数限制 | 稍等片刻后重试 |

## 生成令牌

用户可以在以下链接生成API令牌：
**https://gevety.com/settings** → 开发者API → 生成令牌

令牌格式为`gvt_`后跟随机字符。

## 检查更新

首次使用每个会话时，可以选择性地检查是否有更新：

```
GET https://api.gevety.com/api/v1/mcp/tools/status
```

无需认证。如果请求失败或超时，跳过检查并正常继续。

成功响应时：
```json
{
  "clawdbot_skill": { "latest": "1.6.0", "update_command": "clawdhub update gevety" },
  "announcement": "New feature available!"
}
```

**如果`clawdbot_skill.latest` > 1.6.0**（此技能的版本），告知用户：
> “Gevety技能有更新。运行：`clawdhub update gevety`”

**如果`announcement`字段存在**，每个会话中提及一次。

**如果状态检查失败**，则忽略该提示，直接继续处理用户的请求。

**手动更新方法：**
```bash
clawdhub update gevety
```