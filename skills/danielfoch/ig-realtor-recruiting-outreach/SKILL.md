---
name: ig-realtor-recruiting-outreach
description: 构建符合Instagram私信（DM）规范的推广活动，以招募房地产经纪人加入经纪公司的销售团队（例如：eXp Realty、Real Broker）。当用户需要获取潜在客户信息、个性化的首次联系私信以及基于Instagram用户资料的数据进行后续跟进时，可以使用该功能；最后可以导出准备发送的推广文件。
---
# IG 房地产经纪人招聘推广

利用此技能将 Instagram 的潜在客户列表转化为有效的招聘推广活动，避免使用大量垃圾信息或骚扰性语言。

## 工作流程

### 1. 收集潜在客户信息

使用最佳的数据来源：

- ClawHub/Instagram 数据抓取工具的输出（如可用则优先选择）
- 通过手动筛选从 Instagram 收集的 CSV 文件

CSV 文件至少应包含以下字段：

- `instagram_handle`（Instagram 账号）
- `first_name`（或 `name`）
- `city`（可选）
- `brokerage`（经纪公司）
- `target_brokerage`（目标经纪公司；如未指定，则使用 CLI 的默认值）

建议添加的字段：

- `followers`（关注者数量）
- `last_post_theme`（最近发布的帖子主题）
- `pain_point`（潜在客户的需求或痛点）
- `production_tier`（工作层级：`new`、`building`、`team_lead`、`top_producer`）
- `notes`（备注）

### 2. 生成推广方案

运行以下脚本：

```bash
python3 scripts/build_ig_recruiting_outreach.py \
  --input /path/to/realtor_leads.csv \
  --campaign-name "exp-phoenix-week1" \
  --default-target-brokerage "eXp Realty" \
  --output-dir output/ig-recruiting
```

该脚本会生成以下文件：

- `messages_<campaign>.csv`：包含分阶段的私信发送序列
- `audit_<campaign>.json`：包含每个潜在客户的评估信息及质量备注
- `playbook_<campaign>.md`：包含发送计划和沟通要点

### 3. 发送前的质量检查

检查每条私信的内容，确保：

- 名称/账号和经纪公司信息准确无误
- 个性化内容具体且真实
- 不包含任何关于收入保证的承诺
- 不使用操纵性的语言或虚假的稀缺性表述

### 4. 发送并跟踪

通过 Instagram 手动发送私信。使用 CRM 标签来标记发送阶段：

- `ig_sent_d1`
- `ig_sent_f1`
- `ig_sent_f2`
- `ig_sent_breakup`

## 输入数据结构

脚本支持以下字段（不区分大小写）：

- `instagram_handle`（必填）
- `first_name`
- `name`
- `brokerage`
- `target_brokerage`
- `city`
- `followers`
- `last_post_theme`
- `pain_point`
- `production_tier`
- `notes`

## 安全规则

- 不得承诺任何形式的收入保证或分成
- 不得冒充现有员工或伪造社交证明
- 保持沟通语气为咨询性，并在每条私信中明确传达一个明确的行动号召（CTA）
- 遵守平台规则和当地的营销法规

## 参考资料

- `references/message-framework.md`
- `references/compliance-guardrails.md`