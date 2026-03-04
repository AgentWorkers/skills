---

**名称：openclaw-growth-pack**  
**描述：** 将新安装的 OpenClaw 转变为一个可靠的执行代理。适用于用户报告“需要逐步指导”、“任务中途卡住”、“令牌不匹配”或模型路由/认证失败的情况。应用生产环境的基本配置：模型路由、网关令牌一致性、防卡顿机制、轻量级自主检查循环以及验证检查列表。  

---

### OpenClaw Growth Pack  
使用此工具将新的 OpenClaw 实例配置为稳定、能够完成任务的环境。  

按照以下步骤操作：  
1. 确保模型路由与提供者端点一致。  
2. 确保所有运行时环境中的网关令牌值一致。  
3. 在 `AGENTS.md` 和 `HEARTBEAT.md` 中安装防卡顿执行逻辑。  
4. 启用轻量级的定期自我检查功能。  
5. 在确认设置完成之前，运行验证流程。  

请保持更改最小化、可审计且可逆。  

#### 1) 模型路由基线  
在 `~/.openclaw/openclaw.json` 中使用唯一的数据源：  

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "YOUR_CODING_PLAN_KEY"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/qwen3-coder-plus"
      }
    }
  }
}
```  

**规则：**  
- 不要将 `coding-intl.dashscope.aliyuncs.com` 保留在活跃配置中。  
- 除非绝对必要，否则不要在多个文件中重复定义提供者信息。  
- 如果存在 `~/.openclaw/agents/main/agent/models.json`，请删除其中的冲突提供者配置。  

#### 2) 网关令牌一致性  
确保所有令牌值保持一致：  
- `openclaw.json` 中的 `gateway.auth.token`  
- `openclaw.json` 中的 `gateway.remote.token`（如果存在）  
- 仪表板控制界面的令牌值（使用相同的值）  

**PowerShell 审计：**  
```powershell
$cfg = Get-Content "$HOME/.openclaw/openclaw.json" -Raw | ConvertFrom-Json
$auth = $cfg.gateway.auth.token
$remote = $cfg.gateway.remote.token
"auth.token   = $auth"
"remote.token = $remote"
if ($remote -and $auth -ne $remote) { Write-Warning "Token mismatch in openclaw.json" }
```  

**任何令牌更改后：**  
```powershell
openclaw gateway restart
```  

#### 3) 防卡顿机制**  
在 `AGENTS.md` 中编写或更新以下强制性的约束规则：  
- 对每个重要任务输出状态：`Goal`（目标）、`Progress`（进度）、`Next`（下一步）。  
- 除非遇到明确阻碍或用户主动停止，否则不得停止执行。  
- 失败时：重试，然后回退，最后报告最小的解堵输入信息。  
- 多步骤任务完成后，必须提供证据文件路径或命令结果摘要。  

在 `HEARTBEAT.md` 中编写或更新以下内容：  
- 每个周期最多执行 1-2 次检查。  
- 要么生成执行证据，要么返回 `HEARTBEAT_OK`。  
- 如果队列中有任务，执行一个具体步骤，然后将证据日志记录到 `memory/YYYY-MM-DD.md` 中。  

#### 4) 轻量级自主检查循环**  
如果可以使用 cron 或系统事件，创建以下定期任务：  
- 每日：检查未完成的任务。  
- 每周：审查内存使用情况并分析潜在问题。  

如果无法使用 cron，需手动执行相应操作：  
- 每天开始时：查看 `tasks/QUEUE.md`，选择一项可操作的任务。  
- 每天结束时：将一条经验记录添加到 `memory/YYYY-MM-DD.md` 中。  

#### 5) 验证流程（不可跳过）**  
只有满足所有以下条件，才能认为设置完成：  
- 模型调用通过主要路由成功。  
- 网关访问成功且令牌匹配正确。  
- 多步骤任务完成并留下证据。  
- 至少有一个阻碍路径被记录在 `memory/blocked-items.md` 中。  

**推荐的验证证据：**  
- 命令摘要  
- 证据文件路径或 URL  
- 最终状态（`done` 或 `blocked`，并附上所需输入信息）  

#### 6) 回滚机制**  
在编辑之前，请创建备份：  
```powershell
Copy-Item "$HOME/.openclaw/openclaw.json" "$HOME/.openclaw/openclaw.json.bak" -Force
```  

**执行回滚：**  
```powershell
Copy-Item "$HOME/.openclaw/openclaw.json.bak" "$HOME/.openclaw/openclaw.json" -Force
openclaw gateway restart
```  

#### 参考资料**  
有关具体的命令示例和故障排除指南，请参阅：  
- `references/examples.md`