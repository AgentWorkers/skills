---
name: crm
description: 这是一个用于管理联系人、关系及跟进工作的个人CRM系统，支持使用Markdown文件进行操作。当用户需要添加联系人、跟踪关系、设置跟进提醒、按标签/公司/位置查询联系人、导入/导出联系人或管理潜在客户时，可以使用该系统。该系统还支持通过自然语言输入来添加联系人。
---

# 个人CRM技能

使用Markdown文件来管理联系人、关系以及后续跟进工作，无需数据库。

## 设置

在内存中初始化联系人数据，以便进行语义搜索：
```bash
mkdir -p memory/contacts/{people,companies,events,_templates,scripts}
cp skills/crm/assets/templates/*.md memory/contacts/_templates/
cp skills/crm/scripts/*.py memory/contacts/scripts/
clawdbot memory index
```

## 自然语言输入

当用户以自然的方式描述一个联系人时，系统会提取相关信息并创建相应的联系人记录：

**用户输入：**“我在Web3峰会上遇到了Sarah Lee。她是位于迪拜的Polygon公司的合作伙伴关系负责人。她的Telegram账号是@sarahlee。”

**提取的信息：**
```yaml
name: Sarah Lee
company: Polygon
role: Head of Partnerships
location: Dubai
telegram: "@sarahlee"
met_at: web3-summit
tags: [web3, partnership]
```

**然后执行以下命令：**`memory/contacts/memory/contacts/scripts/crm-add.py person "Sarah Lee" --company "Polygon" --role "Head of Partnerships" --location "Dubai" --telegram "@sarahlee" --tags "web3,partnership"`

## 脚本

所有脚本均使用`/usr/bin/python3`执行，并需要PyYAML库。

### 查询联系人
```bash
memory/contacts/scripts/crm-query.py --list people          # List all people
memory/contacts/scripts/crm-query.py --tag investor         # Filter by tag
memory/contacts/scripts/crm-query.py --company "Acme"       # Filter by company
memory/contacts/scripts/crm-query.py --introduced-by bob    # Find introductions
memory/contacts/scripts/crm-query.py --location singapore   # Filter by location
memory/contacts/scripts/crm-query.py --search "supply chain" # Full-text search
memory/contacts/scripts/crm-query.py -v                     # Verbose output
```

### 添加联系人
```bash
memory/contacts/scripts/crm-add.py person "Name" --company "Co" --role "Title" --tags "a,b"
memory/contacts/scripts/crm-add.py company "Company Name" --industry "Tech"
memory/contacts/scripts/crm-add.py event "Event Name" --date 2026-03-15 --location "City"
```

### 更新联系人信息
```bash
memory/contacts/scripts/crm-update.py alice-chen --interaction "Called about demo"
memory/contacts/scripts/crm-update.py alice-chen --set-follow-up 2026-02-15
memory/contacts/scripts/crm-update.py alice-chen --add-tag vip
memory/contacts/scripts/crm-update.py alice-chen --touch  # Update last_contact to today
```

### 后续跟进与提醒
```bash
memory/contacts/scripts/crm-followups.py --summary         # Quick summary
memory/contacts/scripts/crm-followups.py --days 7          # Due in 7 days
memory/contacts/scripts/crm-followups.py --dormant 90      # Not contacted in 90 days
memory/contacts/scripts/crm-remind.py contact --in 3d      # Remind in 3 days
memory/contacts/scripts/crm-remind.py --list               # List reminders
memory/contacts/scripts/crm-remind.py --check              # Check due reminders
```

### 导入/导出联系人数据
```bash
memory/contacts/scripts/crm-import.py contacts.csv                    # Import CSV
memory/contacts/scripts/crm-import.py contacts.vcf                    # Import vCard
memory/contacts/scripts/crm-import.py linkedin.csv --format linkedin  # LinkedIn export
memory/contacts/scripts/crm-export.py --csv out.csv                   # Export CSV
memory/contacts/scripts/crm-export.py --vcard out.vcf --type people   # Export vCard
```

### 重新生成索引
```bash
memory/contacts/scripts/crm-index.py  # Rebuilds contacts/_index.md
```

## 联人信息结构
```yaml
---
name: Alice Chen
type: person  # person | company | event
tags: [investor, crypto]
company: Acme Corp
role: Partner
email: alice@acme.com
phone: +1-555-0123
telegram: "@alice"
twitter: "@alice"
linkedin: https://linkedin.com/in/alice
location: Singapore
introduced_by: bob-smith  # slug of introducer
met_at: token2049-2025    # slug of event
first_contact: 2025-09-20
last_contact: 2026-01-27
follow_up: 2026-02-15
status: active  # active | dormant | archived
---

# Alice Chen

## Context
Partner at Acme Corp. Met through Bob at Token2049.

## Interactions
- **2026-01-27**: Called about pilot program.
- **2025-09-20**: First met at conference.

## Notes
- Prefers Signal over email
```

## 文件夹结构
```
memory/
└── contacts/             # Inside memory/ for semantic search
    ├── people/           # One file per person
    ├── companies/        # One file per company
    ├── events/           # One file per event
    ├── _templates/       # Templates for new contacts
    ├── _index.md         # Auto-generated lookup table
    ├── .reminders.json   # Reminder data
    └── scripts/          # CLI tools
```

## 相关参考

- **YAML字段：**`introduced_by: bob-smith`, `met_at: event-slug`
- **笔记中的Wiki链接：**`[[bob-smith]]`, `[[acme-corp]]`
- **语义搜索：**系统能够从文本中自动提取并关联联系人信息

## 与HEARTBEAT系统的集成
将相关代码添加到HEARTBEAT.md文件中：
```markdown
### CRM Follow-ups (check 1-2x daily)
1. Run: `/usr/bin/python3 contacts/memory/contacts/scripts/crm-followups.py --summary`
2. Run: `/usr/bin/python3 contacts/memory/contacts/scripts/crm-remind.py --check`
If there are due items, notify the user.
```

## 使用技巧

- 在导入联系人数据前，可以使用`--dry-run`选项进行预览。
- 在批量修改联系人信息后，运行`crm-index.py`以更新索引。
- 标签应为小写，用逗号分隔。
- 联人信息的唯一标识符（slug）会自动生成（格式为小写字母加连字符）。
- 对于通过自然语言输入创建的联系人，系统会自动提取相关信息并使用`crm-add.py`脚本进行处理。