---
name: gate-exchange-subaccount
version: "2026.3.12-1"
updated: "2026-03-12"
description: 在 Gate Exchange 中管理子账户，包括查询子账户状态、列出子账户、创建子账户、锁定子账户以及解锁子账户。每当用户询问有关子账户管理、子账户状态、创建子账户、锁定子账户或解锁子账户的问题时，均可使用此技能。相关触发短语包括：“sub-account”、“subaccount”、“sub account status”、“create sub-account”、“lock sub-account”、“unlock sub-account”、“list sub-accounts”、“my sub-accounts”，或任何涉及子账户查询或管理操作的请求。
---
# Gate Exchange子账户管理技能

提供在Gate平台上管理子账户的功能，包括查询子账户状态、列出所有子账户、创建新子账户以及锁定/解锁子账户。

## 先决条件

- **MCP依赖**：需要安装[gate-mcp](https://github.com/gate/gate-mcp)。
- **身份验证**：所有子账户操作均需使用主账户的API密钥进行身份验证。
- **权限**：当前用户必须是主账户持有者才能管理子账户。

## 可用的MCP工具

| 工具 | 需要身份验证 | 描述 |
|------|------|-------------|
| `cex_sa_get_sa` | 是 | 通过用户ID获取特定子账户的详细信息 |
| `cex_sa_list_sas` | 是 | 列出主账户下的所有子账户 |
| `cex_sa_create_sa` | 是 | 创建一个新的普通子账户 |
| `cex_sa_lock_sa` | 是 | 锁定子账户以禁用登录和交易 |
| `cex_sa_unlock_sa` | 是 | 解锁之前被锁定的子账户 |

## 工作流程

### 第一步：识别用户意图

解析用户的消息以确定他们需要执行哪种子账户操作。

需要提取的关键数据：
- `intent`：`query_status`、`list_all`、`create`、`lock`、`unlock`之一
- `user_id`：子账户的UID（`query_status`、`lock`、`unlock`操作必需）
- `login_name`：所需的子账户用户名（`create`操作可能需要用户提供）

意图检测规则：

| 信号关键词 | 意图 |
|----------------|--------|
| "子账户状态"、"子账户UID {id}"、"检查子账户" | `query_status` |
| "所有子账户"、"列出子账户"、"我的子账户" | `list_all` |
| "创建子账户"、"新子账户"、"添加子账户" | `create` |
| "锁定子账户"、"禁用子账户"、"冻结子账户" | `lock` |
| "解锁子账户"、"启用子账户"、"解冻子账户" | `unlock` |

### 第二步：根据意图执行操作

#### 情况A：查询子账户状态 (`query_status`)

调用 `cex_sa_get_sa`，传入：
- `user_id`：用户提供的子账户UID

需要提取的关键数据：
- `login_name`：子账户用户名
- `remark`：子账户备注
- `state`：账户状态（正常/锁定）
- `type`：账户类型（普通/池）
- `create_time`：账户创建时间

以结构化格式展示子账户的详细信息。

#### 情况B：列出所有子账户 (`list_all`)

调用 `cex_sa_list_sas`，传入：
- `type`："0"（仅列出普通子账户）

需要提取的关键数据：
- 对于每个子账户：`user_id`、`login_name`、`remark`、`state`、`create_time`

将结果以表格形式展示，包括用户名、UID、备注（如果有）和当前状态。

#### 情况C：创建子账户 (`create`)

**预检查**：调用 `cex_sa_list_sas`，传入 `type`："0" 以获取当前所有普通子账户的列表。根据返回的列表数量判断用户是否还可以创建更多子账户。

如果可以创建新账户：
1. 请求用户提供新子账户的用户名
2. 可选地收集：电子邮件、备注
3. 在继续之前与用户确认所有详细信息
4. 调用 `cex_sa_create_sa`，传入：
   - `login_name`：用户提供的用户名（必需）
   - `email`：用户提供的电子邮件（可选）
   - `remark`：用户提供的备注（可选）
5. 展示新创建的子账户的详细信息

需要提取的关键数据：
- `user_id`：新创建的子账户UID
- `login_name`：确认的用户名
- `state`：应为“正常”

**注意**：此技能仅支持创建普通子账户。

#### 情况D：锁定子账户 (`lock`)

1. 验证是否提供了 `user_id`；如果没有，请用户提供。
2. 调用 `cex_sa_get_sa`，传入 `user_id` 以确认子账户存在并且属于主账户。
3. 如果子账户已经被锁定，告知用户并停止操作。
4. 与用户确认：“您确定要锁定子账户 {user_id} ({login_name}) 吗？这将禁用该子账户的登录和交易功能。”
5. 确认后，调用 `cex_sa_lock_sa`，传入：
   - `user_id`：子账户UID
6. 报告操作结果

需要提取的关键数据：
- 锁定操作的成败状态

#### 情况E：解锁子账户 (`unlock`)

1. 验证是否提供了 `user_id`；如果没有，请用户提供。
2. 调用 `cex_sa_get_sa`，传入 `user_id` 以确认子账户存在并且当前被锁定。
3. 如果子账户已经被解锁或处于正常状态，告知用户并停止操作。
4. 与用户确认：“您确定要解锁子账户 {user_id} ({login_name}) 吗？”
5. 确认后，调用 `cex_sa_unlock_sa`，传入：
   - `user_id`：子账户UID
6. 报告操作结果

需要提取的关键数据：
- 解锁操作的成败状态

### 第三步：格式化并响应

使用以下报告模板展示结果。始终包含相关上下文和下一步操作建议。

## 判断逻辑总结

| 条件 | 操作 |
|-----------|--------|
| 用户请求查询特定子账户的状态及其UID | 跳转到情况A：`query_status` |
| 用户请求查看所有子账户 | 跳转到情况B：`list_all` |
| 用户想要创建新子账户 | 跳转到情况C：`create` |
| 用户想要锁定某个子账户 | 跳转到情况D：`lock` |
| 用户想要解锁某个子账户 | 跳转到情况E：`unlock` |
| 操作所需的信息（如UID）未提供 | 询问用户子账户的UID |
| 创建操作所需的信息（如用户名）未提供 | 询问用户用户名 |
| 子账户已经处于目标状态（锁定/解锁） | 告知用户，无需操作 |
| API返回身份验证错误 | 提示用户登录 |
| API返回权限错误 | 告知用户需要主账户权限 |
| 子账户不存在或不属于用户 | 告知用户提供的UID无效 |

## 报告模板

### 查询状态响应

```
Sub-Account Details
---
Username:      {login_name}
UID:           {user_id}
Status:        {state}
Type:          {type}
Remark:        {remark or "N/A"}
Created:       {create_time}
```

### 列出所有子账户响应

```
Your Sub-Accounts
---
| # | Username | UID | Status | Remark |
|---|----------|-----|--------|--------|
| 1 | {login_name} | {user_id} | {state} | {remark or "-"} |
| 2 | ... | ... | ... | ... |

Total: {count} sub-account(s)
```

### 创建子账户响应

```
Sub-Account Created Successfully
---
Username:      {login_name}
UID:           {user_id}
Status:        Normal
Remark:        {remark or "N/A"}

Note: Only normal sub-accounts can be created through this interface.
```

### 锁定/解锁响应

```
Sub-Account {Action} Successfully
---
Username:      {login_name}
UID:           {user_id}
Previous Status: {previous_state}
Current Status:  {new_state}
```

## 相关领域知识

- Gate上的主账户可以创建多个子账户，用于资产隔离、策略分离或团队管理。
- 子账户共享主账户的KYC验证信息，但具有独立的交易和钱包功能。
- 锁定子账户会禁用登录和交易功能；资产仍然安全，但在解锁前无法访问。
- 子账户有两种类型：普通（type=0）和池（type=1）。此技能仅支持创建普通子账户。
- 创建子账户需要提供唯一的用户名。电子邮件和备注是可选的。

## 安全规则

- **写入操作**（`cex_sa_create_sa`、`cex_sa_lock_sa`、`cex_sa_unlock_sa`）：在执行前必须获得用户的明确确认，严禁自动执行。
- **UID验证**：在锁定/解锁操作前，始终验证子账户是否存在并且属于当前主账户。
- **状态检查**：在锁定/解锁操作前，检查子账户的当前状态以避免重复操作。
- **不暴露敏感数据**：严禁泄露API密钥、内部端点URL或原始错误日志。
- **仅限创建普通子账户**：只能创建普通子账户（type=0），禁止尝试创建池类型子账户。

## 错误处理

| 条件 | 响应 |
|-----------|----------|
| 身份验证端点返回“未登录” | “请先登录您的Gate账户。” |
| 用户不是主账户 | “子账户管理需要主账户权限。请切换到主账户。” |
- 未找到子账户UID | “未找到UID为{user_id}的子账户。请检查UID并重试。” |
- 子账户不属于用户 | “该子账户不属于您的主账户。” |
- 子账户已经被锁定 | “子账户{user_id}已经被锁定。无需操作。” |
- 子账户已经解锁 | “子账户{user_id}已经处于正常（解锁）状态。无需操作。” |
- 创建子账户失败（达到上限） | “您已达到子账户的最大数量。如需更多子账户，请联系支持。” |
- 创建子账户失败（用户名重复） | “用户名‘{login_name}’已被占用。请选择其他名称。” |
- 未知错误 | “处理请求时发生错误。请稍后再试。” |

## 提示示例与场景

请参阅 [scenarios.md](references/scenarios.md) 以获取完整的提示示例和预期行为。