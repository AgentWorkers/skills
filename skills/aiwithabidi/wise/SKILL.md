---
name: wise
description: "Wise（TransferWise）——提供国际转账服务、多货币账户管理、收款人信息查询、实时汇率更新以及交易明细报表。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "💸", "requires": {"env": ["WISE_API_TOKEN"]}, "primaryEnv": "WISE_API_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 💸 Wise

Wise（TransferWise）——提供国际转账、多货币账户管理、收款人信息、汇率查询以及交易对账单等服务。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `WISE_API_TOKEN` | ✅ | Wise API令牌 |


## 快速入门

```bash
# List profiles (personal/business)
python3 {{baseDir}}/scripts/wise.py get-profiles

# Get multi-currency balances
python3 {{baseDir}}/scripts/wise.py get-balances --profile-id <value>

# List recipients
python3 {{baseDir}}/scripts/wise.py list-recipients --profile-id <value>

# Create recipient
python3 {{baseDir}}/scripts/wise.py create-recipient --profile-id <value> --currency <value> --type <value> --details "JSON"

# Create transfer quote
python3 {{baseDir}}/scripts/wise.py create-quote --profile-id <value> --source <value> --target <value> --amount <value>

# Create transfer
python3 {{baseDir}}/scripts/wise.py create-transfer --quote-id <value> --recipient-id <value> --reference <value>

# Fund a transfer
python3 {{baseDir}}/scripts/wise.py fund-transfer --profile-id <value> --transfer-id <value>

# Get transfer status
python3 {{baseDir}}/scripts/wise.py get-transfer <id>

# List transfers
python3 {{baseDir}}/scripts/wise.py list-transfers --profile-id <value> --limit "10"

# Get exchange rate
python3 {{baseDir}}/scripts/wise.py get-rate --source <value> --target <value>

# Get statement
python3 {{baseDir}}/scripts/wise.py get-statement --profile-id <value> --balance-id <value>
```


## 输出格式

所有命令默认以JSON格式输出结果。


## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/wise.py` | 主要的命令行工具（包含所有Wise相关命令） |


## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，代码源代码托管在 [GitHub](https://github.com/aiwithabidi) 上。  
该工具是 **AgxntSix Skill Suite** 的一部分，专为OpenClaw代理设计。  

📅 **需要帮助为您的业务设置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)