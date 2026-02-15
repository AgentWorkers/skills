---
name: css-to-tailwind
description: 将 CSS 文件转换为 Tailwind 公用类。在从传统 CSS 迁移到 Tailwind 时使用此方法。
---

# CSS 到 Tailwind 的转换工具

将 CSS 代码迁移到 Tailwind 框架意味着需要将数百条 CSS 规则重写为相应的实用类（utility classes）。没人愿意手动完成这项工作。这款工具可以读取您的 CSS 文件，并将其转换为等效的 Tailwind 类，从而让您能够专注于处理那些复杂或边缘性的问题。

**只需一个命令，无需任何配置，即可完成转换。**

## 快速入门

```bash
npx ai-css-to-tailwind styles.css
```

## 工具功能

- 读取 CSS 文件，并将其中的规则转换为 Tailwind 实用类
- 支持常见的属性，如内边距（padding）、外边距（margin）、颜色（colors）、字体样式（typography）以及弹性布局（flexbox）
- 保留原有的类结构，便于您将旧类映射到新的 Tailwind 类中
- 处理媒体查询（media queries），将其转换为 Tailwind 的响应式前缀（responsive prefixes）
- 生成一个映射文件，显示旧 CSS 规则与新的 Tailwind 类之间的对应关系

## 使用示例

```bash
npx ai-css-to-tailwind styles.css
npx ai-css-to-tailwind src/styles/
npx ai-css-to-tailwind "src/**/*.css"
```

## 最佳实践

- **一次转换一个文件**：这样更容易验证转换结果
- **检查自定义值**：Tailwind 有固定的单位规范，自定义的像素值可能需要更新主题配置（theme config）
- **保留旧 CSS 代码作为备份**：在确认所有内容都正常工作之前，请勿删除旧代码

## 适用场景

- 将现有项目迁移到 Tailwind 框架
- 将组件库中的 CSS 代码转换为 Tailwind 实用类
- 了解您的 CSS 代码对应的 Tailwind 类

## 本工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发工具之一。免费版本无需支付费用、注册账号或使用 API 密钥，只需使用命令行工具即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

## 工作原理

该工具会解析您的 CSS 文件，将每一对属性值（property-value pair）映射到最接近的 Tailwind 实用类。对于存在歧义的转换或没有直接对应关系的自定义值，工具会利用人工智能进行处理。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。