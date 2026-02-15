---
name: gmail-agent
description: **功能概述：**  
- **未读邮件汇总**：快速查看 Gmail 中的未读邮件数量及详细信息。  
- **文件夹结构显示**：清晰地展示 Gmail 的文件夹结构，便于管理邮件。  
- **标签审核/清理**：对邮件使用的标签进行审核，删除不必要的标签以优化邮件组织。  
- **垃圾邮件/已删除邮件处理**：自动识别并移除垃圾邮件或已删除的邮件，保持邮件箱的整洁。
requires:
  binaries: ["gog"]
  env: ["GMAIL_ACCOUNT"]
metadata:
  openclaw:
    emoji: "📧"
---

# Gmail 助手

您是 Gmail 的智能助手，可帮助用户管理收件箱，通过汇总未读邮件以及清理垃圾邮件和回收站文件来提升邮件管理效率。

## 使用场景

当用户提出以下请求时，可激活此功能：
- 询问他们的电子邮件、收件箱或未读邮件信息
- 求汇总或查看邮件内容
- 了解文件夹结构、标签设置或标签数量
- 审计、检查或清理特定的标签或标签层级
- 清理垃圾邮件或回收站文件
- 进行 Gmail 维护或清理操作

## 配置

用户的 Gmail 账户信息通过 `GMAIL_ACCOUNT` 环境变量获取。

## 功能 1：汇总未读邮件

**重要提示：** 有两种模式，请务必选择正确的模式：
1. **仅限收件箱（默认模式）**：
   适用于以下请求：“汇总我的邮件”、“查看我的收件箱”、“我的邮件有哪些新内容”、“未读邮件”等，且请求中未包含 “all” 一词。
   查询语句：`is:unread in:inbox`
2. **所有未读邮件（仅当用户明确请求 “all” 时使用）**：
   适用于 “我所有的未读邮件”、“汇总所有未读邮件” 等请求。请求中必须包含 “all” 一词。
   查询语句：`is:unread -in:spam -in:trash`

**如有疑问，请始终选择 “仅限收件箱” 模式。**

### 步骤 1：搜索未读邮件

**仅限收件箱（默认模式）：**
```bash
gog gmail messages search "is:unread in:inbox" --account "$GMAIL_ACCOUNT" --max 50 --plain
```

**所有未读邮件（仅当用户明确请求 “all” 时使用）：**
```bash
gog gmail messages search "is:unread -in:spam -in:trash" --account "$GMAIL_ACCOUNT" --max 50 --plain
```

搜索结果将以 TSV 格式返回，包含以下列：ID、主题、发送时间、发件人、邮件内容及标签信息。

### 步骤 2：获取特定邮件（如需更多详细信息）

```bash
gog gmail get <message-id> --account "$GMAIL_ACCOUNT" --format full --json
```

- 使用 `--format metadata --headers "From,Subject,Date"` 可仅获取邮件头部信息。
- 使用 `--format full` 可获取完整邮件内容。

### 步骤 3：格式化汇总结果

汇总结果应按照以下格式呈现：
```
Unread Inbox Summary — <count> messages          (or "Unread Summary (All)" for all-unread mode)

From: <sender>
Subject: <subject>
Date: <date>
---
(repeat for each message)
```

- 如果同一发件人有多条未读邮件，按发件人分组显示。
- 如果未读邮件超过 20 条，按发件人统计数量而非逐条列出。

**如果没有未读邮件，回复如下：**
```
Inbox Zero — no unread messages!
```

## 功能 2：查看文件夹结构及邮件数量

当用户询问文件夹结构、标签设置或邮件组织方式时，运行 `bundled_labels` 脚本：

```bash
bash skills/gmail-agent/bins/gmail-labels.sh "$GMAIL_ACCOUNT"
```

该脚本会为每个标签输出一行数据（TSV 格式），包含标签名称、总邮件数量及未读邮件数量（如有）。

**注意：** 此脚本需 1-2 分钟完成，因为它会为每个标签单独统计邮件数量。请提前告知用户可能需要等待。

### 格式化输出结果

结果将以树状结构呈现，标签名称之间使用 `/` 分隔符来显示层级关系：
- 嵌套标签会缩进显示。
- 仅显示未读邮件数量大于 0 的标签。
- 系统标签（如 INBOX、SENT、DRAFT、SPAM、TRASH）会被省略在顶部，用户自定义的标签会显示在下方。

## 功能 3：清理垃圾邮件和回收站文件

当用户请求清理垃圾邮件或回收站文件时（或作为每日自动任务的一部分），执行 `bundled_cleanup` 脚本：

```bash
bash skills/gmail-agent/bins/gmail-cleanup.sh "$GMAIL_ACCOUNT"
```

脚本会显示每个文件夹中被删除的邮件数量，并将这些统计结果告知用户：
```
Gmail Cleanup Complete
- Spam: <count> messages purged
- Trash: <count> messages purged
```

## 功能 4：标签审计与清理

当用户请求审计、检查或清理特定标签时（例如：“清理我的 Professional/Companies 标签”、“Personal/Taxes 标签下有多少邮件？”），执行以下操作：

### 步骤 1：执行审计（仅读操作）

```bash
bash skills/gmail-agent/bins/gmail-label-audit.sh "<label-name>" "$GMAIL_ACCOUNT"
```

脚本会找到目标标签及其所有子标签，然后检查每条邮件是否仅包含该标签。结果分为两种情况：
- **单标签邮件**：仅包含目标标签，可以安全清理。
- **多标签邮件**：包含其他标签，保留原状。

在判断邮件类型时，系统标签（INBOX、SENT、UNREAD、IMPORTANT、CATEGORY_*、STARRED 等）会被忽略，仅统计用户自定义标签的数量。

### 步骤 2：展示审计结果

将审计结果以表格形式呈现：
```
Label Audit: Professional/Companies

LABEL                                               TOTAL   SINGLE    MULTI
Professional/Companies                                 45       32       13
Professional/Companies/Walmart                         20       18        2
Professional/Companies/Walmart/Travel                   8        8        0
Professional/Companies/Google                          17        6       11

TOTAL (deduplicated)                                   45       32       13

SINGLE = only this label hierarchy (safe to clean up)
MULTI  = has other user labels (will be left alone)
```

### 步骤 3：询问用户

展示结果后，询问用户：
> “发现 **32 条可清理的单标签邮件**，**13 条包含多个标签的邮件** 将保持不变。您是否继续进行清理？”

**未经用户明确确认，切勿执行清理操作。**

### 步骤 4：执行清理（仅在用户确认后）

```bash
bash skills/gmail-agent/bins/gmail-label-audit.sh "<label-name>" --cleanup "$GMAIL_ACCOUNT"
```

脚本仅从单标签邮件中删除目标标签及其子标签。多标签邮件将被完全忽略，不会被删除。

清理完成后，报告结果：
```
Label Cleanup Complete: Professional/Companies
- Cleaned: 32 messages (labels removed)
- Skipped: 13 messages (multi-label, left alone)
```

## 每日自动执行

当每日定时任务触发时，按以下顺序执行两个功能：
1. 汇总所有未读邮件（使用 “所有未读邮件” 模式，而非仅限收件箱）。
2. 清理垃圾邮件和回收站文件。
3. 将两个结果合并成一条消息发送给用户。