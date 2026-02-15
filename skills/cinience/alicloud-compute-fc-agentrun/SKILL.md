---
name: alicloud-compute-fc-agentrun
description: 通过 OpenAPI 管理 Function Compute AgentRun 的资源（包括运行时环境、沙箱环境、模型、内存使用情况以及认证信息）。该接口可用于创建运行时环境/端点、查询工作流程的状态以及排查 AgentRun 相关的故障。
---

**类别：服务**

# Function Compute AgentRun (OpenAPI)**

使用 `AgentRun` OpenAPI（ROA）来管理运行时环境、沙箱、模型服务、内存以及凭据。

## 前提条件**

- 通过 RAM 用户（具有最低权限）获取 `AccessKey`。
- 选择正确的区域端点（请参阅 `references/endpoints.md`）。如果不确定，请为任务选择最合适的区域，或咨询相关用户。
- 使用 OpenAPI Explorer 或官方 SDK 以避免手动签名（ROA 需要使用 SignatureV1）。

## 工作流程**

1. 选择区域端点（格式：`agentrun.cn-<region>.aliyuncs.com`）。
2. 创建运行时环境 → 发布版本 → 创建运行时端点。
3. （如需要）创建沙箱或模板。
4. 根据要求配置凭据和模型服务。
5. 查询资源以进行故障排查。

## API 组

请参阅 `references/api_overview.md` 以获取完整的 API 列表和分组信息。

## 脚本快速入门

```bash
python skills/compute/fc/alicloud-compute-fc-agentrun/scripts/quickstart.py
```

**环境变量：**
- `AGENTRUN_ENDPOINT`
- `ALICLOUD_ACCESS_KEY_ID`
- `ALICLOUD_ACCESS_KEY_SECRET`
- `OUTPUT_DIR`（可选）

## 运行时环境脚本

```bash
AGENTRUN_RUNTIME_NAME="my-runtime" \\
AGENTRUN_RUNTIME_ENDPOINT_NAME="my-runtime-endpoint" \\
python skills/compute/fc/alicloud-compute-fc-agentrun/scripts/runtime_flow.py
```

**环境变量：**
- `AGENTRUN_ENDPOINT`
- `ALICLOUD_ACCESS_KEY_ID`
- `ALICLOUD_ACCESS_KEY_SECRET`
- `AGENTRUN_RUNTIME_NAME`
- `AGENTRUN_RUNTIME_ENDPOINT_NAME`
- `AGENTRUN_RUNTIME_DESC`（可选）
- `OUTPUT_DIR`（可选）

## 清理脚本

```bash
AGENTRUN_RUNTIME_ID="runtime-id" \\
AGENTRUN_RUNTIME_ENDPOINT_ID="endpoint-id" \\
python skills/compute/fc/alicloud-compute-fc-agentrun/scripts/cleanup_runtime.py
```

**环境变量：**
- `AGENTRUN_ENDPOINT`
- `ALICLOUD_ACCESS_KEY_ID`
- `ALICLOUD_ACCESS_KEY_SECRET`
- `AGENTRUN_RUNTIME_ID`
- `AGENTRUN_RUNTIME_ENDPOINT_ID`
- `OUTPUT_DIR`（可选）

## SDK 说明**

请参阅 `references/sdk.md` 以获取 SDK 的获取指南。

## 输出路径

如果您存储了任何生成的文件或响应，请将它们保存在以下路径下：
`output/compute-fc-agentrun/`

## 参考资料**

- API 概述和操作列表：`references/api_overview.md`
- 区域端点：`references/endpoints.md`
- SDK 使用指南：`references/sdk.md`
- 源代码列表：`references/sources.md`