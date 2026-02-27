---
name: gpu-cli
description: 在远程的 NVIDIA GPU（A100、H100、RTX 4090）上运行机器学习训练、大型语言模型推理以及 ComfyUI 工作流程。利用智能文件同步功能进行云 GPU 计算——只需在命令前加上 ‘gpu’ 即可远程执行这些命令。
version: 0.14.0
metadata:
  openclaw:
    requires:
      bins:
        - gpu
    install:
      brew: gpu-cli/tap/gpu
      script: curl -fsSL https://gpu-cli.sh/install | sh
    homepage: https://gpu-cli.sh
    tags:
      - gpu
      - machine-learning
      - cloud-compute
      - remote-execution
      - llm
      - comfyui
      - nvidia
      - cuda
      - training
      - inference
      - runpod
      - pytorch
      - stable-diffusion
---
# GPU 命令行界面 (GPU CLI)

GPU 命令行界面 (GPU CLI) 通过在前缀加上 `gpu` 来在远程 NVIDIA GPU 上运行本地命令。它负责创建容器（pod）、同步代码、流式传输日志以及将输出结果同步回来。例如，`uv run python train.py` 会转换为 `gpu run uv run python train.py`。

## 快速诊断工具

```bash
gpu doctor --json       # Check if setup is healthy (daemon, auth, provider keys)
gpu status --json       # See running pods and costs
gpu inventory --json    # See available GPUs and pricing
```

## 命令分类

### 入门命令

| 命令 | 功能 |
|---|---|
| `gpu login` | 基于浏览器的身份验证 |
| `gpu logout [-y]` | 注销会话 |
| `gpu init [--gpu-type T] [--force]` | 初始化项目配置 |
| `gpu upgrade` | 打开订阅升级页面 |

### 运行代码

| 命令 | 功能 |
|---|---|
| `gpu run <command>` | 在远程 GPU 上执行命令 |
| `gpu run -d <command>` | 在后台（分离模式）运行命令 |
| `gpu run -a <job_id>` | 重新连接到正在运行的作业 |
| `gpu run --cancel <job_id>` | 取消正在运行的作业 |
| `gpu status [--json]` | 显示项目状态、容器信息及费用 |
| `gpu logs [-j JOB] [-f] [--tail N] [--json]` | 查看作业输出 |
| `gpu attach <job_id>` | 重新连接到作业的输出流 |
| `gpu stop [POD_ID] [-y]` | 停止活动的容器 |

`gpu run` 命令的主要参数包括：`--gpu-type`、`--gpu-count <1-8>`、`--min-vram`、`--rebuild`、`-o/--output`、`--no-output`、`--sync`、`-p/--publish <PORT>`、`-e <KEY=VALUE>`、`-i/--interactive`。

### GPU 资源管理

| 命令 | 功能 |
|---|---|
| `gpu inventory [--available] [--min-vram N] [--max-price P] [--json]` | 列出可用 GPU 及其价格信息 |

### 卷管理

| 命令 | 功能 |
|---|---|
| `gpu volume list [--detailed] [--json]` | 列出所有网络卷 |
| `gpu volume create [--name N] [--size GB] [--datacenter DC]` | 创建卷 |
| `gpu volume delete <VOL> [--force]` | 删除卷 |
| `gpu volume extend <VOL> --size <GB>` | 扩展卷容量 |
| `gpu volume set-global <VOL>` | 设置默认使用卷 |
| `gpu volume status [--volume V] [--json]` | 查看卷使用情况 |
| `gpu volume migrate <VOL> --to <DC>` | 将卷迁移至指定数据中心 |
| `gpu volume sync <SRC> <DEST>` | 在卷之间同步数据 |

### 加密存储（Vault）

| 命令 | 功能 |
|---|---|
| `gpu vault list [--json]` | 列出所有加密存储文件 |
| `gpu vault export <PATH> <DEST>` | 导出加密文件 |
| `gpu vault stats [--json] | 查看存储使用统计信息 |

### 配置管理

| 命令 | 功能 |
|---|---|
| `gpu config show [--json]` | 显示配置信息 |
| `gpu config validate` | 校验配置是否符合规范 |
| `gpu config schema` | 打印配置的 JSON 模式 |
| `gpu config set <KEY> <VALUE>` | 设置全局配置选项 |
| `gpu config get <KEY>` | 获取全局配置值 |

### 身份验证

| 命令 | 功能 |
|---|---|
| `gpu auth login [--profile P]` | 使用云服务提供商进行身份验证 |
| `gpu auth logout` | 注销登录 |
| `gpu auth status` | 查看身份验证状态 |
| `gpu auth add <HUB>` | 添加 Hub 账户（如 hf、civitai） |
| `gpu auth remove <HUB>` | 删除 Hub 账户 |
| `gpu auth hubs` | 列出已配置的 Hub |

### 组织管理

| 命令 | 功能 |
|---|---|
| `gpu org list` | 列出所有组织 |
| `gpu org create <NAME>` | 创建新组织 |
| `gpu org switch [SLUG]` | 切换当前使用的组织 |
| `gpu org invite <EMAIL>` | 邀请成员加入组织 |
| `gpu org service-account create --name N` | 创建服务账户 |
| `gpu org service-account list` | 查看服务账户列表 |
| `gpu org service-account revoke <ID>` | 取消服务账户权限 |

### 大语言模型 (LLM) 推理

| 命令 | 功能 |
|---|---|
| `gpu llm run [--ollama\|--vllm] [--model M] [-y] | 启动 LLM 推理 |
| `gpu llm info [MODEL] [--url URL] [--json] | 查看模型信息 |

### ComfyUI 工作流程管理

| 命令 | 功能 |
|---|---|
| `gpu comfyui list [--json]` | 查看可用的工作流程 |
| `gpu comfyui info <WORKFLOW> [--json] | 查看工作流程详情 |
| `gpu comfyui validate <WORKFLOW> [--json] | 预检工作流程 |
| `gpu comfyui run <WORKFLOW>` | 在 GPU 上运行工作流程 |
| `gpu comfyui generate "<PROMPT>"` | 生成文本图像 |
| `gpu comfyui stop [WORKFLOW] [--all]` | 停止 ComfyUI 容器 |

### 笔记本管理

| 命令 | 功能 |
|---|---|
| `gpu notebook [FILE] [--run] [--new NAME]` | 在 GPU 上运行 Marimo 笔记本 |

**别名**: `gpu nb`

### 无服务器端点 (Serverless Endpoints)

| 命令 | 功能 |
|---|---|
| `gpu serverless deploy [--template T] [--json] | 部署无服务器端点 |
| `gpu serverless status [ENDPOINT] [--json] | 查看端点状态 |
| `gpu serverless logs [ENDPOINT]` | 查看请求日志 |
| `gpu serverless list [--json] | 列出所有端点 |
| `gpu serverless delete [ENDPOINT] | 删除端点 |
| `gpu serverless warm [--cpu\|--gpu] | 预热端点 |

### 模板管理

| 命令 | 功能 |
|---|---|
| `gpu template list [--json] | 查看官方提供的模板 |
| `gpu template clear-cache` | 清除缓存模板 |

### 守护进程控制

| 命令 | 功能 |
|---|---|
| `gpu daemon status [--json] | 查看守护进程状态 |
| `gpu daemon start` | 启动守护进程 |
| `gpu daemon stop` | 停止守护进程 |
| `gpu daemon restart` | 重启守护进程 |
| `gpu daemon logs [-f] [-n N]` | 查看守护进程日志 |

### 工具与实用程序

| 命令 | 功能 |
|---|---|
| `gpu dashboard` | 用于查看容器和作业的交互式图形界面 |
| `gpu doctor [--json] | 进行诊断检查 |
| `gpu agent-docs` | 将代理配置打印到标准输出 |
| `gpu update [--check]` | 更新 CLI 工具 |
| `gpu changelog [VERSION]` | 查看版本更新记录 |
| `gpu issue ["desc"]` | 报告问题 |
| `gpu desktop` | 管理桌面应用程序 |
| `gpu support` | 访问社区 Discord 频道以获取帮助 |

## 常见使用流程

1. **设置**: 先执行 `gpu login`，然后 `gpu init`。
2. **运行作业**: `gpu run python train.py --epochs 10`。
3. **指定使用特定 GPU**: `gpu run --gpu-type "RTX 4090" python train.py`。
4. **在后台运行作业**: `gpu run -d python long_training.py`，之后使用 `gpu status --json` 查看状态。
5. **查看日志**: `gpu logs --json`。
6. **停止容器**: `gpu stop -y`。
7. **启动 LLM 推理**: `gpu llm run --ollama --model llama3 -y`。
8. **使用 ComfyUI**: `gpu comfyui run flux_schnell`。
9. **进行故障诊断**: `gpu doctor --json`。

`gpu run` 命令支持容器复用：命令执行完成后，后续的 `gpu run` 会重用现有的容器，直到你手动停止容器或达到冷却时间限制。

## JSON 输出格式

大多数命令支持使用 `--json` 选项来输出结构化数据（到标准输出），而状态信息和进度消息则输出到标准错误流（stderr）。

支持 `--json` 的命令包括：`status`、`logs`、`doctor`、`inventory`、`config show`、`daemon status`、`volume list`、`volume status`、`vault list`、`vault stats`、`comfyui list`、`comfyui info`、`serverless deploy`、`serverless status`、`serverless list`、`template list`、`llm info`。

## 错误代码

| 代码 | 含义 | 处理方式 |
|---|---|---|
| `0` | 成功 | 继续执行 |
| `1` | 一般错误 | 请查看标准错误流（stderr） |
| `2` | 使用错误 | 请检查命令语法 |
| `10` | 需要身份验证 | 请执行 `gpu auth login` |
| `11` | 超出配额 | 请尝试 `gpu upgrade` 或等待 |
| `12` | 资源未找到 | 请检查资源 ID |
| `13` | 守护进程不可用 | 请尝试 `gpu daemon start` 并重试 |
| `14` | 超时 | 请重试 |
| `15` | 任务被取消 | 如有需要，请重新运行 |
| `130` | 进程被中断 | 请重新尝试 |

## 配置文件

- 项目配置文件: `gpu.toml`、`gpu.jsonc` 或 `pyproject.toml [tool.gpu]`
- 全局配置文件: `~/.gpu-cli/config.toml`（通过 `gpu config set/get` 进行配置）
- 配置文件的上传/下载规则由 `.gitignore` 文件控制
- 机密信息和凭证必须保存在操作系统的密钥链中，切勿以明文形式保存在项目文件中
- CI 环境变量: `GPU_RUNPOD_API_KEY`、`GPU_SSH_PRIVATE_KEY`、`GPU_SSH_PUBLIC_KEY`

## 参考资料

- 项目创建和任务设置: `references/create.md`
- 调试及常见故障处理: `references/debug.md`
- 配置模式和字段示例: `references/config.md`
- 成本与 GPU 选择指南: `references/optimize.md`
- 持久化存储和卷管理: `references/volumes.md`