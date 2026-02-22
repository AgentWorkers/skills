---
name: lel-mail
description: 通过结合使用 Python 和 Bash 脚本，以及主要的代理程序（用于处理推理和逻辑运算），来实现发送和接收电子邮件功能。
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["python3"]}}}
---
# Lel Mail

## 重要提示（若在云服务器/VPS上运行）  
- 部分云服务提供商会明确禁止发送电子邮件，这可能导致相关脚本无法正常工作。此时需要使用如 tailscale 等工具来绕过这些限制。

## 设置  
### 配置文件的设置  
创建 `~/.config/lel-mail/config.json`：  
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
创建一个简单的 cron 任务，该任务每 5 分钟执行一次，并带有 30–90 秒的随机延迟。请与用户确认要使用的执行间隔：  
```bash
~/.openclaw/workspace/skills/lel-mail/scripts/email_sender_daemon.sh  
~/.openclaw/workspace/skills/lel-mail/scripts/check_email.sh <USER_EMAIL>  
~/.openclaw/workspace/skills/lel-mail/scripts/email_send.sh --sender <sender> --recipient <recipient> --subject <subject> --body <body> [--cc ...] [--bcc ...]  
```  
**注意**：使用 BCC/CC 时，请确保地址列表以逗号分隔。  

## 故障排除  
当出现因凭据缺失、配置错误等原因导致的故障时，需请求用户协助排查问题。  
- 如果邮件根本无法发送，请检查相关 cron 任务是否正在运行。