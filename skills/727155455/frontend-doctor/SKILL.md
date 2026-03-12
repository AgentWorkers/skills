---
name: Frontend Doctor
description: 诊断并解决常见的前端问题——白屏、JavaScript错误、资源加载失败、React/Vue组件的渲染问题、浏览器扩展程序弹窗以及CSS布局错误。
metadata:
  openclaw:
    emoji: 🩺
    homepage: https://github.com/openclaw/clawhub
    skillKey: frontend-doctor
    always: false
    requires:
      bins:
        - node
---
# 前端问题诊断与修复指南

作为一名资深的前端工程师和调试专家，当用户遇到前端问题时，请按照以下诊断流程来定位问题的根本原因，并提供具体的解决方案。

## 支持的问题类型

1. **白屏** — 页面完全空白，没有任何可见内容
2. **JavaScript错误** — 运行时出现的JavaScript异常导致页面崩溃
3. **资源加载失败** — 脚本、样式表、字体或图片无法加载（404错误、CORS问题、CSP策略问题）
4. **React/Vuehydration错误** — 预渲染（SSR/SSG）后的数据与客户端渲染结果不匹配
5. **浏览器扩展程序弹窗未显示** — 点击扩展程序图标无反应或弹窗内容为空
6. **CSS布局问题** — 布局混乱、元素溢出、`z-index`设置错误、Flexbox或Grid布局错位

---

## 诊断流程

### 第一步：收集相关信息

向用户询问以下信息：
- 使用的框架/库（React、Vue、Svelte、纯JavaScript等）
- 构建工具（Vite、Webpack、Next.js、Nuxt等）
- 浏览器型号及版本
- 具体的错误信息或症状
- 相关的代码片段（组件代码、配置文件、HTML代码）
- 控制台输出（错误信息、警告提示）
- 网络请求的详细信息（请求失败、状态码等）

### 第二步：进行针对性诊断

#### 🔲 白屏问题

**常见原因：**
- JavaScript代码包加载失败或在组件挂载前抛出异常
- HTML文件中缺少根元素（`#app`、`#root`）
- 路由器配置错误（单页应用在刷新时显示404错误）
- 构建过程中缺少环境变量
- 异步组件或懒加载的代码在加载完成前就引发了错误

**检查清单：**
```
□ Open DevTools → Console: any uncaught errors?
□ Open DevTools → Network: is main bundle (main.js / chunk.js) returning 200?
□ Check HTML source: does <div id="root"> or <div id="app"> exist?
□ Check if window.__INITIAL_STATE__ or similar SSR data is missing
□ Add error boundary (React) or errorCaptured (Vue) to catch silent throws
□ Verify VITE_* / NEXT_PUBLIC_* env vars are set in production build
```

**快速修复方法：**
```jsx
// React: Add error boundary at root
class ErrorBoundary extends React.Component {
  state = { error: null }
  componentDidCatch(error) { this.setState({ error }) }
  render() {
    if (this.state.error) return <pre>{this.state.error.message}</pre>
    return this.props.children
  }
}
```

```js
// Vite SPA: fix 404 on refresh — configure server fallback
// vite.config.ts
export default { server: { historyApiFallback: true } }
// For nginx: try_files $uri $uri/ /index.html;
```

---

#### ⚠️ JavaScript错误

**常见原因：**
- 试图访问`undefined`或`null`对象的属性
- 模块未找到或导入路径错误
- 异步请求未完成就尝试访问相关资源
- 第三方脚本之间存在冲突
- TypeScript编译结果不符合预期

**检查清单：**
```
□ Read the full stack trace — find YOUR file, not node_modules
□ Check if the error is in an async callback (add try/catch)
□ Verify all imports resolve (check tsconfig paths, aliases)
□ Check if optional chaining (?.) is needed
□ Look for useEffect cleanup missing (React)
```

**快速修复方法：**
```js
// Safe optional chaining
const name = user?.profile?.name ?? 'Anonymous'

// React: cancel async on unmount
useEffect(() => {
  let cancelled = false
  fetchData().then(data => { if (!cancelled) setData(data) })
  return () => { cancelled = true }
}, [])
```

---

#### 📦 资源加载失败

**常见原因：**
- 构建配置中的`publicPath`或`base`路径设置错误
- CDN或API请求缺少CORS头信息
- 内容安全策略（CSP）阻止了脚本的加载
- 部署后资源哈希值发生变化（导致缓存失效）
- CSS文件中引用的字体/图片路径错误

**检查清单：**
```
□ Network tab: check exact URL being requested vs actual file location
□ Check response headers for CORS: Access-Control-Allow-Origin
□ Check browser console for CSP violations
□ Verify base URL in vite.config.ts / next.config.js / webpack output.publicPath
□ Hard refresh (Cmd+Shift+R) to rule out cache
```

**快速修复方法：**
```ts
// vite.config.ts — fix base path for subdirectory deploy
export default defineConfig({ base: '/my-app/' })

// next.config.js — fix asset prefix
module.exports = { assetPrefix: 'https://cdn.example.com' }
```

```nginx
# nginx CORS for fonts/assets
location ~* \.(woff2?|ttf|eot|svg)$ {
  add_header Access-Control-Allow-Origin *;
}
```

---

#### ⚛️ React/Vuehydration错误

**常见原因：**
- 服务器返回的HTML内容与客户端渲染的内容不匹配（如日期、随机ID、`window`对象的检查结果不一致）
- 在组件渲染过程中错误地使用了`typeof window !== 'undefined'`来判断窗口是否已加载
- 第三方组件不支持预渲染（SSR）
- HTML代码中的空白字符设置不正确

**React组件的检查清单：**
```
□ Error: "Hydration failed because the initial UI does not match"
□ Find component that reads browser-only APIs (localStorage, window, Date.now())
□ Wrap browser-only code in useEffect or dynamic import with ssr: false
```

**快速修复方法：**
```jsx
// Next.js: disable SSR for a component
import dynamic from 'next/dynamic'
const BrowserOnlyChart = dynamic(() => import('./Chart'), { ssr: false })

// React 18: suppress hydration warning for intentional mismatch
<time suppressHydrationWarning>{new Date().toLocaleString()}</time>
```

**Vue/Nuxt组件的检查清单：**
```
□ Error: "Hydration node mismatch"
□ Use <ClientOnly> wrapper for browser-only components
□ Avoid v-if based on window/document in SSR context
```

```vue
<!-- Nuxt: wrap browser-only content -->
<ClientOnly>
  <BrowserOnlyComponent />
</ClientOnly>
```

---

#### 🧩 浏览器扩展程序弹窗未显示

**常见原因：**
- `manifest.json`文件中未声明弹窗相关的配置
- 内容安全策略阻止了弹窗中的脚本执行
- 弹窗脚本在渲染前抛出了JavaScript错误
- 使用了错误的Manifest V3版本，导致服务工作者（service worker）未正确注册
- 开发服务器的URL被误用为扩展程序的URL

**检查清单：**
```
□ Check manifest.json → action.default_popup points to correct HTML file
□ Open chrome://extensions → click "Errors" button on your extension
□ Right-click extension icon → "Inspect popup" → check Console
□ Verify popup.html has <script src="popup.js"> (no inline scripts in MV3)
□ Check that popup.js is listed in web_accessible_resources if needed
```

**快速修复方法：**
```json
// manifest.json (MV3)
{
  "manifest_version": 3,
  "action": {
    "default_popup": "popup.html",
    "default_icon": "icon.png"
  },
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'"
  }
}
```

```html
<!-- popup.html — no inline scripts allowed in MV3 -->
<!DOCTYPE html>
<html>
  <body>
    <div id="root"></div>
    <script src="popup.js"></script>
  </body>
</html>
```

---

#### 🎨 CSS布局问题

**常见原因：**
- Flexbox或Grid布局中的子元素溢出问题
- `z-index`设置不正确，导致元素堆叠顺序错误
- 使用`position: absolute`时父元素的定位方式不正确
- 在移动设备上`100vh`的布局失效
- 边距塌陷（margin collapse）现象
- CSS选择器的优先级冲突

**检查清单：**
```
□ Open DevTools → Elements → Computed styles: check display, position, overflow
□ Use DevTools Layout panel to visualize flex/grid
□ Check if z-index parent has position set (required for z-index to work)
□ Check if overflow: hidden on parent clips child
□ Use outline: 1px solid red on elements to debug box model
```

**快速修复方法：**
```css
/* Fix z-index not working — parent needs a stacking context */
.parent {
  position: relative; /* or absolute/fixed/sticky */
  z-index: 0;
}

/* Fix 100vh on mobile */
.full-height {
  height: 100vh;
  height: 100dvh; /* dynamic viewport height */
}

/* Fix flex child overflow */
.flex-child {
  min-width: 0; /* allows text truncation inside flex */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Debug layout quickly */
* { outline: 1px solid rgba(255, 0, 0, 0.2); }
```

---

## 第三步：提供解决方案

诊断完成后，需要提供以下内容：
1. **根本原因** — 用一句话清晰地说明问题所在
2. **修复方案** — 包含必要的代码修改（如有必要，可提供修改前后的对比）
3. **验证方法** — 说明如何确认修复方案有效
4. **预防措施** — 提供避免问题再次发生的建议

---

## 使用示例

```
/frontend-doctor my Next.js page is white screen in production but works locally
/frontend-doctor React hydration error: "did not match. Server: 'div' Client: 'span'"
/frontend-doctor Chrome extension popup blank after clicking icon
/frontend-doctor flexbox items overflowing container on mobile
/frontend-doctor CORS error loading fonts from CDN
```