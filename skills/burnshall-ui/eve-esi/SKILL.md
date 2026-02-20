---
name: eve-esi
description: "通过 ESI（EVE Swagger Interface）REST API 查询和管理《EVE Online》中的角色。当用户需要查询《EVE Online》中的角色数据、钱包余额、ISK 交易记录、资产信息、技能队列、技能点数、克隆位置、植入物信息、装备配置、合约详情、市场订单、邮件内容、工业任务、击杀通知、星球交互信息、忠诚度点数，或任何其他与《EVE Online》账户管理相关的信息时，可以使用该接口。"
env:
  - name: EVE_CLIENT_ID
    description: "EVE Developer Application Client ID (from https://developers.eveonline.com/applications). Optional: only needed if using $ENV: references in your dashboard config instead of passing --client-id to auth_flow.py directly."
    required: false
    sensitive: false
  - name: EVE_TOKEN_MAIN
    description: "ESI OAuth2 access token for the main character. Optional: scripts auto-manage tokens via ~/.openclaw/eve-tokens.json (written by auth_flow.py). Only set this if using $ENV: references in your dashboard config."
    required: false
    sensitive: true
  - name: EVE_REFRESH_MAIN
    description: "ESI OAuth2 refresh token for automatic access token renewal. Optional: scripts auto-manage tokens via ~/.openclaw/eve-tokens.json. Only set this if using $ENV: references in your dashboard config."
    required: false
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

该技能仅与官方的EVE Online ESI API (`esi.evetech.net`) 和 EVE SSO (`login.eveonline.com`) 进行交互。  
任何角色数据都不会被传输到第三方服务器。  
可选的集成功能（如Telegram、Discord）由用户通过环境变量进行配置，且仅传输用户自定义的警报信息。

# EVE Online ESI  

ESI（EVE Swagger Interface）是EVE Online的官方REST API，用于第三方开发：  
- 基本URL：`https://esi.evetech.net/latest`  
- 规范文档：`https://esi.evetech.net/latestswagger.json`  
- API浏览器：`<https://developers.eveonline.com/api-explorer>`  

## 技能文件存放位置  

所有相关脚本均位于：`~/.openclaw/workspace/skills/eve-esi/scripts/`  

调用脚本时请使用完整路径：  
```bash  
SKILL=~/.openclaw/workspace/skills/eve-esi  
```  

## 认证  

认证令牌存储在 `~/.openclaw/eve-tokens.json` 文件中（由 `auth_flow.py` 生成，权限设置为 `chmod 600`）。  
所有脚本（`get_token.py`、`esi_query.py`）都会直接从这个文件中读取令牌——**正常运行无需环境变量**。  

**首次设置**（每个角色仅需执行一次）：  
1. 在本地电脑上建立SSH隧道：  
   ```bash  
   ssh -L 8080:127.0.0.1:8080 user@your-server -N  
   ```  
2. 在服务器上运行认证脚本（直接提供客户端ID）：  
   ```bash  
   python3 ~/.openclaw/workspace/skills/eve-esi/scripts/auth_flow.py --client-id <YOUR_CLIENT_ID> --char-name main  
   ```  
3. 在浏览器中打开相应URL，使用EVE账户登录。  

**获取新的访问令牌**（令牌有效期约为20分钟，系统会自动刷新）：  
```bash  
TOKEN=$(python3 ~/.openclaw/workspace/skills/eve-esi/scripts/get_token.py --char main)  
```  

**列出已认证的角色**：  
```bash  
python3 ~/.openclaw/workspace/skills/eve-esi/scripts/get_token.py --list  
```  

有关OAuth2/PKCE的详细信息，请参阅 `references/authentication.md`。  

## 公共API端点（无需认证）  

```bash  
# 角色公开信息  
curl -s "https://esi.evetech.net/latest/characters/2114794365/" | python -m json.tool  

# 角色头像链接  
curl -s "https://esi.evetech.net/latest/characters/2114794365/portrait/"  

# 角色所属公司信息  
curl -s "https://esi.evetech.net/latest/characters/2114794365/corporationhistory/"  

# 批量查询角色所属联盟信息  
curl -s -X POST "https://esi.evetech.net/latest/characters/affiliation/" \
  -H "Content-Type: application/json" \
  -d '[2114794365, 95538921]'  
```  

## 角色信息（需认证）  

```bash  
TOKEN="<your_access_token>"  
CHAR_ID="<your_character_id>"  

# 角色在线状态  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/online/"  
```  

## 钱包信息  

```bash  
# 账户余额  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/wallet/"  

# 钱包交易记录（分页显示）  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/wallet/journal/?page=1"  

# 资产信息  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/wallet/transactions/"  
```  

## 资产相关操作  

```bash  
# 查看所有资产（分页显示）  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/assets/?page=1"  

# 解析资产位置信息  
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '[1234567890, 9876543210]' \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/assets/locations/"  

# 解析资产名称  
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '[1234567890]' \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/assets/names/"  
```  

## 技能信息  

```bash  
# 查看所有已学习的技能及总技能点数  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/skills/"  

# 技能队列  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/skillqueue/"  

# 角色属性（智力、记忆等）  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/attributes/"  
```  

## 位置与飞船信息  

```bash  
# 当前位置  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/location/"  

# 当前飞船信息  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/ship/"  
```  

## 克隆与植入物信息  

```bash  
# 克隆信息及母星位置  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/clones/"  

# 活动中的植入物信息  
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://esi.evetech.net/latest/characters/$CHAR_ID/implants/"  
```  

## 其他API端点  

有关合同、装备、邮件、工业任务、击杀通知、市场订单、采矿、星球交互、忠诚度点数、蓝图、排名等角色相关功能的详细信息，请参阅 [references/endpoints.md](references/endpoints.md)。  

## 仪表盘配置  

该技能支持模块化的仪表盘配置，用于设置警报、报告和市场监控功能。用户可通过JSON配置文件自定义所需显示的内容：  
- **配置架构**：`config/schema.json`（包含所有字段、类型及默认值）  
- **示例配置**：`config/example-config.json`（可直接使用的模板）  

### 功能说明  

| 模块          | 功能描述                                      |  
|-----------------|-----------------------------------------|  
| **警报**        | 实时监控战争决策、结构攻击、技能完成情况、钱包变化等              |  
| **报告**        | 定时生成报告（资产净值、技能队列、工业任务、市场订单等）           |  
| **市场**        | 跟踪资产价格及价格趋势                            |  

### 安全注意事项  

令牌切勿以明文形式存储，建议使用环境变量进行引用：  
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
```  
示例配置文件：`python scripts/validate_config.py --example`  
JSON架构文件示例：`python scripts/validate_config.py --schema`  

## 使用查询脚本  

```bash  
SKILL=~/.openclaw/workspace/skills/eve-esi  
TOKEN=$(python3 $SKILL/scripts/get_token.py --char main)  
CHAR_ID=$(python3 $SKILL/scripts/get_token.py --char main --json | python3 -c "import sys,json; print(json.load(sys.stdin)) 2>/dev/null")  

# 简单查询  
python3 $SKILL/scripts/esi_query.py --token "$TOKEN" --endpoint "/characters/$CHAR_ID/wallet/" --pretty  

# 获取所有资产信息  
python3 $SKILL/scripts/esi_query.py --token "$TOKEN" --endpoint "/characters/$CHAR_ID/assets/" --pages --pretty  

# 发送POST请求（例如查询资产名称）  
python3 $SKILL/scripts/esi_query.py --token "$TOKEN" --endpoint "/characters/$CHAR_ID/assets/names/" \
  --method POST --body '[1234567890]' --pretty  
```  

## 最佳实践：  
- **缓存**：尊重响应中的 `Expires` 头部信息，避免在令牌过期前频繁请求。  
- **错误限制**：监控 `X-ESI-Error-Limit-Remain` 头部信息，遇到错误时适当延迟请求。  
- **User-Agent**：务必设置包含联系信息的描述性User-Agent。  
- **请求速率限制**：部分API（如邮件、合同相关请求）有速率限制，请求失败时可能返回HTTP 520错误。  
- **分页**：根据 `X-Pages` 头部信息进行分页查询。  
- **版本控制**：使用 `/latest/` 获取最新的稳定接口地址（`/dev/` 可能会随时更改）。  

## 类型ID解析  

ESI返回的类型ID为数字形式（例如飞船、物品、技能的ID）。可通过以下方式解析名称：  
```bash  
# 单个类型信息  
curl -s "https://esi.evetech.net/latest/universe/types/587/"  

# 批量查询名称（最多1000个ID）  
curl -s -X POST "https://esi.evetech.net/latest/universe/names/" \
  -H "Content-Type: application/json" \
  -d '[587, 638, 11393]'  
```