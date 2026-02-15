---
name: react-best-practices
model: standard
version: 1.0.0
description: >
  React and Next.js performance optimization guidelines from Vercel Engineering.
  57 rules across 8 categories for writing, reviewing, and refactoring React code.
tags: [react, nextjs, performance, optimization, ssr, bundle, rendering]
license: MIT
author: vercel
---

# React最佳实践

本指南由Vercel Engineering团队编写，为React和Next.js应用程序提供了全面的性能优化建议。指南包含57条规则，分为8个类别，并根据规则的影响程度进行了优先级排序。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install react-best-practices
```

## 本指南的作用

本指南提供了以下方面的实用建议：
- 消除请求堆积（request waterfalls）
- 优化打包文件大小（bundle size）
- 提升服务器端性能
- 优化客户端数据获取（client-side data fetching）
- 减少不必要的重新渲染（minimize re-renders）
- 优化渲染性能
- 对JavaScript代码进行微优化
- 针对特殊情况的高级优化方案

## 适用场景

- 在编写新的React组件或Next.js页面时
- 实现数据获取（无论是客户端还是服务器端）
- 检查代码中的性能问题
- 重构React/Next.js应用程序
- 优化打包文件大小或加载时间
- 调试渲染缓慢或请求堆积的问题

## 关键词

- React性能（React performance）
- Next.js优化（Next.js optimization）
- 打包文件大小（bundle size）
- 请求堆积（request waterfalls）
- Suspense（用于处理异步操作）
- 服务器端组件（server components）
- RSC（React Static Compilation）
- 重新渲染（rerender）

## 规则分类（按优先级）

| 优先级 | 类别 | 影响程度 | 规则前缀 |
|------|----------|--------|-------------|
| 1 | 消除请求堆积 | 关键（CRITICAL） | `async-` |
| 2 | 打包文件大小优化 | 关键（CRITICAL） | `bundle-` |
| 3 | 服务器端性能 | 高（HIGH） | `server-` |
| 4 | 客户端数据获取 | 中等偏高（MEDIUM-HIGH） | `client-` |
| 5 | 重新渲染优化 | 中等（MEDIUM） | `rerender-` |
| 6 | 渲染性能 | 中等（MEDIUM） | `rendering-` |
| 7 | JavaScript性能 | 低至中等（LOW-MEDIUM） | `js-` |
| 8 | 高级优化方案 | 低（LOW） | `advanced-` |

## 快速参考

### 1. 消除请求堆积（关键）

| 规则 | 说明 |
|------|-------------|
| `async-defer-await` | 将`await`语句移至实际需要使用的位置 |
| `async-parallel` | 对独立的操作使用`Promise.all()` |
| `async-dependencies` | 对部分依赖项使用更合适的处理方式 |
| `async-api-routes` | 在API路由中尽早启动Promise请求，延迟`await`操作 |
| `async-suspense-boundaries` | 使用`Suspense`来按需加载内容 |

### 2. 打包文件大小优化（关键）

| 规则 | 说明 |
|------|-------------|
| `bundle-barrel-imports` | 直接导入代码，避免使用打包文件（barrel files） |
| `bundle-dynamic-imports` | 对大型组件使用`next/dynamic`功能 |
| `bundle-defer-third-party` | 在组件加载完成后再加载第三方库/日志 |
| `bundle-conditional` | 仅在功能启用时才加载相关模块 |
| `bundle-preload` | 在用户悬停或聚焦时预加载相关内容 |

### 3. 服务器端性能（高）

| 规则 | 说明 |
|------|-------------|
| `server-auth-actions` | 对服务器端的操作（如API请求）进行身份验证 |
| `server-cache-react` | 使用`React.cache()`来避免重复请求 |
| `server-cache-lru` | 使用LRU缓存机制来存储跨请求的数据 |
| `server-dedup-props` | 避免在RSC（React Static Compilation）中重复序列化属性 |
| `server-serialization` | 减少传递给客户端组件的数据量 |
| `server-parallel-fetching` | 重构组件结构以并行处理数据请求 |
| `server-after-nonblocking` | 对非阻塞操作使用`after()`函数 |

### 4. 客户端数据获取（中等偏高）

| 规则 | 说明 |
|------|-------------|
| `client-swr-dedup` | 使用SWR（Static Web Rendering）来自动去除重复的请求 |
| `client-event-listeners` | 去除全局事件监听器的重复实例 |
| `client-passive-event-listeners` | 对滚动事件使用被动监听器 |
| `client-localstorage-schema` | 优化localStorage的数据存储方式 |

### 5. 重新渲染优化（中等）

| 规则 | 说明 |
|------|-------------|
| `rerender-defer-reads` | 只对在回调函数中使用的状态进行重新渲染 |
| `rerender-memo` | 将计算量大的操作提取到 memoized 组件中 |
| `rerender-memo-with-default-value` | 将默认的非原始值提取出来并缓存 |
| `rerender-dependencies` | 在效果函数（effects）中使用原始类型的依赖项 |
| `rerender-derived-state` | 在渲染时计算派生状态，而不是在效果函数中 |
| `rerender-derived-state-no-effect` | 在渲染时计算派生状态，而不是在效果函数中 |
| `rerender-functional-setstate` | 对稳定的回调函数使用函数式的`setState` |
| `rerender-lazy-state-init` | 对计算量大的值使用`useState`的函数形式 |
| `rerender-simple-expression-in-memo` | 对简单的原始类型避免使用memoization |
| `rerender-move-effect-to-event` | 将交互逻辑放入事件处理函数中 |
| `rerender-transitions` | 对非紧急的更新使用`startTransition` |
| `rerender-use-ref-transient-values` | 对频繁变化的值使用`refs`来保存状态 |

### 6. 渲染性能（中等）

| 规则 | 说明 |
|------|-------------|
| `rendering-animate-svg-wrapper` | 对`div`包装器进行动画处理，而不是对SVG元素本身 |
| `rendering-content-visibility` | 对长列表使用`content-visibility`属性 |
| `rendering-hoist-jsx` | 将静态的JSX代码提取到组件外部 |
| `rendering-svg-precision` | 降低SVG坐标的精度 |
| `rendering-hydration-no-flicker` | 对仅客户端需要的数据使用内联脚本 |
| `rendering-hydration-suppress-warning` | 抑制预期的不匹配警告 |
| `rendering-activity` | 使用`Activity`组件来控制元素的显示/隐藏 |
| `rendering-conditional-render` | 使用三元表达式而不是`&&`来进行条件判断 |
| `rendering-usetransition-loading` | 对加载状态使用`useTransition`效果 |

### 7. JavaScript性能（低至中等）

| 规则 | 说明 |
|------|-------------|
| `js-batch-dom-css` | 通过类或`cssText`批量处理CSS更改 |
| `js-index-maps` | 为重复的查找操作构建映射（Map） |
| `js-cache-property-access` | 在循环中缓存对象属性 |
| `js-cache-function-results` | 在模块级别缓存函数的结果 |
| `js-cache-storage` | 缓存`localStorage`和`sessionStorage`的读取操作 |
| `js-combine-iterations` | 将多个过滤/映射操作合并为一个循环 |
| `js-length-check-first` | 在执行复杂操作前先检查数组长度 |
| `js-early-exit` | 尽早从函数中返回 |
| `js-hoist-regexp` | 将正则表达式的创建移到循环外部 |
| `js-min-max-loop` | 使用循环来计算最小值/最大值，而不是排序 |
| `js-set-map-lookups` | 使用`Set`或`Map`来进行O(1)时间的查找 |
| `js-tosorted-immutable` | 使用`toSorted()`来保证数据的不可变性 |

### 8. 高级优化方案（低）

| 规则 | 说明 |
|------|-------------|
| `advanced-event-handler-refs` | 将事件处理函数存储在`refs`中 |
| `advanced-init-once` | 应用程序加载时只初始化一次 |
| `advanced-use-latest` | 对稳定的回调引用使用`useLatest`函数 |

## 使用方法

`rules/`目录下的每个规则文件都包含：
- 规则的重要性的简要说明
- 错误的代码示例及解释
- 正确的代码示例及解释
- 相关的背景信息和参考资料

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/rerender-memo.md
```

### 完整编译后的文档

如需查看包含所有详细代码示例和解释的完整指南，请参阅`AGENTS.md`文件。该文件包含2900多条规则，适合作为全面的参考资料。

## 关键优化模式

### 并行数据获取（Parallel Data Fetching）

```typescript
// Bad: sequential
const user = await fetchUser()
const posts = await fetchPosts()

// Good: parallel
const [user, posts] = await Promise.all([
  fetchUser(),
  fetchPosts()
])
```

### 动态导入（Dynamic Imports）

```tsx
// Bad: bundles Monaco with main chunk
import { MonacoEditor } from './monaco-editor'

// Good: loads on demand
const MonacoEditor = dynamic(
  () => import('./monaco-editor').then(m => m.MonacoEditor),
  { ssr: false }
)
```

### 函数式`setState`（Functional setState）

```tsx
// Bad: stale closure risk
const addItem = useCallback((item) => {
  setItems([...items, item])
}, [items]) // recreates on every items change

// Good: always uses latest state
const addItem = useCallback((item) => {
  setItems(curr => [...curr, item])
}, []) // stable reference
```

## 绝对不要做的事情

1. **绝不要**顺序执行可以并行执行的操作。
2. **绝不要**从打包文件（barrel files）中导入代码（例如：`import { X } from 'lib'`）——应直接导入所需的模块。
3. **绝不要**在服务器端操作中省略身份验证步骤——应将其视为API请求来处理。
4. **绝不要**将整个对象传递给客户端组件，如果只需要其中一个字段的话。
5. **绝不要**在条件渲染中使用`&&`操作符处理数字——应使用三元表达式。
6. **绝不要**对仅在事件处理函数中使用的状态进行订阅——应根据需要动态获取状态。
7. **绝不要**使用`.sort()`来修改数组——应使用`.toSorted()`方法来排序数组。
8. **绝不要**在`useEffect([])`中初始化状态——应使用模块级别的逻辑来控制状态的初始化。