---
name: ssh-batch-manager
description: 批量SSH密钥管理：支持向多个服务器分发或从多个服务器移除SSH密钥，并具备智能的连接性预检查功能以及源代码追踪机制。
homepage: https://gitee.com/subline/onepeace/tree/develop/src/skills/ssh-batch-manager
metadata:
  {
    "openclaw":
      {
        "emoji": "🔑",
        "requires": { "bins": ["ssh", "ssh-copy-id", "sshpass"], "python_packages": ["cryptography"] },
      },
  }
---
# SSH 批量管理工具

## ⚠️ 重要安全规则

**英文原文：** 在执行任何启用操作之前，代理必须通过消息获得用户的明确确认。未经用户明确批准，切勿执行任何操作。**

---

该工具用于批量管理基于 SSH 密钥的身份验证流程。

## 主要功能

- ✅ 智能连接预检查（速度提升 40 倍）
- ✅ 在 `authorized_keys` 文件中显示来源标识符
- ✅ 强制要求用户进行安全确认
- ✅ 自动启动 Web 用户界面服务

## 安装

```bash
clawhub install ssh-batch-manager
```

安装完成后，Web 用户界面会自动启动！

## 使用方法

```bash
# Enable all servers
python3 ssh-batch-manager.py enable-all

# Disable all servers
python3 ssh-batch-manager.py disable-all

# Web UI: http://localhost:8765
```

## 版本信息

**v2.1.3** – 完整的中文翻译（包含 Web 用户界面、文档和源代码）

## 代码仓库

**来源代码**: https://gitee.com/subline/onepeace/tree/develop/src/skills/ssh-batch-manager

**许可证**: MIT

**作者**: TK