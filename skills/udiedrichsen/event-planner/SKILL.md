---
name: event-planner
description: 通过使用 Google Places API 搜索场所来规划活动（如夜间外出、周末活动、约会之夜、团队出游、用餐、旅行等）。系统会根据地点、预算、参与人数和偏好自动选择最佳的餐厅、酒吧和活动。生成的行程计划会包含详细的时间安排以及 Google 地图链接。适用于需要规划出游活动、创建行程安排、寻找活动场所或组织各类活动的场景。
homepage: https://github.com/clawdbot/clawdbot
metadata: {"clawdbot":{"emoji":"🎉","requires":{"bins":["uv"],"env":["GOOGLE_PLACES_API_KEY"]},"primaryEnv":"GOOGLE_PLACES_API_KEY","install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# 活动策划器

通过搜索场地并生成带有 Google 地图链接的行程来规划活动。

## 快速入门

**规划晚间活动：**

```bash
uv run {baseDir}/scripts/plan_event.py "night out" \
  --location "Times Square, NYC" \
  --party-size 4 \
  --budget medium \
  --duration 4h
```

**规划周末活动：**

```bash
uv run {baseDir}/scripts/plan_event.py "weekend day" \
  --location "Central Park, NYC" \
  --party-size 2 \
  --budget "$100 per person" \
  --preferences "outdoors, casual dining"
```

**规划约会之夜：**

```bash
uv run {baseDir}/scripts/plan_event.py "date night" \
  --location "SoHo, NYC" \
  --budget high \
  --duration 3h
```

## 活动类型

- **晚间活动**：晚餐 + 1-2 家酒吧/休闲场所（3-4 小时）
- **周末活动**：早午餐/午餐 + 活动 + 晚餐（6-8 小时）
- **约会之夜**：浪漫餐厅 + 甜点/饮品场所（2-3 小时）
- **团队活动**：团体活动 + 晚餐场所（3-5 小时）
- **午餐**：单家餐厅推荐
- **晚餐**：单家餐厅推荐
- **旅行**：多日行程及每日计划

## 参数

- `--location`：城市、地址或地标（必填）
- `--party-size`：人数（默认：2 人）
- `--budget`：“低/中/高”或“每人 $X”（默认：中等）
- `--duration`：可用时间（例如：“3小时”、“全天”）
- `--preferences`：用逗号分隔的偏好（例如：“素食、户外座位、现场音乐”）
- `--start-time`：开始时间（默认：根据活动类型推断）
- `--output`：文本 | JSON（默认：文本）
- `--date`：特定日期（格式为 YYYY-MM-DD，用于当天查询，默认：今天）

## 输出格式

**默认（文本）**：包含时间线、场地详情、旅行信息及 Google 地图链接的 Markdown 行程

**JSON**：包含所有场地详情、坐标和解析后的元数据的结构化数据

## 限制

- **API 限制**：Google Places API 有使用配额（请查看您的账单）
- **实时数据**：场地的营业时间可能会变化，请在前往前确认
- **预算估算**：基于 Google 的价格等级（0-4），非实际费用
- **旅行时间**：优先使用 Google Directions API；如无法使用，则根据距离估算并加入 30% 的缓冲时间
- **营业时间**：未验证营业时间的场所会显示警告，请勿假设其可用性
- **活动场所**：文化中心、剧院和活动场所的营业时间可能因预定活动而变化

## API 要求

活动策划器使用以下 API：
- **Google Places API（新）**：用于场地搜索
- **Google Directions API**：可选但推荐，用于获取准确的旅行时间

如果在 Google Cloud Console 中启用了 `GOOGLE_PLACES_API_KEY`，则两个 API 都可以使用相同的密钥。

## 错误处理

- 无效的位置 → 返回错误并提供建议
- 未找到场地 → 放宽筛选条件并重试
- API 故障 → 采用指数级退避策略（尝试 3 次）