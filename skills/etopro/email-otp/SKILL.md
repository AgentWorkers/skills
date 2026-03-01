---
name: email-otp
description: 创建临时电子邮件地址，并监控注册过程中的OTP验证码或验证链接。
version: 1.0.0
metadata:
  author: etopro
---
# 邮箱OTP技能

该技能用于生成临时电子邮件地址，并自动从收到的邮件中提取OTP代码和验证链接。它使用免费的mail.tm API（无需API密钥）。

## 何时使用此技能

当用户需要以下操作时，可以调用此技能：
- 创建临时电子邮件地址
- 获取用于注册/验证的一次性电子邮件地址
- 检查OTP（一次性密码）代码
- 等待邮件验证链接
- 监控收件箱中的认证代码

## 快速入门

```bash
# Create a new temporary email
python3 scripts/tempmail_otp.py create

# Monitor for OTP codes (5 minute timeout)
python3 scripts/tempmail_otp.py check

# List current account and messages
python3 scripts/tempmail_otp.py list
```

## 命令

### 创建账户

```bash
python3 scripts/tempmail_otp.py create [OPTIONS]
```

**选项：**
- `-e, --email_ADDRESS` - 自定义完整电子邮件地址
- `-d, --domain DOMAIN` - 使用的特定域名
- `-p, --password PASSWORD` - 账户密码（未指定时自动生成）
- `--json` - 以JSON格式输出

**示例：**
```bash
python3 scripts/tempmail_otp.py create --domain "marcilzo.com"
```

### 检查OTP/链接

```bash
python3 scripts/tempmail_otp.py check [OPTIONS]
```

**选项：**
- `--timeout SECONDS` - 等待的最大秒数（默认：300）
- `--poll SECONDS` - 轮询间隔（秒）（默认：3）
- `--sender EMAIL` - 仅接受来自该发件人的邮件
- `--subject TEXT` - 仅接受主题中包含该文本的邮件
- `--pattern REGEX` - 用于提取OTP的自定义正则表达式
- `--once` - 找到第一个OTP后退出
- `--json` - 以JSON格式输出消息

**示例：**
```bash
# Wait up to 2 minutes for OTP
python3 scripts/tempmail_otp.py check --timeout 120

# Only accept emails from noreply@example.com
python3 scripts/tempmail_otp.py check --sender "noreply@example.com"

# Exit immediately after finding OTP
python3 scripts/tempmail_otp.py check --once
```

### 列出账户和消息

```bash
python3 scripts/tempmail_otp.py list
```

显示当前账户详细信息以及收件箱中的所有带有提取链接的消息。

### 列出可用域名

```bash
python3 scripts/tempmail_otp.py domains [--json]
```

## 输出文件

当找到OTP或链接时，脚本会自动将它们保存到统一的状态目录中：
- `~/.tempmail_otp/last_otp` - 包含最后提取的OTP代码
- `~/.tempmail_otp/last_link` - 包含第一个找到的验证链接
- `~/.tempmail_otp/account.json` - 账户凭证（JWT令牌、电子邮件地址、密码）

所有状态文件都存储在`~/.tempmail_otp/`目录中，并具有受限权限（0600）。

## OTP检测模式

脚本使用以下模式自动检测OTP代码：
- 6-8位数字（最常见）
- 4位数字
- “code: XXXXXX”格式
- “verification: XXXXXX”格式
- “otp: XXXXXX”格式

## 链接提取

脚本从电子邮件HTML中提取所有HTTP/HTTPS链接，并过滤掉：
- 退订链接
- 跟踪链接
- 图片文件（.png、.jpg、.gif）

## 状态管理

所有状态信息都存储在统一的目录`~/.tempmail_otp/`中：
- `account.json` - 账户凭证和JWT令牌（由`create`命令创建）
- `last_otp` - 最新的OTP代码（由`check`命令创建）
- `last_link` - 第一个提取的验证链接（由`check`命令创建）

文件具有受限权限（0600）以确保安全。`check`和`list`命令会自动使用存储的凭证。

### 设计理念

统一的状态目录遵循CLI工具的最佳实践：
1. **不会污染项目目录** - 不会在工作目录中创建临时文件
2. **位置可预测** - 所有状态信息都集中在一个地方，便于查找和清理
3. **跨会话持久化** - 可以从系统中的任何目录使用
4. **权限安全** - 敏感凭证具有适当的文件权限

要重置所有状态：`rm -rf ~/.tempmail_otp/`

## 典型工作流程

1. **创建账户** - 生成一个新的临时电子邮件地址
2. **使用电子邮件** - 在服务注册时提供该电子邮件地址
3. **监控收件箱** - 运行`check`命令等待OTP/链接
4. **提取代码** - OTP会自动显示并保存到`~/.tempmail_otp/last_otp`
5. **验证** - 使用OTP或链接完成验证

## 示例会话流程

```bash
# Create a temp email
$ python3 scripts/tempmail_otp.py create
Email: a3b7c9d4@marcilzo.com
Password: f8e4d2a1-1234-5678-9abc-123456789abc
Domain: marcilzo.com

Account saved to /home/user/.tempmail_otp/account.json

# In another terminal, wait for OTP
$ python3 scripts/tempmail_otp.py check --once
Monitoring: a3b7c9d4@marcilzo.com
Timeout: 300s | Poll interval: 3s
--------------------------------------------------

📧 New email from: noreply@service.com
   Subject: Your verification code

✅ OTP FOUND: 842197
OTP saved to /home/user/.tempmail_otp/last_otp
--------------------------------------------------
```

## 错误处理**

- 如果电子邮件地址已被占用，脚本会自动尝试新的用户名
- 网络错误会被记录下来，脚本会继续轮询
- 如果账户状态无效，系统会提示用户重新创建账户

## API

该技能使用mail.tm的REST API：
- 基本URL：`https://api.mail.tm`
- 认证：JWT承载令牌
- 不需要API密钥

## 注意事项

- 临时电子邮件可能在一段时间后过期
- 一些服务可能会阻止使用临时电子邮件域名
- 脚本会自动处理账户创建和JWT令牌的管理
- OTP模式涵盖了大多数常见格式，但也可以通过`--pattern`参数提供自定义正则表达式