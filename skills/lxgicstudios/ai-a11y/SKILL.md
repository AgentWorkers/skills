---
name: a11y-checker
description: 使用人工智能技术扫描 HTML 和 JSX 文件中的可访问性问题，并提供相应的修复建议。
---

# A11y 检查器

扫描您的 HTML 和 JSX 文件，查找 WCAG 可访问性问题。提供实际的代码修复方案，而不仅仅是警告。

**一个命令即可完成所有修复工作。**

## 快速入门

```bash
npx ai-a11y ./src/components/Header.tsx
```

## 功能介绍

- 扫描 HTML/JSX 文件中的可访问性违规问题
- 识别不符合 WCAG 规范的内容
- 生成实际的修复代码，而不仅仅是警告
- 可用于单个文件或整个目录

## 使用示例

```bash
# Scan a single component
npx ai-a11y ./src/components/Button.tsx

# Scan all components
npx ai-a11y ./src/components/

# Scan with verbose output
npx ai-a11y ./src --verbose
```

## 常见问题检测

- 图片缺少 alt 文本
- 颜色对比度过低
- 表单标签缺失
- 键盘导航功能不完善
- ARIA 属性使用不当
- 聚焦管理问题

## 适用场景

- 在新功能上线前进行测试
- 审查现有的代码库
- 为满足可访问性标准做准备
- 作为持续集成/持续部署（CI/CD）流程中的可访问性检查环节

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。无需支付费用，也无需注册。

**了解更多信息：** https://github.com/LXGIC-Studios

## 系统要求

- Node.js 18.0 或更高版本
- 需要设置 `OPENAI_API_KEY` 环境变量

## 许可证

MIT 许可证。终身免费使用。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/ai-a11y](https://github.com/lxgicstudios/ai-a11y)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)