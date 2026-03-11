---
name: gmail-label-routing
description: >
  在 Gmail 中配置基于发件人的邮件路由规则，可以使用本地工作流脚本 `scripts/gws_gmail_label_workflow.py`。该脚本支持以下操作：创建/使用标签、创建邮件过滤器、将邮件规则应用到现有邮件（可追溯性地执行），以及可选地将邮件从收件箱（INBOX）中移除。适用于用户需要执行以下操作的场景：  
  - “将此发件人的所有邮件发送到该标签”  
  - “对多个发件人的邮件执行相同操作”  
  - “将现有邮件应用相应的规则”  
  - “将邮件从收件箱中移除”  
  - “清理或替换该发件人的重复邮件过滤器”。
---
# Gmail 标签路由

## 概述

通过统一、一致的流程，标准化 Gmail 中根据发件人更改标签的操作。
优先使用本地脚本，以避免过滤器设置、标签重新应用以及邮件状态（INBOX）之间的手动不一致问题。

## 工作流程

1. 确认用户的操作意图：
- 目标标签
- 一个或多个发件人
- 是否需要将邮件移出 INBOX（默认值：是）
- 是否需要替换该发件人的现有过滤器（仅在用户明确要求或存在冲突时执行）

2. 执行工作流程：

```bash
python3 scripts/gws_gmail_label_workflow.py \
  --label "<Etiqueta>" \
  --sender "correo1@dominio.com" \
  --sender "correo2@dominio.com"
```

> `scripts/gws_gmail_label_workflow.py` 是与该技能相关的脚本文件，位于指定目录中。

## 常见选项：
- 将邮件保留在 INBOX 中：`--keep-inbox`
- 替换发件人的过滤器：`--replace-sender-filters`
- 仅进行模拟操作（不实际修改邮件状态）：`--dry-run`

3. 通过脚本的最终 JSON 输出结果来确认操作结果：
- `createdFilterId`：新创建的过滤器 ID
- `retroApplied`：已重新应用的过滤器设置
- `withLabelCount`：带有新标签的邮件数量
- `inboxCount`：仍保留在 INBOX 中的邮件数量

## 规则：
- 对于每个发件人，都需要重复执行 `--sender` 参数。
- 标签和发件人的名称必须使用引号括起来，以避免解析错误。
- 当同一发件人的规则存在重复时，必须使用 `--replace-sender-filters` 选项。
- 如果用户要求“执行相同的操作”，则需要重复执行以下步骤：设置标签、应用过滤器、回溯现有标签设置，并处理邮件在 INBOX 中的分布情况。
- 如果 `gws` 在处理过滤器时出现权限问题，应使用工作流程中已实现的备用方案（本地 OAuth 凭据）。

## 参考资料

- 请参阅 `references/commands.md` 文件中的示例代码。