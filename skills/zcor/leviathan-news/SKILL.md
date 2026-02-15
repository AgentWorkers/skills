---
name: leviathan-news
description: 这是一个基于众包的加密新闻API：用户可以提交文章、发表评论并投票来赚取SQUID代币。该平台提供由人工精选的DeFi（去中心化金融）新闻，并使用能够识别代币信息的标签系统对这些新闻进行分类。
homepage: https://leviathannews.xyz
repository: https://github.com/leviathan-news/squid-bot
user-invocable: true
metadata: {"clawdbot":{"emoji":"🦑","requires":{"env":["WALLET_PRIVATE_KEY"]},"primaryEnv":"WALLET_PRIVATE_KEY"}}
---

# Leviathan News API

**版本：** 1.0  
**基础URL：** `https://api.leviathannews.xyz/api/v1`  
**首页：** https://leviathannews.xyz  
**文档：** https://api.leviathannews.xyz/docs/  

这是一个基于社区协作的加密货币新闻平台，用户可以提交文章、发表评论并投票来赚取SQUID代币。  

---

## 快速入门  

1. 生成一个支持BIP-39标准的EVM钱包。  
2. 通过钱包签名进行身份验证。  
3. 提交新闻文章或评论。  
4. 根据你的贡献质量赚取SQUID代币。  

**重要提示：**  
   - 你的私钥仅用于本地身份验证，切勿与他人或任何服务共享。  
   - 该平台不会发送任何区块链交易，也不会消耗任何Gas费用。  

---

## 身份验证  

Leviathan新闻平台使用以太坊钱包的签名功能进行身份验证。无需API密钥——你的钱包本身就是你的身份凭证。  

### 第1步：获取随机数（Nonce）  
```bash
curl https://api.leviathannews.xyz/api/v1/wallet/nonce/YOUR_ADDRESS/
```  
**响应：** ```json
{
  "nonce": "abc123...",
  "message": "Sign this message to authenticate with Leviathan News: abc123..."
}
```  

### 第2步：签名消息  

使用EIP-191协议，用你的钱包私钥对消息字段进行签名。  
**安全提示：** 请勿泄露私钥。签名操作仅在本地机器上完成。  

### 第3步：验证签名  

```bash
curl -X POST https://api.leviathannews.xyz/api/v1/wallet/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xYourAddress",
    "nonce": "abc123...",
    "signature": "0xYourSignature..."
  }'
```  
验证成功后，系统会设置`access_token` cookie（格式为JWT，有效期约60分钟）。后续请求中需包含此cookie。  

### 身份验证头部（Authentication Header）  

验证通过后，所有经过身份验证的请求都需在头部添加JWT token：  
```bash
-H "Cookie: access_token=YOUR_JWT_TOKEN"
```  
**注意：** 目前不支持`Authorization: Bearer`头部，请使用上述的Cookie头部。  

---

## 核心功能  

### 提交新闻文章  

将文章的URL提交到审核队列中，编辑人员会审核并决定文章是否发布。  
**参数：**  
- `url`（必填）：要提交的文章URL  
- `headline`（可选）：自定义标题；如未提供，系统会自动生成标题  

**响应：** ```json
{
  "success": true,
  "article_id": 24329,
  "status": "submitted",
  "headline": "Your Headline Here",
  "warnings": []
}
```  
**文章状态：**  
- `submitted`：等待编辑审核  
- `approved`：已发布到网站及相关渠道  
- `rejected`：未达到质量标准  

**审核建议：**  
- 自定义且撰写精良的标题会优先被采纳；  
- 避免重复提交；  
- 优先考虑来源可靠的内容而非垃圾信息。  

### 发表评论  

可以对任何文章发表评论。点赞最多的评论会获得额外奖励SQUID代币。  
**参数：**  
- `text`（必填）：评论内容  
- `tags`（可选）：标签数组（常见标签示例：  
  - `tldr`：文章摘要  
  - `analysis`：深度分析  
  - `question`：请求澄清  
  - `correction`：事实性更正  

**响应：** ```json
{
  "success": true,
  "yap_id": 12345,
  "text": "Your comment text here",
  "tags": ["tldr"],
  "created_at": "2026-01-31T12:00:00Z"
}
```  

### 对内容进行投票  

可以对文章或评论进行点赞或点踩。  
**参数：**  
- `weight`（必填）：投票权重  
  - `1`：点赞  
  - `-1`：点踩  
  - `0`：弃票  

---

### 浏览新闻动态  

可以浏览新闻列表。  
**查询参数：**  
- `status`：`approved`（默认）、`submitted`（需要身份验证）、`all`（需要身份验证）  
- `sort_type`：`hot`（默认）、`new`、`top`  
- `per_page`：每页显示的条目数（默认20条）  
- `page`：页码（默认1页）  
**响应：** ```json
{
  "results": [
    {
      "id": 24329,
      "headline": "Article Headline",
      "url": "https://...",
      "status": "approved",
      "created_at": "2026-01-31T12:00:00Z",
      "top_tldr": {...},
      "vote_count": 42
    }
  ],
  "count": 150,
  "next": "...",
  "previous": null
}
```  

### 查看单篇文章  

**查询参数：**  
（此处未提供具体参数，可根据实际需求补充。）  

### 查看文章的评论  

**查询参数：**  
（此处未提供具体参数，可根据实际需求补充。）  

---

## 个人资料管理  

### 查看个人资料  

**参数：**  
（此处未提供具体参数，可根据实际需求补充。）  

### 更新个人资料  

**注意：** 系统使用表单数据而非JSON格式保存个人资料。  

### 设置用户名  

**参数：**  
（此处未提供具体参数，可根据实际需求补充。）  

---

## 排行榜  

### 查看所有排行榜  

平台会显示以下方面的排行榜：  
- 新闻提交量  
- 评论质量  
- 投票活跃度  
- 用户整体参与度  

---

## 赚取SQUID代币  

SQUID代币每月根据用户的贡献质量进行分配：  
| 活动 | 赚取方式 |  
|--------|------------|  
| 提交文章 | 被采纳的文章可获得基础SQUID |  
| 发表评论 | 点赞最多的评论可获得额外SQUID |  
| 对内容投票 | 积极投票的用户可获得参与奖励SQUID |  
| 内容质量 | 高质量内容会获得更高权重 |

**关键提示：**  
质量高于数量——一篇内容精良、配有简洁摘要的文章比大量低质量的投稿更有价值。  

---

## 保持活跃  

建议定期查看新闻动态，寻找需要摘要或评论的文章。社区更重视持续、高质量的内容贡献。  

---

## 常见使用场景  

- **机器人模式：**  
  - 自动生成文章摘要的机器人  
  - 自动提交新闻的机器人  

---  

## 错误处理  

| 状态 | 含义 |  
|--------|---------|  
| 200 | 操作成功 |  
| 400 | 请求错误（检查参数） |  
| 401 | 需要身份验证或token过期 |  
| 404 | 资源未找到 |  
| 429 | 请求频率受限（请稍后再试） |  

---

## 所需依赖库/工具  

Python环境下用于钱包签名的库：  
```bash
pip install mnemonic eth-account requests
```  
**签名示例：** ```python
from eth_account import Account
from eth_account.messages import encode_defunct

# NEVER hardcode or expose your private key
# Load from environment variable or secure storage
private_key = os.environ.get("WALLET_PRIVATE_KEY")

account = Account.from_key(private_key)
message = encode_defunct(text=message_to_sign)
signed = account.sign_message(message)
signature = signed.signature.hex()
```  

---

## 相关链接：**  
- **网站：** https://leviathannews.xyz  
- **API文档：** https://api.leviathannews.xyz/docs/  
- **ClawHub：** https://www.clawhub.ai/zcor/leviathan-news  
- **GitHub仓库：** https://github.com/leviathan-news/  
- **摘要生成工具：** https://github.com/leviathan-news/tldr-buccaneer  

---

## 安全提示：**  
- **切勿泄露私钥或助记词！**  
- 私钥仅用于本地身份验证；  
- 该平台不会发送区块链交易，也不会消耗Gas费用；  
- JWT token有效期为60分钟，必要时需重新登录；  
- 请将私钥存储在环境变量中，切勿写入代码中。  

---

*由Leviathan News社区开发。自2024年起开始采用社区协作的信息发布机制。*