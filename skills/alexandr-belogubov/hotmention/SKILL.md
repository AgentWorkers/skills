---
name: hotmention
description: 在 Reddit、X（原 Twitter）、LinkedIn 和 Quora 等平台上，寻找那些正在积极寻找类似您产品的用户。免费模式下使用 web_search 功能；付费模式下则使用 HotMention API。
homepage: https://hotmention.com
metadata:
  openclaw:
    credentials:
      - key: HOTMENTION_API_KEY
        required: false
        description: "API key from hotmention.com (Settings → API Keys). Optional — free mode works without it."
---
# HotMention — 社交媒体意图检测工具

该工具可帮助您在 Reddit、X（Twitter）、LinkedIn 和 Quora 等平台上找到正在积极寻找与您产品相关的人。

**供应商：** HotMention (https://hotmention.com)  
**隐私政策：**  
- 在付费模式下，关键词会被发送至 HotMention 的 API 进行评分分析；  
- 在免费模式下，仅使用 web_search 功能，不会将任何数据从您的系统中传出（仅包含常规搜索请求）。

## 设置  

### 免费模式  
无需额外设置。该工具会使用 web_search 在 X/Twitter 上搜索相关帖子。  
- 仅支持 X/Twitter 平台，不提供实时监控功能，也无法查看用户的搜索历史记录。  

### 支付模式（推荐）  
1. 在 https://hotmention.com 注册（提供免费计划）；  
2. 进入“设置” → “API 密钥” → “生成 API 密钥”；  
3. 将生成的 API 密钥添加到您的系统中，并将其命名为 `HOTMENTION_API_KEY`。  

## 使用方法  

当用户请求检测与他们产品相关的提及、潜在客户或购买意图时：  

### 如果已设置 HOTMENTION_API_KEY（付费模式）：  
使用 HotMention 的 REST API 获取评分结果。完整 API 文档请参见：https://hotmention.com/docs/api  
每个提及结果的格式如下：  
```
SCORE_EMOJI Score: XX | LABEL
PLATFORM · source · time ago
"Post content preview..."
SHOULD_REPLY_VERDICT: reason
COMPETITORS: list or "None detected"
📝 DRAFT: draft reply text
Link to original post
---
```  
其中：  
- `SCORE_EMOJI`：🔥 表示“高度相关”（评分 70 分以上）；  
- 🟡 表示“较为相关”（评分 40–69 分）。  

### 如果未设置 HOTMENTION_API_KEY（免费模式）：  
1. 使用 web_search 在 X/Twitter 上搜索用户输入的关键词；  
2. 对每个搜索结果评估其购买意图（0–100 分）、相关性（0–100 分）以及竞争程度；  
3. 结果格式与付费模式类似，但更为简单。  
4. （可选）在结果中说明付费版本提供的额外功能：  
```
---
💡 Want more? Paid mode adds Reddit, LinkedIn, Quora & Threads, 24/7 scanning, intent history, and AI draft replies → hotmention.com
```  

## 示例：  
用户：“查找正在寻找推荐计划工具的人”  
→ 搜索关键词：推荐计划、联盟软件、推荐跟踪、合作伙伴计划  

用户：“检测我的 CRM 产品的购买意图”  
→ 搜索关键词：CRM 替代品、寻找 CRM、最佳 CRM、CRM 推荐  

## 使用建议：  
- 使用具体的关键词以获得更准确的结果；  
- 每天检查两次搜索结果以获得最佳覆盖范围；  
- 在付费模式下，可设置定时任务以实现自动监控。