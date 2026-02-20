# ClawRTC

使用 Proof-of-Antiquity 共识机制，通过您的 AI 代理来挖掘 RTC（Real-Time Clock）代币。

## 功能概述

- **一键安装**：`pip install clawrtc && clawrtc install --wallet my-agent`
- **硬件验证**：通过 6 项加密检查来确认您的设备是真实的（时钟漂移、缓存延迟、SIMD 特性、热熵、指令执行抖动、反仿真机制）
- **自动认证**：每隔几分钟向 RustChain 网络发送认证信息
- **每个时代周期的奖励**：每个时代周期（约 10 分钟）中，RTC 代币会累积到您的钱包中
- **虚拟机检测**：能够检测到虚拟机，并且虚拟机几乎无法获得任何奖励

## 安全性

- **安装过程中无数据传输**：在安装过程中不会发送任何网络数据
- **启用 TLS 验证**：所有对 RustChain API 的调用都会验证 SSL 证书（由可信机构签名）
- **仅包含打包好的代码**：所有挖矿脚本都包含在软件包中，无需额外下载
- **需要用户同意**：安装前会显示交互式确认提示
- **试运行模式**：`clawrtc install --dry-run` 可以预览功能而无需实际安装
- **哈希验证**：`clawrtc install --verify` 可以显示所有打包文件的 SHA256 哈希值
- **彻底卸载**：`clawrtc uninstall` 会删除所有文件、服务及配置
- **默认不启动后台服务**：必须明确使用 `--service` 参数才能启用后台服务
- **源代码公开**：完整源代码可在 [https://github.com/Scottcjn/Rustchain](https://github.com/Scottcjn/Rustchain) 获取（MIT 许可）

### 发送的数据

在认证过程中（即挖矿时），以下数据会被发送到 RustChain 节点：

- CPU 型号和架构（例如：“AMD Ryzen 5”、“x86_64”）
- 时钟延迟信息（用于验证时钟的真实性）
- 缓存延迟数据（用于确认 L1/L2/L3 缓存层的存在）
- 虚拟机检测结果（判断是否存在虚拟机）
- 钱包名称（您选择的标识符）

**不会发送的数据**：文件内容、浏览历史记录、凭据、IP 地理位置、个人数据

## 安装方法

```bash
pip install clawrtc
```

## 使用方法

```bash
# 安装挖矿工具并配置钱包
clawrtc install --wallet my-agent

# 启动挖矿（前台运行）
clawrtc start

# 检查状态
clawrtc status

# 查看日志
clawrtc logs

# 停止挖矿
clawrtc stop

# 彻底卸载
clawrtc uninstall
```

## 奖励倍数

| 硬件类型 | 奖励倍数 |
|---------|---------|
| 现代 x86/ARM 架构 | 1.0x     |
| Apple Silicon (M1-M3) | 1.2x     |
| PowerPC G5    | 2.0x     |
| PowerPC G4    | 2.5x     |
| 虚拟机/模拟器 | 约 0x     （会被检测到并受到惩罚）

## Coinbase 钱包（v1.5.0）

```bash
# 创建 Coinbase Base 钱包
pip install clawrtc[coinbase]
clawrtc wallet coinbase create

# 查看钱包信息
clawrtc wallet coinbase show

# 链接现有 Base 地址
clawrtc wallet coinbase link 0xYourBaseAddress

# USDC 到 wRTC 的兑换指南
clawrtc wallet coinbase swap-info
```

**注意**：创建 Coinbase 钱包需要从 [portal.cdp.coinbase.com](https://portal.cdp.coinbase.com) 获取 CDP 凭据。无需凭据也可以手动链接钱包。

## 相关链接

- 源代码：https://github.com/Scottcjn/Rustchain
- PyPI：https://pypi.org/project/clawrtc/
- npm：https://www.npmjs.com/package/clawrtc
- 区块浏览器：https://rustchain.org/explorer
- 代理钱包：https://rustchain.org/wallets.html
- RustChain 官网：https://rustchain.org
- BoTTube：https://bottube.ai
```