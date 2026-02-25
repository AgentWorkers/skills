---
name: openclaw-guardian
description: 这是一个为 OpenClaw 开发的安全层插件，它通过多守护者代理的投票机制来拦截高风险的人工智能操作（如文件删除、配置修改、外部请求等）。该插件支持分层审核流程：快速通道（自动通过）、简易审核（由单个守护者负责）以及全面审核（由三位守护者从安全性、隐私性、权限、可逆性、成本等多个角度进行评估）。该插件采用基于关键词的风险评分机制，并支持零成本的规则匹配功能；仅针对真正需要审核的操作（约占所有操作的 5%）才会触发基于大型语言模型（LLM）的守护者评估流程。
---
# OpenClaw Guardian

> 为AI代理提供缺失的安全防护层。

## 功能介绍

Guardian位于AI的决策与实际执行之间，自动评估风险，并将具有危险性的操作转发给独立的Guardian代理进行基于投票的审批。

**95%的操作可以立即通过**（无延迟、无成本）；只有约5%的潜在危险操作会触发Guardian的审核。

## 架构

```
Tool Call → Risk Assessor (keyword rules, 0ms)
              ↓
   Score 0-30  → Fast Lane (just execute)
   Score 31-70 → Light Review (1 Guardian, ~1-2s)
   Score 71-100 → Full Vote (3 Guardians, ~2-4s, majority rules)
```

### Guardian的审核维度（全权投票）

| 审核维度        | 重点关注的内容                                      |
|-----------------|----------------------------------------------------|
| 安全性          | 操作的破坏性潜力、系统恢复能力                          |
| 隐私          | 用户凭证、API密钥、个人数据                               |
| 权限            | 用户的授权范围                                    |
| 可逆性          | 操作的可撤销性、影响范围                                |
| 全面性          | 从多个角度进行审核（适用于“快速审核”模式）                        |

## 安装步骤

1. 将插件克隆到您的OpenClaw工作空间中：

```bash
cd ~/.openclaw/workspace
git clone https://github.com/fatcatMaoFei/openclaw-guardian.git
```

2. 在`openclaw.json`文件中注册该插件：

```json
{
  "plugins": {
    "load": {
      "openclaw-guardian": {
        "path": "workspace://openclaw-guardian",
        "enabled": true
      }
    }
  }
}
```

3. 重启OpenClaw网关。

## 配置方法

编辑`default-policies.json`文件以启用或禁用该插件：

```json
{ "enabled": true }
```

## 文件结构

- `index.ts` — 入口文件；注册`before_tool_call`钩子
- `src/blacklist.ts` — 用于风险评分的关键词规则引擎
- `src/llm-voter.ts` — 分层式LLM投票系统（支持并行执行）
- `src/audit-log.ts` — 基于SHA-256哈希链的审计日志记录器
- `openclaw.plugin.json` — 插件配置文件
- `default-policies.json` — 默认风险策略（可用户自定义）

## 代币成本

| 审核模式        | 占操作总数的百分比 | 额外费用                    |
|--------------|-----------------|---------------------------|
| 快速审核模式      | 85-95%       | 0（仅基于规则）                    |
| 快速审核模式      | 5-10%       | 每次审核约500个代币                |
| 全权审核模式      | 1-3%       | 每次审核约1500个代币                |

平均开销：约占总代币使用量的15-35%。

## 许可证

MIT许可证