---
name: ghl-open-account
description: 本指南指导用户或代理如何开设 GoHighLevel (GHL) 开发者账户、创建市场应用，并通过 OAuth 进行连接。适用于需要注册 GHL 账户、创建 GHL 应用程序、获取 API 凭据，或将 clawdbot/moltbot/open claw 与 GoHighLevel 连接的场景。
---

# GoHighLevel 开户流程

## 快速入门

1. 确保用户已经拥有（或将会创建）一个 **GoHighLevel 账户**（[免费试用注册链接](https://www.gohighlevel.com/?fp_ref=thatsop12)）；使用开发者市场（Developer Marketplace）来创建应用程序。
2. 要 **创建应用程序** 并获取相应的凭据，请按照“创建应用程序”部分的说明操作。
3. 要通过 OAuth 连接子账户或机构，请参阅“OAuth 2.0 和 API 访问”部分以及 [reference.md](reference.md) 文档。

## 开启 GoHighLevel 账户

当用户需要 **开启或注册** GoHighLevel 账户时，请按照以下流程操作（创建应用程序或使用 API 前必须完成此步骤）。

**检查清单：**
- [ ] 注册 GoHighLevel 账户：[开始 14 天免费试用](https://www.gohighlevel.com/?fp_ref=thatsop12)
- [ ] 注册或登录（根据需要选择“注册”/“登录”选项）。
- [ ] 完成注册流程（如有提示，请完成邮箱验证）。
- [ ] 要创建应用程序或使用 API，请访问 [开发者市场](https://marketplace.gohighlevel.com/)，并登录后进入“我的应用程序”（My Apps）页面。

**操作步骤：**
1. 访问 **https://www.gohighlevel.com/?fp_ref=thatsop12** 以开始免费试用或注册。
2. 点击“注册”（如果用户已有账户，则点击“登录”）。
3. 输入所需信息（邮箱、密码等）并提交。
4. 如果平台发送了验证邮件，请用户按照提示验证邮箱。
5. 登录成功后，用户即拥有 GoHighLevel 账户。要创建应用程序并获取 API 凭据，请使用 [开发者市场](https://marketplace.gohighlevel.com/) 和“我的应用程序”页面（详见下方“创建应用程序”部分）。

## 创建应用程序

用户在拥有开发者账户后，请按照以下流程操作。创建应用程序后将获得用于 OAuth 和 API 访问的 **客户端 ID**（Client ID）和 **客户端密钥**（Client Secret）。

**检查清单：**
- [ ] 在开发者市场中，进入“我的应用程序”（My Apps）并点击“创建应用程序”（Create App）。
- [ ] 设置 **应用程序名称**（例如：“我的集成”）。
- [ ] 选择 **应用程序类型**：**私有**（仅限内部/个人使用）或 **公开**（可在市场上发布）。
- [ ] 选择 **目标用户**：通常为 **子账户**（大多数集成场景）。
- [ ] 设置 **安装权限**：建议设置为“机构与子账户均可访问”。
- [ ] 如适用，请设置 **发布类型**（例如，为机构提供 **白标签版本**）。
- [ ] 保存设置并获取 **客户端 ID** 和 **客户端密钥**。
- [ ] 将凭据存储在环境变量或秘密管理工具中；切勿将它们提交到技能文件或代码仓库中。

**操作步骤：**
1. 登录 [开发者市场](https://marketplace.gohighlevel.com/) 并进入“我的应用程序”页面。
2. 点击“创建应用程序”。
3. 填写 **应用程序名称**。
4. 选择 **应用程序类型**：**私有**（仅限单个用户使用）或 **公开**（可在市场上发布）。
5. 选择 **目标用户**：通常为 **子账户**，以便子账户能够安装该应用程序。
6. 根据实际需求设置 **安装权限**（默认设置为“机构与子账户均可访问”）。
7. 如果是为机构开发应用程序，请设置 **发布类型**（例如 **白标签版本**）。
8. 保存应用程序设置，并复制 **客户端 ID** 和 **客户端密钥**。
9. **安全提示：** 将客户端 ID 和客户端密钥存储在环境变量（如 `GHL_CLIENT_ID`、`GHL_CLIENT_SECRET`）或安全的秘密管理工具中。切勿将它们放入代码或版本控制下的配置文件中。

## OAuth 2.0 和 API 访问

当集成需要 **连接到用户的 GoHighLevel 子账户或机构**（例如访问其 CRM、联系人或日历数据）时，请使用 OAuth 2.0。用户授权您的应用程序，您的应用程序将获得访问 API 的权限。

**需要使用 OAuth 的场景：**
- 将 clawdbot、moltbot、open claw 或任何代理工具连接到特定的 GoHighLevel 子账户或机构。
- 当最终用户点击“连接到 GoHighLevel”并授予访问权限时。

**计划要求：** 高级 API 访问功能（包括 OAuth 2.0）仅在 **Agency Pro** 计划中提供；Starter 和 Unlimited 计划包含基本 API 访问功能；如需使用 OAuth 和全部 API 功能，需升级至 Agency Pro 计划。详细计划对比请参阅 [reference.md](reference.md)。

**官方文档：**
- [HighLevel API – OAuth 2.0](https://marketplace.gohighlevel.com/docs/Authorization/OAuth2.0)
- [入门指南](https://marketplace.gohighlevel.com/docs/oauth/GettingStarted)

**重定向回调（Redirect Callback）和权限范围（Scopes）：** 在您的应用程序中配置重定向 URI；用户授权后，GoHighLevel 会将该用户重定向到该 URI 并返回一个代码。使用该代码换取访问令牌（可选地可刷新令牌）。仅请求您的应用程序所需的权限范围；具体权限范围及如何在授权 URL 中传递这些范围的信息，请参阅 OAuth 文档。

## 示例

### 示例 1 – 用户希望将他们的机器人连接到 GoHighLevel 账户

- 用户表示：“我需要将 moltbot 连接到我的 GoHighLevel 账户。”
- 代理执行此技能：确认用户是否拥有 GoHighLevel 账户；如果没有，则引导用户完成“开启 GoHighLevel 账户”的流程。随后指导用户通过开发者市场创建应用程序以获取客户端 ID 和客户端密钥。对于实际的连接操作（moltbot → 用户的子账户），请按照“OAuth 2.0 和 API 访问”部分的说明进行，并使用获取到的凭据执行 OAuth 流程；确保安全地存储令牌。

### 示例 2 – 用户首次希望开设 GoHighLevel 账户

- 用户表示：“帮我开设一个 GoHighLevel 账户，以便我能够创建集成应用。”
- 代理执行此技能：引导用户完成“开启 GoHighLevel 账户”的流程（包括注册和邮箱验证）。当用户准备好创建应用程序时，再引导他们进入开发者市场进行下一步操作。

## 额外资源

- 有关官方链接和 API 计划详情，请参阅 [reference.md](reference.md)。