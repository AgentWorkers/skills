---
name: SSHKey
description: "SSH密钥对管理工具。支持生成新的SSH密钥对、列出现有的密钥、将公钥复制到剪贴板、检查密钥指纹、将密钥添加到SSH代理（ssh-agent）中、转换密钥格式以及测试SSH连接。简化了从终端进行SSH密钥管理的流程。"
version: "1.0.0"
author: "BytesAgain"
tags: ["ssh","key","security","authentication","crypto","server","admin","devops"]
categories: ["Security", "System Tools", "Developer Tools"]
---# SSH密钥管理
无需记忆任何参数即可轻松管理SSH密钥，支持生成、列出、复制和测试密钥的功能。
## 命令
- `generate [名称] [类型]` — 生成新的密钥对（ed25519/rsa）
- `list` — 列出现有的SSH密钥
- `fingerprint [密钥文件]` — 显示密钥的指纹信息
- `copy [密钥文件]` — 显示用于复制的公钥
- `test <主机>` — 测试与指定主机的SSH连接
## 使用示例
```bash
sshkey generate myserver ed25519
sshkey list
sshkey fingerprint ~/.ssh/id_ed25519
sshkey copy
sshkey test github.com
```
---
技术支持：BytesAgain | bytesagain.com