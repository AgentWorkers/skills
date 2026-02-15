---
name: a11y-auditor
description: 扫描 HTML 和 JSX 文件中的可访问性问题，并提供修复建议。当需要在问题影响生产环境之前发现 WCAG（Web Content Accessibility Guidelines，网页内容无障碍指南）违规情况时，可以使用此工具。
---

# 可访问性审计工具

可访问性是网站设计中不可或缺的一部分，但手动检查其合规性却非常繁琐。这款工具会扫描您的 HTML 和 JSX 文件，检测 WCAG 规范中的违规之处，并明确指出问题所在以及相应的修复方法。再也不用猜测图片的替代文本是否正确，或者标题层次结构是否合理了。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-a11y src/
```

## 功能介绍

- 扫描 HTML 和 JSX 文件，检测 WCAG 2.1 AA 标准的违规情况
- 发现缺失的替代文本、错误的标题层次结构以及颜色对比度问题
- 生成具体的修复建议，并提供相应的代码示例
- 支持通配符模式，以便针对特定目录进行扫描
- 显示问题的严重程度，帮助您确定优先修复的环节

## 使用示例

```bash
# Scan your entire src directory
npx ai-a11y src/

# Scan specific component files
npx ai-a11y src/components/Button.tsx

# Scan all JSX files
npx ai-a11y "src/**/*.jsx"
```

## 最佳实践

- **在每次提交代码请求（PR）之前运行该工具**——在代码审核之前发现问题，而非之后
- **从访问量最大的页面开始检查**——优先修复那些被大量用户访问的页面
- **不要忽视警告**——今天的警告可能会成为明天的法律纠纷
- **结合手动测试使用**——自动化检查能发现约 30% 的可访问性问题，其余问题则需借助屏幕阅读器进行手动排查

## 适用场景

- 当您正在开发面向公众的 Web 应用程序且需要符合 WCAG 标准时
- 当您的团队没有专门的可访问性审核人员时
- 当您继承了一个完全没有考虑可访问性设计的代码库时
- 当您希望在手动审计之前发现明显的违规问题时

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发者工具之一。免费版本无付费门槛、无需注册，也不需要 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-a11y --help
```

## 工作原理

该工具会读取您的 HTML 或 JSX 文件并提取其 DOM 结构，然后根据 WCAG 2.1 标准检查常见的违规情况（如缺少标签、对比度不足、ARIA 标签使用不当等）。随后，它会将这些问题发送给 AI 模型，由模型生成具体的、可操作的修复建议及相应的代码示例。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。