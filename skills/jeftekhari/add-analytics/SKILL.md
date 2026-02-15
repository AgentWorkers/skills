---
name: add-analytics
description: 将 Google Analytics 4 跟踪功能添加到任何项目中。该功能可以检测项目所使用的开发框架，自动插入跟踪代码，设置相关事件，并配置隐私设置。
argument-hint: "<measurement-id> [--events] [--consent] [--debug]"
---

# Google Analytics 4 设置指南

您正在为一个项目设置 Google Analytics 4 (GA4)。请按照本指南正确配置 Analytics。

## 参数

从 `$ARGUMENTS` 中解析以下内容：
- **测量 ID (Measurement ID)**：格式为 `G-XXXXXXXXXX`（必填，若未提供请询问）
- **--events**：包含自定义事件跟踪功能
- **--consent**：包含 cookie 同意集成功能
- **--debug**：启用调试模式以辅助开发

## 第 1 步：确定项目类型

扫描项目以确定其使用的框架/设置方式：

```
Priority detection order:
1. next.config.js/ts → Next.js
2. nuxt.config.js/ts → Nuxt.js
3. astro.config.mjs → Astro
4. svelte.config.js → SvelteKit
5. remix.config.js → Remix
6. gatsby-config.js → Gatsby
7. vite.config.js + src/App.vue → Vue + Vite
8. vite.config.js + src/App.tsx → React + Vite
9. angular.json → Angular
10. package.json with "react-scripts" → Create React App
11. index.html only → Plain HTML
12. _app.tsx/jsx → Next.js (App Router check: app/ directory)
```

同时检查以下内容：
- 是否使用了 TypeScript（查看 `tsconfig.json`）
- 是否已有 Analytics 配置（搜索 `gtag`、`GA`、`analytics`）
- 项目是否使用了包管理器（查看 `pnpm-lock.yaml`、`yarn.lock`、`package-lock.json`）

## 第 2 步：验证测量 ID

测量 ID 必须满足以下要求：
- 以 `G-` 开头（GA4 格式）
- 后面紧跟 10 个字母数字字符
- 例如：`G-ABC1234567`

如果用户提供了 `UA-` ID，请告知他们：
> “您提供的是一个 Universal Analytics ID（UA-）。GA4 使用以 ‘G-’ 开头的测量 ID。”
> Universal Analytics 于 2024 年 7 月停止支持。您需要在 analytics.google.com 上创建一个新的 GA4 账户。

## 第 3 步：根据框架进行配置

### Next.js（App Router - app/ 目录）

在 `app/layout.tsx` 中进行修改，或创建 `components/GoogleAnalytics.tsx` 文件：

```tsx
// components/GoogleAnalytics.tsx
'use client'

import Script from 'next/script'

interface GoogleAnalyticsProps {
  measurementId: string
}

export function GoogleAnalytics({ measurementId }: GoogleAnalyticsProps) {
  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`}
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${measurementId}');
        `}
      </Script>
    </>
  )
}
```

将相关代码添加到页面布局中：

```tsx
// app/layout.tsx
import { GoogleAnalytics } from '@/components/GoogleAnalytics'

// Add inside <body> or <html>:
<GoogleAnalytics measurementId="G-XXXXXXXXXX" />
```

### Next.js（Pages Router - pages/ 目录）

修改 `pages/_app.tsx` 文件：

```tsx
// pages/_app.tsx
import type { AppProps } from 'next/app'
import Script from 'next/script'

const GA_MEASUREMENT_ID = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`}
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${GA_MEASUREMENT_ID}');
        `}
      </Script>
      <Component {...pageProps} />
    </>
  )
}
```

### React（Vite/CRA）

创建 `src/lib/analytics.ts` 文件：

```typescript
// src/lib/analytics.ts
export const GA_MEASUREMENT_ID = import.meta.env.VITE_GA_MEASUREMENT_ID

declare global {
  interface Window {
    gtag: (...args: unknown[]) => void
    dataLayer: unknown[]
  }
}

export const initGA = () => {
  if (typeof window === 'undefined') return

  const script = document.createElement('script')
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`
  script.async = true
  document.head.appendChild(script)

  window.dataLayer = window.dataLayer || []
  window.gtag = function gtag() {
    window.dataLayer.push(arguments)
  }
  window.gtag('js', new Date())
  window.gtag('config', GA_MEASUREMENT_ID)
}

export const pageview = (url: string) => {
  window.gtag('config', GA_MEASUREMENT_ID, {
    page_path: url,
  })
}

export const event = (action: string, params?: Record<string, unknown>) => {
  window.gtag('event', action, params)
}
```

在 `src/main.tsx` 中初始化 Analytics：

```tsx
import { initGA } from './lib/analytics'

// Initialize before render
if (import.meta.env.PROD) {
  initGA()
}
```

### Vue 3（Vite）

创建 `src/plugins/analytics.ts` 文件：

```typescript
// src/plugins/analytics.ts
import type { App } from 'vue'
import type { Router } from 'vue-router'

const GA_MEASUREMENT_ID = import.meta.env.VITE_GA_MEASUREMENT_ID

declare global {
  interface Window {
    gtag: (...args: unknown[]) => void
    dataLayer: unknown[]
  }
}

export const analyticsPlugin = {
  install(app: App, { router }: { router: Router }) {
    // Load gtag script
    const script = document.createElement('script')
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`
    script.async = true
    document.head.appendChild(script)

    window.dataLayer = window.dataLayer || []
    window.gtag = function gtag() {
      window.dataLayer.push(arguments)
    }
    window.gtag('js', new Date())
    window.gtag('config', GA_MEASUREMENT_ID)

    // Track route changes
    router.afterEach((to) => {
      window.gtag('config', GA_MEASUREMENT_ID, {
        page_path: to.fullPath,
      })
    })

    // Provide global methods
    app.config.globalProperties.$gtag = window.gtag
  }
}
```

### Nuxt 3

创建 `plugins/analytics.client.ts` 文件：

```typescript
// plugins/analytics.client.ts
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const measurementId = config.public.gaMeasurementId

  if (!measurementId) return

  // Load gtag
  useHead({
    script: [
      {
        src: `https://www.googletagmanager.com/gtag/js?id=${measurementId}`,
        async: true,
      },
      {
        innerHTML: `
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${measurementId}');
        `,
      },
    ],
  })

  // Track route changes
  const router = useRouter()
  router.afterEach((to) => {
    window.gtag('config', measurementId, {
      page_path: to.fullPath,
    })
  })
})
```

将相关代码添加到 `nuxt.config.ts` 中：

```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      gaMeasurementId: process.env.NUXT_PUBLIC_GA_MEASUREMENT_ID,
    },
  },
})
```

### Astro

创建 `src/components/Analytics.astro` 文件：

```astro
---
// src/components/Analytics.astro
interface Props {
  measurementId: string
}

const { measurementId } = Astro.props
---

<script
  is:inline
  define:vars={{ measurementId }}
  src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`}
></script>

<script is:inline define:vars={{ measurementId }}>
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  gtag('js', new Date());
  gtag('config', measurementId);
</script>
```

将相关代码添加到页面布局中：

```astro
---
import Analytics from '../components/Analytics.astro'
---
<html>
  <head>
    <Analytics measurementId="G-XXXXXXXXXX" />
  </head>
</html>
```

### SvelteKit

创建 `src/lib/analytics.ts` 和 `src/routes/+layout.svelte` 文件：

```typescript
// src/lib/analytics.ts
import { browser } from '$app/environment'

export const GA_MEASUREMENT_ID = import.meta.env.VITE_GA_MEASUREMENT_ID

export function initGA() {
  if (!browser) return

  const script = document.createElement('script')
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`
  script.async = true
  document.head.appendChild(script)

  window.dataLayer = window.dataLayer || []
  window.gtag = function gtag() {
    window.dataLayer.push(arguments)
  }
  window.gtag('js', new Date())
  window.gtag('config', GA_MEASUREMENT_ID)
}

export function trackPageview(url: string) {
  if (!browser) return
  window.gtag('config', GA_MEASUREMENT_ID, { page_path: url })
}
```

```svelte
<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import { onMount } from 'svelte'
  import { page } from '$app/stores'
  import { initGA, trackPageview } from '$lib/analytics'

  onMount(() => {
    initGA()
  })

  $: if ($page.url.pathname) {
    trackPageview($page.url.pathname)
  }
</script>

<slot />
```

### 纯 HTML

将相关代码添加到 `<head>` 标签中：

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

## 第 4 步：设置环境变量

创建或更新 `.env` 或 `.env.local` 文件：

```bash
# For Next.js
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX

# For Vite (React/Vue/Svelte)
VITE_GA_MEASUREMENT_ID=G-XXXXXXXXXX

# For Nuxt
NUXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

如果已有 `.env.example` 文件，请将其内容添加到 `.env` 文件中（但不要包含实际的测量 ID）：

```bash
# Google Analytics 4 Measurement ID
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

**重要提示**：如果 `.env.local` 文件尚不存在，请将其添加到 `.gitignore` 文件中。

## 第 5 步：事件跟踪功能（如果使用了 `--events` 参数）

创建一个用于处理事件跟踪的实用工具函数：

```typescript
// lib/analytics-events.ts

/**
 * GA4 Event Tracking Utilities
 *
 * Recommended events: https://support.google.com/analytics/answer/9267735
 */

type GTagEvent = {
  action: string
  category?: string
  label?: string
  value?: number
  [key: string]: unknown
}

// Core event function
export const trackEvent = ({ action, category, label, value, ...rest }: GTagEvent) => {
  if (typeof window === 'undefined' || !window.gtag) return

  window.gtag('event', action, {
    event_category: category,
    event_label: label,
    value,
    ...rest,
  })
}

// Engagement events
export const trackClick = (elementName: string, location?: string) => {
  trackEvent({
    action: 'click',
    category: 'engagement',
    label: elementName,
    click_location: location,
  })
}

export const trackScroll = (percentage: number) => {
  trackEvent({
    action: 'scroll',
    category: 'engagement',
    value: percentage,
  })
}

// Conversion events
export const trackSignUp = (method: string) => {
  trackEvent({
    action: 'sign_up',
    method,
  })
}

export const trackLogin = (method: string) => {
  trackEvent({
    action: 'login',
    method,
  })
}

export const trackPurchase = (params: {
  transactionId: string
  value: number
  currency: string
  items?: Array<{
    itemId: string
    itemName: string
    price: number
    quantity: number
  }>
}) => {
  trackEvent({
    action: 'purchase',
    transaction_id: params.transactionId,
    value: params.value,
    currency: params.currency,
    items: params.items,
  })
}

// Content events
export const trackSearch = (searchTerm: string) => {
  trackEvent({
    action: 'search',
    search_term: searchTerm,
  })
}

export const trackShare = (method: string, contentType: string, itemId: string) => {
  trackEvent({
    action: 'share',
    method,
    content_type: contentType,
    item_id: itemId,
  })
}

// Form events
export const trackFormStart = (formName: string) => {
  trackEvent({
    action: 'form_start',
    form_name: formName,
  })
}

export const trackFormSubmit = (formName: string, success: boolean) => {
  trackEvent({
    action: 'form_submit',
    form_name: formName,
    success,
  })
}

// Error tracking
export const trackError = (errorMessage: string, errorLocation?: string) => {
  trackEvent({
    action: 'exception',
    description: errorMessage,
    fatal: false,
    error_location: errorLocation,
  })
}

// Custom event builder for flexibility
export const createCustomEvent = (eventName: string) => {
  return (params?: Record<string, unknown>) => {
    trackEvent({
      action: eventName,
      ...params,
    })
  }
}
```

## 第 6 步：Cookie 同意集成（如果使用了 `--consent` 参数）

创建一个支持用户同意管理的封装函数：

```typescript
// lib/analytics-consent.ts

type ConsentState = 'granted' | 'denied'

interface ConsentConfig {
  analytics_storage: ConsentState
  ad_storage: ConsentState
  ad_user_data: ConsentState
  ad_personalization: ConsentState
}

const CONSENT_COOKIE = 'analytics_consent'

// Initialize with consent mode
export const initWithConsent = (measurementId: string) => {
  if (typeof window === 'undefined') return

  // Set default consent state (denied until user consents)
  window.gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    wait_for_update: 500, // Wait for consent banner
  })

  // Load gtag
  const script = document.createElement('script')
  script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`
  script.async = true
  document.head.appendChild(script)

  window.dataLayer = window.dataLayer || []
  window.gtag = function gtag() {
    window.dataLayer.push(arguments)
  }
  window.gtag('js', new Date())
  window.gtag('config', measurementId)

  // Check for existing consent
  const savedConsent = getCookie(CONSENT_COOKIE)
  if (savedConsent) {
    updateConsent(JSON.parse(savedConsent))
  }
}

// Update consent when user makes a choice
export const updateConsent = (consent: Partial<ConsentConfig>) => {
  if (typeof window === 'undefined' || !window.gtag) return

  const consentState: ConsentConfig = {
    analytics_storage: consent.analytics_storage || 'denied',
    ad_storage: consent.ad_storage || 'denied',
    ad_user_data: consent.ad_user_data || 'denied',
    ad_personalization: consent.ad_personalization || 'denied',
  }

  window.gtag('consent', 'update', consentState)

  // Save to cookie
  setCookie(CONSENT_COOKIE, JSON.stringify(consentState), 365)
}

// Convenience functions
export const acceptAll = () => {
  updateConsent({
    analytics_storage: 'granted',
    ad_storage: 'granted',
    ad_user_data: 'granted',
    ad_personalization: 'granted',
  })
}

export const acceptAnalyticsOnly = () => {
  updateConsent({
    analytics_storage: 'granted',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
  })
}

export const denyAll = () => {
  updateConsent({
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
  })
}

// Cookie utilities
function setCookie(name: string, value: string, days: number) {
  const date = new Date()
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000)
  document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/;SameSite=Lax`
}

function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`))
  return match ? match[2] : null
}
```

## 第 7 步：调试模式（如果使用了 `--debug` 参数）

启用调试模式：

```typescript
// For development, enable debug mode
if (process.env.NODE_ENV === 'development') {
  window.gtag('config', 'G-XXXXXXXXXX', {
    debug_mode: true,
  })
}
```

建议安装 [Google Analytics Debugger](https://chrome.google.com/webstore/detail/google-analytics-debugger/jnkmfdileelhofjcijamephohjechhna) 扩展程序以辅助调试。

## 第 8 步：TypeScript 声明（如果使用了 TypeScript）

如果使用 TypeScript，请创建 `types/gtag.d.ts` 文件：

```typescript
// types/gtag.d.ts
declare global {
  interface Window {
    gtag: Gtag.Gtag
    dataLayer: object[]
  }
}

declare namespace Gtag {
  interface Gtag {
    (command: 'config', targetId: string, config?: ConfigParams): void
    (command: 'set', targetId: string, config: ConfigParams): void
    (command: 'set', config: ConfigParams): void
    (command: 'js', date: Date): void
    (command: 'event', eventName: string, eventParams?: EventParams): void
    (command: 'consent', consentArg: 'default' | 'update', consentParams: ConsentParams): void
    (...args: unknown[]): void
  }

  interface ConfigParams {
    page_title?: string
    page_location?: string
    page_path?: string
    send_page_view?: boolean
    debug_mode?: boolean
    [key: string]: unknown
  }

  interface EventParams {
    event_category?: string
    event_label?: string
    value?: number
    [key: string]: unknown
  }

  interface ConsentParams {
    analytics_storage?: 'granted' | 'denied'
    ad_storage?: 'granted' | 'denied'
    ad_user_data?: 'granted' | 'denied'
    ad_personalization?: 'granted' | 'denied'
    wait_for_update?: number
  }
}

export {}
```

## 第 9 步：验证步骤

配置完成后，请进行以下验证：
1. [ ] 测量 ID 的格式是否正确（以 `G-XXXXXXXXXX` 开头）
2. [ ] 脚本是否在生产环境中成功加载（检查浏览器的网络标签页）
3. [ ] GA4 仪表板中是否显示实时数据
4. [ ] 页面导航时是否能够被正确记录
5. [ ] 控制台中没有与 `gtag` 相关的错误
6. [ ] 环境变量是否未被提交到 Git 仓库
7. [ ] 如果使用了 TypeScript，确保没有类型错误

## 第 10 步：总结与输出

配置完成后，向用户提供以下信息：
1. **已创建/修改的文件**（列出所有文件）
2. **所需的环境变量**（附示例值）
3. **后续步骤**：
   - 将测量 ID 添加到环境变量中
   - 部署并在 GA4 仪表板中验证数据
   - 在 GA4 仪表板中设置转化跟踪
   - 考虑为关键用户操作添加自定义事件

## 常见问题及解决方法

**“gtag 未定义”**
- 可能是因为脚本尚未加载；请确保正确处理了异步加载

**GA4 中没有数据**
- 检查是否存在广告拦截器阻碍了数据跟踪
- 确认测量 ID 是否正确
- 查看浏览器控制台是否有错误信息

**页面浏览次数重复记录**
- 单页应用程序（SPA）的路由系统可能会发送重复的事件；请实现事件去重机制

**GDPR 合规性**
- 对欧盟用户必须启用同意管理功能
- 使用 `--consent` 参数来实现用户同意管理