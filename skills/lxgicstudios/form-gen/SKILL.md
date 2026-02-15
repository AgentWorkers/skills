---
name: form-gen
description: 生成带有验证功能的表单组件。在构建表单时可以使用这些组件。
---

# 表单生成器

填写表单是一件繁琐的事情，而表单验证更是令人头疼。只需描述您需要的字段，即可获得一个包含验证功能的完整表单组件。

**一个命令即可完成所有操作，无需任何配置。**  

## 快速入门

```bash
npx @lxgicstudios/ai-form "signup form with email, password, name"
```

## 功能介绍

- 生成 React 表单组件  
- 集成 `react-hook-form` 和 `zod` 进行表单验证  
- 处理错误状态并确保表单的可访问性  
- 支持 TypeScript（默认启用）  

## 使用示例

```bash
# Signup form
npx @lxgicstudios/ai-form "signup form with email, password, name"

# Checkout form with TypeScript
npx @lxgicstudios/ai-form "checkout form with address and payment" -t

# Contact form to file
npx @lxgicstudios/ai-form "contact form" -o ContactForm.tsx -t
```

## 最佳实践  

- **使用 TypeScript**：在编译时捕获错误  
- **显示即时错误提示**：无需等到提交时才显示错误信息  
- **添加加载状态**：在提交过程中显示进度条  
- **使用键盘进行测试**：确保表单对所有用户都是可访问的  

## 适用场景  

- 需要快速创建表单（无需编写繁琐的代码）  
- 需要设置表单验证规则  
- 用于原型设计（确保表单功能正常）  
- 学习如何使用 `react-hook-form` 和 `zod`  

## 属于 LXGIC 开发工具包  

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥。这些工具都能直接使用。  

**了解更多信息：**  
- GitHub: https://github.com/LXGIC-Studios  
- Twitter: https://x.com/lxgicstudios  
- Substack: https://lxgicstudios.substack.com  
- 官网: https://lxgic.dev  

## 使用要求  

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。  

```bash
npx @lxgicstudios/ai-form --help
```

## 工作原理  

该工具会根据您提供的表单描述自动识别字段及其验证规则，然后使用 `react-hook-form` 管理表单状态，并通过 `zod` 定义验证规则，最终生成完整的 React 表单组件。  

## 许可证  

采用 MIT 许可协议，永久免费。您可以自由使用该工具。