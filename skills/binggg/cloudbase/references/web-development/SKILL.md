---
name: web-development
description: Web前端项目开发规则：在开发Web前端页面、部署静态托管服务以及集成CloudBase Web SDK时，请遵循以下规则。
alwaysApply: false
---
## 何时使用此技能

当您需要进行以下操作时，可以使用此技能进行**Web前端项目开发**：
- 开发Web前端页面和界面
- 将静态网站部署到CloudBase静态托管服务
- 集成CloudBase Web SDK以使用数据库、云函数和身份验证功能
- 设置现代前端构建系统（如Vite、Webpack等）
- 处理静态托管的路由和构建配置

**不适用场景**：
- 小程序开发（请使用**miniprogram-development**技能）
- 后端服务开发（请使用**cloudrun-development**技能）
- 仅涉及UI设计（请使用**ui-design**技能，但可以与该技能结合使用）

---

## 如何使用此技能（对于编码代理）

1. **遵循项目结构规范**：
   - 前端源代码应存储在`src`目录中
   - 构建后的输出文件应放在`dist`目录中
   - 云函数应放在`cloudfunctions`目录中
   - 使用现代前端构建系统（如Vite等）

2. **正确使用CloudBase Web SDK**：
   - 始终使用SDK内置的身份验证功能
   - 绝不在云函数中实现登录逻辑
   - 使用`envQuery`工具获取环境ID

3. **正确进行部署和预览**：
   - 先构建项目（确保执行了`npm install`命令）
   - 在`publicPath`配置中使用相对路径
   - 使用哈希路由以提高静态托管的兼容性
   - 如果用户未指定根目录，则将项目部署到子目录中

---

# Web前端开发规则

## 项目结构

1. **目录组织**：
   - 前端源代码应存储在`src`目录中
   - 构建后的输出文件应放在`dist`目录中
   - 云函数应放在`cloudfunctions`目录中

2. **构建系统**：
   - 项目应使用现代前端构建系统（如Vite）
   - 通过npm安装依赖项

3. **路由**：
   - 如果前端项目涉及路由，默认使用哈希路由
   - 哈希路由可以解决404错误和页面刷新问题，更适合静态网站托管

## 部署和预览

1. **静态托管部署**：
   - 对于前端项目，构建完成后可以使用CloudBase静态托管服务
   - 先进行本地预览，然后确认是否需要部署到CloudBase静态托管
   - 如果用户没有特殊要求，通常不要直接将项目部署到根目录
   - 以markdown链接格式返回部署后的地址

2. **本地预览**：
   - 要在本地预览静态网页，请导航到指定的输出目录并使用`npx live-server`命令

3. **公共路径配置**：
   - 当Web项目部署到静态托管CDN时，由于路径无法提前确定，`publicPath`等配置应使用相对路径而非绝对路径
   - 这可以解决资源加载问题

## CloudBase Web SDK的使用方法

1. **SDK集成**：
   - 如果项目需要数据库、云函数等功能，需要在Web应用程序中引入`@cloudbase/js-sdk@latest`

**重要提示：**身份验证必须使用SDK内置的功能。严禁使用云函数来实现登录逻辑！

```js
import cloudbase from "@cloudbase/js-sdk";

const app = cloudbase.init({
  env: "xxxx-yyy", // Can query environment ID via envQuery tool
});
const auth = app.auth();

// Check current login state
let loginState = await auth.getLoginState();

if (loginState && loginState.user) {
  // Logged in
  const user = await auth.getCurrentUser();
  console.log("Current user:", user);
} else {
  // Not logged in - use SDK built-in authentication features
    
  // Collect user's phone number into variable `phoneNum` by providing a input UI

  // Send SMS code
  const verificationInfo = await auth.getVerification({
    phone_number: `+86 ${phoneNum}`,
  });
  
  // Collect user's phone number into variable `verificationCode` by providing a input UI 
  
  // Sign in
  await auth.signInWithSms({
    verificationInfo,
    verificationCode,
    phoneNum,
  });
}
```

**初始化规则（Web，@cloudbase/js-sdk）**：
- 始终使用上述模式进行**同步初始化**
- **不要**使用`import("@cloudbase/js-sdk")`来懒加载SDK
- **不要**将SDK初始化代码包装在`initCloudBase()`等异步辅助函数中，并使用内部的`initPromise`缓存
- 在前端应用程序中保持一个共享的`app`/`auth`实例；重用该实例而不是重新初始化

### Web SDK API使用规则

- 仅使用**官方文档中记载的**CloudBase Web SDK方法
- 在调用`app`、`auth`、`db`或其他SDK对象的任何方法之前，请确认该方法在官方文档中存在
- 如果某个方法或选项在官方文档中没有提及（例如某些猜测的方法名称），**切勿自行发明或使用该方法**

## 身份验证最佳实践

1. **必须使用SDK内置的身份验证功能**：CloudBase Web SDK提供了完整的身份验证功能，包括短信登录、匿名登录、自定义登录等
2. **禁止使用云函数实现登录逻辑**：不要创建云函数来处理登录逻辑，这是错误的做法
3. **用户数据管理**：登录后，可以通过`authCurrentUser()`获取用户信息，并将其存储到数据库中
4. **错误处理**：所有身份验证操作都应包含完整的错误处理逻辑

## 构建流程

**Web项目构建流程**：确保首先执行`npm install`命令，然后参考项目文档进行构建