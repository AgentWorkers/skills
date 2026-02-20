---
name: contextkeeper
description: **ContextKeeper** — 为 AI 代理提供安全的项目状态跟踪功能。支持手动创建检查点，并确保输入数据的有效性（即数据的正确性和完整性）。该工具不涉及任何后台进程、进程 ID（PID）的操作，也不执行任何命令。
metadata:
  openclaw:
    requires:
      bins: []
    install: []
---
# ContextKeeper 🔮

> 为 AI 代理提供安全的项目状态跟踪功能

该工具能够记录您在不同会话中的工作内容，支持手动创建检查点，并在仪表板上查看项目状态。

---

## 安全性

| 风险 | 缓解措施 |
|------|------------|
| 远程代码执行 | 不会使用用户数据替换命令 |
| 进程 ID（PID）操纵 | 不生成 PID 文件，也不进行进程管理 |
| 后台进程 | 不启用任何监控或守护进程 |
| 注入攻击 | 对输入数据进行验证和处理（防止恶意代码注入） |

---

## 脚本

提供了两个简单的前台脚本：

| 脚本 | 功能 |
|--------|---------|
| `ckpt.sh` | 创建带有消息的检查点 |
| `dashboard.sh` | 查看项目状态 |

---

## 使用方法

```bash
# Create checkpoint
./ckpt.sh "Fixed auth issue"

# View status
./dashboard.sh
```

---

## 系统要求

- 必需安装 bash 工具
- 需要 git 工具（用于项目状态的检测）

---

**所属项目：** [TheOrionAI](https://github.com/TheOrionAI)