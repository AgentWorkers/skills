---
name: omnium-hub-crm
description: 管理 Omnium Hub CRM（联系人、商机、预约）。用于所有与 CRM 相关的任务。
---
# Omnium Hub 技能

此技能允许您与 **Omnium Hub** 客户关系管理（CRM）系统进行交互。

## 先决条件

要使用此技能，您需要一个 **Omnium Hub API 密钥**。
- 如果您没有 API 密钥，请向用户索取：“请提供您的 Omnium Hub API 密钥以继续操作。”
- 获取密钥后，请在以下脚本中使用它。

## 工具

### 1. 管理联系人

使用 `scripts/omnium_client.py` 来管理联系人。

**使用方法：**
```bash
python3 scripts/omnium_client.py --api-key "YOUR_KEY" contacts --action [lookup|create|update] --email "user@example.com" [other options]
```

**可执行的操作：**
- `lookup`：通过电子邮件或电话号码查找联系人。
- `create`：创建新的联系人。
- `update`：更新现有的联系人。

**示例：**
*   “在 Omnium Hub 中查找名为 john@example.com 的联系人。”
    -> `python3 scripts/omnium_client.py --api-key "..." contacts --action lookup --email "john@example.com"`

*   “将 Jane Doe (jane@test.com) 添加到 Omnium Hub 中。”
    -> `python3 scripts/omnium_client.py --api-key "..." contacts --action create --first-name "Jane" --last-name "Doe" --email "jane@test.com"`

### 2. 管理机会（Opportunities）

使用 `scripts/omnium_client.py` 并配合 `opportunities` 命令来管理机会（业务机会）。

**使用方法：**
```bash
python3 scripts/omnium_client.py --api-key "YOUR_KEY" opportunities --action list --pipeline-id "..."
```

## 故障排除**

- **401 Unauthorized**：API 密钥无效。请让用户检查他们的 Omnium Hub 凭据。
- **404 Not Found**：联系人或资源不存在。