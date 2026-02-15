---
name: animation-gen
description: **将简单的英文描述转换为CSS和Framer Motion动画**  
当您需要流畅的动画效果而无需进行复杂的数学计算时，可以使用这种方法。
---

# 动画生成器

描述动画其实很简单，但编写关键帧和缓动函数却并非易事。只需告诉这个工具你想要的效果，它就能为你生成相应的 CSS 或 Framer Motion 代码来实现它。

**一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-animation "fade in from left with bounce"
```

## 功能介绍

- 将简单的文字描述转换为实际的动画代码
- 支持 CSS 关键帧和 Framer Motion 动画格式
- 能处理复杂的多步骤动画
- 生成可直接使用的成品代码

## 使用示例

```bash
# Get CSS keyframes
npx ai-animation "pulse glow effect" -f css

# Get Framer Motion variant
npx ai-animation "staggered list entrance" -f framer

# Save to file
npx ai-animation "smooth slide up reveal" -f both -o animations.ts

# Complex animation
npx ai-animation "shake horizontally three times then settle"
```

## 最佳实践

- **描述具体效果**：例如“先弹跳两次，然后渐隐”，比简单地说“让它动起来”更清晰
- **标注时间**：如果时间控制很重要，请加上“慢速”、“快速”、“0.5秒”等说明
- **指定方向**：如“从左侧开始”、“向上移动”、“对角线移动”等细节会帮助生成更准确的动画效果
- **在设备上测试**：动画在移动设备上的显示效果可能与在桌面不同

## 适用场景

- 制作需要吸引注意力的网站页面时
- 为用户界面添加微交互效果
- 当你能够想象动画效果，但无法用代码实现时
- 在手动微调之前快速进行原型设计

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册，也无需 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-animation --help
```

## 工作原理

该工具会将你的自然语言描述转换为动画所需的原始数据。它能够理解“弹跳”、“缓动”、“交错移动”等常见动画术语，并将其转换为正确的缓动函数和关键帧值。

## 许可证

采用 MIT 许可协议，永久免费使用，你可以随意使用该工具。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/ai-animation](https://github.com/lxgicstudios/ai-animation)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)