---
name: react-composition-patterns
model: standard
---

# React 组合模式

使用复合组件（compound components）、上下文提供者（context providers）和明确的变体（explicit variants）来构建灵活且易于维护的 React 组件。避免使用过多的布尔型属性（boolean props）。

## 什么是组合模式（What are Composition Patterns）？

组合模式能够实现组件的可扩展性：
- 具有共享上下文的复合组件（compound components）
- 用于依赖注入的状态/动作/元数据上下文接口（state/actions/meta context interface）
- 通过明确的变体组件替代布尔型属性
- 将状态管理提升到提供者组件中（Lift state in provider components）
- 使用子组件进行组合，而非直接使用渲染属性（Children composition over render props）

## 何时使用这些模式（When to Use These Patterns）？

- 当需要重构具有大量布尔型属性的组件时
- 在构建可重用的组件库时
- 在设计灵活的组件 API 时
- 在创建复合组件（如 Card、Dialog、Form 等）时
- 当组件需要在同级元素之间共享状态时

## 关键词（Keywords）：

组合（composition）、复合组件（compound components）、上下文（context）、提供者（provider）、布尔型属性（boolean props）、变体（variants）、React 模式（React patterns）、组件架构（component architecture）、渲染属性（render props）、子组件（children）

**来源：** Vercel Engineering

## 安装（Installation）

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install composition-patterns
```


---

## 核心原则（Core Principles）

**避免使用过多的布尔型属性。** 每一个布尔型属性都会导致状态数量的倍增。**

```tsx
// BAD: 4 booleans = 16 possible states
<Composer isThread isDMThread isEditing isForwarding />

// GOOD: Explicit variants, clear intent
<ThreadComposer channelId="abc" />
<EditComposer messageId="xyz" />
```

---

## 模式 1：复合组件（Pattern 1: Compound Components）

使用共享上下文来构建复杂的组件。组件使用者可以根据需要组合所需的组件部分。

**用法：**

```tsx
<Composer.Provider state={state} actions={actions} meta={meta}>
  <Composer.Frame>
    <Composer.Header />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Submit />
    </Composer.Footer>
  </Composer.Frame>
</Composer.Provider>
```

---

## 模式 2：通用上下文接口（Pattern 2: Generic Context Interface）

定义一个所有提供者都可以实现的契约：`state`（状态）、`actions`（动作）、`meta`（元数据）。

**相同的 UI，不同的提供者：**

```tsx
// Local state provider
function ForwardMessageProvider({ children }) {
  const [state, setState] = useState(initialState)
  return (
    <ComposerContext value={{
      state,
      actions: { update: setState, submit: useForwardMessage() },
      meta: { inputRef: useRef(null) },
    }}>
      {children}
    </ComposerContext>
  )
}

// Global synced state provider  
function ChannelProvider({ channelId, children }) {
  const { state, update, submit } = useGlobalChannel(channelId)
  return (
    <ComposerContext value={{
      state,
      actions: { update, submit },
      meta: { inputRef: useRef(null) },
    }}>
      {children}
    </ComposerContext>
  )
}
```

这两种方式都可以与相同的 `<Composer.Input />` 组件配合使用。

---

## 模式 3：明确的变体（Pattern 3: Explicit Variants）

为每种使用场景创建专门的组件，而不是使用布尔型属性来表示不同的状态。

**实现方式：**

```tsx
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <ThreadProvider channelId={channelId}>
      <Composer.Frame>
        <Composer.Input />
        <AlsoSendToChannelField channelId={channelId} />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Submit />
        </Composer.Footer>
      </Composer.Frame>
    </ThreadProvider>
  )
}

function EditComposer({ messageId }: { messageId: string }) {
  return (
    <EditProvider messageId={messageId}>
      <Composer.Frame>
        <Composer.Input />
        <Composer.Footer>
          <Composer.CancelEdit />
          <Composer.SaveEdit />
        </Composer.Footer>
      </Composer.Frame>
    </EditProvider>
  )
}
```

---

## 模式 4：状态管理提升（Pattern 4: Lifted State）

位于视觉层次结构之外的组件可以通过提供者来访问状态。

**关键点：** 提供者的边界很重要，而不是组件的视觉嵌套方式。

---

## 模式 5：使用子组件进行组合（Pattern 5: Children Over Render Props）

使用子组件来进行组合；仅在需要传递数据时才使用渲染属性。

**何时使用渲染属性：**

```tsx
// Passing data to children
<List
  data={items}
  renderItem={({ item, index }) => <Item item={item} index={index} />}
/>
```

---

## 模式 6：将状态与 UI 解耦（Pattern 6: Decouple State from UI）

只有提供者知道状态是如何被管理的。UI 只需要使用提供的接口来获取状态。

```tsx
// BAD: UI coupled to state implementation
function ChannelComposer({ channelId }) {
  const state = useGlobalChannelState(channelId)  // Knows about global state
  const { submit } = useChannelSync(channelId)    // Knows about sync
  
  return <Composer.Input value={state.input} onChange={...} />
}

// GOOD: State isolated in provider
function ChannelProvider({ channelId, children }) {
  const { state, update, submit } = useGlobalChannel(channelId)
  
  return (
    <Composer.Provider
      state={state}
      actions={{ update, submit }}
      meta={{ inputRef: useRef(null) }}
    >
      {children}
    </Composer.Provider>
  )
}

// UI only knows the interface
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Input />  {/* Works with any provider */}
      <Composer.Submit />
    </Composer.Frame>
  )
}
```

---

## 快速参考（Quick Reference）

| 不推荐的做法 | 推荐的解决方案 |
|--------------|----------|
| 使用布尔型属性 | 使用明确的变体组件 |
| 用渲染属性来构建组件结构 | 使用子组件进行组合 |
- 将状态放在组件内部 | 将状态管理提升到提供者中 |
- 使组件依赖于具体的状态实现 | 使用通用的上下文接口 |
- 使用大量的条件渲染 | 明确地组合组件的各个部分 |

---

## 相关文件（Related Files）：

- `rules/architecture-avoid-boolean-props.md` - 关于避免使用布尔型属性的详细指导
- `rules/architecture-compound-components.md` - 复合组件模式
- `rules/state-context-interface.md` - 上下文接口的设计
- `rules/state-decouple-implementation.md` - 状态的解耦
- `rules/state-lift-state.md` - 提供者模式
- `rules/patterns-explicit-variants.md` - 明确的变体组件
- `rules/patterns-children-over-render-props.md` - 使用子组件进行组合

---

**注意事项：**

- **切勿**：
  - 为了自定义组件行为而添加布尔型属性（应使用组合模式）
  - 创建具有超过 2-3 个布尔型属性的组件
  - 将 UI 组件与特定的状态实现绑定在一起
  - 在子组件需要访问状态时使用渲染属性
  - 将状态封闭在组件内部，而让同级组件无法访问