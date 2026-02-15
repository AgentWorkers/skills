---
name: agent-wallet-nwc-bridge
version: 0.1.0
description: 将本地的 @moneydevkit/agent-wallet 暴露为 Nostr Wallet Connect (NIP-47) 钱包服务（systemd 用户服务）。
repo: https://github.com/kristapsk/agent-wallet-nwc-bridge
---

# agent-wallet-nwc-bridge（技能）

该技能提供了一个小型、自托管的**Nostr钱包连接（NIP-47）**桥接器，允许NWC客户端（例如Stacker.News）向本地的**@moneydevkit/agent-wallet**发送`makeinvoice`/`payinvoice`请求。

该服务设计为以**systemd用户服务**的形式运行。

## 收获内容

- `index.js`：桥接器实现代码
- 可移植的`agent-wallet-nwc-bridge.service`系统服务单元文件（使用了 `%h` 标签）
- 安装脚本 `install_systemd_user.sh`
- 环境变量配置文件 `nwc.env` 和状态文件 `state.json`（存储在本地，不会被提交到版本控制系统中）

## 系统要求

- 支持systemd用户服务的Linux系统
- 安装了Node.js和npm
- 具备Nostr中继访问权限（示例中使用了 `wss://nos.lol`）

## 安装

```bash
git clone https://github.com/kristapsk/agent-wallet-nwc-bridge
cd agent-wallet-nwc-bridge

npm install
cp -n nwc.env.example nwc.env

# initialize state + create wallet service pubkey
node index.js init --relay wss://nos.lol

# install + start as user service
./install_systemd_user.sh

# follow logs
journalctl --user -u agent-wallet-nwc-bridge.service -f
```

## 配置

编辑 `nwc.env` 文件：

- `NWC_RELAYS`：以逗号分隔的中继服务器列表（例如 `wss://nos.lol,wss://relay.damus.io`）
- `NWC_STATE`：默认使用 `state.json` 文件（位于工作目录下）
- `NWC_AUTO REGISTER`：建议设置为 `0`（建议使用明确的URI和权限设置）
- `NWC_DEFAULT_BUDGET_SATS`：生成URI时的默认支出限额

**安全提示：** `state.json` 文件包含Nostr钱包的连接密钥，请勿将其提交到版本控制系统中。

## 典型使用流程（以Stacker.News为例）

1. 运行桥接器服务。
2. 生成用于接收NWC币的URI，并将其添加到SN钱包的UI中。
3. 生成用于发送NWC币的URI（包含支出权限），并将其添加到SN钱包中。
4. 验证端到端流程：
   - SN钱包的`makeinvoice`请求会记录在桥接器日志中。
   - SN钱包的`payinvoice`请求会被处理，并生成相应的支付记录。

## 操作说明

修改配置后，请重启服务：

```bash
systemctl --user restart agent-wallet-nwc-bridge.service
```

## 关闭服务

```bash
systemctl --user disable --now agent-wallet-nwc-bridge.service
```

## 发布到ClawHub

- 确保`README.md`、`SKILL.md`和`package.json`文件存在。
- 请将敏感配置信息（如`nwc.env`、`state.json`）保留在本地文件系统中，避免将其提交到Git仓库中（`node_modules/`目录下的文件默认不会被包含在版本控制范围内）。