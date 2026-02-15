---
name: Mail
description: 执行电子邮件操作时，会采用针对特定平台的优化措施和安全协议。
---

## 平台检测与路由

**macOS**: 使用 Apple Mail 的 SQLite 查询（速度比 AppleScript 快 100 倍）。

**跨平台**: 使用 himalaya CLI 进行完整的 IMAP/SMTP 操作。

**切勿在同一任务中混合使用多种方法**，选择一种方法以避免状态冲突。

## Apple Mail SQLite 的注意事项

**查询路径**: `~/Library/Mail/V*/MailData/Envelope\Index`

**关键表**: `messages`（主题、发件人、接收日期）、`addresses`（地址信息）、`mailboxes`（邮箱信息）。

**强制同步数据**: 使用 `osascript -e 'tell app "Mail" to check for new mail'` 命令进行同步；否则 SQLite 会读取过时的数据。

**最近收到的邮件筛选条件**: `WHERE date_received > strftime('%s','now','-7 days')`

**数据关联方式**: 通过 `message_id` 将 `messages` 表与 `addresses` 表关联以查找发件人信息。

**附件检查**: 检查 `messages.attachment_count` 是否大于 0；附件文件位于 `~/Library/Mail/V*/MAILBOX/Messages/` 目录下。

## himalaya CLI 的使用技巧

**安装**: 使用 `cargo install himalaya` 或 `brew install himalaya` 进行安装。

**编程解析时务必使用**: `--output json` 标志以获取 JSON 格式的输出结果。

**列出邮件**: 使用 `himalaya envelope list -o json`（而非 `message list`）。

**文件夹操作**: `himalaya message move <id> <folder>`（文件夹名称区分大小写）。

**缓存更新**: 在服务器端文件夹发生变化后，运行 `himalaya folder list` 命令更新缓存。

## 发送邮件协议

**邮件撰写-审核-发送的工作流程**: 先撰写邮件，然后向用户显示邮件内容，用户确认后才能发送。

**回复邮件时的线程处理**: 必须包含 `In-Reply-To` 和 `References` 标头，否则回复邮件会断开线程。

**使用 himalaya send 发送邮件**: `himalaya message send` 会根据 RFC 2822 协议从标准输入读取邮件内容。

**SMTP 拒绝情况**: 如果邮件中的 `From` 标头与认证用户的地址不匹配，某些服务器会拒绝发送邮件。

## 凭据管理

**macOS Keychain**: 使用 `security add-internet-password -s imap.gmail.com -a user@gmail.com -w 'app-password'` 命令设置密码。

**Gmail/Google Workspace**: 需要启用 2FA 的 App Password，而非普通密码。

**OAuth 令牌**: himalaya 支持通过 `config.toml` 文件中的 `token_cmd` 配置 XOAUTH2 认证。

## 线程处理机制

**邮件线程的识别方式**: 根据 `In-Reply-To` 标头来区分邮件线程，而非主题内容。“Re:” 前缀不可靠。

**轮询间隔**: 最大为 15-30 分钟。如需实时更新，可使用 `himalaya envelope watch` 命令。