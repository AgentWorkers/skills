---
name: auth-web-cloudbase
description: >
  **CloudBase Web Authentication 快速指南**  
  本指南提供了简洁实用的 Web 前端认证解决方案，支持多种登录方式，并具备完善的用户管理功能。
alwaysApply: false
---
## 概述

**先决条件**：CloudBase 环境 ID (`env`)  
**先决条件**：CloudBase 环境区域 (`region`)  

---

## 核心功能

**使用场景**：使用 `@cloudbase/js-sdk@2.24.0+` 进行用户身份验证的 Web 前端项目  
**主要优势**：与 `supabase-js` API 兼容，支持手机、邮箱、匿名登录、用户名/密码以及第三方登录方式  
**`@cloudbase/js-sdk` 的 CDN 源代码**：`https://static.cloudbase.net/cloudbase-js-sdk/latest/cloudbase.full.js`  

## 先决条件

- 自动使用 `auth-tool-cloudbase` 来获取 `publishable key` 并配置登录方式。  
- 如果 `auth-tool-cloudbase` 失败，用户可以访问 `https://tcb.cloud.tencent.com/dev?envId={env}#/env/apikey` 获取 `publishable key`，并访问 `https://tcb.cloud.tencent.com/dev?envId={env}#/identity/login-manage` 来设置登录方式。  

## 快速入门

```javascript
// 使用 OTP 进行登录
const { data, error } = await auth signInWithOtp({ phone: '13800138000' });
const { data, error } = await data.verifyOtp({ token: '123456' };

// 使用邮箱进行登录
const { data, error } = await auth signInWithEmail({ email: 'user@example.com' });
const { data, error } = await data.verifyOtp({ token: '654321' });

// 使用密码进行登录
const { data, error } = await auth signInWithPassword({ username: 'test_user', password: 'pass123' });
const { data, error } = await auth signInWithPassword({ email: 'user@example.com', password: 'pass123' });
const { data, error } = await auth signInWithPassword({ phone: '13800138000', password: 'pass123' });

// 注册新账户（包含 OTP 验证）
const { data, error } = await auth.signUp({ email: 'new@example.com', nickname: 'User' });
const { data, error } = await data.verifyOtp({ token: '123456' });

// 匿名登录
const { data, error } = await auth/signInAnonymously();

// 使用 OAuth 进行登录
const { data, error } = await auth signInWithOAuth({ provider: 'google' });
window.location.href = data.url;

// 使用自定义票证进行登录
await auth signInWithCustomTicket(async () => {
  const res = await fetch('/api/ticket');
  return (await res.json()).ticket;
});

// 登录会话
const { data, error } = await auth.getSession();
const { data, error } = await auth.signUp({
  phone: '13800000000',
  anonymous_token: data.session.access_token,
});
await signUpData.verifyOtp({ token: '123456' });

// 登出
const { data, error } = await auth.signOut();

// 获取用户信息
const { data, error } = await auth.getUser();
console.log(data.user.email, data.user.phone, data.usermetadata?.nickName);

// 更新用户信息（除邮箱和电话号码外）
const { data, error } = await auth.updateUser({ nickname: 'New Name', gender: 'MALE', avatar_url: 'url' });

// 更新用户信息（邮箱或电话号码）
const { data, error } = await auth.updateUser({ email: 'new@example.com' });
const { data, error } = await data.verifyOtp({ email: "new@example.com", token: "123456" });

// 重置密码
const { data, error } = await auth.resetPasswordForOld({ old_password: 'old', new_password: 'new' });

// 重置密码（忘记密码）
const { data, error } = await auth.reauthenticate();
const { data, error } = await data.updateUser({ nonce: '123456', password: 'new' });

// 关联第三方身份
const { data, error } = await auth.linkIdentity({ provider: 'google' });

// 查看/解除关联身份
const { data, error } = await auth.getUserIdentities();
const { data, error } = await authunlinkIdentity({ provider: data.identities[0].id });

// 删除账户
const { data, error } = await auth.deleteMe({ password: 'current' });

// 监听状态变化
const { data, error } = auth.onAuthStateChange((event, session, info) => {
  // INITIAL_SESSION, SIGNED_IN, SIGNED_OUT, TOKEN_REFRESHED, USER_UPDATED, PASSWORD_RECOVERY, BIND_IDENTITY;
});

// 获取访问令牌
const { data, error } = await auth.getSession();
fetch('/api/protected', { headers: { Authorization: `Bearer ${data.session?.access_token}` });

// 刷新用户信息
const { data, error } = await auth.refreshUser();
```

---

## 数据结构定义

```typescript
// 用户数据结构
declare type User {
  id: any;
  aud: string;
  role: string[];
  email: any;
  email_confirmed_at: string;
  phone: any;
  phone_confirmed_at: string;
  confirmed_at: string;
  last_sign_in_at: string;
  app_metadata: {
    provider: any;
    providers: any[];
  };
  user_metadata: {
    name: any;
    picture: any;
    username: any;
    gender: any;
    locale: any;
    uid: any;
    nickName: any;
    avatarUrl: any;
    location: any;
    hasPassword: any;
  };
  identities: any;
  created_at: string;
  updated_at: string;
  is_anonymous: boolean;
}
```

---

## 示例代码

```javascript
// 手机登录页面
class PhoneLoginPage {
  async sendCode() {
    const phone = document.getElementById('phone').value;
    if (!/^1[3-9]\d{9}$/.test(phone)) {
      alert('无效的电话号码');
    }

    const { data, error } = await auth signInWithOtp({ phone });
    if (error) {
      alert('发送验证码失败: ' + error.message);
    }

    this.verifyFunction = data.verify;
    document.getElementById('codeSection').style.display = 'block';
    this.startCountdown(60);
  }

  async verifyCode() {
    const code = document.getElementById('code').value;
    if (!code) {
      alert('请输入验证码');
    }

    const { data, error } = await this.verifyFunction(code);
    if (error) {
      alert('验证码验证失败: ' + error.message);
    }

    console.log('登录成功:', data.user);
    window.location.href = '/dashboard';
  }

  startCountdown(seconds) {
    let countdown = seconds;
    const btn = document.getElementById('resendBtn');
    btn.disabled = true;

    const timer = setInterval(() => {
      countdown--;
      btn.innerText = `重新发送验证码（剩余 ${countdown} 秒）`;
      if (countdown <= 0) {
        clearInterval(timer);
        btn.disabled = false;
        btn.innerText = '重新发送';
      }
    }, 1000);
  }
}

// 使用 OpenID 进行登录
const { data, error } = await auth signInWithOpenId(); // 默认为微信云模式
const { data, error } = await auth signInWithOpenId({ useWxCloud: false }); // HTTP 模式

// 使用手机验证码进行登录
const { data, error } = await auth signInWithPhoneAuth({ phoneCode: 'xxx' });
```