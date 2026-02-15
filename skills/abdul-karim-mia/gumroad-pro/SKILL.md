---
name: gumroad-pro
description: "Gumroad提供了全面的商家管理功能，包括产品目录管理、销售数据分析、订阅服务监控、许可证密钥管理以及财务支付追踪。您可以在以下情况下使用这些功能：  
1. 查看销售量或收入报告；  
2. 管理产品的可用性和定价信息；  
3. 创建或编辑折扣代码；  
4. 验证或更换许可证密钥；  
5. 审计支付历史和即将到账的款项；  
6. 配置用于商店事件的自动化Webhook。"
---

# Gumroad Pro

这是一个高级的商家管理工具，用于管理您的数字产品。它支持交互式用户界面（按钮/编号列表）和直接的命令行界面（CLI）操作。

## 设置

使用此工具需要一个Gumroad访问令牌（Access Token）。该令牌可以存储在环境变量中（`GUMROAD_ACCESS_TOKEN`），或者作为技能配置中的`API_KEY`。

### 选项1（推荐）：简单的API密钥
```json
"skills": {
  "entries": {
    "gumroad-pro": {
      "apiKey": "your_token_here"
    }
  }
}
```

### 选项2：环境变量
```json
"skills": {
  "entries": {
    "gumroad-pro": {
      "env": {
        "GUMROAD_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

## 命令

### 交互式界面
- `/gp`、`/gumroad`、`/gumroad-pro` 或 `/gumroad_pro`：打开主控制中心。该界面在支持的平台上显示按钮（如Telegram、Discord），在其他平台上显示编号列表（如WhatsApp、Signal）。

### 技术参考（核心CLI命令）

#### 产品管理
- `gp products list`：列出所有产品的ID和详细信息。
- `gp products details --id <id>`：查看产品的完整规格和元数据。
- `gp products create --name <name> --price <cents> [--description <text>] [--url <custom_link>] [--taxable <bool_string>] [--currency <iso>]`
- `gp products update --id <id> --name <name> --price <cents> [--description <text>] [--url <link>]`
- `gp products enable/disable --id <id>`：切换产品的可见性。
- `gp products delete --id <id>`：永久删除产品。

#### 销售与收入分析
- `gp sales list [--after YYYY-MM-DD] [--before YYYY-MM-DD] [--page <key>] [--product_id <id>] [--email <addr>] [--order_id <id>]`
- `gp sales details --id <id>`：查看客户数据、自定义字段和发货状态。
- `gp sales refund --id <id> --amount <cents>`：默认为全额退款。
- `gp sales resend-receipt --id <id>`：重新发送购买收据。
- `gp sales mark-shipped --id <id> --tracking <url_or_number>`

#### 许可证与订阅管理
- `gp licenses verify/enable/decrement/rotate --product <id> --key <key>`
- `gp subscribers list --product <id>`：列出所有订阅用户。
- `gp subscribers details --id <sub_id>`：检查订阅状态和账单信息。

#### 收入与支付管理
- `gp payouts list [--after YYYY-MM-DD] [--before YYYY-MM-DD] [--page <key>] [--upcoming <false|true>]`
- `gp payouts details --id <id>`：查看支付处理的时间戳和处理器信息。

#### 产品定制（变体与分类）
- `gp variant-categories list/create/update/delete --product <id> --title <name>] [--id <cat_id>]`
- `gp variants list/create/update/delete --product <id> --category <cat_id> [--name <name>] [--price <diff_cents>] [--limit <max>] [--id <var_id>]`

#### 自定义结算字段
- `gp custom-fields list/create/update/delete --product <id> --name <name>] [--required <true|false>]`

#### 自动化（Webhooks）
- `gp subscriptions list [--type <event>]`
- `gp subscriptions create --url <url> --type <event_type>`
- `gp subscriptions delete --id <id>`

## LLM指导与操作协议

### CLI执行协议
- **Shell模式**：使用 `node skills/gumroad-pro/scripts/gumroad-pro.js <command> <subcommand> [flags]`。
- **标志敏感性**：布尔标志（如`--upcoming`或`--required`）必须以字符串形式传递（例如，`"false"`或`"true"`）。
- **价格处理**：所有价格输入均以**分**为单位（例如，$10.00表示为`1000`）。在创建工作流程时请务必明确这一点。

### 用户界面交互
- **重要提示**：在Telegram和Discord上，必须使用`message`工具配合`buttons`来显示主菜单和所有子菜单。**绝对不要**直接向用户显示原始文本列表或CLI输出。
- **自适应渲染**：在Telegram/WebChat上使用`buttons`和`edit`；在WhatsApp/Signal上使用`numbered lists`和`send`。
- **状态捕获**：多步骤操作（例如创建折扣）应使用`handler.js`中的`pending_input.json`状态模式。
- **主动提示**：在查看销售数据时，如果存在`license_key`，请始终提供“检查许可证”的选项。

### 安全性与完整性
- **确认要求**：在执行`delete`或`refund`操作前，必须先进行确认。
- **ID完整性**：始终使用`list`命令返回的ID；ID是区分大小写的。
- **错误处理**：如果出现`502`或`401`错误，请建议用户检查他们的`GUMROAD_ACCESS_TOKEN`。