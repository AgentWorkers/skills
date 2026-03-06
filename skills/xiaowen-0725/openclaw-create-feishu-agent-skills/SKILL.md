---
name: openclaw-create-agent
description: 创建并配置一个新的 OpenClaw 代理，该代理遵循固定的工作流程。此功能适用于以下场景：用户请求创建/添加新的 OpenClaw 代理时；需要自动化 Feishu 系统中多个代理的配置；需要修改 `~/.openclaw/openclaw.json` 文件中的通道账户、绑定信息以及 `session.dmScope` 设置；或者需要执行后续操作（如重启代理服务器或验证绑定配置）。
---
# 创建 OpenClaw 代理

使用此技能可以一次性创建一个新的 OpenClaw 代理，并完成路由/配置的更新。

此技能仅适用于 Feishu 平台，切勿用于 Telegram、Slack 或其他渠道。

## 必需输入信息

首先确认用户的目标场景，然后收集所需的字段。仅收集缺失的必填字段。

**场景确认问题（必须首先询问）：**
- 选项 A：创建一个新的机器人/应用程序，并将其映射到一个新的代理（`routing_mode=account`）
- 选项 B：将现有的/新的群组映射到同一个机器人下的新代理（`routing_mode=peer`）

| 字段 | 是否必填 | 备注 |
| --- | --- | --- |
| `agent_id` | 是 | 仅允许使用小写字母、数字和 `-` |
| `workspace` | 是 | 使用项目的绝对路径作为工作空间 |
| `model` | 否 | 可选，用于指定该代理的模型 |
| `routing_mode` | 是 | `account` 或 `peer` |
| `channel` | 否 | 固定为 `feishu` |

**对于 `routing_mode=account`（每个代理对应一个机器人）：** 需要收集以下信息：  
- `account_id`（必填）  
- `app_id`、`app_secret`、`bot_name`（可选，但推荐提供）

**对于 `routing_mode=peer`（单个机器人，多个群组）：** 需要收集以下信息：  
- `peer_kind`（`group` 或 `direct`，必填）  
- `peer_id`（必填）  
- `account_id`（可选，提供后可以缩小匹配范围）  
- 如果是新创建的群组，则仅在完成步骤 0.5 的引导流程后收集 `peer_id`  

## 工作流程**

1. 确认场景（每个代理对应一个新机器人或多个群组）。  
2. 对于多群组场景，执行步骤 0.5 中的引导流程。  
3. 读取当前配置并备份。  
4. 使用 OpenClaw CLI 创建代理运行时环境。  
5. 更新代理的配置信息，包括通道、账户绑定和 `dmScope` 设置。  
6. 重启代理并验证配置是否正确。  
7. 返回详细的变更总结。  

## 步骤 0：确认需求  

首先询问用户的需求：  
```text
你是要哪一种？
1) 新建一个机器人，对应一个新 Agent（account 路由）
2) 已有一个机器人，在新群里绑定一个新 Agent（peer 路由）
```  

根据用户的回答选择相应的 `routing_mode`：  
- 选项 1 → `routing_mode=account`  
- 选项 2 → `routing_mode=peer`  

如果用户的回答不明确，请停止操作并先澄清需求，再继续编辑配置。  

## 步骤 0.5：多群组引导流程  

当用户需要为多个群组创建代理时，请执行此步骤：  
1. 引导用户创建一个新的群组，并将机器人添加到该群组中。  
2. 暂停并等待用户确认：“已创建群组”。  
3. 在收到确认后，引导用户在群组中发送一条消息以生成日志。  
4. 暂停并等待用户确认：“已发送”。  
5. 在收到确认后，检查 OpenClaw 日志并提取 `chat_id`（格式为 `oc_xxxxx`）。  

**建议使用的命令：**  
```bash
openclaw logs --follow
```  

**日志中应出现的提示信息：**  
```text
Received message from peer: { kind: "group", id: "oc_xxxxxxxxxxxxxxxx" }
```  

## 步骤 1：预检查和备份  

运行以下命令：  
```bash
test -f ~/.openclaw/openclaw.json
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d%H%M%S)
```  

如果配置文件缺失，请停止操作并要求用户先初始化 OpenClaw。  

## 步骤 2：创建代理运行时环境  

首先运行 OpenClaw CLI（此步骤为必填）：  
```bash
openclaw agents add <agent_id> --workspace <workspace> --non-interactive
```  

如果用户提供了模型信息：  
```bash
openclaw agents add <agent_id> --workspace <workspace> --model <model> --non-interactive
```  

## 步骤 3：更新 `openclaw.json` 配置文件  

使用随附的脚本：  
```bash
python3 scripts/upsert_openclaw_agent.py \
  --config ~/.openclaw/openclaw.json \
  --agent-id <agent_id> \
  --routing-mode <account|peer> \
  [--account-id <account_id>] \
  [--app-id <app_id>] \
  [--app-secret <app_secret>] \
  [--bot-name <bot_name>] \
  [--peer-kind <group|direct>] \
  [--peer-id <peer_id>]
```  

请从该技能文件夹中运行此脚本，或用该脚本的绝对路径替换 `scripts/upsert_openclaw_agent.py`。  
脚本功能：  
- 当使用 `routing_mode=account` 时，更新 `channels.<channel>.accounts.<account_id>` 的配置；  
- 为该代理创建一个绑定关系；  
- 在多代理的 Feishu 环境中，始终设置 `session.dmScope = per-account-channel-peer`。  

**建议参考文档：**  
[references/routing-modes.md](references/routing-modes.md) （在路由方式不明确时请参考此文档。）  

## 步骤 4：重启并验证配置  

运行以下命令：  
```bash
openclaw gateway restart
openclaw agents list --bindings
```  

验证以下内容：  
- 目标代理是否已成功创建并显示在列表中；  
- 绑定关系是否正确地指向预期的通道/账户或通道/代理。  

## 步骤 5：返回结果  

返回以下信息：  
- 创建/更新的绑定关系详情；  
- 是否添加或更新了账户信息；  
- `dmScope` 设置是否发生了变化；  
- 配置验证的结果。  

## 限制条件：  
- 保持现有代理、账户和绑定关系的不变性；  
- 避免路由冲突（同一通道/账户/代理已被其他代理使用）；  
- 除非用户明确要求交互式操作，否则不显示交互式提示；  
- 假设所有通道均为 `feishu`；  
- 在多群组场景中，只有在收到“已创建群组”和“已发送”的确认后，才能继续执行后续步骤。