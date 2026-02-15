---
name: invoice-chaser
description: 自动化发票催收流程：从友好提醒逐步升级为强硬措施。系统会跟踪未支付的发票，定期发送带有 escalating tone（语气逐渐强硬）的提醒邮件，记录付款相关的所有交互信息，并生成应收账款 aging reports（逾期报告）。这些工作由专业代理负责处理，让您无需亲自处理那些棘手的沟通，从而确保现金流的稳定以及与客户关系的维护，让您能够专注于核心业务。您可以配置发票跟踪功能、根据不同催收阶段定制邮件模板（友好提醒 → 强硬要求 → 最终通知），设定邮件发送的时间规则，并让代理全天候跟进付款事宜。该功能适用于添加新发票、发起付款催收、检查付款状态或生成应收账款报告等场景。
metadata:
  clawdbot:
    emoji: "💸"
    requires:
      skills:
        - gog
      env:
        - GOG_DEFAULT_ACCOUNT
---

# Invoice Chaser — 别再费心追款了，让这个工具来帮你吧！

**你完成了工作，你的代理会帮你收款。**

每个自由职业者、顾问和小型企业主都经历过这种困扰：你完成了工作，发出了发票，但接下来却没有任何回应。跟进付款过程既尴尬又浪费时间。而追讨欠款更是浪费了本可以用来处理新工作的项目时间。

Invoice Chaser 能自动完成整个追款流程。它会按照预定时间发送提醒邮件，逐步提升沟通的语气，跟踪付款进度，并在需要人工干预时及时通知你。你可以把它想象成一个高效、专业的收款助手，永远不会忘记任何细节，也不会让你感到尴尬。

**它的独特之处在于：** 这不仅仅是一个“7天后发送提醒”的简单工具。Invoice Chaser 拥有完整的收款管理流程，包括状态管理、自动升级机制和逐步升级的沟通策略。它知道何时该保持友好态度（“只是提醒一下”），何时该强硬一些（“付款已经逾期30天了”），以及何时需要你介入处理。这种多阶段的处理方式能够更好地应对现实世界中的复杂付款情况。

## 设置

1. 运行 `scripts/setup.sh` 命令来初始化配置文件和数据目录。
2. 修改 `~/.config/invoice-chaser/config.json` 文件，设置邮件模板、发送时间以及升级规则。
3. 确保已经安装了 `gog` 插件（用于发送 Gmail 邮件）。
4. 在 `~/.clawdbot/secrets.env` 文件中设置 `GOG_DEFAULT_ACCOUNT`（例如：`your-email@gmail.com`）。
5. 通过 `scripts/add-invoice.sh --test` 命令进行测试。

## 配置

配置文件位于 `~/.config/invoice-chaser/config.json`。详细结构请参考 `config.example.json`。

**关键配置项：**
- **business**：你的公司名称、联系方式和付款条款。
- **stages**：每个升级阶段的邮件模板（提醒、逾期、强硬、最终通知）。
- **timing**：每个阶段发送邮件的时间（从发票日期算起的天数）。
- **escalation**：自动升级规则和人工干预的触发条件。
- **payment_methods**：在提醒邮件中包含付款链接或说明。
- **reporting**：邮件发送的渠道、频率以及收款信息的分类方式。

邮件模板支持以下变量：`{client_name}`、`{invoice_number}`、`{amount}`、`{due_date}`、`{days_overdue}`、`{payment_link}`。

## 脚本

| 脚本 | 功能 |
|--------|---------|
| `scripts/setup.sh` | 初始化配置文件和数据目录。 |
| `scripts/add-invoice.sh` | 将新发票添加到跟踪系统中。 |
| `scripts/chase.sh` | 运行追款流程（检查状态、发送提醒、升级处理）。 |
| `scripts/status.sh` | 显示发票状态和收款进度报告。 |
| `scripts/report.sh` | 生成详细的收款 aging 报告。 |

所有脚本都支持 `--dry-run` 参数，用于在不发送邮件的情况下进行测试。

## 添加发票

```bash
# Add invoice manually
scripts/add-invoice.sh \
  --number "INV-2025-042" \
  --client "Acme Corp" \
  --email "billing@acme.com" \
  --amount 2500.00 \
  --date "2025-01-15" \
  --due "2025-02-14" \
  --net 30

# Quick add (assumes net-30 terms)
scripts/add-invoice.sh --number "INV-042" --client "Acme Corp" --email "billing@acme.com" --amount 2500

# Mark as paid
scripts/status.sh INV-042 --paid --date "2025-02-10"
```

## 追款流程

建议每天通过 cron 任务运行 `scripts/chase.sh`。追款流程包括：
1. 从跟踪数据库中加载所有未支付的发票。
2. 计算发票日期至今的天数以及逾期天数。
3. 根据配置规则确定每张发票的当前处理阶段。
4. 发送相应的提醒邮件（使用不同阶段的模板，并逐步提升语气）。
5. 记录所有发送的邮件和流程进展。
6. 当达到预设条件（例如逾期60天）时，触发人工干预。
7. 生成状态报告。

## 升级流程

```
SENT → REMINDER (friendly) → OVERDUE (professional) → FIRM (insistent) → FINAL (urgent) → ESCALATED
  ↓         ↓ day 3              ↓ day 7+             ↓ day 30         ↓ day 45        ↓ day 60
PAID (any time) ✅
```

**默认时间线：**
- **第3天**：友好提醒（“您的发票即将到期...”）
- **第7天及以上**：到期日提醒（“付款截止日期为 [date]...”）
- **第30天**：首次逾期通知（“您的账户已逾期30天...”）
- **第45天**：强硬通知（“我们必须立即收到付款...”）
- **第60天**：最终通知（“若7天内未付款，我们将启动追讨流程...”）
- **第75天及以上**：触发人工干预。

所有时间设置都可以在 `config.json` 中进行修改。

## 邮件语气逐步升级

**第1阶段 — 友好提醒（第3天）：**
> 亲爱的 [客户]，
>
> 只是想提醒您，编号为 [number] 的发票（金额为 [amount]）的付款截止日期为 [due_date]。如果有任何问题，请随时告知！

**第2阶段 — 专业逾期通知（第14天）：**
> 亲爱的 [客户]，
>
> 我想跟进一下编号为 [number] 的发票（金额为 [amount]），付款截止日期为 [due_date]。如果您已经付款，请忽略此邮件。如果有任何付款问题，请告知我们。

**第3阶段 — 强硬通知（第30天）：**
> 亲爱的 [客户]，
>
> 您的账户已经逾期30天。编号为 [number] 的发票（金额为 [amount]）的付款截止日期为 [due_date]。请立即付款，以避免服务中断和滞纳金。

**第4阶段 — 最终通知（第45天）：**
> 亲爱的 [客户]，
>
> 最终通知：编号为 [number] 的发票已经逾期45天。如果7天内仍未付款，我们将不得不启动追讨流程。

所有邮件模板都可以根据需要进行自定义。

## 付款跟踪

```bash
# Mark invoice as paid
status.sh INV-042 --paid --date "2025-02-10"

# Add payment note
status.sh INV-042 --note "Client called, payment sent via check"

# Pause reminders (client asked for extension)
status.sh INV-042 --pause --until "2025-03-01"

# Archive without payment (write-off)
status.sh INV-042 --archive --reason "Bad debt write-off"
```

## 收款 aging 报告

```bash
# Show summary
scripts/report.sh

# Output:
# 📊 Accounts Receivable Aging Report
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Current (0-30 days):     $12,500  (5 invoices)
# 31-60 days:              $3,200   (2 invoices) ⚠️
# 61-90 days:              $1,800   (1 invoice)  🚨
# 90+ days:                $500     (1 invoice)  💀
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Total Outstanding:       $18,000  (9 invoices)

# Detail view
scripts/report.sh --detail

# Export to CSV
scripts/report.sh --export ar-aging-2025-01-28.csv
```

## 数据文件

```
~/.config/invoice-chaser/
├── config.json               # User configuration
├── invoices.json             # Invoice database (state machine)
├── chase-log.json            # Email send history
├── last-chase-report.json    # Latest chase run data
└── archives/
    └── YYYY-MM/              # Archived paid/written-off invoices
```

## 自动化设置

可以通过 cron 任务每天自动运行追款流程：

```bash
# Run every morning at 9 AM
0 9 * * * cd ~/clawd/skills/invoice-chaser && scripts/chase.sh >> ~/.config/invoice-chaser/chase.log 2>&1

# Weekly AR report to Telegram (Mondays at 8 AM)
0 8 * * 1 cd ~/clawd/skills/invoice-chaser && scripts/report.sh --channel telegram
```

或者使用 Clawdbot 的 cron 集成功能：
```bash
clawdbot cron add \
  --schedule "0 9 * * *" \
  --command "cd ~/clawd/skills/invoice-chaser && scripts/chase.sh" \
  --label "invoice-chaser-daily"
```

## 发票状态

```
DRAFT → SENT → REMINDED → OVERDUE → FIRM → FINAL → ESCALATED
                                                        ↓
                                                   (human intervention)
Any state → PAID ✅
Any state → PAUSED ⏸ (temporary hold)
Any state → ARCHIVED 📁 (written off or canceled)
```

## 与会计系统的集成

Invoice Chaser 可以跟踪付款状态。如需实现与会计系统的全面集成：
- 使用 `--export` 参数导出发票数据。
- 将数据导入 QuickBooks、FreshBooks 等会计软件。
- 或者自行开发自定义适配器（详见 `references/accounting-adapters.md`）。

## 安全功能

- **测试模式**：在不发送邮件的情况下测试邮件模板。
- **暂停提醒**：为有特殊情况的客户暂停提醒通知。
- **手动干预**：对敏感客户阻止自动升级。
- **邮件预览**：在首次发送前预览邮件内容。
- **发送频率限制**：限制每天发送邮件的数量，避免被标记为垃圾邮件。
- **取消订阅处理**：尊重客户的退订请求（手动将客户从跟踪列表中移除）。

## 最佳实践：

1. **保持一致性**：每天运行追款流程，帮助客户养成按时付款的习惯。
2. **个性化邮件内容**：在邮件中使用客户名称，并提及具体的工作内容。
3. **提供付款链接**：提供便捷的付款方式（如 Stripe、PayPal 或银行账户信息）。
4. **逐步升级沟通**：不要跳过任何沟通阶段，逐步提升语气以维护良好的关系。
5. **适时暂停**：如果客户沟通有困难，暂停追款并手动跟进。
6. **定期归档**：每月将已支付的发票移至归档文件夹，保持数据库整洁。
7. **定期监控**：每周生成收款 aging 报告，及时发现长期逾期付款的问题。

## 示例工作流程

**初始设置：**
```bash
scripts/setup.sh
# Edit ~/.config/invoice-chaser/config.json with your details
```

**发送发票后：**
```bash
scripts/add-invoice.sh --number "INV-042" --client "Acme Corp" --email "billing@acme.com" --amount 2500 --date "2025-01-15" --due "2025-02-14"
```

**每日自动追款（通过 cron）：**
```bash
scripts/chase.sh  # Runs every morning, sends reminders based on timing rules
```

**收到付款后：**
```bash
scripts/status.sh INV-042 --paid --date "2025-02-12"
```

**每周审核：**
```bash
scripts/report.sh  # Check AR aging, identify problem invoices
```

## 故障排除**

**邮件未发送：**
- 确保已安装 `gog` 插件：运行 `gog gmail whoami` 命令检查。
- 验证 `~/.clawdbot/secrets.env` 文件中的 `GOG_DEFAULT_ACCOUNT` 设置。
- 使用 `--dry-run` 参数测试邮件预览功能。

**升级阶段错误：**
- 检查 `config.json` 文件中的 `timing` 配置。
- 核对发票的 `date` 和 `due_date` 字段。
- 使用 `status.sh INV-XXX` 命令查看当前的计算结果。

**客户付款后仍收到提醒邮件：**
- 运行 `status.sh INV-XXX --paid` 命令将发票状态标记为已支付。
- 检查 `invoices.json` 文件以确认状态是否已更新。

## 使用理念

你完成了工作，理应获得报酬。你不应该为了收款而费心。

Invoice Chaser 负责处理自由职业者最头疼的部分——跟进未支付的发票。它通过持续的努力和适当的强硬态度来处理这些烦人的事务。在早期阶段，它会保持专业的沟通方式；但在必要时，它也会坚决维护你的权益。

现金流是小型企业的命脉。逾期付款会危及企业的生存。Invoice Chaser 帮你确保资金流动顺畅，让你能够专注于自己的核心工作。

---

**别再自己费心追款了，让 Invoice Chaser 来帮你吧！**