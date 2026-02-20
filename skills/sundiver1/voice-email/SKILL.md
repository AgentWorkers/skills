---
name: voice-email
version: 1.0.0
description: 通过自然语音命令发送电子邮件——专为提升用户体验和可访问性而设计
---
# 语音邮件功能

通过自然的语音命令发送电子邮件，非常适合辅助技术（accessibility）场景的使用。

## 功能概述

当您收到语音消息时，系统会解析该消息并发送相应的电子邮件：

**输入格式：**
```
new email to [recipient], subject [subject], body [body], send
```

**示例：**
- “new email to john@example.com, subject Hello, body How are you doing, send”  
- “send email to mom@gmail.com, subject Dinner, body See you at 7pm, send”  

## 安装要求

1. **gogcli**：用于操作Gmail的Google命令行工具  
2. **Deepgram**：用于将语音转换为文本  
3. **Telegram**：用于接收语音消息  

### 安装gogcli  
```bash
curl -sL https://gogcli.ai/install.sh | bash
gog auth add your-email@gmail.com
```

### 配置Deepgram  
将以下配置添加到`openclaw.json`文件中：  
```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "models": [{ "provider": "deepgram", "model": "nova-3" }]
      }
    }
  }
}
```

## 工作原理

1. 用户通过Telegram发送语音消息  
2. Deepgram将语音转换为文本  
3. 系统解析消息中的收件人、主题和正文信息  
4. 系统通过`gog gmail send --to "..." --subject "..." --body "..."`命令发送电子邮件  
5. 系统会确认邮件发送是否成功  

## 命令解析规则

系统会提取以下信息：  
- `to`：电子邮件地址（通常位于“to”、“email to”或“send to”之后）  
- `subject`：邮件主题（位于“subject”之后）  
- `body`：邮件正文（位于“body”之后，但在“send”之前）  

## 使用方法

只需使用相应的语音命令发送消息，系统会：  
1. 将语音转换为文本  
2. 解析邮件信息  
3. 发送电子邮件  
4. 通过语音或文本方式确认邮件发送结果  

## 示例命令  

- “new email to john@example.com, subject Hello, body Just saying hi, send”  
- “email to mom, subject Check this out, body Here’s what I found, send”  
- “send email to boss@company.com, subject Project Update, body Phase one complete, send”