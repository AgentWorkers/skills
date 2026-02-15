---
name: purelymail
description: 为 Clawdbot 代理设置并测试 PurelyMail 邮件服务。生成配置文件，测试 IMAP/SMTP 协议的连接性，并验证收件箱的可用性。
homepage: https://purelymail.com
metadata:
  clawdhub:
    emoji: "📬"
    requires:
      bins: ["python3"]
---

# 为Clawdbot配置PurelyMail

使用[PurelyMail](https://purelymail.com)为您的Clawdbot代理设置电子邮件账户——这是一个简单且注重隐私保护的电子邮件服务，非常适合代理的收件箱。

## 为什么选择PurelyMail？

- **价格实惠**：每年约10美元，可无限使用电子邮件地址。
- **操作简单**：没有多余的功能，只有基本的电子邮件服务。
- **隐私保护**：服务器位于美国，数据保留量极少。
- **可靠性高**：邮件送达率非常出色。
- **易于使用**：IMAP/SMTP配置非常简单。

## 快速入门（向导）

最简单的设置方式是使用交互式向导：

```bash
purelymail wizard
```

向导会完成以下操作：
1. ✓ 检查您是否拥有PurelyMail账户。
2. ✓ 测试您的IMAP/SMTP连接。
3. ✓ 生成`clawdbot.json`配置文件。
4. （可选）发送一封测试邮件。

## 手动设置

### 1. 创建PurelyMail账户

1. 访问[purelymail.com](https://purelymail.com)并注册。
2. 添加您的域名（或使用他们的子域名）。
3. 为您的代理创建一个邮箱（例如：`agent@yourdomain.com`）。
4. 记下密码。

### 2. 生成Clawdbot配置文件

```bash
purelymail config --email agent@yourdomain.com --password "YourPassword"
```

生成的JSON文件将添加到您的`clawdbot.json`中：

```json
{
  "skills": {
    "entries": {
      "agent-email": {
        "env": {
          "AGENT_EMAIL": "agent@yourdomain.com",
          "AGENT_EMAIL_PASSWORD": "YourPassword",
          "AGENT_IMAP_SERVER": "imap.purelymail.com",
          "AGENT_SMTP_SERVER": "smtp.purelymail.com"
        }
      }
    }
  }
}
```

### 3. 测试连接

```bash
purelymail test --email agent@yourdomain.com --password "YourPassword"
```

测试IMAP和SMTP的连接是否正常。

### 4. 发送测试邮件

```bash
purelymail send-test --email agent@yourdomain.com --password "YourPassword" --to you@example.com
```

### 5. 查看收件箱

```bash
purelymail inbox --email agent@yourdomain.com --password "YourPassword" --limit 5
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `config` | 生成`clawdbot.json`配置文件片段。 |
| `test` | 测试IMAP/SMTP连接是否正常。 |
| `send-test` | 发送一封测试邮件。 |
| `inbox` | 列出收件箱中的最新邮件。 |
| `read` | 读取指定的邮件。 |
| `setup-guide` | 打印完整的设置说明。 |

## 环境变量

在`clawdbot.json`中配置这些环境变量后，它们就可以被使用了：

- `AGENT_EMAIL` - 代理的电子邮件地址。
- `AGENT_EMAIL_PASSWORD` - 代理的密码。
- `AGENT_IMAP_SERVER` - IMAP服务器（imap.purelymail.com）。
- `AGENT_SMTP_SERVER` - SMTP服务器（smtp.purelymail.com）。

## PurelyMail设置

| 设置 | 值 |
|---------|-------|
| IMAP服务器 | `imap.purelymail.com` |
| IMAP端口 | `993`（SSL） |
| SMTP服务器 | `smtp.purelymail.com` |
| SMTP端口 | `465`（SSL）或`587`（STARTTLS） |
| 认证方式 | 电子邮件 + 密码 |

## 提示

- 为代理设置一个强大且唯一的密码。
- 考虑为代理的电子邮件创建一个专用的域名。
- PurelyMail支持使用“catch-all”地址（便于邮件路由）。
- 为您的PurelyMail账户启用双重身份验证（使用应用生成的密码进行登录）。