---
name: vercel-react-best-practices
description: 来自 Vercel Engineering 的 React 和 Next.js 性能优化指南。在编写、审查或重构 React/Next.js 代码时，应遵循这些最佳实践，以确保代码具备最佳的性能表现。这些指南适用于涉及 React 组件、Next.js 页面、数据获取、代码包优化以及性能提升的相关任务。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React最佳实践

这份由Vercel维护的指南为React和Next.js应用程序提供了全面的性能优化建议。指南包含45条规则，分为8个类别，并根据规则对代码重构和代码生成的影响程度进行了优先级排序。

## 适用场景

在以下情况下请参考这些指南：
- 编写新的React组件或Next.js页面
- 实现数据获取（客户端或服务器端）
- 检查代码中的性能问题
- 重构现有的React/Next.js代码
- 优化打包大小或加载时间

## 规则类别及优先级

| 优先级 | 类别 | 影响程度 | 前缀 |
|----------|----------|--------|--------|
| 1 | 消除不必要的代码执行顺序（Critical） | `async-` |
| 2 | 打包大小优化（Critical） | `bundle-` |
| 3 | 服务器端性能优化（High） | `server-` |
| 4 | 客户端数据获取（Medium-High） | `client-` |
| 5 | 重渲染优化（Medium） | `rerender-` |
| 6 | 渲染性能优化（Medium） | `rendering-` |
| 7 | JavaScript性能优化（Low-Medium） | `js-` |
| 8 | 高级优化技巧（Low） | `advanced-` |

## 快速参考

### 1. 消除不必要的代码执行顺序（Critical）

- `async-defer-await`：将`await`语句移至实际需要的地方
- `async-parallel`：使用`Promise.all()`处理独立的操作
- `async-dependencies`：使用`better-all`处理部分依赖关系
- `async-api-routes`：在API路由中尽早启动Promise请求，延迟执行`await`
- `async-suspense-boundaries`：使用`Suspense`来按需加载内容

### 2. 打包大小优化（Critical）

- `bundle-barrel-imports`：直接导入模块，避免使用打包文件
- `bundle-dynamic-imports`：对于重量级组件，使用`next/dynamic`动态导入
- `bundle-defer-third-party`：在组件加载完成后再加载第三方库/日志
- `bundle-conditional`：仅在功能启用时才加载相关模块
- `bundle-preload`：通过悬停/聚焦等操作预加载内容

### 3. 服务器端性能优化（High）

- `server-cache-react`：使用`React.cache()`实现请求级别的数据去重
- `server-cache-lru`：使用LRU缓存机制进行跨请求缓存
- `server-serialization`：减少传递给客户端组件的数据量
- `server-parallel-fetching`：重构组件结构以并行处理数据请求
- `server-after-nonblocking`：使用`after()`处理非阻塞操作

### 4. 客户端数据获取（Medium-High）

- `client-swr-dedup`：使用SWR（Swerve React Router）实现请求去重
- `client-event-listeners`：避免重复注册全局事件监听器

### 5. 重渲染优化（Medium）

- `rerender-defer-reads`：仅对回调中使用的状态进行重新渲染
- `rerender-memo`：将计算成本较高的操作提取到 memoized 组件中
- `rerender-dependencies`：在效果函数中使用基本类型的依赖项
- `rerender-derived-state`：仅对派生的布尔值进行重新渲染
- `rerender-functional-setstate`：使用函数式`setState`处理稳定的状态变化
- `rerender-lazy-state-init`：对于计算成本较高的状态值，使用函数传递给`useState`
- `rerender-transitions`：使用`startTransition`处理非紧急的界面更新

### 6. 渲染性能优化（Medium）

- `rendering-animate-svg-wrapper`：对`div`包装器进行动画处理，而不是直接操作SVG元素
- `rendering-content-visibility`：对于长列表，使用`content-visibility`来控制元素的可见性
- `rendering-hoist-jsx`：将静态JSX代码提取到组件外部
- `rendering-svg-precision`：降低SVG坐标的精度
- `rendering-hydration-no-flicker`：使用内联脚本处理仅客户端需要的数据
- `rendering-activity`：使用`Activity`组件来控制元素的显示/隐藏
- `rendering-conditional-render`：使用三元运算符而非`&&`进行条件判断

### 7. JavaScript性能优化（Low-Medium）

- `js-batch-dom-css`：通过`classes`或`cssText`批量应用CSS更改
- `js-index-maps`：为重复查询创建索引映射
- `js-cache-property-access`：在循环中缓存对象属性
- `js-cache-function-results`：在模块级别缓存函数执行结果
- `js-cache-storage`：缓存`localStorage`/`sessionStorage`的读取操作
- `js-combine-iterations`：将多个`filter`/`map`操作合并为一个循环
- `js-length-check-first`：在进行复杂比较前先检查数组长度
- `js-early-exit`：尽早退出函数
- `js-hoist-regexp`：将正则表达式的创建移出循环外
- `js-min-max-loop`：使用循环实现最小值/最大值计算
- `js-set-map-lookups`：使用`Set`/`Map`实现O(1)级别的查找
- `js-tosorted-immutable`：使用`toSorted()`函数保持数据不可变性

### 8. 高级优化技巧（Low）

- `advanced-event-handler-refs`：将事件处理器存储在`refs`中
- `advanced-use-latest`：使用`latest`函数获取最新的事件处理器引用

## 使用方法

详细说明和代码示例请参阅相应的规则文件：

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/_sections.md
```

每个规则文件包含：
- 规则的重要性的简要说明
- 错误的代码示例及解释
- 正确的代码示例及解释
- 额外的背景信息和参考资料

## 完整指南

如需查看包含所有规则的完整指南，请参阅`AGENTS.md`文件。