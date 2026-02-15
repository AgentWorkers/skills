---
name: cover-letter-gen
description: 使用人工智能生成定制的求职信。在申请工作时可以使用这些求职信。
---

# 自动生成求职信工具

撰写求职信是一件繁琐的任务，大多数人通常只是重复使用相同的模板。这款工具能够根据你申请的职位生成个性化的求职信。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-cover-letter "frontend role at Stripe"
```

## 功能介绍

- 生成符合职位要求的专业求职信
- 使语气与公司的企业文化相匹配
- 突出与职位相关的重要技能
- 避免使用泛泛而谈的填充内容

## 使用示例

```bash
# Frontend role
npx ai-cover-letter "frontend role at Stripe"

# Senior position
npx ai-cover-letter "senior backend engineer at Vercel"

# Startup vs enterprise
npx ai-cover-letter "ML engineer at early stage AI startup"

# Save to file
npx ai-cover-letter "devops engineer at Netflix" -o cover-letter.md
```

## 使用建议

- **明确说明职位要求**：务必提及公司名称和具体职位
- **介绍自身背景**：说明你的工作经验和核心技能
- **仔细审阅并个性化内容**：说明为什么选择这家公司
- **保持简洁**：没人会阅读长达三页的求职信

## 适用场景

- 在申请工作时对撰写求职信感到头疼
- 需要一个好的起点来定制求职信内容
- 希望使自己的语气与公司的企业文化相符
- 需要批量申请不同职位并生成多样化的求职信

## 本工具属于 LXGIC 开发者工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发者工具之一。免费版本无需支付费用、无需注册，也无需使用 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-cover-letter --help
```

## 工作原理

该工具会根据你对职位和公司的描述，生成突出你相关技能的求职信，并调整其语气以匹配公司的文化风格。AI 能够理解不同公司的文化特点，从而相应地调整信件的正式程度。

## 许可证

采用 MIT 许可协议，永久免费。你可以随意使用该工具。