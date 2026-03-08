---
name: wise-readonly
description: 仅限读取的Wise API操作，用于账户查询、外汇汇率查询、收款人信息以及转账历史记录的获取。当需要列出用户资料、账户余额、收款人信息、转账记录、报价信息、交货预估时间，或查看当前/历史汇率时，可以使用这些API，但无需创建新的转账记录、收款人信息或报价信息等可变数据。
---
**OpenClaw的只读Wise API技能**

## **要求**  
- 需要设置`WISE_API_TOKEN`环境变量。  
- 运行时主机必须能够访问`https://api.wise.com`。  

## **支持的命令**  
- `list_profiles`（默认会屏蔽个人身份信息（PII）  
- `get_profile --profile-id <id>`（默认会屏蔽个人身份信息）  
- `list_balances --profile-id <id> [--types STANDARD,SAVINGS]`  
- `get_balance --profile-id <id> --balance-id <id>`  
- `get_exchange_rate --source <CUR> --target <CUR>`  
- `get_exchange_rate_history --source <CUR> --target <CUR> --from <ISO> --to <ISO> [--group day|hour|minute]`  
- `get_temporary_quote --source <CUR> --target <CUR> [--source-amount <N> | --target-amount <N>]`  
- `get_quote --quote-id <id>`  
- `list_recipients --profile-id <id> [--currency <CUR>]`（默认会屏蔽个人身份信息）  
- `get_recipient --account-id <id>`（默认会屏蔽个人身份信息）  
- `get_account_requirements --source <CUR> --target <CUR> --source-amount <N>`  
- `list_transfers --profile-id <id> [--status <s>] [--created-date-start <ISO>] [--created-date-end <ISO>] [--limit <N>] [--offset <N>]`（默认会屏蔽个人身份信息）  
- `get_transfer --transfer-id <id>`（默认会屏蔽个人身份信息）  
- `get_delivery_estimate --transfer-id <id>`  

**命令执行脚本**：`scripts/wise_readonly.mjs`  

## **隐私与安全**  
- 默认情况下，响应中会屏蔽个人身份信息（PII）相关的字段。  
- 仅在绝对必要时才使用`--raw`选项。  
- 该技能仅支持读操作，不执行任何写操作。  
- 禁止执行的操作包括创建报价、转账、创建/更新/删除收款人信息、资金转账以及取消操作。  

## **快速测试**  
```bash
export WISE_API_TOKEN=...
node scripts/wise_readonly.mjs list_profiles
node scripts/wise_readonly.mjs list_balances --profile-id <id>
node scripts/wise_readonly.mjs get_exchange_rate --source GBP --target EUR
```  

## **版本说明**  
### 1.0.3**  
- 基于`wise-mcp`的架构，扩展了只读API的功能。  
- 新增了查询余额、收款人信息、转账记录、报价信息以及历史汇率的只读命令。  
- 严格遵循“只读”原则，禁止任何写入操作（如创建、转账、删除等）。  
- 改进了ClawHub和OpenClaw用户界面的元数据显示效果。  

### 1.0.2**  
- 添加了ClawHub所需的秘密元数据（必须提供`WISE_API_TOKEN`）。  
- 默认情况下，用户界面会禁止隐式调用相关功能。  

### 1.0.1**  
- 实现了个人身份信息的屏蔽功能，并优化了错误处理机制。  
- 移除了允许创建报价的写操作。  

### 1.0.0**  
- 首次实现了只读查询个人资料、余额和汇率的功能。  

## **来源参考**  
该技能基于以下项目的只读接口设计进行扩展：  
https://github.com/Szotasz/wise-mcp  

## **致谢**  
该技能的实现灵感来源于Szotasz开发的`wise-mcp`项目：  
https://github.com/Szotasz/wise-mcp