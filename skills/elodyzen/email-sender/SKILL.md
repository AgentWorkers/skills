# OpenClaw 邮件功能

## 描述
使用 SMTP 通过 OpenClaw 发送电子邮件（可附加文件）。此功能依赖于使用应用密码（App Password）登录的 Gmail 账户。

## 使用场景
- **适用场景**：用户需要发送报告、日志或任何文件时使用。
- **参数**：
  - `to` (string, 必填): 收件人电子邮件地址。
  - `subject` (string, 必填): 电子邮件主题。
  - `body` (string, 必填): 纯文本邮件正文。
  - `attachment_path` (string, 可选): 要附加的文件的绝对路径。

## 工具
该功能提供了一个名为 `send_email` 的函数，可以通过 OpenClaw 的函数工具来调用。