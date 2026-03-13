---
name: codex-usage
description: 已弃用的 `/codex_usage` 相关功能（即“shim”功能），请改用 `codex-profiler`；`codex-usage` 已不再得到维护。
---
> ⚠️ **已弃用：** `codex-usage` 已不再作为独立技能进行维护。  
> 请使用 **codex-profiler** 来执行所有与 `/codex_usage` 和 `/codex_auth` 相关的操作。  

运行 `scripts/codex_usage.py` 可以生成从本地身份验证配置文件中提取的 Codex 配置报告。  

## 安全默认设置  
- `/codex_usage` 模式为只读。  
- 对任何配置更改操作，都需要用户明确确认，并建议先使用 `--dry-run` 选项进行测试。  
- 有关允许或禁止的操作范围，请参阅 `RISK.md` 文件。  

## 用户体验要求（跨渠道）  
在用户触发 `/codex_usage` 请求时，首先通过单独的消息发送进度通知：  
- “正在执行 Codex 使用情况检查…”  
完成检查后，再发送最终的使用结果（请不要忽略进度通知）。  

**交付规则：**  
- 如果进度通知是通过渠道消息工具发送的，那么最终结果也应通过相同的渠道消息工具发送（相同的接收方/会话），之后返回 `NO_REPLY` 以避免信息传递不匹配的问题。  
- 不要将进度通知与最终结果通过不同的方式发送（例如：通过工具发送进度通知，通过普通助手回复发送结果）。  

### 用户交互适配器  
- 如果支持内联按钮：显示选择按钮（默认选项：/ 所有配置文件 / 被发现的配置文件）。  
- 如果不支持内联按钮：显示文本菜单作为替代方案（选项：/default | all | <profile>）。  
- 为每个用户设置 20 秒的重复请求限制，以防止意外的大量请求。  

## 命令说明  
- `/codex_usage`：**必须** 首先显示选择按钮（默认选项：/ 所有配置文件 / 被发现的配置文件）。  
- `/codex_usage default`  
- `/codex_usage all`  
- `/codex_usage <profile>`  
- `/codex_usage delete <profile>`（执行任何配置更改前需要用户明确确认）。  

## 运行方式  
从工作区根目录执行：  

```bash
python3 skills/codex-usage/scripts/codex_usage.py --profile all --timeout-sec 25 --retries 1 --debug
python3 skills/codex-usage/scripts/codex_usage.py --profile all --format text
```  

**针对特定配置文件的示例：**  
```bash
python3 skills/codex-usage/scripts/codex_usage.py --profile default --timeout-sec 25 --retries 1 --debug
python3 skills/codex-usage/scripts/codex_usage.py --profile openai-codex:default --timeout-sec 25 --retries 1 --debug
python3 skills/codex-usage/scripts/codex_usage.py --profile <suffix> --timeout-sec 25 --retries 1 --debug
```  

**删除配置文件的示例（包含安全机制）：**  
```bash
# preview only (required guard response without --confirm-delete)
python3 skills/codex-usage/scripts/codex_usage.py --delete-profile openai-codex:mine

# safe preview with explicit confirm but no file mutation
python3 skills/codex-usage/scripts/codex_usage.py --delete-profile openai-codex:mine --confirm-delete --dry-run

# safer default mutation: detach from order/lastGood only (keeps token/profile entry)
python3 skills/codex-usage/scripts/codex_usage.py --delete-profile openai-codex:mine --confirm-delete

# permanent delete: remove profile + usage entries (creates backup first)
python3 skills/codex-usage/scripts/codex_usage.py --delete-profile openai-codex:mine --confirm-delete --hard-delete
```  

## 安全性规定  
- 该技能不允许执行远程 shell 命令（如 `curl|bash`、`wget|sh`）。  
- 该技能不会执行 `sudo` 操作、SSH 连接或系统服务相关的配置更改。  
- 网络请求仅限于受信任的 Codex 使用端点（`chatgpt.com`，通过 HTTPS 协议）。  
- 绝不允许打印完整的 API 令牌；请将回调/令牌信息视为敏感数据。  

## 其他注意事项：  
- 该技能默认从 `~/.openclaw/agents/main/agent/auth-profiles.json` 文件中读取 OAuth 凭据（可通过 `--auth-path` 参数进行覆盖）。  
- 使用的 Codex 使用端点为：`https://chatgpt.com/backend-api/wham/usage`。  
- 该端点仅允许来自受信任的 HTTPS 主机（当前为 `chatgpt.com`）。  
- 如果端点无法访问，脚本会切换为仅显示本地配置文件的运行状态（而不会崩溃）。  
- 如果端点返回 `401` 错误码，脚本会报告 `auth_not_accepted_by_usage_endpoint`，并继续显示本地配置文件的运行状态。  
- `401` 错误通常表示端点不接受当前的 OAuth/会话令牌格式（而非 Codex CLI 未安装）。  
- 脚本会自动添加 Codex 使用端点所需的请求头：`Authorization`、`ChatGPT-Account-Id`（如果存在）以及 `User-Agent: CodexBar`。  
- 报告本地配置文件的运行状态（有效期、最后一次使用时间、错误/速率限制信息），以及远程端点的使用情况（每周 5 小时）。  
- 报告易于理解的格式化信息（如 `reset_in`、`reset_at`，以用户所在时区显示）。  
- 支持重试、超时设置以及用于诊断的调试信息（如尝试次数、耗时、状态等）。  
- 报告结果时包含 `summary`、`formatted_profiles` 和 `suggested_user_message` 等字段，以简化命令行输出的格式。  
- 优先使用基于换行的严格输出格式（不使用 `|` 分隔符）：  
  - `Profile: %name%`  
  - `Usable: ✅/❌`  
  - `Limited: ✅/❌`  
  - `5h Left: %remaining left`  
  - `5h Reset: dd/mm/yyyy, hh:mm`  
  - `5h Time left: x 天，y 小时，z 分钟`  
  - `Week Left: %remaining left`  
  - `Week Reset: dd/mm/yyyy, hh:mm`  
  - `Week Time left: x 天，y 小时，z 分钟`  
- 不同配置文件之间用空行分隔。  
- 绝不允许打印完整的 API 令牌。