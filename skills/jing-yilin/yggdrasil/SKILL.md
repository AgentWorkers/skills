---
name: yggdrasil-setup
description: 诊断并指导 Yggdrasil 的安装过程，以确保代理能够建立可全局路由的 IPv6 P2P 连接。
version: 0.1.0
metadata:
  openclaw:
    emoji: "🌐"
    homepage: https://github.com/ReScienceLab/claw-p2p
    install:
      - kind: node
        package: "@resciencelab/claw-p2p"
---
# Yggdrasil 设置技巧

Yggdrasil 为每个 OpenClaw 代理分配一个可通过全球网络路由的 `200::/8` IPv6 地址，该地址是根据其 Ed25519 密钥对生成的。如果没有 Yggdrasil，P2P 地址将仅限于本地使用，其他机器上的对等节点无法访问这些地址。

## 使用场景

| 情况 | 应采取的操作 |
|---|---|
| 用户询问 “P2P 功能是否正常？” 或 “我能否连接？” | 调用 `yggdrasil_check()` 并解释结果 |
| 用户首次询问 “我的地址是什么？” | 调用 `yggdrasil_check()` 以确认地址是否可路由 |
| `p2p_send_message` 失败 | 调用 `yggdrasil_check()` 进行故障排查 |
| 用户表示未安装 Yggdrasil | 指导用户进行安装（请参阅 `references/install.md`） |
| 用户询问 Yggdrasil 是什么 | 简要说明后，询问用户是否需要安装 |

## 解读 `yggdrasil_check` 的结果

| 地址类型 | 含义 | 应告知用户的提示 |
|---|---|---|
| `yggdrasil` | Yggdrasil 守护进程正在运行，地址可全球路由 | 准备就绪，可以与其他对等节点共享该地址。 |
| `test_mode` | 仅限本地或 Docker 环境使用 | 适用于在同一台机器/网络内进行测试，不适用于互联网对等节点。 |
| `derived_only` | Yggdrasil 未运行 | 地址无法被访问，请先安装 Yggdrasil。 |

## 安装完成后

告知用户：“请重启 OpenClaw 网关。插件会自动检测到 Yggdrasil 并启动守护进程——无需额外配置。”

然后再次调用 `yggdrasil_check()`，以确认守护进程已启动并显示实际的可路由地址。

具体平台的安装命令请参阅 `references/install.md`。