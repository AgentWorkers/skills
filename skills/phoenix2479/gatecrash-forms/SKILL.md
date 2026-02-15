---
name: gatecrash-forms
description: 这是一个以命令行界面（CLI）为主的表单生成工具，遵循“按需构建（Build-What-You-Need, BYOK）”的设计理念。该工具能够根据 JSON 数据结构生成美观的 HTML 表单，通过用户自有的 SMTP 服务器处理表单提交，并将响应数据存储在本地。我们的核心功能是修复现有的系统漏洞（“crash gates”），而非不断开发新的系统组件。
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

**基于 CLI 的表单生成工具，遵循“Bring Your Own Keys”（BYOK）的设计理念**

该工具能够根据 JSON 模式生成美观且安全的 HTML 表单。所有电子邮件通知通过您的 SMTP 服务器发送，表单响应数据存储在您的基础设施上。无需依赖任何外部服务，也没有任何限制或管控。

## 快速入门

### 生成表单

```bash
./scripts/generate.sh examples/feedback.json output.html
```

### 启动服务器

```bash
./scripts/serve.sh 3000
```

访问 http://localhost:3000 可查看所有表单。

### 初始化项目

```bash
./scripts/init.sh
```

系统会自动创建 `forms/` 和 `responses/` 两个目录，并在其中生成示例表单。

## 主要特性

- 🎨 **8 种以上字段类型**：文本、电子邮件、文本区域、下拉菜单、单选按钮、复选框、评分/等级选择、日期输入
- 🔒 **强化安全性**：防止 XSS 攻击、使用 CSRF 令牌、设置垃圾邮件防护机制、实施速率限制
- 📧 **支持自定义 SMTP 服务器**：您可以使用自己的 SMTP 服务（如 Zoho、Gmail、SendGrid 等）
- 💾 **本地数据存储**：表单响应数据以 JSON 或 CSV 格式保存
- 🎨 **美观的用户界面**：采用渐变紫色主题，支持响应式设计
- 🚀 **可自托管**：可在任何支持 Node.js 的环境中部署

## 配置

您可以全局配置 SMTP 信息：

```bash
gatecrash-forms config smtp.host smtp.zoho.in
gatecrash-forms config smtp.port 465
gatecrash-forms config smtp.secure true
gatecrash-forms config smtp.auth.user your-email@example.com
gatecrash-forms config smtp.auth.pass your-password
```

或者根据具体需求在 JSON 模式中为每个表单单独设置配置。

## 表单示例模板

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

- **客户反馈**：收集产品/服务的使用反馈
- **联系表单**：用于网站的简单联系表单
- **活动注册**：用于研讨会/活动的报名表单
- **调查问卷**：用于市场调研或用户调查
- **潜在客户获取**：无需借助第三方服务即可收集潜在客户信息

## 设计理念：我们“突破限制”（We “crash gates”）

GateCrash Forms 并不是一个服务，而是一个工具开发平台。所有关键资源（SMTP 服务器、数据存储、部署环境、数据存储）都由您自行控制。

- ✅ SMTP 服务器：由您负责管理（用于发送电子邮件通知）
- ✅ 数据存储：由您负责（表单响应数据存储在您的服务器上）
- ✅ 部署环境：您可以自由选择（在任何支持 Node.js 的环境中部署）
- ✅ 数据所有权：您完全拥有（数据存储在您的服务器上，无外部服务器参与）

**无 GateCrash 账户**，**无 GateCrash 服务器**，**无任何限制或管控**。

## 链接

- **GitHub 仓库**：https://github.com/Phoenix2479/gatecrash-forms
- **npm 包**：https://www.npmjs.com/package/gatecrash-forms
- **项目宣言**：请阅读项目中的 `MANIFESTO.md`
- **完整文档**：详见 `README.md`

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

## 许可证

MIT 许可证——您可以自由使用、修改或出售该工具，但请不要对其进行任何限制或管控。

---

*由 Dinki 和 Molty 制作*

**“我们致力于突破各种限制，而非新建限制。”**