---
name: power-automate-debug
description: 使用 FlowStudio MCP 服务器来调试失败的 Power Automate 云流程。在需要以下操作时，请加载此技能：调试流程、调查流程失败的原因、检查流程输出结果、找出流程错误的根本原因、修复有问题的 Power Automate 流程、诊断超时问题、追踪 DynamicOperationRequestFailure 错误、检查连接器身份验证错误、读取流程的错误详细信息，或排查表达式故障。此功能需要 FlowStudio MCP 订阅权限——详情请参阅：https://mcp.flowstudio.app
  Debug failing Power Automate cloud flows using the FlowStudio MCP server.
  Load this skill when asked to: debug a flow, investigate a failed run, why is
  this flow failing, inspect action outputs, find the root cause of a flow error,
  fix a broken Power Automate flow, diagnose a timeout, trace a DynamicOperationRequestFailure,
  check connector auth errors, read error details from a run, or troubleshoot
  expression failures. Requires a FlowStudio MCP subscription — see https://mcp.flowstudio.app
metadata:
  openclaw:
    requires:
      env:
        - FLOWSTUDIO_MCP_TOKEN
    primaryEnv: FLOWSTUDIO_MCP_TOKEN
    homepage: https://mcp.flowstudio.app
---
# 使用 FlowStudio MCP 进行 Power Automate 调试

这是一个逐步诊断流程，用于通过 FlowStudio MCP 服务器调查失败的 Power Automate 流程。

**先决条件**：必须能够使用有效的 JWT 访问 FlowStudio MCP 服务器。有关连接设置，请参阅 `power-automate-mcp` 技能。  
在 [https://mcp.flowstudio.app](https://mcp.flowstudio.app) 订阅该服务。

---

## 信息来源

> **始终先调用 `tools/list`** 以确认可用的工具名称及其参数格式。工具名称和参数可能会因服务器版本而异。  
> 本文档涵盖了响应格式、行为说明和诊断模式——这些信息 `tools/list` 无法提供。如果本文档与 `tools/list` 的输出或实际 API 响应不一致，以 API 的输出为准。

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

## FlowStudio for Teams：快速诊断（跳过步骤 2–4）

如果您拥有 FlowStudio for Teams 订阅，`get_store_flow_errors` 可以通过一次调用返回每次运行的失败数据（包括操作名称和修复提示），无需逐个查看 API 响应。

```python
# 快速获取失败总结
summary = mcp("get_store_flow_summary", environmentName=ENV, flowName=FLOW_ID)
# 示例输出：{"totalRuns": 100, "failRuns": 10, "failRate": 0.1,
#          "averageDurationSeconds": 29.4, "maxDurationSeconds": 158.9,
#          "firstFailRunRemediation": "<提示或空>"}
print(f"失败率：{summary['failRate']:%}（共 {summary['totalRuns']）次运行")

# 每次运行的错误详情（需要配置活动监控）
errors = mcp("get_store_flow_errors", environmentName=ENV, flowName=FLOW_ID)
if errors:
    for r in errors[:3]:
        print(r["startTime"], "|", r.get("failedActions"), "|", r.get("remediationHint"))
    # 如果错误确认了具体的失败操作，则跳转到步骤 6（应用修复措施）
else:
    # 该流程没有运行级别的详细信息——请使用实时工具（步骤 2–5）
    pass
```

## 完整的流程管理信息

```python
record = mcp("get_store_flow", environmentName=ENV, flowName=FLOW_ID)
# 示例输出：{"displayName": "我的流程", "state": "已启动",
#          "runPeriodTotal": 100, "runPeriodFailRate": 0.1, "runPeriodFails": 10,
#          "runPeriodDurationAverage": 29410.8,   # 单位：毫秒
#          "runError": "{\"code\": \"EACCES\", ...}",  # JSON 字符串，需解析
#          "description": "...", "tier": "高级", "complexity": "{...}"}
if record.get("runError"):
    last_err = json.loads(record["runError"])
    print("上次运行错误：", last_err)
```

---

## 步骤 1 — 定位流程

```python
result = mcp("list_live_flows", environmentName=ENV)
target = next(f for f in result["flows"] if "我的流程名称" in f["displayName"])
FLOW_ID = target["id"]  # 直接使用此 UUID 作为流程名称
print(FLOW_ID)
```

## 步骤 2 — 查找失败的运行

```python
runs = mcp("get_live_flow_runs", environmentName=ENV, flowName=FLOW_ID, top=5)
for r in runs:
    print(r["name"], r["status"], r["startTime"])
RUN_ID = next(r["name"] for r in runs if r["status"] == "Failed")
```

## 步骤 3 — 获取根本原因

```python
err = mcp("get_live_flow_run_error",
    environmentName=ENV, flowName=FLOW_ID, runName=RUN_ID)
# 示例输出：
# {
#   "runName": "08584296068667933411438594643CU15",
#   "failedActions": [
#     {"actionName": "Apply_to_each_prepare_workers", "status": "失败",
#      "error": {"code": "ActionFailed", "message": "某个操作失败..."},
#      "startTime": "...", "endTime": "..."},
#     {"actionName": "HTTP_find_AD_User_by_Name", "status": "失败",
#      "code": "NotSpecified", "startTime": "...", "endTime": "..."},
#   ],
#   "allActions": [
#     {"actionName": "Apply_to_each", "status": "跳过"},
#     {"actionName": "Compose_WeekEnd", "status": "成功"},
#     ...
# ]
# }
# `failedActions` 的顺序是从外到内；根本原因是最后一个条目。
root = err["failedActions"][-1]
print(f"根本原因：{root['actionName']} → 代码：{root.get('code')}")
```

## 步骤 4 — 查看流程定义

```python
defn = mcp("get_live_flow", environmentName=ENV, flowName=FLOW_ID)
actions = defn["properties"]["definition"]["actions"]
print(list(actions.keys()))
```

在定义中找到失败的操作，检查其 `inputs` 表达式以了解它期望接收的数据。

## 步骤 5 — 检查操作输出

对于导致失败的每个操作，检查其运行时的输出：

```python
for action_name in ["Compose_WeekEnd", "HTTP_Get_Data", "Parse_JSON"]:
    result = mcp("get_live_flow_run_action_outputs",
        environmentName=ENV,
        flowName=FLOW_ID,
        runName=RUN_ID, actionName=action_name)
    out = result[0] if result else None
    print(action_name, out.get("status"))
    print(json.dumps(out.get("outputs", {}), indent=2)[:500])
```

> ⚠️ 来自数组处理操作的输出可能非常大。打印前请务必对其进行切片（例如：`[:500]`）。

## 步骤 6 — 确定根本原因

### 表达式错误（例如：`split` 操作处理空值）

如果错误信息中提到 `InvalidTemplate` 或函数名称：
1. 在定义中找到相关操作。
2. 检查该操作读取的上游操作/表达式。
3. 检查上游操作的输出中是否存在空值或缺失的字段。

```python
# 示例：操作使用了 `split(item()?['Name'], ' ')`；
# → 如果源数据中的 `Name` 为空，则会导致错误。
result = mcp("get_live_flow_run_action_outputs", ..., actionName="Compose_Names")
if not result:
    print("Compose_Names 操作没有返回任何输出")
else:
    names = result[0].get("outputs", "").get("body") or []
nulls = [x for x in names if x.get("Name") is None]
print(f"有 {len(nulls)} 条记录的 `Name` 字段为空")
```

### 错误的字段路径

表达式 `triggerBody()?['fieldName']` 返回空值时，说明字段路径错误。
请使用以下命令检查触发器的输出格式：

```python
mcp("get_live_flow_run_action_outputs", ..., actionName="<trigger-action-name>")
```

### 连接/身份验证失败

如果出现 `ConnectionAuthorizationFailed` 错误，说明连接所有者与运行流程的服务账户不匹配。此问题无法通过 API 解决，需要在 PA 设计器中进行修复。

## 步骤 7 — 应用修复措施

**对于表达式/数据问题**：

```python
defn = mcp("get_live_flow", environmentName=ENV, flowName=FLOW_ID)
acts = defn["properties"]["definition"]["actions"]

# 示例：修复可能为空的 `Name` 字段的处理
acts["Compose_Names"]["inputs"] = "@coalesce(item()?['Name'], 'Unknown')"

conn_refs = defn["properties"]["connectionReferences"]
result = mcp("update_live_flow",
    environmentName=ENV,
    flowName=FLOW_ID,
    definition=defn["properties"]["definition"],
    connectionReferences=conn_refs)

print(result.get("error"))  # 如果结果为 `None`，则表示修复成功。
```

> ⚠️ `update_live_flow` 操作总是返回一个 `error` 键。`null`（Python 中的 `None`）表示修复成功。

## 步骤 8 — 验证修复效果

```python
# 重新提交失败的运行
resubmit = mcp("resubmit_live_flow_run",
    environmentName=ENV, flowName=FLOW_ID, runName=RUN_ID)
print(resubmit)

# 等待约 30 秒后检查结果
import time; time.sleep(30)
new_runs = mcp("get_live_flow_runs", environmentName=ENV, flowName=FLOW_ID, top=3)
print(new_runs[0]["status"]  # 如果结果为 `Succeeded`，则表示修复成功
```

### 测试使用 HTTP 触发的流程

对于使用 `Request`（HTTP）触发器的流程，使用 `trigger_live_flow` 而不是 `resubmit_live_flow_run` 来测试自定义数据：

```python
# 首先检查触发器的期望输入格式
schema = mcp("get_live_flow_http_schema",
    environmentName=ENV, flowName=FLOW_ID)
print("预期的输入格式：", schema.get("triggerSchema"))
print("响应格式：", schema.get("responseSchemas"))

# 使用测试数据触发流程
result = mcp("trigger_live_flow",
    environmentName=ENV,
    flowName=FLOW_ID,
    body={"name": "Test User", "value": 42})
print(f"状态：{result['status']}, 输出：{result.get('body')}")
```

> `trigger_live_flow` 会自动处理通过 AAD 进行身份验证的触发器。
> 仅适用于使用 `Request`（HTTP）触发器的流程。

---

## 快速参考：诊断决策树

| 症状 | 首先使用的工具 | 需要检查的内容 |
|---|---|---|
| 流程显示为失败 | `get_live_flow_run_error` | `failedActions` 中的最后一个操作的名称（根本原因） |
| 表达式崩溃 | 在之前的操作上使用 `get_live_flow_run_action_outputs` | 输出结果中的空值/错误类型的字段 |
| 流程从未启动 | `get_live_flow` | 检查 `properties.state` 是否为 “已启动” |
| 操作返回错误数据 | `get_live_flow_run_action_outputs` | 实际输出与预期输出是否一致 |
| 修复后仍然失败 | 重新提交后使用 `get_live_flow_runs` | 新运行的状态字段 |

---

## 参考文件

- [common-errors.md](references/common-errors.md) — 错误代码、可能的原因及修复方法
- [debug-workflow.md](references/debug-workflow.md) — 复杂故障的完整诊断流程

## 相关技能

- `power-automate-mcp` — 核心的连接设置和操作参考
- `power-automate-build` — 构建和部署新流程