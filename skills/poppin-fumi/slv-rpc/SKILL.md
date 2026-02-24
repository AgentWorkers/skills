# SLV RPC 技能

提供用于部署和管理 Solana RPC 节点（主网、测试网、开发网）的 Ansible 演示剧本和 Jinja2 模板。

## 支持的 RPC 类型

| 类型 | 描述 |
|---|---|
| `RPC` | 标准 RPC 节点 |
| `Index RPC` | 全索引 RPC 节点（使用 Old Faithful/yellowstone-faithful） |
| `Geyser gRPC` | 带有 Geyser gRPC 流式的 RPC |
| `Index RPC + gRPC` | 全索引 + gRPC 流式 |

## 目录结构

```
ansible/
  mainnet-rpc/   — Mainnet RPC playbooks
  testnet-rpc/   — Testnet RPC playbooks
  devnet-rpc/    — Devnet RPC playbooks
  cmn/           — Shared common playbooks
jinja/
  mainnet-rpc/   — Mainnet Jinja2 templates
  testnet-rpc/   — Testnet Jinja2 templates
  devnet-rpc/    — Devnet Jinja2 templates
  cmn/           — Shared templates
```

## CLI 命令 ↔ 演示剧本映射

`slv r` CLI 命令直接对应以下演示剧本。`{net}` 表示 `mainnet-rpc`、`testnet-rpc` 或 `devnet-rpc`：

| CLI 命令 | 演示剧本 | 描述 |
|---|---|---|
| `slv r deploy` | `{net}/init.yml` | 完整 RPC 节点初始化和部署 |
| `slv r start` | `{net}/start_node.yml` | 启动 RPC 节点 |
| `slv r stop` | `{net}/stop_node.yml` | 停止 RPC 节点 |
| `slv r restart` | `{net}/restart_node.yml` | 重启 RPC 节点 |
| `slv r build:solana` | `{net}/install_solana.yml` | 从源代码构建 Solana |
| `slv r install:solana` | `cmn/install_solana.yml` | 安装 Solana 可执行文件（已弃用，建议使用构建方式） |
| `slv r setup:firedancer` | `{net}/setup_firedancer.yml` | 设置 Firedancer |
| `slv r update:firedancer` | `cmn/update_firedancer.yml` | 更新 Firedancer 可执行文件 |
| `slv r update:script` | `{net}/update_startup_config.yml` | 从模板更新 start-validator.sh 脚本 |
| `slv r update:geyser` | `{net}/update_geyser.yml` | 更新 Geyser 插件 |
| `slv r get:snapshot` | `{net}/wget_snapshot.yml` | 通过 aria2c 下载快照 |
| `slv r cleanup` | `cmn/rm_ledger.yml` | 删除账本/快照文件 |
| `slv r list` | *(无演示剧本)* | 列出 RPC 节点（仅限 CLI） |
| `slv r update:allowed-ips` | *(无演示剧本)* | 更新允许的 IP 地址（仅限 CLI） |
| `slv r init` | *(无演示剧本)* | 交互式向导（仅限 CLI） |

## 所有演示剧本

### 主网 RPC (`mainnet-rpc/`)

| 演示剧本 | 描述 |
|---|---|
| `init.yml` | 完整 RPC 节点初始化 |
| `init_richat_geyser.yml` | 初始化 Richat Geyser 配置 |
| `restart_node.yml` | 重启 RPC 节点 |
| `start_node.yml` | 启动 RPC 节点 |
| `stop_node.yml` | 停止 RPC 节点 |
| `install_solana.yml` | 从源代码构建 Solana |
| `install_agave.yml` | 从源代码构建 Agave |
| `install_jito.yml` | 从源代码构建 Jito |
| `install_rust.yml` | 安装 Rust 工具链 |
| `install_package.yml` | 安装系统包 |
| `install_richat.yml` | 安装 Richat gRPC 插件 |
| `install_of1.yml` | 安装 Old Faithful（yellowstone-faithful） |
| `install_of1_service.yml` | 设置 Old Faithful 的 systemd 服务 |
| `geyser_build.yml` | 从源代码构建 Yellowstone gRPC |
| `geyser_richat_build.yml` | 从源代码构建 Richat gRPC 插件 |
| `update_geyser.yml` | 更新 Geyser 插件 |
| `update_startup_config.yml` | 从模板更新 start-validator.sh 脚本 |
| `update_ubuntu.yml` | 更新 Ubuntu 包 |
| `setup_firedancer.yml` | 设置 Firedancer |
| `setup-solv-service.yml` | 设置 systemd 服务 |
| `start-solv-service.yml` | 启动 systemd 服务 |
| `setup_ufw.yml` | 配置 UFW 防火墙 |
| `setup_logrotate.yml` | 设置日志轮换 |
| `setup_norestart.yml` | 禁用自动重启 |
| `configure_hugetlbfs.yml` | 为 Firedancer 配置 hugepages |
| `fail2ban_solana_rate_limit.yml` | 设置 fail2ban 速率限制 |
| `fail2ban_sshd.yml` | 为 SSH 设置 fail2ban |
| `allow_ufw.yml` | 添加 UFW 允许规则 |
| `add_solv.yml` | 添加 solv 用户 |
| `copy_keys.yml` | 复制节点密钥 |
| `create-start-validator-sh.yml` | 从模板生成启动脚本 |
| `create-symlink.yml` | 创建版本符号链接 |
| `mount_disks.yml` | 挂载和格式化磁盘 |
| `optimize_system.yml` | 优化系统设置 |
| `run_restarter.yml` | 运行重启脚本 |
| `run_snapshot_finder.yml` | 查找并下载最佳快照 |

### 测试网 RPC (`testnet-rpc/`)

| 演示剧本 | 描述 |
|---|---|
| `init.yml` | 完整测试网 RPC 初始化 |
| `restart_node.yml` | 重启节点 |
| `start_node.yml` / `stop_node.yml` | 启动/停止节点 |
| `install_solana.yml` | 从源代码构建 Solana |
| `install_agave.yml` / `install_jito.yml` | 从源代码构建客户端 |
| `install_richat.yml` | 安装 Richat 插件 |
| `geyser_build.yml` | 构建 Yellowstone gRPC |
| `geyser_richat_build.yml` | 从源代码构建 Richat 插件 |
| `update_geyser.yml` | 更新 Geyser 插件 |
| `update_firedancer.yml` | 更新 Firedancer |
| `update_startup_config.yml` | 更新启动脚本 |
| `setup_firedancer.yml` | 设置 Firedancer |
| `setup_solv_service.yml` | 设置 systemd 服务 |
| `create-start-validator-sh.yml` | 生成启动脚本 |
| `wget_snapshot.yml` | 下载快照 |

### 开发网 RPC (`devnet-rpc/`)

| 演示剧本 | 描述 |
|---|---|
| `init.yml` | 完整开发网 RPC 初始化 |
| `restart_node.yml` | 重启节点 |
| `start_node.yml` / `stop_node.yml` | 启动/停止节点 |
| `install_solana.yml` | 从源代码构建 Solana |
| `install_agave.yml` / `install_jito.yml` | 从源代码构建客户端 |
| `install_richat.yml` | 安装 Richat 插件 |
| `geyser_build.yml` | 构建 Yellowstone gRPC |
| `geyser_richat_build.yml` | 从源代码构建 Richat 插件 |
| `update_geyser.yml` | 更新 Geyser 插件 |
| `update_startup_config.yml` | 更新启动脚本 |
| `setup_firedancer.yml` | 设置 Firedancer |
| `setup_solv_service.yml` | 设置 systemd 服务 |
| `create-start-validator-sh.yml` | 生成启动脚本 |

### 公共脚本 (`cmn/`)

| 演示剧本 | 描述 |
|---|---|
| `build_solana.yml` | 从源代码构建 Solana（派生自 build_agave/build_jito） |
| `build_agave.yml` | 从 GitHub 源代码构建 Agave |
| `build_jito.yml` | 从 GitHub 源代码构建 Jito |
| `install_solana.yml` | 安装 Solana 可执行文件（已弃用） |
| `install_package.yml` | 安装系统包 |
| `install_rust.yml` | 安装 Rust 工具链 |
| `mount_disks.yml` / `mount-disks.yml` | 挂载和格式化磁盘 |
| `optimize_system.yml` | 优化系统设置 |
| `disable_swap.yml` | 禁用交换分区 |
| `setup_logrotate.yml` | 配置日志轮换 |
| `setup_node_exporter.yml` | 设置 Prometheus 节点导出器 |
| `setup_norestart.yml` | 禁用自动重启 |
| `setup_unstaked_identity.yml` | 设置未质押的身份密钥对 |
| `restart_solv.yml` | 重启 solv 服务 |
| `start_solv.yml` / `stop_solv.yml` | 启动/停止 solv 服务 |
| `start_firedancer.yml` / `stop_firedancer.yml` | 启动/停止 Firedancer |
| `copy_restart_sh.yml` | 复制重启脚本 |
| `copy_rpc_keys.yml` | 复制 RPC 密钥 |
| `update_ubuntu.yml` | 更新 Ubuntu 包 |
| `wget_snapshot.yml` | 下载快照 |
| `add_solv.yml` | 添加 solv 用户 |
| `fix_permissions.yml` | 修改文件权限 |

## 关键变量（`extra_vars`）

| 变量 | 描述 | 默认值 |
|---|---|---|
| `rpc_type` | RPC 节点类型（`RPC`, `Index RPC`, `Geyser gRPC`, `Index RPC + gRPC`） | `RPC` |
| `validator_type` | 客户端类型（`agave`, `jito`, `firedancer-agave`, `firedancer-jito`） | — |
| `solana_version` | Solana/Agave 版本 | — |
| `jito_version` | Jito 版本 | — |
| `firedancer_version` | Firedancer 版本 | — |
| `yellowstone_grpc_version` | Yellowstone gRPC 版本 | — |
| `richat_version` | Richat 插件版本（例如 `richat-v8.1.0`） | — |
| `snapshot_url` | 快照下载 URL | — |
| `tpu_peer_address` | TPU 对等地址（用于 Index RPC 交易转发） | — |
| `limit_ledger_size` | 账本大小限制 | `200000000`（Index），`100000000`（其他类型） |
| `dynamic_port_range` | 端口范围 | `8000-8025` |
| `port_rpc` | RPC 端口 | `8899` |
| `port_grpc` | gRPC 端口 | `10000` |

## Geyser 插件来源

这两个插件都是从源代码构建的（无二进制文件下载）：
- **Yellowstone gRPC**: https://github.com/rpcpool/yellowstone-grpc
- **Richat**: https://github.com/lamports-dev/richat

## 使用方法

```bash
ansible-playbook -i inventory mainnet-rpc/init.yml \
  -e '{"rpc_type":"Index RPC","solana_version":"3.1.8","snapshot_url":"https://..."}'
```

不需要 `versions.yml` 文件——所有变量都可以通过 `extra_vars` 传递。

## 交互式部署流程

请参阅 `AGENT.md` 以获取完整的逐步流程，以及 `examples/inventory.yml` 以了解输出格式。

### 必需变量

| 变量 | 提示 | 验证 |
|---|---|---|
| `server_ip` | “目标服务器 IP？” | 有效的 IPv4 地址 |
| `network` | “主网、测试网还是开发网？” | `mainnet`, `testnet`, `devnet` |
| `region` | “服务器区域？” | 字符串 |
| `rpc_type` | “RPC 类型？” | `RPC`, `Index RPC`, `Geyser gRPC`, `Index RPC + gRPC` |
| `validator_type` | “底层客户端类型？” | `agave`, `jito`, `jito-bam`, `firedancer-agave` |
| `solana_version` | “Solana 版本？”（默认：3.1.8） | Semver 格式 |
| `identity_account` | “节点身份公钥？” | Base58 公钥 |
| `snapshot_url` | “快照 URL？”（ERPC 时自动提供） | 必须提供（初始化时不能为空） |

### 条件性必需变量

| 变量 | 默认值 | 需要的条件 |
|---|---|---|
| `jito_version` | 必须与 `solana_version` 匹配 | `jito/jito-bam` 类型 |
| `firedancer_version` | — | `firedancer` 类型 |
| `yellowstone_grpc_version` | — | `Yellowstone gRPC` 插件 |
| `richat_version` | — | `Richat` 插件 |
| `of1_version` | — | `Index RPC（Old Faithful） |
| `epoch` | — | `Index RPC（faithful service） |
| `faithful_proxy_target_url` | — | `Index RPC` |

### 可选变量

| 变量 | 默认值 | 需要的条件 |
|---|---|---|
| `ssh_user` | `solv` | 总是需要 |
| `port_rpc` | `8899`（ERPC：`7211`） | 总是需要 |
| `limit_ledger_size` | `100000000` | 总是需要 |
| `dynamic_port_range` | `8000-8025` | 总是需要 |
| `port_grpc` | `10000` | 仅限 gRPC 类型 |
| `tpu_peer_address` | — | `Index RPC`（交易转发） |
| `allowed_ssh_ips` | — | 强烈推荐（用于 UFW） |
| `allowed_ips` | — | 可选（用于 UFW） |
| `expected_shred_version` | 依赖于 epoch | 仅限测试网 |

### 可选：参考 RPC

| 变量 | 描述 | 默认值 |
|---|---|---|
| `reference_rpc_url` | 用于槽同步比较的参考 RPC 端点（例如 ERPC） | — |

ERPC API 密钥可在 https://erpc.global 获取——在部署和更新过程中启用完整的槽同步监控。

### 部署前的准备工作：新服务器设置

```bash
ansible-playbook -i inventory.yml cmn/add_solv.yml \
  -e '{"ansible_user":"ubuntu"}' --become
```

### 部署命令

所有路径均相对于技能的 `ansible/` 目录：

```bash
cd /path/to/slv-rpc/ansible/
ansible-playbook -i inventory.yml {network}-rpc/init.yml \
  -e '{"rpc_type":"<type>","solana_version":"<version>"}'
```