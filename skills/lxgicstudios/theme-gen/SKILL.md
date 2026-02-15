---
name: theme-gen
description: **使用 AI 从品牌颜色生成完整的设计系统**  
适用于新项目启动或需要统一颜色方案的场景。
---

# 主题生成器

只需提供您的品牌颜色，即可获得一个完整的设计系统，其中包括语义化标记、颜色渐变以及可直接使用的 CSS 变量或 Tailwind 配置文件。再也不用手动选择九种不同的蓝色色调了。

**一个命令，零配置，即可使用。**

## 快速入门

```bash
npx ai-theme --primary "#3B82F6" --secondary "#10B981"
```

## 功能介绍

- 根据您提供的基础颜色（50 至 950 级）生成完整的颜色渐变系列
- 创建诸如“成功”（success）、“警告”（warning）、“错误”（error）、“信息”（info）等语义化标记
- 输出 CSS 自定义属性或 Tailwind 配置文件，或同时输出两者
- 确保前景色与背景色之间的对比度符合可访问性标准
- 生成统一的空间布局和字体样式规则

## 使用示例

```bash
# Generate from primary color only
npx ai-theme --primary "#6366F1"

# Full brand palette
npx ai-theme --primary "#3B82F6" --secondary "#10B981" --accent "#F59E0B"

# Output Tailwind config
npx ai-theme --primary "#8B5CF6" --format tailwind

# Include dark mode variants
npx ai-theme --primary "#EC4899" --dark-mode

# Export to file
npx ai-theme --primary "#14B8A6" -o ./theme.css
```

## 最佳实践

- **从您的主题色开始**：主要颜色决定了整个设计的基调，请先确定好这个颜色。
- **不要随意修改生成的渐变方案**：这些渐变方案是经过数学计算平衡后的结果，请相信系统的输出。
- **在实际项目中测试**：将生成的变量应用到项目中，查看它们在用户界面上的效果。
- **生成后进行个性化调整**：以该工具为起点，再对个别颜色进行微调。

## 适用场景

- 开始新项目时需要快速建立颜色系统
- 客户提供了单一品牌颜色，但要求您提供完整的配色方案
- 将杂乱无章的代码库转换为统一的设计规范
- 在设计初期探索颜色选项

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-theme --help
```

## 工作原理

该工具根据您提供的基础颜色，运用色彩理论原理生成和谐的渐变系列。它会计算每个颜色点的亮度值，以确保渐变中的每个颜色段都具有适当的对比度，然后将这些颜色映射到具体的用途（如背景色、文本颜色和交互状态）。

## 许可证

MIT 许可协议。永久免费使用，可按需自由使用。