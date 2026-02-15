---
name: animation-gen
description: 将普通的英文描述转换为 CSS 和 Framer Motion 动画代码。当你需要无需数学计算即可实现平滑动画效果时，可以使用这种方法。
---

# 动画生成器

描述动画很容易，但编写关键帧和缓动函数却并非易事。只需告诉这个工具你想要的效果，它就会为你生成相应的CSS或Framer Motion代码来实现它。

**一个命令，零配置，立即可用。**

## 快速入门

```bash
npx ai-animation "fade in from left with bounce"
```

## 功能介绍

- 将简单的文字描述转换为实际的动画代码
- 支持CSS关键帧和Framer Motion格式
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

## 使用建议

- **描述具体效果**：例如“先弹跳两次，然后渐隐”，比“让它动起来”更清晰
- **标注时间**：如果时间控制很重要，请注明“慢速”、“快速”或“0.5秒”
- **指定方向**：如“从左侧开始”、“向上移动”或“对角线移动”等详细信息会很有帮助
- **在设备上测试**：动画在移动设备上的显示效果可能与桌面不同

## 适用场景

- 制作吸引注意力的网站页面
- 为用户界面添加微交互效果
- 当你能够想象动画效果但无法编写代码时
- 在手动微调之前快速进行原型设计

## 属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发工具之一。免费版本无付费门槛、无需注册，也不需要API密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。运行时需要设置`OPENAI_API_KEY`环境变量。

```bash
npx ai-animation --help
```

## 工作原理

该工具会将你的自然语言描述转换为动画所需的原始数据。它能够理解“弹跳”、“缓动”、“交错”等常见的动画术语，并将其转换为正确的计时函数和关键帧值。

## 许可证

采用MIT许可证，永久免费。你可以随意使用这个工具。