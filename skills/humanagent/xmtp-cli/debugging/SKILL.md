---
name: xmtp-cli-debugging
description: 通过环境变量启用 CLI 调试日志记录功能。在排查问题或检查 CLI 行为时使用该功能。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# CLI调试

通过环境变量启用XMTP CLI的调试日志功能。

## 适用场景

- 故障排除：用于诊断CLI的行为或连接问题
- 查看详细的日志（调试级别）

## 规则

- `force-debug-env`：对应环境变量 `XMTP_FORCE_DEBUG` 和 `XMTP_FORCE_DEBUG_LEVEL`

## 快速入门

在 `.env` 文件中设置相关环境变量，或使用 `export` 命令进行配置：

```bash
XMTP_FORCE_DEBUG=true
XMTP_FORCE_DEBUG_LEVEL=debug
```

详情请参阅 `rules/force-debug-env.md` 文件。