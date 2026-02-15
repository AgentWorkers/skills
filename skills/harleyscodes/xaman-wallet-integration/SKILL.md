---
name: xaman-wallet
description: Integrate Xaman wallet (formerly Xumm) for XRP Ledger authentication and transactions. Use for: (1) Adding wallet connection to a webapp, (2) Implementing sign-in with Xaman, (3) Requesting payment/signatures from users, (4) Loading XummPkce SDK from CDN.
---

# Xaman 钱包集成

## 快速入门

1. **加载 SDK**（在 `layout.tsx` 或 HTML 的 `<head>` 部分）：
```html
<script src="https://xumm.app/assets/cdn/xumm-oauth2-pkce.min.js"></script>
```

2. **初始化并连接**：
```typescript
const XummPkce = (window as any).XummPkce;
const xumm = new XummPkce(API_KEY, {
  redirectUrl: window.location.origin + "/dashboard"
});

// Listen for auth events
xumm.on("success", async (state) => {
  const account = (await xumm.state())?.me?.account;
  console.log("Connected:", account);
});

// Start auth flow (opens popup)
await xumm.authorize();
```

## API 密钥

请从以下链接获取您的 API 密钥：https://xumm.app/dashboard/developer
环境变量：`NEXT_PUBLIC_XAMAN_API_KEY`

## 主要方法

- `new XummPkce(apiKey, options)` - 初始化 SDK
- `xumm.authorize()` - 启动 OAuth 流程，打开 Xaman 应用
- `xumm.state()` - 获取当前用户会话
- `xumm.logout()` - 清除会话
- `xumm.on("success", callback)` - 监听授权成功事件
- `xumm.on("error", callback)` - 监听错误事件

## 选项设置

```typescript
{
  redirectUrl: string,      // Where to redirect after auth
  rememberJwt: boolean,     // Persist session in localStorage (default: true)
  storage: Storage,        // Custom storage (default: localStorage)
  implicit: boolean        // Use implicit flow (default: false)
}
```

## 会话恢复

SDK 会自动恢复会话。在调用 `authorize()` 之前，请先调用 `xumm.logout()` 以强制重新登录。

## 常见问题解决方法

- **弹窗被阻止**：浏览器弹窗拦截器可能会阻止 `authorize()` 的执行——请确保用户手动允许弹窗。
- **账户信息未定义**：在授权成功后，使用 `xumm.state().then(s => s.me.account)` 来获取用户信息。
- **CORS 错误**：请确保 `redirectUrl` 与您的应用程序的域名匹配。