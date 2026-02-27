---
name: Google Play Store
slug: google-play-store
version: 1.0.0
homepage: https://clawic.com/skills/google-play-store
description: 通过发布自动化工具、应用商店优化（ASO）、政策合规性管理以及应用被拒绝后的恢复机制，实现Android应用的发布、优化和在Google Play平台上的扩展。
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用本工具时，请阅读 `setup.md` 以获取集成指南。

## 使用场景

用户需要将 Android 应用发布到 Google Play 平台、进行管理或优化。该工具负责处理发布工作流程、应用优化、政策合规性检查、审核流程以及处理应用被拒的原因。

## 架构

应用程序的相关数据存储在 `~/google-play-store/` 目录下。具体结构请参考 `memory-template.md` 文件。

```
~/google-play-store/
├── memory.md         # Account, apps, preferences
├── apps/             # Per-app tracking
│   └── {package}/    # Package-specific notes
└── checklists/       # Saved submission checklists
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 内存管理模板 | `memory-template.md` |
| 发布跟踪与推广策略 | `tracks.md` |
| 应用商店优化 | `aso.md` |
| 政策合规性 | `policies.md` |
| 应用被拒后的处理 | `rejections.md` |
| 使用 Fastlane 实现自动化 | `fastlane.md` |

## 核心规则

### 1. 发布阶段的推进流程

| 阶段 | 目的 | 审核流程 | 使用者范围 |
|-------|---------|--------|-------|
| 内部测试 | 每日构建，质量保证 | 无 | 最多 100 名测试者 |
| 封闭测试 | 测试版测试者 | 2-6 小时 | 通过电子邮件通知 |
| 公开测试 | 公开测试版测试者 | 2-6 小时 | 任何人都可以参与 |
| 正式发布 | 正式版本 | 2-24 小时 | 所有用户 |

**新应用必须遵循的推进流程：**
```
Internal → Closed (20+ testers, 14+ days) → Production
```

如果跳过此步骤，应用将立即被拒绝。请在第一天就开始进行封闭测试。

### 2. 提交前的检查清单

在每次提交应用之前，请务必运行以下检查：

```
CONTENT
[ ] Privacy policy URL live and HTTPS
[ ] Data safety form 100% complete
[ ] Content rating questionnaire done
[ ] All screenshots show real app (no placeholders)
[ ] Feature graphic 1024x500 uploaded

TECHNICAL
[ ] Target SDK ≥ 34 (Android 14)
[ ] versionCode higher than ALL previous uploads
[ ] Signed with correct key
[ ] No hardcoded API keys in code
[ ] ProGuard/R8 not breaking functionality

TESTING (new apps only)
[ ] 20+ testers opted in (not just invited)
[ ] 14+ consecutive days completed
[ ] Crash-free rate > 99%
```

### 3. 版本代码策略

```
versionCode must ALWAYS increase. Cannot reuse. Ever.

Pattern: YYYYMMDDHH
Example: 2025022514 (Feb 25, 2025, 2pm)

Why: Rejected uploads "burn" the versionCode.
     Multiple builds per day need unique codes.
```

### 4. 应用签名方式

| 签名方式 | 控制权 | 恢复措施 | 适用场景 |
|-------|---------|----------|----------|
| 由 Google 管理 | Google 持有签名密钥 | 简单 | 新应用 |
| 用户上传密钥 | 用户签名，Google 重新签名 | 中等难度 | 大多数应用 |
| 自行管理 | 用户完全控制签名密钥 | 困难 | 企业级应用 |

**建议：**新应用应采用由 Google 管理的签名方式；更新应用时使用用户上传的密钥。

**重要提示：**创建密钥后，请立即导出并备份。

### 5. 分阶段发布协议

| 阶段 | 发布比例 | 发布时间 | 发布条件 |
|-------|---|----------|------|
| 预发布阶段（Canary） | 1% | 24-48 小时 | 应用崩溃率低于 0.1% |
| 早期测试阶段 | 5% | 48-72 小时 | 应用无异常（ANR）率低于 0.5% |
| 中期测试阶段 | 20% | 72-96 小时 | 应用评分稳定 |
| 后期测试阶段 | 50% | 96-120 小时 | 无功能回归 |
| 正式发布阶段 | 100% | 无问题 | 所有测试通过 |

**触发停止发布的条件：**应用崩溃率激增、异常（ANR）率激增、评分骤降、收到严重漏洞报告。

### 6. 应用商店优化（ASO）要点

| 元素 | 最大限制 | 影响程度 |
|---------|-------|--------|
| 应用标题 | 30 个字符 | 最重要 |
| 简短描述 | 80 个字符 | 非常重要 |
| 详细描述 | 4000 个字符 | 一般重要 |
| 屏幕截图 | 每种类型 8 张 | 非常重要 |
| 功能图示 | 1024x500 像素 | 一般重要 |

**关键词策略：**
- 应用标题：包含主要关键词和品牌名称
- 简短描述：自然融入前 3 个关键词
- 详细描述：包含长尾关键词
- 根据 Search Console 的数据定期更新关键词内容

### 7. 响应时间服务水平协议（SLA）

| 操作 | Google 的响应时间 | 用户的截止时间 |
|--------|-----------------|---------------|
| 政策相关邮件 | 7 天内解决 | 3 天内回复 |
| 提出申诉 | 3-7 天内 | 24 小时内提交申诉材料 |
| 数据请求 | 30 天内 | 14 天内完成提供数据 |
| 严重问题 | 应用被暂停发布 | 立即处理 |

**规则：**切勿忽视 Google 发来的政策相关邮件。沉默即表示默认接受规定。

## 常见问题及解决方法

### 发布相关问题
- **跳过封闭测试** → 应用无法正式发布。新应用必须完成至少 14 天的封闭测试。
- **数据收集不完整** → 应用会被立即拒绝。即使“未收集到数据”，也请填写所有字段。
- **使用模拟截图** → 会导致应用被拒绝。请使用真实的应用截图。
- **隐私政策相关问题（如 404 错误）** → 应用会被拒绝。每次提交前请确保相关链接有效。

### 技术相关问题
- **版本代码未递增** → 上传申请会被拒绝；即使被拒绝，已上传的文件仍会保留。
- **目标 SDK 版本过旧** → 应用会被拒绝。构建应用前请确认当前版本要求。
- **忘记上传密钥的密码** → 无法更新应用。请将密钥保存在密码管理工具中。
- **ProGuard 配置错误** → 应用发布后可能会出现崩溃。请务必测试发布版本。

### 政策相关问题
- **未声明必要的权限** → 违反政策规定。请为每个需要使用的权限提供合理解释。
- **不必要的后台定位功能** → 应用会被拒绝；如有此类功能，请删除或提供合理解释。
- **未声明适用于儿童的内容** → 违反政策规定。如果应用面向儿童用户，请务必声明。
- **误导性广告** → 会导致应用被暂停发布。请遵守广告展示规则。

### 商业相关问题
- **不采用分阶段发布策略** → 所有用户都会同时收到更新通知，可能导致问题。建议从 1% 的用户开始分阶段发布。
- **忽视政策相关邮件** → 会导致应用被暂停发布。请在 3 天内回复。
- **使用多个账户进行操作** → 会导致账户被封禁。一次违规即可能导致账户被永久关闭。

## 安全与隐私

**仅存储本地数据：**
- 应用包名称和应用状态（存储在 `~/google-play-store/` 目录下）
- 提交前的检查清单和工作流程记录
- 发布历史及经验总结

**本工具仅存储非敏感的元数据：**
- 应用名称和包标识符
- 应用发布阶段（内部测试/封闭测试/正式发布）
- 工作流程设置（手动发布或使用 CI/CD 工具）
- 检查清单的完成情况

**本工具不会存储以下内容：**
- API 密钥、服务账户的 JSON 数据
- 密钥库文件或密码
- OAuth 令牌及 Play Console 的认证信息
- 任何敏感信息或凭证

**本工具不会执行以下操作：**
- 上传应用或发送网络请求
- 访问签名密钥或证书
- 直接执行 Fastlane 命令

用户需在自己的 CI/CD 系统中管理所有认证信息，并自行执行相关命令。Fastlane 的示例仅用于说明用途。

## 相关工具

如果用户需要安装相关工具，请使用以下命令：
- `clawhub install <slug>`：
  - `android`：用于 Android 开发
  - `app-store`：用于 iOS 和 Android 应用的发布管理
  - `mobile`：用于跨平台应用的发布管理

## 反馈建议

- 如觉得本工具有用，请给 `clawhub` 评分（例如：`clawhub star google-play-store`）
- 为了获取最新信息，请使用 `clawhub sync` 命令进行同步。