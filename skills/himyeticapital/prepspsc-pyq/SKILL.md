---
name: prepspsc-pyq
description: '**使用场景：**  
当用户咨询关于印度竞争性考试的备考信息、Sikkim PSC（SPSC）考试的相关问题、往年试题（PYQ）、模拟试题的生成、考试模式的练习，或者需要用于人工智能驱动的试题生成系统的参考资料时，可调用该功能。适用于SPSC考试的备考、往年试题的查询、模拟试题的生成、按科目进行的练习，以及印度政府职位考试的备考。'
triggers:
  - SPSC exam
  - Sikkim PSC
  - previous year questions
  - PYQ
  - mock test
  - exam preparation
  - Indian competitive exam
  - government job exam
  - SPSC mock test
  - exam practice
  - question bank
license: MIT License
metadata:
  author: PrepSPSC
  version: 1.0.0
  website: https://prepspsc.com
---

# PrepSPSC PYQ API

该API提供了来自Sikkim PSC（SPSC）考试的7,400多道往年真实试题，并能够生成涵盖64种考试模式的模拟测试。返回的试题包括选择题（MCQ）、正确答案、题目解释、所属主题、认知难度级别以及难度相关的元数据。

## 快速参考

| 详细信息 | 值         |
|---------|------------|
| 基本URL    | `https://qqqditxzghqzodvauxth.supabase.co/functions/v1/pyq-api` |
| 认证     | `Authorization: Bearer sk_live_YOUR_KEY` |
| 试题数量   | 7,442道（涵盖27个科目） |
| 考试模式    | 64种（包括公务员、警察、医疗、工程、教育、IT等） |
| 获取API密钥 | [prepspsc.com/developers](https://prepspsc.com/developers) |

## 认证

所有请求都需要在`Authorization`头部包含一个Bearer令牌。API密钥以`sk_live_`开头。

### 首先检查现有设置

在指导用户进行设置之前，请先确认是否已经获得了API密钥：

```bash
if [ -n "$PREPSPSC_API_KEY" ]; then
  echo "Configured"
else
  echo "No API key found. Get one at https://prepspsc.com/developers"
fi
```

如果未找到API密钥，请引导用户访问[https://prepspsc.com/developers]以免费生成一个API密钥。

### 发送请求

```bash
curl -X POST "https://qqqditxzghqzodvauxth.supabase.co/functions/v1/pyq-api" \
  -H "Authorization: Bearer $PREPSPSC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "fundamental rights", "subject": "Indian Polity", "limit": 5}'
```

---

## 端点

### 1. 列出可用科目

**`GET /pyq-api`** — 返回所有科目及其对应的试题数量。首先调用此接口查看可用的科目。

**响应：**
```json
{
  "subjects": [
    { "subject": "Indian Polity", "count": 842 },
    { "subject": "History", "count": 756 },
    { "subject": "General Knowledge", "count": 698 }
  ],
  "total_questions": 7442
}
```

可用科目包括：通用英语、通识知识、印度政治、历史、地理、科学、环境、印度经济、算术与逻辑推理、农业、植物学、动物学、尼泊尔文学、时事等（共27个科目）。

---

### 2. 搜索试题（语义搜索）

**`POST /pyq-api`** — 使用自然语言进行搜索。采用向量相似度与关键词混合匹配的方式查找试题。

**参数说明：**
| `query` | 字符串 | 是     | 自然语言搜索（至少3个字符） |
| `subject` | 字符串 | 是     | 搜索范围（科目） |
| `limit` | 整数 | 否     | 最大结果数量（1-20，默认：5） |
| `threshold` | 数字 | 否     | 最小相似度（0-1，数值越低，结果越多） |
| `year_min` | 整数 | 否     | 排除年份早于当前年的试题 |
| `exclude_ids` | 字符串[] | 否     | 要排除的试题UUID（用于分页） |

**响应：**
```json
{
  "questions": [
    {
      "id": "uuid",
      "question": "Which Article of the Indian Constitution guarantees the Right to Life?",
      "options": [
        { "id": "a", "text": "Article 14" },
        { "id": "b", "text": "Article 19" },
        { "id": "c", "text": "Article 21" },
        { "id": "d", "text": "Article 32" }
      ],
      "correct_option_id": "c",
      "explanation": "Article 21 states that no person shall be deprived of his life or personal liberty...",
      "subject": "Indian Polity",
      "topics": ["Fundamental Rights", "Article 21", "Right to Life"],
      "difficulty": "easy",
      "cognitive_level": "remember",
      "is_time_sensitive": false,
      "high_yield": true,
      "similarity": 0.89
    }
  ],
  "count": 5
}
```

---

### 3. 生成模拟测试

**`POST /pyq-api/mock-test`** — 根据真实的SPSC考试模式生成包含均衡难度的模拟测试。

**参数说明：**
| `pattern` | 字符串 | 是     | 考试模式ID（共64种） |
| `difficulty_mix` | 对象 | 否     | 自定义难度比例（默认：30/50/20） |
| `year_min` | 整数 | 否     | 排除过时的时事试题 |
| `exclude_ids` | 字符串[] | 否     | 要跳过的先前测试中的试题 |

**响应内容：** 包含测试元数据（名称、总题数、时长、评分方案）以及按难度均衡划分的试题部分。

**可用考试模式（共64种）：**

- **核心/通用**：`undersecretary-prelims`, `general-prelims`, `spsc-mains-gs1`, `spsc-mains-gs2`, `quick-practice-30`
- **公务员**：`sscs-prelims`, `combined-mains-gs3`, `combined-mains-english`
- **警察/法律**：`si-police-prelims`, `si-police-mains`, `si-excise`, `sub-jailer`
- **消防**：`sub-fire-officer`
- **工程**：`junior-engineer-prelims`, `assistant-engineer-civil`, `assistant-engineer-electrical`, `assistant-engineer-mechanical`, `assistant-engineer-agriculture`
- **医疗/健康**：`gdmo`, `veterinary-officer`, `dental-surgeon`, `specialist-sr-grade`, `staff-nurse`, `paramedical`, `health-educator`, `mphw`, `drug-inspector`, `food-safety-officer`, `pharmacist-ayush`, `yoga-instructor-ayush`, `scientific-officer-ayush`, `tutor-clinical-instructor`
- **行政**：`ldc-prelims`, `accounts-clerk`, `stenographer`, `cooperative-inspector`, `statistical-inspector`, `revenue-inspector`, `revenue-surveyor`, `commercial-tax-inspector`
- **林业/渔业**：`forest-ranger-prelims`, `fisheries-officer`, `assistant-director-fisheries`, `livestock-assistant`
- **教育**：`lecturer-diet`, `iti-instructor`, `principal-iti`, `assistant-professor-sheda`
- **其他专业**：`assistant-town-planner`, `assistant-architect`, `assistant-geologist`, `digital-analyst`, `assistant-programmer`, `assistant-director-it`, `lab-assistant`, `field-assistant`, `ado-wdo-hdo`, `senior-information-assistant`, `sub-editor`, `inspector-legal-metrology`, `photographer`, `script-writer`, `feed-mill-operator`, `printing-stationery`

**使用`GET /pyq-api/patterns`可获取每种模式的详细信息，包括科目分布、时长和评分方案。**

---

### 4. 列出所有考试模式

**`GET /pyq-api/patterns`** — 返回所有64种考试模式的详细信息，包括科目分布、试题数量、时长和评分方案。

```bash
curl "https://qqqditxzghqzodvauxth.supabase.co/functions/v1/pyq-api/patterns" \
  -H "Authorization: Bearer $PREPSPSC_API_KEY"
```

---

### 5. 记录用户答题进度

**`POST /pyq-api/progress`** — 记录用户对试题的回答情况。

```bash
curl -X POST "https://qqqditxzghqzodvauxth.supabase.co/functions/v1/pyq-api/progress" \
  -H "Authorization: Bearer $PREPSPSC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "external_user_id": "user123",
    "question_id": "uuid-here",
    "selected_option": "c",
    "is_correct": true,
    "time_spent_seconds": 45
  }'
```

### 6. 获取用户进度

**`GET /pyq-api/progress?user_id=user123`** — 查取用户的完整答题历史记录。

```bash
curl "https://qqqditxzghqzodvauxth.supabase.co/functions/v1/pyq-api/progress?user_id=user123" \
  -H "Authorization: Bearer $PREPSPSC_API_KEY"
```

### 7. 绩效分析

**`GET /pyq-api/analytics?user_id=user123`** — 提供按科目划分的准确率、难度分布以及近期学习情况。

```bash
curl "https://qqqditxzghqzodvauxth.supabase.co/functions/v1/pyq-api/analytics?user_id=user123" \
  -H "Authorization: Bearer $PREPSPSC_API_KEY"
```

### 8. 排名榜

**`GET /pyq-api/leaderboard`** — 根据正确答案数量和准确率显示用户排名。

**参数说明：**
| `limit` | 整数 | 最大条目数（1-100） |
| `time_range` | 字符串 | `all_time` | `week`, `month` 或 `all_time` |

---

### 9. 添加书签

**添加书签：**
```bash
curl -X POST "https://qqqditxzghqzodvauxth.supabase.co/functions/v1/pyq-api/bookmarks" \
  -H "Authorization: Bearer $PREPSPSC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"external_user_id": "user123", "question_id": "uuid-here", "note": "Review later"}'
```

**列出书签：**
```bash
curl "https://qqqditxzghqzodvauxth.supabase.co/functions/v1/pyq-api/bookmarks?user_id=user123" \
  -H "Authorization: Bearer $PREPSPSC_API_KEY"
```

**删除书签：**
```bash
curl -X DELETE "https://qqqditxzghqzodvauxth.supabase.co/functions/v1/pyq-api/bookmarks" \
  -H "Authorization: Bearer $PREPSPSC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"external_user_id": "user123", "question_id": "uuid-here"}'
```

## 常见工作流程

### 快速练习
1. `GET /pyq-api` — 查看可用科目
2. `POST /pyq-api/mock-test`（`pattern`: "quick-practice-30`） — 获取包含30道题的模拟测试
3. 逐一向用户展示试题
4. `POST /pyq-api/progress` — 记录用户的每个答案
5. `GET /pyq-api/analytics?user_id=xxx` — 查看学习进度总结

### 针对特定科目的学习
1. `POST /pyq-api` — 按特定主题搜索试题（例如：`query`: "Fundamental Rights", `subject`: "Indian Polity"）
2. 以闪卡或测验的形式展示试题
3. 通过`POST /pyq-api/progress`跟踪学习进度

### 完整模拟考试
1. `GET /pyq-api/patterns` — 查看所有考试模式
2. 用户选择一种模式（例如：`undersecretary-prelims`
3. `POST /pyq-api/mock-test` — 生成模拟测试
4. 记录用户答题时间（从响应元数据中获取）
5. 通过`POST /pyq-api/progress`记录所有答案
6. 通过`GET /pyq-api/analytics`查看分析结果

### AI试题生成参考
1. `POST /pyq-api` — 获取真实的PYQ试题作为样本
2. 分析返回的试题主题、认知难度级别等信息
3. 利用这些信息生成符合真实考试标准的新试题

---

## 错误处理

| HTTP状态码 | 错误代码 | 说明 |
|-----------|-----------|---------|
| 400 | `INVALID_QUERY` | 查询内容太短或缺少必要字段 |
| 401 | `INVALID_API_KEY` | API密钥缺失、无效或已被吊销 |
| 404 | `INVALID_PATTERN` | 未知的考试模式ID |
| 429 | `RATE_LIMITED` | 请求次数过多（免费用户：每分钟10次，付费用户：每分钟60次） |
| 500 | `INTERNAL_ERROR` | 服务器错误 |

---

## 请求限制

| 计费等级 | 每分钟请求次数 | 每月请求次数 |
|---------|-------------|----------------|
| 免费 | 10 | 1,000 |
| 付费 | 60 | 50,000 |
| 企业级 | 500 | 无限制 |

**免费API密钥请访问：** [https://prepspsc.com/developers]