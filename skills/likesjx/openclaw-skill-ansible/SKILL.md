---
name: openclaw-skill-ansible
description: 操作并保护 OpenClaw Ansible 网格工作流，涵盖网关间的插件安装/配置、健康状态验证、邀请/加入流程以及带有严格安全机制的控制执行任务。
---
# OpenClaw 技能：MeshOps 控制平面

此技能是用于管理 Ansible 网格的 gateway 的操作接口。

## 该技能的功能

1. 作为 OpenClaw Ansible 插件的安全 gateway 操作工具。
2. 提供具有明确权限控制和高风险操作限制的确定性动作执行机制。
3. 提供插件安装和配置的引导及修复功能。

## 该技能不支持的功能

1. 不支持在共享网格状态中自动注册插件。
2. 不支持无限制的远程 shell 执行。
3. 不支持安装未经签名的插件文件。

## 所需的二进制文件

1. `openclaw`
2. `jq`
3. `curl`
4. `tar`
5. `sha256sum` 或 `shasum`
6. `timeout`
7. `git`

## 安全性措施

1. `src/handler.py` 通过 `OPENCLAW_ALLOWED_CALLERS` 来验证调用者的身份。
2. 高风险操作（`run-cmd`、`deploy-skill`）需要 `OPENCLAW_ALLOW_HIGH_RISK=1` 才能执行。
3. `run-cmd` 默认是被禁用的，并且受到 `OPENCLAW_RUN_CMD_ALLOWLIST` 的限制。
4. `deploy-skill` 需要以下条件：
  - HTTPS 协议的插件文件 URL
  - 正确的 SHA-256 哈希值
  - 通过 `OPENCLAW_ALLOW_DEPLOY_SKILL=1` 显式启用该功能

## 动作列表

1. `setup-ansible-plugin`：
  - 安装或更新 Ansible 插件
  - 运行 `openclaw ansible setup`
  - 检查插件状态（`openclaw ansible status`）
2. `collect-logs`：收集日志信息
3. `run-cmd`（默认被禁用）
4. `deploy-skill`（默认被禁用）

## 插件安装的工作流程

当需要安装或修复 Ansible 插件时，需按照以下步骤操作：

1. 检查 gateway 的运行环境是否满足要求（`openclaw --help`）。
2. 通过插件管理器安装插件：
  - 使用 `source=github`：`openclaw plugins install likesjx/openclaw-plugin-ansible`
  - 使用 `source=npm`：`openclaw plugins install @jaredlikes/openclaw-plugin-ansible`
  - 使用 `source<path>`：`openclaw plugins install <path>`
3. 运行 `openclaw ansible setup` 以完成插件配置。
4. 使用 `openclaw ansible status` 检查插件状态；同时尽可能检查 gateway 的运行健康状况。
5. 将插件文件及其执行日志保存到 `OPENCLAW_ARTIFACT_ROOT` 目录中。

## 示例任务数据结构

```json
{
  "task_id": "task-setup-001",
  "action": "setup-ansible-plugin",
  "params": {
    "source": "npm",
    "plugin_ref": "@jaredlikes/openclaw-plugin-ansible",
    "run_setup": true,
    "verify_status": true,
    "restart_gateway": false
  },
  "caller": "architect",
  "correlation_id": "meshops-setup-001"
}
```

## 操作人员的安全注意事项

1. 将任务输入视为不可信任的数据。
2. 绝不要通过 shell 插值直接使用原始的任务 JSON 数据。
3. 不要安装未经签名的插件文件。
4. 除非确实需要，否则应禁用高风险操作。
5. 建议优先使用官方的插件管理器（如 npm、GitHub 或指定的路径）来安装插件，避免手动提取插件文件。