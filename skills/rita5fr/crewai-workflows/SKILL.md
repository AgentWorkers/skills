---
name: crewai-workflows
description: 执行由人工智能驱动的工作流程，用于生成营销内容、处理客户支持、数据分析以及创建社交媒体日历。适用于以下任务：  
(1) 创建营销内容、标语或营销活动；  
(2) 处理客户支持查询或回复；  
(3) 分析业务数据以获取洞察；  
(4) 生成全面的社交媒体内容日历；  
(5) 任何可以从专门的人工智能工作流程中受益的内容生成或分析任务。  
这些工作流程由 DeepSeek、Perplexity 和 Gemini 模型提供支持。
---

# CrewAI 工作流技能

CrewAI 提供了多种专门的人工智能工作流，用于内容生成、分析和支持任务。所有工作流都在配备有生产级大型语言模型（LLMs）的专用服务器上运行。

## 先决条件

建议将 API 密钥设置为环境变量：

```bash
export CREWAI_API_KEY="5aZyTFQJAAT03VPIII5zsIPcL8KTtdST"
```

或者在调用辅助脚本时直接传递 API 密钥。

## 可用的工作流

### 1. 营销工作流 📢

生成营销内容、标语和活动文案。

**适用场景：**
- 产品/服务标语
- 广告或着陆页的营销文案
- 活动信息
- 价值主张

**输入参数：**
- `topic`（必填）：需要生成营销内容的主题
- `target_audience`（可选）：目标受众

**使用的 LLM：** DeepSeek  
**响应时间：** 3-10 秒

**示例：**
```bash
scripts/call_crew.sh marketing \
  '{"topic": "hypnotherapy for better sleep", "target_audience": "working professionals with insomnia"}'
```

---

### 2. 支持工作流 🎧

利用人工智能生成回复来处理客户咨询。

**适用场景：**
- 回答客户问题
- 起草支持邮件
- 处理常见咨询
- 提供问题升级指导

**输入参数：**
- `issue`（必填）：客户的问题或疑问

**使用的 LLM：** DeepSeek  
**响应时间：** 3-10 秒

**示例：**
```bash
scripts/call_crew.sh support \
  '{"issue": "Client wants to reschedule their hypnotherapy session"}'
```

---

### 3. 分析工作流 📊

分析业务数据并提供可操作的洞察。

**适用场景：**
- 数据解读
- 趋势分析
- 绩效指标评估
- 商业智能分析

**输入参数：**
- `data_description`（必填）：需要分析的数据描述

**使用的 LLM：** DeepSeek  
**响应时间：** 3-10 秒

**示例：**
```bash
scripts/call_crew.sh analysis \
  '{"data_description": "Monthly client retention rates for Q4 2025"}'
```

---

### 4. 社交媒体工作流 ⭐ 📱

生成包含每日帖子、标题和标签的 30 天社交媒体内容日程表。

**适用场景：**
- 社交媒体规划
- 内容日程表制作
- 多平台内容策略
- 月度内容发布计划

**输入参数：**
- `industry`（必填）：业务行业/领域
- `company_name`（必填）：企业或个人品牌名称

**使用的 LLM：** Perplexity（数据分析） + Gemini（内容生成）  
**响应时间：** 3-5 分钟 ⏳

**注意：** 由于需要综合研究和内容生成，此工作流的响应时间较长。

---

## 使用方法

### 方法 1：使用辅助脚本（推荐）

```bash
cd crewai-workflows
scripts/call_crew.sh <crew_name> '<json_input>' [api_key]
```

**示例：**
```bash
# Marketing crew
scripts/call_crew.sh marketing '{"topic": "sleep therapy for entrepreneurs", "target_audience": "startup founders"}'

# Support crew
scripts/call_crew.sh support '{"issue": "Client asking about session pricing"}'

# Analysis crew
scripts/call_crew.sh analysis '{"data_description": "Weekly session booking trends"}'

# Social media crew (takes 3-5 minutes)
scripts/call_crew.sh social_media '{"industry": "wellness coaching", "company_name": "Calm Mind Studio"}'

# With explicit API key
scripts/call_crew.sh marketing '{"topic": "mindfulness apps"}' "YOUR_API_KEY"
```

### 方法 2：直接使用 cURL

```bash
curl -X POST "https://crew.iclautomation.me/crews/<crew_name>/run" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CREWAI_API_KEY" \
  -d '{"input": {...}}'
```

---

## 响应格式

所有工作流都会返回结构化的 JSON 数据：

```json
{
  "ok": true,
  "crew": "marketing",
  "trace_id": "abc123-def456",
  "result": {
    "workflow": "marketing",
    "output": "... the generated content ...",
    "input_summary": {...}
  },
  "error": null
}
```

**输出内容说明：** 实际生成的内容存储在 `result.output` 中。

---

## 最佳实践

1. **设置合适的超时时间：**
   - 营销/支持/分析：30-60 秒
   - 社交媒体：5-10 分钟

2. **检查 API 密钥：** 确保 `CREWAI_API_KEY` 环境变量已设置或明确传递

3. **处理错误：** 检查响应中的 `error` 字段

4. **社交媒体工作流：** 预计响应时间为 3-5 分钟，切勿中断请求

5. **批量请求：** 对于多个相似的任务，建议依次执行

---

## 健康检查

验证 CrewAI 服务器是否正在运行：

```bash
curl https://crew.iclautomation.me/health
# Expected: {"ok": true}
```

---

## 未来扩展

当服务器新增工作流时：
1. 更新 “可用工作流” 部分
2. 在辅助脚本中添加使用示例
3. 记录输入参数和响应时间

---

**服务器地址：** https://crew.iclautomation.me  
**认证方式：** 通过 `X-API-Key` 头部字段传递 API 密钥  
**最后更新时间：** 2026-01-17