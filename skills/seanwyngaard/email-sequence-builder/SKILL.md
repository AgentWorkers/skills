---
name: email-sequence-builder
description: 构建完整的电子邮件营销序列（包括欢迎邮件、培育客户关系邮件、销售邮件以及重新参与活动邮件），其中包含邮件主题行、正文内容以及适用于各种邮件平台的发送格式。这些模板可用于创建电子邮件活动、持续发送的邮件序列（drip sequences）或自动化邮件流程，以满足客户的需求。
argument-hint: "[sequence-type] [business-description]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# 电子邮件序列生成器

该工具可为任何类型的业务生成完整的、可直接部署的电子邮件序列。输出内容包括邮件正文、主题行、预览文本、呼叫行动（CTA）以及发送时间。

## 使用方法

```
/email-sequence-builder welcome "Online fitness coaching platform, $49/mo subscription"
/email-sequence-builder sales "B2B SaaS analytics tool, $99/mo, targeting marketing managers"
/email-sequence-builder nurture "Real estate agent targeting first-time home buyers"
/email-sequence-builder re-engagement "E-commerce clothing store, customers inactive 60+ days"
```

- `$ARGUMENTS[0]`：序列类型：`welcome`（欢迎）、`sales`（销售）、`nurture`（培养）、`re-engagement`（重新参与）、`onboarding`（入职引导）、`launch`（产品发布）、`webinar`（网络研讨会）、`abandoned-cart`（购物车放弃）
- `$ARGUMENTS[1]`：业务描述，包括目标受众和定价信息

## 序列类型

### 欢迎序列（5封邮件，发送周期为14天）
**目标**：将新订阅者转化为活跃用户

| 邮件 | 发送时间 | 目的 |
|-------|--------|---------|
| 1 | 立即 | 欢迎订阅者 + 提供吸引人的内容 + 设定期望 |
| 2 | 第2天 | 介绍公司的背景及业务理念 |
| 3 | 第4天 | 发送最优质的内容或快速展示产品价值 |
| 4 | 第7天 | 展示成功案例或用户反馈 |
| 5 | 第10天 | 解答常见疑问 + 提出首次购买建议 |
| 6 | 第12天 | 提供更多价值 + 强化购买建议 |
| 7 | 第14天 | 直接提供产品或服务 + 明确的购买提示 |

### 销售序列（5封邮件，发送周期为7-10天）
**目标**：将潜在客户转化为实际买家

| 邮件 | 发送时间 | 目的 |
|-------|--------|---------|
| 1 | 第0天 | 介绍产品及最大优势 |
| 2 | 第2天 | 展示成功案例或用户转型故事 |
| 3 | 第4天 | 解答价格相关疑问 |
| 5 | 第5天 | 解答“这产品适合我吗？”等疑问 |
| 7 | 第7天 | 提供常见问题解答及用户反馈 |
| 8 | 第8天 | 强调紧迫性（优惠活动即将结束） |
| 10 | 第10天 | 最后一次提醒 + 最后购买机会 |

### 培养序列（5封邮件，发送周期为30天）
**目标**：与尚未准备购买的潜在客户建立信任

| 邮件 | 发送时间 | 目的 |
|-------|--------|---------|
| 1 | 第1周 | 提供有价值的教育性内容 |
| 2 | 第2周 | 行业洞察或趋势分析 |
| 3 | 第3周 | 指出常见错误及避免方法 |
| 4 | 第4周 | 展示实际应用效果 |
| 5 | 第5周 | 提供后续服务建议 |

### 重新参与序列（3封邮件，发送周期为10天）
**目标**：让不活跃的订阅者或客户重新回归

| 邮件 | 发送时间 | 目的 |
|-------|--------|---------|
| 1 | 第0天 | 表示想念 + 介绍最新动态 |
| 2 | 第3天 | 提供独家优惠 |
| 7 | 第7天 | 最后一次提醒 + 调查问卷（询问离开原因） |
| 10 | 第10天 | 最后一封邮件：决定继续订阅或取消订阅 |

### 购物车放弃序列（3封邮件，发送周期为3天）
| 邮件 | 发送时间 | 目的 |
|-------|--------|---------|
| 1 | 发送后1小时 | 提醒用户未完成购买 |
| 2 | 发送后24小时 | 展示其他用户的购买案例或处理用户疑虑 |
| 3 | 发送后72小时 | 强调紧迫性并提供折扣（最后机会，享受9折优惠）

## 邮件结构模板

对于序列中的每封邮件，系统会生成以下内容：

```yaml
email_number: 1
send_timing: "Immediately after signup"
subject_line_a: "Your first subject line variant"
subject_line_b: "A/B test variant"
preview_text: "First 40-90 chars shown in inbox preview"

body: |
  Hi {{first_name}},

  [Opening hook — 1-2 sentences, personal, relevant]

  [Body — 3-5 short paragraphs]
  - Use bullet points for scanability
  - Bold key phrases
  - Keep paragraphs to 2-3 sentences max

  [CTA — clear, single action]

  [Sign-off]
  {{sender_name}}

  P.S. [Reinforce CTA or add bonus — P.S. lines get read more than body text]

cta_text: "Start Your Free Trial"
cta_url: "{{cta_link}}"
```

## 内容编写规则

1. **主题行**：4-7个单词，激发读者的好奇心或明确产品优势。避免使用全部大写字母或过多的标点符号。每封邮件都应进行A/B测试。
2. **预览文本**：与主题行内容互补，长度为40-90个字符。
3. **开头语**：不要以“希望您一切安好”开头，可以使用问题句、强调句或与读者相关的内容。
4. **正文**：
   - 语言应简单易懂（适合6-8年级学生阅读）
   - 使用“您”这个词的频率是“我们”或“我”的3倍
   - 每封邮件只讨论一个主题
   - 句子简短，段落简洁，适当使用空格
5. **呼叫行动（CTA）**：每封邮件中包含一个主要的购买建议，按钮文字应具有行动导向性（例如“获取我的免费指南”）
6. **附言**：在销售和欢迎序列中包含购买提示，或再次强调购买建议。
7. **个性化**：在主题行和开头语中使用`{{first_name}}`（用户名）；在B2B场景中使用`{{company_name}}`（公司名称）。

## 平台输出格式

系统会生成可导入的电子邮件序列文件：

### 通用格式（Markdown）
每封邮件保存为单独的文件：

```
output/email-sequence/
  sequence-config.md     # Overview, timing, goals
  email-01-welcome.md
  email-02-story.md
  ...
```

### Mailchimp格式
生成包含以下列的CSV文件：`subject`（主题行）、`preview_text`（预览文本）、`html_body`（邮件正文）、`send_delay_days`（发送延迟天数）

### ConvertKit/Kit格式
生成包含合并标签的纯文本文件：`{{subscriber.first_name}}`

### ActiveCampaign格式
使用合并标签生成邮件：`%FIRSTNAME%`

在`sequence-config.md`文件中需包含以下信息：
- 序列名称和目标
- 触发事件（什么会启动该序列）
- 邮件发送间隔
- 退出条件（用户购买、取消订阅、点击特定链接）
- 推荐的受众群体
- 需要跟踪的KPI（打开率、点击率、转化率）
- 各行业的预期指标

## 质量检查标准

- 每封邮件都有两种不同的主题行以进行A/B测试
- 预览文本针对每封邮件单独编写，不从邮件正文中自动生成
- 每封邮件中都包含明确的购买建议
- 邮件长度不超过300字（200字为最佳）
- 序列内容具有清晰的情感逻辑（从提供价值到建立信任，再到提出购买请求）
- 个性化内容使用正确
- 序列配置中包含取消订阅的提醒
- 发送时间考虑周末因素（避免在周日发送销售邮件）