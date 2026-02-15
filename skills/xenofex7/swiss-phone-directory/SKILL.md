---
name: swiss-phone-directory
description: "通过 search.ch API 查找瑞士电话目录信息。可以搜索企业、个人信息，或进行电话号码的反向查询。适用场景包括：(1) 查找瑞士公司或个人的联系方式；(2) 通过名称或电话号码查找地址；(3) 进行电话号码的反向查询；(4) 查找企业所属类别。使用该服务需要 SEARCHCH_API_KEY。"
metadata:
  openclaw:
    requires:
      env:
        - SEARCHCH_API_KEY
---

# Swiss Phone Directory Skill

您可以使用瑞士电话目录（search.ch）来查找企业、个人和电话号码。

## 快速入门

```bash
# Search for a business
python3 scripts/searchch.py search "Migros" --location "Zürich"

# Search for a person
python3 scripts/searchch.py search "Müller Hans" --type person

# Reverse phone number lookup
python3 scripts/searchch.py search "+41442345678"

# Business-only search
python3 scripts/searchch.py search "Restaurant" --location "Bern" --type business --limit 5
```

## 命令

### search
用于搜索企业、个人或电话号码。

```bash
python3 scripts/searchch.py search <query> [options]

Options:
  --location, -l    City, ZIP, street, or canton (e.g., "Zürich", "8000", "ZH")
  --type, -t        Filter: "business", "person", or "all" (default: all)
  --limit, -n       Max results (default: 10, max: 200)
  --lang            Output language: de, fr, it, en (default: de)
```

### 示例

```bash
# Find restaurants in Rapperswil
python3 scripts/searchch.py search "Restaurant" -l "Rupperswil" -t business -n 5

# Find a person by name
python3 scripts/searchch.py search "Meier Peter" -l "Zürich" -t person

# Reverse lookup a phone number
python3 scripts/searchch.py search "044 123 45 67"

# Search with canton abbreviation
python3 scripts/searchch.py search "Bäckerei" -l "SG"
```

## 输出格式

搜索结果包含以下信息（如可用）：
- **名称** - 企业或个人名称
- **类型** - 组织或个人
- **地址** - 街道、邮政编码、城市、州
- **电话** - 可点击的电话链接（例如：`[044 123 45 67](tel:+41441234567)`
- **传真** - 可点击的电话链接
- **电子邮件** - 电子邮件地址
- **网站** - 网站地址
- **类别** - 企业类别

### 可点击的电话号码 📞

电话号码会自动格式化为带有 `tel:` 协议的 Markdown 链接：
```
📞 [044 123 45 67](tel:+41441234567)
```

这支持在移动设备（如 Telegram、Signal、WhatsApp 等）上直接拨打电话。

如需禁用可点击链接，请使用 `--no-clickable` 参数。

## 配置

### 获取 API 密钥（免费）

1. **请求密钥**：https://search.ch/tel/api/getkey.en.html
2. 填写表格（姓名、电子邮件、使用场景）
3. **审核**：大约需要 10-15 分钟，密钥将通过电子邮件发送给您

### 设置环境变量

```bash
export SEARCHCH_API_KEY="your-api-key-here"
```

有关永久性设置的详细信息，请参阅 [references/configuration.md](references/configuration.md)。

## API 参考

- 基本 URL：`https://search.ch/tel/api/`
- 调用限制：取决于 API 密钥的等级
- 完整文档：https://search.ch/tel/api/help.en.html