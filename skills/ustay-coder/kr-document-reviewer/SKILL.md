---
name: kr-document-reviewer
description: "审核与验证韩国商业文件（包括税务发票、合同书、银行对账单副本、报价单、交易明细单、营业执照、业务费用申请函、补助金申请表、审核报告、转账确认单以及结果报告）。该功能用于检查这些文件的格式是否符合规范、所需字段是否填写完整、数据是否准确，以及文件内容之间是否保持一致。触发条件包括：文件审核、文件确认、税务发票验证、合同书审查、报价单确认、银行对账单验证、交易明细单确认、营业执照验证、审核报告验证、转账确认单验证以及结果报告审核。"
---

# 韩国商务文件审核技巧

文件以图片或PDF格式接收并进行审核。需遵循每种文件类型的必填项和验证规则。

## 工作流程 — 使用Sonnet子代理进行分布式处理（推荐）

当文件种类超过3种时，建议采用**Sonnet子代理分布式处理**方式：
这种方式可将成本降低约30%，并且由于并行处理，速度也会更快。

### 第一阶段：预处理

1. 将PDF转换为图片（使用`pdftoppm -png -r 200`命令）。
2. **确认文件类型**：如果文件名为UUID格式，仅凭文件名无法判断文件类型，需在**第二阶段**进行自动识别。
3. 将文件按2-3种类型进行分组（将相关文件放在一起）；
   - 如果文件与类型之间的对应关系不明确，需将所有文件平均分成2-3组，并指示“先阅读文件，再确定类型”。

### 第二阶段：使用Sonnet子代理进行OCR处理及单独审核

将每个分组通过`sessions_spawn`任务委托给Sonnet子代理：

**分组示例（基于11种文件类型）：**
- 组1：税务发票 + 转账确认单（可核对金额）
- 组2：合同书 + 报价单（可核对金额/商品信息）
- 组3：检验报告 + 交易明细单（可核对交货/检验信息）
- 组4：银行对账单×2 + 企业注册证（可核对机构信息）
- 组5：补助金申请表（或费用申请函、结果报告）

**子代理任务编写规则：**
- 明确指定图片文件路径，并指示使用“Read tool”进行阅读。
- 在任务中包含针对文件类型的检查清单。
- **指定返回格式为JSON**（用于交叉验证的关键数据）。
- 关键字段包括：企业注册号、公司名称、负责人、金额、日期、账号。
- 包含**自动识别文件类型的指令**（如果文件名为UUID格式，可能无法自动识别类型）。
- 如果文件类型与预期不同，需指示子代理提取实际类型。

### 第三阶段：交叉验证（使用Sonnet子代理）

收到子代理的结果后：
1. 收集JSON结果，并根据实际文件类型重新整理数据。
2. **额外启动一个用于交叉验证的Sonnet子代理**，将所有提取的数据及验证项以文本形式传递给该代理。
3. 交叉验证代理生成最终报告。

**需传递给交叉验证代理的内容：**
- 第二阶段提取的JSON数据（以文本形式）。
- 验证项列表（企业注册号、金额、日期、双方信息、账号、缺失的文件）。
- 指定报告的输出格式。

**注意：**不要将图片发送给交叉验证代理（仅发送文本，以节省Token）。
对可疑的OCR结果，需在主会话中直接查看原始图片。

### 成本对比

| 处理方式 | 成本 | 备注 |
|------|------|------|
| 在Opus主系统中直接处理 | 约12美元 | 随着处理量的增加，成本会急剧上升 |
| 使用Sonnet子代理进行分布式处理 | 约0.7美元 | **成本降低约94%**（基于11种文件、14页的实际测试数据） |

---

## 工作流程 — 单一会话（文件种类为1-2种）

如果文件种类只有1-2种，也可以在主会话中直接处理：

1. 确定文件类型。
2. 加载相应类型的检查清单（文件路径：`references/<type>.md`）。
3. 进行OCR处理或提取文本（图片 → vision工具；PDF → pdftoppm + read命令）。
4. 根据检查清单逐项验证文件。
5. 输出审核结果报告。

---

## 各文件类型的参考文档

- **税务发票**：[references/tax-invoice.md](references/tax-invoice.md)
- **合同书**：[references/contract.md](references/contract.md)
- **银行对账单**：[references/bank-account.md](references/bank-account.md)
- **报价单**：[references/estimate.md](references/estimate.md)
- **交易明细单**：[references/transaction-statement.md](references/transaction-statement.md)
- **企业注册证**：[references/business-registration.md](references/business-registration.md)
- **费用申请函**：[references/expense-request.md](references/expense-request.md)
- **补助金申请表**：[references/subsidy-application.md](references/subsidy-application.md)
- **检验报告**：[references/inspection-report.md](references/inspection-report.md)
- **转账确认单**：[references/transfer-confirmation.md](references/transfer-confirmation.md)
- **结果报告**：[references/result-report.md]

## 审核结果输出格式

### 基本格式：JSON输出

JSON格式规范：[`schema/review-result.schema.json`](schema/review-result.schema.json)
示例输出：[`schema/sample-output.json`](schema/sample-output.json)

**结构如下：**
```
{
  "meta": { reviewDate, reviewId, transaction: { summary, buyer, supplier, totalAmount } },
  "documents": [
    {
      docId, docType, party, status(pass|warning|fail),
      extractedData: { businessRegNo, companyName, representative, address,
                       supplyAmount, taxAmount, totalAmount, date,
                       bankName, accountNo, accountHolder, items },
      checklist: [ { item, status(pass|warning|fail|na), value?, note? } ]
    }
  ],
  "crossValidation": [
    {
      category(금액흐름|당사자정보|계좌정보|날짜정합성|누락서류),
      item, status, expected, actual, docs[], note?
    }
  ],
  "summary": { totalDocs, pass, warning, fail, criticalIssues[], actionRequired[], opinion }
}
```

**向子代理发送JSON格式的规范时需说明：**
- 第二阶段的OCR处理子代理：仅返回`documents[]`数组。
- 第三阶段的交叉验证子代理：返回`crossValidation[]`和`summary`。
- 主会话中添加`meta`字段后，再组装最终的JSON结果。

**输出文件：**
- 将JSON结果保存在工作空间：`reviews/REV-{YYYYMMDD}-{NNN}.json`
- 在聊天中仅发送基于`summary`的摘要（根据Discord等聊天渠道的特性进行格式化）。

### 用于聊天的摘要输出（辅助功能）

根据JSON结果的`summary`内容，生成适合聊天渠道的摘要格式：

```
## 📋 서류 검토 결과 (N건)

**거래 개요**: (요약)

### ✅ 일치 확인 항목
- (항목): (설명)

### ⚠️ 주의 항목
- (항목): (설명)

### ❌ 누락/오류 항목
- (항목): (설명)

### 💡 조치 필요
1. 🔴 (high) ...
2. 🟡 (medium) ...
```

## 交叉验证项目

当提交多份文件时，需进行文件间的交叉验证：

### 金额核对
- 报价单上的执行金额与合同书上的合同金额是否一致？
- 合同书上的金额与税务发票上的供应金额是否一致？
- 税务发票上的总金额（含增值税）与转账确认单上的金额是否一致？
- 检验报告上的金额与税务发票上的供应金额是否一致？
- 交易明细单上的供应金额与税务发票上的供应金额是否一致？
- 申请表上的执行明细与税务发票/合同书上的金额是否一致？
- 结果报告中的费用金额与合同书/税务发票上的金额是否一致？

### 双方信息核对
- 所有文件中的企业注册号是否一致？
- 公司名称/负责人名称是否一致？
- 企业注册证上的信息与税务发票/合同书/报价单上的信息是否一致？
- 企业类型（法人/个人）是否一致（根据企业注册证与合同书判断）？

### 账户信息核对
- 转账确认单上的付款账号与受助企业的银行对账单是否一致？
- 转账确认单上的收款账号与供应商机构的银行对账单是否一致？
- 申请表上的收款账号与受助企业的银行对账单是否一致？
- 对账单上的存款人是否与合同中的交易方一致？

### 日期核对
- 报价日期 → 合同签订日期 → 税务发票/转账日期 → 检验日期 → 申请日期（确认顺序）。
- 如果存在预付款情况，税务发票的日期可能早于检验日期（需特别标注）。

### Sonnet OCR错误修正规则（基于实际测试数据）
- 账号前缀缺失（例如：601- → 01-）
- 韩文人名误读（例如：“홍길동” → “홍길등”，“김철수” → “김첼수”，“박영희” → “박영의”）
- 公司名称误读（例如：“대성테크” → “대상테크”，“대성데코”）
- 企业类型误读（例如：“제조업” → “현대”）
- 管理点名称/电话号码混淆
- 存款类型误读
- 地址细节错误（例如：“외동읍” → “안동읍”，“문산산단” → “문산2산1”）
**核对原则：**当OCR结果与其他文件不一致时，需直接查看原始图片进行确认。