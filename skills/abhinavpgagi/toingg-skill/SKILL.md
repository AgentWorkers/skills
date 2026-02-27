---
name: toingg-skill
description: End-to-end Toingg ops: create campaigns, (optionally) schedule daily analytics pulls, and turn Excel contact sheets into WhatsApp outreach via add_contacts + send_whatsapp_templates. Use when Codex needs to automate Toingg voice/WhatsApp workflows and requires scripts for campaign POSTs, analytics cron setup, or bulk contact uploads.
---

# Toingg 操作工具包

该工具包汇集了通过 Claw 管理 Toingg 活动所需的所有功能：

- **活动创建**：通过 `create_campaign.py` 实现
- **可选的每日分析任务**（晚上 7 点执行），由 `get_campaign_analytics.py` 提供支持
- **联系人上传 + WhatsApp 模板发送**：使用 `xlsx_to_contacts.py`、`add_contacts.py` 和 `send_whatsapp_templates.py` 完成

所有 HTTP 请求均使用 `TOINGG_API_TOKEN` 作为身份验证令牌。

## 设置

1. 在运行这些脚本的每个环境中（网关、定时任务、终端）导出你的 API 令牌。  
   ```bash
   export TOINGG_API_TOKEN="tg_..."
   ```

2. 如果你需要处理 Excel 文件，请一次性安装 Python 相关依赖项：  
   ```bash
   pip install openpyxl requests
   ```

3. 根据你的安全策略，将数据 payload（活动 JSON 数据、分析结果快照、联系人信息）保存在版本控制系统中或共享存储空间中。

## 活动创建流程

1. 从用户处收集活动相关信息（标题、语音内容、语言、脚本、用途、语气、通话后通知方式、自动回复设置等）。
2. 使用 [`references/payload-template.md`](references/payload-template.md) 作为模板，起草活动数据的 JSON 格式。
3. 运行相关辅助脚本：  
   ```bash
   cd skills/toingg-skill
   ./scripts/create_campaign.py payloads/my_campaign.json > responses/create-$(date +%s).json
   ```
4. 将 API 的响应（活动 ID、状态或验证错误）返回给用户，并记录日志。

## 每日分析任务（晚上 7 点执行）

仅当用户明确要求时才提供此功能。

1. 确认所需的调度时间和输出目录。
2. 遵循 [`references/analytics-cron.md`](references/analytics-cron.md) 的说明，使用提供的命令片段创建定时任务 `openclaw cron create toingg-analytics-digest ...`。如有需要，请调整路径。
3. 在启用定时任务之前，确保网关能够访问 `TOINGG_API_TOKEN`。
4. 定时任务首次执行后，告知用户分析结果的保存位置以及如何禁用该任务（使用命令 `openclaw cron delete ...`）。

`get_campaign_analytics.py` 也可以根据需要手动运行，以获取实时分析数据：  
```bash
./scripts/get_campaign_analytics.py > analytics.json
```

## 联系人上传 + WhatsApp 模板发送

当用户提供 Excel 文件（包含姓名、电话号码和上下文信息）并希望发送 WhatsApp 模板时：

1. **将 Excel 文件转换为 JSON 格式**：  
   ```bash
   ./scripts/xlsx_to_contacts.py ~/Downloads/leads.xlsx contacts.json
   ```  
   请参阅 [`references/contact-workflow.md`](references/contact-workflow.md) 以了解列格式的要求和故障排除方法。该脚本会跳过空白行并规范电话号码格式。
2. **将联系人信息上传到 Toingg 的联系人列表中**（如果列表不存在，则会自动创建）：  
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
   - 仅当用户希望重新联系现有收件人时，才使用 `--resend` 参数。
4. 在 Toingg 中确认消息发送状态，并将任何错误反馈给用户（辅助脚本会打印完整的 JSON 响应以供日志记录）。

## 文件映射

| 脚本 | 功能 |
|--------|---------|
| `scripts/create_campaign.py` | 向 `/api/v3/create_campaign` 发送带有任意数据的 POST 请求 |
| `scripts/get_campaign_analytics.py` | 向 `/api/v3/get_campaign_analytics` 发送 GET 请求（适用于定时任务） |
| `scripts/xlsx_to_contacts.py` | 将 Excel 文件转换为 Toingg 的联系人 JSON 格式 |
| `scripts/add_contacts.py` | 通过 `/api/v3/add_contacts` 上传联系人信息 |
| `scripts/send_whatsapp_templates.py` | 触发 `/api/v3/send_whatsapp_templates` 以发送 WhatsApp 模板 |

请保持该工具包的简洁性：当 Toingg 添加新的字段或工作流程时，及时更新相关文档，以便其他操作人员能够遵循相同的操作模式。