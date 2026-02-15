---
name: migma
description: 通过 Migma CLI，您可以从终端生成、发送、验证并导出由 AI 支持的电子邮件；同时还可以管理联系人、邮件分组、标签、域名以及 Webhook 设置。
metadata:
  openclaw:
    requires:
      env:
        - MIGMA_API_KEY
      bins:
        - migma
    primaryEnv: MIGMA_API_KEY
    emoji: "\u2709"
    homepage: https://migma.ai
    install:
      - kind: node
        package: "@migma/cli"
        bins: [migma]
---

# Migma

使用人工智能创建并发送专业的、符合品牌风格的电子邮件。您的代理可以根据提示设计电子邮件，通过托管的域名立即发送，并管理整个受众群体——所有这些操作都可以在终端中完成。

请始终使用 `--json` 选项以获得结构化的输出。

## 首次设置

如果用户尚未进行设置，请按照以下步骤操作一次：

```bash
# 1. Create an instant sending domain (no DNS needed)
migma domains managed create <companyname> --json
# → Sends from: hello@<companyname>.migma.email

# 2. Set a default project (brand)
migma projects list --json
migma projects use <projectId>
```

## 创建电子邮件

当用户请求创建、设计或生成电子邮件时：

```bash
migma generate "Welcome email for new subscribers" --wait --json
```

`--wait` 标志会等待人工智能完成处理。JSON 响应中包含 `conversationId`、`subject` 和 `html`。

若要将生成的 HTML 保存到本地，请添加 `--save ./email.html`。若要包含参考图片（截图或设计原型图），请添加 `--image <url>`。

## 发送电子邮件

当用户请求向某人发送电子邮件时：

```bash
# Send a generated email directly
migma send --to sarah@example.com --subject "Welcome!" \
  --from-conversation <conversationId> \
  --from hello@company.migma.email --from-name "Company" --json

# Or send from a local HTML file
migma send --to sarah@example.com --subject "Hello" \
  --html ./email.html \
  --from hello@company.migma.email --from-name "Company" --json

# Send to an entire segment or tag
migma send --segment <id> --subject "Big News" --html ./email.html \
  --from hello@company.migma.email --from-name "Company" --json

# Personalize with template variables
migma send --to user@example.com --subject "Hi {{name}}" --html ./email.html \
  --from hello@company.migma.email --from-name "Company" \
  --var name=Sarah --var discount=20 --json
```

`--from-conversation` 会自动导出生成的电子邮件中的 HTML 内容——无需单独进行导出操作。

## 验证电子邮件

当用户希望在发送前检查电子邮件时：

```bash
migma validate all --html ./email.html --json
migma validate all --conversation <conversationId> --json
```

系统会返回总体评分以及各项检查结果：兼容性（支持 30 多种电子邮件客户端）、链接是否有效、拼写/语法错误以及邮件的送达率/垃圾邮件评分。具体检查项目包括：`migma validate compatibility`、`links`、`spelling`、`deliverability`。

## 导出到邮件服务提供商（ESP）或下载文件

当用户希望将电子邮件内容导出到邮件服务提供商或下载文件时：

```bash
migma export html <conversationId> --output ./email.html
migma export klaviyo <conversationId> --json
migma export mailchimp <conversationId> --json
migma export hubspot <conversationId> --json
migma export pdf <conversationId> --json
migma export mjml <conversationId> --json
```

## 管理联系人

```bash
migma contacts add --email user@example.com --firstName John --json
migma contacts list --json
migma contacts import ./contacts.csv --json
migma contacts remove <id> --json
```

## 管理标签和受众群体

```bash
migma tags create --name "VIP" --json
migma tags list --json
migma segments create --name "Active Users" --description "..." --json
migma segments list --json
```

## 导入品牌信息

当用户希望从网站导入新的品牌信息时：

```bash
migma projects import https://yourbrand.com --wait --json
migma projects use <projectId>
```

系统会自动获取品牌的标志、颜色、字体和品牌风格。

## 错误处理

在发生错误时，`--json` 选项会返回详细的错误信息：

```json
{"error": {"message": "Not found", "code": "not_found", "statusCode": 404}}
```