---
name: theta-edgecloud-skill
description: Theta EdgeCloud 的运行时框架采用 API 密钥作为身份验证的依据，支持安全、基于命令范围的权限控制，并具备安全测试（dry-run）功能。
metadata:
  openclaw:
    homepage: https://docs.thetatoken.org/docs/edgecloud-api-keys
    primaryEnv: THETA_EC_API_KEY
    requires:
      env:
        - THETA_EC_API_KEY
        - THETA_EC_PROJECT_ID
---
# Theta EdgeCloud 技能（云 API 运行时）

## 已知的临时限制（2026-03-07）
- 专用的推理端点（`theta.inference.models`、`theta.inference.chat`）目前被视为实验性功能/被平台限制使用，因为上游服务的稳定性尚未得到验证。
- 观察到的现象是：虽然部署状态显示为“运行中”（`Running`/`1/1`），但经过身份验证的请求仍可能返回 502/503 错误。
- 在 Theta 官方确认问题得到解决之前，请将这些命令仅用于诊断目的（不可用于生产环境）。

## 凭据范围模型（非常重要）
该技能的权限是基于具体命令来划分的：仅提供您所使用的命令系列所需的凭据。

- 控制器/部署/项目相关命令：`THETA_EC_API_KEY`、`THETA_EC PROJECT_ID`
- 平衡相关命令：需要添加 `THETA_ORG_ID`
- 按需推理命令：`THETA_ONDEMAND_API_TOKEN` 或 `THETA_ONDEMAND_API_KEY`
- 推理端点相关命令：`THETA_INFERENCE_ENDPOINT` 以及相应的认证信息（`THETA_INFERENCE_AUTH_TOKEN` 或用户名/密码）

上述凭据并非所有命令都需要同时提供。

## 快速设置（新用户）
1) 登录至 `https://www.thetaedgecloud.com/`。
2) 进入 **账户 -> 项目**，选择您的项目。
3) 点击 **创建 API 密钥** 并复制密钥。
4) 在安装/设置过程中提供以下信息：
   - `THETA_EC_API_KEY`
   - `THETA_EC PROJECT_ID`
5) （针对按需图像/视频生成功能）创建按需 API 密钥/令牌，并设置：
   - `THETA_ONDEMAND_API_KEY`（或 `THETA_ONDEMAND_API_TOKEN`）

如果某个命令提示缺少密钥，请运行 `theta.auth.capabilities` 以查看具体需要配置哪些内容。

此运行时组件仅适用于云 API 操作。

## 安全行为（明确说明）
- 运行时命令处理器不会执行本地 shell 命令。
- 运行时不会读取本地文件以进行上传操作。
- 运行时不会调用本地的 RPC 端点。
- 在运行时命令中，专用推理端点的设置会被 `args.endpoint` 取代；请使用 `THETA_INFERENCE_ENDPOINT`。
- 运行时在解析敏感信息时，首先使用 OpenClaw 的秘密管理机制，其次使用环境变量：
  - `THETA_ONDEMAND_API_TOKEN`
  - `THETA_INFERENCE_AUTH_TOKEN`
  - `THETA_INFERENCE_AUTH_USER` / `THETA_INFERENCE_AUTH_PASS`
- 支付相关操作由用户触发，并可以通过 `THETA_DRY_RUN=1` 来限制其执行。

## 用户实际需要的凭据
用户需要一个启用了计费/信用功能的 Theta EdgeCloud 账户才能执行支付操作。

仅使用您计划使用的功能集所需的凭据：
- 部署相关 API：
  - `THETA_EC_API_KEY`
  - `THETA_EC PROJECT_ID`
- 专用推理端点：
  - `THETA_INFERENCE_ENDPOINT`
  - 基本认证方式：
    - `THETA_INFERENCE_AUTH_USER`
    - `THETA_INFERENCE_AUTH_PASS`
  - 或者使用 bearer token 进行认证：
    - `THETA_INFERENCE_AUTH_TOKEN`
- 按需模型 API：
  - `THETA_ONDEMAND_API_TOKEN`
- Theta 视频 API：
  - `THETA_VIDEO_SA_ID`
  - `THETA_VIDEO_SA_SECRET`

## 仅适用于运行时的包
此 ClawHub 组件是一个用于透明检查的文档包，旨在减少扫描时的复杂度。

## 环境变量（可选配置）
- `THETA_DRY_RUN`
- `THETA_EC_API_KEY`
- `THETA_ECPROJECT_ID`
- `THETA_ORG_ID`
- `THETA_INFERENCE_ENDPOINT`
- `THETA_INFERENCE_AUTH_USER`
- `THETA_INFERENCE_AUTH_PASS`
- `THETA_INFERENCE_AUTH_TOKEN`
- `THETA_ONDEMAND_API_TOKEN`
- `THETA_ONDEMAND_API_KEY`
- `THETA_VIDEO_SA_ID`
- `THETA_VIDEO_SA_SECRET`
- `THETA_HTTP_TIMEOUT_MS`
- `THETA_HTTP_MAX_RETRIES`
- `THETA_HTTP_RETRY_BACKOFF_MS`

## AI 服务支持的功能
- 部署相关 API：列出、创建、停止、删除部署
- 专用模型模板：标准模板和自定义模板
- 按需模型 API：实时发现、推理、状态查询、轮询
- 专用推理端点：模型管理、聊天功能
- 专用部署列表
- Jupyter 笔记本列表
- GPU 节点和 GPU 集群列表
- 持久化存储列表
- 代理 AI（聊天机器人）列表
- Theta 视频 API：模型列表、上传、视频流处理、存储操作

## 仅适用于 Theta 的 OpenClaw 运行选项（无需其他订阅）
如果 Theta 是唯一的付费 AI 后端，此技能仍能覆盖大部分 OpenClaw 的执行流程：
- 内容生成：
  - 图像/标志/创意生成（`flux`、`stable_diffusion_*`）通过 `theta.ondemand.infer`
  - 图像增强/缩放（`esrgan`）
  - 保持图像质量的生成（`instant_id`）
  - 虚拟试穿/产品可视化（`stable_viton`）
  - 视频生成（`step_video`）和语音头像（`talking_head`）
- 网站 AI 功能：
  - 使用按需大型语言模型（`llama_3_8b`、`llama_3_1_70b`）实现聊天机器人、支持、问答、内容重写
- 视觉/媒体智能：
  - 字幕生成/替代文本（`blip`）、对象检测（`grounding_dino`）、文本转录（`whisper`）
- 视频基础设施：
  - 上传/视频流处理/存储操作（`theta.video.*`）
- 计算/操作相关：
  - 虚拟机/部署生命周期管理、GPU/存储资源查询、能力/平衡检查（`theta.deployments.*`、`theta.ai.*`、`theta.auth.capabilities`、`theta.billing.balance`）

**推荐的可靠性方案：**
- 对于生产自动化场景，建议优先使用按需服务和视频/控制器相关的流程。
- 在平台问题得到解决之前，将专用推理端点命令（`theta.inference.models`、`theta.inference.chat`）视为实验性功能。

## 组织与项目范围
- Theta 仪表板使用组织（Organization）和项目（Project）的上下文信息。
- 运行时命令具有项目范围限制，在相关情况下需要明确提供 `projectId`。
- 组织成员资格/邀请/会话管理相关的端点需要通过 Web 仪表板进行身份验证，不包含在此技能的运行时功能中。

## API 密钥与用户名/密码认证（已验证）
- API 密钥（`THETA_EC_API_KEY`）加上项目/组织 ID 可以访问项目范围内的控制器 API 和组织资源信息。
- 对于运行时操作，API 密钥已足够；这些操作不需要使用仪表板的用户名/密码。
- 账户管理相关的端点（组织/项目成员资格、邀请、使用记录查询）仍然需要用户名/密码进行身份验证。

## 按需 API 密钥别名
运行时接受 `THETA_ONDEMAND_API_TOKEN` 或 `THETA_ONDEMAND_API_KEY` 作为按需模型 API 的认证方式。

## 可靠性行为
- `theta.ai.dedicatedDeployments.list` 在服务模板调用失败时会输出警告信息，避免出现空输出的情况。
- `theta.ondemand.listServices` 会根据服务来源（`live` 或 `catalog`）返回服务条目，并在实时发现功能不可用时提供错误原因/警告信息。

## 认证诊断
使用 `theta.auth.capabilities` 可快速查看当前凭据集支持哪些命令系列以及缺少哪些环境变量。

## 首次运行时的设置命令
使用 `theta.setup` 为新用户提供一站式设置指南，包括在哪里创建 API 密钥以及需要设置哪些环境变量。