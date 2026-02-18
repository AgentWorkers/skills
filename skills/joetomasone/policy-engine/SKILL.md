---
name: policy-engine
description: OpenClaw 工具执行的确定性治理层：通过 `before_tool_call` 钩子来执行工具允许列表、拒绝模式、路径允许列表、风险等级、Dry-Run 模式以及升级跟踪等操作。所有决策都会被记录下来以供审计。该系统经过了 88 次测试的严格验证，并修复了三个可能导致死锁的问题（deadlock issues）。
tags: [security, governance, policy, tools, audit]
type: plugin
---
# 政策引擎（Policy Engine）

这是一个确定性的治理层，它会拦截 `before_tool_call` 事件，以控制代理可以使用的工具、阻止危险命令、执行写路径限制，并对每个操作进行审计。

## 安装

```bash
clawhub install policy-engine
```

然后在您的 `openclaw.json` 文件中启用该功能：

```jsonc
{
  "plugins": {
    "policy-engine": {
      "enabled": true
    }
  }
}
```

## 快速入门

**最小限制配置**——将子代理限制为仅能使用只读工具：

```jsonc
{
  "plugins": {
    "policy-engine": {
      "enabled": true,
      "allowlists": {
        "readonly": ["read", "web_fetch", "web_search", "message"]
      },
      "routing": {
        "research-agent": { "toolProfile": "readonly" }
      }
    }
  }
}
```

## 功能

### 工具允许列表（Tool Allowlists）
为每个代理配置允许使用的工具。通过基于代理 ID 的 `routing` 规则来分配相应的配置文件。

### 拒绝模式（Deny Patterns）
内置的模式可以阻止以下操作：创建分叉炸弹文件、执行 `rm -rf` 命令、创建文件系统（`mkfs`）、擦除磁盘数据以及写入系统路径。这些模式只会检查相关参数（例如，执行命令时会检查 `command`，写入操作时会检查 `path`），而不会检查文件内容。您还可以为特定工具添加自定义的拒绝模式。

### 路径允许列表的执行（Path Allowlist Enforcement）
使用 `path.resolve()` 方法对文件路径进行规范化处理，然后检查路径是否属于允许的目录前缀。这样可以防止路径遍历攻击（例如，通过提示注入尝试访问 `/etc/passwd`）。

```jsonc
{
  "pathAllowlists": {
    "write": ["/Users/joe/.openclaw/workspace"],
    "edit": ["/Users/joe/.openclaw/workspace"]
  }
}
```

使用以下配置：
- 写入 `/Users/joe/.openclaw/workspace/foo.txt` 是允许的。
- 写入 `/Users/joe/.openclaw/workspace/../../etc/hosts` 会被**阻止**（因为路径超出了允许的目录前缀）。

### 风险等级（Risk Tiers）
- **T0**——只读（读取、网络请求、搜索）——始终允许，即使在权限升级的情况下也是如此。
- **T1**——写入（写入、编辑、发送消息）。
- **T2**——执行系统命令（执行系统命令、使用浏览器、部署应用程序）。

您可以使用 `riskTiers` 对象来覆盖这些默认设置：

```jsonc
{ "riskTiers": { "my_custom_tool": "T2" } }
```

### 干运行模式（Dry-Run Mode）
在不会阻止任何操作的情况下测试政策配置。关键工具（如发送消息、访问网关、获取会话状态）始终能够通过，以防止代理陷入死锁。

```jsonc
{ "dryRun": true, "dryRunAllowT0": true }
```

### 升级跟踪（Escalation Tracking）
记录每个会话中被阻止的尝试次数。当达到 `maxBlockedRetries`（默认值：3）次后，非关键操作将被阻止，并显示一条提示信息。

### 热重载（Hot-Reload）
通过 `gateway config.patch` 修改配置后，更改会立即生效——无需重启系统。

### 错误时继续执行（Fail-Open on Error）
如果政策引擎本身出现故障，工具调用仍会继续执行。在这种情况下，安全性优先于系统的正常运行。

### 紧急情况下的绕过机制（Break-Glass）
将 `OPENCLAW_POLICY_BYPASS` 设置为 `1` 可以绕过所有检查。此操作会被记录为警告，用于审计。

## 配置参考

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `enabled` | 布尔值 | `true` | 全局启用/禁用该功能 |
| `dryRun` | 布尔值 | `false` | 仅记录日志模式（不阻止任何操作） |
| `dryRunAllowT0` | 布尔值 | 在干运行模式下允许使用 T0 级别的工具 |
| `dryRunEssentialTools` | 字符串数组 | `[message, gateway, session_status, sessions_send, sessions_list, tts]` | 在干运行模式下始终允许使用的工具 |
| `maxBlockedRetries` | 数字 | `3` | 每个会话的允许尝试次数上限 |
| `riskTiers` | 对象 | `{}` | 定义工具对应的风险等级（T0、T1、T2） |
| `denyPatterns` | 对象 | `{}` | 被禁止的命令参数模式 |
| `allowlists` | 对象 | `{}` | 允许使用的工具名称列表 |
| `routing` | 对象 | `{}` | 根据代理 ID 分配工具配置的规则 |
| `pathAllowlists` | 对象 | `{}` | 允许的目录前缀列表 |

## 常见配置示例

### 限制子代理的权限（Restrictive Sub-Agent）

```jsonc
{
  "allowlists": {
    "researcher": ["read", "web_fetch", "web_search", "message"],
    "coder": ["read", "write", "edit", "exec", "message"]
  },
  "routing": {
    "research-bot": { "toolProfile": "researcher" },
    "code-bot": { "toolProfile": "coder" }
  }
}
```

### 阻止危险命令及自定义拒绝模式（Block Dangerous Commands + Custom Patterns）

```jsonc
{
  "denyPatterns": {
    "exec": ["npm publish", "docker push"],
    "write": ["/secrets/", "/credentials/"]
  }
}
```

### 干运行测试（Dry-Run Testing）
启用干运行模式，以便在正式应用规则之前查看哪些操作会被阻止：

```jsonc
{ "dryRun": true }
```

检查日志中是否包含 `[policy-engine] DRYRUN` 的记录，确认无误后即可关闭此模式。

### 基于代理的路由配置（Per-Agent Model Routing）

```jsonc
{
  "routing": {
    "cheap-tasks": { "model": "ollama/qwen2.5:latest" },
    "complex-tasks": { "model": "anthropic/claude-opus-4", "toolProfile": "full" }
  }
}
```

## `/policy` 命令
该插件支持以下 `/policy` 命令：
- `/policy status` — 显示当前配置和会话状态。
- `/policy reset` — 重置错误计数器。

## 架构（Architecture）
有关详细的设计决策、死锁分析以及开发过程中发现的并修复的死锁问题，请参阅 [DESIGN.md](DESIGN.md)。