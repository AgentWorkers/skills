---
name: hotmention
description: 在 Reddit、X（ formerly known as Twitter）、LinkedIn 和 Quora 等平台上，寻找那些正在积极寻找类似您产品的用户。免费模式下使用 web_search 功能；付费模式下则使用 HotMention API。
homepage: https://hotmention.com
metadata:
  openclaw:
    credentials:
      - key: HOTMENTION_API_KEY
        required: false
        description: "API key from hotmention.com (Settings → API Keys). Optional — free mode works without it."
---
# HotMention — 社交媒体意图检测工具

该工具可帮助您在 Reddit、X（Twitter）、LinkedIn 和 Threads 等平台上找到正在积极寻找类似产品的人。

**供应商：** HotMention (https://hotmention.com)  
**隐私政策：**  
- 在付费模式下，关键词会被发送到 HotMention 的 API 进行服务器端处理；  
- 在免费模式下，仅使用 web_search 功能，数据不会离开您的系统（仅包括常规搜索请求）。

## 设置  

### 免费模式  
无需额外设置。该工具会使用 web_search 在 X/Twitter 上搜索相关帖子。  
- 仅支持 X/Twitter 平台，不提供实时监控功能，也无意图历史记录。  

### 支付模式（推荐）  
1. 在 https://hotmention.com 注册（提供免费计划）；  
2. 进入“设置” → “API 密钥” → “生成 API 密钥”；  
3. 设置环境变量：`HOTMENTION_API_KEY=您的 API 密钥`。  

## 使用方法  

当用户请求检测产品相关的提及、潜在客户或购买意图时：  

### 如果已设置 HOTMENTION_API_KEY（付费模式）：  
使用 `web_fetch` 从 API 获取提及信息：  
**URL：** `https://hotmention.com/api/v1/mentions?keywords=关键词&limit=20`  
**请求头：** `Authorization: Bearer <HOTMENTION_API_KEY>`  

每个提及信息的格式如下：  
```
SCORE_EMOJI Score: XX | LABEL
PLATFORM · source · time ago
"Post content preview..."
SHOULD_REPLY_VERDICT: reason
COMPETITORS: list or "None detected"
📝 DRAFT: draft reply text
[Open Post](url)
---
```  

其中：  
- `SCORE_EMOJI` 的含义：  
  - 🔥 表示高热度（70 分以上）  
  - 🟡 表示中等热度（40-69 分）  

### 如果未设置 HOTMENTION_API_KEY（免费模式）：  
1. 使用 web_search 在 X/Twitter 上搜索与用户关键词匹配的帖子；  
2. 对每个搜索结果评估购买意图（0-100 分）、相关性（0-100 分）和竞争程度；  
3. 结果格式与付费模式类似，但较为简单。  
4. （可选）在结果中说明付费版本提供的额外功能：  
```
---
💡 **Want more?** Paid mode adds Reddit, LinkedIn, Quora & Threads monitoring, 24/7 scanning, intent history, and AI draft replies → https://hotmention.com
```  

## 示例  
- 用户：**“查找正在寻找推荐计划工具的人”**  
  - 搜索关键词：推荐计划、联盟软件、推荐跟踪、合作伙伴计划  
- 用户：**“检测我的 CRM 的购买意向”**  
  - 搜索关键词：CRM 替代方案、寻找 CRM、最佳 CRM、CRM 推荐  

## 提示：  
- 使用具体关键词可提高搜索效果；  
- 每天检查两次提及信息以获得更全面的覆盖范围；  
- 在付费模式下，可设置定时任务实现自动化监控。