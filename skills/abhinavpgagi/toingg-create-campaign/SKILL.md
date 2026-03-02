---
name: toingg-create-campaign
description: End-to-end Toingg ops: create campaigns, (optionally) schedule daily analytics pulls, and turn Excel contact sheets into WhatsApp outreach via add_contacts + send_whatsapp_templates. Use when Codex needs to automate Toingg voice/WhatsApp workflows and requires scripts for campaign POSTs, analytics cron setup, or bulk contact uploads.
---

# Toingg 操作工具包

此工具包汇集了通过 Claw 管理 Toingg 活动所需的所有功能：

- **活动创建**：通过 `create_campaign.py` 实现
- **活动查询**：通过 `fetch_campaigns.py` 查询用户的活跃活动 ID
- **按需拨打电话**：通过 `make_call.py`（在收集了姓名、电话号码和活动信息后执行）
- **可选的分析任务（每日晚上 7 点自动执行）**：由 `get_campaign_analytics.py` 提供
- **联系人上传 + WhatsApp 模板发送**：使用 `xlsx_to_contacts.py`、`add_contacts.py` 和 `send_whatsapp_templates.py` 完成

所有 HTTP 请求均使用 `TOINGG_API_TOKEN` 作为身份验证令牌。

## 设置

1. 在运行这些脚本的每个环境中（包括网关、定时任务程序和终端）导出你的 API 令牌。
   ```bash
   export TOINGG_API_TOKEN="tg_..."
   ```
2. 如果你需要处理 Excel 文件，请一次性安装 Python 相关依赖项：
   ```bash
   pip install openpyxl requests
   ```
3. 根据安全策略，将活动数据（JSON 格式）、分析结果和联系人信息存储在版本控制系统中或共享存储空间中。

## 活动查询工作流程

当用户需要查看活跃活动或在拨打电话前获取活动 ID 时，请使用此流程：

1. 询问用户是否已知活动 ID。如果不知道，可以提供最新的活动列表（默认的分页设置即可，除非用户要求不同的页面数量）。
2. 运行以下命令：
   ```bash
   ./scripts/fetch_campaigns.py --skip 0 --limit 10 --sort -1 > responses/campaigns-$(date +%s).json
   ```
   如果用户需要更详细的页面内容或不同的排序方式，请调整 `--skip/--limit/--sort` 参数。
3. 向用户反馈查询结果，至少包括 `campID`、`name`、`status` 及相关日期，以便用户能够做出明智的选择。
4. 如果后续操作依赖于这些分析结果，请将 JSON 输出内容保存下来。

## 按需拨打电话工作流程

当用户要求拨打电话时，在调用 API 之前，请收集以下信息：

1. **来电者姓名**（在 Toingg 日志中显示的字符串）
2. **国际格式的电话号码**
3. **活动选择**：如果用户未指定活动，可以询问是否需要最新的活动列表，然后使用上述活动查询流程提供选项并确认用户的选择。

确认这些信息后，触发 API 请求：

```bash
./scripts/make_call.py "Recipient Name" +919999999999 64fd3f9...
```

根据产品团队的默认设置，辅助脚本始终会发送以下参数：`asr=AZURE`、`startMessage=true`、`clearMemory=false` 和 `extraParams={}`。将 API 的响应结果（成功或失败）反馈给用户，以便他们了解通话状态。

## 活动创建工作流程

1. 从用户那里收集活动相关信息（如标题、语音内容、语言、脚本、用途、语气、通话后处理方式、通知号码、自动拨号设置等）。
2. 使用 [`references/payload-template.md`](references/payload-template.md) 作为模板，生成活动数据的 JSON 格式。
3. 运行辅助脚本：
   ```bash
   cd skills/toingg-create-campaign
   ./scripts/create_campaign.py payloads/my_campaign.json > responses/create-$(date +%s).json
   ```
4. 将 API 的响应结果（活动 ID、状态或验证错误）返回给用户，并记录在日志中。

## 每日分析任务（每日晚上 7 点自动执行）

仅当用户明确要求时，才提供此功能：

1. 确认用户所需的分析时间表和输出目录。
2. 按照 [`references/analytics-cron.md`](references/analytics-cron.md) 的说明，使用提供的命令片段创建定时任务 `openclaw cron create toingg-analytics-digest ...`。如有需要，请调整路径。
3. 在启用定时任务之前，确认 `TOINGG_API_TOKEN` 能够被网关识别。
4. 定时任务首次执行后，告知用户 JSON 分析结果的存储位置以及如何禁用该任务（使用 `openclaw cron delete ...`）。

`get_campaign_analytics.py` 也可以根据需要手动运行，以获取实时分析数据：
```bash
./scripts/get_campaign_analytics.py > analytics.json
```

## 联人信息上传 + WhatsApp 模板发送

当用户提供 Excel 文件（包含姓名、电话号码和上下文信息）并希望发送 WhatsApp 模板时：

1. **将 Excel 文件转换为 JSON 格式**
   ```bash
   ./scripts/xlsx_to_contacts.py ~/Downloads/leads.xlsx contacts.json
   ```
   请参考 [`references/contact-workflow.md`](references/contact-workflow.md) 以了解具体的列要求及故障排除方法。该脚本会跳过空白行并规范化电话号码。
2. **将联系人信息上传到 Toingg 的联系人列表中**（如果列表不存在，系统会自动创建）：
   ```bash
   ./scripts/add_contacts.py ClawTest contacts.json
   ```
3. **发送 WhatsApp 模板**：
   ```bash
   ./scripts/send_whatsapp_templates.py \
     231565687 \
     bfesfbgf \
     en-US \
     ClawTest \
     --payload template-variables.json
   ```
   - 如果模板不包含变量，请省略 `--payload` 参数（默认值为 `[]`）。
   - 仅当用户明确要求重新联系现有收件人时，才使用 `--resend` 参数。
4. 在 Toingg 中确认消息发送状态，并将任何错误信息反馈给用户（辅助脚本会打印完整的 JSON 响应结果以供日志记录）。

## 文件对照表

| 脚本 | 功能 |
|--------|---------|
| `scripts/create_campaign.py` | 使用任意数据发送 POST 请求到 `/api/v3/create_campaign` |
| `scripts/fetch_campaigns.py` | 使用 GET 请求 `/api/v3/get_campaigns` 快速查询活动列表 |
| `scripts/make_call.py` | 在收集到姓名、电话号码和活动信息后，发送 POST 请求到 `/api/v3/make_call` |
| `scripts/get_campaign_analytics.py` | 使用 GET 请求 `/api/v3/get_campaign_analytics`（适用于定时任务） |
| `scripts/xlsx_to_contacts.py` | 将 Excel 文件转换为 Toingg 的联系人 JSON 格式 |
| `scripts/add_contacts.py` | 通过 `/api/v3/add_contacts` 上传联系人信息 |
| `scripts/send_whatsapp_templates.py` | 触发 `/api/v3/send_whatsapp_templates` 来发送 WhatsApp 模板 |

请保持此工具包的简洁性：当 Toingg 添加新的字段或工作流程时，及时更新相关文档，以便其他操作人员能够遵循相同的操作规范。