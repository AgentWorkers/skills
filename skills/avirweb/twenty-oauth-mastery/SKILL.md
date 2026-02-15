# Twenty CRM OAuth 精通技能

**作者**：基于在 OpenCode 中进行的广泛 OAuth 调试会话生成  
**最后更新**：2026-02-08  
**版本**：1.0  

---

## 技能元数据  

```yaml
name: twenty-oauth-mastery
description: Expert-level OAuth authentication knowledge for Twenty CRM including implementation, troubleshooting, and best practices
expertise_level: Expert/Mastery
category: Authentication
applicable_to:
  - Twenty CRM authentication
  - Google/Microsoft OAuth
  - Token refresh management
  - Domain restrictions
  - Email/Calendar sync integration
prerequisites:
  - Knowledge of TypeScript/JavaScript
  - Understanding of OAuth 2.0 protocol
  - Familiarity with NestJS framework
keywords:
  - oauth
  - authentication
  - twenty-crm
  - google-oauth
  - microsoft-oauth
  - token-refresh
  - sync-integration
  - domain-restriction
```  

---

## 快速入门  

### 何时使用此技能  

在以下情况下应使用此技能：  
✅ **实现**新的 OAuth 提供者  
✅ **修复** OAuth 登录问题  
✅ **设置** OAuth 后的自动 Gmail/日历同步  
✅ **调试** 令牌刷新失败  
✅ **配置** 域名限制  
✅ **排查** 重定向循环问题  

### 常见问题的快速参考  

| 问题 | 需检查的文件 | 快速解决方法 |  
|-------|---------------|-----------|  
| 重定向循环 | `auth.service.ts` | 重新构建：`npx nx build twenty-server` |  
| .co 域名被阻止 | `google-auth.controller.ts` | 添加到允许列表：`['company.com', 'company.co']` |  
| 同步未启动 | `google.auth.strategy.ts` | 在 `validate()` 方法中返回令牌 |  
| Cookie 无法读取 | 控制器 Cookie 设置 | 将 `httpOnly` 设置为 `false` |  
| 无限循环 | `SignInUpGlobalScopeFormEffect.tsx` | 跟踪已处理的令牌签名 |  

---

## 核心知识  

### 1. Twenty CRM OAuth 架构  

**关键文件**：`twenty/packages/twenty-server/src/engine/core-modules/auth/`  

**结构**：  
```
auth/
├── strategies/         # Passport strategies (Google, Microsoft)
├── controllers/        # OAuth endpoints and callbacks
├── services/          # Auth logic, sync setup, token management
├── guards/            # Auth guards and validation
└── utils/             # Scope configuration, utilities
```  

---

### 2. 关键代码模式  

#### Passport 策略模式（必须遵循）  

```typescript
@Injectable()
export class GoogleStrategy extends PassportStrategy(Strategy, 'google') {
  constructor(twentyConfigService: TwentyConfigService) {
    super({
      clientID: twentyConfigService.get('AUTH_GOOGLE_CLIENT_ID'),
      clientSecret: twentyConfigService.get('AUTH_GOOGLE_CLIENT_SECRET'),
      callbackURL: twentyConfigService.get('AUTH_GOOGLE_CALLBACK_URL'),
      scope: getGoogleApisOauthScopes(),
      passReqToCallback: true, // 🔴 CRITICAL: Required for request state
    });
  }

  async validate(
    request: GoogleRequest,
    _accessToken: string,
    _refreshToken: string,
    profile: GoogleProfile,
  ) {
    // 🔴 CRITICAL: Include tokens in return object
    // Without this, automatic sync setup fails
    return {
      ...profile,
      accessToken: _accessToken,
      refreshToken: _refreshToken,
      hostedDomain: request.query.hosted_domain || profile.emails?.[0]?.value?.split('@')[1],
    };
  }
}
```  

**为什么这很重要**：  
- `passReqToCallback: true`：允许访问请求状态  
- 令牌保存：对于 OAuthSyncService 的正常运行是必需的  

---

### 3. 常见问题及解决方案  

#### 问题 1：OAuth 后出现重定向循环  

**症状**：OAuth 完成后用户仍停留在欢迎页面  

**根本原因**：  
1. **后端未编译**：源代码有修复，但容器运行的是旧版本的 JavaScript  

**解决方法**：  
```bash
   npx nx build twenty-server
   docker restart fratres-twenty
   ```  

2. **缺少 `isSingleDomainMode`：重定向逻辑未包含在编译后的代码中  

**检查**：  
```bash
   docker exec fratres-twenty cat /app/dist/engine/core-modules/auth/services/auth.service.js | grep isSingleDomainMode
   ```  

3. **Cookie 域名不匹配**：Cookie 无法访问  

**解决方法**：  
```typescript
   // auth.service.ts - Remove explicit domain attribute
   res.cookie('tokenPair', JSON.stringify(authTokens), {
     path: '/',
     secure: true,
     sameSite: 'lax',
     httpOnly: false, // 🔴 Must be false for JavaScript access
   });
   ```  

---

#### 问题 2：.co 域名的用户被拒绝登录  

**症状**：仅允许访问 `.com` 域名的用户  

**三个可能的解决方法**：  
1. **Google 策略**（`google.auth.strategy.ts`）：  
```typescript
   // ❌ WRONG - Hardcoded
   hd: 'company.com'
   
   // ✅ CORRECT - Remove hd parameter
   // (no hd parameter)
   ```  

2. **控制器**（`google-auth.controller.ts`）：  
```typescript
   // ❌ WRONG - Hardcoded check
   if (hostedDomain !== 'company.com') { throw ... }
   
   // ✅ CORRECT - Allowlist
   const allowedOAuthDomains = ['company.com', 'company.co'];
   if (!hostedDomain || !allowedOAuthDomains.includes(hostedDomain)) {
     throw new UnauthorizedException(
       `Only ${allowedOAuthDomains.map(d => `@${d}`).join(', ')} allowed`
     );
   }
   ```  

3. **数据库**（`workspaceMetadata` 表）：  
```sql
   INSERT INTO "workspaceMetadata" ("id", "workspaceId", "key", "value", "createdAt", "updatedAt")
   VALUES (gen_random_uuid(), 'workspace-id', 'approvedAccessDomains', '["company.com", "company.co"]', NOW(), NOW());
   ```  

---

#### 问题 3：自动同步未触发  

**症状**：用户登录后，关联的账户或同步渠道未创建  

**根本原因**：`validate()` 方法中丢失了令牌  

**解决方法**：  
```typescript
// google.auth.strategy.ts validate()
async validate(request, accessToken, refreshToken, profile) {
  // ❌ WRONG - Tokens lost
  return { ...profile };
  
  // ✅ CORRECT - Tokens preserved
  return {
    ...profile,
    accessToken,
    refreshToken,
  };
}
```  

**其他检查**：  
1. 确认 `auth.service.ts` 在登录后调用了 `oauthSyncService.setupSyncForOAuthUser()`  
2. 确认令牌已传递给同步服务  
3. 确认 Google 的权限范围包含 `gmail.readonly` 和 `calendar.events`  
4. 确认 `CALENDAR_PROVIDER_GOOGLE_ENABLED` 为 `true`  

---

#### 问题 4：前端令牌处理循环  

**症状`：`SignInUpGlobalScopeFormEffect` 不停运行，导致 API 调用无限次  

**根本原因**：同一个令牌被多次处理  

**解决方法**：  
```typescript
// SignInUpGlobalScopeFormEffect.tsx
useEffect(() => {
  const tokenPairFromUrl = getAuthPairFromUrl();
  
  if (tokenPairFromUrl) {
    const tokenSignature = JSON.stringify(tokenPairFromUrl);
    
    // 🔴 CRITICAL: Skip if already processed
    if (processedTokenSignatures.current.has(tokenSignature)) {
      return;
    }
    
    // Track this signature
    processedTokenSignatures.current.add(tokenSignature);
    
    // Now process the token
    setAuthTokens(tokenPairFromUrl);
  }
}, []);
```  

---

### 4. OAuth 同步集成  

**使用场景**：用户应在 OAuth 登录后自动连接到 Gmail/日历  

**实现步骤**：  
1. **创建 OAuthSyncService**：  
```typescript
   async setupSyncForOAuthUser(input: {
     workspaceId: string;
     userId: string;
     workspaceMemberId: string;
     email: string;
     accessToken: string;
     refreshToken: string;
     scopes: string[];
   }) {
     // 1. Create/update connected account with tokens
     // 2. Create message channel
     // 3. Create calendar channel (if enabled)
     // 4. Queue initial sync jobs
   }
   ```  
2. **集成到 AuthService**：  
```typescript
   // auth.service.ts:signInUpWithSocialSSO()
   const { redirectUrl, authTokens } = await this.generateTokens(...);
   
   // 🔴 CRITICAL: Call sync setup BEFORE redirect
   if (provider === 'google') {
     try {
       await this.oauthSyncService.setupSyncForOAuthUser({
         workspaceId,
         userId,
         email: user.email,
         accessToken: authTokens.authToken.accessToken,
         refreshToken: authTokens.authToken.refreshToken,
         scopes: user.scopes || [],
       });
     } catch (error) {
       // Log error but don't fail login
       this.logger.error('Failed to setup OAuth sync', error);
     }
   }
   
   return { redirectUrl, authTokens };
   ```  

**注意事项**：  
- 使用 `try/catch` 防止同步设置过程中登录失败  
- 检查是否存在重复的同步渠道  
- 仅在需要时为特定提供者/域名运行同步  

---

### 5. 令牌刷新管理  

**令牌刷新模式**：  
```typescript
async refreshTokens(refreshToken: string): Promise<ConnectedAccountTokens> {
  const oAuth2Client = new google.auth.OAuth2(clientId, clientSecret);
  oAuth2Client.setCredentials({ refresh_token: refreshToken });
  
  try {
    const { token } = await oAuth2Client.getAccessToken();
    
    // 🔴 CRITICAL: Preserve original refresh token
    // Google may not return a new one
    return {
      accessToken: token,
      refreshToken: refreshToken,
    };
  } catch (error) {
    throw parseGoogleOAuthError(error);
  }
}
```  

**错误处理**：  
```typescript
export const parseGoogleOAuthError = (error: unknown) => {
  const gaxiosError = error as GaxiosError;
  const code = gaxiosError.response?.status;
  const reason = gaxiosError.response?.data?.error;
  
  switch (code) {
    case 400:
      if (reason === 'invalid_grant') {
        // 🔴 FATAL: Refresh token expired/revoked
        return new ConnectedAccountRefreshAccessTokenException(
          'invalid_grant',
          ConnectedAccountRefreshAccessTokenExceptionCode.INVALID_REFRESH_TOKEN,
        );
      }
      break;
    case 401:
      return new ConnectedAccountRefreshAccessTokenException(
        'unauthorized',
        ConnectedAccountRefreshAccessTokenExceptionCode.UNAUTHORIZED,
      );
    case 429:
      // 🔴 RETRYABLE: Rate limit error
      return new ConnectedAccountRefreshAccessTokenException(
        'rate_limit',
        ConnectedAccountRefreshAccessTokenExceptionCode.RATE_LIMIT_ERROR,
      );
  }
  
  return new ConnectedAccountRefreshAccessTokenException('unknown', ...);
};
```  

---

### 6. 测试策略  

#### 单元测试（令牌刷新）  
```typescript
describe('GoogleAPIRefreshAccessTokenService', () => {
  it('should refresh token successfully', async () => {
    const mockRefreshToken = 'valid-refresh-token';
    const mockNewAccessToken = 'new-access-token';
    
    jest.spyOn(google.auth, 'OAuth2').mockImplementation(() => ({
      setCredentials: jest.fn(),
      getAccessToken: jest.fn().mockResolvedValue({ token: mockNewAccessToken }),
    }));
    
    const result = await service.refreshTokens(mockRefreshToken);
    
    expect(result.accessToken).toBe(mockNewAccessToken);
    expect(result.refreshToken).toBe(mockRefreshToken); // Original preserved
  });
});
```  

#### Cookie 注入测试（Playwright）  
```typescript
// Test: frontend reads and processes cookie
await context.addCookies([{
  name: 'tokenPair',
  value: JSON.stringify({ authToken: { accessToken: 'fake-token' } }),
  domain: 'isearch.1791technology.com',
  path: '/',
  secure: true,
  sameSite: 'Lax',
}]);

await page.goto('https://isearch.1791technology.com');

// Check console logs
const logs = await page.evaluate(() => window.tokenPairLogs || []);
assert(logs.includes('tokenPairPayload from cookies: found'));
assert(logs.includes('Setting auth tokens...'));
```  

---

### 7. 配置  

**所需的环境变量**：  
```bash
# Google OAuth
AUTH_GOOGLE_ENABLED=true
AUTH_GOOGLE_CLIENT_ID=849758856044-54v9md2rt6ucthch26p8g4etotcb8gth.apps.googleusercontent.com
AUTH_GOOGLE_CLIENT_SECRET=GOCSPX-...
AUTH_GOOGLE_CALLBACK_URL=https://yourdomain.com/auth/google/redirect

# Calendars/Email
CALENDAR_PROVIDER_GOOGLE_ENABLED=true
MESSAGING_PROVIDER_GMAIL_ENABLED=true

# Billing (disable for self-hosted)
IS_BILLING_ENABLED=false
```  

**Google Cloud 控制台**：  
- 重定向 URI：`https://yourdomain.com/auth/google/redirect`  
- 授权来源：`https://yourdomain.com`  

---

### 8. 部署检查清单  

**部署前**：  
- [ ] TypeScript 源代码已更新  
- [ ] 单元测试通过  
- [ ] 使用 `npx nx typecheck twenty-server` 进行类型检查  
- [ ] 使用 `npx nx build twenty-server` 进行构建  
- [ ] 确认编译后的 JavaScript 有更改（检查 `dist/` 文件夹）  
- [ ] 将 `dist/` 文件夹复制到容器中  
- [ ] 重启容器  
- [ ] 检查健康状态：`curl -f /healthz`  

**部署后**：  
- [ ] 手动测试 OAuth 流程  
- [ ] 检查浏览器控制台  
- [ ] 确认重定向到仪表板  
- [ ] 检查数据库中是否有关联的账户  
- [ ] 确认是否创建了同步渠道（如适用）  

---

### 9. 故障排除工作流程  

**步骤 1：确认容器正在运行新代码**  
```bash
docker ps | grep fratres-twenty
docker exec fratres-twenty cat /app/dist/engine/core-modules/auth/services/auth.service.js | grep isSingleDomainMode
```  

**步骤 2：检查 Google Cloud 控制台**  
- 重定向 URI 是否与生产环境匹配  
- 客户端 ID 和密钥是否正确  
- OAuth 同意屏幕是否配置正确  

**步骤 3：检查环境**  
```bash
docker exec fratres-twenty env | grep AUTH_GOOGLE
docker exec fratres-twenty env | grep CALENDAR_PROVIDER
```  

**步骤 4：测试 OAuth 入口点**  
```bash
curl -v https://yourdomain.com/auth/google | grep Location
# Should redirect to accounts.google.com with correct client_id
```  

**步骤 5：检查数据库（同步问题）**  
```sql
-- Check connected accounts
SELECT id, handle, provider, "accessToken" IS NOT NULL
FROM "connectedAccount"
WHERE handle = 'user@example.com';

-- Check sync channels
SELECT id, "syncStatus"
FROM "messageChannel"
WHERE "connectedAccountId" = 'account-id';
```  

**步骤 6：检查日志**  
```bash
docker logs fratres-twenty --tail 100 | grep -i oauth
```  

---

### 10. 常见陷阱 ❌**  
1. **忘记重新构建**：源代码更改不会自动编译  
2. **硬编码域名**：使用允许列表代替  
3. **将 `httpOnly` 设置为 `true`：前端无法读取 `tokenPair` Cookie  
4. **在 `validate()` 方法中丢失令牌**：必须返回 `accessToken`/`refreshToken`  
5. **未保存刷新令牌**：Google 可能不会返回新的令牌  
6. **未设置 `passReqToCallback: true`：无法访问请求状态  
7. **未使用真实的 OAuth 进行测试**：模拟测试会遗漏边缘情况  
8. **跳过健康检查**：容器可能仍在运行旧代码  

---

## 专家见解  

### 当 OAuth 可用但同步失败时  

**调试步骤**：  
1. 检查 `oauth-sync.service.ts` 是否存在并已被调用  
2. 确认令牌已通过 `validate()` 方法  
3. 确认权限范围包含 `gmail.readonly` 和 `calendar.events`  
4. 确认 `CALENDAR_PROVIDER_GOOGLE_ENABLED` 为 `true`  
5. 检查数据库中是否有关联的账户  

**常见解决方法**：在 `validate()` 方法中返回令牌  

---

### 当 .co 域名的用户无法登录时  

**调试步骤**：  
1. 检查 `google.auth_strategy.ts` 中是否硬编码了 `hd` 参数  
2. 检查 `google-auth.controller.ts` 中的域名验证逻辑  
3. 检查 `auth.service.ts` 中的域名允许列表  
4. 检查数据库中的 `workspaceMetadata.approvedAccessDomains`  

**常见解决方法**：  
- 删除硬编码的 `hd` 参数  
- 更新控制器/服务的允许列表  
- 将域名添加到数据库中  

---

### 当前端停留在欢迎页面时  

**调试步骤**：  
1. 检查 `auth.service.ts` 中的 `isSingleDomainMode` 逻辑  
2. 检查编译后的 `auth.service.js` 是否包含相关逻辑  
3. 检查 `computeRedirectURI` 是否返回 `AppPath.Index`  
4. 检查 Cookie 的 `httpOnly` 属性  

**常见解决方法**：  
- 重新构建后端：`npx nx build twenty-server`  
- 确保重定向到仪表板：`AppPath.Index`  
- 将 Cookie 的 `httpOnly` 属性设置为 `false`  

---

## 快速命令  

```bash
# Build backend
npx nx build twenty-server

# Build frontend
npx nx build twenty-front

# Typecheck
npx nx typecheck twenty-server

# Restart container
docker restart fratres-twenty

# Check logs
docker logs fratres-twenty --tail 100

# Health check
curl -f https://yourdomain.com/healthz

# Test OAuth redirect
curl -v https://yourdomain.com/auth/google
```  

---

## 总结  

本技能提供了关于 Twenty CRM 的高级 OAuth 知识，涵盖：  
1. **架构**：使用 Passport 策略的 OAuth 架构  
2. **常见问题**：5 大问题及详细的解决方法  
3. **自动同步**：OAuth 后的 Gmail/日历同步  
4. **令牌管理**：令牌刷新模式和错误处理  
5. **测试**：单元测试和集成测试方法  
6. **配置**：所需的环境变量  
7. **部署**：详细的部署步骤  
8. **故障排除**：系统的故障排除流程  

**在以下情况下使用此技能**：  
- 实现新的 OAuth 提供者  
- 修复 OAuth 登录问题  
- 设置自动同步集成  
- 调试令牌刷新失败  
- 配置域名限制  
- 排查重定向循环问题