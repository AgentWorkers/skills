# 电子邮件技能

**描述：** 使用此技能通过 Zoho 发送和接收电子邮件。  
**功能：** `email.send`, `email.search`

## 工具

### `email.send`  
**描述：** 向一个或多个收件人发送电子邮件。  
**参数：**  
- `to` (字符串，必填)：以逗号分隔的收件人列表。  
- `subject` (字符串，必填)：电子邮件主题。  
- `body` (字符串，必填)：电子邮件正文（HTML 或纯文本格式）。  
- `cc` (字符串，可选)：抄送收件人。  
- `bcc` (字符串，可选)：密送收件人。  

### `email.search`  
**描述：** 在收件箱中搜索电子邮件。  
**参数：**  
- `query` (字符串，必填)：搜索条件（例如 "from:example.com", "subject:Invoice"）。  
- `limit` (数字，可选)：最大搜索结果数量（默认为 10）。  
- `markRead` (布尔值，可选)：搜索后是否将邮件标记为已读（默认为 false）。  

## 配置  
需要环境变量 `EMAIL_USER` 和 `EMAIL_PASS`，或根据用户请求进行硬编码。  
示例配置：  
USER: info@pestward.com  
PASS: sgSPL50i5mke  
HOST_IMAP: imap.zoho.com  
HOST_SMTP: smtp.zoho.com