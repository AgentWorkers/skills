# 技能：通过 Pave Query API 操作 JobTread

## 概述  
该技能允许您完全通过 OpenClaw，利用 `https://api.jobtread.com/pave` 上的基于 Pave 的 API 来操作 JobTread。每个请求都是一个 POST 请求，其中包含一个 `query` 对象，该对象使用 GraphQL 风格的表达式来定义需要获取的数据字段。通过正确的授权密钥，您可以创建和管理账户（客户/供应商）、任务、文档、位置以及自定义字段，并且还可以订阅 Webhook 以接收实时更新。

## 设置与凭证  
1. **创建授权密钥：** 登录到 `https://app.jobtread.com/grants` 并创建一个新的自动化授权密钥。复制一次性的 `grantKey`（它以 `grant_` 开头，且只会显示一次）。  
2. **本地存储密钥：** 将密钥保存在安全的位置，例如 `~/.config/jobtread/grant_key` 文件中。  
3. **保持密钥的有效性：** JobTread 会在 3 个月无活动后失效，因此请安排定时任务（如 cron/heartbeat）来轮换或重新使用该密钥。  
4. **可选的 Webhook 密钥：** 如果您计划接收 Webhook，请记录其端点 URL 并将 Webhook ID 保存在同一文件夹中，以便后续禁用或检查。

## 认证  
- 所有发送到 `/pave` 的 POST 请求都必须包含 `query.$.grantKey`。示例请求体：  
   ```json
  {
    "query": {
      "$": { "grantKey": "grant_xxx" },
      "currentGrant": { "id": {}, "user": { "name": {} } }
    }
  }
  ```  
- 如果需要抑制通知或限制查询结果的范围，您还可以在 `$` 中设置 `notify`、`timeZone` 或 `viaUserId`。  
- 对于需要签名的请求（PDF 令牌、预签名数据），请使用 `pdfToken: { _: signQuery, $: { query: {...} } }`，并将生成的令牌附加到 `https://api.jobtread.com/t/`。

## API 基础与请求流程  
- 所有请求都发送到 `POST https://api.jobtread.com/pave`，并且请求头必须设置为 `Content-Type: application/json`。  
- 请求的结构如下：  
   ```json
  {
    "query": {
      "$": { "grantKey": "grant_xxx" },  
      "operation": {
        "$": { ...inputs... },
        "field": { ...fields... }
      }
    }
  }
  ```  
- 您请求的字段（如 `id`、`name` 等）决定了 JobTread 返回的数据内容。在后续引用对象时，请务必包含 `id` 字段。  
- 响应中的 `_type` 字段用于指示数据的结构（即数据所属的类型）。

## 常见用法与示例  
### 1. 获取组织 ID  
```yaml
currentGrant:
  user:
    memberships:
      nodes:
        organization:
          id: {}
          name: {}
```  
使用返回的 `organization.id` 在后续的查询中识别组织。  

### 2. 创建客户/供应商  
- **创建客户：**  
```yaml
createAccount:
  $:
    name: "Test Customer"
    type: customer
    organizationId: "ORG_ID"
  createdAccount:
    id: {}
    name: {}
    type: {}
```  
- **创建供应商：** （与上述相同，但设置 `type: vendor`）。  

### 3. 读取或更新账户信息  
- **读取账户信息：** 提供 `id` 并指定需要获取的字段：  
```yaml
account:
  $:
    id: "ACCOUNT_ID"
  id: {}
  name: {}
  isTaxable: {}
```  
- **更新账户信息：** 如有需要，可以添加 `customFieldValues`：  
```yaml
updateAccount:
  $:
    id: "ACCOUNT_ID"
    isTaxable: false
  account:
    id: {}
    isTaxable: {}
```  

### 4. 分页、排序和过滤账户列表  
```yaml
organization:
  $: {}
  id: {}
  accounts:
    $:
      size: 5
      page: "1"
      sortBy:
        - field: type
          order: desc
      where:
        and:
          - - type
            - =
            - customer
          - - name
            - =
            - "Sebas Clients"
    nextPage: {}
    nodes:
      id: {}
      name: {}
      type: {}
```  

### 5. 使用 `where` 进行查询（支持 `or`、嵌套字段和自定义字段）  
- 根据自定义字段名称查找账户：  
```yaml
organization:
  $: {}
  id: {}
  contacts:
    $:
      with:
        cf:
          _: customFieldValues
          $:
            where:
              - - customField
                - name
              - "VIP"
            values:
              $:
                field: value
      where:
        - - cf
          - values
        - =
        - "Yes"
    nodes:
      id: {}
      name: {}
```  

### 6. 地点信息及嵌套过滤  
- 创建地点信息并查找与该地点关联的其他账户：  
```yaml
createLocation:
  $:
    accountId: "ACCOUNT_ID"
    name: Test Location
    address: "123 Main St"
  createdLocation:
    id: {}
    name: {}

organization:
  $: {}
  id: {}
  locations:
    $:
      where:
        - - account
          - name
        - Test Name
    nodes:
      id: {}
      name: {}
      account:
        id: {}
        name: {}
```  

### 7. 文档、任务及其汇总数据  
- 按类型/状态分组获取任务文档并计算总数：  
```yaml
job:
  $:
    id: "JOB_ID"
  documents:
    $:
      where:
        - - type
          - in
          - - customerInvoice
            - customerOrder
      group:
        by:
          - type
          - status
        aggs:
          amountPaid:
            sum: amountPaid
          priceWithTax:
            sum: priceWithTax
    withValues: {}
```  
- 获取文档的 PDF 令牌（将其附加到 `https://api.jobtread.com/t/{{token}}`）：  
```yaml
pdfToken:
  _: signQuery
  $:
    query:
      pdf:
        $:
          id: "DOCUMENT_ID"
```  

### 8. 自定义字段  
- 读取记录的自定义字段值（每次请求最多获取 25 个值）：  
```yaml
account:
  $:
    id: "ACCOUNT_ID"
  customFieldValues:
    $:
      size: 25
    nodes:
      id: {}
      value: {}
      customField:
        id: {}
```  
- 通过 `customFieldValues` 更新自定义字段：  
```yaml
updateAccount:
  $:
    id: "ACCOUNT_ID"
    customFieldValues:
      "CUSTOM_FIELD_ID": "New value"
  account:
    id: {}
```  

### 9. Webhook  
- 使用 JobTread 的用户界面创建 Webhook 并复制其 ID。  
- 通过 API 管理 Webhook：使用 `listWebhook(id: "ID")` 列出所有 Webhook，或使用 `deleteWebhook` 删除它们。  
- 示例创建请求：  
```yaml
createWebhook:
  $:
    organizationId: "ORG_ID"
    url: "https://your-endpoint/hooks/jobtread"
    eventTypes:
      - jobCreated
      - documentUploaded
  createdWebhook:
    id: {}
    url: {}
```  

## 在 OpenClaw 中使用该技能  
- 可以使用 `curl` 或您喜欢的 HTTP 客户端，通过 OpenClaw 的 `exec` 工具发送请求。  
- 按照示例构建 JSON 请求体（务必在 `$` 中包含授权密钥）。  
- 为了便于使用，您也可以将请求体保存在 shell 变量或辅助脚本中，以便后续通过名称调用（例如 “run job summary” 或 “create customer”）。  
- 将每个自动化脚本记录在 JobTread 的配置文件中，以便在后续会话中直接调用而无需翻阅日志。

## 自动化应用示例  
1. **夜间任务总结：** 查询所有未完成的任务，统计已批准的客户订单，并将结果存储在 Obsidian 中（或通过 WhatsApp 发送）。  
2. **Webhook 监控：** 自动触发 Webhook 监控文件上传，并通过小型服务器将通知转发到 Slack/WhatsApp。  
3. **批量创建账户：** 提供客户/供应商的 CSV 列表，使用相同的授权密钥批量创建账户。  
4. **文档检查：** 查询状态为 “pending”的文档，并在每天早上发送汇总信息。  

## 故障排除与提示  
- **速率限制：** 授权密钥有使用次数限制。如果超出限制，请在请求之间添加 `time.sleep` 间隔或减少请求数量。  
- **缺少 ID：** 如果忘记请求 `id`，API 会提示 “id field required”。在修改记录时请务必包含该字段。  
- **授权密钥过期：** 如果请求返回 “invalid key”，请更新 `~/.config/jobtread/grant_key`。  
- **Webhook：** 记录 Webhook ID 的使用情况，以便后续禁用或重新配置它们。  
- **签名令牌：** 在需要临时访问文档 PDF 时使用 `signQuery`，以避免存储原始文档 ID。