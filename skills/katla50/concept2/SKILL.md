---
name: concept2
description: 通过 API 获取并分析 Concept2 训练日志数据，支持脉搏区域分析和趋势跟踪功能。适用于用户需要检索划船/滑雪/骑行等运动的数据、分析心率变化情况、跟踪训练趋势、获取包含性能洞察的训练总结或评估训练效果的场景。该功能包括脉搏区域分布（5 区模型）、每周趋势分析、配速稳定性评估、进步情况跟踪以及个性化训练建议等。使用前需具备 Concept2 API 访问令牌。
---
# Concept2 日志本 API 技能

从 Concept2 日志本中获取并分析锻炼数据，支持高级脉搏区间分析和趋势分析功能。

## 快速入门

使用提供的脚本来获取锻炼数据：

```bash
python3 scripts/fetch_workouts.py --token <API_TOKEN> --from-date 2026-03-01 --format table
```

## API 认证

需要 Concept2 API 访问令牌。请从以下链接获取令牌：
https://log.concept2.com/developers/keys

令牌必须通过 `Authorization: Bearer <token>` 头部字段传递。

## 主要端点

| 端点 | 描述 |
|----------|-------------|
| `GET /api/users/me` | 获取已认证用户信息 |
| `GET /api/users/me/results` | 获取锻炼数据（分页显示） |
| `GET /api/users/me/results/{id}` | 获取特定锻炼数据 |
| `GET /api/users/me/results/{id}/strokes` | 获取划船动作数据 |

## 结果查询参数

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| `from` | date | 开始日期（YYYY-MM-DD） |
| `to` | date | 结束日期（YYYY-MM-DD） |
| `type` | string | 锻炼类型：划船、滑雪、骑行等 |
| `per_page` | integer | 每页显示的结果数量（最多 250 条） |

## 锻炼类型

| 类型 | 描述 |
|------|-------------|
| JustRow | 自由划船 |
| FixedDistanceSplits | 固定距离分段训练 |
| FixedTimeSplits | 固定时间分段训练 |
| FixedCalorie | 固定卡路里目标 |
| FixedWattMinute | 固定瓦特-分钟目标 |
| FixedTimeInterval | 基于时间的训练区间 |
| FixedDistanceInterval | 基于距离的训练区间 |
| FixedCalorieInterval | 基于卡路里的训练区间 |
| FixedWattMinuteInterval | 基于瓦特-分钟的训练区间 |
| VariableInterval | 变化区间训练 |
| VariableIntervalUndefinedRest | 休息时间不固定的训练 |

## 设备类型

| 类型 | 描述 |
|------|-------------|
| rower | 划船机 |
| skierg | 滑雪机 |
| bike | 自行车训练器 |
| dynamic | 动态划船机 |
| slides | 带滑动装置的划船机 |
| paddle | 划桨训练器 |
| water | 水上划船机 |
| snow | 滑雪（北欧式滑雪） |
| rollerski | 滚雪机 |
| multierg | 多功能训练器 |

## 脚本使用方法

### 基本用法 - 包含脉搏区间分析
```bash
# Auto-detect max HR from birthdate in profile
python3 scripts/fetch_workouts.py --token <TOKEN> --from-date 2026-03-01

# Specify max HR manually
python3 scripts/fetch_workouts.py --token <TOKEN> --max-hr 165 --from-date 2026-02-01

# Estimate max HR from age
python3 scripts/fetch_workouts.py --token <TOKEN> --age 59 --from-date 2026-02-01
```

### 趋势分析（8 周）
```bash
python3 scripts/fetch_workouts.py --token <TOKEN> --trends 8 --from-date 2026-01-01
```

### 其他格式
```bash
# Simple table
python3 scripts/fetch_workouts.py --token <TOKEN> --format table

# JSON export
python3 scripts/fetch_workouts.py --token <TOKEN> --format json > workouts.json

# Filter by equipment type
python3 scripts/fetch_workouts.py --token <TOKEN> --type skierg
```

## 脉搏区间分析（5 区间模型）

区间划分基于最大心率的百分比：

| 区间 | 名称 | 范围 | 用途 |
|------|------|-------|---------|
| 🟢 1 | 恢复区 | 0-60% | 恢复、热身 |
| 🔵 2 | 有氧能力区 | 60-70% | 基础训练 |
| 🟡 3 | 有氧效果区 | 70-80% | 速度训练 |
| 🟠 4 | 无氧阈值区 | 80-90% | 阈值训练/间歇训练 |
| 🔴 5 | 最大能力区 | 90-100% | 最大摄氧量/冲刺 |

## 最大心率计算
- 手动输入：`--max-hr 165`
- 根据年龄计算：`--age 59`（使用 Tanaka 公式：208 - 0.7×年龄）
- 从用户资料中读取：从用户数据中获取出生日期

## 趋势分析

每周汇总以下数据：
- 总距离 |
- 总时间 |
- 锻炼次数 |
- 平均配速 |
- 进步率（配速变化百分比）

## 锻炼质量指标

### 配速稳定性
- 根据分段数据计算（如有）
- 标准差 / 平均配速 |
- 评分：🟢 良好 | 🟡 一般 | 🔴 不稳定

### 划船动作频率（SPM）评估
- 🟢 18-22：高效、有力的划船动作 |
- 🔵 <18：恢复阶段较快 |
- 🟡 24-28：正常速度 |
- 🟠 >30：频率过高，需检查技术

## 训练建议

脚本提供个性化建议：
- 训练频率评估 |
- 高强度训练平衡（第 4-5 区间建议占比 20%） |
- 长时间锻炼建议 |
- 间歇训练提醒

## 常用计算

### 计算配速
```python
pace_tenths = (time_tenths / distance_m) * 500
```

### 时间格式
```python
total_seconds = time_tenths / 10
minutes = int(total_seconds // 60)
seconds = total_seconds % 60
formatted = f"{minutes}:{seconds:04.1f}"
```

### 距离格式
- 距离以米为单位存储 |
- 5000 米 = 5 公里

### 划船动作数据
- 距离以分米为单位（递增记录） |
- 时间以十分之一秒为单位（递增记录） |
- 配速以每 500 米或 1000 米的十分之一秒为单位记录

## 错误代码

| 代码 | 含义 | 处理方式 |
|------|---------|------------|
| 200 | 成功 | 操作成功 |
| 400 | 请求错误 | 请检查请求格式 |
| 401 | 未授权 | 令牌无效或已过期 |
| 403 | 禁止访问 | 用户未授权使用该应用 |
| 404 | 未找到资源 | 资源不存在 |
| 409 | 数据重复 | 存在重复记录 |
| 422 | 数据无效 | 验证错误 |
| 500 | 服务器错误 | 请稍后再试 |
| 503 | 服务暂时不可用 | API 正在维护中 |

## 分页

分页响应包含 `metapagination` 对象：

```json
{
  "meta": {
    "pagination": {
      "total": 150,
      "count": 50,
      "per_page": 50,
      "current_page": 1,
      "total_pages": 3,
      "links": {
        "next": "https://log.concept2.com/api/users/me/results?page=2"
      }
    }
  }
}
```

默认每页显示 50 条记录，最多可显示 250 条记录。

## 参考资料

- 完整 API 文档：https://log.concept2.com/developers/documentation/
- API 令牌：https://log.concept2.com/developers/keys |
- 在线验证工具：https://log.concept2.com/developers/validator