---
name: vaibot-guard
description: VAIBot/OpenClaw操作采用基于策略的控制机制（Policy-gated execution），并具备防篡改的审计追踪功能（tamper-evident audit trail）。该机制用于在shell命令执行前进行预检查、拒绝操作或要求审批，并生成带有签名（哈希链技术）的日志记录，以记录操作决策及执行结果。
---
# VAIBot Guard（OpenClaw技能）

该技能提供了一项**本地策略决策服务**，以及一个名为`vaibot-guard`的命令行工具（CLI），用于执行**预执行检查**并生成**防篡改的审计日志**。

## 部署模式

- **本地工作站模式（推荐默认设置）**：将`vaibot-guard`作为**systemd用户服务**运行（使用`systemctl --user`命令），可选地与`openclaw-gateway.service`关联，以便在OpenClaw启动时自动启动（通常是在登录时）。
- **VPS/生产环境模式**：将`vaibot-guard`作为**systemd系统服务**运行（使用`sudo systemctl`命令），并采用更严格的沙箱机制，在系统启动时自动启动。

详情请参阅：`references/ops-runbook.md`。

注意：某些注册表或包管理工具可能会删除`.service`文件。该技能的`install-local`命令会在安装时自动生成相应的用户服务单元文件，因此通过Clawhub安装的软件包无需包含`systemd/*/*.service`文件。

## 快速入门（本地工作站）

### 0) 一次性安装并配置（推荐）

快速安装方法：通过一个命令完成本地安装。

安装过程将：
- 创建一个`systemd用户服务`（文件路径为`~/.config/systemd/user/vaibot-guard.service`）。
- 如果不存在，会创建`~/.config/vaibot-guard/vaibot-guard.env`文件，并设置文件权限为`0600`。
- 如果`VAIBOT_GUARD_TOKEN`尚未设置，系统会自动生成该令牌。

```bash
node scripts/vaibot-guard.mjs install-local
```

或者，您也可以选择仅运行交互式配置工具来配置`vaibot-guard.env`文件（配置完成后使用`chmod 600`命令设置文件权限）：

```bash
node scripts/vaibot-guard.mjs configure
```

### 1) 启动并执行简单测试

#### 前台模式（快速开发测试）

在`vaibot-guard`技能目录下执行相应命令：

```bash
# 1) Start the guard service (foreground)
# Reads VAIBOT_GUARD_TOKEN (and other settings) from:
#   - env vars, or
#   - ~/.config/vaibot-guard/vaibot-guard.env
node scripts/vaibot-guard-service.mjs
```

在另一个终端中执行其他命令：

```bash
# 2) Precheck + exec (example)
node scripts/vaibot-guard.mjs precheck --intent '{"tool":"system.run","action":"exec","command":"/bin/echo","cwd":".","args":["hello"],"expectedOutputs":["hello"]}'

node scripts/vaibot-guard.mjs exec --intent '{"tool":"system.run","action":"exec","command":"/bin/echo","cwd":".","args":["hello"],"expectedOutputs":["hello"]}' -- /bin/echo hello
```

#### 使用systemd服务（推荐）

安装完成后，您可以使用以下命令来管理`vaibot-guard`服务：

```bash
systemctl --user daemon-reload
systemctl --user enable --now vaibot-guard
systemctl --user status vaibot-guard --no-pager
```

注意事项：
- `install-local`命令会根据预设模板生成用户服务单元文件，因此发布或安装该技能时无需附带`systemd/*/*.service`文件。
- 也支持在VPS或生产环境中部署`vaibot-guard`作为系统服务；详情请参阅`references/ops-runbook.md`。

### 2) （可选）将VAIBot Guard的审核机制集成到OpenClaw中（通过插件桥接）

如果您使用`vaibot-guard-bridge`插件来实现与OpenClaw的集成（禁止`system.run`操作，允许`vaibot_exec`操作），请按照以下步骤操作：

```bash
# VAIBOT_GUARD_TOKEN must match what your running guard service expects.
export VAIBOT_GUARD_TOKEN="..."
node scripts/wire-openclaw-bridge.mjs

# then restart gateway
openclaw gateway restart
```

## 组件结构

- `scripts/vaibot-guard-service.mjs`：本地HTTP策略服务
  - 提供`GET /health`接口用于检查服务状态。
  - 提供`POST /v1/decide/exec`接口用于执行策略决策。
  - 提供`POST /v1/finalize`接口用于完成决策流程。
  - 提供`POST /api/proof`接口用于生成Merkle哈希证明。

- `scripts/vaibot-guard.mjs`：命令行工具的入口点，可以通过`node scripts/vaibot-guard.mjs ...`命令来运行该工具。

## 所需环境（最低配置要求）

- 主机上必须安装Node.js 18及以上版本。

可选配置参数：
- `VAIBOT_GUARD_HOST`（默认值：`127.0.0.1`）
- `VAIBOT_GUARD_PORT`（默认值：`39111`）
- `VAIBOT_WORKSPACE`（默认值：`process.cwd()`）
- `VAIBOT_GUARD_LOG_DIR`（默认值：`${VAIBOT_WORKSPACE}/.vaibot-guard`）
- `VAIBOT_GUARD_TOKEN`（推荐设置）：用于访问服务端点的令牌（如`/v1/decide/exec`、`/v1/finalize`、`/v1/flush`、`/api/proof`）。
- `VAIBOT_policy_PATH`（默认值：`references/policy.default.json`）：策略配置文件，包含令牌验证规则、允许访问的域名列表、文件修改规则等。
- `VAIBOT_CHECKPOINT_HASH_ALG`（预留参数）：用于将来将检查点哈希算法从SHA-256升级为SHA-3-512。目前仍使用SHA-256以保证一致性。
- `VAIBOT_API_URL`（例如：`https://www.vaibot.io/api`）：用于通过`/prove`接口生成验证凭证。
- `VAIBOT_API_KEY`（用于`/prove`接口的令牌）：请求头中的授权信息（格式为`Authorization:Bearer <API KEY>`）。
- `VAIBOT_PROVE_MODEL`（默认值：`vaibot-guard`）：`VAIBot `/api/prove`接口所需的模型字段。
- `VAIBOT_PROVE_MODE`（默认值：`best-effort`；推荐设置为`required`）：在“required”模式下，所有验证操作都会失败并终止。对于注重安全性的部署环境，建议设置为`required`。
- `VAIBOT_MERKLE_CHECKPOINT_EVERY`（默认值：`50`）：基于事件次数的检查点生成间隔。
- `VAIBOT_MERKLE_CHECKPOINT_EVERY_MS`（默认值：`600000`）：基于时间的检查点生成间隔（单位：毫秒）。

检查点的生成规则如下：只要满足任一阈值，并且自上次生成检查点以来有新事件发生，系统就会生成新的检查点。建议的间隔设置为10分钟，或者根据验证频率调整为几百到几千次事件。

## 必须遵守的规则

1) 确保在每台主机上启动`vaibot-guard`服务：

```bash
node scripts/vaibot-guard-service.mjs
```

2) 在执行任何可能带来风险的操作之前，必须先进行预检查：

```bash
node scripts/vaibot-guard.mjs precheck --intent '<json>'
```

3) 如果决策结果为“拒绝”，则禁止执行相关操作。

4) 如果决策结果为“批准”，则需要用户明确批准（推荐设置`approvalId`以记录审批信息）。

5) 只有在获得明确批准后，才能执行相关操作：

```bash
node scripts/vaibot-guard.mjs exec --intent '<json>' -- <command...>
```

6) 确保操作完成后会自动完成流程（`exec`命令会在执行完成后自动调用；您也可以手动调用该命令）：

```bash
node scripts/vaibot-guard.mjs finalize --run_id <id> --result '<json>'
```

## 请求数据格式（最低要求）

`vaibot-guard`服务至少需要接收以下字段：

```json
{
  "tool": "system.run",
  "action": "exec",
  "command": "/usr/bin/uname",
  "cwd": "."
}
```

建议添加的额外字段（根据实际需求使用）：
- `args`：字符串数组
- `env_keys`：字符串数组
- `network`：对象，包含允许访问的目标地址列表
- `files`：对象，包含允许读写/删除的文件列表
- `correlation`：对象，包含代理ID、会话ID和跟踪ID等信息

## 更详细的配置信息请参阅

- `references/policy.md`：策略配置指南
- `references/receipt-schema.md`：请求数据格式规范
- `references/checkpoint-schema.md`：检查点生成规则
- `references/idempotency.md`：幂等性相关说明
- `references/metadata-indexing.md`：元数据索引机制
- `references/merkle-replay.md`：Merkle哈希验证相关文档
- `references/inclusion-proofs.md`：包含证明文件的相关说明
- `references/required-mode.md`：安全策略要求

## 输出与日志记录

- 所有的决策结果和操作完成信息会被记录到`.vaibot-guard/`目录下的JSONL日志文件中，这些日志采用哈希链格式存储，具有防篡改功能（每条日志记录都会包含前一个检查点的哈希值）。