---
name: airtable
description: "您可以通过 Airtable API 直接读取 Airtable 中的数据库、表格和记录。当您需要从 Airtable 中获取电子表格或数据库数据时，可以使用此方法。该方法会直接调用 api.airtable.com，无需借助任何第三方代理。"
metadata:
  openclaw:
    requires:
      env:
        - AIRTABLE_PAT
      bins:
        - python3
    primaryEnv: AIRTABLE_PAT
    files:
      - "scripts/*"
---
# Airtable

您可以通过 `api.airtable.com` 直接读取数据库（bases）、表格（tables）和记录（records）。

## 设置（只需一次）

1. 访问 https://airtable.com/create/tokens
2. 点击 “+ 创建新令牌”（Create new token），并为其命名
3. 选择所需的权限范围：
   - `data.records:read`（读取记录）
   - `schema.bases:read`（读取数据库结构）
4. 在 “访问权限”（Access）部分，选择要授予访问权限的数据库（或全部数据库）
5. 复制生成的令牌——令牌以 `pat` 开头
6. 设置环境变量：
   ```
   AIRTABLE_PAT=pat_your_token_here
   ```

## 命令

### 列出所有可访问的数据库
```bash
python3 /mnt/skills/user/airtable/scripts/airtable.py list-bases
```

### 列出某个数据库中的所有表格
```bash
python3 /mnt/skills/user/airtable/scripts/airtable.py list-tables <base_id>
```

### 列出某个表格中的所有记录
```bash
python3 /mnt/skills/user/airtable/scripts/airtable.py list-records <base_id> "Table Name"
python3 /mnt/skills/user/airtable/scripts/airtable.py list-records <base_id> "Table Name" --limit 50
```

### 使用公式过滤记录
```bash
python3 /mnt/skills/user/airtable/scripts/airtable.py list-records <base_id> "Tasks" --filter "{Status}='Done'"
python3 /mnt/skills/user/airtable/scripts/airtable.py list-records <base_id> "Contacts" --filter "NOT({Email}='')"
```

### 仅根据特定字段过滤记录
```bash
python3 /mnt/skills/user/airtable/scripts/airtable.py list-records <base_id> "People" --fields "Name,Email,Company"
```

### 使用特定的视图（view）显示数据
```bash
python3 /mnt/skills/user/airtable/scripts/airtable.py list-records <base_id> "Tasks" --view "Active Tasks"
```

### 获取特定记录
```bash
python3 /mnt/skills/user/airtable/scripts/airtable.py get-record <base_id> "Table Name" <record_id>
```

### 搜索记录
```bash
python3 /mnt/skills/user/airtable/scripts/airtable.py search-records <base_id> "Contacts" "Smith"
python3 /mnt/skills/user/airtable/scripts/airtable.py search-records <base_id> "Contacts" "smith@acme.com" --field "Email"
```

## 注意事项

- 免费计划：支持无限数量的数据库，每个数据库最多可存储 1,000 条记录。免费用户也可以使用 API 功能。
- 数据库的 ID 以 `app` 开头，记录的 ID 以 `rec` 开头。
- 表格名称区分大小写，必须完全匹配；如果名称包含空格，请使用引号。
- Airtable 已在 2024 年 2 月停止支持旧的 API 密钥，现在仅支持个人访问令牌（Personal Access Tokens，简称 PAT）。