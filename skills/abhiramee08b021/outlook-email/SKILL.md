---
name: outlook
emoji: f4e7
description: 通过 Microsoft Graph API 使用 Microsoft Outlook/Live.com 邮件客户端：可以执行邮件列表查询、搜索、阅读、发送以及回复操作。
homepage: https://github.com/abhiramee08b021/outlook-cli
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "bins": ["python3"], "python_packages": ["requests"] },
        "install":
          [
            {
              "id": "manual",
              "kind": "manual",
              "label": "Requires Azure AD app registration",
            },
          ],
      },
  }
---

# Outlook CLI

这是一个用于 Microsoft Outlook/Live/Hotmail 的命令行电子邮件客户端，它通过 Microsoft Graph API 进行操作。

## 设置

1. **创建 Azure AD 应用程序：**  
   访问 [Azure Portal](https://portal.azure.com) → **应用注册**  
   - 应用程序名称：`outlook-cli`  
   - 账户类型：仅限“个人 Microsoft 账户”  
   - 重定向 URI：`http://localhost:8080/callback`  

2. 从应用程序注册中获取凭据。  

3. **配置：**  
   ```bash
   outlook configure
   ```  

4. **身份验证：**  
   ```bash
   outlook auth
   ```  

## 命令

| 命令 | 描述 |
|---------|-------------|
| `outlook list [n]` | 列出最近的电子邮件 |
| `outlook search "query" [n]` | 搜索电子邮件 |
| `outlook read <id>` | 通过 ID 读取电子邮件 |
| `outlook send --to ...` | 发送电子邮件 |
| `outlook reply <id>` | 回复电子邮件 |
| `outlook status` | 检查身份验证状态 |

## 示例

**列出电子邮件：**  
```bash
outlook list 20
```  

**搜索：**  
```bash
outlook search "from:linkedin.com"
outlook search "subject:invoice"
```  

**发送邮件：**  
```bash
outlook send --to "user@example.com" --subject "Hello" --body "Message"
outlook send --to "a@x.com,b@x.com" --cc "boss@x.com" --subject "Update" --body-file ./msg.txt
```  

**回复邮件：**  
```bash
outlook reply EMAIL_ID --body "Thanks!"
outlook reply EMAIL_ID --all --body "Thanks everyone!"
```  

## 搜索操作符

- `from:email@domain.com` - 发件人  
- `subject:keyword` - 主题行  
- `body:keyword` - 电子邮件正文  
- `received:YYYY-MM-DD` - 收件日期  
- `hasattachment:yes` - 是否包含附件  

## 文件

- `SKILL.md` - 本文档  
- `outlook` - 主要的 CLI 脚本  
- `README.md` - 完整的文档说明