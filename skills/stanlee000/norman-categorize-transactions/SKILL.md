---
name: categorize-transactions
description: >
  **功能说明：**  
  审核并分类未分类的银行交易记录，将这些交易与发票进行匹配，并验证会计分录的准确性。  
  **适用场景：**  
  当用户需要审核交易记录、对支出进行分类、进行会计处理或核对银行账户余额时，可使用该功能。
version: 1.0.0
metadata:
  openclaw:
    emoji: "\U0001F3F7"
    homepage: https://norman.finance
    requires:
      mcp:
        - norman-finance
---
帮助用户对银行交易进行分类和组织：

1. **获取未分类的交易**：调用 `search_transactions` 来查找需要处理的交易。注意那些未验证或未分类的交易记录。

2. **智能分类**：对于每笔交易，根据以下信息建议一个分类：
   - 交易描述/参考文本
   - 交易对手名称
   - 交易金额及交易模式（如果交易是重复性的，很可能属于订阅服务）
   - 以往类似的交易记录

3. **更新交易分类**：使用 `categorize_transaction` 函数为交易分配正确的记账分类（适用于德国企业的 SKR04 账户体系）。

4. **发票匹配**：当某笔交易看起来像是收款时：
   - 调用 `list_invoices` 来查找匹配的未支付发票（可以按金额或客户名称进行筛选）
   - 使用 `link_transaction` 将收款记录与相应的发票关联起来

5. **文档附件**：提醒用户为支出交易附上收据：
   - 使用 `upload_bulkattachments` 功能上传多张收据
   - 使用 `link_attachment_transaction` 将收据与交易记录关联起来

6. **验证交易**：分类完成后，使用 `change_transaction_verification` 函数将交易标记为已验证状态。

建议以每批 10-15 笔交易的形式展示交易信息，以便于用户进行管理。展示的内容包括：日期、金额、交易描述以及建议的分类。