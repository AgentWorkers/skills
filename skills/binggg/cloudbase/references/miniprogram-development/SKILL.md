---
name: miniprogram-development
description: 微信小程序开发规则。在开发微信小程序、集成CloudBase功能以及部署小程序项目时，请使用此技能。
alwaysApply: false
---
## 何时使用此技能

当您需要进行以下操作时，可以使用此技能进行**微信小程序开发**：
- 开发微信小程序页面和组件
- 集成 CloudBase 功能（数据库、云函数、存储）
- 部署和预览小程序项目
- 处理小程序认证和用户身份验证
- 在小程序中调用 AI 模型
- 获取微信步数数据

**不建议用于以下场景**：
- Web 前端开发（请使用 web-development 技能）
- 后端服务开发（请使用 cloudrun-development 技能）
- 仅进行 UI 设计（请使用 ui-design 技能，但可以结合此技能使用）

---

## 如何使用此技能（对于编程代理）

1. **遵循项目结构规范**：
   - 小程序代码应放在 `miniprogram` 目录中
   - 云函数应放在 `cloudfunctions` 目录中
   - 使用最新的基础库版本
   - 在生成页面时，需要包含页面配置文件（例如 `index.json`）

2. **了解认证特性**：
   - **重要提示**：使用 CloudBase 的小程序默认无需登录
   - **严禁生成登录页面或登录流程**
   - 可以通过 `cloud.getWXContext().OPENID` 在云函数中获取用户身份

3. **正确使用微信开发者工具**：
   - 在打开项目之前，请检查 `project.config.json` 是否包含 `appid` 字段
   - 使用 CLI 命令打开包含 `project.config.json` 的目录

4. **妥善管理资源**：
   - **推荐使用 Icons8**：使用 Icons8 作为图标图像资源（例如，tabbar 的 `iconPath`）
     - 图标 URL 格式：`https://img'icon8.com/{style}/{size}/{color}/{icon-name}.png`
     - 参数：
       - `style`：`ios`（轮廓样式）或 `ios-filled`（实心样式）
       - `size`：建议使用 100px（文件大小应小于 5KB）
       - `color`：不带 # 的十六进制颜色代码（例如，`8E8E93` 表示灰色，`FF3B30` 表示红色）
       - `icon-name`：图标名称（例如，`checked--v1`）
     - 示例：
       - 未选中状态（灰色轮廓）：`https://img'icon8.com/ios/100/8E8E93/checked--v1.png`
       - 已选中状态（红色实心）：`https://img'icon8.com/ios-filled/100/FF3B30/checked--v1.png`
     - 优点：
       - 文件大小非常小（通常小于 3KB）
       - 支持自定义颜色
       - 图标设计简洁专业
   - 使用 `downloadRemoteFile` 工具下载资源
   - 确保所有引用的资源都存在，以避免构建错误

---

# 微信小程序开发规则

## 项目结构

1. **CloudBase 集成**：
   - 如果需要开发小程序，您将使用微信 CloudBase 的各种功能来构建项目
   - 小程序基础库应使用最新版本

2. **目录组织**：
   - 小程序项目应遵循微信 CloudBase 的最佳实践
   - 小程序代码通常放在 `miniprogram` 目录中
   - 如果需要开发云函数，可以将其存储在 `cloudfunctions` 目录中
   - 小程序的 `project.config.json` 需要指定 `miniprogramRoot` 及其他配置信息

3. **页面生成**：
   - 在生成小程序页面时，必须包含页面配置文件（如 `index.json`）
   - 必须遵守相关规范以避免编译错误

## 开发工具

**使用微信开发者工具打开项目的工作流程**：
- 当检测到当前项目为小程序项目时，建议用户使用微信开发者工具进行预览、调试和发布
- 在打开项目之前，请确认 `project.config.json` 中已配置 `appid` 字段。如果未配置，请让用户提供该信息
- 使用微信开发者工具内置的 CLI 命令打开项目（指向包含 `project.config.json` 的目录）：
  - Windows：`"C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat" open --project "项目根目录路径"`
  - macOS：`/Applications/wechatwebdevtools.app/Contents/MacOS/cli open --project "/path/to/project/root"`
- 项目根目录是指包含 `project.config.json` 文件的目录

## CloudBase 集成

1. **环境配置**：
   - 在小程序中使用 `wx.cloud` 时，需要指定环境 ID
   - 可以通过 `envQuery` 工具查询环境 ID

2. **资源管理**：
   - 在生成小程序代码时，如果需要素材图片（如 tabbar 的 `iconPath` 等），建议使用 Icons8（详见第 4 节）
   - 使用 `downloadRemoteFile` 工具下载资源
   - 在生成小程序代码时，如果使用了 `iconPath` 等资源，需帮助用户下载相应的图标文件以避免构建错误

## 小程序认证特性

**重要提示：使用 CloudBase 的小程序默认无需登录。严禁生成登录页面或登录流程！**

1. **无需登录**：使用 CloudBase 的小程序不需要用户登录，可以通过 wx-server-sdk 在云函数中获取用户身份
2. **用户身份获取**：在云函数中，可以通过 `cloud.getWXContext().OPENID` 获取用户的唯一标识符

3. **用户数据管理**：可以在云函数中根据 `OPENID` 管理用户数据，无需登录流程

```js
// Example of getting user identity in cloud function
exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  
  return { openid: openid };
};
```

## AI 模型调用

从基础库版本 3.7.1 开始，小程序已支持直接调用 AI 模型

```js
// Create model instance, here we use DeepSeek AI model
const model = wx.cloud.extend.AI.createModel("deepseek");

// First set AI's system prompt, here using seven-character quatrain generation as example
const p =
  "请严格按照七言绝句或七言律诗的格律要求创作，平仄需符合规则，押韵要和谐自然，韵脚字需在同一韵部。创作内容围绕用户给定的主题，七言绝句共四句，每句七个字；七言律诗共八句，每句七个字，颔联和颈联需对仗工整。同时，要融入生动的意象、丰富的情感与优美的意境，展现出古诗词的韵味与美感。";

// User's natural language input, e.g., '帮我写一首赞美玉龙雪山的诗'
const userInput = "帮我写一首赞美玉龙雪山的诗";

// Pass system prompt and user input to AI model
const res = await model.streamText({
  data: {
    model: "deepseek-v3", // Specify specific model
    messages: [
      { role: "system", content: p },
      { role: "user", content: userInput },
    ],
  },
});

// Receive AI model's response
// Since AI model's return result is streaming, we need to loop to receive complete response text
for await (let str of res.textStream) {
  console.log(str);
}
```

## 微信步数数据获取

**获取微信步数数据时，必须使用 CloudID 方法（基础库版本 2.7.0 及以上）**：
- **前端**：使用 `wx.getWeRunData()` 获取 CloudID，然后通过 `wx.cloud.CloudID(cloudID)` 将其传递给云函数
- **云函数**：直接使用 `weRunData.data` 获取解密的步数数据，并检查 `weRunData.errCode` 以处理错误
- **禁止使用手动解密 session_key 的方法**：CloudID 更安全且更简单
- **必须实现备用机制**：在 CloudID 获取失败时，需要提供模拟数据作为备用方案

## 云函数部署和权限注意事项

- 在 AI 模型自动部署后，云函数可能缺少某些权限（如云调用权限）
- 建议用户在微信开发者工具中右键点击云函数，选择“在云端安装依赖项”
- 对于需要云调用权限的功能（例如获取微信步数数据），建议用户通过开发者工具手动部署云函数以获取完整权限
- 如果遇到权限问题，请提示用户检查云函数的服务授权和 API 权限配置

## 开发工作流程指导

- 完成小程序项目开发后，主动建议用户使用微信开发者工具进行预览、调试和发布
- 如果用户同意，使用 CLI 命令打开包含 `project.config.json` 的项目根目录
- 提醒用户在微信开发者工具中进行真实设备的预览、调试和发布操作