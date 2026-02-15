---
name: tailwind-config-gen
description: 根据品牌颜色生成 `tailwind.config.js` 文件。在设置 Tailwind CSS 时使用该文件。
---

# Tailwind 配置生成器

如果您拥有品牌颜色，那么这个工具可以帮助您生成完整的 Tailwind CSS 配置文件。它可以根据您提供的颜色生成一个完整的主题。

**只需一个命令，无需任何额外的配置设置，即可立即使用。**

## 快速入门

```bash
npx ai-tailwind "#FF4500" "#1A1A2E"
```

## 功能介绍

- 从您提供的品牌颜色出发，生成完整的颜色调色板
- 生成 `tailwind.config.js` 文件
- 包含颜色的渐变版本以及具有语义意义的颜色名称（如 `success`、`error`、`warning` 等）

## 使用示例

```bash
# Two colors
npx ai-tailwind "#FF4500" "#1A1A2E"

# Three colors
npx ai-tailwind "#3B82F6" "#10B981" "#F59E0B" -o tailwind.config.js
```

## 最佳实践

- **首先确定品牌的主要颜色和辅助颜色**
- **生成这些颜色的渐变版本（范围：50% 到 950%）**
- **包含具有语义意义的颜色（如成功、错误、警告等状态的颜色）**
- **测试颜色对比度**——良好的颜色对比度对用户体验至关重要

## 适用场景

- 设置新的 Tailwind 项目
- 实施品牌设计规范
- 创建设计系统
- 生成颜色调色板

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本没有任何付费限制、注册要求或 API 密钥，只需使用即可。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-tailwind --help
```

## 工作原理

该工具会接收您提供的十六进制颜色代码，然后生成一个包含完整颜色渐变效果、具有语义命名以及合理颜色关系的 Tailwind CSS 主题。

## 许可证

采用 MIT 许可协议，永久免费。您可以随心所欲地使用该工具。