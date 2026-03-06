---
name: theta-edgecloud-skill
description: 运行时安全的 Theta EdgeCloud 云 API 框架（支持部署、推理、视频处理及按需服务），并具备干运行（dry-run）安全功能。
metadata:
  openclaw:
    primaryEnv: THETA_EC_API_KEY
    requires:
      env:
        - THETA_EC_API_KEY
        - THETA_EC_PROJECT_ID
        - THETA_INFERENCE_ENDPOINT
        - THETA_INFERENCE_AUTH_USER
        - THETA_INFERENCE_AUTH_PASS
        - THETA_ONDEMAND_API_TOKEN
        - THETA_VIDEO_SA_ID
        - THETA_VIDEO_SA_SECRET
        - THETA_DRY_RUN
        - THETA_HTTP_TIMEOUT_MS
        - THETA_HTTP_MAX_RETRIES
        - THETA_HTTP_RETRY_BACKOFF_MS
---
# Theta EdgeCloud 技能（云 API 运行时）

此运行时组件仅用于云 API 操作。

## 安全行为（明确说明）：
- 运行时命令处理器不会执行本地 shell 命令。
- 运行时不会读取本地文件以进行上传操作。
- 运行时不会调用本地的 RPC 端点（localhost/default）。
- 运行时在解析密钥时，会首先使用 OpenClaw 的密钥管理机制，如果该机制不可用，则会使用环境变量 `THETA_ONDEMAND_API_TOKEN`。
- 支付相关或需要修改配置的操作由用户触发，并且可以通过设置 `THETA_DRY_RUN=1` 来限制这些操作的执行。

## 支持的接口和服务：
- EdgeCloud 部署控制器 API
- 专用推理端点（兼容 OpenAI）
- Theta 视频 API
- Theta 按需模型 API（`ondemand(thetaedgecloud.com`）

## 仅用于运行时的软件包：
此 ClawHub 组件是一个包含文档的打包文件，旨在方便检查并减少扫描器的扫描范围。

## 可配置的环境变量：
- `THETA_DRY_RUN`：控制是否执行支付相关或需要修改配置的操作。
- `THETA_EC_API_KEY`：云 API 的访问密钥。
- `THETA_EC PROJECT_ID`：项目 ID。
- `THETA_INFERENCE_ENDPOINT`：推理服务的端点地址。
- `THETA_ONDEMAND_API_TOKEN`：按需模型的访问令牌。
- `THETA_HTTP_TIMEOUT_MS`：HTTP 请求的超时时间（以毫秒为单位）。
- `THETA_HTTP_MAX_RETRIES`：HTTP 请求的最大重试次数。
- `THETA_HTTP_RETRY_BACKOFF_MS`：每次重试之间的等待时间（以毫秒为单位）。