---
name: expo-appstore-deploy
description: 使用 EAS Build + Submit 将 Expo/React Native 应用程序部署到 Apple App Store 和 Google Play Store。该工具适用于构建 iOS/Android 的正式版本（production builds）、提交应用到应用商店、管理证书/配置文件（provisioning profiles），以及解决 EAS 构建过程中出现的故障。相关操作会在应用商店部署、EAS 构建、正式版本构建或提交到应用商店时触发。
---
# 在App Store中部署应用

完整的部署流程详情请参阅 `references/guide.md`。

## 快速命令

```bash
# iOS: first-time (interactive Apple login required)
npx eas-cli build --platform ios --profile production

# iOS: subsequent builds
npx eas-cli build --platform ios --profile production --non-interactive

# Android
npx eas-cli build --platform android --profile production --non-interactive

# Submit
npx eas-cli submit --platform ios --id <BUILD_ID>
npx eas-cli submit --platform android --id <BUILD_ID>

# Build + submit in one step
npx eas-cli build --platform ios --profile production --auto-submit
```

## 常见故障及解决方法

| 错误 | 解决方案 |
|-------|-----|
| 安装依赖项失败 | 从 `devDependencies` 中移除本地包 |
| 凭据未设置 | 首先以交互式方式运行构建过程（不要使用 `--non-interactive` 选项） |
| Apple 二次验证代码无效 | 使用短信验证码，切勿重复使用相同的验证码 |
| `ascAppId` 不能为空 | 在首次提交时移除该字段，之后再添加返回的 `ID` |
| 该构建已提交过 | 这不是错误——之前的提交已经成功 |

## 先决条件

1. 拥有有效的 Apple 开发者计划（Apple Developer Program）。
2. 完成 Google Play 控制台（Google Play Console）的注册及身份验证。
3. 已安装 `eas-cli`：运行 `npx eas-cli --version` 检查版本。
4. 在 `app.config.ts` 文件中配置了包含 `projectId` 的 `eas.json` 文件。

## 在App Store中提交应用的注意事项

- 对于人工智能（AI）应用，通常需要满足 12 岁或 17 岁以上的年龄评级要求。
- 如果应用使用了麦克风功能，必须明确说明麦克风的用途（`NSMicrophoneUsageDescription`）。
- 如果应用依赖于外部服务器，请确保能够正常处理离线情况。
- 如果应用支持多种社交登录方式，必须启用 Apple Sign In。
- 对于付费应用，必须提供“恢复购买”（Restore Purchases）功能。
- 在提交申请时，需要在审核备注中提供测试账户（Demo account）和服务器的 URL。
- 所有链接（包括隐私政策、支持页面和营销页面的链接）在提交前都必须返回 HTTP 200 状态码。