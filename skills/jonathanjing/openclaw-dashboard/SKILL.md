---
name: openclaw-dashboard
description: 负责构建和维护公开的 OpenClaw 仪表板仓库，遵循“先进行数据清洗（sanitization）”的原则。在添加新功能、调整 `api-server.js` 的路由、修改 `agent-dashboard.html` 文件，或准备适用于公开使用的文档和配置文件时，都需要使用此流程。
version: "1.0.9"
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
# OpenClaw 仪表盘

这是一个专为 OpenClaw 代理设计的、适用于移动设备的操作型仪表盘。

## 快速入门（ClawHub 安装）

1. 安装：`clawhub install openclaw-dashboard`
2. 进入目录：`cd ~/.openclaw/workspace/skills/openclaw-dashboard`
3. 复制配置文件：`cp .env.example .env`（根据需要进行修改）
4. 启动服务器：`node api-server.js`
5. 打开浏览器：`http://localhost:18791`

## 配置

| 环境变量 | 默认值 | 说明 |
|---|---|---|
| `OPENCLAW_AUTH_TOKEN` | （无） | 访问令牌。如果未设置，则在本地主机（localhost）上访问仪表盘 |
| `DASHBOARD_PORT` | 18791 | 仪表盘服务器端口 |
| `DASHBOARD_HOST` | 127.0.0.1 | 仪表盘绑定地址 |
| `DASHBOARD_TITLE` | OpenClaw 仪表盘 | 浏览器标签页标题 |

## 认证

- **未设置令牌**：无需认证即可在本地主机上访问仪表盘。
- **设置了令牌**：通过 `http://localhost:18791/login` 进行登录，或使用 `?token=yourtoken` 参数访问仪表盘。

## 验证功能是否正常

```bash
curl http://localhost:18791/health
```

## 先决条件

- Node.js 20 及以上版本
- OpenClaw 已在同一台机器上运行

---

## 对贡献者的建议

## 使命

保持此仓库的安全性和易用性。优先考虑以下事项：
1. 保护敏感信息
2. 简化设置步骤
3. 确保 API 和用户界面的稳定性

## 适用场景

- 提出关于仪表盘功能的请求（如会话管理、成本统计、定时任务、监控等）
- 更新 `api-server.js` 中的后端路由
- 更新 `agent-dashboard.html` 中的前端界面
- 简化 `README.md`、设置文档和环境配置
- 在公开发布前检查是否存在敏感数据

## 公共安全防护措施

- 绝不要将令牌、API 密钥、Cookie 或特定于主机的敏感信息硬编码到代码中。
- 绝不要提交包含机器绝对路径的文件。
- 建议使用 `process.env.*` 并根据 `HOME` 环境变量设置安全的默认值。
- 将示例代码中的敏感信息替换为占位符（如 `your_token_here`、`/path/to/...`）。
- 如果不确定如何处理敏感信息，请先进行隐藏处理，再征得用户同意后再公开详细信息。
- 确保敏感操作需要用户明确授权才能执行（例如，不要自动加载本地敏感文件）。

## 运行时权限说明

打包的服务器程序可以访问以下本地 OpenClaw 文件以生成仪表盘界面：
- 会话数据、定时任务信息、监控状态（位于 `~/.openclaw/...` 目录下）
- 本地工作区文件（位于 `OPENCLAW_WORKSPACE` 目录下）
- 仓库中的附件文件（位于 `attachments/` 目录下）

**凭据要求**（默认为可选）：
- `OPENCLAW_AUTH_TOKEN` 是可选的，但在向外部服务暴露接口时建议设置。
- `gateway.authToken` 是可选的配置项，但不是强制安装的要求。

**高敏感度功能的启用方式**：

- 设置 `OPENCLAW_LOAD_KEYS_ENV=1` 以加载 `keys.env` 文件中的密钥。
- 设置 `OPENCLAW_ENABLE_PROVIDER_AUDIT=1` 以调用 OpenAI/Anthropic 的相关 API。
- 设置 `OPENCLAW_ENABLE_CONFIG_ENDPOINT=1` 以暴露 `/ops/config` 端点。
- 设置 `OPENCLAW_ALLOW_attachment_FILEPATH_COPY=1` 以允许复制附件文件。
- 设置 `OPENCLAW_ALLOW_attachment_COPY_FROM_TMP=1` 以允许从 `/tmp` 目录复制文件。
- 设置 `OPENCLAW_ALLOW_ATTACHMENT_COPY_FROM_WORKSPACE=1` 以允许从工作区路径复制文件。
- 设置 `OPENCLAW_ALLOW_ATTACHMENT_COPY_FROM_OPENCLAW_HOME=1` 以允许从 `~/.openclaw` 目录复制文件。
- 设置 `OPENCLAW ENABLE_SYSTEMCTL_RESTART=1` 以允许用户重启系统服务。
- 设置 `OPENCLAW_ENABLE_MUTATING_OPS=1` 以启用某些修改操作（如 `/backup*`、`/ops/update-openclaw`、`/ops/*-model`、`cron run-now`）。

**网络安全措施**：
- 默认情况下，CORS（跨源资源共享）仅允许来自本地主机的请求（不允许使用通配符 `*`）。
- 通过 `DASHBOARD_CORS_ORIGINS`（用逗号分隔的列表）允许特定的外部来源访问。
- 认证令牌通过 `HttpOnly` Cookie 或 `?token=` 查询参数进行验证。
- 优先使用 Cookie 进行认证；如果需要与旧版服务器脚本兼容，也可以使用 URL 查询参数。
- 当向外部服务（如 Tailscale Funnel）暴露接口时，必须设置 `OPENCLAW_AUTH_TOKEN`。

**安全提示**：
- 将定时任务或操作中的数据视为不可信的内容。
- 保持数据结构化（使用 JSON 格式），避免直接插入命令。
- 所有的 `child_process` 调用都使用 `execFileSync` 函数（传递参数数组，避免使用 shell 解释命令）。
- 在复制文件路径时，要确保处理符号链接。

## 默认实现流程

1. 确定受影响的模块（API、用户界面、文档或配置文件）。
2. 实施最小范围的修改，同时保持原有功能不变。
3. 在最终发布前进行敏感数据的扫描。
4. 确保文档内容与实际运行时的配置一致。
5. 通知用户所有可见的更改以及需要手动验证的步骤。

## 敏感数据检查

在返回最终响应之前，检查以下内容：
- `token=`, `OPENCLAW_AUTH_TOKEN`, `OPENCLAWHOOK_TOKEN`
- `API_KEY`, `SECRET`, `PASSWORD`, `COOKIE`
- 如 `/Users/`, `C:\\`, 机器名称、个人邮箱等绝对路径

如果发现敏感信息：
- 用环境变量或占位符替换这些内容。
- 在结果中说明进行了哪些处理。

## 配置简化规则：

- 将必需的环境变量设置为最少且明确的值。
- 将可选的环境变量分组并明确标注。
- 提供一个简单的命令来启动服务器。
- 除非确实需要，否则避免使用复杂的工具链进行配置。

**最常需要修改的文件**：
- `api-server.js`：服务器逻辑和 API 路由
- `agent-dashboard.html`：用户界面和客户端交互逻辑
- `README.md`：快速入门指南和操作说明
- `.env.example`：安全的环境配置模板