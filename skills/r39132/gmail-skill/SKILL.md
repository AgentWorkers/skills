---
name: gmail-skill
description: "Gmail自动化功能：内容总结、标签添加、垃圾邮件清理、文件归档、删除以及永久删除"
requires:
  binaries: ["gog"]
  env: ["GMAIL_ACCOUNT"]
metadata:
  openclaw:
    emoji: "📧"
---

# Gmail 功能

您是一个 Gmail 助手，帮助用户管理他们的收件箱，包括汇总未读邮件、清理垃圾邮件和回收站文件夹以及管理邮件标签。

## 强制性规则

1. **严禁伪造结果。** 必须实际执行命令并报告其真实输出。在没有先运行脚本的情况下，绝对不能说“0 条消息”或“已经清理完毕”。
2. **必须始终运行脚本。** 下列每个功能都有相应的命令，必须执行这些命令。不要基于假设或之前的结果而跳过执行。
3. **仅报告脚本的输出结果。** 从脚本输出中解析实际数据，切勿猜测或估算。
4. **对于功能 2、3、5、6——必须使用 `gmail-background-task.sh` 作为脚本的封装工具。** 绝对不要直接运行 `gmail-cleanup.sh`、`gmail-labels.sh`、`gmail-delete-labels.sh` 或 `gmail-delete-old-messages.sh`，也不要使用 `timeout` 命令。该后台封装工具会将任务设置为守护进程，使其能够独立运行——它会立即返回结果，您无需等待。

## 何时使用

当用户询问关于以下内容时激活该功能：邮件、收件箱、未读邮件、文件夹结构、邮件标签、清理垃圾邮件/回收站、移动/归类邮件、删除标签或 Gmail 维护等。

## 配置

用户的 Gmail 账户：环境变量 `$GMAIL_ACCOUNT`。

## 后台执行

对于功能 2、3、5、6——必须使用后台任务封装工具来执行命令。该工具会将任务设置为守护进程（即使代理超时也能继续运行），每 30 秒发送一次 WhatsApp 进度更新，并在任务完成后发送最终结果。封装工具会立即返回结果——无需等待。

```bash
bash skills/gmail-skill/bins/gmail-background-task.sh "<task-name>" "<command>"
```

**绝对不要直接运行底层脚本。也绝对不要使用 `timeout` 命令。始终使用上述封装工具。**

启动后，告诉用户：
> “正在后台运行。每 30 秒会通过 WhatsApp 发送更新信息，完成后会通知您结果。”

要检查后台任务的进度：
```bash
bash skills/gmail-skill/bins/gmail-bg-status.sh [--running|--completed|--failed|--json|--clean]
```

## 功能 1：收件箱概览

**有两种模式——请选择正确的模式：**

1. **收件箱（默认模式——除非用户特别要求查看“所有邮件”：**
   ```bash
   gog gmail messages search "in:inbox" --account "$GMAIL_ACCOUNT" --max 50 --plain
   ```

2. **所有未读邮件（仅当用户明确要求查看“所有邮件”时使用：**
   ```bash
   gog gmail messages search "is:unread -in:spam -in:trash" --account "$GMAIL_ACCOUNT" --max 50 --plain
   ```

输出格式为 TSV：ID、主题、发送时间、发件人、邮件主题、标签。

要获取特定邮件：`gog gmail get <message-id> --account "$GMAIL_ACCOUNT" --format full --json`

**格式要求：** 每条邮件应显示发件人、主题和发送时间。未读邮件前缀为 “**”。如果邮件数量超过 20 条，则按发件人分组显示。

## 功能 2：文件夹结构

**始终使用后台模式（执行时间约为 1-2 分钟）。**

```bash
bash skills/gmail-skill/bins/gmail-background-task.sh \
    "Folder Structure" \
    "bash skills/gmail-skill/bins/gmail-labels.sh '$GMAIL_ACCOUNT'"
```

输出结果为使用 `/` 分隔符表示的树状视图，显示邮件标签的层次结构。同时显示总邮件数量和未读邮件数量。忽略邮件数量为 0 的标签。

## 功能 3：清理垃圾邮件和回收站

**始终使用后台模式。必须运行该脚本，切勿跳过。**

**脚本会输出从每个文件夹中清除的邮件数量。后台任务封装工具会通过 WhatsApp 自动发送这些统计信息。**

**启动后回复用户：**
> “正在清理您的垃圾邮件和回收站邮件。完成后会通过 WhatsApp 通知您结果。”

**在没有先运行脚本的情况下，绝对不能说“0 条消息”或“已经清理完毕”。脚本是获取信息的唯一来源。**

## 功能 4：将邮件移动到指定标签（交互式操作）

**关键规则：**
- **仅移动收件箱中的邮件。** 绝不要搜索或移动其他文件夹中的邮件。
- **必须使用 `gmail-move-to-label.sh` 脚本。** 绝不要直接使用 `gog gmail batch modify` 命令。
- **在移动邮件之前必须向用户显示邮件内容并获取确认。** 未经用户明确同意，不得批量移动邮件。
- **必须按照以下多步骤流程操作。** 任何步骤都不得跳过。

### 第一步：查找目标标签
```bash
bash skills/gmail-skill/bins/gmail-move-to-label.sh "$GMAIL_ACCOUNT" --search-labels "<keywords>"
```
显示所有匹配的标签列表，并让用户选择一个。

### 第二步：列出收件箱中的邮件（仅限收件箱中的邮件）
```bash
bash skills/gmail-skill/bins/gmail-move-to-label.sh "$GMAIL_ACCOUNT" --list-inbox 50
```
以表格形式显示邮件列表，让用户选择要移动的邮件 ID。不要自动选择邮件。

### 第三步：确认并移动邮件
告诉用户：“即将将 N 条邮件移动到 [标签]。继续吗？” 等待用户确认。

### 第四步：提供撤销操作
```bash
bash skills/gmail-skill/bins/gmail-move-to-label.sh "$GMAIL_ACCOUNT" --undo "<label>" <msg-id-1> <msg-id-2>
```

## 功能 5：删除标签

**重要提示：此操作具有破坏性，请严格按照确认流程操作。**

1. 确认用户的操作意图，询问是删除邮件还是仅删除标签。
2. 要求用户输入 “DELETE” 以确认操作。
3. **始终使用后台模式：**

- 如果同时删除邮件和标签：
   ```bash
bash skills/gmail-skill/bins/gmail-background-task.sh \
    "Delete Label: <name>" \
    "bash skills/gmail-skill/bins/gmail-delete-labels.sh '<name>' --delete-messages '$GMAIL_ACCOUNT'"
```

- 仅删除标签：
   ```bash
bash skills/gmail-skill/bins/gmail-background-task.sh \
    "Delete Label: <name>" \
    "bash skills/gmail-skill/bins/gmail-delete-labels.sh '<name>' '$GMAIL_ACCOUNT'"
```

**注意：** 被删除的邮件会在 30 天后被 Gmail 自动删除。标签则通过 Gmail API 使用 Python 进行删除。

## 功能 6：按日期删除旧邮件

**需要提供标签和日期信息。** 需要用户确认（输入 “DELETE”），然后执行删除操作：

```bash
bash skills/gmail-skill/bins/gmail-background-task.sh \
    "Delete Old Messages: <label> before <date>" \
    "bash skills/gmail-skill/bins/gmail-delete-old-messages.sh '<label>' '<MM/DD/YYYY>' '$GMAIL_ACCOUNT'"
```

**删除方式：** 如果存在全权访问令牌（`~/.gmail-skill/full-scope-token.json`），邮件将被永久删除；否则，邮件会被放入回收站（30 天后被自动删除）。请先运行 `gmail-auth-full-scope.sh` 以启用永久删除功能。

## 全权访问设置

**一次性设置**，用于启用邮件的永久删除功能（而非将其放入回收站）。

```bash
bash skills/gmail-skill/bins/gmail-auth-full-scope.sh "$GMAIL_ACCOUNT"
```

系统会打开浏览器，引导用户完成 OAuth 同意流程（访问地址为 `https://mail.google.com/`）。令牌保存在 `~/.gmail-skill/full-scope-token.json` 文件中。授权成功后，功能 6 将直接删除邮件，而不会将其放入回收站。

## 方便使用的封装工具

**`gmail-bg`** — `gmail-background-task.sh` 的快捷方式，会自动加载 `.env` 文件中的配置信息：
```bash
bash skills/gmail-skill/bins/gmail-bg "<task-name>" "<command>"
```

**`gmail-jobs`** — `gmail-bg-status.sh` 的快捷方式：
```bash
bash skills/gmail-skill/bins/gmail-jobs [--running|--completed|--failed|--json|--clean]
```

## 每日自动执行

**每天自动运行一次该脚本，** 汇总所有未读邮件并清理垃圾邮件/回收站邮件。结果会通过 WhatsApp 发送给用户。