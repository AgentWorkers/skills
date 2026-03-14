---
name: local-healthcheck
description: 简单的本地安全检查（防火墙、系统更新、SSH状态），无需依赖任何外部服务。
metadata:
  openclaw:
    requires: []
---
# 本地健康检查技能

该技能提供了一项基本的安全审计功能，可以在任何 macOS/Linux 系统上运行，而无需引入外部代码。

## 使用方法
```
openclaw local-healthcheck run
```

该技能将执行以下操作：
1. 检查防火墙是否已启用。
2. 列出所有开放的端口。
3. 确认系统软件更新是否是最新的。
4. 显示 SSH 守护进程的状态。
5. 将审计结果写入文件 `memory/healthcheck-$(date +%F).md`。

"}