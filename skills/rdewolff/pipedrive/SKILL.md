---
name: pipedrive
description: Pipedrive CRM API 用于管理交易、联系人（个人）、组织、活动、潜在客户、销售流程、产品以及备注。该 API 可用于销售流程管理、交易跟踪、联系人/组织管理、活动调度、潜在客户处理，或任何与 Pipedrive CRM 相关的任务。
---

# Pipedrive

这是一个用于管理销售线索（deals）、联系人（contacts）、组织（organizations）、活动（activities）、销售流程（pipelines）、潜在客户（leads）以及备注（notes）的销售CRM（Customer Relationship Management） API。

## 设置

从Pipedrive获取您的API令牌：
1. 进入“设置”（Settings） → “个人偏好设置”（Personal preferences） → “API”（API）
2. 复制您的个人API令牌

将令牌保存到`~/.clawdbot/clawdbot.json`文件中：
```json
{
  "skills": {
    "entries": {
      "pipedrive": {
        "apiToken": "YOUR_API_TOKEN"
      }
    }
  }
}
```

或者通过环境变量设置：`PIPEDRIVE_API_TOKEN=xxx`

## 快速参考

### 销售线索（Deals）（非常重要！）
```bash
{baseDir}/scripts/pipedrive.sh deals list                    # List all deals
{baseDir}/scripts/pipedrive.sh deals list --status open      # Open deals only
{baseDir}/scripts/pipedrive.sh deals search "query"          # Search deals
{baseDir}/scripts/pipedrive.sh deals show <id>               # Get deal details
{baseDir}/scripts/pipedrive.sh deals create --title "Deal" --person <id> --value 1000
{baseDir}/scripts/pipedrive.sh deals update <id> --value 2000 --stage <stage_id>
{baseDir}/scripts/pipedrive.sh deals won <id>                # Mark deal as won
{baseDir}/scripts/pipedrive.sh deals lost <id> --reason "Reason"  # Mark deal as lost
{baseDir}/scripts/pipedrive.sh deals delete <id>             # Delete deal
```

### 联系人（Persons）（联系人）
```bash
{baseDir}/scripts/pipedrive.sh persons list                  # List all persons
{baseDir}/scripts/pipedrive.sh persons search "query"        # Search persons
{baseDir}/scripts/pipedrive.sh persons show <id>             # Get person details
{baseDir}/scripts/pipedrive.sh persons create --name "John Doe" --email "john@example.com"
{baseDir}/scripts/pipedrive.sh persons update <id> --phone "+1234567890"
{baseDir}/scripts/pipedrive.sh persons delete <id>           # Delete person
```

### 组织（Organizations）
```bash
{baseDir}/scripts/pipedrive.sh orgs list                     # List all organizations
{baseDir}/scripts/pipedrive.sh orgs search "query"           # Search organizations
{baseDir}/scripts/pipedrive.sh orgs show <id>                # Get organization details
{baseDir}/scripts/pipedrive.sh orgs create --name "Acme Corp"
{baseDir}/scripts/pipedrive.sh orgs update <id> --address "123 Main St"
{baseDir}/scripts/pipedrive.sh orgs delete <id>              # Delete organization
```

### 活动（Activities）
```bash
{baseDir}/scripts/pipedrive.sh activities list               # List activities
{baseDir}/scripts/pipedrive.sh activities list --done 0      # Upcoming activities
{baseDir}/scripts/pipedrive.sh activities show <id>          # Get activity details
{baseDir}/scripts/pipedrive.sh activities create --subject "Call" --type call --deal <id>
{baseDir}/scripts/pipedrive.sh activities done <id>          # Mark activity done
```

### 销售流程与阶段（Pipelines & Stages）
```bash
{baseDir}/scripts/pipedrive.sh pipelines list                # List all pipelines
{baseDir}/scripts/pipedrive.sh pipelines stages <pipeline_id>  # List stages in pipeline
```

### 潜在客户（Leads）
```bash
{baseDir}/scripts/pipedrive.sh leads list                    # List all leads
{baseDir}/scripts/pipedrive.sh leads show <id>               # Get lead details
{baseDir}/scripts/pipedrive.sh leads create --title "New Lead" --person <id>
{baseDir}/scripts/pipedrive.sh leads convert <id>            # Convert lead to deal
```

### 产品（Products）
```bash
{baseDir}/scripts/pipedrive.sh products list                 # List all products
{baseDir}/scripts/pipedrive.sh products search "query"       # Search products
```

### 备注（Notes）
```bash
{baseDir}/scripts/pipedrive.sh notes list --deal <id>        # Notes for a deal
{baseDir}/scripts/pipedrive.sh notes list --person <id>      # Notes for a person
{baseDir}/scripts/pipedrive.sh notes create --content "Note text" --deal <id>
```

## 销售线索状态

- `open`：处于销售流程中的活跃线索
- `won`：已成交的线索
- `lost`：未成交的线索
- `deleted`：已删除的线索

## 活动类型

常见类型：`call`（电话）、`meeting`（会议）、`task`（任务）、`deadline`（截止日期）、`email`（电子邮件）、`lunch`（午餐）

## 备注

- API基础地址：`https://api.pipedrive.com/v1`
- 认证方式：通过`api_token`查询参数传递API令牌
- 请求限制：每秒10次请求，每家公司每天100,000次请求
- 分页：使用`start`（偏移量）和`limit`参数进行分页
- 在创建、更新或删除记录之前，请务必确认操作内容

## API参考

有关详细端点文档，请参阅[references/api.md](references/api.md)。