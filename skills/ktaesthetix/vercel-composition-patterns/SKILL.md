---
name: vercel-composition-patterns
description:
  React composition patterns that scale. Use when refactoring components with
  boolean prop proliferation, building flexible component libraries, or
  designing reusable APIs. Triggers on tasks involving compound components,
  render props, context providers, or component architecture. Includes React 19
  API changes.
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---

# React 组合模式

这些组合模式用于构建灵活且易于维护的 React 组件。通过使用复合组件、提升状态（state-lifting）以及组合内部逻辑，可以避免布尔属性（boolean props）的过度使用。这些模式使得代码库在扩展时更易于人类和人工智能工具进行理解和处理。

## 适用场景

在以下情况下，请参考这些指南：
- 重构具有大量布尔属性的组件
- 构建可重用的组件库
- 设计灵活的组件 API
- 审查组件架构
- 使用复合组件或上下文提供者（context providers）

## 规则分类（按优先级）

| 优先级 | 分类                | 影响程度 | 前缀          |
| -------- | ----------------------- | ------ | --------------- |
| 1        | 组件架构              | 高      | `architecture-`     |
| 2        | 状态管理              | 中等      | `state-`        |
| 3        | 实现模式              | 中等      | `patterns-`     |
| 4        | React 19 API            | 中等      | `react19-`      |

## 快速参考

### 1. 组件架构（高优先级）

- `architecture-avoid-boolean-props` - 不要使用布尔属性来自定义组件行为；应使用组合模式
- `architecture-compound-components` - 使用共享上下文（shared context）来构建复杂组件

### 2. 状态管理（中等优先级）

- `state-decouple-implementation` - 只有状态提供者（state provider）知道状态是如何管理的
- `state-context-interface` - 定义包含状态、操作（actions）和元数据（meta data）的通用接口，以便进行依赖注入
- `state-lift-state` - 将状态移至提供者组件中，以便其他组件能够访问

### 3. 实现模式（中等优先级）

- `patterns-explicit-variants` - 创建明确的变体组件（variant components），而不是使用布尔属性来表示不同的行为模式
- `patterns-children-over-render-props` - 使用子组件（children）进行组合，而不是使用 `renderX` 类型的属性

### 4. React 19 API（中等优先级）

> **⚠️ 仅适用于 React 19 及更高版本。** 如果使用的是 React 18 或更低版本，请跳过此部分。
- `react19-no-forwardref` - 不要使用 `forwardRef`；请使用 `use()` 替代 `useContext()`

## 使用方法

有关详细说明和代码示例，请阅读各个规则文件：

```
rules/architecture-avoid-boolean-props.md
rules/state-context-interface.md
```

每个规则文件包含：
- 该规则重要性的简要说明
- 错误的代码示例及其解释
- 正确的代码示例及其解释
- 额外的背景信息和参考资料

## 完整的编译文档

如需查看包含所有规则的完整指南，请参阅 `AGENTS.md`。