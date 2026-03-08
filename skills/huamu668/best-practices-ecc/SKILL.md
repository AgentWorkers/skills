---
name: best-practices
description: 应用现代Web开发的最佳实践，以确保安全性、兼容性、代码质量和编码标准。涵盖KISS/DRY/YAGNI原则、TypeScript/JavaScript编程规范、React开发模式、运行时代码质量检查机制，以及全面的代码审查清单。
license: MIT
metadata:
  author: web-quality-skills
  version: "2.0"
  origin: "ECC + web-quality-skills"
---
# 最佳实践

本文档遵循基于 Lighthouse 最佳实践审计的现代 Web 开发标准以及经过生产环境验证的编码规范，涵盖了安全性、浏览器兼容性、代码质量模式以及代码编写时的质量控制措施。

## 代码质量原则

### 1. 可读性优先
- 代码的阅读频率远高于编写频率
- 变量和函数名称应清晰明了
- 优先使用能够自我解释的代码而非注释
- 保持代码格式的一致性

### 2. KISS（保持简单）
- 选择最简单且有效的解决方案
- 避免过度设计
- 不要过早进行优化
- 理解代码比编写复杂的代码更为重要

### 3. DRY（避免重复）
- 将常见的逻辑提取到函数中
- 创建可重用的组件
- 在不同模块之间共享实用工具
- 避免复制粘贴代码

### 4. YAGNI（你不会需要它）
- 在实际需要之前不要开发功能
- 避免过度泛化
- 仅在必要时增加复杂性
- 从简单开始，必要时再进行重构

---

## TypeScript/JavaScript 标准

### 变量命名

```typescript
// ✅ GOOD: Descriptive names
const marketSearchQuery = 'election'
const isUserAuthenticated = true
const totalRevenue = 1000

// ❌ BAD: Unclear names
const q = 'election'
const flag = true
const x = 1000
```

### 函数命名

```typescript
// ✅ GOOD: Verb-noun pattern
async function fetchMarketData(marketId: string) { }
function calculateSimilarity(a: number[], b: number[]) { }
function isValidEmail(email: string): boolean { }

// ❌ BAD: Unclear or noun-only
async function market(id: string) { }
function similarity(a, b) { }
function email(e) { }
```

### 不可变性模式（至关重要）

```typescript
// ✅ ALWAYS use spread operator
const updatedUser = {
  ...user,
  name: 'New Name'
}

const updatedArray = [...items, newItem]

// ❌ NEVER mutate directly
user.name = 'New Name'  // BAD
items.push(newItem)     // BAD
```

### 错误处理

```typescript
// ✅ GOOD: Comprehensive error handling
async function fetchData(url: string) {
  try {
    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw new Error('Failed to fetch data')
  }
}

// ❌ BAD: No error handling
async function fetchData(url) {
  const response = await fetch(url)
  return response.json()
}
```

### 异步/等待最佳实践

```typescript
// ✅ GOOD: Parallel execution when possible
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats()
])

// ❌ BAD: Sequential when unnecessary
const users = await fetchUsers()
const markets = await fetchMarkets()
const stats = await fetchStats()
```

### 类型安全

```typescript
// ✅ GOOD: Proper types
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
  created_at: Date
}

function getMarket(id: string): Promise<Market> {
  // Implementation
}

// ❌ BAD: Using 'any'
function getMarket(id: any): Promise<any> {
  // Implementation
}
```

---

## React 最佳实践

### 组件结构

```typescript
// ✅ GOOD: Functional component with types
interface ButtonProps {
  children: React.ReactNode
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({
  children,
  onClick,
  disabled = false,
  variant = 'primary'
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  )
}

// ❌ BAD: No types, unclear structure
export function Button(props) {
  return <button onClick={props.onClick}>{props.children}</button>
}
```

### 自定义钩子

```typescript
// ✅ GOOD: Reusable custom hook
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}

// Usage
const debouncedSearch = useDebounce(searchQuery, 300)
```

---

## 代码审查检查清单

### 提交前的自我检查

在提交代码进行审查之前，请确保：

```markdown
### Functionality
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] Error paths tested
- [ ] No hardcoded secrets or values

### Code Quality
- [ ] Follows naming conventions
- [ ] No code duplication (DRY)
- [ ] Functions are focused (single responsibility)
- [ ] No unnecessary complexity (KISS)
- [ ] No speculative features (YAGNI)

### TypeScript/JavaScript
- [ ] Proper types (no `any`)
- [ ] Null checks where needed
- [ ] Async/await used correctly
- [ ] No mutation of props/state

### React
- [ ] Proper hook dependencies
- [ ] No memory leaks (cleanup)
- [ ] Keys provided for lists
- [ ] Accessibility attributes

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests if needed
- [ ] All tests passing
- [ ] No test coverage gaps

### Documentation
- [ ] Complex logic commented
- [ ] API changes documented
- [ ] README updated if needed
```

---

## 编码时的质量控制

### 保存时自动格式化

配置编辑器，在保存代码时自动格式化：

```json
// VS Code settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[typescript]": {
    "editor.defaultFormatter": "vscode.typescript-language-features"
  }
}
```

### 提交前钩子

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{js,jsx}": ["eslint --fix", "prettier --write"]
  }
}
```

### Claude 代码钩子集成

在 Claude 代码会话期间，利用这些钩子实现自动代码质量检查：

```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "npm run lint:fix"
      }]
    }]
  }
}
```

---

## 安全性

### 全部使用 HTTPS

**强制使用 HTTPS：**
```html
<!-- ❌ Mixed content -->
<img src="http://example.com/image.jpg">
<script src="http://cdn.example.com/script.js"></script>

<!-- ✅ HTTPS only -->
<img src="https://example.com/image.jpg">
<script src="https://cdn.example.com/script.js"></script>

<!-- ✅ Protocol-relative (will use page's protocol) -->
<img src="//example.com/image.jpg">
```

**HSTS 头部：**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

### 内容安全策略（CSP）

```html
<!-- Basic CSP via meta tag -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' https://trusted-cdn.com; 
               style-src 'self' 'unsafe-inline';
               img-src 'self' data: https:;
               connect-src 'self' https://api.example.com;">

<!-- Better: HTTP header -->
```

**推荐的 CSP 头部：**
```
Content-Security-Policy: 
  default-src 'self';
  script-src 'self' 'nonce-abc123' https://trusted.com;
  style-src 'self' 'nonce-abc123';
  img-src 'self' data: https:;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'self';
  base-uri 'self';
  form-action 'self';
```

**为内联脚本使用随机数：**
```html
<script nonce="abc123">
  // This inline script is allowed
</script>
```

### 安全头部

```
# Prevent clickjacking
X-Frame-Options: DENY

# Prevent MIME type sniffing
X-Content-Type-Options: nosniff

# Enable XSS filter (legacy browsers)
X-XSS-Protection: 1; mode=block

# Control referrer information
Referrer-Policy: strict-origin-when-cross-origin

# Permissions policy (formerly Feature-Policy)
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

### 避免使用有漏洞的库

```bash
# Check for vulnerabilities
npm audit
yarn audit

# Auto-fix when possible
npm audit fix

# Check specific package
npm ls lodash
```

**保持依赖项更新：**
```json
// package.json
{
  "scripts": {
    "audit": "npm audit --audit-level=moderate",
    "update": "npm update && npm audit fix"
  }
}
```

**需要避免的已知漏洞模式：**
```javascript
// ❌ Prototype pollution vulnerable patterns
Object.assign(target, userInput);
_.merge(target, userInput);

// ✅ Safer alternatives
const safeData = JSON.parse(JSON.stringify(userInput));
```

### 输入验证

```javascript
// ❌ XSS vulnerable
element.innerHTML = userInput;
document.write(userInput);

// ✅ Safe text content
element.textContent = userInput;

// ✅ If HTML needed, sanitize
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 安全的 Cookie

```javascript
// ❌ Insecure cookie
document.cookie = "session=abc123";

// ✅ Secure cookie (server-side)
Set-Cookie: session=abc123; Secure; HttpOnly; SameSite=Strict; Path=/
```

---

## 浏览器兼容性

### doctype 声明

```html
<!-- ❌ Missing or invalid doctype -->
<HTML>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">

<!-- ✅ HTML5 doctype -->
<!DOCTYPE html>
<html lang="en">
```

### 字符编码

```html
<!-- ❌ Missing or late charset -->
<html>
<head>
  <title>Page</title>
  <meta charset="UTF-8">
</head>

<!-- ✅ Charset as first element in head -->
<html>
<head>
  <meta charset="UTF-8">
  <title>Page</title>
</head>
```

### 视口元标签

```html
<!-- ❌ Missing viewport -->
<head>
  <title>Page</title>
</head>

<!-- ✅ Responsive viewport -->
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page</title>
</head>
```

### 特性检测

```javascript
// ❌ Browser detection (brittle)
if (navigator.userAgent.includes('Chrome')) {
  // Chrome-specific code
}

// ✅ Feature detection
if ('IntersectionObserver' in window) {
  // Use IntersectionObserver
} else {
  // Fallback
}

// ✅ Using @supports in CSS
@supports (display: grid) {
  .container {
    display: grid;
  }
}

@supports not (display: grid) {
  .container {
    display: flex;
  }
}
```

### 在需要时使用 Polyfill

```html
<!-- Load polyfills conditionally -->
<script>
  if (!('fetch' in window)) {
    document.write('<script src="/polyfills/fetch.js"><\/script>');
  }
</script>

<!-- Or use polyfill.io -->
<script src="https://polyfill.io/v3/polyfill.min.js?features=fetch,IntersectionObserver"></script>
```

---

## 已弃用的 API

### 避免使用这些 API

```javascript
// ❌ document.write (blocks parsing)
document.write('<script src="..."></script>');

// ✅ Dynamic script loading
const script = document.createElement('script');
script.src = '...';
document.head.appendChild(script);

// ❌ Synchronous XHR (blocks main thread)
const xhr = new XMLHttpRequest();
xhr.open('GET', url, false); // false = synchronous

// ✅ Async fetch
const response = await fetch(url);

// ❌ Application Cache (deprecated)
<html manifest="cache.manifest">

// ✅ Service Workers
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
```

### 事件监听器的被动模式

```javascript
// ❌ Non-passive touch/wheel (may block scrolling)
element.addEventListener('touchstart', handler);
element.addEventListener('wheel', handler);

// ✅ Passive listeners (allows smooth scrolling)
element.addEventListener('touchstart', handler, { passive: true });
element.addEventListener('wheel', handler, { passive: true });

// ✅ If you need preventDefault, be explicit
element.addEventListener('touchstart', handler, { passive: false });
```

---

## 控制台与错误处理

### 不要显示控制台错误

```javascript
// ❌ Errors in production
console.log('Debug info'); // Remove in production
throw new Error('Unhandled'); // Catch all errors

// ✅ Proper error handling
try {
  riskyOperation();
} catch (error) {
  // Log to error tracking service
  errorTracker.captureException(error);
  // Show user-friendly message
  showErrorMessage('Something went wrong. Please try again.');
}
```

### 错误处理（React）

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, info) {
    errorTracker.captureException(error, { extra: info });
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

### 全局错误处理器

```javascript
// Catch unhandled errors
window.addEventListener('error', (event) => {
  errorTracker.captureException(event.error);
});

// Catch unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  errorTracker.captureException(event.reason);
});
```

---

## 源映射

### 生产环境配置

```javascript
// ❌ Source maps exposed in production
// webpack.config.js
module.exports = {
  devtool: 'source-map', // Exposes source code
};

// ✅ Hidden source maps (uploaded to error tracker)
module.exports = {
  devtool: 'hidden-source-map',
};

// ✅ Or no source maps in production
module.exports = {
  devtool: process.env.NODE_ENV === 'production' ? false : 'source-map',
};
```

---

## 性能最佳实践

### 避免阻塞操作

```javascript
// ❌ Blocking script
<script src="heavy-library.js"></script>

// ✅ Deferred script
<script defer src="heavy-library.js"></script>

// ❌ Blocking CSS import
@import url('other-styles.css');

// ✅ Link tags (parallel loading)
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="other-styles.css">
```

### 高效的事件处理

```javascript
// ❌ Handler on every element
items.forEach(item => {
  item.addEventListener('click', handleClick);
});

// ✅ Event delegation
container.addEventListener('click', (e) => {
  if (e.target.matches('.item')) {
    handleClick(e);
  }
});
```

### 内存管理

```javascript
// ❌ Memory leak (never removed)
const handler = () => { /* ... */ };
window.addEventListener('resize', handler);

// ✅ Cleanup when done
const handler = () => { /* ... */ };
window.addEventListener('resize', handler);

// Later, when component unmounts:
window.removeEventListener('resize', handler);

// ✅ Using AbortController
const controller = new AbortController();
window.addEventListener('resize', handler, { signal: controller.signal });

// Cleanup:
controller.abort();
```

---

## 代码质量

### 合法的 HTML

```html
<!-- ❌ Invalid HTML -->
<div id="header">
<div id="header"> <!-- Duplicate ID -->

<ul>
  <div>Item</div> <!-- Invalid child -->
</ul>

<a href="/"><button>Click</button></a> <!-- Invalid nesting -->

<!-- ✅ Valid HTML -->
<header id="site-header">
</header>

<ul>
  <li>Item</li>
</ul>

<a href="/" class="button">Click</a>
```

### 语义化 HTML

```html
<!-- ❌ Non-semantic -->
<div class="header">
  <div class="nav">
    <div class="nav-item">Home</div>
  </div>
</div>
<div class="main">
  <div class="article">
    <div class="title">Headline</div>
  </div>
</div>

<!-- ✅ Semantic HTML5 -->
<header>
  <nav>
    <a href="/">Home</a>
  </nav>
</header>
<main>
  <article>
    <h1>Headline</h1>
  </article>
</main>
```

### 图像的宽高比

```html
<!-- ❌ Distorted images -->
<img src="photo.jpg" width="300" height="100">
<!-- If actual ratio is 4:3, this squishes the image -->

<!-- ✅ Preserve aspect ratio -->
<img src="photo.jpg" width="300" height="225">
<!-- Actual 4:3 dimensions -->

<!-- ✅ CSS object-fit for flexibility -->
<img src="photo.jpg" style="width: 300px; height: 200px; object-fit: cover;">
```

---

## 权限与隐私

### 正确请求权限

```javascript
// ❌ Request on page load (bad UX, often denied)
navigator.geolocation.getCurrentPosition(success, error);

// ✅ Request in context, after user action
findNearbyButton.addEventListener('click', async () => {
  // Explain why you need it
  if (await showPermissionExplanation()) {
    navigator.geolocation.getCurrentPosition(success, error);
  }
});
```

### 权限策略

```html
<!-- Restrict powerful features -->
<meta http-equiv="Permissions-Policy" 
      content="geolocation=(), camera=(), microphone=()">

<!-- Or allow for specific origins -->
<meta http-equiv="Permissions-Policy" 
      content="geolocation=(self 'https://maps.example.com')">
```

---

## 审计检查清单

### 安全性（至关重要）
- [ ] 已启用 HTTPS，无混合内容
- [ ] 无漏洞依赖项（`npm audit`）
- [ ] 已配置 CSP 头部
- [ ] 已设置安全头部
- [ ] 无暴露的源映射文件

### 兼容性
- [ ] 使用有效的 HTML5 doctype
- [ ] 在 `<head>` 标签中首先声明字符集
- [ ] 已设置 viewport 元标签
- [ ] 未使用已弃用的 API
- [ ] 滚动/触摸事件使用被动监听器

### 代码质量
- [ ] 无控制台错误
- [ ] 使用有效的 HTML（无重复的 ID）
- [ ] 使用语义化的 HTML 元素
- [ ] 适当的错误处理
- [ ] 组件中的内存清理

### 用户体验
- [ ] 无侵入式的弹窗广告
- [ ] 在适当的情况下请求权限
- [ ] 明确的错误信息
- [ ] 适当的图像宽高比

## 工具

| 工具 | 用途 |
|------|---------|
| `npm audit` | 检查依赖项中的漏洞 |
| [SecurityHeaders.com](https://securityheaders.com) | 分析 HTTP 头部信息 |
| [W3C Validator](https://validator.w3.org) | HTML 验证 |
| Lighthouse | 最佳实践审计 |
| [Observatory](https://observatory.mozilla.org) | 安全性扫描 |

## 参考资料

- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web Quality Audit](../web-quality-audit/SKILL.md)