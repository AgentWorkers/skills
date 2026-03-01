---
name: hummingbot-developer
description: 开发人员技能：能够从源代码层面运行 Hummingbot 和 Gateway，构建 wheel 包以及 Docker 镜像，并针对从源代码运行的 Hummingbot API 进行测试。当开发人员需要在本地构建、运行或测试 Hummingbot 组件时，可以使用这些技能。
metadata:
  author: hummingbot
commands:
  start:
    description: Check dev environment — repo branches, prereqs, running services
  install-deps:
    description: Auto-install missing dev dependencies (conda, node, pnpm, docker, git)
  select-branches:
    description: Interactively pick branches for hummingbot, gateway, and hummingbot-api
  install-all:
    description: Install all three repos in order (hummingbot → gateway → hummingbot-api)
  build-all:
    description: Build hummingbot wheel + all Docker images in order
  verify-build:
    description: Verify all builds are correct and in sync across repos
  run-dev-stack:
    description: Start the full dev stack from source (infra + gateway + API)
  setup-hummingbot:
    description: Install Hummingbot from source (branch, conda env, solders fix)
  run-hummingbot:
    description: Run Hummingbot CLI from source
  build-hummingbot:
    description: Build Hummingbot wheel and Docker image from source
  setup-gateway:
    description: Install and configure Gateway from source (pnpm install/build/setup)
  run-gateway:
    description: Run Gateway from source in dev mode
  build-gateway:
    description: Build Gateway Docker image from source
  setup-api-dev:
    description: Configure Hummingbot API to use local Hummingbot source (pip install -e)
  run-api-dev:
    description: Run Hummingbot API from source with hot-reload against local Hummingbot
  test-integration:
    description: Smoke test the full stack — API, Gateway, and Hummingbot connectivity
---
# hummingbot-developer

这是一套用于从源代码构建和运行整个Hummingbot开发栈的开发工作流程工具集。

**命令**（使用格式 `/hummingbot-developer <命令>` 执行）：

| 命令 | 描述 |
|---------|-------------|
| `start` | 检查开发环境状态 |
| `select-branches` | 为所有3个仓库选择分支 |
| `install-all` | 按顺序安装所有3个仓库 |
| `build-all` | 构建wheel文件及所有Docker镜像 |
| `verify-build` | 验证构建是否正确且同步 |
| `run-dev-stack` | 从源代码启动整个开发栈 |
| `setup-hummingbot` | 从源代码安装Hummingbot |
| `run-hummingbot` | 从源代码运行Hummingbot CLI |
| `build-hummingbot` | 构建wheel文件及Docker镜像 |
| `setup-gateway` | 从源代码安装Gateway |
| `run-gateway` | 以开发模式运行Gateway |
| `build-gateway` | 构建Gateway的Docker镜像 |
| `setup-api-dev` | 将API连接到本地Hummingbot源代码 |
| `run-api-dev` | 从源代码运行API，并支持热重载 |
| `test-integration` | 对整个开发栈进行简单测试 |

**典型的开发工作流程：**
```
install-deps → select-branches → install-all → build-all → verify-build → run-dev-stack → test-integration
```

**仓库位置（均在工作区中）：**

| 仓库 | 路径 |
|------|------|
| hummingbot | `~/.openclaw/workspace/hummingbot` |
| gateway | `~/.openclaw/workspace/hummingbot-gateway` |
| hummingbot-api | `~/.openclaw/workspace/hummingbot-api` |

可以通过环境变量 `HUMMINGBOT_DIR`、`GATEWAY_DIR`、`HUMMINGBOT_API_DIR` 或 `WORKSPACE` 来覆盖这些路径。

---

## 命令：install-deps

自动安装所有缺失的开发依赖项。可以安全地重新运行此命令——会跳过已安装的依赖项。

```bash
bash scripts/install_deps.sh
```

**仅安装缺失的依赖项：**
- Homebrew（macOS）
- Xcode命令行工具（macOS——用于Cython的`build_ext`构建）
- Miniconda（conda）
- Node.js v22（通过nvm、Homebrew或手动安装nvm）
- pnpm（通过npm或Homebrew）
- Git
- Docker Desktop（macOS——通过Homebrew cask或直接下载）

**选项：**
```bash
--check         # check only, don't install anything
--conda         # only install conda
--node          # only install node + nvm
--pnpm          # only install pnpm
```

**安装完成后**，请重启终端（或执行 `source ~/.zshrc`）以应用PATH设置的变化，然后运行 `check_env.sh` 进行确认。

---

## 命令：select-branches

交互式地为每个仓库选择分支，切换到相应分支，并将结果保存到 `.dev-branches` 文件中。

```bash
bash scripts/select_branches.sh
```

**非交互式选项：**
```bash
# Use development for all
bash scripts/select_branches.sh --defaults

# Specify each branch
bash scripts/select_branches.sh \
  --hummingbot development \
  --gateway core-2.7 \
  --api development
```

分支选择结果会被保存到 `$WORKSPACE/.dev-branches` 文件中，并会被 `install_all.sh`、`build_all.sh` 和 `verify-build.sh` 脚本自动读取。

---

## 命令：install-all

按正确顺序安装所有三个仓库。需要先执行 `select-branches` 命令（或使用 `--defaults` 选项）。

**执行步骤：**
1. 从 `environment.yml` 文件中移除 `solders` 依赖项（仅针对pip环境）。
2. 在 `hummingbot` 仓库中执行 `make install`。
3. 将 `solders` 包安装到 `hummingbot` 环境中（版本要求 `>=0.19.0`）。
4. 对 `gateway` 仓库执行 `pnpm install`、`pnpm build` 和 `pnpm run setup:with-defaults`。
5. 为 `hummingbot-api` 仓库创建一个新的conda环境。
6. 使用 `pip install -e <hummingbot_dir> --no-deps` 将本地源代码连接到API环境。

**选项：**
```bash
--skip-hbot      # skip hummingbot conda install
--skip-gateway   # skip gateway pnpm install
--skip-api       # skip hummingbot-api install
--no-local-hbot  # use PyPI hummingbot in API env instead of local source
```

---

## 命令：build-all

按正确顺序构建hummingbot的wheel文件及所有Docker镜像。

**构建顺序：**
1. 使用 `python setup.py bdist_wheel` 构建 `hummingbot` 的wheel文件（输出到 `dist/` 目录）。
2. 构建 `hummingbot/hummingbot:dev` Docker镜像。
3. 构建 `hummingbot/gateway:dev` Docker镜像（同时也会重新构建 `dist/` 目录）。
4. 构建 `hummingbot/hummingbot-api:dev` Docker镜像。

**每个镜像都会带有分支名称的标签**（例如：`hummingbot/gateway:core-2.7`）。

**选项：**
```bash
--wheel-only     # only build hummingbot wheel, no Docker
--no-docker      # skip all Docker builds
--no-hbot        # skip hummingbot builds
--no-gateway     # skip gateway builds
--no-api         # skip hummingbot-api builds
--tag <name>     # Docker tag (default: dev)
```

## 命令：verify-build

验证所有构建是否正确且同步。

**检查内容：**
1. 每个仓库都位于 `.dev-branches` 中指定的分支上。
2. `hummingbot` 的wheel文件存在于 `dist/` 目录中。
3. Gateway的构建版本与源代码一致且没有过时。
4. 本地hummingbot源代码在 `hummingbot-api` 环境中处于活动状态。
5. Docker镜像带有正确的分支标签。
6. 运行的服务（API和Gateway）可以访问。
7. API与Gateway之间能够正常通信。

```bash
bash scripts/verify_build.sh
```

## 命令：run-dev-stack

从源代码启动整个开发栈。

**启动顺序：**
1. 通过 `docker compose up emqx postgres -d` 启动Docker基础设施（包括postgres和EMQX）。
2. 在后台运行 `node dist/index.js --passphrase=hummingbot --dev` 来启动Gateway。
3. 在前台运行 `uvicorn main:app --reload` 来启动Hummingbot API。

**选项：**
```bash
--no-gateway           # skip gateway start
--passphrase <pass>    # gateway passphrase (default: hummingbot)
--stop                 # stop everything
--status               # show running status
```

**日志记录：**
- Gateway日志：`tail -f ~/.openclaw/workspace/.gateway.log`
- API日志：输出到终端。

---

## 命令：start

检查整个开发环境并显示状态摘要。

### 第一步：运行环境检查

```bash
bash scripts/check_env.sh --json
```

### 第二步：检查仓库分支

```bash
bash scripts/check_repos.sh --json
```

### 第三步：检查运行中的服务

```bash
bash scripts/check_api.sh --json
bash scripts/check_gateway.sh --json
```

### 第四步：显示状态检查列表

```
Dev Environment Status
======================
  [x] Prerequisites     — conda, node, pnpm, docker, git OK
  [x] Hummingbot repo   — branch: development, env: hummingbot (installed)
  [x] Gateway repo      — branch: development, built: yes
  [x] Hummingbot API    — running at http://localhost:8000
  [x] Gateway           — running at http://localhost:15888
  [ ] Local hummingbot  — hummingbot-api NOT using local source

Next: run /hummingbot-developer setup-api-dev to wire API to local source
```

根据实际情况调整流程。如果一切正常，将显示相应的测试命令。

---

## 命令：setup-hummingbot

从源代码在 `development` 分支上安装Hummingbot。

**步骤：**
1. 检查先决条件。
2. 切换到 `development` 分支。
3. 从 `environment.yml` 文件中移除 `solders` 依赖项（仅针对pip环境）。
4. 安装conda环境。

**创建`hummingbot` conda环境**。首次运行可能需要3-10分钟。

### 第五步：通过pip安装`solders`依赖项（不在conda环境中）

```bash
conda run -n hummingbot pip install "solders>=0.19.0"
```

**输出解释：**
- `conda develop .` 成功执行：开发环境安装完成，可以继续下一步。
- `PackagesNotFoundError: solders`：忘记执行第3步？请重新运行命令并重新安装依赖项。
- `Error: Conda is not found`：conda未添加到PATH中？请执行 `source ~/.zshrc` 或安装Anaconda。
- `build_ext` 出现错误：缺少构建工具？请安装Xcode CLT：`xcode-select --install`。

**安装完成后：**
```
  [x] conda env "hummingbot" created
  [x] solders installed via pip
  Run hummingbot: /hummingbot-developer run-hummingbot
  Build image:    /hummingbot-developer build-hummingbot
```

---

## 命令：run-hummingbot

从源代码运行Hummingbot CLI。

**或者通过 `make` 命令来运行：**
```bash
cd <HUMMINGBOT_DIR>
make run
```

**注意：** 这会打开交互式的Hummingbot CLI。使用 `exit` 命令退出。

**要使用特定配置运行Hummingbot CLI，请执行：**
```bash
make run ARGS="--config-file-name conf_pure_mm_1.yml"
```

---

## 命令：build-hummingbot

从源代码构建hummingbot的wheel文件和/或Docker镜像。

**构建wheel文件（用于本地pip安装）：**
```bash
cd <HUMMINGBOT_DIR>
conda activate hummingbot
pip install build wheel  # if not already installed
python -m build --wheel --no-isolation
```

构建后的wheel文件会保存在 `dist/hummingbot-*.whl` 目录中。

**重要提示：** wheel文件必须使用Python 3.12版本构建，以确保与hummingbot-api的环境兼容。

**使用此wheel文件在其他环境中安装：**
```bash
pip install dist/hummingbot-*.whl --force-reinstall --no-deps
```

**为Docker构建Linux版本的wheel文件：**
在构建hummingbot-api的Docker镜像时，需要使用Linux版本的wheel文件（不适用于macOS/Windows）。请在Docker容器内进行构建以确保兼容性：

**平台对应的wheel文件后缀：**
- `linux_x86_64` — Linux AMD/Intel 64位系统
- `linux_aarch64` — Linux ARM64系统（Apple Silicon Docker或AWS Graviton）
- `macosx_11_0_arm64` — macOS Apple Silicon系统（仅适用于本地环境，不适用于Docker）
- `macosx_10_9_x86_64` — macOS Intel系统（仅适用于本地环境，不适用于Docker）

**构建Docker镜像：**
```bash
cd <HUMMINGBOT_DIR>
docker build -t hummingbot/hummingbot:dev -f Dockerfile .
```

**或者使用 `make` 命令构建：**（构建完成后还会清理临时文件）

**用于hummingbot-api的镜像标签：**
```bash
docker build -t hummingbot/hummingbot:development -f Dockerfile .
```

**输出解释：**
- `Successfully built` + wheel文件路径：wheel文件构建成功，保存在 `dist/` 目录中。
- `Successfully tagged hummingbot/hummingbot:dev`：Docker镜像构建完成。
- `build_ext` 出现错误：可能是Cython编译问题，请检查conda环境是否正常。

---

## 命令：setup-gateway

从源代码安装和配置Gateway。

**步骤：**
1. 检查先决条件（需要Node.js 20.0以上版本、pnpm和git）。

**步骤：**
```bash
bash scripts/check_env.sh
```

**步骤：** 切换到 `development` 分支。

**步骤：** 安装依赖项。

**如果在macOS上遇到USB HID设备相关错误：**
```bash
pnpm install --force
```

**步骤：** 构建TypeScript代码。

**步骤：** 运行 `setup` 命令。

**设置完成后：**
- 会生成以下文件：**
  - `conf/`：包含链式连接、连接器、令牌和RPC配置。
  - `certs/`：包含TLS证书（开发用途的自签名证书）。

**输出解释：**
- `Gateway setup complete`：配置完成，可以运行 `run-gateway` 命令。
- 如果出现 `tsc` 编译错误，请检查Node.js版本（`node --version` 应大于或等于20）。
- 如果 `pnpm` 未安装，请执行 `npm install -g pnpm`。
- 如果出现 `ENOSPC` 错误，可能是磁盘空间不足，请释放更多空间。

---

## 命令：run-gateway**

以开发模式从源代码运行Gateway（不使用TLS）。

**默认密码与hummingbot-api配置相同：** `hummingbot`。

**`--dev` 参数的作用：**
- 以HTTP模式（不使用TLS）在端口15888上运行Gateway。
- 启用详细日志记录。
- Hummingbot API会自动连接到 `http://localhost:15888`。

**验证运行状态：**
```bash
curl http://localhost:15888/
```

**查看启动顺序的日志：**
```
Gateway listening on port 15888
Solana mainnet-beta initialized
...
```

**建议配置自定义RPC设置（以避免速率限制）：**
```bash
# After gateway is running, update RPC via API
curl -X POST http://localhost:15888/network/config \
  -H "Content-Type: application/json" \
  -d '{"chain": "solana", "network": "mainnet-beta", "nodeURL": "https://your-rpc.com"}'
```

---

## 命令：build-gateway**

从源代码构建Gateway的Docker镜像。

**构建完成后，镜像会被标记为开发版本（用于与hummingbot-api配合使用）：**
```bash
docker tag hummingbot/gateway:dev hummingbot/gateway:development
```

**验证镜像：**
```bash
docker run --rm hummingbot/gateway:dev node -e "console.log('OK')"
```

---

## 命令：setup-api-dev**

配置Hummingbot API以使用本地的Hummingbot源代码版本，而不是PyPI版本的软件包。

**步骤：**
1. 创建 `hummingbot-api` 的conda环境（使用PyPI版本的hummingbot）。

**步骤：** 将本地的hummingbot代码安装到`hummingbot-api`环境中。

**选项A：** 可编辑的安装方式（推荐用于开发环境）：
**此方式下，对hummingbot源代码的修改会立即生效，无需重新安装。**

**选项B：** 使用wheel文件安装（用于测试特定版本）：
**此方式适用于测试特定版本的hummingbot。**

**步骤：** 验证本地版本是否生效。

**应显示的路径：**
- 正常情况下，路径应在 `<HUMMINGBOT_DIR>` 目录下。
- 如果路径在 `anaconda3/.../site-packages` 目录下，说明仍在使用PyPI版本的hummingbot。

**步骤：** 安装`solders`依赖项。

**输出解释：**
- 如果路径显示在 `hummingbot` 目录下，说明本地代码已成功安装。
- 如果路径在 `anaconda3/.../site-packages` 目录下，说明仍在使用PyPI版本的hummingbot。

**步骤：** 运行 `run-api-dev`**

**步骤：**
1. 首先通过Docker启动基础设施（包括postgres和EMQX）。
**步骤：** 确认它们运行正常。

**步骤：** 使用 `uvicorn` 和热重载功能运行API。

**API的地址：** `http://localhost:8000`。
**Swagger UI的地址：** `http://localhost:8000/docs`。

**热重载的功能：** 对 `hummingbot-api` 中的`.py` 文件进行修改后，这些修改会立即生效。同时，对本地hummingbot源代码的修改也会在重新加载时得到应用。

**步骤：** 确认本地hummingbot环境已正确配置。**

**有用的开发命令：**
```bash
# Watch logs
conda run -n hummingbot-api uvicorn main:app --reload --log-level debug

# Run on different port
conda run -n hummingbot-api uvicorn main:app --reload --port 8001

# Check what's running
docker compose ps
curl http://localhost:8000/health
```

## 命令：test-integration**

对整个开发栈进行简单测试——包括API、Gateway和它们之间的通信是否正常。

**测试内容：**
- **API健康检查**：`GET /health` 请求应返回200状态码。
- **API版本检查**：确认使用的确实是本地源代码版本（而非PyPI版本）。
- **Gateway健康检查**：`GET /` 请求在端口15888上应返回200状态码。
- **API与Gateway的通信**：确认API能够连接到Gateway。
- **连接器的测试**：至少有一个连接器可以通过API访问。

**输出解释：**
- 如果所有测试项都通过，说明开发环境正常运行。

**问题排查：**
- 如果某个测试项失败，请根据输出提示进行相应的修复。