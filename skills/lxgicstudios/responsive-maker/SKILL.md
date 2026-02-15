---
name: responsive-maker
description: 通过设置适当的断点（breakpoints），使组件具备响应式设计。当你的组件在移动设备上显示效果不佳时，可以使用这种方法进行优化。
---

# Responsive Maker

您的组件在桌面设备上显示效果很好，但当有人在手机上打开它时，界面可能会变得混乱不堪。这款工具会为您的组件添加适当的响应式断点（responsive breakpoints），处理媒体查询（media queries）、Flexbox布局调整以及字体缩放（font scaling），确保用户界面在所有屏幕尺寸上都能正常显示。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-responsive src/components/Hero.tsx
```

## 功能介绍

- 分析组件的结构并添加响应式断点
- 将固定布局转换为能够适应不同屏幕尺寸的灵活布局
- 添加以移动设备优先的媒体查询（mobile-first media queries）或Tailwind CSS的响应式前缀（responsive prefixes）
- 处理字体缩放、间距调整以及布局重排（layout reflows）
- 在保留现有样式的同时，为组件添加响应式功能

## 使用示例

```bash
npx ai-responsive src/components/Hero.tsx
npx ai-responsive src/components/
npx ai-responsive "src/**/*.tsx"
```

## 最佳实践

- **优先考虑移动设备的设计**：从最小屏幕尺寸开始设计，再逐步增加复杂度
- **在实际设备上进行测试**：模拟器可能无法完全模拟真实设备的显示效果，请在真实手机上进行测试
- **不要在移动设备上隐藏内容**：应重新组织页面结构，确保手机用户也能获取所有信息

## 适用场景

- 当您的组件原本仅适用于桌面设备，但需要在移动设备上也能正常使用
- 当您需要为现有项目添加响应式设计
- 当客户反馈网站在手机上显示异常时

## 该工具属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要API密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。

## 工作原理

该工具会读取组件的代码，分析布局结构，并生成相应的响应式CSS或Tailwind CSS样式。通过人工智能技术，它会为每个屏幕尺寸确定最佳的断点和布局调整方案。

## 许可证

采用MIT许可证，永久免费。您可以随心所欲地使用该工具。