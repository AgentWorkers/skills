---
name: react-perf
description: React 和 Next.js 的性能优化技巧。适用于编写、审查或优化用于 Web 应用程序、Remotion 视频或任何基于 React 的用户界面的 React 代码。内容涵盖消除不必要的代码层级（waterfall elimination）、优化代码打包（bundle optimization）、防止不必要的重新渲染（re-render prevention）以及服务器端优化策略（server-side optimization）。
metadata:
  author: misskim
  version: "1.0"
  origin: Concept from Vercel react-best-practices (57 rules), distilled to essentials
---

# React 性能优化模式

在编写 React 代码时，以下是一些关键的性能优化模式。

## 按优先级划分的核心规则

### 🔴 关键性（CRITICAL）：消除水坝效应（Waterfall Effect）

```javascript
// ❌ 순차 await — 각 요청이 이전을 기다림
const user = await getUser();
const posts = await getPosts();

// ✅ 병렬 — 독립 요청은 Promise.all
const [user, posts] = await Promise.all([getUser(), getPosts()]);
```

- 将 `await` 语句移至实际需要使用的代码分支中（以消除不必要的等待）
- 使用 `Suspense` 来控制内容的加载顺序

### 🔴 关键性（CRITICAL）：减小打包文件的大小（Bundle Size）

```javascript
// ❌ barrel import — 전체 모듈 로드
import { Button } from '@/components';

// ✅ 직접 import
import { Button } from '@/components/ui/Button';
```

- 使用 `next/dynamic` 功能延迟加载重量较大的组件
- 将分析或日志记录操作推迟到组件渲染完成后再执行
- 通过预加载（preload）来提升用户操作时的响应速度（例如：鼠标悬停或焦点聚焦时）

### 🟡 高度建议（HIGH）：服务器端优化

- 使用 `React.cache()` 来避免重复请求
- 减少传递给客户端的数据量
- 通过调整组件结构来并行化数据请求

### 🟢 中等建议（MEDIUM）：避免不必要的重新渲染（Prevent Re renders）

```javascript
// ❌ 콜백에서만 쓰는 state를 구독
const [items, setItems] = useState([]);
const handleClick = () => process(items);

// ✅ ref로 전환 (리렌더 방지)
const itemsRef = useRef([]);
const handleClick = () => process(itemsRef.current);
```

- 将计算成本较高的操作封装到 `memo` 组件中
- 将函数作为初始状态值传递给 `useState`（实现惰性初始化）
- 使用 `startTransition` 来延迟非紧急的更新
- 将衍生状态（derived state）的计算放在组件渲染过程中进行，而不是在效应（effect）中

### 🔵 低优先级（LOW）：提升 JavaScript 性能

- 对于重复查询，使用 `Map` 或 `Set` 数据结构（时间复杂度为 O(1)）
- 将 `filter().map()` 操作合并为一个循环来减少执行次数
- 避免在循环内部创建正则表达式（RegExp）
- 先检查 `array.length`，然后再进行代价较高的比较操作

## Remotion 中的 React

由于 Remotion 视频组件也是基于 React 实现的，因此同样适用以下原则：
- `interpolate()` 方法会在每一帧中都被调用，如果计算成本较高，应使用缓存机制
- 对于计算量较大的操作，使用 `useMemo` 或 `useCallback` 来避免重复计算
- 尽量减少非屏幕可见元素的渲染