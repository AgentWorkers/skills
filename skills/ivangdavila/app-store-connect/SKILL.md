---
name: App Store Connect
slug: app-store-connect
version: 1.0.0
homepage: https://clawic.com/skills/app-store-connect
description: 通过 App Store Connect API 管理 iOS 应用程序、TestFlight 构建版本、提交过程以及相关分析数据。
metadata: {"clawdbot":{"emoji":"🍎","requires":{"bins":[],"env":["ASC_ISSUER_ID","ASC_KEY_ID","ASC_PRIVATE_KEY_PATH"]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户需要通过 App Store Connect 管理 iOS/macOS 应用程序。代理负责处理 API 认证、构建管理、TestFlight 分发、应用审核提交以及分析数据的获取。

## 快速参考

| 主题 | 文件 |
|-------|------|
| API 认证 | `api-auth.md` |
| 常见工作流程 | `workflows.md` |

## 核心规则

### 1. 必须使用 JWT 进行认证
App Store Connect API 使用用您的私钥签名的 JWT 令牌进行认证。

```bash
# Required environment variables:
# ASC_ISSUER_ID     - From App Store Connect > Users > Keys
# ASC_KEY_ID        - From the API key you created
# ASC_PRIVATE_KEY_PATH - Path to your .p8 private key file
```

请使用 ES256 算法生成 JWT 令牌，有效期最长为 20 分钟。具体代码示例请参见 `api-auth.md`。

### 2. API 版本控制
在请求中始终指定 API 的版本。

```bash
curl -H "Authorization: Bearer $JWT" \
     "https://api.appstoreconnect.apple.com/v1/apps"
```

当前稳定版本为 `v1`。有关 v2 的端点信息，请参阅 Apple 的官方文档。

### 3. 构建处理状态
构建文件上传后会经历以下状态：

| 状态 | 含义 | 操作 |
|-------|---------|--------|
| PROCESSING | 上传成功，正在处理 | 等待 |
| FAILED | 处理失败 | 检查日志 |
| INVALID | 验证失败 | 修复问题后重新上传 |
| VALID | 可以进行测试或提交 | 继续下一步 |

切勿提交状态为 `INVALID` 的构建文件。

### 4. TestFlight 分发
- **内部测试**：最多支持 100 名测试者，构建文件处理完成后即可立即使用。
- **外部测试**：最多支持 10,000 名测试者，首次发布版本时需要通过 Beta App Review 测试。
- 外部测试团队需要提供：应用描述、反馈邮箱地址和隐私政策链接。

### 5. 应用审核提交
在提交审核之前，请确保：
- 所有必要的元数据（描述、关键词、截图）都已填写完整。
- 应用预览视频时长不超过 30 秒。
- 隐私政策链接有效且可访问。
- 联系信息是最新的。

提交审核后，系统会创建一个 `appStoreVersion`，状态为 `PENDING_DEVELOPERRELEASE` 或 `WAITING_FOR_REVIEW`。

### 6. 请求速率限制
API 每小时有请求速率限制。如果遇到 429 错误，请使用指数退避策略进行处理。

```bash
# Respect Retry-After header
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

### 7. 包 ID 管理
包 ID 一旦创建后是不可删除或重命名的。

- 使用反向域名格式：`com.company.appname`
- 注册前请仔细规划包 ID 的命名。
- 每个包 ID 只能属于一个团队。

## 常见问题

- **JWT 令牌过期**：令牌的有效期最长为 20 分钟。在操作前请重新生成令牌。
- **API 密钥权限错误**：API 密钥需要具有相应的权限（例如管理员、应用管理员等）。
- **缺少合规性文件**：包含加密功能的应用需要提供 ECCN 或豁免证明文件。
- **构建版本冲突**：每个构建文件都需要唯一的版本号和构建编号组合。
- **截图尺寸**：截图尺寸必须与每种设备类型完全匹配（不允许缩放）。
- **分阶段发布混淆**：分阶段发布仅适用于 App Store，不适用于 TestFlight。

## 外部端点

| 端点 | 发送的数据 | 用途 |
|----------|-----------|---------|
| api.appstoreconnect.apple.com | 应用元数据、构建信息 | App Store Connect API |

没有其他数据会被发送到外部。

## 安全与隐私

**离开您机器的数据：**
- 发送给 Apple 的应用元数据（用于 App Store 列表展示）
- 用于处理的构建信息
- 分析数据查询结果

**保留在本地的数据：**
- API 私钥（.p8 文件）——绝对不能传输
- 生成的 JWT 令牌
- 下载的报告文件

**本技能不包括以下内容：**
- 以明文形式存储您的 .p8 密钥
- 与第三方共享凭据
- 访问团队之外的应用程序

## 相关技能
如果用户需要，可以使用以下命令进行安装：
- `clawhub install <slug>`：安装相关工具
- `ios`：iOS 开发相关知识
- `swift`：Swift 语言参考资料
- `xcode`：Xcode 集成开发环境使用指南

## 反馈
- 如果觉得本文档有用，请给它打星：`clawhub star app-store-connect`
- 保持更新：`clawhub sync`