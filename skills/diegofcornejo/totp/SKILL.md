---
name: totp
description: 基于 TOTP（Time-Based One-Time Password）的 OTP 验证机制，用于处理敏感操作（如环境变量设置、网关重启、备份删除、关键配置更改等）。该机制使用 `tplib` 库，并设置验证窗口为 2 分钟（即用户有 2 分钟的时间来完成 OTP 验证）。
metadata:
  {
    "openclaw": {
      "requires": { "env": ["TOTP_SECRET"], "bins": ["node"] },
      "primaryEnv": "TOTP_SECRET",
      "emoji": "🔐"
    }
  }
---
# TOTP验证技能

使用基于时间的单次密码（TOTP）进行安全OTP验证，以保护敏感操作。

## 目的

保护对以下内容的访问：
- `.env` 变量
- `openclaw.json` 配置文件
- 网关重启操作
- 备份删除操作
- 重要配置更改
- 外部API密钥操作

## 设置

1. **安装依赖项：**
   ```bash
   npm install
   ```

2. **生成密钥和二维码：**
   ```bash
   npm run generate
   ```
   （可选）输入服务名称和账户名称：
   ```bash
   node scripts/generate-secret.js MyService myuser
   ```

3. **在 `.env` 文件中设置 TOTP_SECRET：**
   ```env
   TOTP_SECRET=YOUR_BASE32_SECRET_HERE
   ```

4. **使用生成的密钥配置 Google Authenticator 或 Authy：**

## 使用方法

当请求执行敏感操作时：

1. **代理：** “请提供您的OTP代码”
2. **用户：** 从认证应用程序中输入6位数字的OTP代码
3. **代理：** 运行验证：
   ```bash
   TOTP_SECRET=$TOTP_SECRET node scripts/verify.js 123456
   ```
4. **如果验证通过（返回0）：** 继续执行操作
5. **如果验证失败（返回1）：** 拒绝访问

## 相关文件

- `scripts/generate-secret.js` - 生成新的TOTP密钥和二维码
- `scripts/verify.js` - 验证OTP令牌（容忍时间偏差为1分钟）
- `SKILL.md` - 本文档

## 安全注意事项

- **时间偏差容忍范围：** 1分钟
- **加密算法：** SHA1
- **密码长度：** 6位数字
- **更新周期：** 30秒
- **密钥存储方式：** 以Base32编码的形式存储在 `.env` 文件中（键名为 `TOTP_SECRET`）

## 集成方式

此验证机制应集成到代理的决策流程中，适用于以下情况：
- 用户请求访问 `.env` 变量
- 用户请求查看 `openclaw.json` 文件内容
- 用户请求重启网关
- 用户请求删除备份数据
- 任何被标记为“关键操作”的操作