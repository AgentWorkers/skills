---
name: roast-gen
description: 让你的代码在幽默和富有建设性的反馈中得到“审视”。当你需要诚实的代码审查时，就可以使用这个工具。
---

# Roast Gen

想要获得关于你代码的坦诚反馈吗？这个工具可以帮你“审视”你的代码，指出其中的缺陷、偷懒的写法，以及那些让人费解的设计决策。不过，与那些刻薄的代码审查者不同，它总是以幽默的方式表达反馈，并且还会提供实际的修改建议。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-roast ./src/app.ts
```

## 功能介绍

- 分析你的代码，找出所有存在的问题；
- 用幽默的方式而非官方术语来提供反馈；
- 指出代码中的不良实践、潜在问题以及有争议的设计决策；
- 为每个问题提供具体的修改建议；
- 评估你的代码是否适合“生产环境使用”。

## 使用示例

```bash
# Roast a single file
npx ai-roast ./src/checkout.ts

# Roast your entire codebase (brave)
npx ai-roast ./src/

# Get a gentle roast
npx ai-roast ./src/utils.ts --level mild

# Full savage mode
npx ai-roast ./src/legacy.js --level brutal
```

## 使用建议

- **别太当真**——批评的对象是代码，不是你个人；
- **从温和的反馈开始**——逐渐增加对批评的接受度；
- **与团队分享**——集体讨论可以增强团队凝聚力；
- **务必解决问题**——虽然批评很有趣，但关键还是改进代码。

## 适用场景

- 当你需要代码审查的反馈，但又不想麻烦同事时；
- 团队回顾项目时，想一起吐槽那些遗留的代码问题；
- 在新员工入职时，想让他们了解哪些做法是不可取的；
- 当你对自己的代码很有信心，但希望得到客观的评价时。

## 属于 LXGIC 开发工具包

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本没有任何付费门槛、注册要求或 API 密钥，只提供实用的功能。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-roast --help
```

## 工作原理

该工具会检查你的代码中常见的缺陷，如命名不规范、代码结构复杂、存在不良实践或有争议的设计决策。它以幽默的方式呈现反馈，并提供切实可行的改进方案。

## 许可证

MIT 许可证。永久免费，你可以随意使用。