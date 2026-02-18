---
name: Mail
slug: mail
version: 1.2.0
description: 执行电子邮件操作时，会利用平台特定的优化机制，并确保凭证处理的安全性。
changelog: Added explicit scope, requirements, and data access documentation
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["himalaya"]},"os":["darwin","linux"]}}
---
## 要求

**二进制文件：**
- `himalaya` - IMAP/SMTP 命令行工具（使用 `brew install himalaya` 或 `cargo install himalaya` 安装）
- `osascript` - 仅适用于 macOS，为内置脚本

**凭据：**
- Gmail 的应用密码（非普通密码），存储在 macOS 的 Keychain 中
- 配置信息位于 `~/.config/himalaya/config.toml` 文件中

## 数据访问

**只读路径：**
- `~/Library/Mail/V*/MailData/Envelope Index` - Apple Mail 的 SQLite 数据库（仅适用于 macOS）
- `~/Library/Mail/V*/MAILBOX/Messages/` - 附件文件（仅适用于 macOS）

## 功能范围

- ✅ 通过 `himalaya` 命令行工具或 Apple Mail 的 SQLite 数据库读取电子邮件
- ✅ 通过 `himalaya` 发送电子邮件（遵循“草稿-审核-发送”的工作流程）
- ✅ 搜索和过滤邮件
- ❌ 绝不修改凭据
- ❌ 未经明确确认，绝不删除电子邮件
- ❌ 未经用户审核，绝不自动发送电子邮件

## 快速参考

| 主题 | 文件 |
|-------|------|
| Apple Mail 的 SQLite 查询 | `apple-mail.md` |
- `himalaya` 命令行工具的使用方法 | `himalaya.md` |
| 发送/回复邮件协议 | `sending.md` |

## 核心规则

### 1. 平台检测
- **使用 Apple Mail 的 macOS 系统**：优先使用 SQLite 查询（速度比 AppleScript 快 100 倍）
- **跨平台环境**：使用 `himalaya` 命令行工具进行完整的 IMAP/SMTP 操作
- **同一任务中严禁混合使用不同方法**，以避免状态冲突

### 2. Apple Mail 的 SQLite 数据库
- 查询路径：`~/Library/Mail/V*/MailData/Envelope\ Index`
- **强制同步数据**：执行 `osascript -e 'tell app "Mail" to check for new mail'`，否则 SQLite 可能会读取过时的数据
- 近期邮件的筛选条件：`WHERE date_received > strftime('%s','now','-7 days')`
- 通过 `message_id` 将 `messages` 和 `addresses` 表连接起来以查找发件人信息

### 3. `himalaya` 命令行工具
- **务必使用** `--output json` 标志进行程序化数据解析
- 列出电子邮件：`himalaya envelope list -o json`（注意：使用 `message list` 是错误的命令）
- 文件夹名称区分大小写
- 在服务器端文件夹结构发生变化后，需要运行 `himalaya folder list` 命令

### 4. 发送邮件协议
- **遵循“草稿-审核-发送”的工作流程**：编写邮件 → 显示邮件完整内容 → 待用户确认后发送
- 回复邮件时需要包含 `In-Reply-To` 和 `References` 头部字段，以确保邮件正确关联
- 某些 SMTP 服务器会拒绝接收发件人地址与认证用户不符的邮件

### 5. 凭据管理
- 使用 macOS 的 Keychain 存储凭据：`security add-internet-password -s imap.gmail.com -a user@gmail.com -w 'app-password'`
- Gmail/Google Workspace 要求启用 2FA 功能的应用密码
- `himalaya` 支持通过 `config.toml` 文件中的 `token_cmd` 配置 XOAUTH2 认证

### 6. 邮件线程管理
- 邮件线程的区分依据是 `In-Reply-To` 头部字段，而非邮件主题
- 前缀 “Re:” 不可靠，不能用于判断邮件是否属于同一线程
- 轮询间隔建议设置为 15-30 分钟；如需实时监控，可使用 `himalaya envelope watch` 命令