---
name: gatecrash-forms
description: 这是一个以命令行界面（CLI）为主的设计工具，遵循“按需构建（Build-On-Request, BYOK）”的开发理念。它能够根据 JSON 数据结构自动生成美观的 HTML 表单，通过用户自定义的 SMTP 服务器处理表单提交，并将响应数据存储在本地。该工具是 Kimi Claw 的原生组件。我们的策略是“修复现有问题”，而非不断创建新的功能或组件。
metadata:
  {
    "openclaw":
      {
        "emoji": "🚀",
        "requires": { "bins": ["gatecrash-forms", "node"] },
        "install":
          [
            {
              "id": "npm-global",
              "kind": "node",
              "package": "gatecrash-forms",
              "bins": ["gatecrash-forms"],
              "label": "Install GateCrash Forms globally (npm)",
            },
          ],
      },
  }
---
# GateCrash Forms 技能

**基于 CLI 的表单生成工具，遵循“BYOK”（Bring Your Own Keys）理念**

该工具能够根据 JSON 模式生成美观且安全的 HTML 表单。所有邮件通知通过您的 SMTP 服务器发送，表单响应数据存储在您的基础设施上。无需依赖任何外部服务，也没有任何访问限制。

## ✨ 适用于 Kimi Claw

**完美适配 Kimi 的 24/7 在线助手：**
- ✅ 可在 Kimi.com 的浏览器标签页中直接使用
- ✅ 通过 ClawHub 的 5,000 多个技能库进行安装
- ✅ 提供 40GB 的云存储空间用于保存表单响应数据
- ✅ 支持多种便捷的邮件发送服务（agentmail.to、Resend 等）

现在，您的人工智能助手可以为您生成和管理表单了！

## 快速入门

### 生成表单
```bash
./scripts/generate.sh examples/feedback.json output.html
```

### 启动服务器
```bash
./scripts/serve.sh 3000
```

访问 http://localhost:3000 可查看所有生成的表单。

### 初始化项目
```bash
./scripts/init.sh
```

系统会自动创建 `forms/` 和 `responses/` 两个目录，并在其中生成示例表单。

## 主要功能

- 🎨 **支持 8 种字段类型：** 文本、电子邮件、文本区域、下拉菜单、单选按钮、复选框、评分等级、日期选择
- 🔒 **强化安全性：** 防止 XSS 攻击、CSRF 令牌、垃圾邮件防护机制、速率限制
- 📧 **支持自定义邮件发送：** 使用您自己的 SMTP 服务器（Zoho、Gmail、SendGrid 等）
- 💾 **本地数据存储：** 表单响应数据可保存为 JSON 或 CSV 格式
- 🎨 **美观的用户界面：** 采用渐变紫色主题，响应式设计
- 🚀 **可自定义部署：** 可在支持 Node.js 的任何环境中部署

## 配置

您可以全局配置 SMTP 信息：
```bash
gatecrash-forms config smtp.host smtp.example.com
gatecrash-forms config smtp.port 465
gatecrash-forms config smtp.secure true
gatecrash-forms config smtp.auth.user your-email@example.com
gatecrash-forms config smtp.auth.pass your-password
```

或者根据具体需求在 JSON 模式中进行个性化配置。

## 示例表单结构
```json
{
  "title": "Customer Feedback",
  "description": "We'd love to hear from you!",
  "fields": [
    {
      "type": "scale",
      "name": "rating",
      "label": "Overall satisfaction",
      "min": 1,
      "max": 5,
      "required": true
    },
    {
      "type": "checkbox",
      "name": "topics",
      "label": "What interested you most?",
      "options": ["Product", "Service", "Price", "Experience"]
    },
    {
      "type": "textarea",
      "name": "comments",
      "label": "Additional comments",
      "maxLength": 500
    }
  ],
  "submit": {
    "email": "your-email@example.com",
    "storage": "responses/feedback.json"
  }
}
```

## 使用场景

- **客户反馈：** 收集产品/服务使用反馈
- **联系表单：** 网站上的简单联系表单
- **活动注册：** 工作坊/活动的报名表单
- **调查问卷：** 市场调研或用户调查
- **潜在客户获取：** 无需第三方服务即可捕获潜在客户信息

## 开发理念：我们专注于“打破限制”（“We crash gates”）

GateCrash Forms 并非一个独立的服务，而是一个工具开发平台。所有核心功能都由您自行掌控：
- ✅ 您负责邮件通知的发送（通过 SMTP 服务器）
- ✅ 表单响应数据的存储（使用您的存储系统）
- ✅ 项目的部署（可在任意地方进行）
- ✅ 数据的所有权（数据存储在您的服务器上，无外部服务器参与）

**无需注册 GateCrash 账户或使用其服务器，也没有任何访问限制。**

## 链接

- **GitHub：** https://github.com/Phoenix2479/gatecrash-forms
- **npm：** https://www.npmjs.com/package/gatecrash-forms
- **项目宣言：** 详细阅读 `MANIFESTO.md` 文件
- **文档：** 完整的文档请参阅 `README.md`

## 命令参考
```bash
# Generate form from schema
gatecrash-forms generate schema.json output.html

# Start HTTP server
gatecrash-forms serve [port]

# Set global config
gatecrash-forms config <key> <value>

# Initialize project
gatecrash-forms init

# Show help
gatecrash-forms help
```

## 许可协议

MIT 许可协议——您可以自由使用、修改或出售该工具，但请勿设置任何访问限制。

---

*由 Dinki 和 Molty 创作*

**“我们致力于‘打破限制’，而非构建新的限制。”**