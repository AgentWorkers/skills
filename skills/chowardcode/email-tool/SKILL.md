# 电子邮件技能

**描述：** 使用此技能可以发送和接收电子邮件（支持 IMAP/SMTP 协议）。该技能专为 Zoho Mail 设计，但也可进行自定义配置。  
**功能：** `email.send`、`email.search`

## 工具

### `email.send`  
向一个或多个收件人发送电子邮件。  

**参数：**  
- `to` (字符串，必填)：以逗号分隔的收件人列表。  
- `subject` (字符串，必填)：电子邮件主题。  
- `body` (字符串，必填)：电子邮件正文（支持 HTML 或纯文本格式）。  
- `cc` (字符串，可选)：抄送收件人。  
- `bcc` (字符串，可选)：密送收件人。  

### `email.search`  
在收件箱中搜索电子邮件。  

**参数：**  
- `query` (字符串，必填)：搜索条件（例如：`from:example.com`、`subject:Invoice`）。  
- `limit` (数字，可选)：返回的最大结果数量（默认值：10）。  
- `markRead` (布尔值，可选)：搜索完成后将邮件标记为已读（默认值：false）。  

## 配置（严禁硬编码敏感信息）  
此技能 **严禁** 包含任何敏感信息（如用户名和密码）。  

敏感信息将从以下两种方式之一获取：  
1) JSON 文件 `%OPENCLAW_SECRETS_DIR%/email-tool.json`（推荐方式）；  
2) 环境变量（备用方式）。  

**必填配置项：**  
- `EMAIL_USER`  
- `EMAIL_PASS`  

**可选配置项（显示默认值）：**  
- `HOST_IMAP` (imap.zoho.com)  
- `PORT_IMAP` (993)  
- `HOST_SMTP` (smtp.zoho.com)  
- `PORT_SMTP` (465)  
- `SECURE_SMTP` (true)  

**注意事项：**  
在打包或上传此技能之前，请先运行 `node scripts/secret-scan.js` 脚本，以确保没有敏感信息被泄露。