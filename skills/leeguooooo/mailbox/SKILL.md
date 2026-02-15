# Mailbox CLI（OpenClaw技能）

使用mailbox CLI工具来读取和管理电子邮件。OpenClaw负责处理邮件的发送和调度。mailbox CLI会返回结构化的JSON数据以及可选的文本摘要。

## 前提条件
- 已安装mailbox CLI（通过`npm install -g mailbox-cli`命令安装）。
- 需要在`~/.config/mailbox/auth.json`文件中配置登录凭据。

## 命令示例
- `mailbox account list --json`：列出所有账户。
- `mailbox email list --limit 20 --json`：列出前20封电子邮件（按发送时间排序）。
- `mailbox email show <email_uid> --account-id <account_id> --json`：显示指定账户的电子邮件信息。
- `mailbox email show <email_uid> --account-id <account_id> --preview --no-html --json`：显示指定账户的电子邮件信息，并以纯文本形式预览（不含HTML格式）。
- `mailbox email show <email_uid> --account-id <account_id> --preview --no-html --strip-urls --json`：显示指定账户的电子邮件信息，以纯文本形式预览，并去除URL链接。
- `mailbox email delete <email_uid> --account-id <account_id> --folder INBOX --confirm --json`：从收件箱中删除指定电子邮件。
- `mailbox digest run --json`：运行邮件摘要生成任务。
- `mailbox monitor run --json`：监控邮件系统的运行状态。
- `mailbox inbox --limit 15 --text`：查看收件箱中的前15封电子邮件（以纯文本形式）。

## 安全规则
- 在自动化操作中务必使用`--json`选项，并检查操作是否成功（`success`字段）。
- 对于可能具有破坏性影响的操作（如删除邮件），必须提供`--account-id`参数。
- 除非指定了`--confirm`选项，否则破坏性操作默认会先进行模拟运行（dry-run）。
- 在实际修改数据之前，建议先使用`--dry-run`选项进行测试。

## 输出格式
- JSON响应包含`success`和`error`字段。
- `error`字段是一个对象，格式为`{ code, message, detail? }`。
- 成功返回代码：0；操作失败返回代码：1；使用方式错误返回代码：2。