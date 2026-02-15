---
name: responsive-fix
description: 使组件具有响应式设计，并设置适当的断点（breakpoints）。
---

# 响应式修复工具

将仅适用于桌面端的组件转换为支持移动设备的响应式代码。

## 快速入门

```bash
npx ai-responsive ./src/components/Dashboard.tsx
```

## 功能介绍

- 分析页面布局结构  
- 添加适当的断点（breakpoints）  
- 将固定宽度元素转换为响应式元素  
- 处理网格（grid）和弹性布局（flex layout）的调整  
- 应用以移动设备优先的样式（mobile-first design）  

## 使用示例

```bash
# Fix a component
npx ai-responsive ./src/components/Sidebar.tsx

# Specify breakpoints
npx ai-responsive ./components/Nav.tsx --breakpoints sm,md,lg

# CSS-in-JS output
npx ai-responsive ./components/Card.tsx --format styled
```

## 修复的问题

- 固定的像素宽度 → 响应式单位  
- 桌面端的网格布局 → 移动设备上的堆叠布局（stack layout）  
- 隐藏在移动设备上的元素 → 正确地显示/隐藏  
- 触控目标元素 → 最小尺寸为 48px  
- 字体大小 → 可响应式缩放  

## 输出示例

```tsx
// Before: grid-cols-4
// After: grid-cols-1 sm:grid-cols-2 lg:grid-cols-4
```

## 系统要求

- Node.js 18.0 或更高版本  
- 需要 OPENAI_API_KEY  

## 许可证

- MIT 许可证。永久免费使用。  

---

**开发团队：LXGIC Studios**  
- GitHub: [github.com/lxgicstudios/ai-responsive](https://github.com/lxgicstudios/ai-responsive)  
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)