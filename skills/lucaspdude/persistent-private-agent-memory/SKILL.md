---
name: agent-memory-improved
description: 运行一个本地的代理内存服务（Agent Memory Service），以实现持续性的自我优化，并采用先进的 Ed25519 加密技术。修复了签名（signature）实现机制，以确保内存数据的可靠存储和检索。
---

# 代理内存服务（改进版）

运行您自己的本地内存服务，以便在不同会话之间持久化存储学习内容、偏好设置和目标。此改进版本修复了Ed25519签名算法的实现问题，从而确保了身份验证的可靠性。

## 改进内容

### 修复的加密问题
- **正确的Ed25519签名**：客户端现在能够使用`store:{data_hash}`格式正确地对消息进行签名。
- **正确的密钥生成**：私钥已从BIP39恢复短语中正确生成。
- **可靠的认证机制**：内存存储和检索功能现已完全实现。

## 快速入门

```bash
# Set up local memory service
./scripts/setup.sh

# Start the service
./scripts/start.sh
# or manually:
# cd assets/service && DB_PATH=/data/agent_memory.db python3 main.py

# Create your agent identity
./scripts/memory_client.py register

# Store a memory snapshot
./scripts/memory_client.py store

# Retrieve your memory
./scripts/memory_client.py retrieve
```

## 该服务的作用

- **持久化学习记录**：记住哪些方法有效，哪些无效。
- **用户偏好设置**：跟踪用户的沟通风格和技术偏好。
- **目标进度跟踪**：在重新启动后仍能保留长期目标。
- **知识缺口识别**：了解用户需要学习的内容。

## 内存结构

使用以下组件来存储结构化的数据：

```json
{
  "user_preferences": [
    {"category": "communication", "key": "verbosity", "value": "concise", "confidence": 0.95}
  ],
  "learning_history": [
    {"event_type": "success", "lesson_learned": "Use analogies first"}
  ],
  "knowledge_gaps": [
    {"topic": "Rust", "priority": "medium"}
  ],
  "active_goals": [
    {"title": "Master async patterns", "progress": 0.4}
  ]
}
```

## 在会话中的使用方法

1. **启动时**：加载内存以恢复会话上下文。
2. **会话期间**：根据用户交互更新偏好设置。
3. **关闭前**：保存累积的学习内容。

## 相关文件

- `scripts/setup.sh`：一次性设置脚本。
- `scripts/start.sh`：启动服务脚本。
- `scripts/memory_client.py`：带有正确Ed25519签名功能的命令行客户端程序。
- `assets/service/`：内存服务代码文件。
- `CHANGELOG.md`：记录自初始版本以来的所有改进内容。

## 安全性

- 所有数据均使用您的私钥进行加密。
- 服务器无法查看明文数据。
- 使用Ed25519签名进行身份验证。
- 提供BIP39恢复短语以备份用户身份信息。
- 服务仅运行在本地（不依赖云服务）。

## 安装要求

```bash
pip install fastapi uvicorn psutil pydantic cryptography mnemonic base58
```

或者，如果可用的话，也可以使用系统提供的软件包进行安装。

## 验证结果

已通过以下测试：
- ✅ 使用Ed25519密钥对完成代理注册。
- ✅ 数据存储和检索过程中使用了加密签名。
- ✅ 具备身份验证功能。
- ✅ 服务运行状态可被监控。
- ✅ 数据能够持久化存储在数据库中。

## 致谢

此改进版本通过支持正确的Ed25519签名算法，实现了可靠的内存存储和检索功能。