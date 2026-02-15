---
name: Invoice Generator
description: 使用 Markdown 和 HTML 格式生成专业的发票。
---

# 发票生成器

您可以生成专业的发票，格式清晰、易于发送。

## 需要提供的信息

1. **您的企业信息：** 公司名称、地址、电子邮件地址、电话号码（以便后续使用）
2. **客户信息：** 客户公司名称、联系人姓名、地址
3. **发票编号：** 可以自动生成（格式为 INV-YYYY-NNN）
4. **商品明细：** 产品描述、数量、单价
5. **付款条款：** 现款结算（30天内支付）、货到付款等
6. **付款方式：** 银行转账、PayPal、Stripe 等
7. **货币：** 默认为美元（USD）
8. **税率：** 如适用（以百分比表示）
9. **备注：** 任何特殊条款或逾期付款费用等

## 发票模板

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    INVOICE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FROM:                          INVOICE #: [INV-2024-001]
[Your Business Name]           DATE: [2024-01-15]
[Address]                      DUE DATE: [2024-02-14]
[Email] | [Phone]

TO:
[Client Company]
[Contact Name]
[Address]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DESCRIPTION              QTY    RATE      AMOUNT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Service/Product]        [1]    [$X]      [$X]
[Service/Product]        [2]    [$Y]      [$2Y]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                          SUBTOTAL:    $[X]
                          TAX ([X]%):  $[X]
                          ━━━━━━━━━━━━━━━━
                          TOTAL:       $[X]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PAYMENT TERMS: [Net 30]

PAYMENT METHODS:
• Bank Transfer: [Details]
• PayPal: [email]
• [Other]

NOTES:
[Late payment fee: 1.5% per month on overdue balances]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Thank you for your business.
```

## 输出格式

### Markdown（默认格式）
生成简洁的 Markdown 表格格式，方便直接粘贴到电子邮件或文档中。

### HTML
生成格式美观的 HTML 文件，用户可以在浏览器中打开并打印或保存为 PDF：
- 格式专业、美观
- 适合打印（无多余的背景颜色，节省墨水）
- 保存文件名为 `invoice-[编号].html`

## 规则

- 必须正确计算总金额，并仔细核对计算结果。
- 发票编号应连续编号；如可能，请检查是否已有相同编号的发票。
- 到期日期 = 发票日期 + 付款期限（例如：现款结算为 30 天后）
- 必须包含所有法律要求的必要信息（具体要求因地区而异，如有疑问请咨询）
- 将生成的发票保存到 `invoices/` 目录中以备记录
- 如果用户之前已经生成过发票，可重复使用其企业信息
- 货币格式应使用正确的符号和小数位（例如：$1,234.56）

## 定期发票

如果需要定期向同一客户开具发票：
- “为 [客户] 生成本月的发票” → 复制之前的发票，更新日期、编号和周期
- 记录每个客户的发票历史记录

## 快速命令

- “为 [客户] 开具金额为 [金额]、商品描述为 [描述] 的发票” → 使用默认设置生成发票
- “查看我的发票” → 列出 `invoices/` 目录中的所有发票
- “未支付的发票有哪些？” → 显示所有逾期未付的发票

---

## 🔗 更多 AfrexAI 功能（在 ClawHub 上免费使用）

| 功能 | 安装方式 |
|-------|---------|
| AI 人性化生成器 | `clawhub install afrexai-humanizer` |
| SEO 写作工具 | `clawhub install afrexai-seo-writer` |
| 电子邮件生成工具 | `clawhub install afrexai-email-crafter` |
| 提案生成工具 | `clawhub install afrexai-proposal-gen` |
| 发票生成工具 | `clawhub install afrexai-invoice-gen` |
| 客户开发工具 | `clawhub install afrexai-onboarding` |
| 会议准备工具 | `clawhub install afrexai-meeting-prep` |
| 社交媒体内容优化工具 | `clawhub install afrexai-social-repurposer` |
| 常见问题解答生成工具 | `clawhub install afrexai-faq-builder` |
| 评论回复工具 | `clawhub install afrexai-review-responder` |
| 报告生成工具 | `clawhub install afrexai-report-builder` |
| 客户关系管理（CRM）更新工具 | `clawhub install afrexai-crm-updater` |
| 演示文稿审核工具 | `clawhub install afrexai-pitch-deck-reviewer` |
| 合同分析工具 | `clawhub install afrexai-contract-analyzer` |
| 价格优化工具 | `clawhub install afrexai-pricing-optimizer` |
| 客户评价收集工具 | `clawhub install afrexai-testimonial-collector` |
| 竞争对手监控工具 | `clawhub install afrexai-competitor-monitor` |

## 🚀 升级至专业版：行业特定功能包（每包 47 美元）

通过行业特定功能包，让您的 AI 助手具备深入的行业专业知识。

→ **[查看所有功能包](https://afrexai-cto.github.io/context-packs/)**

**免费工具：** [AI 收入计算器](https://afrexai-cto.github.io/ai-revenue-calculator/) | [代理设置向导](https://afrexai-cto.github.io/agent-setup/)

*由 [AfrexAI](https://afrexai-cto.github.io/context-packs/) 开发 🖤💛*