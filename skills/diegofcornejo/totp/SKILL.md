---
name: totp
description: 基于 TOTP（Time-Based One-Time Password）的 OTP 验证机制，用于处理敏感操作（如环境变量设置、网关重启、备份删除、关键配置更改等）。该机制使用 `obtplib` 库，并设置超时时间为 2 分钟（允许 1 分钟内的延迟）。
metadata:
  {
    "openclaw": {
      "requires": { "env": ["TOTP_SECRET"], "bins": ["node"] },
      "primaryEnv": "TOTP_SECRET",
      "emoji": "🔐"
    }
  }
---
# TOTP 验证技能

使用基于时间的一次性密码（TOTP）来保护敏感操作的验证过程。

## 目的

保护对以下内容的访问：
- `.env` 变量
- `openclaw.json` 配置文件
- 网关重启操作
- 备份删除操作
- 关键配置更改
- 外部 API 密钥操作

## 设置

1. **安装依赖项：**
   ```bash
   npm install
   ```

2. **生成密钥和 QR 图像：**
   ```bash
   npm run generate
   ```
   （可选）输入服务名称和账户名称：
   ```bash
   node scripts/generate-secret.js MyService myuser
   ```

3. **将生成的 QR 图像（`qr.png`）发送给用户，然后立即删除它：**
   ```bash
   rm qr.png
   ```

4. **在 `.env` 文件中设置 TOTP_SECRET：**
   ```env
   TOTP_SECRET=YOUR_BASE32_SECRET_HERE
   ```

5. **使用生成的密钥或 QR 图像配置 Google Authenticator 或 Authy：**

## 使用方法

当需要执行敏感操作时：

1. **代理：** “请输入您的 OTP。”
2. **用户：** 从身份验证应用程序中输入 6 位数字。
3. **代理：** 运行验证：
   ```bash
   TOTP_SECRET=$TOTP_SECRET node scripts/verify.js 123456
   ```
4. **如果验证通过（返回代码 0）：** 继续执行操作。
5. **如果验证失败（返回代码 1）：** 拒绝访问。

## 相关文件

- `scripts/generate-secret.js` - 生成新的 TOTP 密钥和 QR 图像。
- `scripts/verify.js` - 验证 OTP 令牌（容忍时间误差为 1 分钟）。
- `SKILL.md` - 本文档。

## 安全注意事项

- **时间误差容忍范围：** 1 分钟（2 分钟内允许时间偏差）。
- **算法：** SHA1。
- **密码长度：** 6 位数字。
- **更新周期：** 30 秒。
- **密钥存储方式：** 使用 Base32 编码，存储在 `.env` 文件中，字段名为 `TOTP_SECRET`。

## 集成方式

此验证技能应集成到代理的决策流程中，适用于以下情况：
- 用户请求访问 `.env` 变量。
- 用户请求查看 `openclaw.json` 文件内容。
- 用户请求重启网关。
- 用户请求删除备份数据。
- 任何被标记为“关键操作”的操作。