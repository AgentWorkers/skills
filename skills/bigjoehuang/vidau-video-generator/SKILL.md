---
name: vidau
version: "1.0.0"
license: MIT
description: 使用 Vidau Open API 可以利用 Veo3、Sora2 等模型生成短视频，或查询账户余额。请访问 superaiglobal.com 进行注册并配置 API 密钥。
homepage: https://vidau.ai
metadata:
  openclaw:
    requires:
      env: ["VIDAU_API_KEY"]
    primaryEnv: "VIDAU_API_KEY"
    homepage: "https://doc.superaiglobal.com/cn/overview/introduction"
compatibility: Python 3.x required; network access to api.superaiglobal.com
---
# Vidau 视频生成器

**版本:** 1.0.0

## 使用场景

- 用户请求“生成视频”、“使用 Veo3/Sora 创建短视频”、“根据提示/图片生成视频”、“根据脚本制作视频片段”等。
- 用户询问“我有多少 Vidau 信用点数”、“查看我的 Vidau 余额”、“查询 Vidau 信用点数”等。
- 用户请求“查看我的视频任务状态”、“我的 Vidau 任务是否已完成”、“通过 UUID 查询任务”等。

## 不适用场景

- 用户仅希望编辑或处理现有的本地视频文件（例如裁剪、合并、转码），而不调用任何云 API。
- 用户请求使用其他视频 API（例如 Runway、Pika）；如果可用，请使用相应的服务。
- 用户没有提及 Vidau/Veo/Sora/Seedance，也没有提到“生成视频”或“创建视频”，而是只是在讨论概念或其他工具。

## 回复语言

在向用户返回结果（视频链接、信用点数或错误信息）时，使用与用户提问相同的语言（例如，如果用户用中文提问，则使用简体中文；如果用户用英文提问，则使用英文）。

## 先决条件

必须设置环境变量 `VIDAU_API_KEY`（由 OpenClaw 从 `skills.entries.vidau.apiKey` 或 `env` 中获取）。如果用户没有 API 密钥，他们必须访问 [https://www.superaiglobal.com/](https://www.superaiglobal.com/) 进行注册。如果未配置此变量，请勿触发此技能。

## 环境检查

在运行任何脚本之前，请确保已安装 Python 3：

1. 运行 `python3 --version` 或 `python --version`。如果其中任何一个命令成功，则在调用以下脚本时使用该命令。
2. 如果两个命令都失败，请尝试为当前平台安装 Python：
   - **macOS**: `brew install python3`（需要 Homebrew）。
   - **Linux (Debian/Ubuntu)**: `sudo apt-get update && sudo apt-get install -y python3`。
   - **Windows**: 如果可用，运行 `winget install Python.Python.3.12`；否则，告知用户从 [python.org](https://www.python.org/downloads/) 下载并安装。
3. 如果安装失败（例如权限问题或操作系统不支持），回复一条简短的消息，说明需要 Python 3，并提供 [python.org/downloads](https://www.python.org/downloads/) 的链接，然后停止操作。在安装 Python 之前，请勿运行 Vidau 脚本。

这些脚本仅使用标准库，不需要安装任何 pip 包。

## 可用的脚本

- **`scripts/query_credit.py`** — 查询当前可用的信用点数；无需参数；输出包含 `data.availableCredit` 和 `data.userId` 的 JSON 数据。
- **`scripts/create_task.py`** — 创建视频任务；需要 `--prompt` 参数，`--model` 参数可选；输出包含 `data.taskUUID` 的 JSON 数据。
- **`scripts/query_task.py`** — 一次性查询任务状态和结果；需要 `--task-uuid` 参数；输出包含 `taskStatus` 的 JSON 数据，成功时还会打印 `[VIDAU_VIDEO_URL]` 和 `[VIDAU_THUMB_PATH]` 的链接。在向用户展示成功结果时，**请直接复制这些链接**（不要重写或缩短链接）。当任务状态变为 `succeeded` 或 `failed` 时，脚本会将 `[OPENCLAW] DELETE_SCHEDULED_TASK task_uuid=<uuid>` 打印到标准错误输出（stderr），以便平台删除相应的定时任务。
- **`scripts/wait_task.py`** — 监控任务的状态（直到成功或失败，或超时）；需要 `--task-uuid` 参数；`--interval` 参数可选（默认为 10 秒），`--timeout` 参数可选（默认为 600 秒 = 10 分钟）。成功时输出与 `query_task.py` 相同的 JSON 数据以及 `[VIDAU_VIDEO_URL]` 和 `[VIDAU_THUMB_PATH]` 的链接。退出代码：0 表示成功，1 表示失败，2 表示超时。

## 工作流程（生成视频）

1. **可选**：在创建任务之前，先调用 `scripts/query_credit.py` 来检查是否有足够的信用点数，以避免因信用不足导致的失败。
2. 调用 `scripts/create_task.py`，并提供 `--prompt`（必需）、`--resolution`（必需）、`--model`（默认为 `veo@3:normal`）等参数；根据需要提供其他参数。
3. 从脚本的标准输出（stdout）中读取 `data.taskUUID`。
4. **推荐方案 A**：调用 `scripts/wait_task.py --task-uuid <taskUUID>` 来监控任务进度（默认间隔为 10 秒，超时时间为 10 分钟）。**方案 B**：手动每隔 5–10 秒调用 `scripts/query_task.py --task-uuid <taskUUID>`，直到任务状态变为 `succeeded` 或 `failed`；总等待时间不超过 3–5 分钟。
5. **成功**：将视频和缩略图链接返回给用户。**请直接复制脚本输出中的链接**：显示给用户的视频和缩略图链接必须完全复制自脚本输出中的 `[VIDAU_VIDEO_URL]` 和 `[/VIDAU_VIDEO_URL]`、`[VIDAU_THUMB_PATH]` 和 `[/VIDAU_THUMB_PATH]` 之间的内容——不要重写、截断或替换链接；请以代码块的形式呈现链接，以便用户可以直接复制。
6. **失败**：使用 API 返回的 `message` 或错误代码向用户解释原因（例如信用不足、违反政策等）。
7. **当任务达到最终状态**（成功或失败）时：如果为该任务 UUID 创建了定时任务，请取消/删除该定时任务，以防止平台继续重复查询。`query_task.py` 会在最终状态时将 `[OPENCLAW] DELETE_SCHEDULED_TASK task_uuid=<uuid>` 打印到标准错误输出（stderr），以便平台进行相应的处理。

## 工作流程（查询信用点数）

当用户询问余额时，调用 `scripts/query_credit.py`（无需参数），从标准输出（stdout）中读取 `data.availableCredit` 并回复结果；可选地包含 `data.userId`。

## 参数（create_task.py）

| 参数 | 是否必需 | 说明 |
|-----------|----------|-------------|
| `--prompt` | 是 | 最多 2000 个字符的文本描述 |
| `--model` | 否 | 默认值为 `veo@3:normal`；详见下面的模型列表 |
| `--negative-prompt` | 否 | 负面提示，最多 2000 个字符 |
| `--image-url` | 否 | 第一帧图像的 URL |
| `--last-image-url` | 否 | 最后一帧图像的 URL |
| `--duration` | 否 | 视频时长（以秒为单位） |
| `--generate-audio` | 否 | 是否生成音频；true/false |
| `--seed` | 否 | 随机种子 |
| `--resolution` | 是 | 分辨率，例如 `720p`、`1080p` |
| `--ratio` | 否 | 宽高比，例如 `16:9`、`9:16` |

有效值：`resolution` 通常为 `720p` 或 `1080p`；`ratio` 例如 `16:9`、`9:16`。更多详细信息请参阅 [references/parameters.md](references/parameters.md)。运行 `python scripts/create_task.py --help` 可查看所有参数。

## 模型列表

常见的模型 ID（与 API 对应）：

- **Veo 3**: `veo@3:normal`
- **Veo 3.1**: `veo@3.1:normal`, `veo@3.1:fast`
- **Sora 2**: `sora@2:normal`, `sora@2:pro`
- **Seedance**: `seedance@1:pro`, `seedance@1:pro_fast`
- **Wan 2.5**: `wan@2.5:preview`
- **Vidu Q2**: `vidu@q2:turbo`, `vidu@q2:pro`

更多模型和用例请参阅 [references/models.md](references/models.md)。

## 错误处理

- 如果未设置 `VIDAU_API_KEY`，脚本将退出并显示错误信息；告知用户访问 [https://www.superaiglobal.com/](https://www.superaiglobal.com/) 进行注册以获取 API 密钥，然后在 OpenClaw 中配置该密钥。
- 常见的 API 错误代码包括 `CreditInsufficient`、`TaskPromptPolicyViolation`、`ImageDownloadFailure`。将这些 API 错误信息以用户的语言形式反馈给用户。更多错误代码和相应的用户提示信息请参阅 [references/errors.md](references/errors.md)。

## 示例用法

- **生成视频**：用户请求例如“使用 Veo3 根据这个脚本生成一个 8 秒的视频”或“使用 Sora2 生成一个 10 秒的日落海滩视频片段”。处理流程：（可选）`query_credit.py` → `create_task.py --prompt "..." --resolution 720p --duration 8 --model veo@3:normal` → 读取 `taskUUID` → `wait_task.py --task-uuid <uuid>` → 从输出中返回视频链接或解释失败原因。
- **查询信用点数**：用户请求例如“我有多少 Vidau 信用点数？”或“查看我的 Vidau 余额”。处理流程：`query_credit.py` → 返回 `data.availableCredit`（以及可选的 `data.userId`）。
- **查询任务状态**：用户请求例如“我的视频任务完成了吗？UUID 是 xxx”。处理流程：`wait_task.py --task-uuid xxx` 或 `query_task.py --task-uuid xxx` → 返回任务状态或视频链接。当任务成功或失败时，取消所有正在查询该任务 UUID 的定时任务。