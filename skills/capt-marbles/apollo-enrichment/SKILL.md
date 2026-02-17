---
name: apollo
description: Apollo.io 的联系人和公司信息扩展 API：该 API 可用于获取联系人的电子邮件、电话号码、职位以及公司的相关信息（如行业、收入、员工人数和融资情况），同时也能获取公司的详细信息。适用于用户需要补充联系人信息、查找电子邮件地址、查询公司资料或搜索潜在客户时的场景。
version: 1.3.0
author: captmarbles
---

# Apollo 数据增强技能

使用 [Apollo.io](https://apollo.io) 的 API 来增强联系人（contacts）和公司（companies）的信息。

## 设置

1. 从 [Apollo 设置](https://app.apollo.io/#/settings/integrations/api) 获取您的 API 密钥。
2. 设置环境变量：
   ```bash
   export APOLLO_API_KEY=your-api-key-here
   ```

## 使用方法

该技能中的所有命令都依赖于该技能目录下自带的 `apollo.py` 脚本。

### 增强个人信息

获取联系人的电子邮件、电话、职位和公司信息。

```bash
# By email
python3 apollo.py enrich --email "john@acme.com"

# By name + company
python3 apollo.py enrich --name "John Smith" --domain "acme.com"

# Include personal email & phone
python3 apollo.py enrich --email "john@acme.com" --reveal-email --reveal-phone
```

### 批量增强个人信息

一次操作可以增强最多 10 个人的资料。

```bash
# From JSON file with array of {email, first_name, last_name, domain}
python3 apollo.py bulk-enrich --file contacts.json

# Reveal personal contact info
python3 apollo.py bulk-enrich --file contacts.json --reveal-email --reveal-phone
```

**contacts.json 示例：**
```json
[
  {"email": "john@acme.com"},
  {"first_name": "Jane", "last_name": "Doe", "domain": "techcorp.io"}
]
```

### 增强公司信息

获取公司的行业、收入、员工人数和融资信息。

```bash
python3 apollo.py company --domain "stripe.com"
```

### 搜索联系人

根据指定条件查找潜在客户。

```bash
# By title and company
python3 apollo.py search --titles "CEO,CTO" --domain "acme.com"

# By title and location
python3 apollo.py search --titles "VP Sales" --locations "San Francisco"

# Limit results
python3 apollo.py search --titles "Engineer" --domain "google.com" --limit 10

# Exclude competitors (Hathora/Edgegap/Nakama)
python3 apollo.py search --titles "CTO" --exclude-competitors
```

**过滤选项：**
- `--exclude-competitors` 或 `-x` — 自动过滤掉来自 Hathora、Edgegap 和 Nakama (Heroic Labs) 公司的员工。

## 示例命令：

- *"使用 Apollo 增强 john@acme.com 的信息"*
- *"获取 stripe.com 的公司信息"*
- *"查找纽约市金融科技公司的首席技术官（CTO）"
- *"批量增强这些联系人的信息"*
- *"Notion 公司的员工人数和收入是多少？"*

## 返回的数据

**个人信息：**
- 姓名、职位、头衔
- 电子邮件（工作邮箱和个人邮箱）
- 电话（固定电话和手机号）
- 公司名称、所属行业
- LinkedIn 链接
- 所在地

**公司信息：**
- 公司名称、域名、公司标志
- 所属行业、关键词
- 员工人数、年收入
- 融资轮次、投资方
- 使用的技术
- 社交媒体链接

## 许可证（Credits）

使用 Apollo 服务需要支付许可证费用。您可以在 [apollo.io/settings/credits](https://app.apollo.io/#/settings/credits) 查看您的使用情况。