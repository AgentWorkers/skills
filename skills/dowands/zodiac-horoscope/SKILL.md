---
name: zodiac-horoscope
description: >
  根据用户的出生星盘计算结果，从 zodiac-today.com API 获取个性化的每日星座运势预测。该功能适用于以下场景：  
  (1) 用户需要了解当天应从事或避免的活动建议；  
  (2) 用户希望获得生活规划方面的帮助，例如面试、旅行、恋爱或重要决策的最佳时机；  
  (3) 用户希望根据运势预测来优化自己的日程安排（包括精力、专注度、运气及恋爱运势）；  
  (4) 用户想了解当天的幸运颜色和数字；  
  (5) 用户需要为未来事件（如活动、旅行或重要里程碑）进行日期分析（此功能需付费）。  
  触发关键词：  
  horoscope（星座运势）、zodiac（黄道十二宫）、star sign forecast（星座运势）、daily guidance（每日建议）、lucky day（幸运日）、best day to（最佳时机）、astrology advice（占星建议）、what should I do today（我今天该做什么）、is today a good day for（今天是适合……的日子吗？）、plan my week astrology（规划我的一周运势）。
env:
  ZODIAC_API_KEY:
    description: "API key from zodiac-today.com (starts with hsk_)"
    required: true
  ZODIAC_PROFILE_ID:
    description: "Profile ID for the user's birth chart"
    required: true
---
# 星座运势

根据用户的出生星盘和行星运行轨迹，提供个性化的、可操作的每日运势建议。

## 隐私声明

本功能会收集用于生成出生星盘的 **敏感个人信息**（电子邮件、出生日期、出生城市）。请注意保护这些数据：
- 绝不要在公共渠道中记录或泄露这些信息
- 将 API 密钥和用户 ID 存储在环境变量中，而非明文文件中
- 在收集出生信息之前，必须获得用户的明确同意

## 该功能如何帮助用户

- **日常决策**：例如“今天是否适合进行重要的对话？”——可以判断冲突是否有利
- **时间安排优化**：将高能量任务安排在精力充沛的日子里，休息则选择低能量的日子
- **生活事件规划**：为求职面试、初次约会、旅行或大额消费选择最佳时机（高级会员可查看更详细的日期建议）
- **人际关系分析**：通过星座指标帮助用户挑选理想的约会日期
- **激励与自我反思**：每日运势总结可促使用户进行自我反思并更有目的地生活

## 设置流程

所有操作均通过 API 完成，无需使用浏览器。

### 1. 注册并获取 API 密钥

```bash
# Send verification code (creates account if new)
curl -s -X POST https://zodiac-today.com/api/auth/send-code \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'

# Verify code (check email inbox for 6-digit code)
curl -s -X POST https://zodiac-today.com/api/auth/verify \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"user@example.com","code":"123456"}'

# Create API key (use session cookie from verify step)
curl -s -X POST https://zodiac-today.com/api/keys \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"name":"My Agent"}'
# Response: {"id":"...","key":"hsk_...","name":"My Agent"}
```

将 `hsk_` 密钥保存为环境变量 `ZODIAC_API_KEY`。

### 2. 创建个人资料

```bash
curl -s -X POST https://zodiac-today.com/api/profiles \
  -H "Authorization: Bearer hsk_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"name":"John","birthDate":"1990-05-15","birthCity":"London, UK"}'
```

将返回的 `id` 保存为环境变量 `ZODIAC_PROFILE_ID`。

## 工作流程

### 新用户的首次设置
1. 获取用户的电子邮件、出生日期和出生城市
2. 通过 `/api/auth/send-code` 注册 → 从邮件中获取验证码 → 通过 `/api/auth/verify` 验证
3. 使用会话 cookie 通过 `POST /api/keys` 创建 API 密钥
4. 使用 API 密钥通过 `POST /api/profiles` 创建个人资料
5. 将 `ZODIAC_API_KEY` 和 `ZODIAC_PROFILE_ID` 保存为环境变量

### 每日运势查询
1. 使用 `Authorization: Bearer $ZODIAC_API_KEY` 调用 `GET /api/horoscope/daily?profileId=$ZODIAC_PROFILE_ID&startDate=YYYY-MM-DD&endDate=YYYY-MM-DD`
2. 解析响应并呈现可操作的运势建议

### 向用户展示结果

将原始数据转化为 **实用的建议**：
- **整体运势评分**（1-10 分）：例如“今天非常棒！”（8 分以上）、“今天表现不错”（6-8 分）、“今天需要放松”（6 分以下）
- **有利/不利事项**：以“适合……”和“最好避免……”的形式列出
- **重点指标**：突出显示当日的高能量状态，例如“今天你的精力非常充沛，非常适合处理那个项目”
- **幸运颜色**：提供穿搭或装饰建议
- **幸运数字**：轻松提及，增添趣味性
- **运势总结**：结合星座运势的描述，使建议更具吸引力和实用性

### 长期规划（高级会员）

对于使用高级会员功能的用户，可以查询特定日期范围内的运势建议：
- “这个月哪一天最适合我参加求职面试？”
- “我应该什么时候安排我们的周年纪念晚餐？”
- 比较不同日期的整体运势评分，推荐最佳日期

## API 详细信息

请参阅 [references/api.md](references/api.md)，以获取完整的端点文档、参数、会员等级和响应格式信息。

## 示例 curl 命令

```bash
curl "https://zodiac-today.com/api/horoscope/daily?profileId=PROFILE_ID&startDate=2026-02-15&endDate=2026-02-15" \
  -H "Authorization: Bearer hsk_your_api_key"
```