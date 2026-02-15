---
name: 4todo
description: 管理来自聊天工具的 4todo（4to.do）任务：捕获任务信息，使用艾森豪威尔矩阵对任务进行优先级排序，重新排列任务顺序，完成任务，并在工作空间之间管理重复出现的任务。
---

# 4todo  
[4to.do] 艾森豪威尔矩阵待办事项列表  

## 目标  
- 使用 `curl` 调用 4todo API (`https://4to.do/api/v0`) 来管理：  
  - 工作区（workspaces）  
  - 待办事项（todos）  
  - 定期重复的任务（recurring todos）  
- 以一种安全的方式存储 API 令牌（避免泄露风险；建议使用 OpenClaw 在每次运行时动态注入令牌；切勿将令牌粘贴到聊天记录、日志或仓库文件中）。  

## 必需的环境变量  
- `FOURTODO_API_TOKEN`：你的 4todo API 令牌（Bearer 令牌）  
- 如果该变量缺失，请让用户通过 OpenClaw 配置来设置它（切勿要求用户在聊天中输入令牌）。  

## 运行时要求  
- `curl` 必须在 `PATH` 中可用（如果代理处于沙箱环境中，也需要在沙箱容器内可用）。  

## 面向用户的输出规则（非常重要）  
- 默认情况下，输出应保持非技术性，重点关注任务的结果，而非实现细节。  
  - 避免提及：`curl`、端点（endpoints）、请求头（headers）、API 机制（API mechanics）、JSON 数据格式（JSON payloads）或配置修改（config patches）。  
  - 仅在调试时或用户明确询问“它是如何工作的？”时才提供技术细节。  
- 默认情况下，不要显示内部 ID：  
    - 除非用户请求，否则不要显示 `ws_...`、`todo_...`、`rec_todo_...` 等内容。  
    - 使用任务的**名称**来引用工作区和任务。  
    - 如果需要区分同名任务，请先询问用户以获取明确的信息，然后提供任务的名称列表；只有在用户要求时才显示 ID。  
  - 对于任务的分类（四个象限），在聊天中使用通俗的语言，例如：“紧急且重要”、“重要（不紧急）”、“紧急（不重要）”、“两者都不是”。  
  - 在内部调用 API 时使用 `IU | IN | NU | NN` 这些缩写；只有当用户首先提及代码或明确要求时才显示代码。  

### 示例（推荐）  
- 工作区（Workspaces）：  
  ```
Your workspaces:
1) Haoya (default)
2) 4todo
3) Echopark
```  
- 待办事项（Todos）：  
  ```
Urgent & important:
1) UK company dissolution
2) Hetzner monthly payment (recurring, monthly)

Important (not urgent):
1) Weekly review (recurring, Fridays)
```  

## 在 OpenClaw 中存储/注入令牌（推荐）  
OpenClaw 只能在代理运行期间注入环境变量（运行结束后会恢复原始环境设置），这有助于保护敏感信息的安全。  
**生产环境推荐做法**：使用托管提供商提供的秘密存储服务，在 Gateway 进程中设置 `FOURTODO_API_TOKEN`，切勿将令牌保存在聊天记录中。  

### 非沙箱环境（非沙箱运行）：使用 `skills.entries`  
编辑 `~/.openclaw/openclaw.json`：  
```json5
{
  skills: {
    entries: {
      "4todo": {
        enabled: true,
        env: {
          FOURTODO_API_TOKEN: "YOUR_4TODO_API_TOKEN"
        }
      }
    }
  }
}
```  

**注意事项**：  
- `skills.entries.<skill>.env` 仅在变量尚未设置时才会被注入。  

### 沙箱环境：使用 `agentsdefaults.sandbox.docker.env`  
当会话处于沙箱环境中时，技能相关的环境变量不会传播到 Docker 容器中。请通过 Docker 环境变量提供令牌：  
```json5
{
  agents: {
    defaults: {
      sandbox: {
        docker: {
          env: {
            FOURTODO_API_TOKEN: "YOUR_4TODO_API_TOKEN"
          }
        }
      }
    }
  }
}
```  

## 请求规范  
- 每个请求都必须包含 `Authorization: Bearer <token>`。  
- 带有 JSON 数据体的请求必须指定 `Content-Type: application/json`。  
- 请求 `/todos` 时需要提供 `workspace` 查询参数。  
- 任务分类使用 `IU | IN | NU | NN` 这些缩写。  

## 工作流程（推荐顺序）  
复制此清单并在执行过程中持续更新：  
```
Task checklist:
- [ ] List workspaces (pick `ws_...`)
- [ ] List todos for that workspace
- [ ] Perform the requested mutation (create / complete / reorder / recurring)
- [ ] Re-fetch to verify the change
```  
1. `GET /workspaces`：选择一个目标工作区（通常为默认工作区）。  
2. `GET /todos?workspace=ws_...`：获取按分类分组的所有待办事项。  
3. 创建新任务：`POST /todos`。  
4. 完成任务：`POST /todos/:id/complete`（该操作是幂等的）。  
5. 重新排序或移动任务：`POST /todos/reorder`。  
6. 管理定期重复的任务：使用 `/recurring-todos` 端点。  

## HTTP 请求示例（使用 `curl`）  
本技能特意使用 `curl`，以确保其在不同操作系统和环境中的兼容性。  
**注意事项**：  
- 仅使用 HTTPS 协议（`https://4to.do/api/v0`）。  
- 始终通过 `FOURTODO_API_TOKEN` 传递令牌（切勿将令牌粘贴到聊天记录中）。  
```bash
curl -sS -H "Authorization: Bearer $FOURTODO_API_TOKEN" -H "Accept: application/json" "https://4to.do/api/v0/workspaces"
curl -sS -H "Authorization: Bearer $FOURTODO_API_TOKEN" -H "Accept: application/json" "https://4to.do/api/v0/todos?workspace=ws_...&show=all"
curl -sS -X POST -H "Authorization: Bearer $FOURTODO_API_TOKEN" -H "Accept: application/json" -H "Content-Type: application/json" --data-raw '{"name":"...","quadrant":"IU","workspace_id":"ws_..."}' "https://4to.do/api/v0/todos"
curl -sS -X POST -H "Authorization: Bearer $FOURTODO_API_TOKEN" -H "Accept: application/json" "https://4to.do/api/v0/todos/todo_.../complete"
curl -sS -X POST -H "Authorization: Bearer $FOURTODO_API_TOKEN" -H "Accept: application/json" -H "Content-Type: application/json" --data-raw '{"moved_todo_id":"todo_...","previous_todo_id":"todo_...","next_todo_id":null,"quadrant":"IN"}' "https://4to.do/api/v0/todos/reorder"
```  

**注意**：如果 `moved_todo_id` 以 `rec_todo_` 开头，API 仅更新该定期重复任务的分类，而不会修改 `previous_todo_id` 或 `next_todo_id`。  

## 常见错误处理（给代理的提示）  
- `401 token_expired`/`invalid_token`：停止重试；请用户重新生成令牌并更新 OpenClaw 配置。  
- `402 WORKSPACE_RESTRICTED`：当前工作区为只读模式；请切换工作区或提示用户升级/解锁权限。  
- `429 rate_limited`：遵守 `Retry-After` 或 `X-RateLimit-*` 的限制，适当延迟后再重试。  
- `400 Invalid quadrant type`：确保任务分类属于 `IU | IN | NU | NN` 中的一个。  

## 参考资料  
- 该技能的完整 API 文档位于：`{baseDir}/references/api_v0.md`