---
name: pitch-gen
description: 使用人工智能生成创业演示文稿内容。适用于制作投资者推介材料或创业演示文稿。
---

# 演讲稿生成工具

需要向投资者展示你的创业想法，但面对空白的演示文稿却不知从何下手？这个工具可以帮你生成完整的演讲稿内容，包括问题描述、市场规模分析、商业模式、竞争分析等所有必要的幻灯片。所有这些内容通常都需要花费大量时间来撰写。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-pitch "AI-powered code review platform for teams"
```

## 工具功能

- 根据你的创业想法生成完整的演讲稿内容
- 制作具有吸引力的问题/解决方案幻灯片
- 提供市场规模估算（包括TAM/SAM/SOM等细分数据）
- 编写关于公司竞争优势和市场壁垒的分析
- 生成商业模式和市场推广策略相关的幻灯片

## 使用示例

```bash
# Generate pitch content from an idea
npx ai-pitch "marketplace for freelance AI engineers"

# Specify output format
npx ai-pitch "B2B SaaS for inventory management" --format markdown

# Focus on specific sections
npx ai-pitch "mobile app for pet owners" --sections problem,solution,market
```

## 使用建议

- **明确你的创业想法**：例如，“AI代码审查”这个描述比较模糊；而“针对金融科技领域的AI代码安全漏洞审查”则能生成更具体的内容。
- **提供目标市场的详细信息**：该工具无法自动判断你的产品面向哪些客户。
- **将此工具作为起点**：生成的文档只是一个初稿，你需要结合自己的见解和数据进行完善。
- **多次运行工具**：多次运行可以获取不同的分析结果，从中挑选最合适的部分。

## 适用场景

- 当你在准备第一份演讲稿时不知道从何开始
- 需要快速原型化你的创业想法以向投资者展示
- 希望有一个框架来填充你自己的调研数据和信息
- 在头脑风暴中确定如何与竞争对手区分开来

## 该工具属于LXGIC开发工具包的一部分

LXGIC Studios提供了110多种免费开发者工具，这个工具就是其中之一。免费版本无需支付费用、无需注册，也不需要API密钥，直接使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。

```bash
npx ai-pitch --help
```

## 工作原理

该工具会根据你的创业想法，通过结构化的提示生成演讲稿的各个部分。它利用GPT技术，参考成功的演讲稿模板，为每张幻灯片生成适合投资者的文本内容。

## 许可证

采用MIT许可证，永久免费。你可以自由使用该工具。