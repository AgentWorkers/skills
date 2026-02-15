# SKILL.md - 数据增强工具（Data Enricher）

## 功能简介
该工具用于为潜在客户（leads）添加电子邮件地址，并将数据格式化以便在 Notion 中使用。

## 使用的模型
- **ollama/llama3.2:8b**（免费）：用于数据格式化
- **haiku**：用于调用 Hunter.io 的 API

## 速率限制
- 每个会话最多允许进行 10 次 Hunter.io 的查询（API 限制）
- 每次 API 调用之间需等待 5 秒
- 相似的域名应被归为一组进行处理

## 电子邮件获取方法（按顺序）
### 1. 网站联系页面
- 查看 /contact、/about、/pages/contact 等页面
- 寻找包含 “mailto:” 链接的元素
- 检查页面底部的联系方式

### 2. Instagram 个人简介
- 查看个人简介中的电子邮件地址
- 查看 “联系我们”（Contact）按钮

### 3. Hunter.io API
```
GET https://api.hunter.io/v2/domain-search
?domain={domain}
&api_key={HUNTER_API_KEY}
```

API 返回的结果包括：
- 用户的电子邮件地址（emails）
- 识别准确率（confidence score）
- 电子邮件类型（generic 或 personal）

**仅使用识别准确率高于 70% 的电子邮件地址**

### 4. 电子邮件地址模式识别
常见的电子邮件地址模式：
- hello@domain.com
- info@domain.com
- contact@domain.com
- [firstname]@domain.com

## 电子邮件优先级
1. 创始人/所有者的个人电子邮件地址（最佳选择）
2. hello@ 或 hi@ 类型的电子邮件地址（次优选择）
3. info@ 或 contact@ 类型的电子邮件地址（可接受）
4. 通用格式的 support@ 类型电子邮件地址（最后选择）

## 输出格式
```
{
  "domain_key": "brandname.com",
  "brand_name": "Brand Name",
  "niche": "skincare",
  "website_url": "https://brandname.com",
  "ig_handle": "@brandname",
  "followers_est": 15000,
  "contact_email": "hello@brandname.com",
  "email_confidence": "high",
  "email_source": "hunter.io",
  "source": "meta_ads",
  "status": "new"
}
```

## 去重处理
在添加任何潜在客户信息之前，需执行以下操作：
1. 将域名转换为小写格式，删除 “www.” 前缀以及 “https://” 协议
2. 检查该域名是否已存在于 Notion 数据库中
3. 如果存在，则跳过该域名，避免重复添加
4. 记录日志：`Skipped [domain] - 已存在于处理流程中`

## 批量处理
- 每次处理 10 个潜在客户信息
- 在数据同步到 Notion 之前完成所有数据的格式化工作
- 将格式化后的数据保存到 `workspace/leads-enriched-YYYY-MM-DD.json` 文件中