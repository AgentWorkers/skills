---
name: seo-prospector
description: 这是一个自动化SEO潜在客户研究与拓展工具，专为网页设计师、营销机构和自由职业者设计。该工具可用于研究本地商业机会、执行定期的潜在客户开发计划、创建营销资料包、生成每日总结报告以及管理潜在客户信息。触发事件包括：“research prospect”（研究潜在客户）、“find leads”（寻找潜在客户）、“prospect report”（生成潜在客户报告）、“outreach for [business]”（针对特定业务进行营销推广）、“run today’s clusters”（执行当天的潜在客户开发计划）、“daily prospect summary”（生成每日潜在客户总结）、“batch research”（批量研究潜在客户）、“generate outreach”（生成营销材料）、“SEO audit prospect”（进行SEO审计）、“local business leads”（本地商业潜在客户）、“cold outreach”（主动联系冷门潜在客户）以及“lead pipeline”（管理潜在客户流程）。
  Automated SEO prospect research and outreach for web designers, agencies, and freelancers.
  Use when researching local business prospects, running scheduled prospect clusters,
  creating outreach packages, generating daily summaries, or managing a lead pipeline.
  Triggers on "research prospect", "find leads", "prospect report", "outreach for [business]",
  "run today's clusters", "daily prospect summary", "batch research", "generate outreach",
  "SEO audit prospect", "local business leads", "cold outreach", "lead pipeline".
license: Proprietary. See LICENSE.txt for complete terms.
---
# SEO Prospector

这是一个专为网页设计师和营销机构设计的自动化本地业务线索生成工具。

工作流程：发现 → 研究 → 审计 → 报告 → 外展 → 跟踪。

## 工作原理

这个工具能帮助你高效地寻找潜在客户。只需指定目标城市或行业，它就能：

1. 通过SEO审计和网络调研，找出网站存在问题的企业；
2. 生成包含具体问题的详细潜在客户报告；
3. 自动创建个性化的联系信息（包括HTML邮件、LinkedIn消息或私信）；
4. 将所有信息记录在数据库中，并实现去重和集群轮换机制；
5. 每天提供工作流程的汇总报告。

## 设置（首次使用）

使用前，请先配置你的机构信息：

```bash
# Copy and edit the config file
cp references/config-template.json ~/.openclaw/workspace/leads/data/seo-prospector-config.json
```

使用以下代码块更新配置文件：
```json
{
  "agency": {
    "name": "Your Agency Name",
    "owner": "Your Name",
    "phone": "(555) 123-4567",
    "email": "you@agency.com",
    "website": "youragency.com",
    "city": "Your City",
    "tagline": "Your one-liner value prop"
  },
  "outreach": {
    "default_tone": "casual",
    "signature_style": "friendly"
  }
}
```

## 快速参考

### 单个潜在客户的研究
```bash
python3 scripts/research_prospect.py \
  --business "Business Name" --domain "example.com" --industry "Restaurant" \
  --priority HIGH --cluster "Restaurants"
```

### 批量研究（当前轮次）
```bash
python3 scripts/batch_research.py --run morning    # Today's run_1 cluster
python3 scripts/batch_research.py --run afternoon   # Today's run_2 cluster
python3 scripts/batch_research.py --cluster "Restaurants" --limit 5
```

### 生成联系信息
```bash
python3 scripts/create_outreach.py --report path/to/report.md --template casual
python3 scripts/create_outreach.py --business "Name" --template professional --format html
```

### 每日总结
```bash
python3 scripts/daily_summary.py                     # Today, Discord format
python3 scripts/daily_summary.py --date 2026-02-09 --format markdown
```

### 工作流程管理
```bash
python3 scripts/prospect_tracker.py today-clusters
python3 scripts/prospect_tracker.py check --business "Name"
python3 scripts/prospect_tracker.py stats
python3 scripts/prospect_tracker.py outreach-ready
```

## 工作流程

### 1. 检查日程安排和去重
- 运行 `prospect_tracker.py today-clusters` 以查看已安排的集群；
- 在进行研究之前，运行 `prospect_tracker.py check --business "名称"`（确保14天内没有重复记录）。

### 2. 研究阶段
数据来源按优先级排序：
1. **SEO快速审计** (`seo_quick_audit.py`) — 网站页面的技术分析；
2. **Perplexity Search** (`perplexity_search.py`) — 企业信息、评价和声誉调查；
3. **浏览器验证**（可选） — 对高优先级潜在客户进行视觉检查。

### 3. 报告生成
报告遵循 `references/research-template.md` 的格式。主要内容包括：
- 执行摘要（具体问题，而非泛泛而谈）；
- 企业概况（业务内容、成立时间、评价）；
- 在线存在情况分析（SEO审计结果，分为通过/未通过）；
- 为什么选择[你的机构]（根据企业需求定制推销语）；
- 联系方式及下一步行动建议。

输出文件路径：`~/.openclaw/workspace/leads/prospects/YYYY-MM-DD-{cluster}/{business}.md`

### 4. 生成联系信息
`scripts/create_outreach.py` 支持以下格式：
- **HTML邮件**（专业风格，响应式设计）；
- **纯文本邮件**（简洁明了）；
- **LinkedIn消息**（参考 `references/outreach-templates.md`）；
- **私信**（Instagram、Facebook、SMS，参考 `assets/templates/dm-outreach.md`）。

每个联系信息包包含：
- 邮件草稿（HTML或纯文本）；
- 手动质量检查的清单；
- 用于跟踪工作流程状态的JSON数据。

### 5. 工作流程跟踪
每个潜在客户都会通过 `prospect_tracker.py add` 被记录在数据库中。数据库支持去重、覆盖范围统计、集群管理和联系状态跟踪。

工作流程状态：`draft_ready → pending_review → approved → sent → followed_up → responded → closed`

## 优先级评分（严格标准）

目标分配如下：
- **高优先级**：无网站或网站严重损坏，且企业确认仍在运营；
- **中等优先级**：有网站但存在重大SEO问题（如缺少H1标签、元数据、schema信息不完整、移动设备适配不良），且企业确认仍在运营；
- **低优先级**：网站状况尚可但存在小问题，或企业活动未得到确认。

如果不确定，默认归类为中等优先级。

## 验证（必选）

在记录任何潜在客户之前，请进行以下验证：
```bash
python3 scripts/verify_prospect.py <report_path>
```
排除以下情况：无效URL、停放的域名、已暂停服务的网站或已永久关闭的企业。

## 脚本

| 脚本 | 用途 |
|--------|---------|
| `scripts/research_prospect.py` | 单个潜在客户的完整信息收集 |
| `scripts/batch_research.py` | 从指定集群或输入列表中批量收集潜在客户信息 |
| `scripts/create_outreach.py` | 生成个性化的联系信息 |
| `scripts/generate_outreach_batch.py` | 为指定日期的所有潜在客户批量生成联系信息 |
| `scripts/daily_summary.py` | 每日工作流程总结（通过Discord或Markdown发送） |
| `scripts/prospect_tracker.py` | 数据库管理、去重、集群轮换和统计分析 |
| `scripts/verify_prospect.py` | 验证URL、域名和电话号码的真实性 |
| `scripts/seo_quick_audit.py` | 网站页面的SEO技术审计 |

## 参考资料

| 文件 | 使用场景 |
|------|----------|
| `references/research-template.md` | 编写或审阅潜在客户报告时使用 |
| `references/outreach-templates.md` | 制作邮件/LinkedIn/私信内容时使用 |
| `references/industry-insights.md` | 行业特定的交流要点 |
| `references/objection-handling.md` | 处理客户反馈（如“我们已经有网站”等） |
| `references/config-template.json` | 首次配置机构信息时使用 |
| `references/cluster-template.json` | 设置行业集群轮换规则 |

## 资源文件

- `assets/templates/email-html.html` — 专业的HTML邮件模板，支持数据合并 |
- `assets/templates/email-plain.txt` — 纯文本邮件模板 |
- `assets/templates/linkedin-message.md` — LinkedIn联系信息模板 |
- `assets/templates/dm-outreach.md` | 私信模板（用于Instagram、Facebook、SMS） |
- `assets/examples/example-report.md` | 完成的潜在客户报告示例 |
- `assets/examples/example-outreach.md` | 完成的联系信息包示例 |

## Cron任务集成

该工具支持自动化每日潜在客户挖掘任务：
```
8:30 AM  — SERP Gap Scanner (identify opportunities for 5 industries)
10:00 AM — batch_research.py --run morning (Tier A/B cluster)
11:30 AM — batch_research.py --run afternoon (Tier B/C cluster)
5:00 PM  — daily_summary.py (pipeline summary)
```

## 质量标准

1. 首先检查是否存在重复记录（14天窗口内）；
2. 每个潜在客户至少使用两个数据来源（SEO审计和网络调研）；
3. 仅记录具体问题（如“缺少H1标签”，而非笼统的SEO问题）；
4. 如实评价企业的网站质量（如果网站良好，应给予正面评价）；
5. 每个集群最多生成5个潜在客户记录（注重深度而非数量）；
6. 根据行业特点调整联系信息的语气（餐厅行业使用轻松风格，律师事务所使用专业风格）；
7. 在记录前务必验证每个潜在客户的真实性（排除无效URL和停放的域名）；
8. 严禁夸大问题，仅记录审计结果。

## 错误处理

- **网站无法访问**：仅通过网络搜索进行调查；
- **检测到重复记录**：跳过该潜在客户，避免浪费API调用；
- **搜索超时**：继续处理其他潜在客户，并标记为低优先级；
- **集群为空**：记录日志并继续下一轮；
- **数据不足**：至少需要企业名称和域名或行业信息。