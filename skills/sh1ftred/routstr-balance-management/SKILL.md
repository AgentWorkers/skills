---
name: balance-management
description: 管理 Routstr 的余额：可以通过查看余额、创建用于充值的 Lightning 发票以及检查发票的支付状态来实现。
license: MIT
compatibility: opencode
---

## 我的功能  
- 检查当前Routstr API的余额（以satoshis和BTC为单位）  
- 显示使用统计信息（总花费、总请求次数）  
- 生成用于充值支付的Lightning发票  
- 查看现有发票的支付状态  
- 使用Cashu代币为账户充值  

## 何时使用我  
当你需要以下操作时，请使用我：  
- 查看当前Routstr账户的余额  
- 通过生成Lightning发票为账户充值  
- 验证之前创建的发票是否已支付  

## 如何使用我  
这些shell脚本从`~/.openclaw/openclaw.json`文件中读取API配置：  
- `check_balance.sh`：不带参数运行时，会显示当前余额和使用情况  
- `createinvoice.sh <amount_sats>`：为指定金额（以satoshis为单位）生成发票  
- `invoice_status.sh <invoice_id>`：查看发票的支付状态  
- `topup_cashu.sh <cashu_token>`：使用Cashu代币为账户充值  

为方便查看，所有金额都会同时以satoshis和BTC的形式显示。