---
name: power-automate-build
description: 使用 FlowStudio MCP 服务器来构建、搭建和部署 Power Automate 云工作流。当需要执行以下操作时，请使用此技能：创建新的工作流、部署工作流定义、搭建 Power Automate 工作流程框架、生成工作流 JSON 文件、更新现有工作流的步骤、修改工作流定义、向工作流中添加步骤、连接各个组件，或从头开始生成工作流定义。此功能需要 FlowStudio MCP 的订阅权限——详情请访问：https://mcp.flowstudio.app
  Build, scaffold, and deploy Power Automate cloud flows using the FlowStudio
  MCP server. Load this skill when asked to: create a flow, build a new flow,
  deploy a flow definition, scaffold a Power Automate workflow, construct a flow
  JSON, update an existing flow's actions, patch a flow definition, add actions
  to a flow, wire up connections, or generate a workflow definition from scratch.
  Requires a FlowStudio MCP subscription — see https://mcp.flowstudio.app
metadata:
  openclaw:
    requires:
      env:
        - FLOWSTUDIO_MCP_TOKEN
    primaryEnv: FLOWSTUDIO_MCP_TOKEN
    homepage: https://mcp.flowstudio.app
---
# 使用 FlowStudio MCP 构建和部署 Power Automate 流

本文档提供了通过 FlowStudio MCP 服务器以编程方式构建和部署 Power Automate 云流的逐步指南。

**先决条件**：必须能够使用有效的 JWT 访问 FlowStudio MCP 服务器。有关连接设置，请参阅 `power-automate-mcp` 技能。请在 [https://mcp.flowstudio.app](https://mcp.flowstudio.app) 进行订阅。

---

## 信息来源

> **务必先调用 `tools/list` 以确认可用的工具名称及其参数格式**。工具名称和参数可能因服务器版本而异。本文档涵盖了响应格式、行为说明和构建模式——这些信息无法通过 `tools/list` 获得。如果本文档与 `tools/list` 的输出或实际 API 响应不一致，请以 API 的输出为准。

---

## Python 辅助函数

```python
import json, urllib.request

MCP_URL = "https://mcp.flowstudio.app/mcp"
MCP_TOKEN = "<YOUR_JWT_TOKEN>"

def mcp/tool, **kwargs):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                          "params": {"name": tool, "arguments": kwargs}}).encode()
    req = urllib.request.Request(MCP_URL, data=payload,
        headers={"x-api-key": MCP_TOKEN, "Content-Type": "application/json",
                 "User-Agent": "FlowStudio-MCP/1.0"}
    try:
        resp = urllib.request.urlopen(req, timeout=120)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"MCP HTTP 错误：{e.code}: {body[:200]}")
    raw = json.loads(resp.read())
    if "error" in raw:
        raise RuntimeError(f"MCP 错误：{json.dumps(raw['error'])}")
    return json.loads(raw["result"]["content"][0]["text"]

ENV = "<environment-id>"  # 例如：Default-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

---

## 第 1 步 — 安全检查：该流是否存在？

在构建之前，请先检查以避免重复：

```python
results = mcp("list_store_flows",
    environmentName=ENV, searchTerm="My New Flow")

# list_store_flows 返回一个直接数组（无包装对象）
if len(results) > 0:
    # 流已存在——直接修改而不是创建
    # 流的 ID 格式为 "envId.flowId"——拆分以获取流的唯一标识符（UUID）
    FLOW_ID = results[0]["id"].split(".", 1)[1]
    print(f"现有流：{FLOW_ID}")
    defn = mcp("get_live_flow", environmentName=ENV, flowName=FLOW_ID)
else:
    print("未找到流——从头开始构建")
    FLOW_ID = None
```

---

## 第 2 步 — 获取连接引用

每个连接器操作都需要一个 `connectionName`，该名称指向流中 `connectionReferences` 映射中的一个键。该键关联到环境中的已认证连接。

> **强制要求**：必须先调用 `list_live_connections`——不要询问用户连接名称或 GUID。API 会返回您需要的确切值。只有在 API 确认所需连接缺失时才提示用户输入。

### 2a — 必须先调用 `list_live_connections`

```python
conns = mcp("list_live_connections", environmentName=ENV)

# 仅过滤已连接的（已认证的）连接
active = [c for c in conns["connections"]
          if c["statuses"][0]["status"] == "Connected"]

# 创建连接名称到连接 ID 的映射
conn_map = {}
for c in active:
    conn_map[c["connectorName")] = c["id"]

print(f"找到 {len(active)} 个活动连接")
print("可用的连接器：", list(conn_map.keys()))
```

### 2b — 确定流所需的连接器

根据您要构建的流，确定所需的连接器。常见的连接器 API 名称如下：

| 连接器 | API 名称 |
|---|---|
| SharePoint | `shared_sharepointonline` |
| Outlook / Office 365 | `shared_office365` |
| Teams | `shared_teams` |
| Approvals | `shared_approvals` |
| OneDrive for Business | `shared_onedriveforbusiness` |
| Excel Online (Business) | `shared_excelonlinebusiness` |
| Dataverse | `shared_commondataserviceforapps` |
| Microsoft Forms | `shared_microsoftforms` |

> **不需要任何连接的流**（例如：循环执行 + Compose + 仅使用 HTTP）可以跳过第 2 步的其余部分——在部署调用中省略 `connectionReferences`。

### 2c — 如果缺少连接，请指导用户

```python
connectors_needed = ["shared_sharepointonline", "shared_office365"]  # 根据实际需求调整

missing = [c for c in connectors_needed if c not in conn_map]

if not missing:
    print("✅ 所需连接均已获取——继续构建")
else:
    # ── 停止：必须手动创建连接 ──
    # 连接需要浏览器中的 OAuth 认证——API 无法创建它们。
    print("⚠️ 以下连接器在此环境中没有活动连接：")
    for c in missing:
        friendly = c.replace("shared_", "").replace("onlinebusiness", " Online (Business)")
        print(f"   • {friendly}  (API 名称: {c}")
    print()
    print("请创建缺失的连接：")
    print("  1. 打开 https://make.powerautomate.com/connections")
    print("  2. 从右上角的选择器中选择正确的环境")
    print("  3. 为上述每个缺失的连接器点击 ‘+ New connection’")
    print("  4. 按提示登录并授权")
    print("  5. 完成后告诉我——我将重新检查并继续构建")
    # 在用户确认之前，请勿继续执行第 3 步。
    # 用户确认后，重新运行第 2a 步以更新 conn_map。"
```

### 2d — 构建 `connectionReferences` 块

只有在确认没有缺失连接器后，才执行此步骤：

```python
connection_references = {}
for connector in connectors_needed:
    connection_references[connector] = {
        "connectionName": conn_map[connector],   # 来自 list_live_connections 的 GUID
        "source": "Invoker",
        "id": f"/providers/Microsoft.PowerApps/apis/{connector}"
    }
```

> **重要提示**：在构建第 3 步中的操作时，将 `host.connectionName` 设置为该映射中的 **键**（例如 `shared_teams`），而不是连接 GUID。GUID 仅用于 `connectionReferences` 中。引擎会根据 `host.connectionName` 在映射中找到正确的连接。

> **替代方法**：如果您已经有使用相同连接器的流，可以从其定义中提取 `connectionReferences`：
```python
ref_flow = mcp("get_live_flow", environmentName=ENV, flowName="<existing-flow-id>")
connection_references = ref_flow["properties"]["connectionReferences"]
```

有关完整的连接引用结构，请参阅 `power-automate-mcp` 技能的 `connection-references.md` 文档。

---

## 第 3 步 — 构建流定义

构建定义对象。请参阅 [flow-schema.md](references/flow-schema.md) 以获取完整的架构，并参考以下文档中的操作模式模板：
- [action-patterns-core.md](references/action-patterns-core.md) — 变量、控制流、表达式
- [action-patterns-data.md](references/action-patterns-data.md) — 数组转换、HTTP、解析
- [action-patterns-connectors.md](references/action-patterns-connectors.md) — SharePoint、Outlook、Teams、Approvals

```python
definition = {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "contentVersion": "1.0.0.0",
    "triggers": { ... },   # 请参阅 trigger-types.md / build-patterns.md
    "actions": { ... }     # 请参阅 ACTION-PATTERNS-*.md / build-patterns.md
}
```

> 请参阅 [build-patterns.md](references/build-patterns.md) 以获取完整的、可使用的流定义模板，包括循环执行、SharePoint、Teams 等功能。

---

## 第 4 步 — 部署（创建或更新）

`update_live_flow` 功能可以同时处理创建和更新操作。

### 创建新流（没有现有流）

省略 `flowName`——服务器会生成一个新的 GUID 并通过 PUT 请求创建流：

```python
result = mcp("update_live_flow",
    environmentName=ENV,
    # 省略 flowName → 服务器会生成新的 GUID
    definition=definition,
    connectionReferences=connection_references,
    displayName="Overdue Invoice Notifications",
    description="每周从 SharePoint 发送到 Teams 的通知流，由代理创建")
```

如果 `result.get("error")` 不为空，则表示创建失败：

```python
if result.get("error") is not None:
    print("创建失败:", result["error"])
else:
    # 获取新的流 ID 以供后续步骤使用
    FLOW_ID = result["created"]
    print(f"✅ 流已创建：{FLOW_ID}")
```

### 更新现有流

提供 `flowName` 以执行更新操作：

```python
result = mcp("update_live_flow",
    environmentName=ENV,
    flowName=FLOW_ID,
    definition=definition,
    connectionReferences=connection_references,
    displayName="My Updated Flow",
    description="由代理更新，时间：{__import__('datetime').datetime.utcnow().isoformat()}"
```

> ⚠️ `update_live_flow` 总会返回一个 `error` 键。`null`（Python 中的 `None`）表示成功——不要将键的存在视为失败。
> ⚠️ `description` 对于创建和更新操作都是必需的。

### 常见部署错误

| 错误信息 | 原因 | 解决方法 |
|---|---|---|
| `missing from connectionReferences` | 某个操作的 `host.connectionName` 引用的键在 `connectionReferences` 映射中不存在 | 确保 `host.connectionName` 使用的是 `connectionReferences` 中的键（例如 `shared_teams`），而不是原始 GUID |
| `ConnectionAuthorizationFailed` / 403 | 连接 GUID 属于其他用户或未获得授权 | 重新运行第 2a 步，并使用当前 `x-api-key` 用户拥有的连接 |
| `InvalidTemplate` / `InvalidDefinition` | 定义 JSON 中存在语法错误 | 检查 `runAfter` 链接、表达式语法和操作类型拼写 |
| `ConnectionNotConfigured` | 连接器操作存在，但连接 GUID 无效或已过期 | 重新检查 `list_live_connections` 以获取新的 GUID |

---

## 第 5 步 — 验证部署结果

```python
check = mcp("get_live_flow", environmentName=ENV, flowName=FLOW_ID)

# 确认状态
print("状态：", check["properties"]["state"])  # 应显示 "Started"

# 确认我们添加的操作是否存在
acts = check["properties"]["definition"]["actions"]
print("操作：", list(acts.keys()))
```

---

## 第 6 步 — 测试流

> **强制要求**：在触发任何测试运行之前，**请先获得用户的确认**。运行流会产生实际效果——它可能会发送电子邮件、在 Teams 中发布消息、写入 SharePoint 或调用外部 API。在调用 `trigger_live_flow` 或 `resubmit_live_flow_run` 之前，请解释流的功能并等待用户的明确批准。

### 已更新的流（之前已经运行过）

最快的方法是重新提交最近的运行记录：

```python
runs = mcp("get_live_flow_runs", environmentName=ENV, flowName=FLOW_ID, top=1)
if runs:
    result = mcp("resubmit_live_flow_run",
        environmentName=ENV, flowName=FLOW_ID, runName=runs[0]["name"]
    print(result)
```

### 已使用 HTTP 触发的流

可以直接使用测试数据发送请求来测试流：

```python
schema = mcp("get_live_flow_http_schema", environmentName=ENV, flowName=FLOW_ID)
print("预期的请求体：", schema.get("triggerSchema"))

result = mcp("trigger_live_flow",
    environmentName=ENV, flowName=FLOW_ID,
    body={"name": "Test", "value": 1})
print(f"状态：{result['status']}")
```

### 完全新的非 HTTP 流（循环执行、连接器触发等）

全新的循环执行或连接器触发的流没有之前的运行记录，也无法通过 HTTP 端点进行测试。**首先使用临时 HTTP 触发器进行部署，测试操作，然后再切换到生产触发器。**

#### 7a — 保存生产触发器，并使用临时 HTTP 触发器进行部署

```python
# 保存在步骤 3 中创建的生产触发器
production_trigger = definition["triggers"]

# 替换为临时 HTTP 触发器
definition["triggers"] = {
    "manual": {
        "type": "Request",
        "kind": "Http",
        "inputs": {
            "schema": {}
        }
}

# 使用临时触发器进行部署（创建或更新）
result = mcp("update_live_flow",
    environmentName=ENV,
    flowName=FLOW_ID,       # 如果是新建流则省略此步骤
    definition=definition,
    connectionReferences=connection_references,
    displayName="使用临时 HTTP 触发器部署")
```

如果部署失败：

```python
if result.get("error") is not None:
    print("部署失败:", result["error"])
else:
    if not FLOW_ID:
        FLOW_ID = result["created"]
    print("✅ 使用临时 HTTP 触发器成功部署：{FLOW_ID}")
```

#### 7b — 触发流并检查结果

```python
# 触发流
test = mcp("trigger_live_flow",
    environmentName=ENV, flowName=FLOW_ID)
print(f"触发器状态：{test['status']")

# 等待运行完成
import time; time.sleep(15)

# 检查运行结果
runs = mcp("get_live_flow_runs", environmentName=ENV, flowName=FLOW_ID, top=1)
run = runs[0]
print(f"运行结果：{run['name']": run['status']})

if run["status"] == "Failed":
    err = mcp("get_live_flow_run_error",
        environmentName=ENV, flowName=FLOW_ID, runName=run["name"])
    root = err["failedActions"][-1]
    print(f"根本原因：{root['actionName']} → {root.get('code')}")
    # 在继续之前调试并修复定义
    # 有关详细诊断，请参阅 power-automate-debug 技能

#### 7c — 将临时触发器替换为生产触发器

## 注意事项

| 错误 | 后果 | 预防措施 |
|---|---|---|
| 部署时缺少 `connectionReferences` | 会导致 400 错误 | 必须先调用 `list_live_connections` |
| `Foreach` 中缺少 `operationOptions` | 会导致并行执行和写入时的竞争条件 | 必须添加 `"Sequential"` |
| `union(old_data, new_data)` | 会导致旧值覆盖新值 | 应使用 `union(new_data, old_data)` |
| 在可能为空的字符串上使用 `split()` | 会导致 `InvalidTemplate` 错误 | 应使用 `coalesce(field, '')` 进行处理 |
| 检查 `result["error"]` 是否存在 | `result["error"] 总是存在的；真正的错误是 `result.get("error") is not None` |
| 流已部署但状态显示为 "Stopped" | 流不会按计划运行 | 请检查连接授权并重新启用 |
| 在 Teams 中使用 `PostMessageToConversation` 时，`recipient` 参数格式不正确 | 会导致 400 `GraphUserDetailNotFound` 错误 | 使用带有分号的普通字符串 |

---

## 参考文件

- [flow-schema.md](references/flow-schema.md) — 完整的流定义 JSON 模式
- [trigger-types.md](references/trigger-types.md) — 触发器类型模板
- [action-patterns-core.md](references/action-patterns-core.md) — 变量、控制流、表达式
- [action-patterns-data.md](references/action-patterns-data.md) — 数组转换、HTTP、解析
- [action-patterns-connectors.md](references/action-patterns-connectors.md) — SharePoint、Outlook、Teams、Approvals
- [build-patterns.md](references/build-patterns.md) — 完整的流定义模板（包括循环执行、SharePoint、Teams 等）

## 相关技能

- `power-automate-mcp` — 核心连接设置和工具参考
- `power-automate-debug` — 部署后调试失败的流