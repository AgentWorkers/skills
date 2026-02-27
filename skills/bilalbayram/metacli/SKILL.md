---
name: meta
description: Meta Marketing CLI（命令行工具）用于处理广告的认证生命周期、Graph API请求、广告活动的创建与更新、数据洞察报告的生成，以及Instagram内容的发布。适用于通过终端命令执行Meta广告或Instagram相关操作的场景，该工具具备严格的事故恢复（fail-closed）机制，确保操作的安全性和稳定性。
homepage: https://github.com/bilalbayram/metacli
metadata: {"clawdbot":{"emoji":"📣","requires":{"bins":["meta"]},"install":[{"id":"go","kind":"go","module":"github.com/bilalbayram/metacli/cmd/meta@latest","bins":["meta"],"label":"Install meta (go)"}]}}
---
# meta

`meta` 命令用于 Meta Marketing API 和 Instagram 工作流程。如果缺少必要的输入或任何命令执行失败，系统会立即停止并显示错误信息。

**安装：**
- `go install github.com/bilalbayram/metacli/cmd/meta@latest`
- `meta --help`

**操作步骤：**
1. 需要人工进行身份验证（必须首先完成此步骤）。
2. 人工创建一个 Meta 应用程序，并提供 `APP_ID` 和 `APP_SECRET`。
3. 人工在 Meta 开发者设置中配置 OAuth 重定向允许列表（`REDIRECT_URI`）。
4. 重定向路径必须指向 AI 主机的回调端点。对于本地 AI 主机，可以使用以下命令：
  - `cloudflared tunnel --url http://127.0.0.1:53682`（或类似地址，确保使用 HTTPS）
  - 设置 `REDIRECT_URI` 为 `https://<tunnel-domain>/oauth/callback`
5. AI 会运行设置流程，但不会自动打开浏览器：
  - `meta auth setup --profile <PROFILE> --app-id <APP_ID> --app-secret <APP_SECRET> --redirect-uri <REDIRECT_URI> --mode both --scope-pack solo_smb --listen 127.0.0.1:53682 --timeout 180s --open-browser=false`
6. 人工在自己的机器上打开返回的 `auth_url`，登录并授予授权。
7. OAuth 重定向会发送到 AI 主机，然后在那里完成令牌交换。
8. 立即验证授权信息：
  - `meta auth validate --profile <PROFILE> --min-ttl 72h`

**常用命令：**
- **模式同步（建议在写入数据前执行）：** `meta schema sync --schema-dir ~/.meta/schema-packs`
- **账户列表：** `meta --profile <PROFILE> insights accounts list --active-only --output table`
- **图谱读取：** `meta --profile <PROFILE> api get act_<AD_ACCOUNT_ID>/campaigns --fields id,name,status --limit 100 --follow-next`
- **活动预测试：** `meta --profile <PROFILE> campaign create --account-id <AD_ACCOUNT_ID> --params "name=<NAME>,objective=OUTCOME_SALES,status=PAUSED" --schema-dir ~/.meta/schema-packs --dry-run`
- **创建活动：** `meta --profile <PROFILE> campaign create --account-id <AD_ACCOUNT_ID> --params "name=<NAME>,objective=OUTCOME_SALES,status=PAUSED" --schema-dir ~/.meta/schema-packs`
- **更新活动预算：** `meta --profile <PROFILE> campaign update --campaign-id <CAMPAIGN_ID> --params "daily_budget=<AMOUNT_IN_MINOR_units>" --confirm-budget-change`
- **运行分析报告：** `meta --profile <PROFILE> insights run --account-id <AD_ACCOUNT_ID> --date-preset last_7d --level campaign --metric-pack quality --format jsonl`
- **发布 Instagram 内容：** `meta --profile <PROFILE> ig publish feed --media-url <HTTPS_MEDIA_URL> --caption "<CAPTION>" --idempotency-key <UNIQUE_KEY>`

**注意事项：**
- **规则：**
  - 严禁自行创建 ID、个人资料名称、路径、重定向 URL 或数据字段。
  - 在修改预算之前，必须获得明确确认。
  - 为了自动化操作，建议使用机器可读的输出格式（`--output json` 或 `--format jsonl`）。
  - 在输出命令结果时，应隐藏敏感信息（如 `APP_SECRET` 和访问令牌）。