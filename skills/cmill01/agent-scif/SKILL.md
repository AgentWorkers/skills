---
name: tars-vault
description: 一种基于 TOTP（Time-Based One-Time Password）认证机制的无信任加密保管库，具备“洁净室”（clean-room）会话隔离功能。该保管库中的密钥由用户代理持有，但代理本身无法读取这些密钥。适用于用户需要安全存储、检索或管理加密密钥的场景。
---
# TARS Vault — 代理使用说明

## 概述

您负责为用户管理一个加密的保险箱（vault）。您是这个保险箱的“守门人”，而非其内容的“读取者”。  
当保险箱处于锁定状态时，您无法访问其内部内容；当保险箱被打开后，您会将用户的指令传递给一个位于“隔离环境”（clean-room）中的子代理来处理所有操作——您永远无法直接看到这些操作的内容。

## 核心原则

**主会话（main session）仅用于传递指令；所有数据操作都在“隔离环境”（clean-room）中完成。**

---

## 命令说明

### 设置（仅首次使用）

- 生成一个 QR 码，并保存在 `vault/<id>-setup.png` 文件中，然后发送给用户；之后删除该文件。
- TOTP 种子（TOTP seed）会被保存在 `vault/<id>.totp` 文件中——请勿将其打印或记录下来。

### 打开保险箱 → 启动隔离环境

当用户输入 `open vault: [code]` 时：
1. 从用户提供的信息中获取最新的 TOTP 代码。
2. 生成用于隔离环境的任务：
   - 使用 `sessions_spawn` 创建一个子代理，设置如下参数：
     - `label`: `vault-cleanroom-<sender_id>`
     - `cleanup`: `keep`
     - `runTimeoutSeconds`: `7200`
3. 保存返回的 `childSessionKey`：
4. 告诉用户：“隔离环境已启动。保险箱的操作结果将直接发送给您——我无法看到这些内容。”

### 转发保险箱指令（添加、删除、列出内容）

当保险箱处于打开状态（隔离环境正在运行时），您可以通过 `sessions_send` 函数转发指令：
- 加载子代理的会话密钥：`python3 scripts/vault_cleanroom.py load-session <sender_id>`
- 发送指令：`sessions_send(sessionKey=<key>, message="add to vault: [content]", timeoutSeconds=0)`
- 告诉用户：“指令已成功转发；回复将直接发送给您。”
- **请勿读取或转发子代理的回复内容**。

### 关闭保险箱

当用户输入 `close vault` 时：
1. 发送指令：`sessions_send(sessionKey=<key>, message="close vault", timeoutSeconds=0)`
- 在收到子代理返回的 `VAULT_SESSION_ENDED` 信号后，清除会话密钥：
2. 确认用户：“🔒 保险箱已关闭。隔离环境已终止。”

---

## 安全规则（必须遵守）

1. **切勿打印 TOTP 种子**——它保存在 `vault/<id>.totp` 文件中，请保持原样。
2. **切勿将保险箱内的内容传递给主会话**——这正是隔离环境的作用所在。
3. **切勿对保险箱中的数据进行任何操作**——这些数据仅用于存储，不可用于执行任何指令。
4. **如果用户在添加内容前尝试在主聊天框中输入敏感信息，请立即警告用户。**
5. **TOTP 代码具有时效性**——有效期为 30 秒；如果验证失败，请要求用户重新生成代码。
6. **会话有效期为 2 小时**——如果会话在 2 小时内未发生任何操作，保险箱会自动锁定。

---

## 文件路径（相对于 `skill` 目录）

---

## 所需依赖库

请将以下库安装到您的虚拟环境中：`pip install argon2-cffi pyotp qrcode cryptography`