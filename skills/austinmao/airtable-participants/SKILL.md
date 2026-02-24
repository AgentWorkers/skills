---
name: airtable-participants
description: 从 Ceremonia 的 Airtable 数据库中读取和查询静修活动参与者的相关信息。当需要了解参与者信息、订阅者数量、静修活动出席情况、联系方式、电话号码、电子邮件地址或捐赠状态时，可以使用此功能。其他功能（如电子邮件新闻通讯、短信发送）也会依赖此功能来获取接收者列表。默认情况下，该功能的权限仅为只读。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AIRTABLE_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: AIRTABLE_API_KEY
    emoji: "contacts"
    homepage: https://airtable.com/developers/web/api/introduction
---
# Airtable 参与者技能

## 目的

从 Ceremonia 的 Airtable 数据库中查询研讨会参与者的信息。这是确定哪些参与者会收到电子邮件和短信的权威信息来源。默认情况下，访问权限仅为读取；修改记录需要 Austin 的明确指令。

## 必需的设置

确保 `.env` 文件中设置了 `AIRTABLE_API_KEY`。

您还需要：
- **数据库 ID：** [请在 airtable.com/developers 的 Airtable API 文档中核实，或咨询 Austin]
- **表格名称：** [请与 Austin 确认参与者表格的名称]

在核实相关信息后，将确认的数值保存到 `TOOLS.md` 和 `MEMORY.md` 文件中。

## 预期的数据结构

参与者记录至少应包含以下字段：

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| name | 文本 | 全名 |
| email | 电子邮件 | 主要电子邮件地址 |
| phone | 电话号码 | 建议使用 E.164 格式（例如：+1XXXXXXXXXX） |
| retreat_status | 下拉选项 | 例如：active（活跃的）、alumni（校友）、prospective（潜在参与者）、unsubscribed（已取消订阅） |
| tags | 多选字段 | 例如：february-2026（2026 年 2 月参加的）、guide-circle（指导小组成员）、donor（捐赠者） |
| last_contact | 日期 | 最后一次联系的日期 |
| donation_status | 下拉选项 | 例如：donor（捐赠者）、non-donor（非捐赠者） |

[首次使用时，请与 Austin 核实实际的字段名称——确认后更新此部分]

## 常见的查询模式

### 获取所有活跃的参与者（用于发送新闻通讯）
```bash
curl -s "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}?filterByFormula={retreat_status}='active'&fields[]=name&fields[]=email" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | jq '.records[].fields'
```

### 获取有电话号码的参与者（用于短信活动）
```bash
curl -s "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}?filterByFormula=AND({retreat_status}='active',{phone}!='')&fields[]=name&fields[]=phone" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | jq '.records[].fields'
```

### 按状态统计参与者数量
```bash
curl -s "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}?fields[]=retreat_status" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | jq '[.records[].fields.retreat_status] | group_by(.) | map({status: .[0], count: length})'
```

### 按标签筛选参与者
```bash
curl -s "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}?filterByFormula=FIND('february-2026',ARRAYJOIN({tags}))" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | jq '.records[].fields'
```

注意：Airtable 每页显示 100 条记录。使用响应中的 `offset` 参数来获取后续页面的数据：
```bash
curl -s "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}?offset={OFFSET_TOKEN}" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | jq .
```

在报告总数或生成收件人列表之前，务必完整地分页查询所有数据。

## 行为规则

- 默认情况下，访问权限仅为读取；未经 Austin 明确指示，严禁对 Airtable 记录进行 `PATCH`、`POST` 或 `DELETE` 操作。
- 在生成用于电子邮件或短信的收件人列表时，务必过滤掉 `retreat_status` 为 `unsubscribed` 的记录。
- 绝不要在 Slack 消息中包含电子邮件地址或电话号码，仅提供统计数据和分类信息。
- 如果查询结果意外地为 0，请向 Austin 报告问题，而不是发送空列表。
- 所有列表查询都必须完整分页；不要报告部分统计数据或生成不完整的收件人列表。
- 如果 Airtable API 返回错误，请立即将错误代码和错误信息告知 Austin。

## 记录修改（需要 Austin 的批准）

当 Austin 指示修改记录时（例如，将某人标记为已取消订阅或更新 `last_contact`）：
1. 在执行操作前先与 Austin 确认具体的修改内容。
2. 发送 `PATCH` 请求。
3. 在 `memory/logs/crm-writes/YYYY-MM-DD.md` 文件中记录修改信息，内容包括：记录名称/电子邮件、修改的字段、旧值、新值以及 Austin 的指令时间戳。

## 示例调用

- “我们有多少活跃的参与者？”
- “获取 2 月份研讨会的参与者电子邮件列表”
- “谁参加了最近三次研讨会？”
- “系统中有多少人的电话号码？”
- “将 [name] 标记为已取消订阅”（需要 Austin 的批准）
- “获取用于新闻通讯的所有活跃参与者列表”
- “自 1 月以来有多少人新加入？”