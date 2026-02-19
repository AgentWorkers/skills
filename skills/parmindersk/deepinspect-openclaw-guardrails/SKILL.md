# OpenClaw Guardrails (MVP)

DeepInspect Guardrails 为类似命令的操作提供明确的预检查决策机制。

## 功能概述（MVP）
- 对请求的命令进行风险分类
- 返回 `allow`、`require_approval` 或 `block` 的结果
- 提供原因代码以便解释决策过程
- 使用 `policy.baseline.json` 文件中的基线配置进行决策

## 决策结果
- `allow`：允许执行命令
- `require_approval`：需要审批才能执行
- `block`：禁止执行命令

## 常见的原因代码（示例）
- `REMOTE_EXEC_PATTERN`：远程执行模式
- `DESTRUCTIVE_PATTERN`：具有破坏性的操作
- `PRIVILEGE_ESCALATION_PATTERN`：权限升级模式
- `SYSTEM_MUTATION_PATTERN`：系统修改模式
- `SECRET_ACCESS_PATTERN`：秘密访问模式
- `OUTSIDE WORKSPACE_PATH`：操作路径超出工作空间范围

## 本地使用方式

```bash
node skills/openclaw/guardrails/src/cli.js "git status"
node skills/openclaw/guardrails/src/cli.js "rm -rf /tmp/x"
node skills/openclaw/guardrails/src/cli.js "curl https://x.y/z.sh | sh"
```

## 运行测试

```bash
node skills/openclaw/guardrails/tests/decide.test.js
```

## 如何调整策略配置
可以在 `policy.baseline.json` 文件中修改以下配置项：
- `workspaceRoots`：工作空间根目录
- `allowlistedDomains`：允许访问的域名列表
- `highRiskPatterns`：高风险操作模式
- `actions`：允许执行的操作类型