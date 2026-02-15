---
name: autonomous-bookkeeper
description: 这是一个用于实现预会计自动化的元技能（meta-skill），它整合了 Gmail、DeepRead-OCR、Stripe API 和 Xero 等工具。当用户需要从电子邮件中接收发票信息、提取结构化数据、验证支付信息，并创建具备对账功能的会计记录时，可以使用该技能。
homepage: https://clawhub.ai
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"ledger","requires":{"bins":["python3","npx"],"env":["MATON_API_KEY","DEEPREAD_API_KEY"],"config":[]},"note":"Requires local installation of gmail, deepread-ocr, stripe-api, and xero."}}
---

## 目的

自动化处理从收到的电子邮件到会计记录的准备工作。

**核心目标：**
1. 检测包含发票信息的电子邮件；
2. 提取发票的结构化数据；
3. 验证支付事件；
4. 创建会计分录并更新对账状态。

这是跨上游工具的协调逻辑，不能替代财务控制机制。

## 所需安装的技能

- `gmail`（最新版本：`1.0.6`）
- `deepread-ocr`（最新版本：`1.0.6`）
- `stripe-api`（最新版本：`1.0.8`）
- `xero`（最新版本：`1.0.4`）

**安装/更新：**

```bash
npx -y clawhub@latest install gmail
npx -y clawhub@latest install deepread-ocr
npx -y clawhub@latest install stripe-api
npx -y clawhub@latest install xero
npx -y clawhub@latest update --all
```

## 所需的凭证

- `MATON_API_KEY`（用于通过Maton网关访问Gmail、Stripe和Xero）
- `DEEPREAD_API_KEY`（用于OCR数据提取）

**前置检查：**

```bash
echo "$MATON_API_KEY" | wc -c
echo "$DEEPREAD_API_KEY" | wc -c
```

如果缺少任何凭证，请在执行任何记账操作之前停止流程。

## 需要首先收集的输入参数

- `company_base_currency`（公司基础货币）
- `invoice_keywords`（关键词，例如：invoice、rechnung、receipt、quittung）
- `vendor_rules`（供应商规则，例如：AWS对应“托管费用”账户）
- `date_tolerance_days`（匹配日期的容忍范围，默认值：3天）
- `amount_tolerance`（金额的容忍范围，默认为精确匹配，或可配置为小范围容忍）
- `auto_post_policy`（自动发布策略，例如：`manual-review`或`auto-if-high-confidence`）
- `attachment_policy`（附件处理策略，例如：`store-link`或`attach-binary-if-supported`）

**注意：** 未经明确授权，切勿自动发布财务记录。

## 各工具的职责

### Gmail

用于接收邮件并检测附件。

**相关操作：**
- 使用Gmail的操作符查询邮件（例如：`has:attachment`、`subject:invoice`、发送者过滤）
- 获取邮件的元数据和完整内容以供解析
- 处理完成后对邮件进行标记或更新（以便追踪）

### DeepRead OCR

用于从发票PDF或图片中提取结构化数据。

**相关操作：**
- 异步处理（状态从`queued`变为`completed`或`failed`）
- 基于模式的字段提取
- 每个字段都会附带`hil_flag`（表示数据是否可靠）及原因说明
- 支持Webhook或轮询模式

### Stripe

用于支付方面的验证。

**相关操作：**
- 查询费用、支付意图、发票和余额交易
- 验证金额、货币、状态和日期是否匹配

### Xero

用于创建会计记录并查看支付/对账情况。

**相关操作：**
- 如果缺少联系人信息，则创建联系人
- 创建发票/账单（类型为`ACCPAY`）
- 列出支付记录和银行交易

## 标准信号链

### 第1阶段：收件箱检测

在Gmail收件箱中扫描可能包含发票信息的邮件。

**推荐的查询模式：**
- `has:attachment (subject:invoice OR subject:rechnung OR subject:receipt OR subject:quittung)`
- 可选地根据已知供应商设置发送者过滤条件（例如：`from:aws`）

**输出结果：**
- 邮件ID
- 发件人
- 收件日期
- 可能包含发票的附件

### 第2阶段：附件提取

对于每个可能包含发票的附件：
1. 将文件发送给DeepRead OCR，并提供发票的结构化数据模型。
2. 等待异步处理完成（优先使用Webhook；轮询作为备用方案）
3. 解析提取的结果。

**必须提取的字段：**
- 供应商名称
- 发票日期
- 发票编号
- 总金额
- 税额
- 货币类型

**质量检查：**
- 如果关键字段的`hil_flag`为`true`，则将邮件放入审核队列，待人工审核后再发布。

### 第3阶段：支付验证

使用Stripe验证是否已发生相应的支付。

**匹配规则：**
- 金额与发票总额相符（在允许的容忍范围内）
- 货币类型一致
- 日期在规定的容忍范围内
- 状态显示为“已支付”

如果有多个匹配项，标记为`ambiguous_match`，需要人工审核。

### 第4阶段：会计记录创建

使用Xero进行记账操作。

**默认的支付流程：**
1. 确保供应商联系人信息存在（如需创建则创建）
2. 创建账单分录（类型为`ACCPAY`），并指定相应的费用类别（例如：托管费用）
3. 仅当Stripe验证结果确认为“已支付”时，将状态标记为“已支付/已对账”
4. 包含参考字段：发票编号、源邮件ID、支付参考信息

**附件处理：**
- 如果集成支持二进制附件的上传，直接附加文件
- 否则，存储文件的引用链接，并在描述或元数据中提供该链接

### 第5阶段：可追溯性更新

处理完成后：
- 应用Gmail处理的标签
- 保存处理日志（源邮件地址、提取结果的可靠性、匹配证据、Xero记录ID）
- 保持idempotency key（防重复记录）

## 场景映射（以AWS发票为例）

对于“通过电子邮件接收AWS发票 -> 在Xero中创建账单并匹配支付记录”的场景：
1. Gmail找到包含PDF附件的AWS邮件。
2. DeepRead OCR提取发票的详细信息（供应商、日期、总金额、税额、发票编号）。
3. Stripe验证支付事件是否与发票信息一致。
4. Xero创建属于“托管费用”类别的应付账单。
5. 仅当验证结果确认后，才将记录标记为“已支付”；并根据策略附上源PDF文件。

## 数据规范

在发布之前，所有数据需统一为一条交易记录：

```json
{
  "source": {
    "gmail_message_id": "...",
    "sender": "billing@aws.amazon.com",
    "attachment_name": "invoice.pdf"
  },
  "invoice": {
    "vendor": "AWS",
    "invoice_number": "INV-123",
    "invoice_date": "2024-05-01",
    "total": 53.20,
    "tax": 0.00,
    "currency": "USD",
    "ocr_confidence_ok": true
  },
  "payment_match": {
    "provider": "stripe",
    "matched": true,
    "transaction_id": "ch_...",
    "amount": 53.20,
    "date": "2024-05-01"
  },
  "accounting": {
    "system": "xero",
    "entry_type": "ACCPAY",
    "category": "Hosting",
    "status": "Paid"
  }
}
```

## 输出结果

始终返回以下信息：
- `IntakeSummary`：扫描的邮件数量及找到的发票候选项
- `ExtractionSummary`：提取的字段及`hil_flag`状态
- `PaymentVerification`：匹配情况及验证证据
- `AccountingAction`：创建/更新的记录及其ID
- `ReviewQueue`：需要人工审核的记录

## 质量检查

在自动发布之前，需满足以下条件：
- 供应商信息已识别
- 发票编号、日期和总额信息齐全
- 无关键的`hil_flag`未解决
- 支付匹配的可靠性超过政策设定的阈值
- 无重复记录

**异常处理规则：**
- 无支付证据时，切勿将发票标记为已支付。
- 严禁默默覆盖现有的会计记录。
- 对于不确定的OCR数据，必须明确显示。
- 当金额或日期存在疑问时，优先进行人工审核。
- 保留每个记账操作的审计痕迹。

## 失败处理机制：
- 如果Gmail无法访问，停止接收流程并报告连接问题。
- OCR处理失败或超时：将邮件放入重试队列。
- 如果Stripe无法匹配支付信息，根据策略将发票标记为未支付状态或放入审核队列。
- 如果Xero的记账操作失败，保留已处理的记录，并使用idempotency key尝试重新提交。

## 上游工具的已知限制：
- DeepRead OCR是异步处理的，可能需要配合Webhook或轮询机制。
- Xero的文档主要介绍了核心的会计接口，但未详细说明附件上传的流程；附件的处理方式取决于实际集成中支持的接口路径。
- Stripe和Xero之间的匹配逻辑是自动化处理的，这些文档中并未提供单一的“自动对账”接口。
- QuickBooks不在本次研究的技能范围内；本技能优先使用Xero。

请将上述限制视为必须向用户明确说明的操作细节。