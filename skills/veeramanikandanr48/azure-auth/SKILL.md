---
name: azure-auth
description: |
  Microsoft Entra ID (Azure AD) authentication for React SPAs with MSAL.js and Cloudflare Workers JWT validation using jose library. Full-stack pattern with Authorization Code Flow + PKCE. Prevents 8 documented errors.

  Use when: implementing Microsoft SSO, troubleshooting AADSTS50058 loops, AADSTS700084 refresh token errors, React Router redirects, setActiveAccount re-render issues, or validating Entra ID tokens in Workers.
user-invocable: true
---

# Azure Auth - 使用 Microsoft Entra ID 与 Cloudflare Workers 的集成

**依赖包版本**:
- @azure/msal-react@5.0.2
- @azure/msal-browser@5.0.2
- jose@6.1.3

**重要变更**:
- 从 MSAL v4 迁移至 v5（2026年1月）
- Azure AD B2C 服务将于2025年5月停止新用户注册（现有用户可继续使用至2030年）
- ADAL（Azure Active Directory Authentication Library）将于2025年9月完全停止支持

**最后更新时间**: 2026-01-21

---

## 架构概述

**关键限制**:
- MSAL.js 无法在 Cloudflare Workers 中使用（因为它依赖于浏览器或 Node.js 的 API），请使用 jose 库进行后端令牌验证。

---

## 快速入门

### 1. 安装依赖包

### 2. 在 Azure 门户中设置应用程序注册信息
1. 访问 **Microsoft Entra ID** → **应用注册** → **新建注册**
2. 将 **重定向 URI** 设置为 `http://localhost:5173`（单页应用程序类型）
3. 记下 **应用程序（客户端）ID** 和 **租户 ID**
4. 在 **身份验证** 部分：
   - 启用 **访问令牌** 和 **ID 令牌**
   - 添加生产环境的重定向 URI
5. 在 **API 权限** 部分：
   - 添加 `User.Read` 权限（用于访问 Microsoft Graph）
   - 如有需要，请求管理员同意

---

## 前端：使用 MSAL React 的设置

### 配置（src/auth/msal-config.ts）

### 设置 MsalProvider（src/main.tsx）

### 保护路由组件

### 获取令牌以进行 API 调用

---

## 后端：在 Cloudflare Workers 中验证 JWT 令牌

### 为什么使用 jose 而不是 MSAL？
MSAL.js 需要浏览器 API（如 `localStorage`、`sessionStorage`）和 Node.js 的加密模块，但这些在 Cloudflare Workers 的 V8 隔离运行环境中不可用。jose 库是纯 JavaScript 实现的，因此可以在 Cloudflare Workers 中正常使用。

### JWT 令牌验证（src/auth/validate-token.ts）

### 使用中间件模式处理请求

---

## 常见问题及解决方法

### 1. AADSTS50058 - 静默登录循环
**错误**：发送了静默登录请求，但没有任何用户登录。
**原因**：在缓存中不存在用户信息时调用了 `acquireTokenSilent` 函数。
**解决方法**:

### 2. AADSTS700084 - 刷新令牌过期
**错误**：刷新令牌是针对单页应用程序（SPA）颁发的，因此有效期固定为 1 小时。
**原因**：SPA 的刷新令牌在 24 小时后失效，无法延长有效期。
**解决方法**:

### 3. React Router v6 导致无限重定向
**错误**：登录页面和应用程序之间出现无限重定向。
**原因**：React Router v6 可能会删除包含身份验证响应的哈希片段。
**解决方法**：使用自定义的 NavigationClient：

### 4. NextJS 动态路由问题
**错误**：在动态路由中出现 `no_cached_authority_error`。
**原因**：在组件渲染之前 MSAL 实例未正确初始化。
**解决方法**：在 `_app.tsx` 中在设置路由之前初始化 MSAL：

### 5. Safari/Edge 浏览器中的 Cookie 问题
**错误**：在 Safari 或 Edge 浏览器中，身份验证状态丢失，导致无限循环。特别是在 iOS 18 上，即使启用了第三方 Cookie，使用 AADSTS50058 时也会出现此问题。
**来源**：[GitHub 问题 #7384](https://github.com/AzureAD/microsoft-authentication-library-for-js/issues/7384)
**原因**：这些浏览器对 Cookie 的存储有更严格的规定，导致无法存储必要的登录相关 Cookie。
**测试说明**：在 iOS 18 上的 Chrome 浏览器中可以正常工作，但在 Safari 上会出问题。
**解决方法**：在 MSAL 配置中启用 Cookie 存储：

### 6. 无法找到 JWKS URL（在 Cloudflare Workers 中）
**错误**：无法从 `.well-known/jwks.json` 文件中获取 JWKS 令牌。
**原因**：Azure AD 没有在标准的 OpenID Connect 路径提供 JWKS 文件。
**解决方法**：先获取 `openid-configuration`，然后再使用 `jwks_uri`：

### 7. React Router 加载器状态冲突
**错误**：在 React Router 加载器中使用 `acquireTokenSilent` 时，会出现状态更新警告。
**来源**：[GitHub 问题 #7068](https://github.com/AzureAD/microsoft-authentication-library-for-js/issues/7068)
**原因**：在路由加载器和 `MsalProvider` 中使用了相同的 `PublicClientApplication` 实例，导致状态更新。
**解决方法**：在加载器中再次调用 `initialize()` 函数：

### 8. 使用 `setActiveAccount()` 后组件不重新渲染
**问题**：使用 `useMsal()` 的组件在调用 `setActiveAccount()` 后不会更新。
**来源**：[GitHub 问题 #6989](https://github.com/AzureAD/microsoft-authentication-library-for-js/issues/6989)
**验证情况**：多个用户确认了这个问题。
**解决方法**：强制更新组件状态：

---

## 多租户与单租户配置

### 单租户（推荐用于企业环境）
- 只有来自您组织的用户才能登录
- 令牌颁发地址：`https://login.microsoftonline.com/{tenant_id}/v2.0`

### 多租户环境
- 任何 Azure AD 租户的用户都可以登录
- 令牌颁发地址取决于用户所属的租户
- **后端需要处理多个令牌颁发者**：

---

## 环境变量配置

### 前端（.env 文件）

### 后端（wrangler.jsonc 文件）

---

## Azure AD B2C 服务终止

**时间线**：
- **2025年5月1日**：Azure AD B2C 服务不再支持新用户注册
- **2026年3月15日**：所有客户将无法使用 Azure AD B2C 的 P2 版本
- **2030年5月**：微软将继续为现有 B2C 客户提供标准支持

**来源**：[Microsoft 官方问答](https://learn.microsoft.com/en-us/answers/questions/2119363/migrating-existing-azure-ad-b2c-to-microsoft-entra)

**现有 B2C 客户**：可以继续使用 B2C 服务至2030年，但建议迁移到 Microsoft Entra External ID。
**新项目**：建议使用 **Microsoft Entra External ID** 作为用户身份验证方式。

**迁移状态**：
- 自2026年1月起，自动化迁移工具正处于测试阶段。微软 Learn 上提供了手动迁移指南。
**迁移步骤**：
- 更改授权 URL 格式（从 `{tenant}.b2clogin.com` 更改为 `{tenant}.ciamlogin.com`）
- 更新 SDK 支持（使用相同的 MSAL 库）
- 新的定价模式（基于使用量计费）
- 提供自助密码重置（SSPR）功能以帮助用户迁移
- GitHub 上有迁移示例（预览版）
更多信息请访问：https://learn.microsoft.com/en-us/entra/external-id/
迁移指南：https://learn.microsoft.com/en-us/entra/external-id/customers/how-to-migrate-users

---

## ADAL 的完全停止支持
**状态**：Azure AD Authentication Library（ADAL）已于2025年9月30日停止支持。使用 ADAL 的应用程序将不再接收安全更新。
**如果您正在从 ADAL 迁移**：
1. 必须将 ADAL 迁移到 MSAL
2. ADAL 使用的是 v1.0 的 API 端点，而 MSAL 使用的是 v2.0 的 API 端点
3. 令牌缓存格式不同，用户需要重新认证
**关键迁移事项**：
更多信息请查看：https://learn.microsoft.com/en-us/entra/msal/javascript/migration/msal-net-migration

---

## 参考资源
- [MSAL React 文档](https://learn.microsoft.com/en-us/entra/msal/javascript/react/)
- [Microsoft Entra ID 应用注册指南](https://learn.microsoft.com/en-us/identity-platform/quickstart-register-app)
- [MSAL.js 的 GitHub 问题列表](https://github.com/AzureAD/microsoft-authentication-library-for-js/issues)
- [jose 库](https://github.com/panva/jose)
- [Cloudflare Workers 与 Azure AD 的集成教程](https://hajekj.net/2021/11/12/cloudflare-workers-and-azure-ad/)