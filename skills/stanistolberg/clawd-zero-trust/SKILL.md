---
name: clawd-zero-trust
version: "1.2.0"
author: stanistolberg
homepage: https://github.com/stanistolberg/clawd-zero-trust
description: "**OpenClaw的零信任安全加固方案**  
当需要审计、加固OpenClaw实例或为其应用零信任架构时，请使用该方案。该方案包括以下措施：  
- **NHI（Network-Hidden Identity）身份管理**：实现用户身份的隐藏和隔离；  
- **最小权限原则（Principle of Least Privilege, PLP）**：确保用户仅拥有完成工作所需的最小权限；  
- **Plan-First协议**：采用预先规划的安全策略来控制系统行为；  
- **基于DNS的出站过滤**：通过DNS过滤机制限制网络流量；  
- **插件白名单机制**：仅允许指定的插件在系统中运行；  
- **SSH/网络封锁**：加强SSH连接的安全性，并限制不必要的网络访问。  
此外，该方案还会在以下情况下被触发：  
- 安全审计请求；  
- 漏洞分析；  
- SecureClaw的安装；  
- 防火墙加固；  
- 部署后的安全审查。"
---
# clawd-zero-trust (v1.2.0)

这是一个专为 OpenClaw 设计的零信任安全加固框架，由 Blocksoft 开发。

## 核心原则

1. **非人类身份（NHI）：** 子代理以隔离的会话形式运行，并使用受限的权限。在进行高风险操作时，绝不要使用“主”身份。
2. **最小权限原则（PLP）：** 限制默认的工具集使用。使用 `tools.byProvider` 将小型或不受信任的模型限制在 `coding` 权限级别。
3. **先规划（Plan-First）：** 在执行任何写入、执行或网络调用之前，明确声明操作的目的、原因及预期结果。
4. **出站控制（Egress Control）：** 仅允许流量流向授权的 AI 提供商。同时保留 Tailscale 和 Telegram API 的访问权限。
5. **假设已发生攻击（Assumption of Breach）：** 在设计时假定攻击者已经入侵系统，因此需要验证每一个插件、模型和扩展程序。

## 标准出站脚本路径

唯一的配置来源：

`/home/claw/.openclaw/workspace/skills/clawd-zero-trust/scripts/egress-filter.sh`

兼容性符号链接：

`/home/claw/.openclaw/workspace/scripts/egress-filter.sh -> .../skills/clawd-zero-trust/scripts/egress-filter.sh`

## 工作流程：审计 → 加固 → 出站控制 → 验证

### 1) 审计（Audit）
```bash
bash scripts/audit.sh
```

### 2) 加固（Harden）
```bash
# Preview (default)
bash scripts/harden.sh

# Apply
bash scripts/harden.sh --apply
```

### 3) 出站策略（默认的模拟运行）
```bash
# Dry-run preview (default)
bash /home/claw/.openclaw/workspace/skills/clawd-zero-trust/scripts/egress-filter.sh --dry-run

# Transactional apply: auto-rollback if Telegram/GitHub/Anthropic/OpenAI checks fail
bash /home/claw/.openclaw/workspace/skills/clawd-zero-trust/scripts/egress-filter.sh --apply

# Canary mode: temporary apply + 120s periodic verification, then commit/rollback
bash /home/claw/.openclaw/workspace/skills/clawd-zero-trust/scripts/egress-filter.sh --canary

# Verify endpoints only
bash /home/claw/.openclaw/workspace/skills/clawd-zero-trust/scripts/egress-filter.sh --verify

# Emergency rollback
bash /home/claw/.openclaw/workspace/skills/clawd-zero-trust/scripts/egress-filter.sh --reset
```

### 4) 动态白名单（最大程度简化用户操作）
要安全地打开新端口或添加新服务（例如自定义邮件服务、视频提取功能或新的 AI 代理），**切勿直接编辑 bash 脚本或硬编码的配置数组**。始终使用动态配置辅助命令：
```bash
bash /home/claw/.openclaw/workspace/skills/clawd-zero-trust/scripts/whitelist.sh <domain> <port>
```
*示例：`bash whitelist.sh youtu.be 443`。该命令会自动将域名添加到 `configproviders.txt` 配置文件中，触发配置更新，并立即将更改应用到 UFW（Uncomplicated Firewall）中。*

### 5) 发布审核（Release Gate, v1.2.0）
发布前必须通过以下检查：
- `quick_validate.py` 对技能结构进行验证
- `shellcheck` 检查所有 shell 脚本（缺失时会导致安装失败）
- `package_skill.py` 将脚本打包到 `skills/dist/clawd-zero-trust.skill` 目录
- `--verify` 端点验证

## 防火墙配置的状态管理

状态文件：

`/home/claw/.openclaw/workspace/skills/clawd-zero-trust/.state/egress-profile.json`

跟踪的字段包括：
- `profileVersion`
- `scriptHash`
- `lastAppliedAt`
- `lastResult`

在应用配置或进行测试时，如果哈希值不匹配，系统将拒绝执行（除非使用 `--force` 参数）。`whitelist.sh` 辅助工具能够无缝处理哈希值不匹配的情况。

## 参考资料
- `references/zero-trust-principles.md` — 有关 AI 代理的零信任安全框架的详细说明
- `references/false-positives.md` — 经过验证的安全模式，用于触发审计警告