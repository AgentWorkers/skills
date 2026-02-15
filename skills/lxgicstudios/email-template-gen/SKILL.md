---
name: email-template-gen
description: 生成响应式电子邮件模板。在构建交易类电子邮件时使用这些模板。
---

# 电子邮件模板生成器

当前的电子邮件HTML设计仍然停留在1999年的水平：使用表格、内联样式以及针对Outlook的特殊技巧。只需描述您的需求，我们就能为您生成一个在所有邮件客户端中都能正常使用的模板。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-email-template "welcome email with verify button"
```

## 功能介绍

- 生成响应式电子邮件模板
- 支持Gmail、Outlook、Apple Mail等邮件客户端
- 支持HTML、React Email和MJML格式
- 提供暗黑模式支持

## 使用示例

```bash
# Welcome email
npx ai-email-template "welcome email with verify button"

# Order confirmation
npx ai-email-template "order confirmation with items table" -f react

# Password reset
npx ai-email-template "password reset" -o reset.html

# Newsletter
npx ai-email-template "weekly newsletter with header and article cards"
```

## 最佳实践

- **在Litmus或Email on Acid中进行测试**——不同的邮件客户端可能有不同的显示效果
- **保持布局简单**——复杂的布局在Outlook中可能会出问题
- **谨慎使用网页字体**——许多邮件客户端不支持这些字体
- **务必包含纯文本**——有些人更喜欢阅读纯文本邮件

## 适用场景

- 构建事务性邮件系统
- 创建营销邮件模板
- 更新旧版的电子邮件模板
- 为React Email项目提供模板起点

## 属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要API密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。运行时需要设置`OPENAI_API_KEY`环境变量。

```bash
npx ai-email-template --help
```

## 工作原理

根据您的描述，该工具会生成适用于各种邮件客户端的基于表格的电子邮件模板。对于React Email格式，它会生成相应的组件；对于MJML格式，它会生成能够安全地转换为HTML的标记语言。

## 许可证

采用MIT许可证，永久免费。您可以随心所欲地使用该工具。