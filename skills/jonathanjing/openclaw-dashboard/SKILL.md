---
name: openclaw-dashboard
description: OpenClaw的实时操作控制面板：用于监控会话、费用、定时任务以及网关的运行状态。在安装控制面板、启动服务器、添加新功能、更新`api-server.js`中的路由配置或修改`agent-dashboard.html`文件时，请使用该面板。该面板支持语言切换（英语/中文），并配有24小时运行的状态指示条以及费用分析功能。
version: "1.5.0"
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["node", "openclaw"] },
        "optionalRequires":
          {
            "config": ["gateway.authToken"],
            "env": ["OPENCLAW_AUTH_TOKEN"],
          },
        "optionalEnv":
          [
            "OPENCLAW_HOOK_TOKEN",
            "OPENCLAW_LOAD_KEYS_ENV",
            "OPENCLAW_KEYS_ENV_PATH",
            "OPENCLAW_ENABLE_PROVIDER_AUDIT",
            "OPENCLAW_ENABLE_CONFIG_ENDPOINT",
            "OPENCLAW_ENABLE_SESSION_PATCH",
            "OPENCLAW_ALLOW_ATTACHMENT_FILEPATH_COPY",
            "OPENCLAW_ALLOW_ATTACHMENT_COPY_FROM_TMP",
            "OPENCLAW_ALLOW_ATTACHMENT_COPY_FROM_WORKSPACE",
            "OPENCLAW_ALLOW_ATTACHMENT_COPY_FROM_OPENCLAW_HOME",
            "OPENCLAW_ENABLE_SYSTEMCTL_RESTART",
            "OPENCLAW_ENABLE_MUTATING_OPS",
            "NOTION_API_KEY",
            "OPENAI_ADMIN_KEY",
            "ANTHROPIC_ADMIN_KEY",
            "VISION_DB_NETWORKING",
            "VISION_DB_WINE",
            "VISION_DB_CIGAR",
            "VISION_DB_TEA",
          ],
      },
  }
---
# OpenClaw 仪表板技能

## 任务目标

确保该仓库的安全性，并便于使用。优先考虑以下方面：
1. 对敏感数据进行加密处理
2. 减少设置步骤
3. 保持 API 和用户界面的稳定性

## 适用场景

此技能适用于以下场景：
- 仪表板功能的请求（会话管理、费用统计、定时任务、监控机制、操作管理等）
- `api-server.js` 中的后端路由更新
- `agent-dashboard.html` 中的前端界面更新
- `README.md`、设置指南及环境配置的简化
- 公开发布前的敏感数据检查

## 安全性防护措施

- 绝不要将令牌、API 密钥、cookie 或特定于主机的敏感信息硬编码到代码中。
- 绝不要提交与特定机器相关的绝对路径。
- 建议使用 `process.env.*` 及基于 `HOME` 变量的安全默认值。
- 将示例代码中的敏感信息替换为占位符（例如 `your_token_here`、`/path/to/...`）。
- 如果不确定如何处理敏感信息，请先进行屏蔽处理，再征得用户同意后再公开详细信息。
- 确保敏感功能的启用是用户主动选择的（不要自动加载本地敏感文件）。

## 运行时访问权限

打包好的服务器可以访问以下本地 OpenClaw 文件以生成仪表板视图：
- 会话数据、定时任务信息、监控状态（位于 `~/.openclaw/...` 目录下）
- 本地工作区文件（位于 `OPENCLAW_WORKSPACE` 目录下）
- 仓库中的任务附件（位于 `attachments/` 目录下）

**凭据要求**（默认为可选）：
- `OPENCLAW_AUTH_TOKEN` 是可选的，但在向外部服务暴露接口时建议使用。
- `gateway.authToken` 是可选的配置项，但不是强制安装的要求。

**高敏感度功能的启用方式**（默认为禁用状态，需要通过环境变量进行配置）：
- `OPENCLAW_LOAD_KEYS_ENV=1`：用于加载 `keys.env` 文件
- `OPENCLAW_ENABLE_PROVIDER_AUDIT=1`：用于调用 OpenAI/Anthropic 的相关 API
- `OPENCLAW ENABLE_CONFIG_ENDPOINT=1`：用于暴露 `/ops/config` 端点
- `OPENCLAW_ALLOWAttachment_FILEPATH_COPY=1`：允许复制附件文件路径
- `OPENCLAW_ALLOWAttachment_COPY_FROM_TMP=1`：允许从 `/tmp` 目录复制文件
- `OPENCLAW_ALLOWAttachment_COPY_FROM_WORKSPACE=1`：允许从工作区路径复制文件
- `OPENCLAW_ALLOWAttachment_COPY_FROM_OPENCLAW_HOME=1`：允许从 `~/.openclaw` 目录复制文件
- `OPENCLAW_ENABLE_SYSTEMCTL_RESTART=1`：允许用户重启系统服务
- `OPENCLAW ENABLE_MUTATING_OPS=1`：允许执行修改操作（如 `/backup*`、`/ops/update-openclaw`、`/ops/*-model`、`cron run-now`）

**网络安全措施**：
- 默认情况下，CORS（跨源资源共享）仅允许来自本地主机的请求（不允许使用通配符 `*`）。
- 可通过设置 `DASHBOARD_CORS_ORIGINS`（用逗号分隔）来允许特定的外部来源访问。
- 通过 `HttpOnly` cookie（`ds`）或 `?token=` 查询参数来验证认证令牌。
- 更推荐使用 cookie 进行认证；URL 中的令牌参数仅用于与旧版服务器监控脚本的兼容性。
- 当向外部服务（如 Tailscale Funnel）暴露功能时，必须设置 `OPENCLAW_AUTH_TOKEN`。

**提示安全性的注意事项**：
- 将定时任务或操作任务的输入内容视为不可信的数据。
- 保持提示信息的结构化（使用 JSON 格式），避免直接插入命令。
- 所有的 `child_process` 调用都应使用 `execFileSync` 方法（传递参数数组，避免使用 shell 解释器）。
- 在复制文件路径时，需要处理符号链接（使用 `realpathSync` 进行路径验证）。

## 默认实现流程

1. 确定受影响的模块（API、用户界面、文档或配置文件）。
2. 实施最小范围的修改，同时保持原有功能不变。
3. 在最终确定修改内容之前，快速扫描敏感字符串。
4. 确保文档内容与实际运行时的默认设置一致。
5. 报告所有对用户可见的修改内容以及任何需要手动验证的步骤。

## 敏感数据检查

在返回最终响应之前，需检查以下内容：
- `token=`, `OPENCLAW_AUTH_TOKEN`, `OPENCLAWHOOK_TOKEN`
- `API_KEY`, `SECRET`, `PASSWORD`, `COOKIE`
- 如 `/Users/`, `C:\\`, 机器名称、个人电子邮件地址等绝对路径

如果发现敏感信息：
- 用环境变量或占位符替换这些内容。
- 在结果中说明对敏感数据进行了哪些处理。

## 配置简化规则

- 将必需的环境变量保持最少且明确无误。
- 将可选的环境变量分类并明确标注。
- 提供一个可以直接复制的启动命令。
- 除非确实需要，否则避免使用复杂的工具链进行配置。

**最常需要修改的文件**：
- `api-server.js`：服务器行为和 API 路由配置
- `agent-dashboard.html`：用户界面和客户端交互逻辑
- `README.md`：快速入门指南和操作员文档
- `.env.example`：安全的环境配置模板