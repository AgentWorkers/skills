---
name: tellermcp-mcp
description: 暴露 Teller 的 delta 中性（delta-neutral）借贷模型上下文协议（delta-neutral lending model context protocol）服务器。当您需要安装、运行或更新 Tellermcp MCP 后端时，请使用该服务器，以便代理（agents）能够获取交易机会（transaction opportunities）、借款条款（borrowing terms）以及用于 Teller 的链上交易构建器（on-chain transaction builders）。
---
# Tellermcp MCP 技能

## 概述
此技能包含一个可立即运行的 MCP 服务器（`scripts/tellermcp-server/`），该服务器提供了 Teller 的Delta-Neutral套利数据、借款池信息、借款条款、借款交易生成工具以及还款辅助功能。在以下情况下需要使用此技能：
- 部署或修改 Tellermcp MCP 服务器
- 重新运行 `npm install`、构建或测试服务器
- 将 Tellermcp 注册到 mcporter/OpenClaw，以便代理可以通过 MCP 工具访问 Teller 的 API

## 快速入门
1. 进入 `scripts/tellermcp-server` 目录
2. 运行 `npm install`
3. （可选）配置环境变量：
   - `TELLER_API_BASE_URL`（默认值为 `https://delta-neutral-api.teller.org`）
   - `TELLER_API_TIMEOUT_MS`（默认值为 15000 毫秒）
4. 运行 `npm run build` 进行 TypeScript 类型检查
5. 运行 `npm start`，通过标准输入（STDIO）启动 `tellermcp` MCP 服务器

## 仓库结构（`scripts/tellermcp-server/`）
- `package.json` / `package-lock.json` – Node 20+ 项目的元数据
- `tsconfig.json` – ES2022/ESNext 构建目标
- `src/client.ts` – 类型化的 Teller REST 客户端（包含请求封装和过滤逻辑）
- `src/types.ts` – 所有 Teller 响应的 TypeScript 接口
- `src/index.ts` – MCP 服务器的逻辑实现（包括以下工具的注册功能）：
  1. `get-delta-neutral-opportunities`（获取 Delta-Neutral 套利机会）
  2. `get-borrow-pools`（获取借款池信息）
  3. `get-borrow-terms`（获取借款条款）
  4. `build-borrow-transactions`（生成借款交易）
  5. `get-wallet-loans`（获取钱包借款信息）
  6. `build-repay-transactions`（生成还款交易）

每个工具都会返回：简短的文本摘要以及包含原始 JSON 数据的 `structuredContent.payload`，以便后续自动化处理。

## 运行流程
### 安装依赖项
```bash
cd scripts/tellermcp-server
npm install
```
该项目故意省略了 `node_modules/` 和 `dist/` 目录；`npm install` 和 `npm run build` 会重新生成这些目录。

### 本地测试
- 运行 `npm build` 进行 TypeScript 编译
- 运行 `npm start` 启动 MCP 服务器。如果后续需要添加更多测试，可以使用 `gh pr checks` 或 `npm test`。

### 在 mcporter/OpenClaw 中注册
在您的 `mcporter`（或代理传输层）配置文件中添加相应的条目：
```jsonc
{
  "name": "tellermcp",
  "command": "npm",
  "args": ["start"],
  "cwd": "/absolute/path/to/scripts/tellermcp-server"
}
```
重新启动 mcporter 后，Codex 代理就可以直接调用这六个 Teller 工具了。

### 部署更新
1. 修改 `src/` 目录下的 TypeScript 文件
2. 在本地运行 `npm build`
3. 通过 GitHub 提交代码并推送更改（如果需要同步到 `teller-protocol/teller-mcp`）
4. 重新启动 mcporter 进程以应用这些更改

## 参考资料
- [references/delta-neutral-api.md](references/delta-neutral-api.md) – Teller API 的简要说明（端点、参数、缓存行为）。在需要详细 REST 接口信息时请参考此文件。

## 打包此技能
当准备发布 `.skill` 包时：
```bash
python3 /usr/local/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py /data/workspace/skills/tellermcp-mcp
```
打包工具会验证 SKILL.md 文件及所有资源，并生成 `tellermcp-mcp.skill`（zip 文件）以供分发。