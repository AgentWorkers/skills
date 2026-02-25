---
name: hubspot
description: "通过 HubSpot API 查询和管理 HubSpot CRM 数据。当您需要搜索或管理联系人、公司、交易记录或销售管道时，可以使用该功能。支持创建、更新和关联 CRM 对象。直接调用 api.hubapi.com，无需通过第三方代理。"
metadata:
  openclaw:
    requires:
      env:
        - HUBSPOT_TOKEN
      bins:
        - python3
    primaryEnv: HUBSPOT_TOKEN
    files:
      - "scripts/*"
---
# HubSpot

您可以通过 HubSpot API (`api.hubapi.com`) 直接与 HubSpot 客户关系管理（CRM）系统进行交互。

## 设置（一次性操作）

1. 在 HubSpot 中，进入“设置”（Settings）→“集成”（Integrations）→“私有应用”（Private Apps），然后创建一个新的私有应用。
2. 为该应用授予以下权限：`crm.objectscontacts.read`、`crm.objectscontacts.write`、`crm.objects.companies.read`、`crm.objects.companies.write`、`crm.objects.deals.read`、`crm.objects.deals.write`、`tickets`。
3. 复制访问令牌（access token）。
4. 设置环境变量：
   ```
   HUBSPOT_TOKEN=pat-na1-...
   ```

## 查询操作

### 搜索联系人
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py search contacts --query "john"
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py search contacts --email "john@example.com"
```

### 列出联系人
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py list contacts --limit 20
```

### 获取特定对象
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py get contacts 12345
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py get companies 67890
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py get deals 11111
```

### 列出公司
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py list companies --limit 20
```

### 搜索公司
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py search companies --query "Acme"
```

### 列出交易记录
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py list deals --limit 20
```

### 搜索交易记录
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py search deals --query "enterprise"
```

### 列出工单
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py list tickets --limit 20
```

### 创建联系人
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py create contacts --email "new@example.com" --firstname "Jane" --lastname "Doe"
```

### 创建公司
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py create companies --name "Acme Corp" --domain "acme.com"
```

### 创建交易记录
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py create deals --dealname "Enterprise Plan" --amount 50000 --pipeline default --dealstage appointmentscheduled
```

### 更新对象
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py update contacts 12345 --email "new@example.com" --phone "+1234567890"
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py update deals 11111 --dealstage closedwon --amount 75000
```

### 关联对象
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py associate contacts 12345 companies 67890
```

### 列出销售流程（pipelines）
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py pipelines deals
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py pipelines tickets
```

### 列出联系人所有者
```bash
python3 /mnt/skills/user/hubspot/scripts/hubspot_query.py owners
```