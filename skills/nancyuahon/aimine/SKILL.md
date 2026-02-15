---
name: aimine
description: 在 BNB 链上挖掘 AIT（人工智能工作证明）。整个安装、配置以及启动/停止挖掘的过程都可以通过 OpenClaw 完成，无需使用终端或手动编辑文件。
metadata: {"openclaw":{"requires":{"bins":["node","npm","git"]},"primaryEnv":"PRIVATE_KEY"}}
---

# AI Mine (PoAIW) — OpenClaw 技能

该技能允许用户完全通过 OpenClaw 来**安装**、**配置**以及**启动/停止** AIT（AI-powered mining）挖矿服务。所有操作均由代理程序通过 `Exec` 功能执行；用户无需手动打开终端或编辑文件。

**支持的用户指令（英文触发短语）：**

- **安装**：例如 “install AIT mining”、“set up AIT miner”、“install the miner”
- **配置**：例如 “configure AIT mining”、“configure mining”、“set up my keys”
- **开始挖矿**：例如 “start mining”、“start AIT mining”、“begin mining”
- **停止挖矿**：例如 “stop mining”、“stop AIT mining”
- **挖矿状态**：例如 “mining status”、“status”、“how is mining doing”
- **余额查询**：例如 “AIT balance”、“check balance”、“my AIT balance”

**约定事项：**

- `AIMINE_DIR`：仓库的根目录，默认为 `~/PoAIW`。挖矿程序的目录为 `$AIMINE_DIR/miner`。
- 挖矿程序的 Web API 端口：`3000`（仅限本地主机）。
- 密钥：用户可以在 OpenClaw 技能配置中设置 `PRIVATE_KEY` 以及 `OPENAI_KEY` 或 `OPENAI_API_KEY`（通过环境变量注入），或者在对话中提供这些密钥。挖矿程序接受这两种环境变量名作为 OpenAI 密钥。之后代理程序会使用这些值来初始化挖矿程序。

---

## 当用户想要安装挖矿程序时

运行以下命令（如果设置了 `AIMINE_DIR`，则使用该目录；否则使用默认的 `$HOME/PoAIW`）：

```
AIMINE_DIR=${AIMINE_DIR:-$HOME/PoAIW}
[ -d "$AIMINE_DIR/.git" ] || git clone https://github.com/AIMineRes/PoAIW.git "$AIMINE_DIR"
cd "$AIMINE_DIR/miner" && npm install
```

请勿要求用户手动打开终端或执行这些操作。

---

## 当用户想要配置挖矿设置时

用户必须提供钱包私钥和 OpenAI API 密钥（可以在 OpenClaw 技能配置中设置为 `PRIVATE_KEY` 和 `OPENAI_KEY` 或 `OPENAI_API_KEY`，或者在对话中提供）。如果用户收到 “无效的 API 密钥” 的提示，请检查：密钥前后不应有空格，且密钥应以 “sk-” 开头。如果使用 OpenClaw 配置，请尝试设置 `OPENAI_API_KEY（某些用户界面使用该名称）。

- **如果密钥已通过环境变量设置**：运行  
  `cd "$AIMINE_DIR/miner" && npx ts-node src/index.ts init --from-env`  
  （确保 `AIMINE_DIR` 已设置，否则使用 `$HOME/PoAIW/miner`）。  
- **如果用户通过消息提供了密钥**：运行  
  `cd "$AIMINE_DIR/miner" && npx ts-node src/index.ts init --private-key <key> --openai-key <key>`  
  使用用户提供的密钥进行初始化。请勿将密钥完整显示出来。

请勿要求用户手动编辑 `.env` 或 `openclaw.json` 文件。

---

## 当用户想要开始挖矿时

运行一次性脚本（如果需要，脚本会后台启动 Web 服务器），然后调用 API。**请勿** 告诉用户先运行 `npm run web`。

```
cd "${AIMINE_DIR:-$HOME/PoAIW}/miner" && node scripts/start-mining.js
```

如果未设置 `AIMINE_DIR`，则使用 `$HOME/PoAIW`（或主机上的相应目录）。脚本会检查端口 3000 是否已有 Web 服务器正在运行，如果没有，则启动服务器；等待几秒钟后，向 `http://127.0.0.1:3000/api/start` 发送 POST 请求。

---

## 当用户想要停止挖矿时

运行以下命令：

```
curl -s -X POST http://127.0.0.1:3000/api/stop
```

---

## 当用户想要查询挖矿状态时

运行以下命令：

```
curl -s http://127.0.0.1:3000/api/status
```

然后以简短的形式总结返回 JSON 数据（`miningActive`、`blocksMined`、`tokenBalance`、`bnbBalance`、`hashRate`）。

---

## 当用户想要查询 AIT 的余额（钱包/挖矿统计信息）时

运行以下命令：

```
cd "${AIMINE_DIR:-$HOME/PoAIW}/miner" && npx ts-node src/index.ts balance
```

为用户汇总查询结果。

---

**总结：**

- **安装**：将仓库克隆到 `AIMINE_DIR`（默认为 `~/PoAIW`），然后执行 `cd miner && npm install`。
- **配置**：使用 `ai-mine init --from-env`（如果密钥已通过环境变量设置），或 `ai-mine init --private-key ... --openai-key ...`（如果用户通过对话提供了密钥）。
- **启动**：在挖矿程序目录中运行 `node scripts/start-mining.js`（无需用户执行 `npm run web`）。
- **停止**：运行 `curl -s -X POST http://127.0.0.1:3000/api/stop`。
- **状态查询**：运行 `curl -s http://127.0.0.1:3000/api/status`。
- **余额查询**：在挖矿程序目录中运行 `npx ts-node src/index.ts balance`。

请始终使用 `AIMINE_DIR/miner` 作为挖矿程序的目录；如果未设置 `AIMINE_DIR`，则默认使用 `~/PoAIW`。