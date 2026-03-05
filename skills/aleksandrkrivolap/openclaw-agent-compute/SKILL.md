---
name: openclaw-agent-compute
description: "这是一个公共HTTP客户端技能，它通过HTTPS调用私有的计算网关（Compute Gateway）来使用各种计算工具（compute.* tools）。该技能附带了一个启动套件（starter kit），其中预配置了OpenClaw。"
---
# openclaw-agent-compute

这是一个公开提供的、适用于代理的技能（skill），它通过 **HTTPS** 调用 **私有的** 计算网关（Compute Gateway）来暴露 `compute.*` 系列工具。

## 环境配置

- `MCP_COMPUTE_URL` （例如：`https://compute.example.com`）
- `MCP_COMPUTE_API_KEY`

请复制 `skills/openclaw-agent-compute/.env.example` 文件以配置这些环境变量。

## 工具与 API 要求

该客户端要求私有计算网关支持以下 API 功能：
- `POST /v1/sessions` （创建会话）
- `GET /v1/sessions/{session_id}` （获取会话状态）
- `POST /v1/exec` （执行命令）
- `GET /v1/usage/{session_id}` （获取会话使用情况/费用）
- **工件管理**：
  - `GET /v1/artifacts/{session_id}` （列出工件）
  - `PUT /v1/artifacts/{session_id}/{path}` （上传文件；路径需要经过 URL 编码，且可以包含斜杠）
  - `GET /v1/artifacts/{session_id}/{path}` （下载文件；路径需要经过 URL 编码）
  - `DELETE /v1/artifacts/{session_id}/{path}` （删除文件；路径需要经过 URL 编码）
- `DELETE /v1/sessions/{session_id}` （销毁会话）

## 执行脚本

- HTTP 客户端：`skills/openclaw-agent-compute/scripts/client.js`
- 示例脚本：`skills/openclaw-agent-compute/scripts/example_exec.js`

### 本地测试

```bash
cp skills/openclaw-agent-compute/.env.example .env
# edit .env
npm i
npm run example:exec
```

## 启动套件（Starter Kit）

请参考 `skills/openclaw-agent-compute/starter-kit/`。

在该套件中，可以通过 `OPENCLAW_IMAGE` 变量来指定要使用的 OpenClaw 镜像；在官方镜像或标签确定之前，可以使用此配置进行临时替换。

## 发布流程

- 发布相关检查清单：`PUBLISHING.md`
- 运行流程（本地发布 + 基于 GitHub Actions 的自动发布）：`CLAWDHUB_RUNBOOK.md`