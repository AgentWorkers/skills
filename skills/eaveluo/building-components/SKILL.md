---
name: building-components
description: React组件构建与组合的最佳实践。适用于创建、审查或重构React组件时参考。内容包括组件结构、属性使用模式、组合技术以及可重用性指南。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---
# 构建 React 组件

构建可重用、易于维护的 React 组件的最佳实践。

## 适用场景

在以下情况下，请参考这些指南：
- 创建新的 React 组件
- 审查组件结构和 API 设计
- 重构组件以提高可重用性
- 实现组件组合模式
- 设计属性接口

## 核心原则

### 1. 单一职责原则
每个组件应该专注于完成一项任务。将大型组件拆分为更小、更具体的功能模块。

### 2. 组合优于继承
优先使用组件组合的方式，而不是复杂的继承层次结构。

```jsx
// ✅ Good: Composition
function Page() {
  return (
    <Layout>
      <Header />
      <Main>
        <Article />
      </Main>
      <Footer />
    </Layout>
  );
}

// ❌ Avoid: Deep nesting
function Page() {
  return <LayoutWithHeaderAndFooter><MainContent /></LayoutWithHeaderAndFooter>;
}
```

### 3. 属性设计
- 使用 TypeScript 进行属性类型定义
- 保持属性接口简洁明了
- 更倾向于使用多个小属性，而不是少数大对象
- 使用 `children` 属性来组合内容

### 4. 组件结构
```tsx
// ✅ Recommended structure
import { FC } from 'react';

interface Props {
  title: string;
  children?: React.ReactNode;
}

export const Card: FC<Props> = ({ title, children }) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  );
};
```

### 5. 状态管理
- 尽可能将状态放在需要使用它的地方
- 只有在必要时才将状态提升到更高层级的组件
- 考虑使用自定义钩子来实现可重用的状态逻辑

## 常见模式

### 复合组件
适用于像 `Select/Option`、`Tabs/TabList/Tab/TabPanel` 这样的灵活 API。

### 渲染属性
用于在保持渲染控制权的同时共享组件行为。

### 钩子
用于在组件之间共享有状态逻辑。

## 相关资源
- vercel-react-best-practices
- next-best-practices
- vercel-composition-patterns