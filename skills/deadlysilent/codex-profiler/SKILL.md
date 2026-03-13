---
name: codex-profiler
description: Maintained Codex operations skill: unified /codex_usage + /codex_auth path. Standalone codex-usage/codex-auth are deprecated.
---

> ✅ **维护路径：** 所有 Codex 配置文件的操作均使用 `codex-profiler` 工具完成。  
> 独立的 `codex-usage` 和 `codex-auth` 工具已被弃用。  

该技能整合了以下两个脚本：  
- `scripts/codex_usage.py`（用于检查代码的使用情况及限制）  
- `scripts/codex_auth.py`（用于处理 OAuth 认证流程及安全应用操作）  

## 安全默认设置  
- 默认情况下，代码使用情况的检查仅限读取操作。  
- 对代码路径的修改需要用户明确确认，并且应先进行模拟测试（dry-run）。  
- 有关允许或禁止的操作范围，请参阅 `RISK.md` 文件。  

## 命令  
### 代码使用情况检查  
- `/codex_usage` → 选择器（默认值：/all/ 或所有已发现的配置文件）  
- `/codex_usage <profile>`  
- `/codex_usage delete <profile>`（需要用户确认；默认仅执行安全分离操作，并会进行备份）  

### OAuth 认证  
- `/codex_auth` → 选择器（配置文件）  
- `/codex_auth <profile>`  
- `/codex_auth finish <profile> <callback_url>`  

## 用户体验要求（跨渠道）  
- 对于 `/codex_usage` 命令，首先会通过单独的消息发送进度提示：  
  “正在执行 Codex 使用情况检查…”  

**消息传递规则：**  
- 如果进度信息通过渠道消息工具发送，最终结果也应通过相同的路径发送（相同的接收方/会话），之后返回 `NO_REPLY`。  
- 避免混合使用消息传递方式（即同时使用工具进度信息和最终回复）。  

**对于排队中的认证操作：**  
- 在重启系统前会发出警告提示：  
  “系统将通过后台任务进行重启，请避免执行耗时较长的操作。”  

### 用户交互方式  
- 如果支持内联按钮，请使用相应的按钮进行操作；  
- 如果不支持内联按钮，则使用文本提示。  
- 对于同一用户，系统会在 20 秒内抑制重复的请求。  
- 严禁在响应中完整显示回调 URL。  

## 运行方式  
```bash
python3 skills/codex-profiler/scripts/codex_usage.py --profile all --timeout-sec 25 --retries 1 --debug
python3 skills/codex-profiler/scripts/codex_usage.py --profile all --format text
python3 skills/codex-profiler/scripts/codex_auth.py start --profile default
python3 skills/codex-profiler/scripts/codex_auth.py finish --profile default --callback-url "http://localhost:1455/auth/callback?code=...&state=..." --queue-apply
python3 skills/codex-profiler/scripts/codex_auth.py status
```  

## 安全性要求  
- 该技能不允许执行远程 shell 命令（如 `curl|bash`、`wget|sh`）。  
- 该技能不包含任何 `sudo`、SSH 或系统级别的主机修改命令。  
- 代码使用情况的检查仅限于受信任的 HTTPS 端点（`chatgpt.com`）。  
- 回调 URL 和相关凭据信息属于敏感数据，严禁完整显示。  

## 多账户管理指南  
- 如需了解如何切换多个 Codex 账户或配置文件、多账户管理策略或备用方案，请参阅：`references/multi-account-rotation.md`。  

- 对于简单的咨询，可使用简短模板；对于复杂的设置或故障排除需求，请使用详细模板。  

## 其他说明  
- 该技能默认使用位于 `~/.openclaw/agents/main/agent/auth-profiles.json` 中的认证配置文件。  
- Codex 代码使用情况检查的 API 地点是 `https://chatgpt.com/backend-api/wham/usage`。  
- 如果检查失败，系统会返回 `401` 错误码，并明确提示“认证未被使用端点接受”，同时仍会返回当前配置文件的运行状态。  
- 使用结果包括以下信息：  
  - `Profile: %name%`  
  - `Usable: ✅/❌`（代码是否可用）  
  - `Limited: ✅/❌`（代码使用是否有限制）  
  - `5h Left: %remaining left`（剩余使用时间）  
  - `5h Reset: dd/mm/yyyy, hh:mm`（重置时间）  
  - `Week Left: %remaining left`（剩余使用周期）  
  - `Week Reset: dd/mm/yyyy, hh:mm`（下周重置时间）  
- 各配置文件的信息之间用空行分隔。  

**OAuth 流程：**  
- 使用 OpenAI 的认证服务；回调请求通过本地端口 1455 发送。  
- 在使用该技能时，无需安装 Codex 的命令行工具（CLI）。