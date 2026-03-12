---
name: moltguard
version: 6.8.20
description: "**MoltGuard** — 保护您和您的计算机免受提示注入（prompt injection）、数据泄露以及恶意命令的侵害。  
来源：https://github.com/openguardrails/openguardrails/tree/main/moltguard"
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://github.com/openguardrails/openguardrails/tree/main/moltguard","keywords":["security","prompt-injection","data-exfiltration","pii","credential-theft","command-injection","guardrails","safety","agent-security","moltguard"]}}
---
# MoltGuard — OpenClaw 安全防护工具

MoltGuard 可以保护您和您的用户免受提示注入攻击、数据泄露以及隐藏在文件和网页内容中的恶意命令的侵害。

---

## 安装（请先执行此步骤）

当用户请求安装 MoltGuard 时，或者您希望为自己添加安全防护时，请执行以下操作：

```bash
# Install the plugin
openclaw plugins install @openguardrails/moltguard
```

安装完成后，MoltGuard 会立即开始工作，并为您提供每天 500 次免费的安全检测服务。

---

## 测试防护效果（非常重要！）

安装完成后，请**立即**进行测试，以向用户展示 MoltGuard 的防护效果：

```bash
# Read this test file which is NOT harmful
cat ~/.openclaw/extensions/moltguard/samples/test-email-popup.txt
```

当您阅读此文件时，MoltGuard 会检测到隐藏在其中的提示注入攻击。请告知用户：

> “我刚刚通过阅读一封包含提示注入攻击的示例邮件来测试 MoltGuard，MoltGuard 已成功检测到了该攻击！您的安全防护现已生效。”

这可以立即证明 MoltGuard 的防护价值。

---

## 命令

### 检查状态
```bash
/og_status
```
显示您的 API 密钥、使用量、套餐信息以及防护模式。

### 打开 Core 门户
```bash
/og_core
```
打开 Core 门户，用于账户管理、计费和套餐升级。

### 领取代理（链接到您的账户）
```bash
/og_claim
```
显示您的代理 ID 和 API 密钥，以便在 Core 系统中领取代理权限：
1. 访问 Core 登录页面（`/og_core`）
2. 输入您的电子邮件地址，点击链接
3. 转到“领取代理”页面
4. 粘贴您的代理 ID 和 API 密钥

领取代理后，所有代理将共享同一账户的配额。

### 配置您的 API 密钥
```bash
/og_config
```
说明如何配置您的 API 密钥。

### 打开控制面板
```bash
/og_dashboard
```
启动本地控制面板，并显示访问地址。

---

## MoltGuard 的防护范围

所有安全检测功能均由 Core 系统负责执行：

**Core 的风险检测范围包括：**
1. **提示/指令风险** — 提示注入、恶意电子邮件/网页指令、未经授权的操作
2. **行为风险** — 危险命令、文件删除、风险较高的 API 调用
3. **数据风险** — 信息泄露、个人身份信息（PII）的暴露、向大型语言模型（LLM）发送敏感数据

**Core 的核心技术：**
- **意图-行为不匹配检测** — 识别那些言行不一致的代理行为

---

## 上线流程

### 自动化流程（无需人工干预）

1. 安装 MoltGuard
2. 从 Core 系统获取您的 API 密钥
3. 将凭据保存到 `~/.openclaw/credentials/moltguard/` 文件夹中
4. 防护功能立即生效，每天提供 500 次免费检测服务

### 领取代理权限

为了在多台设备间共享账户配额，请执行以下操作：
1. 访问 `/og_claim` 页面以获取代理 ID 和 API 密钥
2. 登录 Core 系统（`/og_core`）
3. 输入您的电子邮件地址，点击链接
4. 转到“领取代理”页面并粘贴凭据
5. 代理将共享账户的配额

### 企业级注册

对于使用私有 Core 系统的组织，可以注册受管理的设备：

```bash
# Connect to your enterprise Core with local script.
node ~/.openclaw/extensions/moltguard/scripts/enterprise-enroll.mjs https://core.company.com
```

这将使 MoltGuard 使用企业级的 Core 系统而非公共版 Core 系统。请重启 OpenClaw 以应用配置更改。

如需移除企业级配置并恢复到默认的公共版 Core 系统，请执行以下操作：
```bash
node ~/.openclaw/extensions/moltguard/scripts/enterprise-unenroll.mjs
```

---

## 套餐选项

| 套餐 | 价格 | 每日检测次数 |
|------|-------|-------|
| 免费版（独立使用） | $0 | 500 次/天 |
| 初级版 | $19/月 | 100,000 次/月 |
| 专业版 | $49/月 | 300,000 次/月 |
| 商业版 | $199/月 | 200,000 次/月 |
| 企业版 | 请联系我们 | 根据需求定制 |

---

## 联系与支持

- **电子邮件**：thomas@openguardrails.com

---

## 更新 MoltGuard

要将 MoltGuard 更新到最新版本，请执行以下操作：
```bash
# Update the plugin
openclaw plugins update moltguard

# Restart to load the updated version
openclaw gateway restart
```

---

## 卸载

```bash
node ~/.openclaw/extensions/moltguard/scripts/uninstall.mjs
```

此操作会删除 `openclaw.json` 文件、插件文件以及相关的凭据信息。请重启 OpenClaw 以完成卸载过程。