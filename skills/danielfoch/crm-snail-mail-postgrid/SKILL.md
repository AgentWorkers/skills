---
name: crm-snail-mail-postgrid
description: 使用 PostGrid 从 CRM 联系人发送实体邮件。适用于从 GoHighLevel (GHL) 或 Follow Up Boss (FUB) 中提取联系人信息、映射联系人/地址字段、生成个性化的邮件内容，并通过 PostGrid API 发送信件或明信片的情况。此外，当其他技能已经生成了 GHL/FUB 联系人的 JSON 数据，并且需要从该数据集中发送邮件时，也可以使用此方法。
---
# 通过 PostGrid 进行 CRM 直邮营销

使用此技能，可以从 CRM 联系人中发送定向的直邮邮件。

## 工作流程

1. 选择数据源：`ghl`、`fub` 或预先导出的联系人 JSON 文件。
2. 将联系人数据拉取并转换为统一的格式。
3. 筛选出具有可邮寄地址的记录。
4. 生成个性化的邮件内容。
5. 将邮件发送任务提交到 PostGrid（支持 `letters` 或 `postcards` 格式），并提供试运行功能。
6. 返回每个联系人的发送结果（成功/失败状态）。

## 脚本

- `scripts/crm_postgrid_mailer.py`：
  用途：从 GHL/FUB 获取联系人数据（或从 JSON 文件中加载数据），对字段进行标准化处理，渲染邮件模板，并发送到 PostGrid。
- `scripts/postgrid_api.py`：
  用途：提供全面的 PostGrid API 功能，包含丰富的端点目录，并为未文档化的端点提供 `call-raw` 作为备用方案。

## 环境变量

- `GHL_API_KEY`：GHL API 密钥/令牌。
- `GHL_BASE_URL`（可选）：默认值为 `https://services.leadconnectorhq.com`。
- `FUB_API_KEY`：Follow Up Boss API 密钥。
- `FUB_BASE_URL`（可选）：默认值为 `https://api.followupboss.com/v1`。
- `POSTGRID_API_KEY`：PostGrid API 密钥。
- `POSTGRID_BASE_URL`（可选）：默认值为 `https://api.postgrid.com/print-mail/v1`。

## 常用命令

- 列出此技能包含的所有 PostGrid 端点：```bash
python3 scripts/postgrid_api.py list-endpoints
```
- 调用已注册的 PostGrid 端点：```bash
python3 scripts/postgrid_api.py call contacts.list
```
- 直接调用任意 PostGrid 端点（提供完整文档说明）：```bash
python3 scripts/postgrid_api.py call-raw GET /letters \
  --base-url https://api.postgrid.com/print-mail/v1
```
- 将 FUB 数据转换为 JSON 格式：```bash
python3 scripts/crm_postgrid_mailer.py fetch \
  --provider fub \
  --limit 200 \
  --output /tmp/fub_contacts_normalized.json
```
- 将 GHL 数据转换为 JSON 格式：```bash
python3 scripts/crm_postgrid_mailer.py fetch \
  --provider ghl \
  --location-id "$GHL_LOCATION_ID" \
  --limit 200 \
  --output /tmp/ghl_contacts_normalized.json
```
- 试运行 PostGrid 邮件内容生成：```bash
python3 scripts/crm_postgrid_mailer.py send \
  --contacts-file /tmp/ghl_contacts_normalized.json \
  --from-json-file references/example_sender_us.json \
  --html-template-file references/example_letter_template.html \
  --mail-route letters \
  --dry-run
```
- 一次性获取并发送邮件：```bash
python3 scripts/crm_postgrid_mailer.py run \
  --provider fub \
  --limit 100 \
  --from-json-file references/example_sender_us.json \
  --html-template-file references/example_letter_template.html \
  --mail-route letters \
  --output /tmp/mail_send_summary.json
```
- 使用其他 GHL/FUB 技能导出的 JSON 数据：```bash
python3 scripts/crm_postgrid_mailer.py run \
  --contacts-file /tmp/contacts_from_other_skill.json \
  --from-json-file references/example_sender_us.json \
  --html-template-file references/example_letter_template.html \
  --mail-route letters
```

## 数据结构

标准化的联系人数据结构包括：

- `id`
- `first_name`（名字）
- `last_name`（姓氏）
- `full_name`（全名）
- `email`（电子邮件地址）
- `phone`（电话号码）
- `address1`（地址1）
- `address2`（地址2）
- `city`（城市）
- `state`（州）
- `postal_code`（邮政编码）
- `country`（国家）
- `tags`（标签）
- `raw`（原始数据）

默认情况下，缺少 `address1`、`city`、`state` 或 `postal_code` 的联系人将被忽略。

## 集成说明

- 如果已有专门的 GHL/FUB 技能并且能够返回联系人 JSON 数据，可以通过 `--contacts-file` 参数传递该文件，从而跳过 API 数据拉取步骤。
- 如果 API 发生变化，请在 `scripts/crm_postgrid_mailer.py` 中调整相关代码，无需重新编写整个工作流程。
- 如果特定账户的 PostGrid 路由与默认值不同，请使用 `--postgrid-route` 参数进行配置。

## PostGrid 安全注意事项

- 在首次正式发送邮件前，使用 `--dry-run` 选项进行测试。
- 在首次正式发送时，设置 `--max-send` 参数以限制发送数量（例如：`--max-send 10`）。
- 使用 `--description` 参数添加清晰的邮件活动元数据。

有关路由/头部信息的详细说明及覆盖策略，请参阅 `references/postgrid-notes.md`。