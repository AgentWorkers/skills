---
name: landing-gen
description: 根据产品描述生成 landing page 的代码
---

# 着陆页生成器

描述您的产品，快速获得一个优化过转化率的着陆页。该工具基于 React 和 Tailwind CSS 构建，可直接部署使用。

## 快速入门

```bash
npx ai-landing "AI tool that writes documentation"
```

## 功能介绍

- 生成完整的着陆页代码
- 包含首页展示区（hero）、产品特性、价格信息以及购买按钮（CTA）
- 支持移动设备响应式设计
- 自动添加 SEO 相关元标签
- 提供优化过的文案内容

## 使用示例

```bash
# Generate from description
npx ai-landing "SaaS for project management"

# Specify sections
npx ai-landing "API monitoring tool" --sections hero,features,pricing,faq

# Choose style
npx ai-landing "Developer tool" --style minimal
```

## 生成内容包含：

- React/Next.js 组件
- Tailwind CSS 样式
- 响应式布局
- 暗黑模式支持
- 占位图片

## 生成的页面结构：

- 带有 `value` 属性的首页展示区（hero）
- 社交证明（social proof）展示区
- 产品特性列表
- 价格表
- 常见问题解答（FAQ）折叠面板
- 带有购买按钮的页脚区域（CTA）

## 系统要求

- 必需安装 Node.js 18.0 及以上版本
- 需要 OPENAI_API_KEY

## 许可证

- MIT 许可协议，永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub 仓库：[github.com/lxgicstudios/ai-landing](https://github.com/lxgicstudios/ai-landing)
- Twitter 账号：[@lxgicstudios](https://x.com/lxgicstudios)