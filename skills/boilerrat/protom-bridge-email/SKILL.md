---
name: proton-bridge-email
description: 通过 Proton Mail Bridge（使用本地主机的 SMTP 服务）发送电子邮件，需使用经过年龄加密（age-encrypted）的凭据。此方法适用于为代理邮箱配置 Proton Bridge、加密 Proton Bridge 的凭据（不使用 1Password），或通过 Proton Bridge 自动发送电子邮件（如每日报告、警报等）。
---

# Proton Bridge 邮件发送（使用 age 加密）

作者：**Boilermolt + Boiler (Chris)**

使用 Proton Mail Bridge 进行本地 SMTP/IMAP 操作，并使用 `age` 对配置文件进行加密。

## 该工具提供的功能：
- 一个简单的 SMTP 发件脚本：`scripts/send_email.py`
- 一个用于加密配置文件的辅助脚本：`scripts/encrypt_env.sh`
- 设置说明：`references/proton-bridge-setup.md`

## 预期的本地密钥存储位置：
- 加密后的配置文件应存储在：`~/clawd/secrets/proton.env.age`
- 用户的 age 身份信息应存储在：`~/.config/age/keys.txt`

加密后的配置文件至少应包含以下内容：
- `PROTON_EMAIL`
- `PROTON_BRIDGE_USER`
- `PROTON_BRIDGE_PASS`（这是用于 Proton Bridge 的密码，而非您的 Proton 网页密码）
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURITY`

## 快速入门：
1) 设置 Proton Bridge（Linux 系统） → 参见 `references/proton-bridge-setup.md`。
2) 创建一个临时的明文配置文件（例如：`/tmp/proton.env`），然后对其进行加密：

```bash
bash scripts/encrypt_env.sh /tmp/proton.env <age-public-key>
```

3) 发送测试邮件：

```bash
python3 scripts/send_email.py \
  --to you@example.com \
  --subject "Test" \
  --body "Sent via Proton Bridge."
```

## 注意事项：
- Proton Bridge 在使用本地地址（localhost）进行 TLS 通信时通常会使用自签名证书。发送脚本支持这种设置。
- Proton Bridge 必须处于运行状态才能使本地 SMTP 功能正常工作。
- 请勿提交或共享任何敏感信息；只有在确实需要时才共享 `.age` 加密文件。