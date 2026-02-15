---
name: landing-gen
description: 根据您的 `package.json` 文件内容，您可以生成一个美观的 HTML 登陆页面。当您需要为项目快速创建一个营销页面时，可以使用这个方法。
---

# 登陆页生成器

您刚刚发布了一个软件包，现在需要一个登录页，但又不想花费两小时去处理 HTML 和 CSS 的细节。这个工具可以读取您的 `package.json` 文件，并通过一个命令生成一个完整且外观精美的登录页。无需配置模板或进行任何设计决策。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-landing .
```

## 功能介绍

- 读取您的 `package.json` 文件，提取项目名称、描述、功能以及仓库链接
- 生成一个包含标题栏、功能展示区和呼叫行动按钮（CTA）的格式化 HTML 登陆页
- 输出一个名为 `landing.html` 的文件，您可以将其部署到任何地方
- 自动支持响应式设计，确保在移动设备上也能良好显示
- 预置了正确的元标签和语义化的 HTML 结构

## 使用示例

```bash
# Generate from current directory
npx ai-landing .

# Generate from a specific project
npx ai-landing ~/projects/my-cool-lib

# Custom output file
npx ai-landing . -o index.html
```

## 最佳实践

- **先编写一份高质量的 `package.json` 描述**：描述越详细，生成的登录页内容就越完善
- **在 `package.json` 中添加关键词**：这些关键词将作为页面上的功能亮点显示
- **部署到 GitHub Pages**：生成的文件是一个独立的 HTML 文件，非常适合用于 GitHub Pages
- **进行个性化调整**：将其作为起点，然后根据您的品牌风格修改颜色和文本内容

## 适用场景

- 您刚刚发布了 npm 包，需要快速搭建一个登录页
- 您需要为黑客马拉松项目创建一个演示页面
- 在构建正式网站之前，需要一个临时占位页面
- 您的开源项目需要比简单的 GitHub README 文件更好的第一印象

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本没有任何付费门槛、注册要求或 API 密钥限制，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-landing --help
```

## 工作原理

该工具会解析您的 `package.json` 文件以提取项目元数据，然后将这些信息发送给 AI 模型，由模型生成结构清晰、语义正确的 HTML 代码。最终生成的文件是一个独立的登录页，可以直接在浏览器中打开或部署到任何静态服务器上。

## 许可协议

MIT 许可协议。永久免费，您可以随意使用该工具。