---
name: power-automate-mcp
description: 通过 FlowStudio MCP 服务器连接到并操作 Power Automate 云流程。在需要执行以下操作时使用该工具：列出流程、读取流程定义、查看运行历史记录、检查操作输出、重新提交流程运行请求、取消正在运行的流程、查看连接信息、获取触发器 URL、验证流程定义、监控流程状态，或任何需要通过 MCP 工具与 Power Automate API 进行交互的任务。此外，该工具还用于 Power Platform 环境的发现和连接管理。使用该工具需要具备 FlowStudio MCP 的订阅权限或兼容的服务器——详情请参见：https://mcp.flowstudio.app
  Connect to and operate Power Automate cloud flows via a FlowStudio MCP server.
  Use when asked to: list flows, read a flow definition, check run history, inspect
  action outputs, resubmit a run, cancel a running flow, view connections, get a
  trigger URL, validate a definition, monitor flow health, or any task that requires
  talking to the Power Automate API through an MCP tool. Also use for Power Platform
  environment discovery and connection management. Requires a FlowStudio MCP
  subscription or compatible server — see https://mcp.flowstudio.app
metadata:
  openclaw:
    requires:
      env:
        - FLOWSTUDIO_MCP_TOKEN
    primaryEnv: FLOWSTUDIO_MCP_TOKEN
    homepage: https://mcp.flowstudio.app
---
# 通过 FlowStudio MCP 使用 Power Automate

此技能允许 AI 代理通过 **FlowStudio MCP 服务器** 以编程方式读取、监控和操作 Microsoft Power Automate 的云流程——无需浏览器、无需用户界面，也无需手动步骤。

> **要求：** 需要 [FlowStudio](https://mcp.flowstudio.app) 的 MCP 订阅（或兼容的 Power Automate MCP 服务器）。您需要以下信息：
> - MCP 端点：`https://mcp.flowstudio.app/mcp`（所有订阅者相同）
> - API 密钥 / JWT 令牌（`x-api-key` 头部字段——**非 Bearer 方式**）
> - Power Platform 环境名称（例如 `Default-<tenant-guid>`）

---

## 信息来源

| 优先级 | 来源 | 涵盖内容 |
|----------|--------|--------|
| 1 | **真实的 API 响应** | 始终信任服务器实际返回的内容 |
| 2 | **`tools/list`** | 工具名称、参数名称、类型、必需的标志 |
| 3 | **技能文档和参考文件** | 响应格式、行为说明、工作流示例 |

> **每次开始新会话时，请使用 `tools/list`。**  
> 它会返回每个工具的权威、最新的信息：参数名称、类型和必需的标志。技能文档会补充 `tools/list` 无法提供的内容：
> 响应格式、不明显的行为以及端到端的工作流模式。

>
> 如果任何文档与 `tools/list` 或真实的 API 响应不一致，
> 以 API 的内容为准。

---

## 推荐语言：Python 或 Node.js

本技能及配套的构建/调试技能中的所有示例都使用 **Python** 和 `urllib.request`（标准库，无需安装 `pip`）。**Node.js** 也是一个不错的选择：从 Node 18.0 开始，`fetch` 是内置的，JSON 处理是原生的，异步/等待（async/await）模型与 MCP 工具调用的请求-响应模式非常匹配——非常适合已经在使用 JavaScript/TypeScript 的团队。

| 语言 | 推荐程度 | 备注 |
|---|---|---|
| **Python** | ✅ 推荐 | JSON 处理简单，无需转义；所有技能示例都使用 Python |
| **Node.js (≥ 18)** | ✅ 推荐 | 内置的 `fetch` + `JSON.stringify`/`JSON.parse`；异步/等待模型与 MCP 调用模式匹配良好；无需额外包 |
| PowerShell | ⚠️ 不建议用于流程操作 | `ConvertTo-Json -Depth` 会默默地截断嵌套定义；引用和转义会破坏复杂的负载数据。适用于快速查询 `tools/list`，但不适合构建或更新流程 |
| cURL / Bash | ⚠️ 可行但易出错 | Shell 对嵌套 JSON 的转义容易出错；没有原生的 JSON 解析器 |

> **总结：** 使用下面的核心 MCP 辅助工具（Python 或 Node.js）。这两种语言都能处理 JSON-RPC 框架、身份验证和响应解析。

---

## 您可以做什么

FlowStudio MCP 有两个访问层级。**FlowStudio for Teams** 订阅者可以访问快速的 Azure 表格存储（缓存的数据快照 + 管理元数据）以及完整的 Power Automate API 访问权限。**仅限 MCP 订阅者** 可以使用实时工具——这些工具足以用于构建、调试和操作流程。

### 实时工具——所有 MCP 订阅者均可使用

| 工具 | 功能 |
|---|---|
| `list_live_flows` | 直接通过 PA API 列出环境中的流程（数据始终是最新的） |
| `list_live_environments` | 列出服务账户可见的所有 Power Platform 环境 |
| `list_live_connections` | 通过 PA API 列出环境中的所有连接 |
| `get_live_flow` | 获取完整的流程定义（触发器、动作、参数） |
| `get_live_flow_http_schema` | 检查 HTTP 触发流程的 JSON 正文格式和响应格式 |
| `get_live_flow_trigger_url` | 获取 HTTP 触发流程的当前签名回调 URL |
| `trigger_live_flow` | 向 HTTP 触发流程的回调 URL 发送 POST 请求（AAD 身份验证自动处理） |
| `update_live_flow` | 一次调用即可创建新流程或修改现有流程的定义 |
| `add_live_flow_to_solution` | 将非解决方案流程迁移到解决方案中 |
| `get_live_flow_runs` | 列出最近的运行历史记录，包括状态、开始/结束时间和错误信息 |
| `get_live_flow_run_error` | 获取失败运行的结构化错误详情（按动作分类） |
| `get_live_flow_run_action_outputs` | 检查运行中任何动作（或每个 foreach 循环）的输入/输出 |
| `resubmit_live_flow_run` | 使用原始的触发负载重新运行失败的或已取消的运行 |
| `cancel_live_flow_run` | 取消当前正在运行的流程 |

### 存储工具——仅限 FlowStudio for Teams 订阅者使用

这些工具可以从 FlowStudio Azure 表格中读取数据（并写入数据）——该表格包含您的租户流程的缓存快照，以及丰富的管理元数据和运行统计信息。

| 工具 | 功能 |
|---|---|
| `list_store_flows` | 根据管理标志、运行失败率和所有者元数据从缓存中搜索流程 |
| `get_store_flow` | 获取单个流程的完整缓存详细信息，包括运行统计和管理字段 |
| `get_store_flow_trigger_url` | 从缓存中获取触发 URL（即时获取，无需调用 PA API） |
| `get_store_flow_runs` | 获取过去 N 天的缓存运行历史记录，包括运行时长和修复建议 |
| `get_store_flow_errors` | 获取仅包含失败记录的缓存数据，包括失败动作名称和修复建议 |
| `get_store_flow_summary` | 统计信息：成功率、失败次数、平均/最长运行时间 |
| `set_store_flow_state` | 通过 PA API 启动或停止流程，并将结果同步回存储 |
| `update_store_flow` | 更新管理元数据（描述、标签、监控标志、通知规则、业务影响） |
| `list_store_environments` | 从缓存中列出所有环境 |
| `list_store_makers` | 从缓存中列出所有创建者（普通开发者） |
| `get_store_maker` | 获取创建者的流程/应用数量和账户状态 |
| `list_store_power_apps` | 从缓存中列出所有 Power Apps 画布应用 |
| `list_store_connections` | 从缓存中列出所有 Power Platform 连接 |

---

## 应先调用哪个工具层级

| 任务 | 工具 | 备注 |
|---|---|---|
| 列出流程 | `list_live_flows` | 数据始终是最新的——直接调用 PA API |
| 读取流程定义 | `get_live_flow` | 数据直接从实时获取——不进行缓存 |
| 调试失败 | `get_live_flow_runs` → `get_live_flow_run_error` | 使用实时运行数据 |

> ⚠️ **`list_live_flows` 返回一个包含 `flows` 数组的包装对象**——通过 `result["flows"]` 访问这些数据。

> 存储工具（`list_store_flows`、`get_store_flow` 等）仅对 **FlowStudio for Teams** 订阅者可用，并提供缓存的管理元数据。在不确定时，请使用实时工具——它们适用于所有订阅层级。

---

## 第一步——发现可用工具

始终首先调用 `tools/list` 以确认服务器是否可访问，并查看可用的工具名称（工具名称可能因服务器版本而异）：

```python
import json, urllib.request

TOKEN = "<YOUR_JWT_TOKEN>"
MCP   = "https://mcp.flowstudio.app/mcp"

def mcp_raw(method, params=None, cid=1):
    payload = {"jsonrpc": "2.0", "method": method, "id": cid}
    if params:
        payload["params"] = params
    req = urllib.request.Request(MCP, data=json.dumps(payload).encode(),
        headers={"x-api-key": TOKEN, "Content-Type": "application/json",
                 "User-Agent": "FlowStudio-MCP/1.0"})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"MCP HTTP {e.code} — check token and endpoint") from e
    return json.loads(resp.read())

raw = mcp_raw("tools/list")
if "error" in raw:
    print("ERROR:", raw["error"]); raise SystemExit(1)
for t in raw["result"]["tools"]:
    print(t["name"], "—", t["description"][:60])
```

---

## 核心 MCP 辅助工具（Python）

在后续的所有操作中都使用此辅助工具：

```python
import json, urllib.request

TOKEN = "<YOUR_JWT_TOKEN>"
MCP   = "https://mcp.flowstudio.app/mcp"

def mcp(tool, args, cid=1):
    payload = {"jsonrpc": "2.0", "method": "tools/call", "id": cid,
               "params": {"name": tool, "arguments": args}}
    req = urllib.request.Request(MCP, data=json.dumps(payload).encode(),
        headers={"x-api-key": TOKEN, "Content-Type": "application/json",
                 "User-Agent": "FlowStudio-MCP/1.0"})
    try:
        resp = urllib.request.urlopen(req, timeout=120)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"MCP HTTP {e.code}: {body[:200]}") from e
    raw = json.loads(resp.read())
    if "error" in raw:
        raise RuntimeError(f"MCP error: {json.dumps(raw['error'])}")
    text = raw["result"]["content"][0]["text"]
    return json.loads(text)
```

> **常见的身份验证错误：**
> - HTTP 401/403 → 令牌缺失、过期或格式不正确。请从 [mcp.flowstudio.app](https://mcp.flowstudio.app) 获取新的 JWT。
> - HTTP 400 → JSON-RPC 负载数据格式不正确。检查 `Content-Type: application/json` 和数据结构。
> - `MCP 错误: {"code": -32602, ...}` → 工具参数错误或缺失。

---

## 核心 MCP 辅助工具（Node.js）

适用于 Node.js 18.0 及更高版本（内置 `fetch`——无需额外包）：

```js
const TOKEN = "<YOUR_JWT_TOKEN>";
const MCP   = "https://mcp.flowstudio.app/mcp";

async function mcp(tool, args, cid = 1) {
  const payload = {
    jsonrpc: "2.0",
    method: "tools/call",
    id: cid,
    params: { name: tool, arguments: args },
  };
  const res = await fetch(MCP, {
    method: "POST",
    headers: {
      "x-api-key": TOKEN,
      "Content-Type": "application/json",
      "User-Agent": "FlowStudio-MCP/1.0",
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`MCP HTTP ${res.status}: ${body.slice(0, 200)}`);
  }
  const raw = await res.json();
  if (raw.error) throw new Error(`MCP error: ${JSON.stringify(raw.error)}`);
  return JSON.parse(raw.result.content[0].text);
}
```

> 需要 Node.js 18.0 或更高版本。对于较旧的 Node.js 版本，请使用标准库中的 `https.request` 或安装 `node-fetch`。

---

## 列出流程

```python
ENV = "Default-<tenant-guid>"

result = mcp("list_live_flows", {"environmentName": ENV})
# Returns wrapper object:
# {"mode": "owner", "flows": [{"id": "0757041a-...", "displayName": "My Flow",
#   "state": "Started", "triggerType": "Request", ...}], "totalCount": 42, "error": null}
for f in result["flows"]:
    FLOW_ID = f["id"]   # plain UUID — use directly as flowName
    print(FLOW_ID, "|", f["displayName"], "|", f["state"])
```

---

## 读取流程定义

```python
FLOW = "<flow-uuid>"

flow = mcp("get_live_flow", {"environmentName": ENV, "flowName": FLOW})

# Display name and state
print(flow["properties"]["displayName"])
print(flow["properties"]["state"])

# List all action names
actions = flow["properties"]["definition"]["actions"]
print("Actions:", list(actions.keys()))

# Inspect one action's expression
print(actions["Compose_Filter"]["inputs"])
```

---

## 查看运行历史

```python
# Most recent runs (newest first)
runs = mcp("get_live_flow_runs", {"environmentName": ENV, "flowName": FLOW, "top": 5})
# Returns direct array:
# [{"name": "08584296068667933411438594643CU15",
#   "status": "Failed",
#   "startTime": "2026-02-25T06:13:38.6910688Z",
#   "endTime": "2026-02-25T06:15:24.1995008Z",
#   "triggerName": "manual",
#   "error": {"code": "ActionFailed", "message": "An action failed..."}},
#  {"name": "08584296028664130474944675379CU26",
#   "status": "Succeeded", "error": null, ...}]

for r in runs:
    print(r["name"], r["status"])

# Get the name of the first failed run
run_id = next((r["name"] for r in runs if r["status"] == "Failed"), None)
```

---

## 检查动作的输出

```python
run_id = runs[0]["name"]

out = mcp("get_live_flow_run_action_outputs", {
    "environmentName": ENV,
    "flowName": FLOW,
    "runName": run_id,
    "actionName": "Get_Customer_Record"   # exact action name from the definition
})
print(json.dumps(out, indent=2))
```

---

## 获取运行的错误信息

```python
err = mcp("get_live_flow_run_error", {
    "environmentName": ENV,
    "flowName": FLOW,
    "runName": run_id
})
# Returns:
# {"runName": "08584296068...",
#  "failedActions": [
#    {"actionName": "HTTP_find_AD_User_by_Name", "status": "Failed",
#     "code": "NotSpecified", "startTime": "...", "endTime": "..."},
#    {"actionName": "Scope_prepare_workers", "status": "Failed",
#     "error": {"code": "ActionFailed", "message": "An action failed..."}}
#  ],
#  "allActions": [
#    {"actionName": "Apply_to_each", "status": "Skipped"},
#    {"actionName": "Compose_WeekEnd", "status": "Succeeded"},
#    ...
#  ]}

# The ROOT cause is usually the deepest entry in failedActions:
root = err["failedActions"][-1]
print(f"Root failure: {root['actionName']} → {root['code']}")
```

---

## 重新运行运行

```python
result = mcp("resubmit_live_flow_run", {
    "environmentName": ENV,
    "flowName": FLOW,
    "runName": run_id
})
print(result)   # {"resubmitted": true, "triggerName": "..."}
```

---

## 取消正在运行的流程

```python
mcp("cancel_live_flow_run", {
    "environmentName": ENV,
    "flowName": FLOW,
    "runName": run_id
})
```

> ⚠️ **不要取消显示为 “Running” 的运行**，因为这表示流程正在等待 Teams 中的人工响应。此状态是正常的——流程暂停以等待人工响应。取消该运行将会丢弃待处理的卡片。

---

## 完整的示例——调试和修复失败的流程

```python
# ── 1. Find the flow ─────────────────────────────────────────────────────
result = mcp("list_live_flows", {"environmentName": ENV})
target = next(f for f in result["flows"] if "My Flow Name" in f["displayName"])
FLOW_ID = target["id"]

# ── 2. Get the most recent failed run ────────────────────────────────────
runs = mcp("get_live_flow_runs", {"environmentName": ENV, "flowName": FLOW_ID, "top": 5})
# [{"name": "08584296068...", "status": "Failed", ...}, ...]
RUN_ID = next(r["name"] for r in runs if r["status"] == "Failed")

# ── 3. Get per-action failure breakdown ──────────────────────────────────
err = mcp("get_live_flow_run_error", {"environmentName": ENV, "flowName": FLOW_ID, "runName": RUN_ID})
# {"failedActions": [{"actionName": "HTTP_find_AD_User_by_Name", "code": "NotSpecified",...}], ...}
root_action = err["failedActions"][-1]["actionName"]
print(f"Root failure: {root_action}")

# ── 4. Read the definition and inspect the failing action's expression ───
defn = mcp("get_live_flow", {"environmentName": ENV, "flowName": FLOW_ID})
acts = defn["properties"]["definition"]["actions"]
print("Failing action inputs:", acts[root_action]["inputs"])

# ── 5. Inspect the prior action's output to find the null ────────────────
out = mcp("get_live_flow_run_action_outputs", {
    "environmentName": ENV, "flowName": FLOW_ID,
    "runName": RUN_ID, "actionName": "Compose_Names"
})
nulls = [x for x in out.get("body", []) if x.get("Name") is None]
print(f"{len(nulls)} records with null Name")

# ── 6. Apply the fix ─────────────────────────────────────────────────────
acts[root_action]["inputs"]["parameters"]["searchName"] = \
    "@coalesce(item()?['Name'], '')"

conn_refs = defn["properties"]["connectionReferences"]
result = mcp("update_live_flow", {
    "environmentName": ENV, "flowName": FLOW_ID,
    "definition": defn["properties"]["definition"],
    "connectionReferences": conn_refs
})
assert result.get("error") is None, f"Deploy failed: {result['error']}"
# ⚠️ error key is always present — only fail if it is NOT None

# ── 7. Resubmit and verify ───────────────────────────────────────────────
mcp("resubmit_live_flow_run", {"environmentName": ENV, "flowName": FLOW_ID, "runName": RUN_ID})

import time; time.sleep(30)
new_runs = mcp("get_live_flow_runs", {"environmentName": ENV, "flowName": FLOW_ID, "top": 1})
print(new_runs[0]["status"])   # Succeeded = done
```

---

## 身份验证和连接注意事项

| 字段 | 值 |
|---|---|
| 身份验证头部 | `x-api-key: <JWT>` — **不要** 使用 `Authorization: Bearer` |
| 令牌格式 | 纯 JSON JWT — 不要删除、修改或添加前缀 |
| 超时 | 对于 `get_live_flow_run_action_outputs`（输出较大时），请设置超时时间 ≥ 120 秒 |
| 环境名称 | `Default-<tenant-guid>`（通过 `list_live_environments` 或 `list_live_flows` 的响应获取） |

---

## 参考文件

- [MCP-BOOTSTRAP.md](references/MCP-BOOTSTRAP.md) — 端点、身份验证、请求/响应格式（请先阅读此文件）
- [tool-reference.md](references/tool-reference.md) — 响应格式和行为说明（参数信息在 `tools/list` 中）
- [action-types.md](references/action-types.md) — Power Automate 动作类型模式 |
- [connection-references.md](references/connection-references.md) — 连接器参考指南

---

## 更多功能

- **用于端到端诊断失败流程**：请使用 `power-automate-debug` 技能。
- **用于构建和部署新流程**：请使用 `power-automate-build` 技能。