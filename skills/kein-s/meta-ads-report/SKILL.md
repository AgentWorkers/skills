# Meta Ads Analytics & Event Finder

这是一个强大的工具包，可让您通过聊天直接监控 Meta（Facebook/Instagram）广告的投放效果。该工具包包含分析报告功能以及事件发现工具，以确保数据追踪的准确性。

## 🚀 主要功能

1. **广告效果报告：**
    - 计算广告支出（Spend）、转化率（Conversions）以及每次获取成本（CAC，Cost Per Acquisition）。
    - 按广告组（Ad Set）对数据进行分类。
    - 支持自然语言日期范围（例如：“昨天”、“上个月”、“过去7天”）。

2. **事件发现工具：**
    - 列出您广告账户中所有当前激活的原始事件名称（例如：`offsite_conversion.custom...`）。
    - 帮助您找到用于配置转化追踪的具体事件名称。

---

## ⚙️ 配置（.env 文件）

要使用此功能，您必须在 OpenClaw 的设置中设置以下环境变量：

| 变量            | 描述                                      | 是否必填 | 默认值         |
|-----------------|-----------------------------------------|---------|--------------|
| `META_ACCESS_TOKEN`    | 来自 Meta 开发者的用户访问令牌                   | 是        |              |
| `META_AD_ACCOUNT_ID`    | 广告账户 ID（必须以 `act_` 开头）                   | 是        |              |
| `META_EVENT_NAME`     | 要追踪的具体转化事件名称                         | 否        | `offsite_conversion.fb_pixel_custom` |

---

## 🔑 获取凭证

### 1. 获取访问令牌
1. 访问 [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)。
2. 选择您的应用程序。
3. 添加权限：`ads_read`、`read_insights`。
4. 点击 **生成访问令牌** 并复制生成的字符串。

### 2. 获取广告账户 ID
1. 访问 [Facebook Ads Manager](https://adsmanager.facebook.com/)。
2. 查看 URL 中的 `act=12345678` 部分。
3. 您的广告账户 ID 为 `act_12345678`（请不要忘记 `act_` 前缀）。

---

## 💬 示例命令

### 检查分析数据
> “显示昨天的广告效果”
> “计算过去7天的每次获取成本（CAC）”
> “2026-02-01 至 2026-02-10 期间的广告支出情况如何？”
> “报告本月的广告支出”

### 查找正确的事件名称
> “列出所有广告事件”
> “显示可用的 Meta 事件名称”

---

## ⚠️ 故障排除

**问题：**我的转化次数为 0，但我有销售记录。
**解答：** 默认的转化事件名称是 `offsite_conversion.fb_pixel_custom`。您的广告像素可能使用了其他名称，如 `purchase`、`lead` 或 `start_trial`。
1. 向机器人询问：**“列出所有广告事件”**。
2. 从列表中复制正确的原始事件名称。
3. 使用该名称更新您的 `META_EVENT_NAME` 变量。