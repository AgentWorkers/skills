---
name: social-gen
description: 为不同的社交媒体平台生成帖子内容。在分享内容时可以使用这些帖子。
---

# 社交媒体发布工具

你创作了一些很棒的内容，现在需要将其分享到 Twitter、LinkedIn 和 Reddit 上。每个平台都有不同的展示格式要求，而这个工具可以帮你解决这个问题。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-social README.md --platform twitter
```

## 功能介绍

- 读取你的内容，并根据不同的平台进行相应的格式调整：
  - Twitter 的内容需要简短精炼；
  - LinkedIn 的内容需要显得专业且正式；
  - Reddit 的内容则需要自然、不带推广性质。

## 使用示例

```bash
# Twitter post
npx ai-social README.md --platform twitter

# LinkedIn post
npx ai-social blog-post.md --platform linkedin

# All platforms
npx ai-social announcement.md --platform all
```

## 使用建议

- **了解目标受众**：每个平台都有不同的用户期望；
- **不要重复发布相同的内容**：否则用户会注意到；
- **积极参与互动，而非单纯发布信息**：社交媒体本质上是互动的；
- **选择合适的时间发布**：不同平台的活跃时间各不相同。

## 适用场景

- 项目发布；
- 博文分享；
- 新功能公告；
- 建立受众群体。

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥，只需使用即可。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-social --help
```

## 工作原理

该工具会读取你的内容，提取核心信息，然后根据平台特点重新编写内容：
- Twitter 的内容会添加标签（hashtags）并保持简洁；
- LinkedIn 的内容会添加换行符和明确的行动号召（CTAs）；
- Reddit 的内容则会采用自然、不带销售性质的表达方式。

## 许可协议

采用 MIT 许可协议，永久免费。你可以随意使用该工具。