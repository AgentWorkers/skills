---
name: ado-sync
description: 关于如何将 Azure DevOps 与 SpecWeave 进行同步的帮助和指导。当您需要了解如何设置 Azure DevOps 的同步配置、配置凭据或解决集成问题时，请参考本文档。若要实际执行同步操作，请使用 `/sw-ado:sync` 命令。
---

# Azure DevOps 同步技能

**功能**：实现 SpecWeave 与 Azure DevOps 之间的无缝同步，以便统一项目跟踪。

**默认行为**：**双向同步**——任一系统中的更改都会自动被同步。

**⚠️ 重要提示**：此技能仅提供关于 Azure DevOps 同步的帮助和指导。实际进行同步操作时，用户应直接使用 `/sw-ado:sync` 命令。该技能不应在调用该命令时自动激活。

**主要功能**：
- 双向同步：SpecWeave ↔ Azure DevOps（默认）
- 从增量创建 Azure DevOps 工作项
- 同步任务进度到 Azure DevOps 评论
- 更新增量状态并反映到 Azure DevOps 中
- 将 Azure DevOps 评论和字段更新同步到 SpecWeave
- 在增量完成后关闭相关 Azure DevOps 工作项
- 支持 Epic、Feature 和 User Story 类型的工作项

---

## 何时激活此技能

✅ **在以下情况下激活**：
- 用户询问：“如何设置 Azure DevOps 同步？”
- 用户询问：“需要哪些 Azure DevOps 凭据？”
- 用户询问：“Azure DevOps 集成是如何工作的？”
- 用户需要帮助配置 Azure DevOps 集成

❌ **在以下情况下不激活**：
- 用户直接调用 `/sw-ado:sync` 命令（该命令会自行处理同步操作）
- 命令已经在运行中（避免重复调用）
- 任务完成钩子正在执行同步操作（此过程是自动的）
- 用户已选择“在任务完成后关闭 Azure DevOps 工作项”

---

## 先决条件

### 1. 安装了 Azure DevOps 插件

```bash
# Check if installed
/plugin list --installed | grep sw-ado

# Install if needed
/plugin install sw-ado@specweave
```

### 2. 拥有 Azure DevOps 个人访问令牌（PAT）

**创建 PAT**：
1. 访问 https://dev.azure.com/{organization}/_usersSettings/tokens
2. 点击“新建令牌”
3. 令牌名称：SpecWeave Sync
4. 权限范围：工作项（读写）、评论（读写）
5. 复制令牌并设置到环境变量中

**设置令牌**：
```bash
export AZURE_DEVOPS_PAT="your-token-here"
```

### 3. 配置 Azure DevOps

将以下配置添加到 `.specweave/config.json` 文件中：
```json
{
  "externalPM": {
    "tool": "ado",
    "enabled": true,
    "config": {
      "organization": "myorg",
      "project": "MyProject",
      "workItemType": "Epic",
      "areaPath": "MyProject\\Team A",
      "syncOnTaskComplete": true
    }
  }
}
```

---

## 可用的命令

### `/sw-ado:create-workitem <increment-id>`

**功能**：根据 SpecWeave 的增量创建 Azure DevOps 工作项

**示例**：
```bash
/sw-ado:create-workitem 0005
```

**结果**：
- 在 Azure DevOps 中创建 Epic/Feature/User Story
- 将工作项与增量关联（元数据）
- 添加包含规格摘要的初始评论
- 设置标签：`specweave`、`increment-0005`

---

### `/sw-ado:sync <increment-id>`

**功能**：同步增量的进度到 Azure DevOps 工作项

**示例**：
```bash
/sw-ado:sync 0005
```

**结果**：
- 计算任务完成百分比
- 更新工作项描述
- 添加进度更新评论
- 更新工作项状态（例如：New → Active → Resolved）

---

### `/sw-ado:close-workitem <increment-id>`

**功能**：在增量完成后关闭对应的 Azure DevOps 工作项

**示例**：
```bash
/sw-ado:close-workitem 0005
```

**结果**：
- 更新工作项状态为“已完成”
- 添加完成总结评论
- 将工作项标记为已解决

---

### `/sw-ado:status <increment-id>`

**功能**：检查增量的同步状态

**示例**：
```bash
/sw-ado:status 0005
```

**结果**：
```
ADO Sync Status
===============
Increment: 0005-payment-integration
Work Item: #12345
URL: https://dev.azure.com/myorg/MyProject/_workitems/edit/12345
State: Active
Completion: 60% (6/10 tasks)
Last Synced: 2025-11-04 10:30:00
Sync Enabled: ✅
```

---

## 自动同步

### 任务完成时

**触发条件**：任务完成后的钩子被触发

**流程**：
1. 用户标记任务完成（例如：`[x] T-005: 添加支付测试`
2. 钩子检测到 Azure DevOps 同步功能已启用
3. 计算新的完成百分比
4. 更新 Azure DevOps 工作项评论

---

### 增量完成时

**触发条件**：执行 `/sw:done` 命令

**流程**：
1. 用户运行 `/sw:done 0005`
2. 确认所有任务均已完成
3. 自动关闭 Azure DevOps 工作项
4. 添加完成总结评论

---

## 工作项类型

### Epic（推荐使用）

**适用场景**：跨越多个冲刺的大型功能

**映射关系**：
- SpecWeave 增量 → Azure DevOps Epic
- 任务 → Epic 描述（待办事项列表）
- 进度 → Epic 评论

---

### Feature

**适用场景**：单个冲刺内的中型功能

**映射关系**：
- SpecWeave 增量 → Azure DevOps Feature
- 任务 → Feature 描述（待办事项列表）
- 进度 → Feature 评论

---

### User Story

**适用场景**：单次冲刺内的小型任务

**映射关系**：
- SpecWeave 增量 → Azure DevOps User Story
- 任务 → User Story 描述（待办事项列表）
- 进度 → User Story 评论

---

## 双向同步（可选）

**启用方式**：在配置文件中设置 `bidirectional: true`

**流程**：
- 用户在 Azure DevOps 中更新工作项状态（例如：从 Active 更改为 Resolved）
- SpecWeave 检测到变化（通过轮询或 Webhook）
- 本地更新增量状态
- 通知用户：“工作项 #12345 已解决 → 增量 0005 被标记为已完成”

**注意**：启用双向同步需要配置 Webhook 或轮询机制。

---

## 配置选项

**`.specweave/config.json` 文件中的配置**：
```json
{
  "externalPM": {
    "tool": "ado",
    "enabled": true,
    "config": {
      "organization": "myorg",
      "project": "MyProject",
      "personalAccessToken": "${AZURE_DEVOPS_PAT}",
      "workItemType": "Epic",
      "areaPath": "MyProject\\Team A",
      "iterationPath": "MyProject\\Sprint 1",
      "syncOnTaskComplete": true,
      "syncOnIncrementComplete": true,
      "createWorkItemsAutomatically": true,
      "bidirectional": false,
      "tags": ["specweave", "increment"],
      "customFields": {
        "incrementId": "Custom.IncrementId"
      }
    }
  }
}
```

---

## 常见问题及解决方法

### 错误：“个人访问令牌无效”

**解决方法**：
1. 确认令牌已设置：`echo $AZURE_DEVOPS_PAT`
2. 检查令牌的权限范围（是否包含“工作项（读写）”
3. 确保令牌未过期
4. 如有必要，重新生成令牌

---

### 错误：“找不到工作项”

**解决方法**：
1. 确认工作项 ID 是否正确
2. 检查是否具有访问该项目的权限
3. 确认工作项未被删除

---

### 错误：“组织或项目未找到”

**解决方法**：
1. 确认组织名称：https://dev.azure.com/{organization}
2. 检查项目名称（区分大小写）
3. 确保具有访问该项目的权限

---

## API 使用限制

**Azure DevOps**：
- 每个 PAT 每分钟允许的请求次数：200 次
- 每小时的最大请求次数：5000 次
**建议**：在配置文件中启用速率限制

**配置方式**：
```json
{
  "externalPM": {
    "config": {
      "rateLimiting": {
        "enabled": true,
        "maxRequestsPerMinute": 150
      }
    }
  }
}
```

## 安全最佳实践

### 应该做的**：
- ✅ 将 PAT 存储在环境变量 `AZURE_DEVOPS_PAT` 中
- ✅ 使用 `.env` 文件（该文件会被 Git 忽略）
- ✅ 仅设置必要的权限范围
- ✅ 每 90 天更新一次 PAT

### 不应该做的**：
- ❌ 将 PAT 提交到 Git
- ❌ 通过 Slack 或电子邮件共享 PAT
- ❌ 使用具有过高权限的 PAT
- ❌ 将 PAT 记录到控制台或文件中

---

## 相关命令

- `/sw:inc`：创建增量（如果启用了同步功能，会自动创建对应的 Azure DevOps 工作项）
- `/sw:do`：执行任务（并自动将进度同步到 Azure DevOps）
- `/sw:done`：完成增量（并自动关闭对应的 Azure DevOps 工作项）
- `/sw:status`：显示增量的状态（包括同步状态）

---

## 示例

### 示例 1：创建增量并同步到 Azure DevOps

```bash
# User
"Create increment for payment integration"

# SpecWeave (if ADO enabled)
1. PM agent generates spec.md
2. Auto-create ADO Epic #12345
3. Link Epic to increment metadata
4. Display: "Created increment 0005 → ADO Epic #12345"
```

### 示例 2：手动同步

```bash
# User completed 3 tasks manually
# Now sync to ADO

/sw-ado:sync 0005

# Result: ADO Epic #12345 updated with 30% progress
```

### 示例 3：检查同步状态

```bash
/sw-ado:status 0005

# Output:
# Work Item: #12345
# URL: https://dev.azure.com/myorg/MyProject/_workitems/edit/12345
# State: Active
# Completion: 60%
# Last Synced: 5 minutes ago
```

---

**状态**：已准备好使用
**版本**：0.1.0
**插件**：specweave-ado