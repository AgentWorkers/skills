---
name: mfa-word
description: 在允许用户访问敏感文件或系统命令之前，会要求用户输入一个秘密单词作为验证。
metadata:
  openclaw:
    category: security
    tags: [security, mfa, privacy, zero-trust, audit-logs]
---

# MFA Word（安全门卫）

## 操作协议
1. **检测：** 在你（AI）执行任何涉及敏感数据（如 `.env` 文件、`.ssh` 文件、密码或数据删除等操作）之前，必须先调用 `check_gate_status` 函数。
2. **标准模式：** 如果 `check_gate_status` 返回 “OPEN”，则可以继续执行操作。当前会话的有效时间为 15 分钟。
3. **“死人开关”机制：** 如果 `check_gate_status` 返回 “OPEN_ONCE”，则执行请求的操作后，立即通知用户会话已被重新锁定以保障安全。
4. **验证请求：** 如果 `check_gate_status` 返回 “LOCKED”，必须停止操作并提示用户：“此请求涉及敏感数据，请提供您的密钥词以继续操作。”
5. **验证：** 用户提供密钥词后，调用 `verify_access` 函数进行验证。只有当验证结果为 “Access Granted” 时，才能继续执行操作。

## 工具

### initialize_mfa
用于设置安全层和用户偏好设置：
- `secret`：主要密钥词。
- `super_secret`：紧急重置密钥词。
- `sensitive_list`：需要保护的字符串或模式列表（默认值：`.env`、密码、配置文件、`sudo` 权限）。
- `use_dead_mans_switch`：布尔值。如果设置为 `true`，则在每次执行敏感操作后都会锁定会话。

### verify_access
用于验证用户提供的密钥词：
- `word`：用户在聊天中输入的密钥词。

### check_gate_status
内部工具，用于检查当前会话是否已通过身份验证。

### reset_mfa
使用紧急重置密钥词来重置用户的密钥词：
- `super_word`：紧急重置密钥词。
- `new_secret`：新的主要密钥词。