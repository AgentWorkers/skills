---
name: theta-edgecloud-skill
description: Theta EdgeCloud API：采用“API密钥优先”的运行时框架，具备安全的命令级权限控制机制以及“干运行”（dry-run）安全功能。
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
- 专用推理端点（`theta.inference.models`、`theta.inference.chat`）目前被视为实验性功能或因上游服务的稳定性问题而被平台禁用。
- 观察到的现象：部署状态显示为“运行中”（`Running`/`1/1`），但经过身份验证的请求仍可能返回 502/503 错误。
- 在 Theta 宣布修复方案之前，请将这些命令仅用于诊断目的（不可用于生产环境）。

## 凭据范围模型（重要）
该技能的使用需要相应的凭据：
- 控制器/部署/项目相关命令：`THETA_EC_API_KEY`、`THETA_EC_PROJECT_ID`
- 平衡相关命令：需要 `THETA_ORG_ID`
- 按需推理命令：需要 `THETA_ONDEMAND_API_TOKEN` 或 `THETA_ONDEMAND_API_KEY`
- 推理端点相关命令：需要 `THETA_INFERENCE_ENDPOINT` 以及相应的认证信息（`THETA_INFERENCE_AUTH_TOKEN` 或用户名/密码）

上述凭据并非所有命令都需要同时提供。

## 快速设置（新用户）
1) 登录至 `https://www.thetaedgecloud.com/`。
2) 转到 **账户 -> 项目**，选择您的项目。
3) 点击 **创建 API 密钥** 并复制密钥。
4) 在安装/设置过程中提供以下凭据：
   - `THETA_EC_API_KEY`
   - `THETA_ECPROJECT_ID`
5) （如需按需生成图像/视频）创建按需 API 密钥/令牌，并设置：
   - `THETA_ONDEMAND_API_KEY`（或 `THETA_ONDEMAND_API_TOKEN`）

如果某个命令提示缺少密钥，请运行 `theta.auth.capabilities` 以查看具体需要配置哪些信息。

此运行时组件仅适用于云 API 操作。

## 安全行为（明确说明）
- 运行时命令处理程序不会执行本地 shell 命令。
- 运行时不会读取本地文件以进行上传操作。
- 运行时不会调用本地的 RPC 端点。
- 对于以下凭据的解析，运行时首先使用 OpenClaw 的秘密管理机制，其次使用环境变量：
  - `THETA_ONDEMAND_API_TOKEN`
  - `THETA_INFERENCE_AUTH_TOKEN`
  - `THETA_INFERENCE_AUTH_USER` / `THETA_INFERENCE_AUTH_PASS`
- 支付相关操作由用户触发，并可通过 `THETA_DRY_RUN=1` 来限制其执行。

## 用户实际所需的凭据
用户需要一个启用了计费/信用功能的 Theta EdgeCloud 账户才能使用这些功能。

仅使用您计划使用的功能所需的凭据：
- 部署 API：`THETA_EC_API_KEY`、`THETA_ECPROJECT_ID`
- 专用推理端点：`THETA_INFERENCE_ENDPOINT` 及相应的认证信息（基本认证或 bearer token 认证）
- 按需模型 API：`THETA_ONDEMAND_API_TOKEN`
- Theta 视频 API：`THETA_VIDEO_SA_ID`、`THETA_VIDEO_SA_SECRET`

## 仅适用于运行时的软件包
此 ClawHub 软件包主要用于透明地检查运行时组件及其接口。

## 环境配置参数（可选）
- `THETA_DRY_RUN`
- `THETA_EC_API_KEY`
- `THETA_ECPROJECT_ID`
- `THETA_INFERENCE_ENDPOINT`
- `THETA_INFERENCE_AUTH_USER`
- `THETA_INFERENCE_AUTH_PASS`
- `THETA_INFERENCE_AUTH_TOKEN`
- `THETA_ONDEMAND_API_TOKEN`
- `THETA_HTTP_TIMEOUT_MS`
- `THETA_HTTP_MAX_RETRIES`
- `THETA_HTTP_RETRY_BACKOFF_MS`

## AI 服务支持的功能
- 部署 API：列表、创建、停止、删除
- 专用模型模板：标准模板和自定义模板
- 按需模型 API：实时发现、推理、状态查询
- 专用推理端点：模型管理、聊天功能
- 专用部署信息查询
- Jupyter 笔记本列表
- GPU 节点和 GPU 集群列表
- 持久化存储信息查询
- 代理 AI（聊天机器人）管理
- Theta 视频 API：列表、上传、视频流处理、存储操作

## 仅适用于 Theta 的 OpenClaw 运行选项（无需其他订阅）
如果 Theta 是唯一的付费 AI 后端，此技能仍能覆盖大部分 OpenClaw 的执行功能：
- 内容生成：
  - 图像/Logo/创意内容生成（`flux`、`stable_diffusion_*`）通过 `theta.ondemand.infer`
  - 图像增强/缩放（`esrgan`）
  - 保持图像质量的生成（`instant_id`）
  - 虚拟试穿/产品可视化（`stable_viton`）
  - 视频生成（`step_video`）和语音头像（`talking_head`）
- 网站 AI 功能：
  - 使用按需 LLM 的聊天机器人/支持/问答/内容重写（`llama_3_8b`、`llama_3_1_70b`）
- 视觉/媒体智能：
  - 字幕生成/替代文本（`blip`）、物体检测（`grounding_dino`）、语音转文字（`whisper`）
- 视频基础设施：
  - 上传/视频流处理/存储操作（`theta.video.*`）
- 计算/操作相关：
  - 虚拟机/部署生命周期管理、GPU/存储信息查询、资源使用情况检查（`theta.deployments.*`、`theta.ai.*`、`theta.auth.capabilities`、`theta.billing.balance`）

**推荐的可靠性方案：**
- 对于生产自动化场景，建议优先使用按需服务和视频/控制器相关功能。
- 在平台问题得到解决之前，将专用推理端点命令（`theta.inference.models`、`theta.inference.chat`）视为实验性功能。

## 组织与项目范围
- Theta 仪表板基于组织和项目进行权限控制。
- 运行时命令具有项目范围限制，在需要时必须提供 `projectId`。
- 组织成员资格/邀请/会话管理相关的端点需要通过 Web 仪表板进行身份验证，不包含在此技能的运行时功能中。

## API 密钥与用户名/密码认证
- API 密钥（`THETA_EC_API_KEY`）加上项目/组织 ID 可以访问项目范围内的控制器 API 和组织资源管理功能。
- 对于运行时操作，API 密钥已足够；仪表板中的用户名/密码不是必需的。
- 账户管理相关的端点（组织/项目成员资格、邀请、使用记录查询）仍需要用户名/密码进行身份验证。

## 按需 API 密钥别名
运行时支持使用 `THETA_ONDEMAND_API_TOKEN` 或 `THETA_ONDEMAND_API_KEY` 进行按需模型 API 的认证。

## 认证诊断
使用 `theta.auth.capabilities` 可快速查看当前凭据集支持哪些命令功能以及缺少哪些环境变量。

## 首次运行时的设置命令
新用户可以使用 `theta.setup` 获取一个简化的设置指南，包括在哪里创建 API 密钥以及需要设置哪些环境变量。