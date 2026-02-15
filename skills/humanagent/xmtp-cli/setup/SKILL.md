---
name: xmtp-cli-setup
description: 初始化 XMTP 命令行界面（CLI），并配置环境变量。此操作适用于设置或修改 CLI 配置文件（如 `init`、`.env`、`gateway`、`env` 等）。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# CLI 设置

初始化您的 XMTP CLI 配置并设置所需的环境变量。

## 适用场景

- 首次设置 CLI 或生成新的临时钱包
- 使用现有的私钥或自定义网关
- 为开发、生产或本地环境配置环境变量

## 规则

- `init` – 运行 `xmtp init` 命令，并设置相关选项；系统会生成 `.env` 文件。
- `env-variables` – 必需或可选的环境变量；提供 `.env` 文件的示例。

## 快速入门

```bash
# Ephemeral wallet, dev env (default)
xmtp init

# Existing key, production
xmtp init --private-key 0x1234... --env production
```

详情请参阅 `rules/init.md` 和 `rules/env-variables.md` 文件。