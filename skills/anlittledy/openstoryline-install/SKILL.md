---
name: openstoryline-install
description: 在本地机器上从源代码安装、配置并启动 FireRed-OpenStoryline。当用户需要设置 OpenStoryline、排查安装问题、下载所需资源、填写 config.toml 文件中的 API 密钥、启动 MCP（Management Console）和 Web 服务时，都可以使用此指南。同时，它也适用于处理中文相关的请求，例如：“安装 OpenStoryline”、“配置 OpenStoryline”、“启动 OpenStoryline”、“运行 OpenStoryline”、“修复 OpenStoryline 的安装问题”或“排查 OpenStoryline 启动失败”等。
---
# OpenStoryline 安装

当需要安装或修复 FireRed-OpenStoryline 的本地源代码仓库时，请使用此技能。

请确保工作流程的确定性：

1. 确认仓库路径，并阅读当前的 `README.md` 和 `config.toml` 文件。
2. 在进行任何更改之前，检查本地是否已满足所有先决条件。
3. 除非用户明确要求使用 Docker 或 `conda`，否则优先选择在本地创建虚拟环境（`venv`）。
4. 仅在 Python 依赖项安装成功后，才下载所需的资源文件。
5. 在宣布安装成功之前，验证导入模块和配置文件的加载情况。
6. 本技能适用于 macOS、Linux 或带有 POSIX shell 的 WSL 环境。

## 本技能涵盖的内容

- 根据需要克隆 GitHub 仓库
- 创建 Python 环境
- 安装 Python 依赖项
- 下载 `.storyline` 模型文件及 `resource/` 目录下的资源文件
- 配置 `config.toml` 文件中的模型设置
- 启动 MCP（Media Content Producer）和 Web 服务器
- 解释常见的安装或文档问题

## 先决条件

请先确保以下条件满足：

- 安装了 `git`
- Python 版本 >= 3.11
- 安装了 `ffmpeg`、`wget` 和 `unzip`
- （可选）安装了 `docker` 或 `conda`

如果缺少 `ffmpeg`、`wget` 或 `unzip`，请通过操作系统包管理器进行安装。

**示例：**

- 在使用 Homebrew 的 macOS 环境中：
  ```bash
  brew install ffmpeg wget unzip
  ```

- 在 Debian/Ubuntu 环境中：
  ```bash
  sudo apt-get update
  sudo apt-get install -y ffmpeg wget unzip
  ```

如果系统中没有支持的包管理器或相应的权限，请立即停止操作，并明确报告缺失的依赖项。

## 解释器的选择

优先选择已存在的且版本符合要求的解释器：

1. 系统自带的 Python 解释器（版本 >= 3.11）
2. 已安装的 `conda` Python 解释器（版本 >= 3.11）
3. 已安装的 `pyenv` Python 解释器（版本 >= 3.11），但前提是基本的标准库模块能够正常使用

在使用解释器之前，请先验证其是否满足要求：
```bash
/path/to/python -c "import ssl, sqlite3, venv; print('stdlib_ok')"
```

如果系统中没有合适的解释器，可以选择使用 `conda` 作为备用方案：
```bash
conda create -y -n openstoryline-py311 python=3.11
conda run -n openstoryline-py311 python --version
conda run -n openstoryline-py311 python -m venv .venv
```

找到合适的解释器后，务必在本地创建一个虚拟环境（`.venv`），并在后续的安装、配置验证和服务启动过程中使用 `.venv/bin/python`。

除非用户明确要求，否则不要为 `pyenv` 或 `conda` 重复执行其余的工作流程。

## 建议的安装路径

从仓库根目录开始安装：
```bash
/path/to/python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
bash download.sh
```

**注意事项：**

- `download.sh` 脚本会下载模型文件和大型资源文件包，这个过程可能需要较长时间，且可能会在网络中断后自动恢复。
- 仅安装 Python 包是不够的，还需要下载资源文件才能完成完整的本地运行环境配置。

## 配置

在启动应用程序之前，请更新 `config.toml` 文件。可以使用 `update_config.py` 脚本来完成配置更新。

至少需要配置以下内容：
```bash
.venv/bin/python scripts/update_config.py --config ./config.toml --set llm.model=REPLACE_WITH_REAL_MODEL
.venv/bin/python scripts/update_config.py --config ./config.toml --set llm.base_url=REPLACE_WITH_REAL_URL
.venv/bin/python scripts/update_config.py --config ./config.toml --set llm.api_key=sk-REPLACE_WITH_REAL_KEY

.venv/bin/python scripts/update_config.py --config ./config.toml --set vlm.model=REPLACE_WITH_REAL_MODEL
.venv/bin/python scripts/update_config.py --config ./config.toml --set vlm.base_url=REPLACE_WITH_REAL_URL
.venv/bin/python scripts/update_config.py --config ./config.toml --set vlm.api_key=sk-REPLACE_WITH_REAL_KEY
```

**可选但常见的配置项：**

- `search_media.pexels_api_key`（用于搜索媒体资源）
- `generate_voiceoverProviders.*` 目录下的 TTS（文本转语音）服务提供商密钥（选择一个提供商）

## 验证

在宣布安装完成之前，请执行以下验证步骤：
```bash
.venv/bin/pip check
PYTHONPATH=src .venv/bin/python -c "from open_storyline.config import load_settings; load_settings('config.toml'); print('config_ok')"
```

同时，请确认所有关键资源文件都已成功下载：

```bash
test -f .storyline/models/transnetv2-pytorch-weights.pth
test -d resource/bgms
```

## 启动服务

有两种常见的服务启动方式。这些服务是长时间运行的进程，无需等待它们正常退出。只需确认服务启动日志或监听端口已正确配置即可，必要时可以在不同的 shell 或会话中继续运行这些服务。

**手动启动服务：**
```bash
PYTHONPATH=src .venv/bin/python -m open_storyline.mcp.server
```

**在另一个 shell 中启动服务：**
```bash
PYTHONPATH=src .venv/bin/python -m uvicorn agent_fastapi:app --host 127.0.0.1 --port 8005
```

## 预期安装结果

安装成功后，应满足以下条件：

- 本地虚拟环境（`.venv/`）已创建
- MCP 服务在配置的本地端口（通常为 `127.0.0.1:8001`）上运行
- Web 服务在配置的 Web 端口（通常为 `127.0.0.1:8005`）上运行（不过 `run.sh` 脚本的默认设置可能有所不同）

## 常见问题

### `download.sh` 脚本运行缓慢或中断

**症状：** 大型文件下载过程中出现卡顿或连接中断

**解决方法：**  
- 允许 `wget` 自动恢复下载；该工具支持中断后继续下载的功能。  
- 不要仅依赖进度条来判断下载是否完成，而是直接检查下载后的文件是否已正确解压。

### Web/MCP 服务器无法绑定端口

**症状：** 在尝试绑定 `127.0.0.1` 或 `0.0.0.0` 端口时出现错误

**解决方法：**  
- 在代理沙箱环境中运行服务时，需要请求相应的权限以允许绑定端口。  
- 除非需要外部访问，否则建议使用 `127.0.0.1` 端口。

## 用户反馈机制

在向用户报告安装状态时，请明确说明以下内容：  
- 已安装的内容  
- 仍在下载的文件  
- 仍缺失的配置项  
- 服务正在监听的地址  

**注意：**  
即使仅安装了 Python 包，但如果资源文件尚未下载完成，也不要声明安装完成。