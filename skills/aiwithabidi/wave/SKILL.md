---
name: wave
description: "Wave Accounting：处理发票、客户、交易、账户、产品及税务信息的工具。专为小型企业设计的命令行界面（CLI）会计软件。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🌊", "requires": {"env": ["WAVE_API_TOKEN"]}, "primaryEnv": "WAVE_API_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 🌊 Wave  
为小型企业提供发票开具和会计管理功能——包括发票、客户信息以及交易记录。  

## 主要功能  
- **企业**：列出关联的企业信息  
- **发票**：创建、发送、查看及删除发票  
- **客户**：管理客户资料  
- **账目**：查看财务报表  
- **交易**：查看财务交易记录  
- **产品与税费**：管理商品信息及税率设置  

## 系统要求  
| 变量          | 是否必需 | 说明            |  
|--------------|---------|----------------|  
| `WAVE_API_TOKEN` | ✅      | Wave系统的API密钥/令牌      |  

## 快速入门  
```bash
python3 {baseDir}/scripts/wave.py businesses
python3 {baseDir}/scripts/wave.py invoices <business-id>
python3 {baseDir}/scripts/wave.py invoice-create <business-id> <customer-id> --amount 500
python3 {baseDir}/scripts/wave.py customers <business-id>
python3 {baseDir}/scripts/wave.py transactions <business-id>
```  

## 开发者信息  
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube频道](https://youtube.com/@aiwithabidi) | [GitHub仓库](https://github.com/aiwithabidi)  
该工具是 **AgxntSix Skill Suite** 的组成部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的企业设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)