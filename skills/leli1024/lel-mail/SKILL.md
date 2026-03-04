---
name: lel-mail
description: 通过结合使用 Python 和 Bash 脚本来发送和读取电子邮件，这些脚本利用了主要的代理（agent）来进行逻辑处理和推理。该技能使代理能够根据电子邮件中的内容将信息存储到内存中，并与用户进行沟通——无论是为了通知他们某些事件的发生，还是请求他们的输入以作出响应。此外，该技能还包括一个 Python 脚本，用于读取和管理电子邮件队列，该脚本具备列出待发送的电子邮件以及在邮件实际发送之前删除它们的功能。请注意，该技能允许代理通过将接收到的电子邮件内容存储到内存中并发送相应的回复来对邮件进行处理。
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["python3"]}}}
---
# Lel Mail

## 重要提示（若在云服务器/VPS上运行）  
- 部分云服务提供商会明确禁止使用电子邮件功能，这可能导致相关脚本无法正常运行；此时需要使用如 tailscale 等工具来绕过这些限制。

## 设置  
### 配置文件的设置  
创建 `~/.config/lel-mail/config.json` 文件：  
```json
[
  {
    "provider": "gmail",
    "config": {
        "smtp": {
        "server": "smtp.gmail.com", //Default url
        "port": 587 //Default port
      },
      "imap": {
        "server": "imap.gmail.com", //Default url
        "port": 993 //Default port
      }
    },
    "auth": {
      "user": "example@gmail.com",
      "password": "XXXX XXXX XXXX XXXX" //Gmail Requires App Specific Password Rather Than Your Normal Password
    },
    "can_send": true,
    "can_read": true
  }
]
```  

### 设置 cron 任务  
配置一个简单的 cron 任务，该任务每 5 分钟执行一次，并带有 30–90 秒的随机延迟。请与用户确认要使用的执行间隔：  
```bash
~/.openclaw/workspace/skills/lel-mail/scripts/email_sender_daemon.sh  
~/.openclaw/workspace/skills/lel-mail/scripts/check_email.sh <USER_EMAIL>  
~/.openclaw/workspace/skills/lel-mail/scripts/email_send.sh --sender <sender> --recipient <recipient> --subject <subject> --body <body> [--cc ...] [--bcc ...]  
```  
**注意**：使用 BCC/CC 时，请确保地址列表以逗号分隔。  

### 3. 管理待发送邮件队列  
待发送的邮件会按照随机时间间隔（30–90 秒）进行发送。您可以在邮件发送前查看或删除这些邮件。  

**查看所有待发送的邮件**：  
```bash
python3 ~/.openclaw/workspace/skills/lel-mail/scripts/manage_queue.py --list
```  

**按 ID 删除特定邮件**：  
```bash
python3 ~/.openclaw/workspace/skills/lel-mail/scripts/manage_queue.py --delete <ID>
```  

## 故障排除  
当出现因凭据缺失、配置错误等原因导致的故障时，需请求用户协助排查：  
- 如果邮件完全无法发送，请检查相关 cron 任务是否正在运行。