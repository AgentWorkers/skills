---
name: agent-spawner
description: 通过对话方式生成一个新的 OpenClaw 代理。该过程使用官方的 Docker 设置进行非交互式的初始化，并继承当前代理的 API 密钥、工具、插件以及技能。用户需要回答 2-3 个问题。适用于用户希望创建、启动、部署或配置新的 OpenClaw 代理的场景。
---
# 代理生成器（Agent Spawner）

以对话方式部署一个新的 OpenClaw 代理。支持官方安装方式，也可以从现有代理中继承配置。用户无需手动编辑任何文件。

## 1. 读取当前配置（静默模式）

```bash
cat ~/.openclaw/openclaw.json
cat ~/.openclaw/.env 2>/dev/null
env | grep -iE 'API_KEY|TOKEN'
ls ~/.openclaw/extensions/
ls <workspace>/skills/
```

需要确认的配置项包括：
- **提供者（Provider）**：查看配置文件中的 `auth.profiles` — 可能包括 Anthropic、OpenAI、Gemini 或自定义提供者等。
- **API 密钥（API Key）**：来自环境变量或配置文件（例如 `ANTHROPIC_API_KEY`、`GEMINI_API_KEY`、`OPENAI_API_KEY`）。
- **模型（Model）**：来自 `agentsdefaults.model`。
- **工具键（Tool Keys）**：所有以 `tools.*` 开头的配置项（用于调用外部 API 等）。
- **插件（Plugins）**：`plugins.installs` 中列出的插件及其 npm 依赖信息。
- **技能（Skills）**：运行 `openclaw skills list` 命令查看哪些技能是默认提供的，哪些是仅在工作区中使用的。仅需要迁移非默认提供的技能。

## 2. 用户提问

1. **“应该部署在哪里？”**：可以选择 Docker 容器（本地或远程 SSH 服务器）或裸机（bare metal）。
2. **“需要给容器起什么名字？”**：如果用户不指定，系统会自动生成一个名称。
3. **“有什么特殊要求吗？”**：例如部署目的或使用限制等。这些问题可选。

请不要询问关于 API 密钥、插件、技能、端口或配置文件的具体内容。所有这些信息都会从现有代理中继承过来，系统会使用默认值。

## 3. 确认部署计划

收集用户信息后，先向用户展示完整的部署方案。将所有相关信息汇总在一个报告中：

```
Here's the plan:

📦 Deploy: Docker on <target>
📛 Name: <agent-name>
🌐 Port: <port>

Carrying over from current agent:
  ✅ Provider: Anthropic (API key)
  ✅ Model: anthropic/claude-sonnet-4-20250514
  ✅ Brave Search API key
  ✅ Plugins: openclaw-agent-reach
  ✅ Skills: agent-spawner, weather
  ✅ Heartbeat: 30m

The new agent will bootstrap its own identity on first message.

Good to go?
```

仅列出实际存在的配置项。在继续操作之前，请用户明确确认所有内容。如果用户需要修改配置，请先进行调整后再确认。

## 4. 部署代理

### 使用 Docker 容器

```bash
git clone https://github.com/openclaw/openclaw.git <agent-name>
cd <agent-name>
```

设置环境变量并执行非交互式的部署命令。确保使用的环境变量与步骤 1 中检测到的提供者相匹配：

```bash
export OPENCLAW_IMAGE=alpine/openclaw:latest
export OPENCLAW_CONFIG_DIR=~/.openclaw-<agent-name>
export OPENCLAW_WORKSPACE_DIR=~/.openclaw-<agent-name>/workspace
export OPENCLAW_GATEWAY_PORT=<unused port, default 18789>
export OPENCLAW_GATEWAY_BIND=lan

mkdir -p $OPENCLAW_CONFIG_DIR/workspace
```

不同提供者的具体部署参数如下：
| 提供者（Provider） | 需要设置的参数（Parameter） |
|-----------------|----------------------|
| Anthropic     | `apiKey`                | `--anthropic-api-key`          |
| Gemini       | `gemini-api-key`            | `--gemini-api-key`          |
| OpenAI       | `apiKey`                | （设置环境变量 `OPENAI_API_KEY`）     |
| 自定义提供者（Custom） | `custom-api-key`          | `--custom-api-key`          | `--custom-base-url`          | `--custom-model-id`         |

```bash
docker compose run --rm openclaw-cli onboard --non-interactive --accept-risk \
  --mode local \
  --auth-choice <detected> \
  --<provider>-api-key "$API_KEY" \
  --gateway-port 18789 \
  --gateway-bind lan \
  --skip-skills

docker compose up -d openclaw-gateway
```

官方推荐的部署方式使用 **bind mounts** — 这种方式下，宿主机用户拥有文件的所有权，因此不会出现权限问题。

在部署过程中，可能会遇到与网关连接相关的问题（因为网关可能尚未启动）。此时系统会自动写入配置文件。

### 使用裸机

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard

openclaw onboard --non-interactive --accept-risk \
  --mode local \
  --auth-choice <detected> \
  --<provider>-api-key "$API_KEY" \
  --gateway-port 18789 \
  --gateway-bind lan \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

## 5. 更新现有代理的配置

### 使用 Docker 容器

通过 CLI 命令更新代理配置：
- Docker：`OC="docker compose exec openclaw-gateway node /app/openclaw.mjs"`
- 裸机：`OC="openclaw"`

**仅更新现有代理中实际存在的配置项：**

```bash
$OC config set agents.defaults.model "<model>"
$OC config set agents.defaults.heartbeat.every "30m"
# Tool keys — only if they exist in current config
$OC config set tools.web.search.apiKey "<key>"
```

### 更新插件配置

插件信息来自当前配置文件中的 `plugins.installs` 部分：

```bash
$OC plugins install <npm-spec>
# Repeat for each plugin
```

### 复制技能配置

将当前工作区中的技能配置复制到新代理中：

```bash
# Docker
docker cp <source-workspace>/skills/ <container>:/home/node/.openclaw/workspace/skills/
# Bare metal
cp -r <source-workspace>/skills/ ~/.openclaw/workspace/skills/
```

### 重启代理

部署完成后，需要重启代理：

```bash
docker compose restart openclaw-gateway  # Docker
openclaw gateway restart                 # bare metal
```

## 6. 交付使用结果

向用户提供代理的访问信息：
- **访问地址（URL）**：`http://<host>:<port>/`
- **访问令牌（Token）**：从配置文件中获取（系统会在部署时自动生成）。
- “输入 ‘hello’ 来启动代理。”

## 注意事项：

- 在 Docker 环境中，`openclaw` 命令不在系统的 PATH 变量中。需要使用 `node /app/openclaw.mjs` 来启动代理。
- 对于非交互式部署，必须使用 `--accept-risk` 参数。
- 推荐使用预构建的官方 Docker 镜像 `alpine/openclaw:latest`。
- 不要使用带有名称的 Docker 卷（否则会导致 root 权限问题）。官方推荐的部署方式使用 bind mounts。
- 如果在同一台主机上部署多个代理，请为每个代理设置不同的 `OPENCLAW_CONFIG_DIR` 和 `OPENCLAW_GATEWAY_PORT`。
- 插件和技能数据会保存在 `~/.openclaw/` 目录中（`extensions/` 和 `workspace/skills/` 子目录下）。
- SSH 密钥、Git 配置文件以及 Apt 包等临时文件不会被保存在 Docker 卷中。