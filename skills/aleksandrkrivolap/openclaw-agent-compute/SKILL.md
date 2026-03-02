---
name: openclaw-agent-compute
description: "这是一个公开提供的HTTP客户端技能，它通过HTTPS调用私有的计算网关（Compute Gateway）来使用各种计算工具（compute.* tools）。该技能附带了一个启动套件（starter kit），其中预先配置好了OpenClaw，用户可以直接使用该套件来运行OpenClaw。"
---
# openclaw-agent-compute

这是一个面向代理的公共技能，它通过**HTTPS**调用**私有的**计算网关（Compute Gateway）来提供`compute.*`工具的接口。

## 环境配置

- `MCP_COMPUTE_URL`（例如：`https://compute.example.com`）
- `MCP_COMPUTE_API_KEY`

请复制`skills/openclaw-agent-compute/.env.example`文件以配置这些环境变量。

## 工具/API接口要求

该客户端要求私有计算网关实现以下接口：
- `POST /v1/sessions`（创建会话）
- `POST /v1/exec`（执行命令）
- `GET /v1/usage/{session_id}`（查询会话使用情况/费用）
- `DELETE /v1/sessions/{session_id}`（销毁会话）

## 脚本

- HTTP客户端脚本：`skills/openclaw-agent-compute/scripts/client.js`
- 示例脚本：`skills/openclaw-agent-compute/scripts/example_exec.js`

### 本地测试

```bash
cp skills/openclaw-agent-compute/.env.example .env
# edit .env
npm i
npm run example:exec
```

## 启动套件

请参考`skills/openclaw-agent-compute/starter-kit/`。

在该套件中，可以通过`OPENCLAW_IMAGE`配置来覆盖默认的OpenClaw镜像，直到官方镜像或标签被正式确定为止。