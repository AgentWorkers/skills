---
name: lemonsqueezy
description: "Lemon Squeezy — 一款用于管理数字产品、订阅服务、订单、客户信息、结账流程、许可证密钥以及折扣的数字商业命令行工具（CLI）。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🍋", "requires": {"env": ["LEMONSQUEEZY_API_KEY"]}, "primaryEnv": "LEMONSQUEEZY_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🍋 Lemon Squeezy  
用于管理数字产品和订阅服务的相关功能，包括订单处理、结账流程、许可证管理以及折扣应用。  

## 主要功能  
- **产品与变体**：列出可购买的数字产品及其不同版本。  
- **订单**：查看用户的购买历史记录。  
- **订阅**：添加或取消订阅服务。  
- **结账**：创建结账会话以完成购买流程。  
- **许可证密钥**：激活并验证许可证的有效性。  
- **客户与折扣**：对客户信息进行管理和应用相应的折扣政策。  

## 系统要求  
| 变量          | 是否必需 | 说明                          |  
|------------------|---------|----------------------------------|  
| `LEMONSQUEEZY_API_KEY` | ✅     | Lemon Squeezy 的 API 密钥/令牌                |  

## 快速入门  
```bash
python3 {baseDir}/scripts/lemonsqueezy.py stores
python3 {baseDir}/scripts/lemonsqueezy.py products
python3 {baseDir}/scripts/lemonsqueezy.py orders
python3 {baseDir}/scripts/lemonsqueezy.py subscriptions
python3 {baseDir}/scripts/lemonsqueezy.py license-validate <key>
python3 {baseDir}/scripts/lemonsqueezy.py me
```  

## 开发者信息  
本项目由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 共同开发。  
更多相关信息请访问：[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
Lemon Squeezy 是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的业务配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)