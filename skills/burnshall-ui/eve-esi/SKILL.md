---
name: eve-esi
description: "通过 ESI（EVE Swagger Interface）REST API 查询和管理《EVE Online》中的角色。当用户需要查询《EVE Online》中的角色信息、钱包余额、ISK（游戏内货币）交易记录、资产、技能队列、技能点数、角色克隆位置、植入物、装备配置、合约、市场订单、邮件内容、工业任务、击杀通知、行星互动信息、忠诚度点数，或任何其他与《EVE Online》账户管理相关的信息时，可以使用该接口。"
primary_credential: EVE_REFRESH_MAIN
env:
  - name: EVE_CLIENT_ID
    description: "EVE Developer Application Client ID (from https://developers.eveonline.com/applications)"
    required: true
    sensitive: false
  - name: EVE_TOKEN_MAIN
    description: "ESI OAuth2 access token for the main character. Expires after ~20 minutes."
    required: true
    sensitive: true
  - name: EVE_REFRESH_MAIN
    description: "ESI OAuth2 refresh token for automatic access token renewal."
    required: true
    sensitive: true
  - name: TELEGRAM_BOT_TOKEN
    description: "Telegram Bot API token for sending alerts and reports."
    required: false
    sensitive: true
  - name: TELEGRAM_CHAT_ID
    description: "Telegram chat ID where notifications are sent."
    required: false
    sensitive: false
  - name: DISCORD_WEBHOOK_URL
    description: "Discord webhook URL for sending alerts and reports."
    required: false
    sensitive: true
---

# 数据处理

该功能仅与EVE Online的官方ESI API（`esi.evetech.net`）和EVE SSO（`login.eveonline.com`）进行交互。  
任何角色数据都不会被传输到第三方服务器。  
可选的集成功能（如Telegram、Discord）由用户通过环境变量进行配置，且仅会传输用户自定义的警报信息。

# EVE Online ESI  

ESI（EVE Swagger接口）是EVE Online官方提供的第三方开发REST API：  
- 基本URL：`https://esi.evetech.net/latest`  
- 规范文档：`https://esi.evetech.net/latestswagger.json`  
- API浏览器：<https://developers.eveonline.com/api-explorer>  

## 认证  

ESI使用EVE SSO进行OAuth 2.0认证。大多数角色相关接口都需要具有正确权限范围的访问令牌。  

认证流程如下：  
1. 在<https://developers.eveonline.com/applications>注册应用程序。  
2. 将用户重定向到EVE SSO的授权页面以获取所需的权限范围。  
3. 用授权码换取访问令牌和刷新令牌。  
4. 在所有ESI请求中添加`Authorization: Bearer <TOKEN>`头。  

详细信息（包括PKCE、令牌刷新、权限范围等）请参阅[references/authentication.md]。  

## 公共接口（无需认证）  

```bash
# Character public info
curl -s "https://esi.evetech.net/latest/characters/2114794365/" | python -m json.tool

# Portrait URLs
curl -s "https://esi.evetech.net/latest/characters/2114794365/portrait/"

# Corporation history
curl -s "https://esi.evetech.net/latest/characters/2114794365/corporationhistory/"

# Bulk affiliation lookup
curl -s -X POST "https://esi.evetech.net/latest/characters/affiliation/" \
  -H "Content-Type: application/json" \
  -d '[2114794365, 95538921]'
```  

## 角色信息（已认证用户可访问）  

```bash
TOKEN="<your_access_token>"
CHAR_ID="<your_character_id>"

# Online status (scope: esi-location.read_online.v1)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/online/"
```  

## 钱包信息  

```bash
# Balance (scope: esi-wallet.read_character_wallet.v1)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/wallet/"

# Journal (paginated)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/wallet/journal/?page=1"

# Transactions
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/wallet/transactions/"
```  

## 资产信息  

```bash
# All assets (paginated; scope: esi-assets.read_assets.v1)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/assets/?page=1"

# Resolve item locations
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '[1234567890, 9876543210]' \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/assets/locations/"

# Resolve item names
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '[1234567890]' \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/assets/names/"
```  

## 技能信息  

```bash
# All trained skills + total SP (scope: esi-skills.read_skills.v1)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/skills/"

# Skill queue (scope: esi-skills.read_skillqueue.v1)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/skillqueue/"

# Attributes (intelligence, memory, etc.)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/attributes/"
```  

## 角色位置与飞船信息  

```bash
# Current location (scope: esi-location.read_location.v1)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/location/"

# Current ship (scope: esi-location.read_ship_type.v1)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/ship/"
```  

## 克隆与植入物信息  

```bash
# Jump clones + home station (scope: esi-clones.read_clones.v1)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/clones/"

# Active implants (scope: esi-clones.read_implants.v1)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/implants/"
```  

## 其他接口  

有关合约、飞船改装、邮件、工业任务、击杀通知、市场订单、采矿、行星交互、忠诚度点数、蓝图、排名等角色相关功能的详细信息，请参阅[references/endpoints.md]。  

## 仪表盘配置  

该功能支持模块化的仪表盘配置，用于显示警报、报告和市场数据跟踪。用户可通过JSON配置文件自定义所需显示的内容：  
- **配置规范**：[config/schema.json]（包含所有字段、类型及默认值）  
- **示例配置**：[config/example-config.json]（可直接使用的模板）  

### 主要功能  

| 模块 | 描述 |  
|--------|-------------|  
| **警报** | 实时监控战争决策、结构攻击、技能完成情况、钱包变动、工业任务、击杀通知等。 |  
| **报告** | 定时生成报告，内容包括净资产、技能任务列表、工业活动、市场订单、钱包状况和资产信息。 |  
| **市场** | 提供价格跟踪功能，支持绝对阈值和趋势分析。 |  

### 安全性提示  

令牌**严禁**以明文形式存储。建议使用环境变量来存储令牌信息：  
```json
{
  "token": "$ENV:EVE_TOKEN_MAIN",
  "refresh_token": "$ENV:EVE_REFRESH_MAIN"
}
```  

配置文件应保存在工作区之外（例如：`~/.openclaw/eve-dashboard-config.json`）。  

### 配置文件验证  

```bash
python scripts/validate_config.py path/to/config.json

# Show example config
python scripts/validate_config.py --example

# Show JSON schema
python scripts/validate_config.py --schema
```  

## 查询脚本的使用  

`scripts/esi_query.py`提供了一个可重用的Python脚本，用于处理分页请求、错误限制和缓存设置。  

```bash
# Simple query
python scripts/esi_query.py --token "$TOKEN" --endpoint "/characters/$CHAR_ID/wallet/" --pretty

# Fetch all pages of assets
python scripts/esi_query.py --token "$TOKEN" --endpoint "/characters/$CHAR_ID/assets/" --pages --pretty

# POST request (e.g. asset names)
python scripts/esi_query.py --token "$TOKEN" --endpoint "/characters/$CHAR_ID/assets/names/" \
  --method POST --body '[1234567890]' --pretty
```  

## 最佳实践：  
- **缓存策略**：遵守`Expires`头部字段的设置，避免在令牌过期前频繁请求。  
- **错误处理**：监控`X-ESI-Error-Limit-Remain`头部信息，当请求次数达到限制时暂停请求。  
- **User-Agent**：务必设置包含联系信息的描述性User-Agent。  
- **请求频率限制**：部分接口（如邮件、合约相关接口）有内部请求频率限制，超出限制会返回HTTP 520错误。  
- **分页机制**：根据`X-Pages`头部字段进行分页请求（示例：`?page=N`）。  
- **版本控制**：使用`/latest/`路径访问当前稳定的API版本；`/dev/`路径可能随时更新。  

## 类型ID的解析  

ESI返回的类型ID为数字形式（例如飞船、物品、技能的ID）。可通过以下方式解析这些ID以获取对应的名称：  
```bash
# Single type
curl -s "https://esi.evetech.net/latest/universe/types/587/"

# Bulk names (up to 1000 IDs)
curl -s -X POST "https://esi.evetech.net/latest/universe/names/" \
  -H "Content-Type: application/json" \
  -d '[587, 638, 11393]'
```