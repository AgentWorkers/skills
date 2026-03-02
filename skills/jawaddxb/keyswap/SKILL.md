---
name: keyswap
description: 用于 OpenClaw Anthropic 用户资料的 Claude Max API 令牌轮换功能。当用户输入“swap key”（交换密钥）、“rotate key”（轮换密钥）或“new key”（新密钥）等指令，或提供一个新的 `sk-ant-` 令牌以替换当前令牌时，应使用此功能。
---
# 密钥轮换

在 OpenClaw 中，为 Anthropic 的两个账户（`anthropic:jawadjarvis` 和 `anthropic:manual`）轮换 Claude Max API 的令牌。

## 操作步骤

1. 如果用户尚未提供令牌，请要求其提供。令牌必须以 `sk-ant-` 开头。
2. 运行轮换脚本：

```bash
bash /opt/homebrew/lib/node_modules/openclaw/skills/keyswap/scripts/keyswap.sh <token>
```

3. 将结果告知用户。如果操作成功，确认两个账户的令牌均已更新，并且网关已重启；如果操作失败，显示错误信息。