# Claw 权限防火墙

这是一个用于代理/技能操作的运行时最小权限防火墙。它会评估请求的操作，并返回以下三种结果之一：

- **ALLOW**（允许执行）
- **DENY**（被策略禁止）
- **NEED_CONFIRMATION**（存在风险；需要用户明确确认）

此外，它还会返回一个已处理敏感信息的操作结果（`sanitizedAction`），以及一个结构化的审计记录。

> 这不是一个用于加固网关的工具，而是通过在运行时执行针对每个操作的策略来补充网关安全扫描器的功能。

---

## 防护内容：
- 防止数据泄露到未知域名
- 防止通过提示框进行秘密信息注入的尝试（检测并隐藏敏感信息）
- 防止读取敏感的本地文件（如 `~/.ssh`、`~/.aws`、`.env` 等）
- 防止不安全的执行方式（如 `rm -rf`、`curl | sh` 等）

---

## 输入：
提供一个需要评估的操作对象：

```json
{
  "traceId": "optional-uuid",
  "caller": { "skillName": "SomeSkill", "skillVersion": "1.2.0" },
  "action": {
    "type": "http_request | file_read | file_write | exec",
    "method": "GET|POST|PUT|DELETE",
    "url": "https://api.github.com/...",
    "headers": { "authorization": "Bearer ..." },
    "body": "...",
    "path": "./reports/out.json",
    "command": "rm -rf /"
  },
  "context": {
    "workspaceRoot": "/workspace",
    "mode": "strict | balanced | permissive",
    "confirmed": false
  }
}
```

---

## 输出：
```json
{
  "decision": "ALLOW | DENY | NEED_CONFIRMATION",
  "riskScore": 0.42,
  "reasons": [{"ruleId":"...","message":"..."}],
  "sanitizedAction": { "...": "..." },
  "confirmation": { "required": true, "prompt": "..." },
  "audit": { "traceId":"...", "policyVersion":"...", "actionFingerprint":"..." }
}
```

---

## 默认策略行为（v1）：
- 默认情况下，执行操作是被禁用的。
- HTTP 请求必须使用 TLS 协议。
- 黑名单会阻止常见的数据泄露目标域名（如剪贴板、原始脚本执行服务器）。
- 文件访问被限制在 `workspaceRoot` 目录内。
- `Authorization`、`Cookie`、`X-API-Key` 以及常见的令牌信息都会被隐藏。

---

## 推荐使用流程：
1) 你的技能创建一个操作对象。
2) 调用此技能来评估该操作。
3) 如果返回 **ALLOW**，则执行处理后的操作结果（`sanitizedAction`）。
4) 如果返回 **NEED_CONFIRMATION**，则请求用户确认，然后重新运行该操作并设置 `context.confirmed=true`。
5) 如果返回 **DENY**，则停止操作并显示拒绝原因。

---

## 相关文件：
- `policy.yaml` 文件中包含策略配置（请根据你的环境进行修改）。