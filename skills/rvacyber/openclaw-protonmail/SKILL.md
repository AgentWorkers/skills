---
name: protonmail
description: 通过 Proton Mail Bridge 实现与 ProtonMail 的集成，以阅读和发送加密邮件。
homepage: https://github.com/rvacyber/openclaw-protonmail-skill
metadata: {"openclaw":{"emoji":"🔐","requires":{"env":["PROTONMAIL_ACCOUNT","PROTONMAIL_BRIDGE_PASSWORD"]},"install":[{"id":"brew-bridge","kind":"brew","formula":"proton-mail-bridge","bins":[],"label":"Install Proton Mail Bridge (macOS)","cask":true}]}}
---
# ProtonMail 技能

通过 Proton Mail Bridge 使用 ProtonMail 进行安全电子邮件通信。

## 设置（只需一次）

1. **安装 Proton Mail Bridge：**
   ```bash
   brew install --cask proton-mail-bridge
   ```

2. **启动 Bridge 并登录：**
   - 打开 Proton Mail Bridge 应用程序
   - 使用您的 ProtonMail 凭据登录
   - Bridge 会生成本地的 IMAP/SMTP 凭据

3. **配置该技能：**
   将其添加到您的 OpenClaw 配置文件（`~/.openclaw/openclaw.json`）中：
   ```json
   {
     "skills": {
       "entries": {
         "protonmail": {
           "enabled": true,
           "env": {
             "PROTONMAIL_ACCOUNT": "your-email@pm.me",
             "PROTONMAIL_BRIDGE_PASSWORD": "bridge-generated-password"
           }
         }
       }
     }
   }
   ```

4. **获取 Bridge 凭据：**
   - 在 Bridge 中，点击您的账户 → 邮箱设置
   - 复制 IMAP 密码（不是您的 ProtonMail 密码）
   - 使用 `skills.entries.protonmail`（而非 `skills.protonmail`）

## CLI 使用方法

该技能提供了一个名为 `protonmail` 的 CLI 工具：

```bash
# List inbox (most recent 10 emails)
protonmail list-inbox --limit=10 [--unread]

# Search emails
protonmail search "from:alice@example.com" --limit=20

# Read specific email
protonmail read <uid>

# Send email
protonmail send --to=bob@example.com --subject="Meeting" --body="See you at 3pm"

# Reply to email
protonmail reply <uid> --body="Sounds good!"
```

## 常见请求

- **查看收件箱：**“查看我的 ProtonMail 收件箱”
- **搜索邮件：**“在 ProtonMail 中搜索来自 alice@example.com 的邮件”
- **阅读邮件：**“阅读 ProtonMail 中 UID 为 31 的邮件”
- **发送邮件：**“通过 ProtonMail 向 bob@example.com 发送关于项目的邮件”
- **回复邮件：**“回复 ProtonMail 中 UID 为 31 的邮件”

## 工作原理

1. Proton Mail Bridge 在本地运行，并连接到您的 ProtonMail 账户
2. Bridge 提供本地的 IMAP（读取）和 SMTP（发送）服务
3. 该技能连接到 Bridge 的本地服务器
4. 所有的加密/解密操作都在本地通过 Bridge 完成
5. 无需使用任何第三方服务——直接与 ProtonMail 集成

## 安全性

- ✅ 官方 Proton 软件（经过审计的开源 Bridge）
- ✅ 保持端到端加密
- ✅ 凭据仅存储在本地
- ✅ 不使用 API 密钥或令牌——仅使用标准的 IMAP/SMTP 协议
- ✅ Bridge 密码与您的 ProtonMail 密码分开

## 故障排除

### “连接被拒绝”错误
- **检查 Bridge 是否正在运行：** 打开 Proton Mail Bridge 应用程序
- **验证端口：** Bridge 应显示 127.0.0.1:1143（IMAP）和 127.0.0.1:1025（SMTP）

### “身份验证失败”
- **使用 Bridge 的密码，而非 ProtonMail 的密码：** 从 Bridge 的“账户”→“邮箱设置”中获取密码
- **检查账户邮箱地址：** 必须完全匹配（例如 `user@pm.me` 或 `user@protonmail.com`）

### “技能未找到”
- **重新安装技能：** 在技能目录中运行 `npm run install-skill`
- **检查 OpenClaw 配置：** 确保 `skills.protonmail.enabled: true` 为 `true`

## 开发

有关开发设置和测试的详细信息，请参阅 [README.md](README.md)。

## 许可证

MIT 许可证 — 详情请参阅 [LICENSE](LICENSE)