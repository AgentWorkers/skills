---
name: linkedin-scraper
description: 使用用户的 Chrome 配置文件来抓取 LinkedIn 用户资料。适用于需要寻找潜在客户、从 LinkedIn 获取用户资料或构建潜在客户列表的场景。触发指令包括：“在 LinkedIn 上查找创始人”、“抓取该 LinkedIn 用户的资料”、“获取这些用户的 LinkedIn 数据”以及“从 LinkedIn 构建潜在客户列表”。
metadata: { "openclaw": { "emoji": "🔍" } }
---
# LinkedIn 数据抓取工具 — 使用 Chrome 浏览器抓取个人资料和搜索结果

本工具利用用户已登录的 Chrome 浏览器会话来抓取 LinkedIn 的个人资料和搜索结果。无需使用 API 密钥，而是通过 Chrome 的浏览器扩展程序或 OpenClaw 功能来实现数据抓取。

## 前提条件

- 安装了 Chrome 浏览器，并已登录 LinkedIn。
- 确保已启用浏览器扩展程序或 OpenClaw 功能，以实现数据中继。
- 需要一个 DuckDB 工作空间来存储抓取到的数据（可选）。

## 核心工作流程

### 1. 单个个人资料抓取
```
browser → open LinkedIn profile URL
browser → snapshot (extract structured data)
→ Parse: name, headline, title, company, location, education, experience, connections, about
→ Return structured JSON or insert into DuckDB
```

### 2. 搜索 + 批量抓取
```
browser → open LinkedIn search URL with filters
browser → snapshot (extract result cards)
→ Parse each result: name, title, company, profile URL
→ For each profile URL: open → snapshot → parse full profile
→ Batch insert into DuckDB
```

### 3. 公司页面抓取
```
browser → open LinkedIn company page
→ Parse: company name, industry, size, description, specialties, employee count
→ Navigate to /people tab for employee list
```

## 实现规则

### 速率限制（至关重要）
- 页面加载之间至少需要等待 3-5 秒。
- 每个会话最多只能抓取 80 个个人资料（LinkedIn 的速率限制）。
- 随机设置加载延迟时间（3-8 秒），以避免被检测到。
- 每抓取 20 个个人资料后，需休息 60 秒。
- 如果检测到验证码或“异常活动”，立即停止并提醒用户。

### 隐秘抓取技巧
- 采用自然滚动的方式浏览页面（缓慢向下滚动，暂停后再继续）。
- 同一个搜索结果页面不要被抓取超过两次。
- 随机调整访问个人资料的顺序，避免按固定顺序访问。
- 定期关闭并重新打开浏览器标签页。

### 数据提取 — 个人资料页面
从 LinkedIn 个人资料页面中提取以下信息：

| 字段 | 位置 | 备注 |
|-------|----------|-------|
| name   | 主标题（h1） | 全名 |
| headline | 名字下方 | 职位名称及所在公司 |
| location | 地理位置信息 | 城市、州/国家 |
| current_title | 经历部分 | 最近的工作职位 |
| current_company | 经历部分 | 所在公司名称 |
| education | 教育背景 | 学校名称、学位信息及毕业时间 |
| connections | 人脉数量 | 显示为“500+”或具体数字 |
| about | 关于自己 | 个人简介（可能需要点击“查看更多”） |
| experience | 经历部分 | 所有工作经历及时间信息 |
| profile_url | 浏览器地址栏显示的链接 | LinkedIn 的官方个人资料链接 |

### 数据提取 — 搜索结果页面
从 LinkedIn 搜索结果页面中提取以下信息：

| 字段 | 位置 |
|-------|----------|
| name   | 结果卡片标题 |
| headline | 名字下方的文字内容 |
| location | 卡片元数据中的地理位置信息 |
| profile_url | 名字下方的链接 |
| mutual_connections | 卡片底部显示的人脉关系信息 |

## 搜索 URL 样式
```
# People search
https://www.linkedin.com/search/results/people/?keywords={query}

# With filters
&geoUrn=%5B%22103644278%22%5D          # United States
&network=%5B%22F%22%2C%22S%22%5D        # 1st + 2nd connections
&currentCompany=%5B%22{company_id}%22%5D # Current company
&schoolFilter=%5B%22{school_id}%22%5D    # School filter

# YC founders (common query)
https://www.linkedin.com/search/results/people/?keywords=Y%20Combinator%20founder

# Company employees
https://www.linkedin.com/company/{slug}/people/
```

## 数据存储到 DuckDB
将抓取到的数据存储到 DuckDB 数据库中，使用 Ironclaw 工作空间：

```sql
-- Check if leads/contacts object exists
SELECT * FROM objects WHERE name = 'leads' OR name = 'contacts';

-- Insert via the EAV pattern or direct pivot view
INSERT INTO v_leads ("Name", "Title", "Company", "LinkedIn URL", "Location", "Source")
VALUES (?, ?, ?, ?, ?, 'LinkedIn Scrape');
```

如果数据库中不存在相应的数据记录，请先创建一个新的记录：
```sql
-- Use Ironclaw's object creation pattern from the dench skill
```

## 错误处理
- 如果出现“登录”页面提示，说明 LinkedIn 会话已过期，请用户重新登录 Chrome 浏览器。
- 如果遇到验证码或安全检查，立即停止操作，等待 30 分钟以上后再尝试。
- 如果搜索到的个人资料不存在，跳过该记录并将相关 URL 记录为无效数据。
- 如果遇到速率限制（429 错误），停止操作，等待 15 分钟后重新尝试，但需增加延迟时间。
- 如果抓取到的数据为空（页面仍在加载中），等待 3 秒后再尝试抓取。

## 输出格式
- 默认输出格式为 JSON。

### 进度报告
对于批量抓取任务，需要提供抓取进度报告：
```
Scraping: 15/50 profiles (30%) — Last: Jane Doe (Acme Corp)
Rate: ~4 profiles/min — ETA: 9 min remaining
```

## 安全注意事项
- 严禁抓取私人或受限制的个人资料。
- 遵守 LinkedIn 的 robots.txt 文件规定，尊重公共页面的使用规则。
- 仅将数据存储在本地（DuckDB）中，严禁泄露数据。
- 用户必须拥有合法的 LinkedIn 访问权限。
- 本工具仅用于辅助用户进行大规模的自动化浏览操作。