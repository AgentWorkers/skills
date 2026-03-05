---
name: lead-gen-pipeline
description: Automated lead generation pipeline with AI-powered lead scoring and personalized follow-up generation. Score leads 0-100 with reasoning, generate context-aware follow-ups in multiple tones. Integrates with any CRM. Use for sales automation, cold outreach, and pipeline management.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, OpenRouter API key
metadata: {"openclaw": {"emoji": "\ud83c\udfa3", "requires": {"env": ["OPENROUTER_API_KEY"]}, "primaryEnv": "OPENROUTER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 销售线索生成流程

这是一个基于人工智能的销售线索生成系统，能够智能地评估线索的质量，生成个性化的跟进信息，并帮助您管理销售流程。

## 快速入门

```bash
export OPENROUTER_API_KEY="your-key"

# Score a lead
python3 {baseDir}/scripts/lead_scorer.py '{"name":"Jane Smith","company":"Acme Corp","title":"VP Marketing","source":"webinar","actions":["downloaded whitepaper","visited pricing page 3x","opened 5 emails"]}'

# Generate follow-up
python3 {baseDir}/scripts/followup_generator.py '{"name":"Jane Smith","company":"Acme Corp","context":"Attended our AI webinar, downloaded whitepaper","stage":"warm","tone":"professional"}'
```

## 线索评分

人工智能评分系统从多个维度对线索进行评估：

| 评分因素 | 权重 | 说明 |
|--------|--------|-------------|
| **匹配度** | 30% | 该线索是否符合您的目标客户群体（行业、公司规模、职位等）？ |
| **购买意向** | 30% | 消费者的行为信号（页面浏览量、文件下载量、电子邮件互动情况） |
| **互动程度** | 20% | 消费者的互动积极性（最近一次互动的时间、频率） |
| **信息来源质量** | 20% | 线索的来源（推荐、网络研讨会还是主动搜索） |

### 评分等级
- **80-100:** 🔥 高热度线索 — 立即联系，购买意向强烈 |
- **60-79:** 🟡 温和线索 — 通过针对性内容进行培养，安排电话沟通 |
- **40-59:** 🟠 中等热度线索 — 添加到持续跟进序列中，监控互动情况 |
- **0-39:** 🔵 低热度线索 — 优先级较低，需要长期培养 |

```bash
# Score with custom ICP
python3 {baseDir}/scripts/lead_scorer.py '{"name":"...","company":"...","icp":{"industries":["SaaS","fintech"],"minEmployees":50,"titles":["VP","Director","C-suite"]}}'
```

## 个性化跟进信息生成

系统可以为销售流程的各个阶段生成个性化的跟进信息：

```bash
# Professional follow-up after demo
python3 {baseDir}/scripts/followup_generator.py '{
  "name": "Jane Smith",
  "company": "Acme Corp",
  "context": "Had a 30-min demo, interested in enterprise plan, concerned about onboarding time",
  "stage": "post-demo",
  "tone": "professional",
  "channel": "email"
}'

# Casual SMS check-in
python3 {baseDir}/scripts/followup_generator.py '{
  "name": "Mike",
  "context": "Met at conference, exchanged cards, talked about AI automation",
  "stage": "initial",
  "tone": "casual",
  "channel": "sms"
}'

# Urgent closing message
python3 {baseDir}/scripts/followup_generator.py '{
  "name": "Sarah Johnson",
  "company": "TechFlow",
  "context": "Proposal sent 5 days ago, no response, deal worth $25k, quarter ending",
  "stage": "closing",
  "tone": "urgent",
  "channel": "email"
}'
```

### 支持的语气风格
- **专业** — 正式的商务沟通风格 |
- **随意** — 友善、对话式的沟通方式 |
- **紧急** — 强调时间紧迫性，需要立即采取行动 |
- **友好** — 以建立良好关系为目标 |
- **咨询式** — 以专家建议的形式提供指导 |

### 支持的沟通渠道
- **电子邮件** — 包含主题行的完整邮件 |
- **短信** — 简短精炼（少于160个字符） |
- **WhatsApp** — 适合对话式交流，支持表情符号 |
- **LinkedIn** — 适合专业社交场景的沟通方式 |

### 销售流程阶段
- **初始阶段** — 第一次联系/主动发起沟通 |
- **温和阶段** — 消费者表现出兴趣但尚未安排会议 |
- **预约会议阶段** — 预约了会议或演示 |
- **演示后阶段** — 演示结束后 |
- **提案阶段** — 发送提案 |
- **成交阶段** — 谈判/最终决策 |
- **重新激活阶段** — 重新联系冷落或失去联系的潜在客户 |

## 冷落线索的跟进模板

### AIDA框架
1. **吸引注意** — 用客户关心的问题引起他们的兴趣 |
2. **激发兴趣** — 表明您了解他们的需求 |
3. **创造需求** — 描述解决方案 |
4. **引导行动** — 提供清晰、易于操作的购买提示 |

### 进阶沟通策略
- **第1天**：发送初次沟通邮件，强调产品价值 |
- **第3天**：通过案例研究或第三方推荐来增强信任 |
- **第7天**：尝试不同的沟通方式（视频、语音留言、表情包） |
- **第14天**：发送总结邮件，询问是否可以继续跟进 |

您可以根据需要生成上述任何一种跟进模板：

```bash
python3 {baseDir}/scripts/followup_generator.py '{"name":"...","stage":"initial","sequence_step":1}'
python3 {baseDir}/scripts/followup_generator.py '{"name":"...","stage":"initial","sequence_step":4}'
```

## 客户关系管理（CRM）集成

### 与GHL（GoHighLevel）集成

```bash
# 1. Score incoming lead
SCORE=$(python3 {baseDir}/scripts/lead_scorer.py '{"name":"...","source":"facebook_ad"}')

# 2. Create contact in GHL with score tag
python3 ../ghl-crm/{baseDir}/scripts/ghl_api.py contacts create '{"firstName":"...","tags":["score-85","hot-lead"]}'

# 3. Add to appropriate pipeline stage
python3 ../ghl-crm/{baseDir}/scripts/ghl_api.py opportunities create '{"pipelineId":"...","stageId":"hot-stage-id","contactId":"..."}'

# 4. Generate and send follow-up
MSG=$(python3 {baseDir}/scripts/followup_generator.py '{"name":"...","stage":"warm","channel":"sms"}')
python3 ../ghl-crm/{baseDir}/scripts/ghl_api.py conversations send-sms <contactId> "$MSG"
```

### 与任何CRM系统集成

系统生成的脚本会以JSON格式输出，可以直接导入任何CRM系统的API接口。线索评分结果及评估理由也可作为CRM备注保存。

## 回复处理

当潜在客户回复时，系统会根据新的信息重新评估线索的评分，并生成相应的回复内容：

```bash
python3 {baseDir}/scripts/lead_scorer.py '{"name":"Jane","company":"Acme","actions":["replied to email","asked about pricing","requested demo"]}'
```

## 开发者信息

本系统由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi)和[agxntsix.ai](https://www.agxntsix.ai)共同开发。
更多相关信息请访问[YouTube](https://youtube.com/@aiwithabidi)和[GitHub](https://github.com/aiwithabidi)。
该系统是**AgxntSix Skill Suite**的一部分，专为OpenClaw代理设计。

📅 **需要帮助为您的业务设置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)