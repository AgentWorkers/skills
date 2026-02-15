---
name: listing-swarm
description: 将您的人工智能产品提交到70多个AI目录中。该代理可自动完成表单填写、验证码识别（支持两种验证码类型）以及电子邮件验证（通过IMAP协议）。这可以节省用户10多个小时的手动提交时间。用户需要提供自己的API密钥——系统中不会存储任何用户的凭证信息。
version: 1.0.3
author: LinkSwarm
website: https://linkswarm.ai/skill/
security: BYOK
metadata:
  openclaw:
    requires:
      env:
        - CAPTCHA_API_KEY
        - CAPTCHA_SERVICE
        - IMAP_USER
        - IMAP_PASSWORD
        - IMAP_HOST
      bins:
        - node
    primaryEnv: CAPTCHA_API_KEY
    user-invocable: true
    disable-model-invocation: true
---

# Listing Swarm 🐝

**这是一个Clawdbot技能，用于将您的人工智能产品发布到70多个AI目录中。**

您的代理负责提交信息，您需要提供Captcha API密钥。在遇到问题时，可以由人工协助解决。

---

## 🔒 安全模型：BYOK（Bring Your Own Key，自行提供密钥）

> **此技能不包含任何敏感信息。** 所有的API密钥和密码都由您在运行时通过环境变量提供。没有任何数据会被存储、记录或传输到LinkSwarm。

| 项目 | 安全性 |
|------|----------|
| Captcha API | ✅ 密钥、账户和计费信息均由您控制 |
| 邮箱/IMAP | ✅ 您的登录凭据（可选），不会被存储 |
| 数据传输 | ✅ 仅包含您的产品信息，不会被泄露 |
| 源代码 | ✅ 完全透明，无任何混淆处理 |

**请参阅[SECURITY.md](SECURITY.md)以获取完整的安全文档。**

---

## 功能介绍

该技能可自动将您的人工智能工具提交到以下目录：
- There's An AI For That
- Futurepedia
- OpenTools
- TopAI.Tools
- AI Tool Guru
- 以及另外65多个目录

## 设置

### 1. 获取自己的Captcha解决API密钥（必需）

⚠️ **您必须自行获取API密钥。** 该技能本身不提供密钥。

1. 访问[2Captcha.com](https://2captcha.com)（推荐）
2. 创建一个账户
3. 充值（约3美元可解决1000个验证码，足够提交到所有70个目录）
4. 从控制面板复制您的API密钥

然后将密钥添加到您的环境变量中：
```bash
export CAPTCHA_API_KEY="your-own-2captcha-key"
export CAPTCHA_SERVICE="2captcha"
```

其他可用服务（操作流程相同）：
- [Anti-Captcha](https://anti-captcha.com)
- [CapSolver](https://capsolver.com)

**没有API密钥？** 代理会标记每个验证码，让您手动解决。

### 2. 通过电子邮件进行自动验证（可选）

大多数目录会发送验证邮件。如果您提供IMAP访问权限，您的代理可以自动处理这些邮件。

**建议：** 为提交操作创建一个专用邮箱：
```
yourproduct.listings@gmail.com
```

**对于Gmail：**
1. 创建新的邮箱账户（或使用现有账户）
2. 启用两步验证：Google账户 → 安全设置 → 两步验证
3. 生成应用密码：Google账户 → 安全设置 → 应用密码 → 生成新密码
4. 复制16位的应用密码

将密码设置到环境变量中：
```bash
export IMAP_USER="yourproduct.listings@gmail.com"
export IMAP_PASSWORD="xxxx xxxx xxxx xxxx"  # app password, not your real password
export IMAP_HOST="imap.gmail.com"
```

**没有电子邮件访问权限？** 代理会提示您：“请查看Futurepedia发送的验证链接。”

### 3. 产品信息

创建一个产品配置文件，供代理参考：
```json
{
  "name": "Your Product Name",
  "url": "https://yourproduct.ai",
  "tagline": "One line description (60 chars)",
  "description": "Full description for directory listings...",
  "category": "AI Writing Tool",
  "pricing": "Freemium",
  "logo_url": "https://yourproduct.ai/logo.png",
  "screenshot_url": "https://yourproduct.ai/screenshot.png",
  "email": "hello@yourproduct.ai"
}
```

## 使用方法

告诉您的Clawdbot代理：

> “使用listing-swarm技能将我的产品提交到AI目录。我的产品信息保存在product.json文件中，我的Captcha密钥已设置到环境变量中。”

代理将执行以下操作：
1. 加载目录列表
2. 访问每个目录的提交页面
3. 使用您提供的产品信息填写表格
4. 通过您的API密钥解决验证码
5. 在遇到问题时（如需要登录或支付）通知您
6. 跟踪提交进度

## 人工干预机制

当代理遇到无法处理的情况时，它会提示您：
- “这个目录需要您先创建账户”
- “这个目录需要付费才能发布”
- “验证码尝试了3次仍未通过，您能帮忙解决吗？”

您解决这些问题后，再让代理继续操作。

## 目录列表

完整的目录列表位于`directories.json`文件中，包含以下信息：
- 目录名称和URL
- 提交页面URL
- 域名评分
- 月访问量
- 是否免费或付费发布
- 提交过程中的注意事项

## 提交记录

提交记录保存在`submissions.json`文件中：
```json
{
  "directory": "Futurepedia",
  "status": "submitted",
  "submitted_at": "2026-02-09",
  "listing_url": null,
  "notes": "Pending review"
}
```

## 相关文件

相关文件请参见`files`目录。

## 使用建议

- **从免费目录开始提交**：许多目录接受免费提交
- **准备好截图**：大多数目录至少需要一张截图
- **保持品牌一致性**：在所有平台上使用相同的名称/标语
- **检查邮件**：许多目录会发送验证链接

## 为什么需要这个技能

将产品发布到AI目录是一项繁琐的任务，因为需要处理70多个不同的网站及其各自的提交流程。让您的代理负责这些基础工作，您可以专注于需要人工处理的部分。

该技能是[LinkSwarm](https://linkswarm.ai)的一部分——一个专注于提升AI产品可见性的平台。