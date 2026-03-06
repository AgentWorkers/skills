---
name: max-auth
description: Security authentication gate for OpenClaw sensitive actions. Deploys a local Node.js auth server with biometric passkeys (WebAuthn/Touch ID/Face ID) and master password. Exposes a dashboard via Tailscale HTTPS. Use when: (1) setting up authentication for sensitive agent actions, (2) checking if user is authenticated before destructive/external operations, (3) registering or managing passkeys, (4) integrating auth into OpenClaw workflows. Sensitive actions = delete files, install packages, send messages to 3rd parties, call mutating APIs.
---

# Max Auth

这是一个用于 OpenClaw 的生物特征识别（Biometric）与密码相结合的认证服务器。该服务器运行在 `http://127.0.0.1:8456`，并通过 Tailscale 提供访问接口：`https://<hostname>/auth`。

## 快速设置

```bash
mkdir -p ~/.max-auth
cp <skill>/assets/auth-server.js ~/.max-auth/
cp <skill>/assets/package.json ~/.max-auth/
cd ~/.max-auth && npm install
node auth-server.js set-password 'your_password'
```

请按照以下步骤将其安装为 systemd 服务并通过 Tailscale 进行配置——详细说明请参阅 `references/api.md`。

## 在执行敏感操作前进行身份验证

```bash
# Shell
STATUS=$(curl -s http://127.0.0.1:8456/status)
HAS_SESSION=$(echo $STATUS | python3 -c "import sys,json; print(json.load(sys.stdin)['hasSession'])")
[ "$HAS_SESSION" = "True" ] || { echo "⚠️ Auth required: https://<hostname>/auth"; exit 1; }
```

**需要身份验证的敏感操作：** 删除文件、安装软件包、修改系统配置、向第三方发送消息/电子邮件、调用外部 API。

**无需身份验证即可执行的操作：** 读取数据、搜索、列出信息、获取网页内容、查询内存数据。

如果未进行身份验证，系统将拒绝执行相关操作，并提示用户：“⚠️ 需要身份验证。请访问 `https://<hostname>/auth` 进行登录。”

## 参考资料

- **完整的 API 说明及设置指南**：`references/api.md`
- **代理集成方案**：`references/integration.md`