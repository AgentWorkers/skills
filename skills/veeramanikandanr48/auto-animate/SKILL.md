---
name: auto-animate
description: |
  Zero-config animations for React, Vue, Solid, Svelte, Preact with @formkit/auto-animate (3.28kb). Prevents 15 documented errors including React 19 StrictMode bugs, SSR imports, conditional parents, viewport issues, drag & drop conflicts, and CSS transform bugs.

  Use when: animating lists/accordions/toasts, troubleshooting SSR animation errors, React 19 StrictMode issues, or need accessible drop-in transitions with auto prefers-reduced-motion.
user-invocable: true
---

# AutoAnimate - 错误预防指南

**包版本**: @formkit/auto-animate@0.9.0（当前版本）  
**支持的框架**: React, Vue, Solid, Svelte, Preact  
**最后更新时间**: 2026-01-21  

---

## SSR安全模式（对Cloudflare Workers/Next.js至关重要）  
```tsx
// Use client-only import to prevent SSR errors
import { useState, useEffect } from "react";

export function useAutoAnimateSafe<T extends HTMLElement>() {
  const [parent, setParent] = useState<T | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && parent) {
      import("@formkit/auto-animate").then(({ default: autoAnimate }) => {
        autoAnimate(parent);
      });
    }
  }, [parent]);

  return [parent, setParent] as const;
}
```  

**重要性**: 该模式可防止问题#1（SSR/Next.js导入错误）。AutoAnimate使用了在服务器端不可用的DOM API。  

---

## 已知问题的预防措施（共15个记录在案的错误）  
本功能可预防**15个**已记录在案的错误：  

### 问题#1：SSR/Next.js导入错误  
**错误**: “无法从非ECMAScript模块中导入‘useEffect’”  
**来源**: https://github.com/formkit/auto-animate/issues/55  
**原因**: AutoAnimate使用了在服务器端不可用的DOM API  
**预防措施**: 使用动态导入（参见`templates/vite-ssr-safe.tsx`）  

### 问题#2：条件性父元素渲染  
**错误**: 当父元素为条件渲染时，动画无法正常工作  
**来源**: https://github.com/formkit/auto-animate/issues/8  
**原因**: 参考（ref）无法绑定到不存在的元素上  
**预防措施**：  

**React解决方案**:  
```tsx
// ❌ Wrong
{showList && <ul ref={parent}>...</ul>}

// ✅ Correct
<ul ref={parent}>{showList && items.map(...)}</ul>
```  

**Vue.js解决方案**:  
```vue
<!-- ❌ Wrong - parent conditional -->
<ul v-if="showList" ref="parent">
  <li v-for="item in items" :key="item.id">{{ item.text }}</li>
</ul>

<!-- ✅ Correct - children conditional -->
<ul ref="parent">
  <li v-if="showList" v-for="item in items" :key="item.id">
    {{ item.text }}
  </li>
</ul>
```  
**来源**: React [问题#8](https://github.com/formkit/auto-animate/issues/8), Vue [问题#193](https://github.com/formkit/auto-animate/issues/193)  

### 问题#3：缺少唯一键  
**错误**: 元素无法正确动画或出现闪烁  
**来源**: 官方文档  
**原因**: React无法追踪哪些元素发生了变化  
**预防措施**: 始终使用唯一且稳定的键（`key={item.id}`）  

### 问题#4：Flexbox宽度和抖动问题  
**错误**: 元素会突然改变宽度，而不是平滑动画；或者在移除元素时容器会抖动  
**来源**: 官方文档，[问题#212](https://github.com/formkit/auto-animate/issues/212)  
**原因**: `flex-grow: 1` 会等待周围内容的变化，导致动画时机问题  
**预防措施**: 对于需要动画的元素，使用固定宽度而非`flex-grow`  
**代码示例**:  
```tsx
// ❌ Wrong - causes shaking
<ul ref={parent} style={{ display: 'flex' }}>
  {items.map(item => (
    <li key={item.id} style={{ flex: '1 1 auto' }}>{item.text}</li>
  ))}
</ul>

// ✅ Correct - fixed sizes
<ul ref={parent} style={{ display: 'flex', gap: '1rem' }}>
  {items.map(item => (
    <li
      key={item.id}
      style={{ minWidth: '200px', maxWidth: '200px' }}
    >
      {item.text}
    </li>
  ))}
</ul>
```  
**维护者备注**: justin-schroeder确认，对于Flex容器来说，使用固定宽度是必要的。  

### 问题#5：表格行显示问题  
**错误**: 移除表格行时，表格结构会破坏  
**来源**: https://github.com/formkit/auto-animate/issues/7  
**原因**: `table-row`的渲染方式与动画冲突  
**预防措施**: 将动画应用于`<tbody>`而不是单个行，或者使用基于`div`的布局  

### 问题#6：Jest测试错误  
**错误**: “找不到模块‘@formkit/auto-animate/react’”  
**来源**: https://github.com/formkit/auto-animate/issues/29  
**原因**: Jest无法正确解析ESM导出  
**预防措施**: 在`jest.config.js`中配置`moduleNameMapper`  

### 问题#7：esbuild兼容性问题  
**错误**: “路径‘.’未被该包导出”  
**来源**: https://github.com/formkit/auto-animate/issues/36  
**原因**: ESM与CommonJS之间的条件不匹配  
**预防措施**: 配置esbuild以正确处理ESM模块  

### 问题#8：CSS定位副作用  
**错误**: 添加AutoAnimate后，布局会出问题  
**来源**: 官方文档  
**原因**: 父元素的`position`属性会被自动设置为`relative`  
**预防措施**: 在CSS中处理位置变化，或明确设置`position`属性  

### 问题#9：Vue/Nuxt注册错误  
**错误**: “无法解析auto-animate指令”  
**来源**: https://github.com/formkit/auto-animate/issues/43  
**原因**: 插件未正确注册  
**预防措施**: 在Vue/Nuxt配置中正确设置插件（参见相关参考资料）  
**Nuxt 3注意事项**: 需要使用v0.8.2及以上版本（2024年4月发布）。早期版本存在ESM导入问题，已由Daniel Roe修复（参见[问题#199](https://github.com/formkit/auto-animate/issues/199)）。  

### 问题#10：Angular ESM相关问题  
**错误**: 使用Angular构建时出现错误  
**来源**: https://github.com/formkit/auto-animate/issues/72  
**原因**: 使用的是CommonJS构建环境  
**预防措施**: 需要为Angular包配置`ng-packagr`  

### 问题#11：React 19的StrictMode导致的重复调用问题  
**错误**: 在React 19的StrictMode下，子元素的动画无法正常工作  
**来源**: https://github.com/formkit/auto-animate/issues/232  
**原因**: StrictMode会多次调用`useEffect`，导致autoAnimate被重复初始化  
**预防措施**: 使用`ref`来跟踪初始化状态  
**代码示例**:  
```tsx
// ❌ Wrong - breaks in StrictMode
const [parent] = useAutoAnimate();

// ✅ Correct - prevents double initialization
const [parent] = useAutoAnimate();
const initialized = useRef(false);

useEffect(() => {
  if (initialized.current) return;
  initialized.current = true;
}, []);
```  
**注意**: React 19在开发模式下默认启用StrictMode，这会影响所有使用React 19的项目。  

### 问题#12：动画在视口外失效  
**错误**: 当列表超出视口时，动画会失效  
**来源**: https://github.com/formkit/auto-animate/issues/222  
**原因**: Chrome可能不会对视口外的元素执行动画API  
**预防措施**: 在应用autoAnimate之前，确保父元素可见  

---  

## 关键规则（错误预防）  

### 必须执行的操作：  
✅ **使用唯一且稳定的键** - 使用`key={item.id}`而非`key={index}`  
✅ **确保父元素始终在DOM中渲染**  
✅ **仅在客户端环境中使用（SSR场景）** - 对服务器环境使用动态导入  
✅ **尊重无障碍设置** - 保持`disrespectUserMotionPreference: false`  
✅ **禁用动画后进行测试** - 确认UI在没有动画的情况下仍能正常工作  
✅ **对需要动画的元素使用固定宽度**  
✅ **对表格应用动画时使用`<tbody>`而非单个行**  

### 绝对不能执行的操作：  
❌ **条件性渲染父元素** - 如`{show && <ul ref={parent}>`  
❌ **使用索引作为键** - `key={index}`会导致动画失效  
❌ **忽略SSR模式** - 这会在Cloudflare Workers/Next.js环境中引发问题  
❌ **强制执行动画** - 设置`disrespectUserMotionPreference: true`会破坏无障碍性  
❌ **直接对表格应用动画** - 应使用`<tbody>`或基于`div`的布局  
❌ **省略唯一键** - 这是正确动画所必需的  
❌ **使用复杂的动画效果** - 可以考虑使用其他库（如Motion）  

**注意**: AutoAnimate会自动遵循`prefers-reduced-motion`设置（切勿禁用该功能）。  

---

## 社区提示（来自社区的建议）  
> **注意**: 这些提示来自社区讨论，请根据您的版本进行验证。  

### 提示：使用模拟包防止测试冻结  
**来源**: [问题#230](https://github.com/formkit/auto-animate/issues/230) | **可靠性**: 中等  
**适用版本**: v0.8.2及以上  
**解决方法**: 在测试时添加`ResizeObserver`模拟：  
```typescript
// jest.setup.js
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

// __mocks__/@formkit/auto-animate.js
const autoAnimate = jest.fn(() => () => {});
const useAutoAnimate = jest.fn(() => [null, jest.fn(), jest.fn()]);
module.exports = { default: autoAnimate, useAutoAnimate };
```  

### 提示：防止内存泄漏  
**来源**: [问题#180](https://github.com/formkit/auto-animate/issues/180) | **可靠性**: 低  
**适用版本**: 所有版本  
**建议**: 对于长时间运行的单页应用（SPAs），确保及时清理资源：  
```tsx
useEffect(() => {
  const cleanup = autoAnimate(parent.current);
  return () => cleanup && cleanup();
}, []);

// useAutoAnimate hook handles cleanup automatically
const [parent] = useAutoAnimate(); // Preferred
```  

---

## 包版本信息  
**最新版本**: @formkit/auto-animate@0.9.0（2025年9月5日）  
**近期发布**:  
- v0.9.0（2025年9月5日） - 当前稳定版本  
- v0.8.2（2024年4月10日） - 修复了Nuxt 3的ESM导入问题及`ResizeObserver`相关问题  
**代码示例**:  
```json
{
  "dependencies": {
    "@formkit/auto-animate": "^0.9.0"
  }
}
```  

**框架兼容性**: React 18及以上版本，Vue 3及以上版本，Solid，Svelte，Preact  

**重要提示**: 对于Nuxt 3用户，需要使用v0.8.2及以上版本。早期版本存在ESM导入问题。  

---

## 官方文档  
- **官方网站**: https://auto-animate.formkit.com  
- **GitHub仓库**: https://github.com/formkit/auto-animate  
- **npm**: https://www.npmjs.com/package/@formkit/auto-animate  
- **React文档**: https://auto-animate.formkit.com/react  

---

## 模板与参考资料  
请查看随包提供的资源：  
- `templates/` - 包含可复用的示例（适用于SSR安全模式、折叠面板、提示框、表单等）  
- `references/` - 包含CSS冲突解决方案、SSR相关模式及库对比信息