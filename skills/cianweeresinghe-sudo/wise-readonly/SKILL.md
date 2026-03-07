---
name: wise-readonly
description: 仅读的Wise API操作，用于账户检查和外汇查询。当需要列出账户信息、查看余额、获取账户详情或查询汇率时使用，无需创建转账记录、指定收款人、生成报价或其他可修改的资源。
---
**OpenClaw的只读Wise API技能**

## **要求**  
- 必须设置`WISE_API_TOKEN`环境变量。  
- 运行时主机需要能够访问`https://api.wise.com`。  

## **支持的命令**  
- `list_profiles`（默认会屏蔽个人身份信息（PII）  
- `get_profile --profile-id <id>`（默认会屏蔽个人身份信息）  
- `list_balances --profile-id <id>`  
- `get_exchange_rate --source <CUR> --target <CUR>`  

**命令执行脚本**：`scripts/wise_readonly.mjs`  

## **隐私与安全**  
- 响应数据会默认屏蔽常见的个人身份信息（PII）字段。  
- 仅在绝对必要时才使用`--raw`选项。  
- 该技能不执行任何写入操作。  
- 禁止执行的操作包括创建报价、转账、创建/更新/删除收款人、资金充值以及取消交易等操作。  

## **快速测试**  
```bash
export WISE_API_TOKEN=...
node scripts/wise_readonly.mjs list_profiles
node scripts/wise_readonly.mjs list_balances --profile-id <id>
node scripts/wise_readonly.mjs get_exchange_rate --source GBP --target EUR
```  

## **故障排除**  
- **错误代码403（未经授权）**：检查令牌的有效性、权限范围以及Wise的IP白名单。  
- **令牌为空或缺失**：确保在同一shell环境中设置了`WISE_API_TOKEN`。  

## **致谢**  
该技能的实现灵感来源于Szotasz的`wise-mcp`项目：  
https://github.com/Szotasz/wise-mcp