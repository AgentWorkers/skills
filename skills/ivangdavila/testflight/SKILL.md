---
name: TestFlight
slug: testflight
version: 1.0.0
homepage: https://clawic.com/skills/testflight
description: 使用 TestFlight 分发 iOS 和 macOS 的测试版本（beta builds），同时实现测试人员管理（tester management）以及持续集成/持续部署（CI/CD）自动化流程。
metadata: {"clawdbot":{"emoji":"🛫","requires":{"bins":[]},"os":["darwin"]}}
---
## 使用场景

用户需要通过 TestFlight 分发测试版本（beta builds）。Agent 负责处理 App Store Connect 的配置、测试者组的设置、构建文件的上传以及与持续集成/持续交付（CI/CD）系统的集成。

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| CI/CD 自动化 | `ci-cd.md` |

## 核心规则

### 1. 先配置 App Store Connect
在上传之前，请确保：
- 在开发者门户（Developer Portal）中注册了 Bundle ID。
- 在 App Store Connect 中创建了应用程序。
- 配置了应用程序专用的密码或 API 密钥。

### 2. 构建要求
每个 TestFlight 构建都需要满足以下条件：
- 具有唯一的构建编号（CFBundleVersion）——必须逐次递增。
- 拥有有效的配给配置文件（用于在 App Store 中分发应用程序）。
- 所有合规性声明都完整无误。

### 3. 测试者组策略

| 组别 | 用途 | 限制 |
|-------|---------|-------|
| 内部测试者 | 具有 App Store Connect 访问权限的团队成员 | 最多 100 人 |
| 外部测试者 | 需要 Apple 审核的测试者 | 最多 10,000 人 |

内部构建可以立即使用；外部测试者的构建需要经过 Apple 的审核（首次提交时通常需要 24–48 小时）。

### 4. 上传方法

| 方法 | 适用场景 |
|--------|----------|
| Xcode | 手动上传，适用于单次构建 |
| `xcrun altool` | 适用于脚本自动化，无需 Fastlane |
| Fastlane | 完全自动化的构建流程，适用于多个应用程序 |
| Xcode Cloud | Apple 自带的持续集成/持续交付解决方案 |
| Transporter | 适用于非开发人员的图形化工具 |

### 5. 构建有效期
TestFlight 构建在 90 天后失效。请据此规划应用程序的发布时间。

## 常见问题及解决方法

- **构建编号未递增**：构建会被立即拒绝，需要重新生成并重新上传。
- **缺少合规性声明**：构建会停留在“处理中”状态，直到在 App Store Connect 中完成相关设置。
- **首次使用外部测试者**：需要先进行完整的测试审核，建议先使用内部测试者。
- **配给配置文件过期**：上传会失败，请在归档前检查配置文件的有效性。
- **在 CI 环境中使用应用程序专用密码**：建议使用 App Store Connect 的 API 密钥（更安全，且无需二次身份验证）。

## CI/CD 快速设置

### 推荐使用 App Store Connect API 密钥

1. 进入 App Store Connect > 用户（Users）> 密钥（Keys）> App Store Connect API。
2. 以“App Manager”角色生成 API 密钥。
3. 下载生成的 `.p8` 文件（仅生成一次）。
4. 请记录发行者 ID（Issuer ID）和密钥 ID。

### 使用 Fastlane 进行上传

```bash
# In Fastfile
lane :beta do
  build_app(scheme: "MyApp")
  upload_to_testflight(
    api_key_path: "fastlane/api_key.json",
    skip_waiting_for_build_processing: true
  )
end
```

### 使用 `xcrun altool`（无需 Fastlane）

```bash
xcrun altool --upload-app \
  --type ios \
  --file "MyApp.ipa" \
  --apiKey "KEY_ID" \
  --apiIssuer "ISSUER_ID"
```

## 安全性与隐私

**会传输到 Apple 服务器的数据：**
- IPA 文件或应用程序二进制文件。
- 构建元数据（版本号、Bundle ID、团队信息）。

**保留在本地的数据：**
- API 密钥和证书（存储在 Keychain 中）。
- 源代码（不会被上传）。

**本技能注意事项：**
- 不会以明文形式存储 Apple 的认证信息。
- 不会将构建文件共享到 Apple 之外的系统。

## 相关技能
如果用户需要，可以使用以下命令进行安装：
- `clawhub install <slug>`：用于安装相关工具。
- `ios`：iOS 开发相关技能。
- `xcode`：Xcode 开发工作流程相关技能。
- `flutter`：跨平台应用程序开发相关技能。

## 反馈建议
- 如果本文档对您有帮助，请给它点赞（star）：`clawhub star testflight`。
- 为了获取最新信息，请定期同步：`clawhub sync`。