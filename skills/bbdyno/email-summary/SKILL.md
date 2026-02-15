---
name: email-summary
description: 从Gmail中获取最近的电子邮件，并提供简洁的摘要。当用户需要查看电子邮件、获取邮件摘要或查看收件箱内容时，可以使用此功能。
homepage: https://github.com/yourusername/email-summary-skill
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - GMAIL_CREDENTIALS_PATH
    os:
      - darwin
      - linux
      - win32
---

# 邮件摘要技能

该技能会从您的Gmail账户中获取最近的邮件，并提供由AI生成的摘要。

## 工作原理

当该技能被调用时，它会执行以下操作：

1. **使用`$GMAIL_CREDENTIALS_PATH`路径中的凭证**通过Gmail API进行身份验证。
2. **获取最近的邮件**（默认：最后10封未读邮件）。
3. **对每封邮件进行摘要总结**，包括：
   - 发件人和主题
   - 邮件正文中的关键内容
   - 建议的操作或回复方式。
4. **以结构清晰、易于阅读的格式呈现结果**。

## 代理的指令

当调用此技能时，请按照以下步骤操作：

1. 首先，确认`$GMAIL_CREDENTIALS_PATH`环境变量中确实存在Gmail API凭证文件。
2. 运行位于`{baseDir}/scripts/fetch_emails.py`的辅助脚本，并提供适当的参数：
   - 默认参数：`python3 {baseDir}/scripts/fetch_emails.py --count 10`
   - 带参数的调用方式：`python3 {baseDir}/scripts/fetch_emails.py $ARGUMENTS`
3. 解析脚本输出的JSON数据。
4. 对每封邮件提供以下内容的简洁摘要：
   - **发件人**：发件人的名称和电子邮件地址
   - **主题**：邮件的主题行
   **摘要**：邮件内容的2-3句话总结
   **建议的操作**：建议采取的行动（回复、归档、标记为待跟进等）。
5. 以格式良好的列表形式展示所有邮件的摘要。

## 使用示例

```
/email-summary
```
获取并总结最后10封未读邮件。

```
/email-summary --count 20
```
获取并总结最后20封未读邮件。

```
/email-summary --all
```
获取并总结所有未读邮件。

## 设置要求

在使用此技能之前，请确保：
- 已配置Gmail API凭证。
- 环境变量`GMAIL_CREDENTIALS_PATH`指向您的凭证JSON文件。
- 已安装Python 3及所需依赖包（详见README.md中的设置指南）。