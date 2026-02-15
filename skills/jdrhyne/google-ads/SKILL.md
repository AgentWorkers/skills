---
name: google-ads
description: "查询、审核和优化 Google Ads 广告活动。支持两种模式：  
(1) API 模式：通过 `google-ads` Python SDK 进行批量操作；  
(2) 浏览器自动化模式：适用于没有 API 访问权限的用户——只需打开 ads.google.com 的浏览器页面即可使用。  
适用于需要检查广告效果、暂停广告活动/关键词、查找浪费的广告费用、审核转化跟踪或优化 Google Ads 账户的场景。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires":
          {
            "anyBins": ["python3"],
            "config": ["~/.google-ads.yaml"],
          },
      },
  }
---

# Google Ads 技能

通过 API 或浏览器自动化工具来管理 Google Ads 账户。

## 模式选择

**选择使用哪种模式：**

1. **API 模式** - 如果用户已配置 `google-ads.yaml` 文件或设置了 `GOOGLE_ADS_*` 环境变量
2. **浏览器模式** - 如果用户表示“没有 API 访问权限”或仅需要进行快速检查

```bash
# Check for API config
ls ~/.google-ads.yaml 2>/dev/null || ls google-ads.yaml 2>/dev/null
```

如果未找到配置信息，询问用户：“您是否有 Google Ads API 凭据？还是应该使用浏览器自动化工具？”

---

## 浏览器自动化模式（通用）

**要求：** 用户已通过浏览器登录 ads.google.com

### 设置步骤
1. 用户打开 ads.google.com 并登录
2. 点击 Clawdbot 浏览器中继工具栏图标（徽章需处于开启状态）
3. 使用 `browser` 工具，并设置 `profile="chrome"` 参数

### 常见操作流程

#### 查看广告活动表现
```
1. Navigate to: ads.google.com/aw/campaigns
2. Set date range (top right date picker)
3. Snapshot the campaigns table
4. Parse: Campaign, Status, Budget, Cost, Conversions, Cost/Conv
```

#### 查找无转化效果的关键词（造成浪费的广告支出）
```
1. Navigate to: ads.google.com/aw/keywords
2. Click "Add filter" → Conversions → Less than → 1
3. Click "Add filter" → Cost → Greater than → [threshold, e.g., $500]
4. Sort by Cost descending
5. Snapshot table for analysis
```

#### 暂停某些关键词或广告活动的投放
```
1. Navigate to keywords or campaigns view
2. Check boxes for items to pause
3. Click "Edit" dropdown → "Pause"
4. Confirm action
```

#### 下载报告
```
1. Navigate to desired view (campaigns, keywords, etc.)
2. Click "Download" icon (top right of table)
3. Select format (CSV recommended)
4. File downloads to user's Downloads folder
```

**有关浏览器操作的详细信息，请参阅 `references/browser-workflows.md`**

---

## API 模式（高级用户）

**要求：** 拥有 Google Ads API 开发者令牌和 OAuth 凭据

### 设置检查
```bash
# Verify google-ads SDK
python -c "from google.ads.googleads.client import GoogleAdsClient; print('OK')"

# Check config
cat ~/.google-ads.yaml
```

### 常见操作

#### 查询广告活动表现
```python
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_storage()
ga_service = client.get_service("GoogleAdsService")

query = """
    SELECT campaign.name, campaign.status,
           metrics.cost_micros, metrics.conversions,
           metrics.cost_per_conversion
    FROM campaign
    WHERE segments.date DURING LAST_30_DAYS
    ORDER BY metrics.cost_micros DESC
"""

response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
```

#### 查找无转化效果的关键词
```python
query = """
    SELECT ad_group_criterion.keyword.text,
           campaign.name, metrics.cost_micros
    FROM keyword_view
    WHERE metrics.conversions = 0
      AND metrics.cost_micros > 500000000
      AND segments.date DURING LAST_90_DAYS
    ORDER BY metrics.cost_micros DESC
"""
```

#### 暂停某些关键词的投放
```python
operations = []
for keyword_id in keywords_to_pause:
    operation = client.get_type("AdGroupCriterionOperation")
    operation.update.resource_name = f"customers/{customer_id}/adGroupCriteria/{ad_group_id}~{keyword_id}"
    operation.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
    operations.append(operation)

service.mutate_ad_group_criteria(customer_id=customer_id, operations=operations)
```

**完整的 API 参考资料请参阅 `references/api-setup.md`

---

## 审计检查清单

对 Google Ads 账户进行快速健康检查：

| 检查项 | 浏览器路径 | 需要关注的内容 |
|-------|--------------|------------------|
| 无转化效果的关键词 | 关键词 → 筛选条件：Conv<1, Cost>$500 | 造成浪费的广告支出 |
| 空广告组 | 广告组 → 筛选条件：Ads=0 | 无广告创意正在运行 |
| 违反政策的情况 | 广告活动 → 状态栏 | 出现黄色警告图标 |
| 优化得分 | 总览页面（右上角） | 优化得分低于 70% 表示需要采取行动 |
| 转化跟踪 | 工具 → 转化数据 | 转化数据不活跃或无最新数据 |

---

## 输出格式

在报告结果时，请使用表格格式：

```markdown
## Campaign Performance (Last 30 Days)
| Campaign | Cost | Conv | CPA | Status |
|----------|------|------|-----|--------|
| Branded  | $5K  | 50   | $100| ✅ Good |
| SDK Web  | $10K | 2    | $5K | ❌ Pause |

## Recommended Actions
1. **PAUSE**: SDK Web campaign ($5K CPA)
2. **INCREASE**: Branded budget (strong performer)
```

---

## 故障排除

### 浏览器模式相关问题
- **无法查看数据**：确认用户访问的是正确的账户（右上角的账户选择器）
- **加载速度慢**：Google Ads 的用户界面较为复杂，请等待数据完全加载
- **会话过期**：用户需要重新登录 ads.google.com

### API 模式相关问题
- **身份验证失败**：刷新 OAuth 令牌，并检查 `google-ads.yaml` 文件的配置
- **开发者令牌被拒绝**：确保令牌已获得批准（非测试模式）
- **客户 ID 错误**：使用不含破折号的 10 位数字客户 ID