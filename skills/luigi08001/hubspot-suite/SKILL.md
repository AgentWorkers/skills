---
name: hubspot-suite
description: "这是一个全面的 HubSpot CRM（客户关系管理）、营销、销售、服务以及内容管理系统（CMS）管理套件。它涵盖了 HubSpot 的所有 API，包括 CRM 对象（联系人、公司、交易、工单、自定义对象）、关联关系、属性、互动记录（电话、电子邮件、会议、笔记、任务）、工作流与自动化流程、列表、表单、电子邮件营销、报告与分析功能、数据质量与去重处理、数据导入/导出、Webhook、数据管道（pipelines）、内容管理以及电子商务相关功能。该套件支持两种认证方式：私有应用（API 密钥）认证和新的 HubSpot 开发者平台（基于 CLI 的应用程序）。适用于所有与 HubSpot 相关的任务，包括 CRM 管理、营销自动化、销售流程管理、数据迁移、报告生成、数据质量审计以及 HubSpot 系统管理。"
---
# HubSpot套件——全面的CRM与营销平台

本文档涵盖了HubSpot平台的全部功能，包括CRM、营销、销售、服务、内容管理系统（CMS）以及开发工具。

## 快速入门

### 1. 认证设置
```bash
# Private App (Recommended)
export HUBSPOT_ACCESS_TOKEN="pat-na1-xxx"  # or pat-eu1-xxx

# Legacy API Key
export HUBSPOT_API_KEY="your-api-key"
```

有关完整的认证指南（包括新的开发者平台），请参阅`references/auth-setup.md`。

### 2. 基本API测试
```bash
curl -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/objects/contacts?limit=1"
```

## 您想要做什么？

**CRM管理：**
- `references/crm-contacts.md` → 创建、更新、搜索联系人
- `references/crm-companies.md` → 公司记录及层级结构
- `references/crm-deals.md` → 销售流程、交易阶段
- `references/crm-tickets.md` → 支持工单、SLA管理
- `references/crm-custom-objects.md` → 自定义对象模式

**数据与关联：**
- `references/associations.md` → 建立记录关联（联系人→公司、交易→联系人）
- `references/properties.md` → 自定义属性、字段组
- `references/data-quality.md` → 数据去重、数据清洗
- `references/import-export.md` → 批量数据导入/导出

**活动与自动化：**
- `references/engagements.md` → 记录通话、电子邮件、会议、任务
- `references/workflows.md` → 自动化流程、触发器、用户注册
- `references/pipelines.md` → 配置自动化流程、阶段设置

**营销与销售：**
- `references/lists.md` → 联系人列表、客户细分
- `references/forms.md` → 登录页面表单
- `references/email-marketing.md` → 电子邮件营销活动
- `references/conversations.md` → 实时聊天、聊天机器人

**分析与报告：**
- `references/reporting.md` → 自定义仪表板、关键绩效指标（KPI）
- `references/webhooks.md` → 实时事件通知

**内容与商务：**
- `references/cms.md` → 网站页面、博客文章、HubDB
- `references/commerce.md` → 产品信息、报价单、发票

**平台与开发：**
- `references/developer-platform.md` → HubSpot命令行界面（CLI）、自定义应用程序
- `references/owners.md` → 用户管理、权限设置
- `references/knowledge-base-tips.md` → 用户界面导航、管理员任务

## 常见操作流程

### 1. 从CSV文件导入联系人
```bash
./scripts/bulk-import.sh contacts contacts.csv
```

### 2. 查找并合并重复联系人
```bash
./scripts/find-duplicates.sh contacts email
./scripts/merge-records.sh contacts ID1 ID2
```

### 3. 创建包含关联关系的交易记录
```bash
# Create deal
curl -X POST "https://api.hubapi.com/crm/v3/objects/deals" \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "dealname": "Big Deal",
      "amount": "50000",
      "dealstage": "qualifiedtobuy"
    }
  }'

# Associate to contact (type 3 = deal→contact)
curl -X PUT "https://api.hubapi.com/crm/v3/objects/deals/DEAL_ID/associations/contacts/CONTACT_ID/3" \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN"
```

### 4. 数据质量审核
```bash
./scripts/data-audit.sh
```

### 5. 导出流程报告
```bash
./scripts/pipeline-report.sh > pipeline_report.csv
```

### 6. 记录活动（通话/电子邮件/会议）
```bash
# Log a sales call
curl -X POST "https://api.hubapi.com/crm/v3/objects/calls" \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "hs_call_title": "Discovery Call",
      "hs_call_duration": "1800000",
      "hs_call_disposition": "Connected"
    },
    "associations": [{
      "to": { "id": "CONTACT_ID" },
      "types": [{ "associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 194 }]
    }]
  }'
```

## 脚本使用

所有脚本均位于`scripts/`目录中。在使用前，请确保脚本可执行：
```bash
chmod +x scripts/*.sh
```

**通用API辅助工具：**
```bash
./scripts/hs-api.sh GET /crm/v3/objects/contacts
./scripts/hs-api.sh POST /crm/v3/objects/companies '{"properties":{"name":"ACME"}}'
```

**数据管理：**
```bash
./scripts/bulk-import.sh [object-type] [csv-file]
./scripts/bulk-export.sh [object-type] [output-file]
./scripts/find-duplicates.sh [object-type] [property]
./scripts/merge-records.sh [object-type] [primary-id] [duplicate-id]
```

**报告与分析：**
```bash
./scripts/data-audit.sh > audit-report.txt
./scripts/pipeline-report.sh > pipeline-analysis.csv
```

## API基础知识

### 请求限制
- **私有应用程序：**每10秒100次请求
- **OAuth应用程序：**每10秒100次请求
- **搜索API：**每秒4次请求
- **批量操作：**每次请求最多100条记录

### 分页
所有列表接口均使用`after`参数进行分页：
```bash
curl "https://api.hubapi.com/crm/v3/objects/contacts?after=12345&limit=100"
```

### 错误处理
- **429：**请求次数超出限制 → 等待后重试
- **400：**请求错误 → 检查属性名称/值
- **401：**认证失败 → 检查令牌/权限范围
- **404：**对象未找到 → 验证ID是否存在

### 常见请求头
```bash
-H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN"
-H "Content-Type: application/json"
```

### 批量操作模式
```bash
curl -X POST "https://api.hubapi.com/crm/v3/objects/contacts/batch/create" \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {"properties": {"firstname": "John", "lastname": "Doe"}},
      {"properties": {"firstname": "Jane", "lastname": "Smith"}}
    ]
  }'
```

## 搜索过滤器与操作符

### 过滤语法
```json
{
  "filters": [{
    "propertyName": "email",
    "operator": "EQ",
    "value": "john@example.com"
  }]
}
```

### 操作符
- **EQ, NEQ：**等于、不等于
- **LT, LTE, GT, GTE：**小于/大于
- **CONTAINS_TOKEN：**包含指定单词
- **HAS_PROPERTY, NOTHAS_PROPERTY：**属性存在/不存在
- **IN, NOT_IN：**值在列表中
- **BETWEEN：**数值/日期范围

### 高级搜索示例
```bash
curl -X POST "https://api.hubapi.com/crm/v3/objects/contacts/search" \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": [{
      "propertyName": "createdate",
      "operator": "GTE", 
      "value": "2024-01-01"
    }],
    "sorts": [{"propertyName": "createdate", "direction": "DESCENDING"}],
    "limit": 100
  }'
```

## 环境变量

请在您的shell或环境中设置以下变量：
```bash
# Required
export HUBSPOT_ACCESS_TOKEN="pat-na1-xxx"  # Private app token

# Optional  
export HUBSPOT_API_KEY="xxx"               # Legacy API key
export HUBSPOT_PORTAL_ID="12345"           # For some API calls
export HUBSPOT_BASE_URL="https://api.hubapi.com"  # Override for testing
```

## 需要帮助吗？

1. **API相关问题：**请参阅`references/rate-limits.md`和`references/search-filters.md`
2. **认证问题：**请参阅`references/auth-setup.md`
3. **用户界面相关问题：**请参阅`references/knowledge-base-tips.md`
4. **数据问题：**请使用`references/data-quality.md`
5. **特定对象操作：**请查找相应的`references/crm-*.md`文件

本文档涵盖了HubSpot平台的全部功能。请根据您的需求从相应的参考文档开始学习，然后使用脚本自动化重复性操作。