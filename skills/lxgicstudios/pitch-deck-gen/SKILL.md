---
name: pitch-gen
description: 生成启动演示文稿（pitch deck）的内容。适用于筹款或产品展示场合。
---

# 项目生成器（Pitch Generator）

撰写商业提案（pitch decks）是一件非常繁琐的工作。使用这个工具，您可以轻松地描述自己的初创公司，并生成结构化好的提案内容，涵盖问题、解决方案、市场情况以及融资需求。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-pitch "AI-powered code review tool for teams"
```

## 功能介绍

- 生成完整的商业提案内容
- 涵盖问题、解决方案、市场规模以及市场竞争情况
- 整理提案的叙述结构
- 输出适合用于幻灯片的Markdown格式内容

## 使用示例

```bash
# Generate pitch content
npx ai-pitch "AI-powered code review tool for teams"

# Save to file
npx ai-pitch "marketplace for freelance designers" -o deck.md
```

## 使用建议

- **首先说明问题**：让投资者感受到问题的紧迫性
- **展示实际进展**：数据比功能本身更重要
- **了解市场规模**：明确总市场容量（TAM）、服务市场容量（SAM）和目标市场容量（SOM）
- **明确融资需求**：具体说明需要多少资金以及用于什么目的

## 适用场景

- 准备投资者会议
- 制作产品演示日（demo day）的演示文稿
- 整理公司的业务故事
- 作为进一步完善的起点

## 该工具属于LXGIC开发工具包（LXGIC Dev Toolkit）的一部分

这是LXGIC Studios开发的110多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要API密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。运行时需要设置`OPENAI_API_KEY`环境变量。

```bash
npx ai-pitch --help
```

## 工作原理

该工具根据您的初创公司描述，使用经过验证的框架生成结构化的提案内容。AI能够理解投资者关注的重点，并据此整理提案的叙述结构。

## 许可协议

采用MIT许可证，永久免费。您可以自由使用该工具。