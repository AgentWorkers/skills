---
name: gmail-cleaner
description: 批量清理和整理Gmail账户。适用于需要清理Gmail邮件、删除垃圾邮件或促销邮件、按发件人批量删除邮件、创建标签、设置自动过滤器或从垃圾箱中恢复邮件的场景。支持通过OAuth令牌文件管理单个或多个Gmail账户，并兼容使用Gmail API的任何Gmail账户。
---
# Gmail清理工具

使用Gmail API批量清理Gmail邮件。每次API调用可处理1000条邮件。

## 前提条件

- 需要安装`google-api-python-client`和`google-auth-oauthlib`这两个Python包（如果未安装，脚本会自动安装）
- 从Google Cloud Console获取OAuth凭证（桌面应用类型）
- 每个账户的令牌文件保存为`.pkl`格式

## 工作流程

### 1. 认证（首次使用或新账户）

```bash
python scripts/auth.py --credentials /path/to/credentials.json --token /path/to/token.pkl --scopes settings
```

- 需要的权限范围：读取/修改/删除邮件及标签  
- 需要添加`gmail.settings.basic`权限范围（用于创建邮件过滤器）  
- 默认令牌文件路径：`~/.openclaw/workspace/gmail_token.pkl`  
- 默认凭证文件路径：`~/.openclaw/workspace/gmail_credentials.json`  

对于第二个账户，请指定不同的令牌文件路径（例如：`gmail_token_work.pkl`）。

### 2. 扫描（确定需要清理的邮件）

```bash
python scripts/scan.py --token /path/to/token.pkl --sample 500
```

显示按类别分类的收件箱邮件数量以及前40位发件人。请先运行此步骤。

### 3. 清理（批量删除垃圾邮件）

```bash
# Trash specific senders:
python scripts/clean.py --from "spam@example.com,news@example.org"

# Trash by Gmail search query:
python scripts/clean.py --query "category:promotions older_than:30d"

# From a JSON config file (list of {query, label}):
python scripts/clean.py --config senders.json

# Permanently delete instead of trash:
python scripts/clean.py --from "spam@example.com" --delete

# Dry run first:
python scripts/clean.py --from "spam@example.com" --dry-run
```

### 4. 深度清理（全面清理）

```bash
# Full deep clean (4 steps: trash promos → archive old → mark read → purge trash):
python scripts/deep_clean.py

# Custom age thresholds:
python scripts/deep_clean.py --promo-days 7 --archive-days 30 --unread-days 14

# Skip trash purge (keep trash for 30-day auto-delete):
python scripts/deep_clean.py --skip-trash-purge
```

### 5. 组织邮件（添加标签和创建过滤器）

```bash
# Apply built-in label set (Business, Banking, Tech, Personal, Trading, Social):
python scripts/organize.py

# Custom labels/rules/filters from JSON:
python scripts/organize.py --config labels.json

# Labels only (no filters):
python scripts/organize.py --skip-filters
```

### 6. 恢复（从垃圾邮件箱中恢复重要邮件）

```bash
# Restore all emails from a sender + apply a label:
python scripts/restore.py --from healthbeat@mail.health.harvard.edu --label "Harvard Health"

# Restore by query:
python scripts/restore.py --query "from:apple.com in:trash" --label "Tech/Apple"
```

## 多个账户

请为每个账户指定不同的令牌文件路径来运行相应的脚本：

```bash
python scripts/scan.py    --token ~/.openclaw/workspace/gmail_token_personal.pkl
python scripts/scan.py    --token ~/.openclaw/workspace/gmail_token_work.pkl
python scripts/deep_clean.py --token ~/.openclaw/workspace/gmail_token_work.pkl
```

## 常见操作模式

**对单个账户进行彻底清理：**
```bash
python scripts/auth.py --scopes settings
python scripts/scan.py                         # identify top senders
python scripts/clean.py --from "..."          # trash specific senders
python scripts/deep_clean.py                   # clean categories
python scripts/organize.py                     # create labels + filters
```

**恢复在批量删除中被误删的重要邮件：**
```bash
python scripts/restore.py --from important@example.com --label "Important"
```

**`clean.py --config`命令中使用的发件人配置文件格式：**
```json
[
  {"query": "from:temu@eu.temuemail.com", "label": "Temu"},
  {"query": "category:promotions older_than:7d", "label": "Old Promos"}
]
```

## 注意事项

- `batchModify`操作会将邮件移动到垃圾箱——Gmail会在30天后自动删除这些邮件  
- `batchDelete`操作是不可逆的，请务必先进行测试  
- 创建Gmail过滤器需要`gmail.settings.basic`权限范围；如果创建过滤器时出现403错误，请使用`--scopes settings`重新认证  
- `scan.py`仅随机抽取N条邮件进行扫描；如果收件箱邮件数量较多，建议使用`--sample 2000`以提高准确性  
- 凭证信息请从Google Cloud Console的“API与服务”→“凭证”→“OAuth 2.0”→“下载JSON”获取