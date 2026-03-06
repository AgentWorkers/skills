---
name: weavmail
description: 使用 weavmail CLI 来管理当前任务相关的电子邮件。当您需要读取、发送、回复或移动电子邮件以完成任务时，请使用该工具。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["uv"] }
      }
  }
---
# `weavmail` 是一个专为 AI 代理设计的命令行电子邮件客户端。使用它来读取、发送、回复和整理电子邮件。

## 设置

首次使用前请先进行一次安装：

```bash
uv tool install weavmail
```

配置一个账户（名为 `default`）：

```bash
weavmail account config \
  --imap-host imap.example.com \
  --smtp-host smtp.example.com \
  --username you@example.com \
  --password your-app-password \
  --addresses you@example.com
```

`--username` 和 `--password` 用于同时设置 IMAP 和 SMTP 凭据。账户名称默认为 `default`，在后续的所有命令中都可以省略。

每个选项都可以独立更新——只有你传递的选项才会被修改，其他设置保持不变。例如，仅更新密码：

```bash
weavmail account config --password new-password
```

`--addresses` 是一个用逗号分隔的电子邮件地址列表，这些地址被授权为该账户的发送者（例如：`--addresses you@example.com,alias@example.com`）。这里列出的所有地址都可以用作发送邮件时的 `--from` 地址。

要查看账户的当前配置，请运行 `account config`（不带任何选项）：

```bash
weavmail account config        # show default account
weavmail account config work   # show account named "work"
```

---

### 配置账户后

**配置任何账户后，务必自动运行以下命令：**

```bash
weavmail mailbox
```

检查输出内容，找到 “Sent” 和 “Trash” 文件夹（文件夹名称因提供商而异，例如：`Sent`、`Sent Messages`、`[Gmail]/Sent Mail`、`Trash`、`Deleted Messages`、`[Gmail]/Trash`）。然后将这些文件夹的路径保存到账户配置中：

```bash
weavmail account config --sent-mailbox "Sent" --trash-mailbox "Trash" --archive-mailbox "Archive"
```

这三个字段都是可选的——如果无法准确识别某个字段，请跳过它。未设置这些字段不会影响其他功能。

---

## 同步收件箱

从收件箱（INBOX）获取最新的电子邮件，并将它们保存为本地 Markdown 文件：

```bash
weavmail sync
```

选项：
- `--account NAMES` — 用逗号分隔的账户名称（默认：所有已配置的账户）
- `--mailbox FOLDER` — 同步另一个文件夹（默认：`INBOX`）
- `--limit N` — 要获取的最新邮件数量（默认：`10`）

每封邮件都会保存到 `./mails/<account>_<mailbox>/<uid>.md` 文件中，并附带 YAML 标头信息：

```yaml
---
uid: "12345"
account: default
mailbox: INBOX
subject: Hello there
from: sender@example.com
to:
- you@example.com
cc: []
date: "01 Jan 2026 12:00:00 +0000"
flags: []
---

Mail body here...
```

**在阅读邮件之前，请务必先进行同步。**同步完成后，直接读取 `.md` 文件——邮件正文从第二个 `---` 标签开始。

---

## 列出邮箱

列出该账户的所有可用 IMAP 文件夹：

```bash
weavmail mailbox
```

在同步非收件箱文件夹之前，使用此命令来获取准确的文件夹名称。文件夹名称区分大小写。

---

## 移动邮件

将一封邮件移动到另一个文件夹，并自动同步源文件夹：

```bash
weavmail move mails/default_INBOX/12345.md "Archive"
```

移动操作完成后，源文件夹会被同步，相应的本地文件也会被自动删除。

要删除一封邮件，只需将其移动到 “Trash” 文件夹。文件夹的名称因提供商而异（例如：`Trash`、`Deleted Messages`、`[Gmail]/Trash`）。请先使用 `weavmail mailbox` 命令查找正确的文件夹名称。

---

## 将邮件放入垃圾箱

将一封或多封邮件移动到账户的垃圾箱文件夹，并自动同步源文件夹：

```bash
weavmail trash mails/default_INBOX/12345.md
weavmail trash mails/default_INBOX/12345.md mails/default_INBOX/67890.md
```

可以传递多个 `MAIL_FILE` 参数以执行批量操作。垃圾箱的名称来自每封邮件的 `--trash-mailbox` 配置。如果账户未配置 `--trash-mailbox`，将会抛出错误。

移动操作完成后，源文件夹会被同步，相应的本地文件也会被自动删除。

---

## 将邮件归档

将一封或多封邮件移动到账户的归档文件夹，并自动同步源文件夹：

```bash
weavmail archive mails/default_INBOX/12345.md
weavmail archive mails/default_INBOX/12345.md mails/default_INBOX/67890.md
```

可以传递多个 `MAIL_FILE` 参数以执行批量操作。归档文件夹的名称来自每封邮件的 `--archive-mailbox` 配置。如果账户未配置 `--archive-mailbox`，将会抛出错误。

移动操作完成后，源文件夹会被同步，相应的本地文件也会被自动删除。

---

## 发送邮件

将邮件正文写入文件，然后发送：

```bash
cat > /tmp/body.txt << 'EOF'
Your message here.
EOF

weavmail send \
  --to recipient@example.com \
  --subject "Hello" \
  --content /tmp/body.txt
```

`--to`、`--cc` 和 `--bcc` 可以用于多个收件人。`--from` 的默认值是第一个配置的账户地址。

---

## 回复邮件

在回复模式下，`subject`、`to` 和 `from` 的值会从原始邮件中自动推断出来。原始邮件正文会被引用并添加到回复邮件中。`In-Reply-To` 和 `References` 标头也会被自动设置。如有需要，可以使用相应的选项进行自定义。

---

## 注意事项

- **切勿猜测 UID（邮件唯一标识符）**。务必先进行同步，然后再从输出结果中引用文件路径。
- **邮箱名称区分大小写**。请使用 `weavmail mailbox` 命令来获取准确的文件夹名称。
- 文件夹名称前的 `mailbox` 字段存储的是未转义的原始名称（例如：`INBOX/Sent`）；目录路径使用 `_` 作为分隔符。
- 文件头中的元数据信息以 `.md` 文件中的内容为准——请始终从文件中读取这些信息。
- 所有命令都支持 `--help` 选项，用于查看完整的使用说明，例如：`weavmail sync --help`。

---

## 多个账户

通过提供账户名称来配置额外的账户：

```bash
weavmail account config work \
  --imap-host imap.work.com \
  --smtp-host smtp.work.com \
  --username you@work.com \
  --password your-password \
  --addresses you@work.com
```

然后在任何命令后添加 `--account` 选项来指定目标账户：

```bash
weavmail sync --account work
weavmail sync --account work,personal   # sync multiple accounts at once
weavmail mailbox --account work
weavmail send --account work --to someone@example.com --subject "Hi" --content /tmp/body.txt
```

不带 `--account` 选项执行 `weavmail sync` 命令时，会自动同步 **所有** 已配置的账户。

对于 `move` 和 `send --reply` 操作，账户信息会从邮件文件中的元数据中读取；你可以添加 `--account` 选项作为安全措施：如果账户名称与文件中的信息不匹配，命令会终止并显示错误。对于 `trash` 和 `archive` 操作，账户信息始终从每封邮件的元数据中读取（不支持 `--account` 选项）。