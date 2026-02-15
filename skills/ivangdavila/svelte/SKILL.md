---
name: Svelte
description: 避免常见的 Svelte 错误：反应式触发器（reactivity triggers）、状态存储订阅（state store subscriptions）以及 SvelteKit 的服务器端渲染（SSR）相关问题。
metadata: {"clawdbot":{"emoji":"🔥","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## 反应性触发条件  
- 赋值操作会触发组件的重新渲染：例如 `arr = arr`（在数组元素被添加或修改后）；或者使用 `arr = [...arr, item]` 的方式。  
- 数组方法本身不会触发组件的重新渲染，因此需要通过赋值来触发反应性：`arr.push()` 需要写成 `arr = arr`。  
- 对象属性的修改同样会触发反应性：`obj.key = val; obj = obj` 或者使用展开运算符 `obj = {...obj, key: val}`。  
- 反应式声明（`$:`）会在依赖项发生变化时执行，但只有顶层赋值操作才会被追踪到。  

## 反应式声明（`$:`）  
- 当依赖项发生变化时，`$:` 会自动执行；它会列出所有被引用的依赖项。  
- 使用 `{}` 块可以同时执行多个反应式声明。  
- `$:` 的执行顺序很重要：后面的声明可能会依赖于前面的声明结果。  
- 应避免在反应式声明中产生副作用；建议使用 `onMount` 来处理副作用。  

## 数据存储（`$store`）  
- `$store` 会在组件创建时自动订阅数据变化，并在组件销毁时自动取消订阅：`const unsub = store.subscribe(v => ...); onDestroy(unsub)`。  
- `writable` 属性表示数据可读写；`readable` 属性表示数据来自外部源；  
- `derived` 属性用于计算属性：`derived(store, $s => $s * 2)`。  

## 组件生命周期  
- `onMount` 在组件首次渲染后执行；在此之前无法访问 DOM（例如 `document`）。  
- `beforeUpdate` 和 `afterUpdate` 主要用于处理 DOM 的同步问题，但在单页渲染（SSR）中很少需要使用。  
- `tick()` 方法用于等待 DOM 更新；可以在状态变化后调用 `await tick()`。  

## 属性（`props`）  
- 使用 `export let propName` 声明属性；如果属性是可选的，可以使用 `export let propName = default` 来指定默认值。  
- 属性具有反应性，因此当属性值发生变化时，组件会重新渲染。  
- `$$props` 和 `$$restProps` 用于传递原始属性值，但建议明确指定需要使用的属性。  

## 事件（`events`）  
- 使用 `createEventDispatcher` 创建自定义事件：`dispatch('eventName', data)`。  
- 使用 `on:eventName` 来监听事件：例如 `on:click`、`on:customEvent`。  
- 可以使用修饰符 `|preventDefault` 来阻止事件传播，或者 `|once` 来确保事件只执行一次。  
- 如果没有处理函数，`on:click` 会直接将事件转发给父组件。  

## SvelteKit  
- 使用 `+page.svelte` 定义页面结构；`+page.server.ts` 用于处理服务器端的逻辑。  
- `load` 函数用于在服务器和客户端导航时获取数据。  
- `$app/stores` 可用于访问页面相关的数据和导航信息（如 `$page.params`、`$page.url`）。  
- `form` 动作用于触发数据更新；这种做法支持渐进式增强（progressive enhancement），即使没有 JavaScript 也能正常工作。  

## 单页渲染（SSR）中的注意事项  
- 在使用 `window` 或 `document` 之前，请先检查 `$app/environment` 中是否提供了相应的对象。  
- `onMount` 仅在客户端执行，因此使用它时需要确保不会影响浏览器 API 的正常工作。  
- 存储（`$store`）在服务器端初始化后会在多个请求中共享；对于特定请求的数据，需要使用上下文（context）来获取。  
- `load` 函数中的 `fetch` 方法处理相对 URL 和身份验证逻辑。  

## Svelte 5 的新特性  
- `$state()` 替代了传统的 `let` 用于声明反应性变量：`let count = $state(0)`。  
- `$derived` 替代了 `$:` 用于计算属性：`let doubled = $derived(count * 2)`。  
- `$effect` 用于处理副作用；它提供了更简洁的方式来管理副作用。  
- 这些新特性是可选的，可以在文件中根据需要启用或禁用。  

## 常见错误  
- 在 Svelte 5 中，解构属性值会失去反应性；请避免使用 `let { prop } = $props()` 的写法。  
- 注意区分存储（`$store`）和用于存储操作的属性（例如用于订阅或设置的属性）。  
- 在条件渲染中使用 `{#if show}<div transition:fade>` 时，需要注意其作用范围（仅影响被 `#key` 包含的元素）。  

希望这些翻译能帮助你更好地理解 Svelte 的相关概念和用法！如果有任何疑问，请随时提问。