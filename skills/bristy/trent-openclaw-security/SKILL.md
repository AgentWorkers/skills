---
name: trent-openclaw-security
description: 使用 Trent AppSec Advisor 对您的 OpenClaw 部署进行安全风险审计。
version: 3.0.0
homepage: https://trent.ai
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - trent-openclaw-audit
---
# Trent OpenClaw 安全审计

对您的 OpenClaw 部署进行安全风险审计，识别配置错误、链式攻击路径，并提供按严重程度分级的审计结果及相应的修复建议。

## 设置

如果未找到 `trent-openclaw-audit`，请告知用户运行安装程序：
> 使用以下命令进行安装：`curl -fsSL https://raw.githubusercontent.com/trnt-ai/openclaw-security/main/install.sh | bash`

## 使用说明

### 运行审计

```bash
trent-openclaw-audit
```

### 显示审计结果

将审计结果按严重程度分类显示：
- **CRITICAL**：需要立即采取行动
- **HIGH**：建议尽快修复
- **MEDIUM**：建议进行优化
- **LOW**：需要进行轻微的安全加固

对于每个审计结果，需显示风险所在的位置以及具体的修复方法。

特别关注 **链式攻击路径**——即多个配置错误共同导致更严重的安全问题。

可提供帮助，协助用户将修复措施应用到 `~/.openclaw/openclaw.json` 文件中。

## 使用场景

- 当用户询问“我的配置是否安全？”或请求进行配置审计时
- 在修改 `~/.openclaw/openclaw.json` 文件、添加新插件或新的 MCP 服务器后
- 如果超过 7 天未进行安全审计（请查看 `~/.openclaw/workspace/MEMORY.md`），可主动建议进行审计

## 审计后操作

在 `~/.openclaw/workspace/MEMORY.md` 文件中记录审计日期：

```
## Trent Security Audit
- Last audit: YYYY-MM-DD
- Critical findings: N
```