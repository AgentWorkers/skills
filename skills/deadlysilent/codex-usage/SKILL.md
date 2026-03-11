---
name: codex-usage
description: 用于查询Codex配置文件状态和使用情况的Telegram命令（采用斜杠分隔的格式）。当用户发送 `/codex_usage`、`/codex_usage default`、`/codex_usage all` 或 `/codex_usage <profile>` 时，或请求检查 openai-codex 的配置文件使用情况、限制或运行状态时，可使用此命令。
---
运行 `scripts/codex_usage.py` 以生成从本地认证配置文件中提取的 Codex 配置报告。

## 安全默认设置
- `/codex_usage` 为只读模式。
- 对任何配置更改操作，都需要用户明确确认，并建议先使用 `--dry-run` 选项进行测试。
- 有关允许或禁止的操作范围，请参阅 `RISK.md` 文件。

## 用户体验要求（跨渠道）
在用户触发 `/codex_usage` 请求并运行脚本之前，应立即发送一条进度通知：
- “正在执行 Codex 使用情况检查……”

完成检查后，再发送最终的使用结果（请不要省略进度通知）。

### 用户交互界面
- 如果支持内联按钮：显示选择按钮（默认选项：/ 所有配置文件 / 被发现的配置文件）。
- 如果不支持内联按钮：显示文本菜单作为替代方案（选项：/ 所有配置文件 | <配置文件>）。
- 为每个用户实施重复请求限制机制（约 20 秒内禁止多次请求），以防止意外发送重复请求。

## 命令参数
- `/codex_usage` → **必须** 首先显示选择按钮（默认选项：/ 所有配置文件 / 被发现的配置文件）
- `/codex_usage default`
- `/codex_usage all`
- `/codex_usage <配置文件>`
- `/codex_usage delete <配置文件>`（执行任何更改操作前需要用户明确确认）

## 运行方式
在 workspace 的根目录下运行脚本：

```bash
python3 skills/codex-usage/scripts/codex_usage.py --profile all --timeout-sec 25 --retries 1 --debug
python3 skills/codex-usage/scripts/codex_usage.py --profile all --format text
```

### 针对特定配置文件的示例：

```bash
python3 skills/codex-usage/scripts/codex_usage.py --profile default --timeout-sec 25 --retries 1 --debug
python3 skills/codex-usage/scripts/codex_usage.py --profile openai-codex:default --timeout-sec 25 --retries 1 --debug
python3 skills/codex-usage/scripts/codex_usage.py --profile <suffix> --timeout-sec 25 --retries 1 --debug
```

### 删除配置文件的示例（包含安全防护机制）：

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

## 安全策略
- 该脚本不允许执行远程 shell 命令（如 `curl|bash`、`wget|sh`）。
- 该脚本不会执行 `sudo` 操作、SSH 连接或系统服务相关的配置更改。
- 网络请求仅限于受信任的 Codex 使用端点主机列表（当前为 `chatgpt.com`，通过 HTTPS 协议）。
- 严禁打印完整的令牌信息；请将回调/令牌数据视为敏感信息。

## 其他注意事项
- 该脚本默认从 `~/.openclaw/agents/main/agent/auth-profiles.json` 文件中读取 OAuth 凭据（可通过 `--auth-path` 参数进行自定义）。
- 使用的 Codex 使用端点为：`https://chatgpt.com/backend-api/wham/usage`。
- 该端点仅允许来自受信任的 HTTPS 主机的请求（当前为 `chatgpt.com`）。
- 如果端点无法访问，脚本会返回本地配置文件的运行状态信息（而不会崩溃）。
- 如果端点返回 `401` 错误码，脚本会报告 “auth_not_accepted_by_usage_endpoint”，并继续显示本地配置文件的运行状态信息。
- `401` 错误通常表示端点不接受当前的 OAuth/会话令牌格式（而非 Codex CLI 未安装的问题）。
- 脚本会自动添加 Codex 使用端点所需的请求头信息：`Authorization`、`ChatGPT-Account-Id`（如果存在的话）以及 `User-Agent: CodexBar`。
- 脚本会报告本地配置文件的运行状态（有效期、最后一次使用时间、错误/速率限制统计信息），以及远程端点的使用情况（5 小时/周内的使用次数、达到使用限制的情况）。
- 报告格式符合用户友好原则（例如：`reset_in`、`reset_at` 以本地时区显示重置时间）。
- 支持重试、超时机制以及用于诊断的调试信息（如尝试次数、耗时等）。
- 报告内容包含三个主要字段：`summary`、`formatted_profiles` 和 `suggested_user_message`，以简化命令行输出的格式。
- 优先使用基于换行的输出格式（不使用 `|` 作为分隔符）：
  - `Profile: %name%`
  - `Usable: ✅/❌`
  - `Limited: ✅/❌`
  - `5h Left: %remaining left`
  - `5h Reset: dd/mm/yyyy, hh:mm`
  - `5h Time left: x Days, y Hours, z Minutes`
  - `Week Left: %remaining left`
  - `Week Reset: dd/mm/yyyy, hh:mm`
  - 每个配置文件的输出内容之间使用空行分隔。

---