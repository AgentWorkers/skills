---
name: foxreach
description: 管理 FoxReach 的冷邮件营销功能——包括潜在客户信息、营销活动、邮件发送序列、模板、电子邮件账户、收件箱以及相关分析数据。当用户需要创建潜在客户信息、管理营销活动、查看分析数据、发送营销邮件或执行与 FoxReach API 相关的任何操作时，可使用此功能。
argument-hint: "[resource] [action] [options]"
allowed-tools: Bash(python *), Bash(cd *), Bash(FOXREACH_API_KEY=* python *), Read, Grep, Glob
---
# FoxReach API管理技能

您通过Python SDK和CLI来管理FoxReach的冷邮件推广平台。本技能涵盖了与潜在客户（leads）、营销活动（campaigns）、邮件发送序列（sequences）、模板（templates）、电子邮件账户（email accounts）、收件箱（inbox）以及分析数据（analytics）相关的所有API操作。

## 设置与身份验证

Python SDK位于`integrations/sdk-python/`目录下，CLI位于`integrations/cli/`目录下。两者都使用API密钥进行身份验证，密钥前缀为`otr_`。

**检查SDK是否可用：**
```bash
python -c "from foxreach import FoxReach; print('SDK ready')"
```

**如果未安装，请安装它：**
```bash
cd integrations/sdk-python && pip install -e .
```

**身份验证**——在调用API之前，务必从用户或环境中获取API密钥。切勿将密钥硬编码到代码中。可以使用环境变量进行配置：
```bash
FOXREACH_API_KEY=otr_... python script.py
```

或者通过CLI配置文件进行设置：
```bash
cd integrations/cli && PYTHONPATH=. python -m foxreach_cli.main config set-key --key otr_...
```

## 如何执行操作

使用SDK编写内联Python脚本。请始终遵循以下格式：

```python
import json
from foxreach import FoxReach

client = FoxReach(api_key="otr_USER_KEY_HERE")

# ... perform operation ...

client.close()
```

对于快速操作，可以使用一行代码来完成：
```bash
python -c "
from foxreach import FoxReach
client = FoxReach(api_key='otr_...')
result = client.leads.list(page_size=10)
for lead in result:
    print(f'{lead.id}  {lead.email}  {lead.status}')
print(f'Total: {result.meta.total}')
client.close()
"
```

---

## 资源参考

有关完整的API详细信息，请参阅[api-reference.md](api-reference.md)。
每个操作的使用示例，请参阅[examples.md](examples.md)。

---

## 快速参考 — 可用的操作

### 潜在客户（Leads）
| 操作 | 方法 | 备注 |
|--------|--------|-------|
| 列出 | `client.leads.list(page=1, page_size=50, search=..., status=..., tags=...)` | 分页显示，可过滤 |
| 获取 | `client.leads.get(lead_id)` | 返回单个潜在客户信息 |
| 创建 | `client.leads.create(LeadCreate(email=..., first_name=..., ...))` | 避免重复（按电子邮件地址唯一） |
| 更新 | `client.leads.update(lead_id, LeadUpdate.company=..., ...))` | 部分更新 |
| 删除 | `client.leads.delete(lead_id)` | 软删除（数据不会立即永久删除） |

### 营销活动（Campaigns）
| 操作 | 方法 | 备注 |
|--------|--------|-------|
| 列出 | `client.campaigns.list(status=...)` | 可按草稿/活跃/暂停/已完成状态过滤 |
| 获取 | `client.campaigns.get(campaign_id)` | 包含活动统计数据 |
| 创建 | `client.campaigns.create(CampaignCreate(name=..., ...))` | 创建新的营销活动（默认为草稿状态） |
| 更新 | `client.campaigns.update(campaign_id, CampaignUpdate(...))` | 活跃状态的活动无法编辑 |
| 删除 | `client.campaigns.delete(campaign_id)` | 必须处于草稿状态 |
| 启动 | `client.campaigns.start(campaign_id)` | 将活动状态切换为“活跃” |
| 暂停 | `client.campaigns.pause(campaign_id)` | 暂停邮件发送 |
| 添加潜在客户 | `client.campaigns.add_leads(campaign_id, [lead_ids])` | 批量添加潜在客户 |
| 添加电子邮件账户 | `client.campaigns.add_accounts(campaign_id, [account_ids])` | 为营销活动分配发送者 |

### 邮件发送序列（Sequences，属于Campaigns的子模块）
| 操作 | 方法 | 备注 |
|--------|--------|-------|
| 列出 | `client.campaigns.sequences.list(campaign_id)` | 查看所有步骤 |
| 创建 | `client.campaigns.sequences.create(campaign_id, SequenceCreate(body=..., ...))` | 添加新的邮件发送步骤 |
| 更新 | `client.campaigns.sequences.update(campaign_id, seq_id, SequenceUpdate(...))` | 修改现有步骤 |
| 删除 | `client.campaigns.sequences.delete(campaign_id, seq_id)` | 删除步骤 |

### 模板（Templates）
| 操作 | 方法 | 备注 |
|--------|--------|-------|
| 列出 | `clienttemplates.list()` | 分页显示 |
| 获取 | `clienttemplates.get(template_id)` | 获取单个模板 |
| 创建 | `clienttemplates.create(TemplateCreate(name=..., body=...))` | 创建新模板 |
| 更新 | `clienttemplates.update(template_id, TemplateUpdate(...))` | 部分更新 |
| 删除 | `clienttemplates.delete(template_id)` | 删除模板 |

### 电子邮件账户（Email Accounts）
| 操作 | 方法 | 备注 |
|--------|--------|-------|
| 列出 | `client.email_accounts.list()` | 分页显示 |
| 获取 | `client.email_accounts.get(account_id)` | 包含账户状态信息 |
| 删除 | `client.email_accounts.delete(account_id)` | 删除账户 |

### 收件箱（Inbox）
| 操作 | 方法 | 备注 |
| 列出邮件线程 | `client.inbox.list_threads(category=..., is_read=..., ...)` | 可过滤 |
| 获取 | `client.inbox.get(reply_id)` | 获取完整的邮件回复信息 |
| 更新 | `client.inbox.update(reply_id, ThreadUpdate(is_read=..., ...))` | 标记邮件为已读或星标 |

### 分析数据（Analytics）
| 操作 | 方法 | 备注 |
|--------|--------|-------|
| 总览 | `client-analytics.overview()` | 查看仪表板关键绩效指标 |
| 营销活动分析 | `client-analytics.campaign(campaign_id)` | 查看活动详细统计数据 |

---

## 分页

列表端点返回`PaginatedResponse`对象：

```python
result = client.leads.list(page=1, page_size=50, search="acme")

# Access data
for lead in result:
    print(lead.email)

# Check pagination info
print(f"Page {result.meta.page}/{result.meta.total_pages}, {result.meta.total} total")

# Get next page
if result.has_next_page():
    next_result = result.next_page()

# Auto-paginate through ALL results
for lead in client.leads.list().auto_paging_iter():
    print(lead.email)
```

---

## 错误处理

请始终使用`try/except`语句来处理API调用中的错误：

```python
from foxreach import FoxReach, NotFoundError, RateLimitError, AuthenticationError, FoxReachError

try:
    lead = client.leads.get("cld_nonexistent")
except NotFoundError:
    print("Lead not found")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except FoxReachError as e:
    print(f"API error: {e}")
```

---

## 模板变量与个性化

电子邮件正文支持使用`{{variable}}`语法进行变量替换：
- `{{firstName}}`, `{{lastName}}`, `{{email}}`
- `{{company}}`, `{{title}}`, `{{phone}}`
- `{{website}}`, `{{linkedinUrl}}`
- 自定义字段：`{{customFieldName}}`

也支持Spintax格式：`{Hi|Hey|Hello} {{firstName}}`

---

## 常见工作流程

### 1. 完整的营销活动设置
当用户需要设置一个完整的营销活动时，请按照以下步骤操作：
1. 使用`campaigns.create()`创建营销活动。
2. 使用`campaigns.sequences.create()`为每个邮件步骤创建相应的序列。
3. 使用`campaigns.add_leads()`添加潜在客户。
4. 使用`campaigns.add_accounts()`为营销活动分配电子邮件账户。
5. 使用`campaigns.start()`启动营销活动。

### 2. 检查营销活动效果
1. 使用`analytics.campaign(id)`获取活动分析数据。
2. 查看已发送、已送达、被退回、已回复的邮件数量以及打开率。
3. 查看回复率和退回率。
4. 如果有每日统计数据，可以汇总趋势。

### 3. 管理收件箱
1. 使用`inbox.list_threads(is_read=False)`列出未读邮件。
2. 通过`inbox.update(id, ThreadUpdate(category="interested"))`对回复邮件进行分类。
3. 常见分类：感兴趣、不感兴趣、不在办公时间、发送给错误的人、已取消订阅。

### 4. 批量导入潜在客户
如果要批量导入潜在客户，请逐一创建它们（API会按电子邮件地址进行去重）：
```python
leads_data = [
    {"email": "a@example.com", "first_name": "Alice", "company": "Acme"},
    {"email": "b@example.com", "first_name": "Bob", "company": "Beta"},
]
created = []
for data in leads_data:
    lead = client.leads.create(LeadCreate(**data))
    created.append(lead)
    print(f"Created: {lead.id} - {lead.email}")
```

---

## 重要说明

- **基础URL**：`https://api.foxreach.io/api/v1`
- **请求速率限制**：每分钟100次请求。SDK会在遇到429错误时自动重试。
- **ID前缀**：潜在客户`cld_`、营销活动`cmp_`、回复邮件`rpl_`、模板`tpl_`
- **时区**：所有日期时间均采用UTC ISO 8601格式。
- **发送时间**：使用整数数组表示，1表示周一，7表示周日。
- **发送时间范围**：0-23表示24小时内的时间。
- **营销活动状态**：草稿 → 活跃 → 暂停 → 完成
- **软删除**：潜在客户被软删除后可以在重新导入时重新出现。
- 在执行删除或启动营销活动等破坏性操作前，请务必确认用户同意。
- 在列出数据时，系统会显示格式化的摘要，而不是原始的JSON格式。
- 在创建资源时，请在执行前与用户确认相关细节。