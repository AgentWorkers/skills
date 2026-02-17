---
name: zodiac-horoscope
description: >
  从 zodiac-today.com 的 API 中获取基于个人出生星盘计算的个性化每日运势预测。该功能适用于以下场景：  
  1. 用户需要每日建议，了解应从事或避免的活动；  
  2. 用户希望获得生活规划方面的帮助（如面试、旅行、恋爱或重要决策的最佳时机）；  
  3. 用户希望了解自己的精力状况、专注力、运势及爱情运势，以便更好地安排日程；  
  4. 用户需要知道当天的幸运颜色和数字；  
  5. 用户希望分析未来日期，以便规划活动、旅行或重要事件（此功能需付费）。  
  所需环境变量：  
  - `ZODIAC_API_KEY`（hsk_API 密钥）  
  - `ZODIAC_PROFILE_ID`（出生星盘的个人资料 ID）  
  该功能会收集用户的敏感个人信息（如电子邮件、出生日期和出生城市），因此需要用户的明确同意。
---
# 星座运势

根据用户的出生星盘和行星运行轨迹，提供个性化的、可操作的每日运势建议。

## 所需的环境变量

| 变量 | 描述 |
|----------|-------------|
| `ZODIAC_API_KEY` | 来自 zodiac-today.com 的 API 密钥（以 `hsk_` 开头） |
| `ZODIAC_PROFILE_ID` | 用户出生星盘的配置文件 ID |

## 隐私声明

本功能会收集 **敏感的个人信息**（电子邮件、出生日期、出生城市），这些信息用于生成出生星盘。请注意以下事项：
- 在收集出生信息之前，必须获得用户的明确同意。
- 绝不要在公共渠道或共享环境中记录或泄露这些个人信息。
- 将 API 密钥和配置文件 ID 存储在环境变量中，而不是纯文本文件中。
- 注册完成后，请删除 `cookies.txt` 文件。

## 该功能如何帮助用户

- **日常决策**： “今天是否适合进行重要的对话？” → 通过运势判断对话的时机是否合适。
- **日程安排优化**： 将精力充沛的日子安排在高能量的任务上，而在精力较低的日子里休息。
- **生活事件规划**： 为求职面试、初次约会、旅行或大额购物等事件选择最佳时机（高级会员可查看更详细的日期建议）。
- **关系洞察**： 星座运势指标可帮助用户挑选理想的约会日期。
- **激励与自我提升**： 每日的运势总结有助于用户进行自我反思和更有目的地生活。

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

将 `hsk_` 密钥保存为环境变量 `ZODIAC_API_KEY`。完成此步骤后，请删除 `cookies.txt` 文件。

### 2. 创建个人资料

```bash
curl -s -X POST https://zodiac-today.com/api/profiles \
  -H "Authorization: Bearer hsk_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"name":"John","birthDate":"1990-05-15","birthCity":"London, UK"}'
```

将返回的 `id` 保存为环境变量 `ZODIAC_PROFILE_ID`。

## 工作流程

### 新用户的初次设置
1. 询问用户的电子邮件、出生日期和出生城市（需获得用户的明确同意，因为这些属于敏感个人信息）。
2. 向用户的电子邮件发送验证码：发送 `POST /api/auth/send-code` 请求。
3. **人工审核**： 要求用户检查电子邮件并输入 6 位验证码。如果管理员具有电子邮件访问权限（例如通过 IMAP），可以从 `noreply@zodiac-today.com` 自动获取验证码。
4. 验证验证码：发送 `POST /api/auth/verify` 请求，并将会话 cookie 保存到临时文件 `cookies.txt` 中。
5. 生成 API 密钥：使用会话 cookie 发送 `POST /api/keys` 请求，并保存返回的 `hsk_` 密钥。
6. **清理**： 立即删除 `cookies.txt` 文件，因为它不再需要。
7. 创建个人资料：使用 API 密钥发送 `POST /api/profiles` 请求，并保存返回的配置文件 `id`。
8. 将 `ZODIAC_API_KEY` 和 `ZODIAC_PROFILE_ID` 保存为环境变量。

### 每日运势查询
1. 使用 `Authorization: Bearer $ZODIAC_API_KEY` 发送 `GET /api/horoscope/daily?profileId=$ZODIAC_PROFILE_ID&startDate=YYYY-MM-DD&endDate=YYYY-MM-DD` 请求。
2. 解析响应内容，并提供可操作的运势建议。

### 向用户展示结果

将原始数据转化为 **实用的建议**：
- **整体运势评分**（1-10 分）：用 “今天很棒！”（8 分以上）、“表现不错”（6-8 分）、“需放松”（6 分以下）来表达。
- **有利/不利事项**：以 “适合……” 和 “最好避免……” 的形式列出。
- **重点指标**：突出显示当天用户的能量状态，例如 “今天你的精力非常充沛，非常适合处理那个项目”。
- **幸运颜色**：提供穿搭或装饰的建议。
- **幸运数字**：轻松提及，增加一些趣味性。
- **运势总结**：结合星座运势的描述，让建议更加生动且实用。

### 长期规划（高级会员）

对于高级会员，可以查询特定日期范围内的运势建议：
- “这个月哪一天最适合我参加求职面试？”
- “我应该什么时候安排我们的周年纪念晚餐？”
- 比较不同日期的总体运势评分，并推荐评分最高的日期。

## API 详细信息

请参阅 [references/api.md](references/api.md)，以获取完整的端点文档、参数、会员等级和响应格式信息。

## 示例 curl 请求

```bash
curl "https://zodiac-today.com/api/horoscope/daily?profileId=PROFILE_ID&startDate=2026-02-15&endDate=2026-02-15" \
  -H "Authorization: Bearer hsk_your_api_key"
```