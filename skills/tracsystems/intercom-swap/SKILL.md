---
name: intercomswap
description: "安装并使用 Intercom Swap：这是一个基于 P2P 技术的 RFQ（Request for Quote）交换平台，支持通过侧链进行 BTC（Lightning Network）与 USDT（Solana）之间的交易。该平台采用共享的托管程序来确保交易的安全性。用户需要提供自己的钱包信息、后端服务配置以及 RPC（Remote Procedure Call）设置；平台可能执行网络相关的代码（例如使用 pinned dependencies 或 docker 镜像进行测试）。所有金融交易操作必须经过人工审批。"
disable-model-invocation: true
disable-autonomous-invocation: true
require-user-approval: true
metadata:
  openclaw:
    category: "p2p-swap"
    risk: "financial"
    purpose: "P2P RFQ swap negotiation over sidechannels; settlement is BTC(LN) <> USDT(Solana)."
    requires:
      network: true
      local_exec: true
      # This skill must run from an operator-provisioned workspace. Do not allow an agent to self-install.
      install_mode: "operator_preprovisioned"
      runtime_downloads: "disallowed_for_agents"
      external_code_fetch:
        - "pinned git dependencies (npm git pins; operator-controlled install)"
        - "optional docker images for LN regtest e2e (test-only; operator-controlled)"
      env:
        - "INTERCOMSWAP_PROMPTD_CONFIG (promptd setup JSON path)"
      optional_env:
        - "OPENAI_API_KEY (prompt-mode only)"
        - "OPENAI_BASE_URL (prompt-mode only)"
        - "OPENAI_MODEL (prompt-mode only)"
      credentials:
        - "Solana signer keypair file path (signing authority)"
        - "Solana RPC endpoint(s)"
        - "Lightning backend credentials (CLN RPC/socket OR LND rpcserver+tls+macaroon+wallet unlock/password file)"
      config_paths:
        - "onchain/** (gitignored; keys/wallets/logs; treat as secrets)"
        - "stores/** (gitignored; peer identities/state; treat as secrets)"
        - "onchain/prompt/*.json (runtime config; may reference secrets)"
    autonomous_invocation: "manual_only"
    approval_required_for:
      - "any LN payment/channel open/close/withdraw/rebalance"
      - "any Solana tx signing/broadcasting on devnet/mainnet"
      - "any mainnet funds movement"
    disable-model-invocation: true
    disable-autonomous-invocation: true
    require-user-approval: true
always: false
autonomous_invocation: "manual_only"
requires_network: true
requires_local_exec: true
required_env_vars:
  # promptd setup JSON path used by the operator/agent runtime
  - INTERCOMSWAP_PROMPTD_CONFIG
optional_env_vars:
  # only required when using Collin prompt-mode / LLM-driven tool calls
  - OPENAI_API_KEY
  - OPENAI_BASE_URL
  - OPENAI_MODEL
required_credentials:
  - "Solana signer keypair file path + funded signer (SOL for fees; USDT inventory if acting as USDT maker)"
  - "Solana RPC endpoint(s) (devnet/mainnet)"
  - "Lightning backend credentials: CLN (RPC/socket) OR LND (rpcserver + tls cert + macaroon + wallet unlock/password file)"
required_config:
  - "promptd setup JSON (templates live under onchain/prompt/*.json; do not commit secrets)"
  - "peer store name/path (stores/**; never run the same store twice in parallel)"
  - "LN network/backend selection (CLN/LND, regtest/mainnet) and any required local binaries or docker access"
sensitive_paths:
  - "onchain/** (keys, wallets, logs; gitignored; treat as secrets)"
  - "stores/** (peer identities/state; gitignored; treat as secrets)"
  - "onchain/prompt/*.json (runtime config; may reference secrets)"
approval_required_for:
  - "Any Lightning payment, channel open/close, withdrawal, or rebalance"
  - "Any Solana transaction signing/broadcasting on devnet/mainnet (escrow init/claim/refund, config setters)"
  - "Any action that moves real funds on mainnet"
risk_notes:
  - "Uses pinned upstream dependencies; any install/update fetch is operator-controlled and should be reviewed. Runtime does not auto-update. Optional docker LN regtest e2e is test-only."
  - "Performs financial operations (LN payments/channel ops, Solana signing). Require explicit approval for mainnet actions."
---
# 交换技能  
## 描述  
此仓库（`TracSystems/intercom-swap`）是上游 Intercom（`Trac-Systems/intercom`：https://github.com/Trac-Systems/intercom`）的**分支**。  

Intercom 是一种用于自主代理（例如 OpenClaw）的技能，它通过点对点（P2P）路由**所有代理之间的通信**。它提供了安全、低延迟的 P2P 通道（子通道）、稀疏的数据存储和共享、一个用于协调的免费智能合约层（包括内置的合约聊天系统），以及一个可选的价值转移层用于支付和合约结算。代理可以打开自定义的/私有的通道以便在需要时进行通信。